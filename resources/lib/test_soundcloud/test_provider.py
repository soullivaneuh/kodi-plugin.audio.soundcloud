__author__ = 'bromix'

from resources.lib.soundcloud.provider import Provider
import unittest


def print_items(items):
    for item in items:
        print item
        pass
    pass

class TestProvider(unittest.TestCase):
    def setUp(self):
        pass

    def test_root(self):
        provider = Provider()

        result = provider.navigate('/')
        items = result[0]

        self.assertEqual(1, len(items))

        print_items(items)
        pass

    pass
