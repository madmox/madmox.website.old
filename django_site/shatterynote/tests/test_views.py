from django.test import TestCase
from django.core.urlresolvers import reverse

from shatterynote.models import Secret


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
        self.assertIsNot(form, None)
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
        self.assertIs(secrets[0].passphrase_hash, None)
        
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
        self.assertIsNot(secrets[0].passphrase_hash, None)


class StatusViewTests(TestCase):
    def setUp(self):
        self.secret = Secret.objects.create_secret('passphrase', 'message')
        self.secret.save()
        self.secret_id = Secret.objects.encrypt_id(self.secret.id)
    
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
        self.assertIs(secret_url, None)
    
    def test_status_view_get_invalid(self):
        """
        Requests a status view on an invalid secret
        Should return a HTTP 404 status code
        """
        
        # Requests view
        self.secret_id = b'ABCD' + self.secret_id
        response = self.client.get(
            reverse('shatterynote:status', args=(self.secret_id,))
        )
        
        # Asserts conditions
        self.assertEqual(response.status_code, 404)


class SecretViewTests(TestCase):
    def create_secret(self, passphrase, message):
        # Initializes data
        self.secret = Secret.objects.create_secret(passphrase, message)
        self.secret.save()
        self.secret_id = Secret.objects.encrypt_id(self.secret.id)
        self.secret_url = self.secret.get_url()
        
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
        try:
            message = response.context['message']
            form = response.context['form']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIs(form, None)
        self.assertEqual(message, 'message')
        self.assertEqual(len(secrets), 0)
        
    def test_secret_view_get_secure(self):
        """
        Requests a secured secret. The secret view should return a
        form to type the passphrase, and not delete the secret.
        """
        
        # Initializes data
        self.create_secret('passphrase', 'message')
        self.assertTrue(self.secret.is_secure())
        
        # Requests
        response = self.client.get(self.secret_url)
        try:
            message = response.context['message']
            form = response.context['form']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIsNot(form, None)
        self.assertIs(message, None)
        self.assertEqual(len(secrets), 1)
        
    def test_secret_view_get_inexistant(self):
        """
        Requests an inexistant secret
        Should return an HTTP 404 status code
        """
        
        # Initializes data
        self.create_secret('', 'message')
        
        # Requests
        fake_url = self.secret_url.replace('/secret/', '/secret/ABCD')
        response = self.client.get(fake_url)
        
        # Assertions
        self.assertEqual(response.status_code, 404)
        
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
        try:
            message = response.context['message']
            form = response.context['form']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsInstance(response.redirect_chain, list)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.status_code, 200)
        self.assertIs(form, None)
        self.assertEqual(message, 'message')
        self.assertEqual(len(secrets), 0)
        
    def test_secret_view_post_secure_valid(self):
        """
        Submits a valid passphrase for a secret which is secure
        The secret view should redirect to the same page, in GET
        """
        
        # Initializes data
        self.create_secret('passphrase', 'message')
        self.assertTrue(self.secret.is_secure())
        
        # Requests
        response = self.client.post(
            self.secret_url,
            {'passphrase': 'passphrase'},
            follow=False
        )
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(secrets), 1)
        self.assertFalse(secrets[0].is_secure())
        
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
            follow=False
        )
        
        self.assertEqual(response.status_code, 200)
        
        try:
            form = response.context['form']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        secrets = Secret.objects.all()
        
        # Assertions
        self.assertIsNot(form, None)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(secrets), 1)
        
    def test_secret_view_post_inexistant(self):
        """
        Requests an inexistant secret
        Should return an HTTP 404 status code
        """
        
        # Initializes data
        self.create_secret('', 'message')
        
        # Requests
        fake_url = self.secret_url.replace('/secret/', '/secret/ABCD')
        response = self.client.post(
            fake_url,
            {'passphrase': 'passphrase'},
            follow=False
        )
        
        # Assertions
        self.assertEqual(response.status_code, 404)
