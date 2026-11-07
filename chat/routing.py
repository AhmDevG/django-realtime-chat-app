from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/rooms/", consumers.RoomConsumer.as_asgi()),
    path("ws/room/<int:room_id>/", consumers.ChatConsumer.as_asgi()),
]
