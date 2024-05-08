from api.PostRequest import post_request
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
    demi_room_a_result = {}
    demi_room_b_result = {}
    final_room_result = {}
    players = []
    status = 0  # 0: waiting | 1: tournament start | 2: end of one demi game | 3: end of all demi game | 4: tour finish

    def __init__(self):
        #self.id = Uniqid.generate()
        self.id = "275317150979901770"
        self.created_date = Uniqid.getUnixTimeStamp()

        self.demi_room_a = Room()
        self.demi_room_b = Room()
        self.final_room = Room()
        #-----------------------------------
        self.demi_room_a.id = "297917151745654778"
        self.demi_room_b.id = "795017151745654737"
        self.final_room.id = "357917151745654735"
        # -----------------------------------
        self.players = []
        self.demi_room_a_result = []
        self.demi_room_b_result = []
        self.final_room_result = []
        self.status = 0
        pass

    def __upStatus(self):
        self.status += 1
        if self.status == 2:
            print("1er demi match fini")
        if self.status == 3:
            print("2eme demi match fini")
        if self.status == 4:
            print("match fini")
            all_match = [self.demi_room_a_result, self.demi_room_b_result, self.final_room_result]
            print(all_match)
            post_request.addPostResultTour(all_match)

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

    def leaveAllPlayers(self):
        for player in self.players:
            if room_client_manager.isClientIdExist(player):
                room_client_manager.getClientById(player).setInARoomTour(False)
                room_client_manager.getClientById(player).setInGameTour(False)

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

    def isRoomExistsById(self, room_id):
        if self.final_room.getId() == room_id:
            return True
        if self.demi_room_a.getId() == room_id:
            return True
        if self.demi_room_b.getId() == room_id:
            return True
        return False

    def setRoomResult(self, room_id, result):
        if self.demi_room_a.getId() == room_id:
            self.demi_room_a_result = result
            self.final_room.addPlayer(result["winner_id"])
            self.__upStatus()
        if self.demi_room_b.getId() == room_id:
            self.demi_room_b_result = result
            self.final_room.addPlayer(result["winner_id"])
            self.__upStatus()
        if self.final_room.getId() == room_id:
            self.final_room_result = result
            self.__upStatus()
