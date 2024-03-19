from .Room import Room


class RoomManager:
    def __init__(self):
        self.rooms = []

    def create_room(self):
        room = Room()
        print(type(room))
        self.rooms.append(room)

    def get_rooms(self):
        return self.rooms


room_manager = RoomManager()
