from room.Room import Room
from room.RoomClientManager import room_client_manager
import uuid
import time

from room.UniqId import Uniqid


class Tournament:
    id = 0
    created_date = 0
    demi_room_a = None
    demi_room_b = None
    final_room = None
    players = []
    status = 0          # 0: waiting | 1: tournament start | 2: end demi | 3: end final

    def __init__(self):
        self.id = Uniqid.generate()
        self.created_date = int(time.time())

        self.demi_room_a = Room()
        self.demi_room_b = Room()
        self.final_room = Room()
        self.players = []
        self.status = 0
        pass

    def __upStatus(self):
        self.status += 1

    def startTournament(self):
        self.__upStatus()
        self.demi_room_a.addPlayer(self.players[0])
        self.demi_room_a.addPlayer(self.players[1])
        self.demi_room_b.addPlayer(self.players[2])
        self.demi_room_b.addPlayer(self.players[3])
        self.setAllPlayersInGameStatus(True)
        pass

    # ======= SETTER =======

    def addPlayer(self, player_id):
        if self.getPlayerNb() < 4:
            self.players.append(player_id)
            return True
        return False

    def removePlayer(self, player_id):
        if self.status != 0:
            return False
        if self.playerIsInTournament(player_id):
            self.players.remove(player_id)
            return True
        return False

    def setAllPlayersInGameStatus(self, status):
        for player in self.players:
            room_client_manager.getClientById(player).setInGameTour(status)

    # ======= GETTER =======

    def getId(self):
        return self.id

    def getCreatedDate(self):
        return self.created_date

    def getPlayerNb(self):
        return len(self.players)

    def getDemiRoomA(self):
        return self.demi_room_a

    def getDemiRoomB(self):
        return self.demi_room_b

    def getFinalRoom(self):
        return self.final_room

    def playerIsInTournament(self, player_id):
        if player_id in self.players:
            return True
        return False

    def isWaiting(self):
        if self.getPlayerNb() != 4:
            return True
        return False
