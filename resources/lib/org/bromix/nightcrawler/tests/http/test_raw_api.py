__author__ = 'bromix'

import unittest

#import requests
import resources.lib.org.bromix.nightcrawler.http as requests


class TestRawHttpApiCalls(unittest.TestCase):
    def test_get(self):
        result = requests.get('http://www.example.com')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(result.reason, 'OK')
        pass

    def test_post(self):
        result = requests.post('http://www.example.com')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(result.reason, 'OK')
        pass

    def test_put(self):
        result = requests.put('http://www.example.com')
        self.assertEquals(result.status_code, 405)
        self.assertEquals(result.reason, 'Method Not Allowed')
        pass

    def test_delete(self):
        result = requests.delete('http://www.example.com')
        self.assertEquals(result.status_code, 405)
        self.assertEquals(result.reason, 'Method Not Allowed')
        pass

    def test_options(self):
        result = requests.options('http://www.example.com')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(result.reason, 'OK')
        pass

    def test_head(self):
        result = requests.head('http://www.example.com')
        self.assertEquals(result.status_code, 200)
        self.assertEquals(result.reason, 'OK')
        pass

    pass
