import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

from chat.RoomManager import room_manager


# https://circumeo.io/blog/entry/django-websockets/

class ChatConsumer(AsyncWebsocketConsumer):
    game_group_name = "game_group"
    update_lock = asyncio.Lock()

    async def connect(self):
        print("New connection")
        await self.accept()
        await self.channel_layer.group_add(
            self.game_group_name, self.channel_name
        )

        await self.send(
            text_data=json.dumps({
                "type": "connection_etalished",
                "message": "Connected"})
        )

        rooms = room_manager.get_rooms()
        for room in rooms:
            print(room.getId())
        # await asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        print("Leave connection")
        await self.channel_layer.group_discard(
            self.game_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        if text_data_json["type"] == "create_room":
            room_manager.create_room()
            return
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                "type": "chat_message",
                "message": text_data_json["message"]
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))


"""

    async def game_loop(self):
        async with self.update_lock:
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    "type": "chat_message",
                    "message": "nice"
                }
            )
            await asyncio.sleep(0.05)
"""
