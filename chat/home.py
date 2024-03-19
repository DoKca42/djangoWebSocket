import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from chat.RoomManager import room_manager


class HomeConsumer(AsyncWebsocketConsumer):
    home_group_name = "home"

    async def connect(self):
        print("[HOME] New connection")
        await self.accept()
        await self.channel_layer.group_add(
            self.home_group_name, self.channel_name
        )

        await self.send(
            text_data=json.dumps({
                "type": "connection_etalished",
                "message": "Home Connected"})
        )

    async def disconnect(self, close_code):
        print("[HOME] Leave connection")
        await self.channel_layer.group_discard(
            self.home_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("[HOME] "+text_data)
        if text_data_json["type"] == "create_room":
            room_id = room_manager.create_room()
            await self.channel_layer.group_send(
                self.home_group_name,
                {
                    "type": "room_action",
                    "room_id": room_id,
                    "action": "add"
                }
            )
            return
        if text_data_json["type"] == "join_room":
            await self.channel_layer.group_send(
                self.home_group_name,
                {
                    "type": "room_action",
                    "room_id": text_data_json["room_id"],
                    "action": "player_join"
                }
            )
            return

    async def room_action(self, event):
        room_id = event['room_id']
        action = event['action']

        await self.send(text_data=json.dumps({
            "type": "room_action",
            "room_id": room_id,
            "action": action
        }))
