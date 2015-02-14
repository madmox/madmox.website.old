from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.http import urlquote

import os.path
import posixpath
from unittest import mock

from share.utils import (
    FileSystemNode,
    get_physical_path
)
from share.settings import SHARE_ROOT


class BaseTestCase(TestCase):

    def setUp(self):
        """Creates the test directory structure in the shared dir"""
        # Creates a directory
        self.dirname = posixpath.join(SHARE_ROOT, 'test_dir')
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
            
        # Creates a file
        self.fname = posixpath.join(self.dirname, 'test_file')
        if not os.path.exists(self.fname):
            with open(self.fname, 'w') as f:
                f.write('test content')
            
        # Creates an accentuated directory
        self.dirname_accent = posixpath.join(SHARE_ROOT, 'test_dir_é')
        if not os.path.exists(self.dirname_accent):
            os.makedirs(self.dirname_accent)
        
        # Creates an accentuated file in the accentuated dir
        self.fname_accent = posixpath.join(self.dirname_accent, 'test_file_é')
        if not os.path.exists(self.fname_accent):
            with open(self.fname_accent, 'w') as f:
                f.write('test content')
            
        # Creates an empty directory
        self.dirname_empty = posixpath.join(SHARE_ROOT, 'test_dir_empty')
        if not os.path.exists(self.dirname_empty):
            os.makedirs(self.dirname_empty)
        
    def tearDown(self):
        """Removes the test directory structure in the shared dir"""
        os.rmdir(self.dirname_empty)
        os.remove(self.fname_accent)
        os.rmdir(self.dirname_accent)
        os.remove(self.fname)
        os.rmdir(self.dirname)


class UtilsTests(BaseTestCase):

    def test_share_helpers_get_physical_path_invalid(self):
        """Asserts an invalid path is correctly detected by the method"""
        
        filepath = get_physical_path('invalid/path/')
        self.assertIsNone(filepath)
    
    def test_share_helpers_get_physical_path_dir(self):
        """Asserts a valid dir path is correctly formatted by the method"""
        
        filepath = get_physical_path('test_dir')
        expected_path = posixpath.normpath(
            posixpath.join(SHARE_ROOT, 'test_dir')
        )
        self.assertEqual(filepath, expected_path)

    def test_share_helpers_get_physical_path_dir_trailing_slash(self):
        """Asserts a valid dir path with a trailing slash is correctly
        formatted by the method"""
        
        filepath = get_physical_path('test_dir/')
        expected_path = posixpath.normpath(
            posixpath.join(SHARE_ROOT, 'test_dir')
        )
        self.assertEqual(filepath, expected_path)

    def test_share_helpers_get_physical_path_file(self):
        """Asserts an valid file path is correctly formatted by the method"""
        
        filepath = get_physical_path('test_dir/test_file')
        expected_path = posixpath.normpath(
            posixpath.join(SHARE_ROOT, 'test_dir/test_file')
        )
        self.assertEqual(filepath, expected_path)
    
    def test_share_helpers_filesystemnode_no_children(self):
        """Checks FileSystemNode() returns an empty node if the given path
        matches an empty directory"""
        
        node = FileSystemNode(self.dirname_empty)
        self.assertTrue(node.isdir)
        self.assertFalse(node.isfile)
        self.assertEqual(len(node.children), 0)
    
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
    
    def test_share_helpers_filesystemnode_dir_accent_and_child(self):
        """Checks FileSystemNode() does not raise any error when
        it has an accent in its name or in a child name"""
        
        node = FileSystemNode(self.dirname_accent)
        self.assertTrue(node.isdir)
        self.assertFalse(node.isfile)
        self.assertEqual(len(node.children), 1)
        
        subnode = node.children[0]
        self.assertFalse(subnode.isdir)
        self.assertTrue(subnode.isfile)
        self.assertEqual(subnode.children, [])
    
    def test_share_helpers_filesystemnode_file(self):
        """Checks FileSystemNode() returns an empty file node if the given
        path matches a valid file"""
        
        node = FileSystemNode(self.fname)
        self.assertFalse(node.isdir)
        self.assertTrue(node.isfile)
        self.assertEqual(node.children, [])


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
        """User is not authorized, the response must not
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
        sub directories and file infos"""
        
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
    
    def test_share_views_browse_root(self):
        """Path is the root directory, the response must be an HTML page
        containing sub directories and file infos"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('',))
        )
        self.assertEqual(response.status_code, 200)
        
        cur_dir = response.context['current_directory']
        self.assertIsNotNone(cur_dir)
        self.assertTrue(cur_dir.isroot)
        self.assertEqual(cur_dir.name, 'share')
        self.assertEqual(cur_dir.url, '')

    def test_share_views_browse_valid_dir_redirect(self):
        """Path is a valid dir, the response must be an HTML page containing
        sub directories and file infos"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('test_dir',)),
            follow=True
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.redirect_chain)
        
        cur_dir = response.context['current_directory']
        self.assertIsNotNone(cur_dir)
        self.assertEqual(cur_dir.name, 'test_dir')
        self.assertEqual(cur_dir.url, 'test_dir/')
    
    def test_share_views_browse_valid_dir_accent(self):
        """Path is a valid accentuated dir, the response must be an HTML page
        containing sub directories and file infos"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('test_dir_é/',))
        )
            
        self.assertEqual(response.status_code, 200)
        
        cur_dir = response.context['current_directory']
        self.assertIsNotNone(cur_dir)
        self.assertEqual(cur_dir.name, 'test_dir_é')
        self.assertEqual(cur_dir.url, 'test_dir_é/')
    
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
        self.assertIsNotNone(response['Content-Type'])
        self.assertFalse(response['Content-Type'].startswith('text/html'))
        self.assertEqual(response['X-SendFile'], urlquote(self.fname))

    def test_share_views_browse_valid_file_accent(self):
        """Path is a valid file, the response must be an HTTP response with
        the file's MIME type and content"""
        
        self.create_authorized_user()
        self.assertTrue(
            self.client.login(username='unittest1', password='unittest1')
        )
        
        response = self.client.get(
            reverse('share:browse', args=('test_dir_é/test_file_é',))
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response['Content-Type'])
        self.assertFalse(response['Content-Type'].startswith('text/html'))
        self.assertEqual(response['X-SendFile'], urlquote(self.fname_accent))
