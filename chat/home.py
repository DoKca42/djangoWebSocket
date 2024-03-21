import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from chat.RoomManager import room_manager


class HomeConsumer(AsyncWebsocketConsumer):
    home_group_name = "home"
    session_id = ""
    player_id = ""
    #client_id envoyer just apres la connexion pour envoyer des msg d'erreur juste a une personne

    async def connect(self):
        print("[HOME] New connection")
        await self.accept()
        await self.channel_layer.group_add(self.home_group_name, self.channel_name)

        await self.send(
            text_data=json.dumps({
                "type": "connection_etalished",
                "message": "Home Connected"})
        )

    async def disconnect(self, close_code):
        print("[HOME] Leave connection")
        await self.channel_layer.group_discard(self.home_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("[HOME] Received data :"+text_data)
        print("session_id = " + self.session_id)
        if text_data_json["type"] == "auth":
            #check si session valid
            self.session_id = text_data_json["session_id"]
            self.player_id = text_data_json["player_id"]
            await self.channel_layer.group_add(self.session_id, self.channel_name)
            return
        if text_data_json["type"] == "create_room":
            room_id = room_manager.createRoom()
            room_player_nb = 0
            if room_manager.isRoomIdExist(room_id):
                room_player_nb = room_manager.getRoomById(room_id).getPlayerNb()
            await self.channel_layer.group_send(
                self.home_group_name,
                {
                    "type": "room_action",
                    "room_id": room_id,
                    "action": "add",
                    "ia_game": "none",
                    "player_nb": room_player_nb
                }
            )
            return
        if text_data_json["type"] == "join_room":
            room_player_nb = 0
            if room_manager.isRoomIdExist(text_data_json["room_id"]):
                room = room_manager.getRoomById(text_data_json["room_id"])
                if not room.playerIdIsInRoom(text_data_json["player_id"]):
                    room.addPlayer(text_data_json["player_id"])  # check le retour et envoyer un msg d'erreur en ca de probleme
                else:
                    await self.channel_layer.group_send(
                        self.session_id,
                        {
                            "type": "notification",
                            "category": "error",
                            "title": "Erreur",
                            "message": "Vous etes deja dans la room"
                        }
                    )
                    return
                room_player_nb = room.getPlayerNb()
            await self.channel_layer.group_send(
                self.home_group_name,
                {
                    "type": "room_action",
                    "room_id": text_data_json["room_id"],
                    "action": "player_join",
                    "ia_game": "none",
                    "player_nb": room_player_nb

                }
            )
            return

    async def room_action(self, event):
        room_id = event['room_id']
        action = event['action']
        ia = event['ia_game']
        player_nb = event['player_nb']

        await self.send(text_data=json.dumps({
            "type": "room_action",
            "room_id": room_id,
            "action": action,
            "ia_game": ia,
            "player_nb": player_nb
        }))

    async def notification(self, event):
        category = event['category']
        title = event['title']
        message = event['message']

        await self.send(text_data=json.dumps({
            "type": "notification",
            "category": category,
            "title": title,
            "message": message
        }))