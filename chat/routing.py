from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/rooms/", consumers.RoomConsumer.as_asgi()),
]
