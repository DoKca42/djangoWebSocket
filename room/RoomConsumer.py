import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from room.RoomManager import room_manager
from room.RoomClient import RoomClient
from room.RoomRequest import RoomRequest
from room.RoomClientManager import room_client_manager


class RoomConsumer(AsyncWebsocketConsumer):
    room_group_name = "room_lobby"
    client = None

    async def connect(self):
        print("[ROOM] New connection")
        await self.accept()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        self.client = RoomClient()
        await RoomRequest.connection(self)

    async def disconnect(self, close_code):
        print("[ROOM] Leave connection")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        if data["type"] == "auth":
            await self.clientAuth(data["session_id"], data["player_id"])
            return
        if data["type"] == "create_room":
            await self.clientCreateRoom()
            return
        if data["type"] == "join_room":
            await self.clientJoinRoom(data["room_id"], self.client.getPlayerId())
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

    async def clientAuth(self, session_id, player_id):
        self.client.printAll()
        room_client_manager.printAll()
        if self.client.isAValidSession():
            return

        if room_client_manager.isClientIdExist(session_id):
            self.client = room_client_manager.getClientById(session_id)
            return

        if session_id != "":  # Auth API check
            self.client.setSessionId(session_id)
            self.client.setPlayerId(player_id)
            room_client_manager.addClient(self.client)
            return
        await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")

    async def clientCreateRoom(self):
        if not self.client.isAValidSession():
            await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")
            return
        if self.client.getOwnerOfARoom():
            await RoomRequest.notification(self, "error", "Erreur", "Vous avez deja creer une room")
            return
        if self.client.getInGame():
            await RoomRequest.notification(self, "error", "Erreur", "Vous ne pouvez pas creer de room en partie")
            return
        room_id = room_manager.createRoom()
        room_player_nb = 0
        if room_manager.isRoomIdExist(room_id):
            room_player_nb = room_manager.getRoomById(room_id).getPlayerNb()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room_action",
                "room_id": room_id,
                "action": "add",
                "ia_game": "none",
                "player_nb": room_player_nb
            }
        )
        await self.clientJoinRoom(room_id, self.client.getPlayerId())

    async def clientJoinRoom(self, room_id, player_id):
        if not self.client.isAValidSession():
            await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")
            return
        if self.client.getInGame():
            await RoomRequest.notification(self, "error", "Erreur", "Vous ne pouvez pas rejoindre de room en partie")
            return
        room_player_nb = 0
        if room_manager.isRoomIdExist(room_id):
            room = room_manager.getRoomById(room_id)
            if not room.playerIdIsInRoom(player_id):
                room.addPlayer(player_id)
            else:
                await RoomRequest.notification(self, "error", "Erreur", "Vous etes deja dans la room")
                return
            room_player_nb = room.getPlayerNb()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "room_action",
                "room_id": room_id,
                "action": "player_join",
                "ia_game": "none",
                "player_nb": room_player_nb

            }
        )
