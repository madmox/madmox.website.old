from django.conf.urls import patterns, url
from shatterynote import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^status/(?P<secret_id>[-_=A-Za-z0-9]+)/$',
        views.status, name='status'),
    url(r'^secret/(?P<encrypted_data>[-_=A-Za-z0-9]+)/$',
        views.secret, name='secret'),
)
