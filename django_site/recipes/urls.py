from django.conf.urls import patterns, url
from recipes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category, name='category'),
    url(r'^detail/(?P<slug>[\w-]+)/$', views.detail, name='detail'),
)
