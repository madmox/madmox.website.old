from django.conf.urls import patterns, url
from share import views


urlpatterns = patterns('',
    url(r'^(?P<path>.*)$', views.browse, name='browse'),
)
