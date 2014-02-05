from django.test import TestCase

import base64

from shatterynote.helpers import (
    hash_passphrase,
    validate_passphrase,
    generate_aes_key,
    AESEncryptor
)


class HelpersTests(TestCase):
    def test_helpers_hash_passphrase(self):
        """
        Compares the result of hash_passphrase with a known
        valid SHA256 hash
        """
        # Hash value
        value = 'value to hash'
        salt = b'0123456789012345'
        hash = hash_passphrase(value, salt=salt)
        
        # Asserts output format
        self.assertIsInstance(hash, bytes)
        self.assertEqual(len(hash), len(salt) + 32)
        
        # Asserts validity
        true_hash = base64.standard_b64decode(
            'KnqrT+2/rH1U6fx0fZ2qpJz3xm8+tr1pFj75lFUtlIM='
        )
        self.assertEqual(hash[len(salt):], true_hash)
    
    def test_helpers_validate_passphrase_true(self):
        """
        Asserts the validate_passphrase returns True for a passphrase
        matching the hash
        """
        passphrase = 'value to hash'
        salt = b'0123456789012345'
        passphrase_hash = base64.standard_b64decode(
            'KnqrT+2/rH1U6fx0fZ2qpJz3xm8+tr1pFj75lFUtlIM='
        )
        
        self.assertTrue(
            validate_passphrase(passphrase, salt+passphrase_hash, len(salt))
        )
    
    def test_helpers_validate_passphrase_false(self):
        """
        Asserts the validate_passphrase returns False for a passphrase
        not matching the hash
        """
        passphrase = 'wrong value to hash'
        salt = b'0123456789012345'
        passphrase_hash = base64.standard_b64decode(
            'KnqrT+2/rH1U6fx0fZ2qpJz3xm8+tr1pFj75lFUtlIM='
        )
        
        self.assertFalse(
            validate_passphrase(passphrase, salt+passphrase_hash, len(salt))
        )
    
    def test_helpers_generate_aes_key_16(self):
        """
        Asserts the function generate_aes_key returns valid AES-128 keys
        """
        aes_key = generate_aes_key(16)
        self.assertIsInstance(aes_key, bytes)
        self.assertEqual(len(aes_key), 16)
    
    def test_helpers_generate_aes_key_24(self):
        """
        Asserts the function generate_aes_key returns valid AES-192 keys
        """
        aes_key = generate_aes_key(24)
        self.assertIsInstance(aes_key, bytes)
        self.assertEqual(len(aes_key), 24)
    
    def test_helpers_generate_aes_key_32(self):
        """
        Asserts the function generate_aes_key returns valid AES-256 keys
        """
        aes_key = generate_aes_key(32)
        self.assertIsInstance(aes_key, bytes)
        self.assertEqual(len(aes_key), 32)
    
    def test_helpers_generate_aes_key_invalid(self):
        """
        Asserts the function generate_aes_key raises an error if the
        length requested is invalid
        """
        with self.assertRaises(ValueError):
            aes_key = generate_aes_key(30)


class AESEncryptorTests(TestCase):
    def setUp(self):
        self.data = b'0123456789'
        self.aes_key = generate_aes_key(32)
        self.encryptor = AESEncryptor(self.aes_key)
    
    def test_helpers_aesencryptor_encrypt_bytes(self):
        """
        Ensures the function passes without error for a bytes input
        """
        try:
            ciphered = self.encryptor.encrypt(self.data)
        except Exception as e:
            self.fail("encrypt raised an error: {0}".format(str(e)))
        self.assertGreaterEqual(len(ciphered), self.encryptor.BLOCK_SIZE)

    def test_helpers_aesencryptor_encrypt_memoryview(self):
        """
        Ensures the function passes without error for a memoryview input
        """
        try:
            ciphered = self.encryptor.encrypt(memoryview(self.data))
        except Exception as e:
            self.fail("encrypt raised an error: {0}".format(str(e)))
        self.assertGreaterEqual(len(ciphered), self.encryptor.BLOCK_SIZE)

    def test_helpers_aesencryptor_decrypt_bytes(self):
        """
        Ensures the encryptor deciphers correctly a bytes input
        """
        ciphered = self.encryptor.encrypt(self.data)
        deciphered = self.encryptor.decrypt(ciphered)
        self.assertEqual(deciphered, self.data)

    def test_helpers_aesencryptor_decrypt_memoryview(self):
        """
        Ensures the encryptor deciphers correctly a memoryview input
        """
        ciphered = self.encryptor.encrypt(self.data)
        deciphered = self.encryptor.decrypt(memoryview(ciphered))
        self.assertEqual(deciphered, self.data)

    def test_helpers_aesencryptor_append_hmac_bytes(self):
        """
        Ensures the encryptor appends a correct HMAC to a bytes input
        """
        ciphered = b'X'
        try:
            ciphered_final = self.encryptor.append_hmac(ciphered)
        except Exception as e:
            self.fail(
                "Could not append HMAC to ciphered data: {0}".format(str(e))
            )
        
        self.assertEqual(len(ciphered_final), len(ciphered)+32)

    def test_helpers_aesencryptor_append_hmac_memoryview(self):
        """
        Ensures the encryptor appends a correct HMAC to a memoryview input
        """
        ciphered = memoryview(b'X')
        try:
            ciphered_final = self.encryptor.append_hmac(ciphered)
        except Exception as e:
            self.fail(
                "Could not append HMAC to ciphered data: {0}".format(str(e))
            )
        
        self.assertEqual(len(ciphered_final), len(ciphered)+32)

    def test_helpers_aesencryptor_validate_hmac_valid_bytes(self):
        """
        Ensures the validates correctly the HMAC of a bytes input
        """
        ciphered = b'X'
        ciphered_final = self.encryptor.append_hmac(ciphered)
        try:
            ciphered_validated = self.encryptor.validate_hmac(ciphered_final)
        except Exception as e:
            self.fail(
                "Could not validate HMAC of ciphered data: {0}".format(str(e))
            )
        
        self.assertEqual(ciphered, ciphered_validated)

    def test_helpers_aesencryptor_validate_hmac_valid_memoryview(self):
        """
        Ensures the validates correctly the HMAC of a bytes input
        """
        ciphered = memoryview(b'X')
        ciphered_final = self.encryptor.append_hmac(ciphered)
        try:
            ciphered_validated = self.encryptor.validate_hmac(ciphered_final)
        except Exception as e:
            self.fail(
                "Could not validate HMAC of ciphered data: {0}".format(str(e))
            )
        
        self.assertEqual(ciphered, ciphered_validated)

    def test_helpers_aesencryptor_validate_hmac_invalid_bytes(self):
        """
        Ensures the validates correctly the HMAC of a bytes input
        """
        ciphered = b'X'
        ciphered_final = self.encryptor.append_hmac(ciphered) + b'X'
        with self.assertRaises(ValueError):
            ciphered_validated = self.encryptor.validate_hmac(ciphered_final)

    def test_helpers_aesencryptor_validate_hmac_invalid_memoryview(self):
        """
        Ensures the validates correctly the HMAC of a bytes input
        """
        ciphered = memoryview(b'X')
        ciphered_final = self.encryptor.append_hmac(ciphered) + b'X'
        with self.assertRaises(ValueError):
            ciphered_validated = self.encryptor.validate_hmac(ciphered_final)
