import time

import requests
from sty import fg, bg, ef, rs
import asyncio
from threading import Thread


class PostSaver:
    def __init__(self):
        self.posts_result_match = []
        thread = Thread(target=self.retryLoop)
        thread.daemon = True
        thread.start()

    def addPostResultMatch(self, post):
        if post not in self.posts_result_match:
            self.posts_result_match.append(post)

    def tryPosts(self):
        for post in self.posts_result_match:
            PostRequest.match(post)

    def retryLoop(self):
        while True:
            self.tryPosts()
            time.sleep(5)

    def printPosts(self):
        for post in self.posts_result_match:
            print(post)


post_saver = PostSaver()


class PostRequest:

    @staticmethod
    def match(match):
        try:
            host = "http://k12r4p6:8000"
            url = host + '/match/post/'
            x = requests.post(url, json=match)
        except Exception as e:
            post_saver.addPostResultMatch(match)
            print(fg.red + "[API] PostRequest Error: " + fg.white + str(e))
