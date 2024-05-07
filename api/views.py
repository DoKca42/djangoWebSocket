from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.decorators import api_view

from room.RoomManager import room_manager
from room.TournamentManager import tournament_manager
from room.UniqId import Uniqid
from .PostRequest import post_request
from .serializer import MatchResultSerializer


# Create your views here.
@api_view(['POST'])
def match_result(request):
    data = MatchResultSerializer(data=request.data)
    if data.is_valid():
        valid_data = data.validated_data
        if valid_data["tournament_id"] == 0:
            if not room_manager.isRoomIdExist(valid_data["match_id"]):
                error_message = "Unknown match id"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            valid_data["timestamp"] = Uniqid.getUnixTimeStamp()
            post_request.addPostResultMatch(valid_data)
            room_manager.removeRoomById(valid_data["match_id"])
        else:
            if not tournament_manager.isTournamentIdExist(valid_data["tournament_id"]):
                error_message = "Unknown tournament id"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

            tour = tournament_manager.getTournament(valid_data["tournament_id"])
            if not tour.isRoomExistsById(valid_data["match_id"]):
                error_message = "Unknown match id"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            #peut etre verfier les autre infos, si les player id sont bien les bon pour cette game

            return Response(data=data.data, status=status.HTTP_200_OK)
        return Response(data=data.data, status=status.HTTP_200_OK)
    else:
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
