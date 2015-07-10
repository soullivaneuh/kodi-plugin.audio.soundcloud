__author__ = 'bromix'

import unittest

from resources.lib.org.bromix import nightcrawler
from resources.lib.de import golem


class TestRun(unittest.TestCase):
    def test_run(self):
        context = nightcrawler.Context()
        provider = golem.Provider()

        nightcrawler.run(provider, context)
        pass

    pass
