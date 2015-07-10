__author__ = 'bromix'

from time import sleep
import os
import unittest

from resources.lib.org.bromix import nightcrawler


class TestFunctionCache(unittest.TestCase):
    def setUp(self):
        self._filename = os.path.join(nightcrawler.Context().get_data_path(), u'kodion', u'cache')
        pass

    def test_get_cached_only(self):
        def _add(x, y):
            return x + y

        cache = nightcrawler.storage.FunctionCache(self._filename)

        cache._clear()
        result = cache.get_cached_only(_add, 5, 6)
        self.assertEqual(None, result)
        result = cache.get(60, _add, 5, 6)
        self.assertEqual(11, result)
        result = cache.get_cached_only(_add, 5, 6)
        self.assertEqual(11, result)

        # named values
        result = cache.get(60, _add, x=5, y=6)
        self.assertEqual(11, result)
        result = cache.get_cached_only(_add, x=5, y=6)
        self.assertEqual(11, result)
        pass

    def test_get(self):
        def _add(x, y):
            return x + y

        cache = nightcrawler.storage.FunctionCache(self._filename)
        cache._clear()
        result = cache.get(60, _add, 5, 6)
        self.assertEqual(11, result)
        result = cache.get(60, _add, 5, 6)
        self.assertEqual(11, result)

        # named values
        result = cache.get(60, _add, x=5, y=6)
        self.assertEqual(11, result)
        pass

    def test_get_with_delay(self):
        def _add(x, y):
            return x + y

        cache = nightcrawler.storage.FunctionCache(self._filename)
        cache._clear()
        result = cache.get(3, _add, 5, 6)
        self.assertEqual(11, result)

        sleep(1)

        result = cache.get(3, _add, 5, 6)
        self.assertEqual(11, result)

        sleep(3)

        result = cache.get(nightcrawler.storage.FunctionCache.ONE_DAY, _add, 5, 6)
        self.assertEqual(11, result)

        # named values
        result = cache.get(60, _add, x=5, y=6)
        self.assertEqual(11, result)
        pass

    pass
