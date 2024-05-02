import time

import requests

from Log.Log import Log
from api.urls_api import BLOCKCHAIN_URL, BLOCKCHAIN_HOST
from threading import Thread


class PostRequest:
    def __init__(self):
        self.posts_result_match = []
        self.posts_room_match = []
        thread = Thread(target=self.retryLoop)
        thread.daemon = True
        thread.start()

    def addPostResultMatch(self, post):
        if post not in self.posts_result_match:
            self.posts_result_match.append(post)

    def addPostRoomMatch(self, post):
        if post not in self.posts_room_match:
            self.posts_room_match.append(post)

    def tryPosts(self):
        Log.debug("[API] TRY'", "")
        for post in self.posts_result_match:
            self.matchResult(post)
        for post in self.posts_room_match:
            self.matchRoom(post)

    def retryLoop(self):
        while True:
            self.tryPosts()
            time.sleep(5)

    def printPosts(self):
        for post in self.posts_result_match:
            print(post)

    # =========== SEND ===========

    def matchResult(self, match):
        try:
            host = BLOCKCHAIN_URL+":"+BLOCKCHAIN_HOST
            url = host + '/match/post/'
            x = requests.post(url, json=match)
            Log.info("[API] Post 'matchResult'", x)
        except Exception as e:
            self.addPostResultMatch(match)
            Log.error("[API] Post 'matchResult' Error", e)

    def matchRoom(self, match):
        try:
            host = BLOCKCHAIN_URL+":"+BLOCKCHAIN_HOST
            url = host + '/match/post/'
            x = requests.post(url, json=match)
            Log.info("[API] Post 'matchRoom'", x)
        except Exception as e:
            self.addPostRoomMatch(match)
            Log.error("[API] Post 'matchRoom' Error", e)


post_request = PostRequest()

