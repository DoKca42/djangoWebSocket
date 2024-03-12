import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


# https://circumeo.io/blog/entry/django-websockets/

class ChatConsumer(AsyncWebsocketConsumer):
    game_group_name = "game_group"

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

    async def disconnect(self, close_code):
        print("Leave connection")
        await self.channel_layer.group_discard(
            self.game_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
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
