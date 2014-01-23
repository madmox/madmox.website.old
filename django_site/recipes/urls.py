from django.conf.urls import patterns, url
from recipes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_id>\d+)/$', views.category, name='category'),
    url(r'^detail/(?P<recipe_id>\d+)/$', views.detail, name='detail'),
)
