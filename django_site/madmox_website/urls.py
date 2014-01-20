from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Administration
    url(r'^admin/', include(admin.site.urls)),

    # Default page redirects to /about/
    url(r'^$', RedirectView.as_view(url='/about/')),

    # Custom applications
    url(r'^about/', include('about.urls', namespace='about')),
)
