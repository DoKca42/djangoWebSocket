import uuid
import time

from api.PostRequest import PostRequest, post_request
from room.RoomClientManager import room_client_manager
from room.UniqId import Uniqid


class Room:
    id = 0
    player_id_a = ""
    player_id_b = ""
    score_player_a = 0
    score_player_b = 0
    game_start_date = 0
    game_end_date = 0
    created_date = 0
    game_started = False
    game_ia = False

    def __init__(self):
        self.id = Uniqid.generate()
        self.player_id_a = ""
        self.player_id_b = ""
        self.score_player_a = 0
        self.score_player_b = 0
        self.game_start_date = 0
        self.game_end_date = 0
        self.created_date = Uniqid.getUnixTimeStamp()
        self.game_started = False
        self.game_ia = False

    # ======= SETTER =======

    def setPlayerA(self, player_id_a):
        self.player_id_a = player_id_a

    def setPlayerB(self, player_id_b):
        self.player_id_b = player_id_b

    def setScorePlayerA(self, score_player_a):
        self.score_player_a = score_player_a

    def setScorePlayerB(self, score_player_b):
        self.score_player_b = score_player_b

    def setGameStartDate(self):
        self.game_start_date = int(time.time())

    def setGameEndDate(self):
        self.game_end_date = int(time.time())

    def addPlayer(self, player_id):
        if self.getPlayerNb() == 2:
            return False
        if self.getPlayerNb() == 1:
            self.setPlayerB(player_id)
        else:
            self.setPlayerA(player_id)
        return True

    def setGameStarted(self):
        self.game_started = True
        post_request.addPostRoomMatch(self.getGameAsJSON())

    def setGameIa(self, ia):
        self.game_ia = ia

    def setAllPlayersInGameStatus(self, status):
        if self.getPlayerA() != "":
            room_client_manager.getClientById(self.getPlayerA()).setInGame(status)
        if self.getPlayerB() != "":
            room_client_manager.getClientById(self.getPlayerB()).setInGame(status)

    def leaveAllPlayers(self):
        if room_client_manager.isClientIdExist(self.player_id_a):
            room_client_manager.getClientById(self.player_id_a).setInARoom(False)
            room_client_manager.getClientById(self.player_id_a).setInGame(False)
        if room_client_manager.isClientIdExist(self.player_id_b):
            room_client_manager.getClientById(self.player_id_b).setInARoom(False)
            room_client_manager.getClientById(self.player_id_b).setInGame(False)

    # ======= GETTER =======

    def getId(self):
        return self.id

    def getPlayerA(self):
        return self.player_id_a

    def getPlayerB(self):
        return self.player_id_b

    def getScorePlayerA(self):
        return self.score_player_a

    def getScorePlayerB(self):
        return self.score_player_b

    def getGameStartDate(self):
        return self.game_start_date

    def getGameEndedDate(self):
        return self.game_end_date

    def getCreatedDate(self):
        return self.created_date

    def getPlayerNb(self):
        if self.player_id_b != "" and self.player_id_b != "":
            return 2
        if self.player_id_a != "" or self.player_id_b != "":
            return 1
        return 0

    def getGameStartedDate(self):
        return self.game_started

    def getGameIa(self):
        return self.game_ia

    def getGameAsJSON(self):
        obj = {
            "match_id": self.id,
            "tournament_id": 0,
            "player1_id": self.getPlayerA(),
            "player2_id": self.getPlayerB()
        }
        return obj

    def playerIdIsInRoom(self, player_id):
        if self.player_id_a == player_id or self.player_id_b == player_id:
            return True
        return False

    def isWaiting(self):
        if self.getGameIa() is False and self.getPlayerNb() == 1:
            return True
        return False
