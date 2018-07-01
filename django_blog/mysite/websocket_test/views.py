#coding=utf-8
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket


# Create your views here.
@accept_websocket
def start_server_script(request):
    if request.is_websocket():
        print('websocket 连接逻辑')
        for info in request.websocket:
            print(info)
            request.websocket.send('hello world')
    else:
        print(u'http 连接')
