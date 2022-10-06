from django.urls import re_path

from daily_app import consumers
# for authentication import the below module

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', consumers.GroupChatConsumer.as_asgi()),
    re_path(r'ws/send_message/', consumers.ChatMessageConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<username>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]