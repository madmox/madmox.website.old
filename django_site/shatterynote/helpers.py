from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter


def hash_passphrase(passphrase, salt_size=16, salt=None):
    if salt is None:
        salt = get_random_bytes(salt_size)
    bytes_passphrase = passphrase.encode('utf8')
    h = SHA256.new()
    h.update(salt + bytes_passphrase)
    return salt + h.digest()


def validate_passphrase(passphrase, passphrase_hash, salt_size=16):

    # Python memoryview inconsistency arround the '+' operator:
    # b'x' + memoryview(b'x') is OK but memoryview(b'x') + b'x' is not...
    # See http://bugs.python.org/issue13298
    if isinstance(passphrase_hash, memoryview):
        passphrase_hash = bytes(passphrase_hash)
        
    salt = passphrase_hash[:salt_size]
    bytes_passphrase = passphrase.encode('utf8')
    h = SHA256.new()
    h.update(salt + bytes_passphrase)
    return h.digest() == passphrase_hash[salt_size:]


def generate_aes_key(size=32):
    if size not in [16, 24, 32]:
        raise ValueError("'size' must be 16, 24 or 32")
    return get_random_bytes(size)


class AESEncryptor:
    """
    Defines an AES 128/192/256 encrypter and decrypter (using CTR mode).
    
    The key is given when instanciating the object. A nonce is randomly
    created upon each encryption and is prepended to the output data for
    decryption.
    """
    
    # AES block size is 128 bits (= 16 bytes)
    BLOCK_SIZE = 16
    
    def __init__(self, key):
        """Initializes the instance and validates the key"""
        
        # PyCrypto 2.6.1 bugfix:
        # The API doesn't support memoryview objects,
        # have to cast it back to a bytes array
        if isinstance(key, memoryview):
            key = bytes(key)
        
        # AES key is either 128, 192 or 256 bits long
        if len(key) not in [16, 24, 32]:
            raise ValueError(
                "'key' length must be 16, 24 or 32. Got {0} instead.".format(
                    len(key)
                )
            )
        self.key = key
        
    def get_encryptor(self, nonce):
        ctr_value = int.from_bytes(nonce, byteorder='big')
        counter = Counter.new(128, initial_value=ctr_value)
        return AES.new(self.key, AES.MODE_CTR, counter=counter)
        
    def encrypt(self, raw_data):
        """Encrypts the given byte string and prepends a random nonce"""
        
        # PyCrypto 2.6.1 bugfix:
        # The API doesn't support memoryview objects,
        # have to cast it back to a bytes array
        if isinstance(raw_data, memoryview):
            raw_data = bytes(raw_data)
        
        nonce = get_random_bytes(self.BLOCK_SIZE)
        encryptor = self.get_encryptor(nonce)
        return nonce + encryptor.encrypt(raw_data)
        
    def decrypt(self, ciphered_data):
        """Decrypts the given byte string using the nonce included in it"""
        
        # PyCrypto 2.6.1 bugfix:
        # The API doesn't support memoryview objects,
        # have to cast it back to a bytes array
        if isinstance(ciphered_data, memoryview):
            ciphered_data = bytes(ciphered_data)
        
        if len(ciphered_data) < self.BLOCK_SIZE:
            raise ValueError(
                "'ciphered_data' length must be at least {0} bytes."
                " Got {0} instead.".format(
                    self.BLOCK_SIZE,
                    len(ciphered_data)
                )
            )
        nonce = ciphered_data[:self.BLOCK_SIZE]
        encryptor = self.get_encryptor(nonce)
        return encryptor.decrypt(ciphered_data[self.BLOCK_SIZE:])
    
    def append_hmac(self, ciphered_data):
        """
        Appends the HMAC-SHA256 at the end of ciphered_data with the
        internal encryptor's AES key
        """
        
        # Python memoryview inconsistency arround the '+' operator:
        # b'x' + memoryview(b'x') is OK but memoryview(b'x') + b'x' is not...
        # See http://bugs.python.org/issue13298
        if isinstance(ciphered_data, memoryview):
            ciphered_data = bytes(ciphered_data)
        
        h = HMAC.new(self.key, digestmod=SHA256)
        h.update(ciphered_data)
        return ciphered_data + h.digest()
    
    def validate_hmac(self, ciphered_data):
        """
        Validates the HMAC-SHA256 at the end of ciphered_data with the
        internal encryptor's AES key
        """
        if len(ciphered_data) < 32:
            raise ValueError("ciphered_data should contain at least 32 bytes")
        
        h = HMAC.new(self.key, digestmod=SHA256)
        h.update(ciphered_data[:-32])
        hmac = h.digest()
        if hmac != ciphered_data[-32:]:
            raise ValueError("HMAC is invalid, could not authenticate the data")
        
        return ciphered_data[:-32]
