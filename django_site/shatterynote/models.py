from django.db import models
from django.core.urlresolvers import reverse

import base64

from shatterynote import settings
from shatterynote.helpers import (
    AESEncryptor,
    generate_aes_key,
    hash_passphrase,
    validate_passphrase
)


class SecretManager(models.Manager):
    """
    Custom manager secrets
    """
    
    def create_secret(self, passphrase, message):
        """
        Initializes the secret with a random AES key (stored in the url)
        The key will be removed from database on first access
        to the '/status/<id>/' U.R.L., but we must store it to be able
        to display it at least one time.
        """
        
        # Initializes instance
        secret = self.create()
        
        # Encrypts the message using a random AES key
        secret.aes_key = generate_aes_key()
        encryptor = AESEncryptor(secret.aes_key)
        message_b = message.encode('utf8')
        secret.encrypted_message = encryptor.encrypt(message_b)
        
        # If passphrase is defined, stores it and encrypts the message one
        # more time
        if passphrase:
            secret.passphrase_hash = hash_passphrase(passphrase)
            # Discards salt
            encryptor2 = AESEncryptor(secret.passphrase_hash[-32:])
            secret.encrypted_message = encryptor2.encrypt(
                secret.encrypted_message
            )
        else:
            secret.passphrase_hash = None
        
        return secret
    
    def purge(self):
        from django.utils import timezone
        now = timezone.now()
        outdated = now - timezone.timedelta(days=7)
        outdated_secrets = self.get_queryset().filter(created_at__lt=outdated)
        outdated_secrets.delete()

    def unpack_infos(self, encrypted_data):
        # Builds AES decipherer
        encryptor = AESEncryptor(settings.AES_KEY)
        
        # Deciphers URL data
        raw_data = base64.urlsafe_b64decode(encrypted_data)
        raw_data = encryptor.validate_hmac(raw_data)
        clear_data = encryptor.decrypt(raw_data)
        secret_id = int.from_bytes(clear_data[:Secret.ID_SIZE], byteorder='big')
        secret_key = clear_data[Secret.ID_SIZE:]
        
        return secret_id, secret_key

    def pack_infos(self, secret_id, secret_key):
        # Builds AES cipherer
        encryptor = AESEncryptor(settings.AES_KEY)
        
        # Ciphers URL data
        bytes_id = int.to_bytes(secret_id, length=Secret.ID_SIZE, byteorder='big')
        clear_data = bytes_id + secret_key
        raw_data = encryptor.encrypt(clear_data)
        raw_data = encryptor.append_hmac(raw_data)
        encrypted_data = base64.urlsafe_b64encode(raw_data)
        
        return encrypted_data
    
    def encrypt_id(self, secret_id):
        """
        Returns an encrypted, base 64 encode ID, based on the given secret ID.
        The encryption is usefull to prevent bruteforce attacks on
        '/status/<id>/' urls to find unread secrets
        """
        if secret_id:
            bytes_id = int.to_bytes(
                secret_id, length=Secret.AUTO_ID_SIZE, byteorder='big'
            )
            encryptor = AESEncryptor(settings.AES_KEY)
            bytes_id = encryptor.encrypt(bytes_id)
            bytes_id = encryptor.append_hmac(bytes_id)
            base64_id = base64.urlsafe_b64encode(bytes_id)
            return base64_id
        else:
            return None
    
    def decrypt_id(self, base64_id):
        """
        Returns a secret ID, based on the given base 64 encoded encrypted
        representation of the ID.
        The encryption is usefull to prevent bruteforce attacks on
        '/status/<id>/' urls to find unread secrets
        """
        if base64_id:
            bytes_id = base64.urlsafe_b64decode(base64_id)
            encryptor = AESEncryptor(settings.AES_KEY)
            bytes_id = encryptor.validate_hmac(bytes_id)
            bytes_id = encryptor.decrypt(bytes_id)
            secret_id = int.from_bytes(
                bytes_id, byteorder='big'
            )
            return secret_id
        else:
            return None


class Secret(models.Model):
    """
    Secret class, defines all persistent informations and data wrapper for
    a secret
    """
    
    encrypted_message = models.BinaryField(null=True, blank=True)
    passphrase_hash = models.BinaryField(null=True, blank=True)
    aes_key = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Custom manager
    objects = SecretManager()
    
    # ID_SIZE is the size (in bytes) of the encrypted secret ID
    # So it includes the auto-id from database (4 bytes) as well as
    # the nonce used to encrypt it (= AES block size)
    AUTO_ID_SIZE = 4
    ID_SIZE = AUTO_ID_SIZE + AESEncryptor.BLOCK_SIZE
    
    def is_secure(self):
        """The secret is secure if it has a passphrase set"""
        return bool(self.passphrase_hash)
    
    def decrypt_message(self, key):
        encryptor = AESEncryptor(key)
        message_b = encryptor.decrypt(self.encrypted_message)
        try:
            message = message_b.decode('utf8')
        except UnicodeDecodeError:
            message = None
        return message
        
    def decrypt_message_with_passphrase(self):
        if self.is_secure():
            # self.passphrase_hash contains the AES-256 key prepended by a salt,
            # so we need to discard it
            encryptor = AESEncryptor(self.passphrase_hash[-32:])
            self.encrypted_message = encryptor.decrypt(self.encrypted_message)
            self.passphrase_hash = None
    
    def is_passphrase_valid(self, passphrase):
        if self.is_secure():
            return validate_passphrase(passphrase, self.passphrase_hash)
        else:
            return True
    
    def get_url(self):
        if self.aes_key:
            # Secret AES key is still stored in database, we can display it
            # to the user ; but we must clear it right after
            encrypted_data = Secret.objects.pack_infos(self.pk, self.aes_key)
            url = reverse('shatterynote:secret', args=(encrypted_data,))
            self.aes_key = None
            self.save()
        else:
            # Secret U.R.L. has already been displayed to the user
            url = None
        
        return url
