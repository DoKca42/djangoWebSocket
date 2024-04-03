from room.Room import Room


class RoomManager:
    def __init__(self):
        self.rooms = []

    def createRoom(self):
        room = Room()
        self.rooms.append(room)
        return room.getId()

    def getRooms(self):
        return self.rooms

    def isRoomIdExist(self, roomId):
        for room in self.rooms:
            if room.getId() == roomId:
                return True
        return False

    def getRoomById(self, roomId):
        for room in self.rooms:
            if room.getId() == roomId:
                return room
        return False

    def getWaitingRoom(self):
        for room in self.rooms:
            if room.isWaiting():
                return room.getId()
        return False


room_manager = RoomManager()
