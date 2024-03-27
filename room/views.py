from django.shortcuts import render
from room.RoomManager import room_manager


# Create your views here.
def lobby(request):
    rooms = room_manager.getRooms()
    for room in rooms:
        print("{VIEW} "+room.getId())
    return render(request, "chat/lobby.html",
                  {"rooms": rooms})
