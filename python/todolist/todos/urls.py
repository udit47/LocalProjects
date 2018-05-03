from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^details/(?P<todo_id>\w{0,50})/$', views.details)
]
