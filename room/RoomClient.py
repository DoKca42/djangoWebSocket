from room.ClientChannel import ClientChannel
from room.RoomManager import room_manager
from room.RoomRequest import RoomRequest


class RoomClient:
    session_id = ""
    session_expired = 0
    player_id = ""
    in_a_room = False
    in_game = False
    in_a_room_tour = False
    in_game_tour = False
    lang = ""
    channels = []

    def __init__(self):
        self.session_id = ""
        self.session_expired = 0
        self. player_id = ""
        self.in_a_room = False
        self.in_game = False
        self.in_a_room_tour = False
        self.in_game_tour = False
        self.lang = "fr"
        self.channels = []

    # ======= SETTER =======

    def setSessionId(self, session_id):
        self.session_id = session_id

    def setSessionExpired(self, session_expired):
        self.session_expired = session_expired

    def setPlayerId(self, player_id):
        self.player_id = player_id

    def setInARoom(self, status):
        self.in_a_room = status

    def setInGame(self, status):
        self.in_game = status

    def setInARoomTour(self, status):
        self.in_a_room_tour = status

    def setInGameTour(self, status):
        self.in_game_tour = status

    def setLang(self, lang):
        self.lang = lang

    async def addChannel(self, obj, channel):
        self.channels.append(channel)
        await obj.channel_layer.group_add(channel, obj.channel_name)

    async def removeChannel(self, obj, channel):
        self.channels.remove(channel)
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    async def leaveChannel(self, obj, channel):
        await obj.channel_layer.group_discard(channel, obj.channel_name)

    # ======= GETTER =======

    def getSessionId(self):
        return self.session_id

    def getSessionExpired(self):
        return self.session_expired

    def getPlayerId(self):
        return self.player_id

    def isInARoom(self):
        return self.in_a_room

    def getInGame(self):
        return self.in_game

    def getInARoomTour(self):
        return self.in_a_room_tour

    def getInGameTour(self):
        return self.in_game_tour

    def getLang(self):
        return self.lang

    def getChannels(self):
        return self.channels

    # ======= OTHER =======

    def isAValidSession(self):
        if self.session_id != "":
            return True
        return False

    def printAll(self):
        print("Variables de RoomClient :")
        print(vars(self))
        pass

    async def updateChannel(self, obj):
        for channel in self.channels:
            await obj.channel_layer.group_discard(channel, obj.channel_name)
            await obj.channel_layer.group_add(channel, obj.channel_name)
            if room_manager.isRoomIdExist(channel) and room_manager.getRoomById(channel).isWaiting():
                await RoomRequest.waitingMatch(channel, True)

