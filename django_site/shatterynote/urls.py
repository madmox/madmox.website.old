from django.conf.urls import patterns, url
from shatterynote import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^status/(?P<secret_id>(?:[-_A-Za-z0-9]{4})*(?:[-_A-Za-z0-9]{2}==|[-_A-Za-z0-9]{3}=)?)/$',
        views.status, name='status'),
    url(r'^secret/(?P<encrypted_data>(?:[-_A-Za-z0-9]{4})*(?:[-_A-Za-z0-9]{2}==|[-_A-Za-z0-9]{3}=)?)/$',
        views.secret, name='secret'),
)
