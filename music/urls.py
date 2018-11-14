from django.contrib import admin
from django.urls import path
from . import views

from django.conf.urls import url, include   #older

app_name = 'music'



urlpatterns = [

    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /music/71/    -- don't forget the comma on the end of the line
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /music/album/add/
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
]

# url(r'^$', views.index, name='index'),
# url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),