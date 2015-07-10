__author__ = 'bromix'

import unittest

from resources.lib.org.bromix import nightcrawler


class TestPath(unittest.TestCase):
    def test_from_uri(self):
        uri = 'plugin://mock.plugin/play/?url=http%3A%2F%2Fvideo.golem.de%2Fgames%2F15600%2Ftrials-fusion-awesome-level-max-trailer-gameplay.html'
        path, params = nightcrawler.utils.path.from_uri(uri)
        self.assertEquals(path, '/play/')
        self.assertEquals(params['url'],
                          'http://video.golem.de/games/15600/trials-fusion-awesome-level-max-trailer-gameplay.html')
        pass

    pass
