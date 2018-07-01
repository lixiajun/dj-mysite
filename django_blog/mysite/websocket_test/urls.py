#coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^websocket/$', views.start_server_script, name="start_to_websocket"),
]