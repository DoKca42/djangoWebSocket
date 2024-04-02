import uuid
import time


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
        self.id = str(uuid.uuid4())
        self.created_date = int(time.time())

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

    def setGameIa(self, ia):
        self.game_ia = ia

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

    def playerIdIsInRoom(self, player_id):
        if self.player_id_a == player_id or self.player_id_b == player_id:
            return True
        return False

    def getGameStartedDate(self):
        return self.game_started

    def getGameIa(self):
        return self.game_ia
