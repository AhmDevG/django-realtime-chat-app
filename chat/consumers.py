import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated : 
            await self.close()
            return


        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_id']}"
        
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        
        await self.channel_layer.group_send(self.room_name , 
            {
                "type" : "user.joined",
                "message" : f"{self.user.username} joined the room.",
                "self_channel_name" : self.channel_name, 
            }
        )



    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.channel_layer.group_send(self.room_name , 
            {
                "type" : "user.disconnect",
                "message" : f"{self.user.username} disconnected from the room.",
            }
        )

    async def user_joined(self, event):
        # send to whole group except self
        if self.channel_name != event["self_channel_name"]:
            await self.send(text_data=json.dumps({
                "type" : "user_connected" , 
                "message": event["message"]
            }))

    async def user_disconnect(self, event):
        await self.send(text_data=json.dumps({
            "type" : "user_disconnected" , 
            "message": event["message"]
        }))

        

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
