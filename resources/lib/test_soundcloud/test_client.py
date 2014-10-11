__author__ = 'bromix'

import unittest
from resources.lib.soundcloud import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_me(self):
        client = Client(access_token=u'1-21686-117607613-6619f148c5da6e')
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
