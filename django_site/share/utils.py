try:
    import magic
except ImportError:
    import mimetypes
import os.path
import re
import sys

from share.settings import SHARE_ROOT


# Classes
class DoesNotExist(Exception):
    pass
    
class IsNotFileOrDirectory(Exception):
    pass

class IsNotFile(Exception):
    pass

 
class FileSystemNode:
    """
    A mapping between a physical directory in the shared folder and metadata
    informations useful for template display.
    """
    
    def __init__(self, path, set_children=True):
        if not os.path.exists(path):
            raise DoesNotExist("The path {0} does not exist.".format(path))
        
        self.path = path
        self.isfile = os.path.isfile(path)
        self.isdir = os.path.isdir(path)
        if not (self.isfile or self.isdir):
            raise IsNotFileOrDirectory(
                "The path {0} is not a file or a directory.".format(path)
            )
        
        self.isroot = (path == SHARE_ROOT)
        if self.isroot:
            self.name = 'share'
        else:
            self.name = os.path.basename(path.rstrip('/\\'))
        self.local_path = self.build_local_path()
        self.url = self.build_url()
        self.parent_url = self.build_parent_url()
        self.size = self.get_size()
        self.children = self.get_children(set_children)
    
    def get_size(self):
        """
        Gets the folder or file total size (including sub dirs and files)
        """
        total_size = 0
        if self.isdir:
            for dirpath, dirnames, filenames in os.walk(self.path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        else:
            total_size = os.path.getsize(self.path)
            
        return total_size
        
    def get_children(self, set_children):
        child_dirs, child_files = [], []
        if self.isdir and set_children:
            for filename in sorted(os.listdir(self.path), key=str.lower):
                escaped_filename = filename.encode('utf8','surrogateescape').decode('utf8')
                abspath = os.path.join(self.path, escaped_filename)
                if os.path.isdir(abspath):
                    child_dirs.append(FileSystemNode(abspath, set_children=False))
                if os.path.isfile(abspath):
                    child_files.append(FileSystemNode(abspath, set_children=False))
        
        return child_dirs + child_files
    
    def build_local_path(self):
        # Removes share root part from path
        # We want users to see the share root as a virtual root
        local_path = '/' + re.sub(
            r'^{0}'.format(re.escape(SHARE_ROOT)),
            r'',
            self.path
        ).replace('\\', '/').lstrip('/')
        return local_path
    
    def build_url(self):
        # Removes share root part from path
        # We want users to see the share root as a virtual root
        relative_url = re.sub(
            r'^{0}'.format(re.escape(SHARE_ROOT)),
            r'',
            self.path
        ).replace('\\', '/').strip('/')
        if self.isdir:
            relative_url += '/'
        
        return relative_url

    def build_parent_url(self):
        if self.isroot:
            return None
        else:
            # Removes share root part from path
            # We want users to see the share root as a virtual root
            relative_url = re.sub(
                r'^{0}'.format(re.escape(SHARE_ROOT)),
                r'',
                self.path
            ).replace('\\', '/').strip('/')
            relative_url = '/'.join(relative_url.split('/')[0:-1])
            if relative_url != '':
                relative_url += '/'
            
            return relative_url


# Helpers
def get_mime_type(file_path):
    if 'magic' in sys.modules:
        return magic.from_file(file_path, mime=True).decode('utf-8')
    else:
        return mimetypes.guess_type(file_path)[0]

def get_physical_path(path):
    """
    Converts the path exracted from the URL to a physical path
    """
    # Security against URL attacks
    if ('..' in path or ':' in path or
        path.startswith('/') or path.startswith('\\')):
        return None, None, None
    
    if path != '':
        path = os.path.normpath(path.replace('\\', '/'))
    path = os.path.normpath(os.path.join(SHARE_ROOT, path))
    if os.path.exists(path):
        if os.path.isdir(path):
            path += os.path.normpath('/')
        return path, os.path.isdir(path), os.path.isfile(path)
    else:
        return None, None, None

def get_file_infos(file_path):
    """
    Creates an HTTP response to stream the given file.
    
    Tries to guess the MIME type from mimetypes built-in module.
    """
    
    if not os.path.exists(file_path):
        raise DoesNotExist("The path {0} does not exist.".format(file_path))
    if not os.path.isfile(file_path):
        raise IsNotFile(
            "The path {0} is not a file or a directory.".format(file_path)
        )
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    mime_type = get_mime_type(file_path) or 'application/octet-stream'
    
    return file_name, file_size, mime_type
