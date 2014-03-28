from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from share.utils import (
    get_physical_path,
    FileSystemNode,
    get_file_infos
)


# Views
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def browse(request, path):
    if request.user.has_perm('share.can_browse'):
        path, isdir, isfile = get_physical_path(path)
        if isdir is True:
            # Path is a directory: display child nodes
            current_directory = FileSystemNode(path)
            return render(
                request,
                'share/browse.html',
                {
                    'authorized': True,
                    'current_directory': current_directory
                }
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
    elif not request.user.is_authenticated():
        url = '{0}?next={1}'.format(
            reverse('accounts:login'),
            reverse('share:browse', args=('',))
        )
        return HttpResponseRedirect(url)
    else:
        return render(
            request,
            'share/browse.html',
            {
                'authorized': False,
                'current_directory': None
            }
        )
