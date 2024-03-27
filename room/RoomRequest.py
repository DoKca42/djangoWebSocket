import json
from channels.layers import get_channel_layer


class RoomRequest:
    channel_layer = get_channel_layer()

    @staticmethod
    async def connection(obj):
        await obj.send(
            text_data=json.dumps({
                "type": "connection_etalished",
                "message": "Room Connected"
                }))

    @staticmethod
    async def notification(obj, category, title, message):
        await obj.send(
            text_data=json.dumps({
                "type": "notification",
                "category": category,
                "title": title,
                "message": message
            }))
