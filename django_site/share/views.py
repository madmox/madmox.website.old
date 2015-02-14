from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    Http404
)
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.cache import cache_control

from madmox_website import settings
from share.utils import (
    FileSystemNode,
    get_physical_path
)


# Views
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def browse(request, path):
    if request.user.has_perm('share.can_browse'):
        # Convert URL path to physical path
        filepath = get_physical_path(path)
        
        # Path does not exist: 404
        if filepath is None:
            raise Http404()
        
        node = FileSystemNode(filepath)
        if node.isdir:
            # Path is a directory: display child nodes
            if (node.url != path):
                url = reverse('share:browse', args=(node.url,))
                return HttpResponsePermanentRedirect(url)
            else:
                return render(
                    request,
                    'share/browse.html',
                    {
                        'authorized': True,
                        'current_directory': node
                    }
                )
        else:
            if settings.RUNNING_DEVSERVER:
                # In dev, let django upload the file itself
                fsock = open(filepath, 'rb')
                fwrapper = FileWrapper(fsock)
                response = HttpResponse(fwrapper, content_type=node.mime_type)
            else:
                # Apache mod-xsendfile intercepts the X-SendFile header and
                # processes the upload itself
                response = HttpResponse(content_type=node.mime_type)
                response['X-SendFile'] = urlquote(filepath)
            response['Content-Disposition'] = (
                'attachment; filename="{0}"'
            ).format(node.name)
            
            # Dev: let the garbage collector close the file,
            # otherwise the transfer gets corrupted
            return response
    elif not request.user.is_authenticated():
        url = '{0}?next={1}'.format(
            reverse('accounts:login'),
            reverse('share:browse', args=(path,))
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
