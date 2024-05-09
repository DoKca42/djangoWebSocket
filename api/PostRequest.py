import json
import time

import requests

from Log.Log import Log
from api.Signature import Signature
from api.urls_api import BLOCKCHAIN_URL, BLOCKCHAIN_HOST, GAMEENGINE_HOST, GAMEENGINE_URL
from threading import Thread
from datetime import datetime, timedelta

from room.UniqId import Uniqid


class PostRequest:
    def __init__(self):
        self.posts_result_match = []
        self.posts_result_tour = []
        self.posts_room_match = []
        thread = Thread(target=self.retryLoop)
        thread.daemon = True
        thread.start()

    def addPostResultMatch(self, post):
        if post not in self.posts_result_match:
            self.posts_result_match.append(post)

    def addPostResultTour(self, post):
        if post not in self.posts_result_tour:
            self.posts_result_tour.append(post)

    def addPostRoomMatch(self, post):
        if post not in self.posts_room_match:
            self.posts_room_match.append(post)

    def removePostResultMatch(self, post):
        if post in self.posts_result_match:
            self.posts_result_match.remove(post)

    def removePostResultTour(self, post):
        if post in self.posts_result_tour:
            self.posts_result_tour.remove(post)

    def removePostRoomMatch(self, post):
        if post in self.posts_room_match:
            self.posts_room_match.remove(post)

    def tryPosts(self):
        for post in self.posts_result_match:
            self.matchResult(post)
        for post in self.posts_result_tour:
            self.tourResult(post)
        for post in self.posts_room_match:
            self.matchRoom(post)

    def retryLoop(self):
        while True:
            self.tryPosts()
            time.sleep(5)

    # =========== SEND ===========

    def matchResult(self, match):
        try:
            data, signature, headers = Signature.create_signed_token(match, "key/blockchain/private_key.pem")

            host = BLOCKCHAIN_URL + ":" + BLOCKCHAIN_HOST
            url = host + '/match/post/'
            x = requests.post(url, json=data, headers=headers)
            Log.info("[API] Post 'matchResult'", x)
            self.removePostResultMatch(match)
        except Exception as e:
            Log.error("[API] Post 'matchResult' Error", e)

    def tourResult(self, tour):
        try:
            data, signature, headers = Signature.create_signed_token(tour, "key/blockchain/private_key.pem")

            host = BLOCKCHAIN_URL + ":" + BLOCKCHAIN_HOST
            url = host + '/tournament/post/'
            x = requests.post(url, json=data, headers=headers)
            Log.info("[API] Post 'tourResult'", x)
            self.removePostResultTour(tour)
        except Exception as e:
            Log.error("[API] Post 'matchResult' Error", e)

    def matchRoom(self, match):
        try:
            data, signature, headers = Signature.create_signed_token(match, "key/gameengine/private_key.pem")

            host = GAMEENGINE_URL + ":" + GAMEENGINE_HOST
            url = host + '/api/create_game/'
            x = requests.post(url, json=data, headers=headers)
            Log.info("[API] Post 'matchRoom'", x)
            self.removePostRoomMatch(match)
        except Exception as e:
            Log.error("[API] Post 'matchRoom' Error", e)


post_request = PostRequest()
