from django.urls import path,re_path
from . import views

app_name = "music"

urlpatterns = [
    # /music/
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    # /music/
    re_path(r'^register/$', views.UserFormView.as_view(), name='register'),
    # /music/71/
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='detail'),
    # /music/album/add/
    re_path(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    # /music/album/2/
    re_path(r'album/(?P<pk>[0-9]+)/$', views.AlbumEdit.as_view(), name='album-update'),
    # /music/album/2/delete/
    re_path(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
]