from room.RoomManager import room_manager
import uuid
import time



class Tournament:
    id = 0
    created_date = 0
    demi_room_a = None
    demi_room_b = None
    final_room = None
    players = []
    status = 0          # 0: waiting | 1: tournament start | 2: end demi | 3: end final

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_date = int(time.time())
        self.demi_room_a = room_manager.createRoom()
        self.demi_room_b = room_manager.createRoom()
        self.final_room = room_manager.createRoom()
        self.players = []
        self.status = 0
        pass

    def __upStatus(self):
        self.status += 1

    def __startTournament(self):
        self.__upStatus()
        self.demi_room_a.addPlayer(self.players[0])
        self.demi_room_a.addPlayer(self.players[1])
        self.demi_room_b.addPlayer(self.players[2])
        self.demi_room_b.addPlayer(self.players[3])
        pass

    # ======= SETTER =======

    def addPlayer(self, player_id):
        if self.getPlayerNb() < 3:
            self.players.append(player_id)
            if len(self.players) == 4:
                self.__startTournament()
            return True
        return False

    def removePlayer(self, player_id):
        if self.status != 0:
            return False
        if self.playerIsInTournament(player_id):
            self.players.remove(player_id)
            return True
        return False

    # ======= GETTER =======

    def getId(self):
        return self.id

    def getCreatedDate(self):
        return self.created_date

    def getPlayerNb(self):
        return len(self.players)

    def playerIsInTournament(self, player_id):
        if player_id in self.players:
            return True
        return False

    def isWaiting(self):
        if self.getPlayerNb() != 4:
            return True
        return False
