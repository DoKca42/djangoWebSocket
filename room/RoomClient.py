class RoomClient:
    session_id = ""
    session_expired = 0
    player_id = ""
    owner_of_a_room = False
    in_game = False
    lang = ""

    def __init__(self):
        self.in_game = False
        self.owner_of_a_room = False
        self.lang = "fr"

    # ======= SETTER =======

    def setSessionId(self, session_id):
        self.session_id = session_id

    def setSessionExpired(self, session_expired):
        self.session_expired = session_expired

    def setPlayerId(self, player_id):
        self.player_id = player_id

    def setOwnerOfARoom(self, status):
        self.owner_of_a_room = status

    def setInGame(self, status):
        self.in_game = status

    def setLang(self, lang):
        self.lang = lang

    # ======= GETTER =======

    def getSessionId(self):
        return self.session_id

    def getSessionExpired(self):
        return self.session_expired

    def getPlayerId(self):
        return self.player_id

    def getOwnerOfARoom(self):
        return self.owner_of_a_room

    def getInGame(self):
        return self.in_game

    def getLang(self):
        return self.lang

    # ======= OTHER =======

    def isAValidSession(self):
        if self.session_id != "":
            return True
        return False

    def printAll(self):
        print("Variables de RoomClient :")
        print(vars(self))

        pass
