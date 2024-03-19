from django.urls import re_path
from . import consumers, home

websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/home/', home.HomeConsumer.as_asgi())
]