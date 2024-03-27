class RoomClientManager:
    def __init__(self):
        self.clients = []

    def addClient(self, client):
        self.clients.append(client)

    def getClients(self):
        return self.clients

    def isClientIdExist(self, sessionId):
        for client in self.clients:
            if client.getSessionId() == sessionId:
                return True
        return False

    def getClientById(self, sessionId):
        for client in self.clients:
            if client.getSessionId() == sessionId:
                return client
        return False

    def printAll(self):
        print("Variables de RoomClientManager :")
        for a in self.clients:
            print("- "+str(a.getSessionId()))


room_client_manager = RoomClientManager()
