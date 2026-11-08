import datetime
import json
from collections import defaultdict
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

active_users = defaultdict(dict) # we gonna use redis later

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated : 
            await self.close()
            return


        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_id']}"
        
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        active_users[self.room_name][self.user.id] = {
            "id": self.user.id,
            "username": self.user.username,
            "profile": self.user.profile.url,
        }
        await self.channel_layer.group_send(self.room_name , 
            {
                "type" : "user.joined",
                "message" : f"{self.user.username} joined the room.",
                "users" : list(active_users[self.room_name].values()),
            }
        )


        



    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        
        room_users = active_users.get(self.room_name , {})
        room_users.pop(self.user.id , None)

        if not room_users:
            active_users.pop(self.room_name , None)
        
        try : 
            await self.channel_layer.group_send(self.room_name , 
                {
                    "type" : "user.disconnect",
                    "message" : f"{self.user.username} disconnected from the room.",
                    "users" : list(room_users.values()),
                }
            )
        except Exception as e: 
            print(f"failed to broadcast the message maybe the room is closed... {e}")

    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_connected",
            "message": event["message"],
            "users": event["users"],
        }))

    async def user_disconnect(self, event):
        await self.send(text_data=json.dumps({
            "type" : "user_disconnected" , 
            "message": event["message"],
            "users": event["users"],
        }))

        
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

        await self.close(code=4004)

        

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