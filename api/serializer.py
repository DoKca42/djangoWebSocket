from rest_framework import serializers

"""
{
    "match_id": 12348546545,
    "tournament_id": 0,
    "player1_score": 0,
    "player2_score": 10,
    "player1_id": 12348546545,
    "player2_id": 12348546545,
    "winner_id": 12348546545
}


{
    "match_id": 12348546545,
    "tournament_id": 0,
    "timestamp": 0,
    "player1_score": 0,
    "player2_score": 10,
    "player1_id": 12348546545,
    "player2_id": 12348546545,
    "winner_id": 12348546545
}
"""


class MatchResultSerializer(serializers.Serializer):
    match_id = serializers.IntegerField()
    tournament_id = serializers.IntegerField()
    player1_score = serializers.IntegerField()
    player2_score = serializers.IntegerField()
    player1_id = serializers.IntegerField()
    player2_id = serializers.IntegerField()
    winner_id = serializers.IntegerField()
