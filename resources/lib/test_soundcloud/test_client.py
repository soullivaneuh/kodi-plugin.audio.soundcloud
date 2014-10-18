# -*- coding: utf-8 -*-

__author__ = 'bromix'

import unittest
from resources.lib.soundcloud import Client


class TestClient(unittest.TestCase):
    TOKEN = u'1-21686-118589874-262b20fc160e44'

    def setUp(self):
        pass

    def test_get_liked_tracks(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_liked_tracks()
        self.assertGreater(len(json_data), 0)

    def test_get_trending(self):
        client = Client()
        json_data = client.get_trending('audio')
        pass

    def test_get_genre(self):
        client = Client()
        json_data = client.get_genre('techno')
        pass

    def test_get_track_url(self):
        client = Client()
        json_data = client.get_track_url(77773864)
        pass

    def test_search(self):
        client = Client()
        json_data = client.search('bäume')
        pass

    def test_get_stream(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_stream()
        pass

    def test_tracks(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_tracks('me')

        json_data = client.get_tracks(1701116)
        pass

    def test_follow(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.follow_user(1701116, False)
        self.assertGreater(len(json_data), 0)

        json_data = client.follow_user(1701116, True)
        self.assertGreater(len(json_data), 0)
        pass

    def test_get_playlist(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_playlist(55019726)
        self.assertGreater(len(json_data), 0)
        pass

    def test_get_playlists(self):
        # me
        client = Client(access_token=self.TOKEN)
        json_data = client.get_playlists('me')
        self.assertGreater(len(json_data), 0)

        # some user
        json_data = client.get_playlists(2442230)
        self.assertGreater(len(json_data), 0)
        pass

    def test_get_favorites(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_favorites('me')
        self.assertGreater(len(json_data), 0)
        pass

    def test_get_follower(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_follower('me')
        self.assertGreater(len(json_data), 0)
        pass

    def test_get_following(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_following('me')
        self.assertGreater(len(json_data), 0)
        pass

    def test_user(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_user('me')

        self.assertGreater(len(json_data), 0)
        pass

    def test_update_token(self):
        client = Client(username='co4hu41hkqud5cm@my10minutemail.com', password='1234567890')
        token = client.update_access_token()

        self.assertTrue(token is not None)
        print "Token: '%s'" % token
        pass

    pass
