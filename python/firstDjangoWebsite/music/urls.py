from django.urls import path,re_path
from . import views

app_name = "music"

urlpatterns = [
    # /music/
    path('', views.index, name='index'),

    # /music/71/
    re_path(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),

    # /music/71/favorite/
    re_path(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
]