from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

import os
from unittest import mock

from share.utils import (
    get_physical_path,
    FileSystemNode,
    get_file_infos,
    DoesNotExist,
    IsNotFile
)
from share.settings import SHARE_ROOT


class BaseTestCase(TestCase):

    def setUp(self):
        """Creates the test directory structure in the shared dir"""
        # Creates a directory
        self.dirname = os.path.join(SHARE_ROOT, 'test_dir')
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        
        # Creates a file
        self.fname = os.path.join(self.dirname, 'test_file')
        if not os.path.exists(self.fname):
            with open(self.fname, 'w') as f:
                f.write('test content')
            
        # Creates an empty directory
        self.dirname_empty = os.path.join(SHARE_ROOT, 'test_dir_empty')
        if not os.path.exists(self.dirname_empty):
            os.makedirs(self.dirname_empty)
        
    def tearDown(self):
        """Removes the test directory structure in the shared dir"""
        os.rmdir(self.dirname_empty)
        os.remove(self.fname)
        os.rmdir(self.dirname)


class UtilsTests(BaseTestCase):

    def test_share_helpers_get_physical_path_invalid(self):
        """Asserts an invalid path is correctly detected by the method"""
        path, isdir, isfile = get_physical_path('invalid_path')
        self.assertIsNone(path)
        self.assertIsNone(isdir)
        self.assertIsNone(isfile)

    def test_share_helpers_get_physical_path_dir(self):
        """Asserts an valid dir path is correctly detected by the method"""
        path, isdir, isfile = get_physical_path('test_dir')
        self.assertTrue(path)
        self.assertTrue(isdir)
        self.assertFalse(isfile)

    def test_share_helpers_get_physical_path_file(self):
        """Asserts an valid file path is correctly detected by the method"""
        path, isdir, isfile = get_physical_path('test_dir/test_file')
        self.assertTrue(os.path.exists(path))
        self.assertFalse(isdir)
        self.assertTrue(isfile)
    
    def test_share_helpers_filesystemnode_does_not_exist(self):
        """Checks FileSystemNode() raises an error if the given path
        does not exist"""
        
        with self.assertRaises(DoesNotExist):
            node = FileSystemNode('/wrong_path/')
    
    def test_share_helpers_filesystemnode_no_children(self):
        """Checks FileSystemNode() returns an empty node if the given path
        matches an empty directory"""
        
        node = FileSystemNode(self.dirname_empty)
        self.assertTrue(node.isdir)
        self.assertFalse(node.isfile)
        self.assertEqual(node.children, [])
    
    def test_share_helpers_filesystemnode_dir_child(self):
        """Checks FileSystemNode() returns a list of valid nodes if the
        path matches a directory containing another node, and checks
        the child is a valid node"""
        
        node = FileSystemNode(self.dirname)
        self.assertTrue(node.isdir)
        self.assertFalse(node.isfile)
        self.assertEqual(len(node.children), 1)
        
        subnode = node.children[0]
        self.assertFalse(subnode.isdir)
        self.assertTrue(subnode.isfile)
        self.assertEqual(subnode.children, [])
        
    def test_share_helpers_get_file_infos_does_not_exist(self):
        """Checks get_file_infos raises an error if the given path does not
        match a valid file"""
        
        with self.assertRaises(DoesNotExist):
            fsock, file_name, file_size, mime_type = get_file_infos('/wrong_path/')
    
    def test_share_helpers_get_file_infos_is_a_directory(self):
        """Checks get_file_infos raises an error if the given path matches
        a valid directory"""
        
        with self.assertRaises(IsNotFile):
            fsock, file_name, file_size, mime_type = get_file_infos(self.dirname)
    
    def test_share_helpers_get_file_infos_valid_text_file(self):
        """Checks get_file_infos returns correct informations and does not
        raise any errors if the given path matches a valid file"""
        
        fsock, file_name, file_size, mime_type = get_file_infos(self.fname)
        self.assertIsNotNone(fsock)
        self.assertEqual(file_name, 'test_file')
        self.assertGreater(file_size, 0)
        self.assertIsNotNone(mime_type)
        self.assertNotEqual(mime_type, '')


class ViewsTests(BaseTestCase):
    
    def create_authorized_user(self):
        # Authorized user
        User = get_user_model()
        content_type = ContentType.objects.get(
            app_label='share',
            model=''
        )
        permission = Permission.objects.get(
            codename='can_browse',
            content_type=content_type
        )
        
        authorized_user = User.objects.create_user(
            username='unittest1',
            email='unittest1@yopmail.com',
            password='unittest1'
        )
        authorized_user.user_permissions.add(permission)
        authorized_user.save()
        
    def create_unauthorized_user(self):
        # Unauthorized user
        User = get_user_model()
        unauthorized_user = User.objects.create_user(
            username='unittest2',
            email='unittest2@yopmail.com',
            password='unittest2'
        )
        
    def test_share_views_browse_anonymous_user(self):
        """User is anonymous, the response must be a redirect to the login
        page"""
        
        response = self.client.get(
            reverse('share:browse', args=('',))
        )
        self.assertRedirects(
            response,
            '{0}?next={1}'.format(
                reverse('accounts:login'),
                reverse('share:browse', args=('',))
            )
        )
        
    def test_share_views_browse_unauthorized_user(self):
        """User has not the permission for browsing, the response must not
        contain the share directory"""
        
        self.create_unauthorized_user()
        
        self.assertTrue(
            self.client.login(username='unittest2', password='unittest2')
        )
        response = self.client.get(
            reverse('share:browse', args=('',))
        )
        self.assertEqual(response.status_code, 200)
        cur_dir = response.context['current_directory']
        authorized = response.context['authorized']
        self.assertIsNone(cur_dir)
        self.assertFalse(authorized)
        
    def test_share_views_browse_login(self):
        """Tests the authorized user has access to the page"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('',))
        )
        self.assertEqual(response.status_code, 200)
        cur_dir = response.context['current_directory']
        authorized = response.context['authorized']
        self.assertIsNotNone(cur_dir)
        self.assertTrue(authorized)
    
    def test_share_views_browse_invalid_path(self):
        """Path is invalid, the response must be an HTTP 404 code"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('wrong_path/',))
        )
        self.assertEqual(response.status_code, 404)
    
    def test_share_views_browse_valid_dir(self):
        """Path is a valid dir, the response must be an HTML page containing
        sub directories and files infos"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('test_dir/',))
        )
            
        self.assertEqual(response.status_code, 200)
        
        cur_dir = response.context['current_directory']
        self.assertIsNotNone(cur_dir)
        self.assertEqual(cur_dir.name, 'test_dir')
        self.assertEqual(cur_dir.url, 'test_dir/')
    
    def test_share_views_browse_valid_file(self):
        """Path is a valid file, the response must be an HTTP response with
        the file's MIME type and content"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('test_dir/test_file',))
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response['Content-Type'].lower().startswith('text/html'))
