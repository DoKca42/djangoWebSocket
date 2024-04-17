import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class RoomRequest:

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

    @staticmethod
    async def waitingMatch(room_group_name, status):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "waiting_match",
                "status": status
            }
        )

    @staticmethod
    async def foundMatch(room_group_name, match_id):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "found_match",
                "match_id": match_id
            }
        )

    @staticmethod
    async def createRoom(room_group_name, room_id, ia_game, player_nb):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "create_room",
                "room_id": room_id,
                "ia_game": ia_game,
                "player_nb": player_nb
            }
        )

    @staticmethod
    async def joinRoom(room_group_name, room_id, player_nb):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "join_room",
                "room_id": room_id,
                "player_nb": player_nb
            }
        )

    @staticmethod
    async def waitingTour(room_group_name, status):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            room_group_name,
            {
                "type": "sendToGroup",
                "rq_type": "waiting_tour",
                "status": status
            }
        )