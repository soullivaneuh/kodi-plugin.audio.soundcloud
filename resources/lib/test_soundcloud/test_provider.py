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

    def test_search(self):
        provider = Provider()

        path = '/%s/query/' % provider.PATH_SEARCH
        result = provider.navigate(path, {'q': 'angerfist'})
        pass

    def test_root(self):
        provider = Provider()

        result = provider.navigate('/')
        items = result[0]

        self.assertEqual(1, len(items))

        print_items(items)
        pass

    def test_get_hires_images(self):
        provider = Provider()

        result = provider._get_hires_image(u'https://i1.sndcdn.com/avatars-000069503963-bk852l-large.jpg')
        self.assertEqual(u'https://i1.sndcdn.com/avatars-000069503963-bk852l-t500x500.jpg', result)

        result = provider._get_hires_image('https://i1.sndcdn.com/avatars-000069503963-bk852l-large.jpg?86347b7')
        self.assertEqual('https://i1.sndcdn.com/avatars-000069503963-bk852l-t500x500.jpg', result)

        result = provider._get_hires_image('https://i1.sndcdn.com/artworks-000044733261-1obt8a-large.jpg?86347b7')
        self.assertEqual('https://i1.sndcdn.com/artworks-000044733261-1obt8a-t500x500.jpg', result)
        pass

    pass
