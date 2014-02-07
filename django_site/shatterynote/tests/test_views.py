from django.test import TestCase
from django.core.urlresolvers import reverse

import base64

from shatterynote import settings
from shatterynote.helpers import AESEncryptor
from shatterynote.models import Secret
from shatterynote.views import unpad_base64_string, pad_base64_string
from shatterynote.tests.common import flip_bits


class IndexViewTests(TestCase):

    def test_index_view_get(self):
        """
        Tests the view returns a 200 HTTP code
        """
        response = self.client.get(reverse('shatterynote:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_post_invalid_data(self):
        """
        Invalid data should display an error message on the same page
        """
        long_message = 'X'*100000
        response = self.client.post(
            reverse('shatterynote:index'),
            {'message': long_message, 'passphrase': ''}
        )
        self.assertEqual(response.status_code, 200)
        try:
            form = response.context['form']
        except KeyError as ke:
            self.fail("Context does not contain key {0}".format(str(ke)))
        self.assertIsNotNone(form)
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_index_view_post_empty_passphrase(self):
        """
        Valid form data should create a new secret and redirect to status
        page
        """
        response = self.client.post(
            reverse('shatterynote:index'),
            {'message': 'message', 'passphrase': ''},
            follow=True
        )
        # Asserts HTTP conditions
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.redirect_chain)
        self.assertEqual(len(response.redirect_chain), 1)
        
        # Asserts model got created
        secrets = Secret.objects.all()
        self.assertEqual(len(secrets), 1)
        self.assertIsNone(secrets[0].passphrase_hash)
        
    def test_index_view_post_with_passphrase(self):
        """
        Valid form data should create a new secret and redirect to status
        page
        """
        response = self.client.post(
            reverse('shatterynote:index'),
            {'message': 'message', 'passphrase': 'passphrase'},
            follow=True
        )
        # Asserts HTTP conditions
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.redirect_chain)
        self.assertEqual(len(response.redirect_chain), 1)
        
        # Asserts model got created
        secrets = Secret.objects.all()
        self.assertEqual(len(secrets), 1)
        self.assertIsNotNone(secrets[0].passphrase_hash)


class StatusViewTests(TestCase):

    def setUp(self):
        self.secret = Secret.objects.create_secret('passphrase', 'message')
        self.secret.save()
        self.secret_id = Secret.objects.encrypt_id(self.secret.id)
        self.secret_id = unpad_base64_string(self.secret_id)
    
    def test_status_view_get_firsttime(self):
        """
        Gets a status view for the first time for this secret
        It should display the secret's U.R.L.
        """
        
        # Requests view
        response = self.client.get(
            reverse('shatterynote:status', args=(self.secret_id,))
        )
        
        # Asserts conditions
        self.assertEqual(response.status_code, 200)
        try:
            secret = response.context['secret']
            secret_url = response.context['secret_url']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertIsNotNone(secret)
        self.assertIsNone(secret.aes_key)
        self.assertRegex(secret_url, '/shatterynote/secret/')
    
    def test_status_view_get_secondtime(self):
        """
        Gets a status view for the second time for this secret
        It should not display the secret's U.R.L.
        """
        
        # Requests view
        response = self.client.get(
            reverse('shatterynote:status', args=(self.secret_id,))
        )
        response = self.client.get(
            reverse('shatterynote:status', args=(self.secret_id,))
        )
        
        # Asserts conditions
        self.assertEqual(response.status_code, 200)
        try:
            secret = response.context['secret']
            secret_url = response.context['secret_url']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertIsNotNone(secret)
        self.assertIsNone(secret.aes_key)
        self.assertIsNone(secret_url)
    
    def test_status_view_get_invalid(self):
        """
        Requests a status view on an invalid secret
        Should return a context without secret
        """
        
        # Requests view
        self.secret_id = b'ABCD' + self.secret_id
        response = self.client.get(
            reverse('shatterynote:status', args=(self.secret_id,))
        )
        
        # Asserts conditions
        self.assertEqual(response.status_code, 200)
        try:
            secret = response.context['secret']
            secret_url = response.context['secret_url']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertIsNone(secret)
        self.assertIsNone(secret_url)
    
    def test_status_view_get_fake_id(self):
        """
        Requests the view with a forged valid HMAC but invalid data, and
        asserts the view returns a context without secret
        """
        
        # Requests view
        fake_id = self.secret.pk + 1
        encrypted_data = Secret.objects.encrypt_id(fake_id)
        url_segment = unpad_base64_string(encrypted_data)
        response = response = self.client.get(
            reverse('shatterynote:status', args=(url_segment,))
        )
        
        # Asserts conditions
        self.assertEqual(response.status_code, 200)
        try:
            secret = response.context['secret']
            secret_url = response.context['secret_url']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertIsNone(secret)
        self.assertIsNone(secret_url)

    def test_status_view_get_fake_invalid_format(self):
        """
        Requests the view with a forged valid HMAC but invalid data, and
        asserts the view returns a context without secret
        """
        
        # Requests view
        invalid_data = b'\x00'
        encryptor = AESEncryptor(settings.AES_KEY)
        encrypted_data = encryptor.encrypt(invalid_data)
        encrypted_data = encryptor.append_hmac(encrypted_data)
        base64_id = base64.urlsafe_b64encode(encrypted_data)
        url_segment = unpad_base64_string(base64_id)
        response = response = self.client.get(
            reverse('shatterynote:status', args=(url_segment,))
        )
        
        # Asserts conditions
        self.assertEqual(response.status_code, 200)
        try:
            secret = response.context['secret']
            secret_url = response.context['secret_url']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertIsNone(secret)
        self.assertIsNone(secret_url)


