from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, Http404
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from share.utils import (
    get_physical_path,
    FileSystemNode,
    get_file_infos
)


# Views
@permission_required('share.can_browse')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def browse(request, path):
    path, isdir, isfile = get_physical_path(path)
    if isdir is True:
        # Path is a directory: display child nodes
        current_directory = FileSystemNode(path)
        return render(
            request,
            'share/browse.html',
            {'current_directory': current_directory}
        )
    elif isfile is True:
        # Path is a file: starts transfer
        fsock, file_name, file_size, mime_type = get_file_infos(path)
        fwrapper = FileWrapper(fsock)
        
        # Builds HTTP response
        response = HttpResponse(fwrapper, content_type=mime_type)
        response['Content-Length'] = file_size
        response['Content-Disposition'] = (
            'attachment; filename={0}'
        ).format(file_name)
    
        # Let the garbage collector close the file,
        # otherwise the transfer gets corrupted
        return response
    else:
        # Path does not exist: 404
        raise Http404()
