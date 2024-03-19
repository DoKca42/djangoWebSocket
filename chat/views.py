from django.shortcuts import render

from chat.RoomManager import room_manager


# Create your views here.
def lobby(request):
    rooms = room_manager.get_rooms()
    return render(request, "chat/lobby.html",
                  {"rooms": rooms})
