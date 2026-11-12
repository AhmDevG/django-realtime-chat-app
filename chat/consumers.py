import datetime
import json
from collections import defaultdict
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message, Room

active_users = defaultdict(dict) # we gonna use redis later

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if not self.user.is_authenticated :
            await self.close()
            return

        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_name = f"room_{self.room_id}"


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


    @database_sync_to_async
    def create_message(self, content , reply_message_id = None):

        reply_message = None
        if reply_message_id :
            reply_message = Message.objects.get(
                id=reply_message_id,
                room_id = self.room_id
            )


        message = Message.objects.create(
            message_author=self.user,
            room_id=self.room_id,
            message_content=content ,
            reply_to =  reply_message
        )

        return_message = {
            "id": message.id,
            "content": message.message_content,
            "author": {
                "username": message.message_author.username,
                "profile": message.message_author.profile.url,
                "user_id": message.message_author.id,
            } ,
            "reply_to" : None ,
        }

        if reply_message :
            return_message["reply_to"] =  {
                "id" : reply_message.id ,
                "content" : reply_message.message_content,
                "author" :  reply_message.message_author.username,
            }


        return return_message


    async def receive(self , text_data):
        data = json.loads(text_data)

        if data.get("type") == "message.created":
            content = data["message"]["content"].strip()
            reply_message_id = data["message"].get("reply_message_id")

            if not content :
                return

            message = await self.create_message(content , reply_message_id)
            await self.channel_layer.group_send(self.room_name , {
                "type" : "message.created",
                "message": message,
            })



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

    async def message_created(self , event):
        message = event["message"]
        await self.send(
            text_data = json.dumps({
                "type" : "message.created",
                "message" : message,
            })
        )



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
