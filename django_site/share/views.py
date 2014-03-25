from django.contrib.auth.decorators import permission_required
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_control

import mimetypes
import os.path

from share.settings import SHARE_ROOT


# Helpers
def get_physical_path(path):
    """
    Converts the path exracted from the URL to a physical path
    """
    # Security against URL attacks
    path = path.replace('..', '')
    
    return os.path.join(SHARE_ROOT, path)

def get_directory_node(directory_path):
    #TODO
    return None
    
def send_file(file_path):
    """
    Creates a HTTP response streaming the given file data.
    
    Tries to guess the MIME type from mimetypes built-in module.
    """
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    mime_type = mimetypes.guess_type(file_path)[0]
    
    # Let the garbage collector close the file,
    # otherwise the transfer gets corrupted
    fsock = open(file_path, 'rb')
    fwrapper = FileWrapper(fsock)
    
    # Builds HTTP response
    response = HttpResponse(fwrapper, content_type=mime_type)
    response['Content-Length'] = file_size
    response['Content-Disposition'] = (
        'attachment; filename={0}'
    ).format(file_name)
    return response


# Views
@permission_required('share.can_browse')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def browse(request, path):
    path = get_physical_path(path)
    if os.path.isdir(path):
        # Path is a directory: display child nodes
        current_directory = get_directory_node(path)
        return render(
            request,
            'share/browse.html',
            {'current_directory': current_directory}
        )
    elif os.path.isfile(path):
        # Path is a file: starts transfer
        return send_file(path)
    else:
        # Path does not exist: 404
        return Http404()
