from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from madmox_website import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Administration
    url(r'^admin/', include(admin.site.urls)),

    # Default page redirects to /about/
    url(r'^$', RedirectView.as_view(url='/about/')),

    # Custom applications
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^about/', include('about.urls', namespace='about')),
    url(r'^recipes/', include('recipes.urls', namespace='recipes')),
    url(r'^shatterynote/', include('shatterynote.urls', namespace='shatterynote')),
    url(r'^share/', include('share.urls', namespace='share')),
)

if settings.DEBUG:
    # Serve media files in DEBUG mode
    urlpatterns += patterns('',
        url(
            r'^{0}/(?P<path>.*)$'.format(settings.MEDIA_URL[1:-1]),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        )
    )
