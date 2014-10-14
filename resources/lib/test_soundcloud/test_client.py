# -*- coding: utf-8 -*-

__author__ = 'bromix'

import unittest
from resources.lib.soundcloud import Client


class TestClient(unittest.TestCase):
    TOKEN = u'1-21686-31343147-274613f4c3e367e'

    def setUp(self):
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

    def test_get_me_posts(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_me_posts()
        pass

    def test_get_me_playlists(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_me_playlists()
        pass

    def test_get_me_following(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_me_following()
        pass

    def test_get_me(self):
        client = Client(access_token=self.TOKEN)
        json_data = client.get_me()

        self.assertGreater(len(json_data), 0)
        pass

    def test_update_token(self):
        client = Client(username='b194139@trbvm.com', password='1234567890')
        token = client.update_access_token()

        self.assertTrue(token is not None)
        print "Token: '%s'" % token
        pass

    pass
