import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class RoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated : 
            await self.close()
            return
        

        
        await self.channel_layer.group_add("rooms", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("rooms", self.channel_name)

    async def receive(self, text_data):
        pass

    async def room_created(self, event):
        room = event["room"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "room.created",
                    "room": room,
                }
            )
        )

    async def room_updated(self, event):
        room = event["room"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "room.updated",
                    "room": room,
                }
            )
        )

    async def room_deleted(self, event):
        room = event["room"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "room.deleted",
                    "room": room,
                }
            )
        )
