from django.conf.urls import patterns, url
from share import views


urlpatterns = patterns('',
    url(r'^browse/(?P<path>.*)$', views.browse, name='browse'),
)