class SecretViewTests(TestCase):

    def create_secret(self, passphrase, message):
        # Initializes data
        self.secret = Secret.objects.create_secret(passphrase, message)
        self.secret.save()
        self.secret_id = Secret.objects.encrypt_id(self.secret.id)
        url_segment = self.secret.get_url_segment()
        url_segment = unpad_base64_string(url_segment)
        if url_segment:
            self.secret_url = reverse('shatterynote:secret', args=(url_segment,))
        else:
            self.secret_url = None
    
    def get_context_params(self, context):
        try:
            message = context['message']
            form = context['form']
            found = context['found']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        return (message, form, found)
        
    def test_secret_view_get_not_secure(self):
        """
        Basic case, the secret view should return the secret info
        and delete the secret afterwards
        """
        
        # Initializes data
        self.create_secret('', 'message')
        self.assertFalse(self.secret.is_secure())
        
        # Requests
        response = self.client.get(self.secret_url)
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsNone(form)
        self.assertEqual(message, 'message')
        self.assertTrue(found)
        self.assertEqual(len(secrets), 0)
        
    def test_secret_view_get_secure(self):
        """
        Requests a secured secret. The secret view should return a
        form to type the passphrase, and sould not delete the secret.
        """
        
        # Initializes data
        self.create_secret('passphrase', 'message')
        self.assertTrue(self.secret.is_secure())
        
        # Requests
        response = self.client.get(self.secret_url)
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsNotNone(form)
        self.assertIsNone(message)
        self.assertTrue(found)
        self.assertEqual(len(secrets), 1)
        
    def test_secret_view_get_inexistant(self):
        """
        Requests an inexistant secret / invalid URL
        Should not return any info about any secret, and should not
        delete/modify any existing secret
        """
        
        # Initializes data
        self.create_secret('', 'message')
        
        # Requests
        fake_url = self.secret_url.replace('/secret/', '/secret/ABCD')
        response = self.client.get(fake_url)
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsNone(form)
        self.assertIsNone(message)
        self.assertFalse(found)
        self.assertEqual(len(secrets), 1)
        
    def test_secret_view_get_fake_id(self):
        """
        Requests the view with a forged valid HMAC but invalid secret ID, and
        asserts the view returns a context with found=False
        """
        
        # Initializes data
        secret = Secret.objects.create_secret('', 'message')
        secret.save()
        fake_id = secret.pk + 1
        encrypted_data = Secret.objects.pack_infos(fake_id, secret.aes_key)
        url_segment = unpad_base64_string(encrypted_data)
        fake_url = reverse('shatterynote:secret', args=(url_segment,))
        
        # Requests
        response = self.client.get(fake_url)
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        
        # Assertions
        self.assertFalse(found)
        self.assertIsNone(message)
        self.assertIsNone(form)

    def test_secret_view_get_fake_aes_key(self):
        """
        Requests the view with a forged valid HMAC but invalid AES key, and
        asserts the view returns a context without message or wrong message
        """
        
        # Initializes data
        secret = Secret.objects.create_secret('', 'message')
        secret.save()
        fake_aes_key = flip_bits(secret.aes_key)
        encrypted_data = Secret.objects.pack_infos(secret.pk, fake_aes_key)
        url_segment = unpad_base64_string(encrypted_data)
        fake_url = reverse('shatterynote:secret', args=(url_segment,))
        
        # Requests
        response = self.client.get(fake_url)
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        
        # Assertions
        self.assertTrue(found)
        self.assertNotEqual(message, 'message')
        self.assertIsNone(form)

    def test_secret_view_get_fake_invalid_format(self):
        """
        Requests the view with a forged valid HMAC but invalid data format, and
        asserts the view returns a context with found=False
        """
        
        # Initializes data
        invalid_data = b'\x00'
        encryptor = AESEncryptor(settings.AES_KEY)
        encrypted_data = encryptor.encrypt(invalid_data)
        encrypted_data = encryptor.append_hmac(encrypted_data)
        base64_id = base64.urlsafe_b64encode(encrypted_data)
        url_segment = unpad_base64_string(base64_id)
        fake_url = reverse('shatterynote:secret', args=(url_segment,))
        
        # Requests
        response = self.client.get(fake_url)
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        
        # Assertions
        self.assertFalse(found)
        self.assertIsNone(message)
        self.assertIsNone(form)


    def test_secret_view_post_not_secure(self):
        """
        Submits a passphrase for a secret which is not secure
        The secret view should redirect to the same page, in GET
        """
        
        # Initializes data
        self.create_secret('', 'message')
        self.assertFalse(self.secret.is_secure())
        
        # Requests
        response = self.client.post(
            self.secret_url,
            {'passphrase': 'passphrase'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsInstance(response.redirect_chain, list)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertIsNone(form)
        self.assertTrue(found)
        self.assertEqual(message, 'message')
        self.assertEqual(len(secrets), 0)
        
    def test_secret_view_post_secure_valid(self):
        """
        Submits a valid passphrase for a secret which is secure
        The secret view should redirect to the same page, in GET,
        and the secret message should be displayed
        """
        
        # Initializes data
        self.create_secret('passphrase', 'message')
        self.assertTrue(self.secret.is_secure())
        
        # Requests
        response = self.client.post(
            self.secret_url,
            {'passphrase': 'passphrase'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsInstance(response.redirect_chain, list)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertIsNone(form)
        self.assertTrue(found)
        self.assertEqual(message, 'message')
        self.assertEqual(len(secrets), 0)
        
    def test_secret_view_post_secure_invalid(self):
        """
        Submits an invalid passphrase for a secret which is secure
        The secret view should render the same page, with validation errors
        """
        
        # Initializes data
        self.create_secret('passphrase', 'message')
        self.assertTrue(self.secret.is_secure())
        
        # Requests
        response = self.client.post(
            self.secret_url,
            {'passphrase': 'wrong_passphrase'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsNone(message)
        self.assertIsNotNone(form)
        self.assertTrue(found)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(secrets), 1)

    def test_secret_view_post_inexistant(self):
        """
        Requests an inexistant secret
        Should not return any info about any secret, and should not
        delete/modify any existing secret
        """
        
        # Initializes data
        self.create_secret('', 'message')
        
        # Requests
        fake_url = self.secret_url.replace('/secret/', '/secret/ABCD')
        response = self.client.post(
            fake_url,
            {'passphrase': 'passphrase'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        message, form, found = self.get_context_params(response.context)
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsNone(message)
        self.assertIsNone(form)
        self.assertFalse(found)
        self.assertEqual(len(secrets), 1)
