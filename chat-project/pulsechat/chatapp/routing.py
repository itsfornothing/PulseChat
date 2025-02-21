from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chatroom/(?P<g_name>[^/]+)/?$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<freind_email>[^/]+)/?$', ChatConsumer.as_asgi()),
    
]


