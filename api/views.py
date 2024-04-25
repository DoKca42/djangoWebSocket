from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.decorators import api_view

from room.UniqId import Uniqid
from .PostRequest import PostRequest
from .serializer import MatchResultSerializer


# Create your views here.
@api_view(['POST'])
def match_result(request):
    data = MatchResultSerializer(data=request.data)
    if data.is_valid():
        valid_data = data.validated_data
        if valid_data["tournament_id"] == 0:
            valid_data["timestamp"] = Uniqid.getUnixTimeStamp()
            PostRequest.matchResult(valid_data)
        else:
            pass
        return Response(data=data.data, status=status.HTTP_200_OK)
    else:
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
