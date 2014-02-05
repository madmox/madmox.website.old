from django.test import TestCase

from shatterynote.models import Secret
from shatterynote.forms import NewSecretForm, SubmitPassphraseForm


class NewSecretFormTests(TestCase):
    def test_newsecretform_valid(self):
        """
        Asserts the form accepts a valid input
        """
        form = NewSecretForm(
            {'passphrase': 'passphrase', 'message': 'message'}
        )
        self.assertTrue(form.is_valid())
    
    def test_newsecretform_invalid_passphrase(self):
        """
        Asserts the form rejects an invalid passphrase
        """
        form = NewSecretForm(
            {'passphrase': 'X'*200, 'message': 'message'}
        )
        self.assertFalse(form.is_valid())
    
    def test_newsecretform_invalid_message(self):
        """
        Asserts the form rejects an invalid message
        """
        form = NewSecretForm(
            {'passphrase': 'passphrase', 'message': 'X'*6000}
        )
        self.assertFalse(form.is_valid())


class SubmitPassphraseFormTests(TestCase):
    def create_secret(self, passphrase, message):
        secret = Secret.objects.create_secret(passphrase, message)
        secret.save()
        return secret
        
    def test_submitpassphraseform_valid(self):
        """
        Asserts the form accepts a valid passphrase and de-secures the secret
        """
        secret = self.create_secret('passphrase', 'message')
        self.assertTrue(secret.is_secure())
        
        form = SubmitPassphraseForm(
            secret,
            {'passphrase': 'passphrase'}
        )
        self.assertTrue(form.is_valid())
        self.assertFalse(secret.is_secure())
        
    def test_submitpassphraseform_invalid(self):
        """
        Asserts the form rejects an invalid passphrase and does not
        de-secure the secret
        """
        secret = self.create_secret('passphrase', 'message')
        self.assertTrue(secret.is_secure())
        
        form = SubmitPassphraseForm(
            secret,
            {'passphrase': 'wrong_passphrase'}
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(secret.is_secure())
        
    def test_submitpassphraseform_secret_not_secure(self):
        """
        Asserts the form accepts any passphrase if the secret is not secure
        """
        secret = self.create_secret('', 'message')
        self.assertFalse(secret.is_secure())
        
        form = SubmitPassphraseForm(
            secret,
            {'passphrase': 'wrong_passphrase'}
        )
        self.assertTrue(form.is_valid())
        self.assertFalse(secret.is_secure())
