import json

from channels.generic.websocket import AsyncWebsocketConsumer
from language.Language import language
from room.ClientChannel import ClientChannel
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
        self.client = RoomClient()
        await self.client.addChannel(self, self.room_group_name)
        await RoomRequest.connection(self)

    async def disconnect(self, close_code):
        print("[ROOM] Leave connection")
        await self.client.leaveChannel(self, self.room_group_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "auth":
            await self.clientAuth(data["session_id"], data["player_id"])
            return
        if data["type"] == "matchmaking":
            await self.clientMatchmaking(data)
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
            await self.client.updateChannel(self)
            return

        if session_id != "":  # Auth API check
            self.client.setSessionId(session_id)
            self.client.setPlayerId(player_id)
            room_client_manager.addClient(self.client)
            return
        await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")

    """
    MATCHMAKING:

    Client need (valid auth / not in game)
    """
    async def clientMatchmaking(self, data):
        lang = self.client.getLang()
        if not self.client.isAValidSession():
            await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")
            return
        if self.client.getInGame():
            await RoomRequest.notification(self, "error",
                    language.get(lang, "notif.error.title"),
                    language.get(lang, "notif.error.already_in_game"))
            return
        if self.client.isInARoom():
            await RoomRequest.notification(self, "error",
                    language.get(lang, "notif.error.title"),
                    language.get(lang, "notif.error.already_waiting"))
            return
        if data["action"] == "find_game":
            await self.mm_findGame()
            return

    """
    FIND MATCH:
    
    Client need (depend on clientMatchmaking)
    """
    async def mm_findGame(self):
        waiting_room = room_manager.getWaitingRoom()

        if waiting_room is False:
            waiting_room = room_manager.createRoom()
            await self.clientJoinRoom(waiting_room, self.client.getPlayerId())
            await RoomRequest.waitingMatch(waiting_room, True)
            self.client.setInARoom(True)
        else:
            if await self.clientJoinRoom(waiting_room, self.client.getPlayerId()):
                room_manager.getRoomById(waiting_room).setGameStarted()
                await RoomRequest.foundMatch(waiting_room, waiting_room)
                await RoomRequest.waitingMatch(waiting_room, False)
                self.client.setInARoom(True)

    """
    JOIN ROOM:
    
    Client need (valid auth / not in game / not already in this room)
    """
    async def clientJoinRoom(self, room_id, player_id):
        lang = self.client.getLang()
        if not self.client.isAValidSession():
            await RoomRequest.notification(self, "error", "Fatal Error", "Login redirection")
            return False
        if self.client.getInGame():
            await RoomRequest.notification(self, "error",
                    language.get(lang, "notif.error.title"),
                    language.get(lang, "notif.error.in_game_join"))
            return False

        if room_manager.isRoomIdExist(room_id):
            room = room_manager.getRoomById(room_id)
            if not room.playerIdIsInRoom(player_id):
                room.addPlayer(player_id)
                await self.client.addChannel(self, room_id)
                return True
            else:
                await RoomRequest.notification(self, "error",
                    language.get(lang, "notif.error.title"),
                    language.get(lang, "notif.error.already_in_room"))
                return False

    async def sendToGroup(self, event):
        event_data = event.copy()
        rq_type = event_data.pop('rq_type')
        event_data['type'] = str(rq_type)
        print(event_data)
        await self.send(text_data=json.dumps(event_data))
