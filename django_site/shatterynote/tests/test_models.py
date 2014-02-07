from django.test import TestCase
from django.db import DatabaseError
from django.utils import timezone

import base64

from shatterynote.models import Secret
from shatterynote.helpers import generate_aes_key
from shatterynote.tests.common import flip_bits


class SecretTests(TestCase):

    def test_models_secret_is_secure_true(self):
        secret = Secret.objects.create_secret('passphrase', 'message')
        secret.save()
        self.assertTrue(secret.is_secure())
    
    def test_models_secret_is_secure_false(self):
        secret = Secret.objects.create_secret('', 'message')
        secret.save()
        self.assertFalse(secret.is_secure())
    
    def test_models_secret_expiration_date(self):
        secret = Secret.objects.create_secret('', 'message')
        secret.save()
        try:
            expires = secret.expiration_date()
        except Exception as e:
            self.fail("Failed to get expiration date: {0}".format(str(e)))
        self.assertGreater(expires, secret.created_at)
        
    def test_model_secret_decrypt_message_key_valid(self):
        secret = Secret.objects.create_secret('', 'message')
        aes_key = secret.aes_key
        secret.save()
        
        message = secret.decrypt_message(aes_key)
        self.assertEqual(message, 'message')
        
    def test_model_secret_decrypt_message_key_invalid(self):
        secret = Secret.objects.create_secret('', 'message')
        aes_key = secret.aes_key
        secret.save()
        
        aes_key = flip_bits(secret.aes_key)
        message = secret.decrypt_message(aes_key)
        self.assertNotEqual(message, 'message')

    def test_model_secret_decrypt_message_with_passphrase_secure(self):
        secret = Secret.objects.create_secret('passphrase', 'message')
        secret.save()
        self.assertTrue(secret.is_secure())
        
        secret.decrypt_message_with_passphrase()
        self.assertFalse(secret.is_secure())

    def test_model_secret_decrypt_message_with_passphrase_not_secure(self):
        secret = Secret.objects.create_secret('', 'message')
        secret.save()
        self.assertFalse(secret.is_secure())
        
        secret.decrypt_message_with_passphrase()
        self.assertFalse(secret.is_secure())

    def test_model_secret_is_passphrase_valid_valid(self):
        secret = Secret.objects.create_secret('passphrase', 'message')
        secret.save()
        self.assertTrue(secret.is_passphrase_valid('passphrase'))

    def test_model_secret_is_passphrase_valid_invalid(self):
        secret = Secret.objects.create_secret('passphrase', 'message')
        secret.save()
        self.assertFalse(secret.is_passphrase_valid('wrong_passphrase'))

    def test_model_secret_is_passphrase_valid_none(self):
        secret = Secret.objects.create_secret('', 'message')
        secret.save()
        self.assertTrue(secret.is_passphrase_valid('passphrase'))

    def test_model_secret_get_url_firstcall(self):
        # Creates secret
        secret = Secret.objects.create_secret('passphrase', 'message')
        secret.save()
        aes_key = secret.aes_key
        
        # Gets URL
        encrypted_data = secret.get_url_segment()
        self.assertIsNotNone(encrypted_data)
        secret_id, secret_key = Secret.objects.unpack_infos(encrypted_data)
        self.assertEqual(secret_id, secret.pk)
        self.assertEqual(secret_key, aes_key)
        self.assertIsNone(secret.aes_key)

    def test_model_secret_get_url_secondcall(self):
        # Creates secret
        secret = Secret.objects.create_secret('passphrase', 'message')
        secret.save()
        aes_key = secret.aes_key
        
        # Gets URL
        url_segment = secret.get_url_segment()
        url_segment = secret.get_url_segment()
        self.assertIsNone(url_segment)
        

class SecretManagerTests(TestCase):

    def test_models_secretmanager_create_without_passphrase(self):
        try:
            secret = Secret.objects.create_secret('', 'message')
            secret.save()
        except Exception as e:
            self.fail("Could not create secret: {0}".format(str(e)))
        
        self.assertIsNotNone(secret.encrypted_message)
        self.assertIsNone(secret.passphrase_hash)
        self.assertIsNotNone(secret.aes_key)

    def test_models_secretmanager_create_with_passphrase(self):
        try:
            secret = Secret.objects.create_secret('passphrase', 'message')
            secret.save()
        except Exception as e:
            self.fail("Could not create secret: {0}".format(str(e)))
        
        self.assertIsNotNone(secret.encrypted_message)
        self.assertIsNotNone(secret.passphrase_hash)
        self.assertIsNotNone(secret.aes_key)
    
    def test_models_secretmanager_purge_old(self):
        secret = Secret.objects.create_secret('', 'message')
        secret.created_at -= (
            timezone.timedelta(days=7) + timezone.timedelta(seconds=10)
        )
        secret.save()
        Secret.objects.purge()
        secrets = Secret.objects.all()
        self.assertEqual(len(secrets), 0)
    
    def test_models_secretmanager_purge_new(self):
        secret = Secret.objects.create_secret('', 'message')
        secret.created_at -= (
            timezone.timedelta(days=7) - timezone.timedelta(seconds=10)
        )
        secret.save()
        Secret.objects.purge()
        secrets = Secret.objects.all()
        self.assertEqual(len(secrets), 1)
    
    def test_models_secretmanager_pack_unpack_infos_valid(self):
        secret_id = 1
        secret_key = generate_aes_key(16)
        base64_data = Secret.objects.pack_infos(secret_id, secret_key)
        
        # Data should contain 68 bytes:
        # - 16 bytes for the AES-CTR nonce
        # - 4 bytes for the secret ID
        # - 16 bytes for the AES-128 key
        # - 16 bytes for the HMAC-MD5
        encrypted_data = base64.urlsafe_b64decode(base64_data)
        self.assertEqual(len(encrypted_data), (16+4+16+16))
        
        id, key = Secret.objects.unpack_infos(base64_data)
        
        # Should get the same data as input
        self.assertEqual(secret_id, id)
        self.assertEqual(secret_key, key)
    
    def test_models_secretmanager_pack_unpack_infos_invalid(self):
        secret_id = 1
        secret_key = generate_aes_key(16)
        encrypted_data = Secret.objects.pack_infos(secret_id, secret_key)
        encrypted_data = b'ABCD' + encrypted_data
        
        with self.assertRaises(ValueError):
            id, key = Secret.objects.unpack_infos(encrypted_data)
        
    def test_models_secretmanager_encrypt_decrypt_id_valid(self):
        secret_id = 1
        encrypted_id = Secret.objects.encrypt_id(secret_id)
        id = Secret.objects.decrypt_id(encrypted_id)
        
        self.assertEqual(secret_id, id)
    
    def test_models_secretmanager_encrypt_decrypt_id_invalid(self):
        secret_id = 1
        encrypted_id = Secret.objects.encrypt_id(secret_id)
        encrypted_id = b'ABCD' + encrypted_id
        
        with self.assertRaises(ValueError):
            id = Secret.objects.decrypt_id(encrypted_id)
    