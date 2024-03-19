import uuid
import time


class Room:
    id = 0
    player_a = {}
    player_b = {}
    score_player_a = 0
    score_player_b = 0
    game_start_date = 0
    game_end_date = 0
    created_date = 0

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_date = int(time.time())

    # ======= SETTER =======

    def setPlayerA(self, player_a):
        self.player_a = player_a

    def setPlayerB(self, player_b):
        self.player_b = player_b

    def setScorePlayerA(self, score_player_a):
        self.score_player_a = score_player_a

    def setScorePlayerB(self, score_player_b):
        self.score_player_b = score_player_b

    def setGameStartDate(self):
        self.game_start_date = int(time.time())

    def setGameEndDate(self):
        self.game_end_date = int(time.time())

    # ======= GETTER =======

    def getId(self):
        return self.id

    def getPlayerA(self):
        return self.player_a

    def getPlayerB(self):
        return self.player_b

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
