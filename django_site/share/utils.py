import os.path
import posixpath
import sys
try:
    import magic
except ImportError:
    import mimetypes

from share.settings import SHARE_ROOT


# Classes
class FileSystemNode:
    """
    A mapping between a physical directory in the shared folder and metadata
    informations useful for template display.
    """
    
    def __init__(self, path, set_children=True):
        self.path = path
        self.isfile = os.path.isfile(path)
        self.isdir = os.path.isdir(path)
        self.isroot = (path == SHARE_ROOT)
        if self.isroot:
            self.name = 'share'
            self.display_path = '/'
        else:
            self.name = os.path.basename(path)
            self.display_path = (
                posixpath.join('/', posixpath.relpath(path, start=SHARE_ROOT))
            )
        self.size = self.get_size()
        self.url = self.build_url()
        self.parent_url = self.build_parent_url()
        if self.isfile:
            self.mime_type = self.get_mime_type()
            self.children = []
        else:
            self.mime_type = None
            if set_children:
                self.children = self.get_children()
            else:
                self.children = []
    
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
        
    def build_url(self):
        relative_url = self.display_path.lstrip('/')
        # URL has trailing slash for directories
        if not self.isroot and self.isdir:
            relative_url += '/'
        return relative_url

    def build_parent_url(self):
        if self.isroot:
            return None
        else:
            relative_url = posixpath.dirname(self.display_path).lstrip('/')
            if relative_url != '':
                relative_url += '/'
            return relative_url

    def get_mime_type(self):
        if 'magic' in sys.modules:
            return magic.from_file(self.path, mime=True).decode('utf-8')
        else:
            return mimetypes.guess_type(self.path)[0]
        
    def get_children(self):
        child_dirs, child_files = [], []
        for child in sorted(os.listdir(self.path), key=str.lower):
            abspath = posixpath.join(self.path, child)
            if os.path.isdir(abspath):
                child_dirs.append(FileSystemNode(abspath, set_children=False))
            if os.path.isfile(abspath):
                child_files.append(FileSystemNode(abspath, set_children=False))
        
        return child_dirs + child_files
    

# Helpers
def get_physical_path(path):
    """
    Converts the path exracted from the URL to a physical path (if path exists)
    """
    
    # Clean up given path to only allow serving files below SHARE_ROOT
    path = posixpath.normpath(path).lstrip('/') # Normalize path Unix-style
    filepath = ''
    for segment in path.split('/'):
        if not segment:
            # Strip empty path components (usually if path is empty)
            continue
        # Remove drive segments on drive-enabled servers (Windows...)
        drive, segment = os.path.splitdrive(segment)
        # Remove possible backslashes in the segment on Windows-style systems
        head, segment = os.path.split(segment)
        # Strip remaining '.' and '..' in path
        if segment in (os.curdir, os.pardir):
            continue
        # Append segment to file path, posix-style
        filepath = posixpath.join(filepath, segment)
    filepath = posixpath.normpath(posixpath.join(SHARE_ROOT, filepath))
    
    if os.path.isdir(filepath) or os.path.isfile(filepath):
        return filepath
    else:
        return None
