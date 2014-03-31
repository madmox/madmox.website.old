from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from madmox_website import settings
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
            file_name, file_size, mime_type = get_file_infos(path)
            
            # Builds HTTP response
            if settings.RUNNING_DEVSERVER:
                # In dev, let django upload the file itself
                fsock = open(path, 'rb')
                fwrapper = FileWrapper(fsock)
                response = HttpResponse(fwrapper, content_type=mime_type)
            else:
                # Apache mod-xsendfile intercepts the X-SendFile header and
                # processes the upload itself
                response = HttpResponse(content_type=mime_type)
                response['X-SendFile'] = path
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
