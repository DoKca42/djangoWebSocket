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

    """
    SOCKET EVENT:
    """
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

    """
    AUTHENTIFY:
    
    Client need (valid auth)
    """
    async def clientAuth(self, session_id, player_id):
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

    """
    CREATE ROOM:
    
    Client need (valid auth / not be owner of other room / not in game)
    """
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

        await RoomRequest.createRoom(self.room_group_name, room_id, False, room_player_nb)
        self.client.setOwnerOfARoom(True)
        await self.clientJoinRoom(room_id, self.client.getPlayerId())

    """
    JOIN ROOM:
    
    Client need (valid auth / not in game / not already in this room)
    """
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
        await RoomRequest.joinRoom(self.room_group_name, room_id, room_player_nb)

    async def sendToGroup(self, event):
        event_data = event.copy()
        rq_type = event_data.pop('rq_type')
        event_data['type'] = str(rq_type)
        print(event_data)
        await self.send(text_data=json.dumps(event_data))
