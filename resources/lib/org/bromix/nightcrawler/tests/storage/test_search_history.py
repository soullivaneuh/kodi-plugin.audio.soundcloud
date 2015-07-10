# -*- coding: utf-8 -*-
import os
import unittest
import time

from resources.lib.org.bromix import nightcrawler


class TestSearchHistory(unittest.TestCase):
    def setUp(self):
        self._filename = os.path.join(nightcrawler.Context().get_data_path(), u'kodion', u'search')
        pass

    def test_rename(self):
        search = nightcrawler.storage.SearchHistory(self._filename)
        search.clear()
        items = search.list()
        self.assertEqual(0, len(items))

        search.update(u'Tipo')
        time.sleep(1)
        search.update(u'Tree')
        items = search.list()
        self.assertEqual(2, len(items))
        self.assertEquals('Tree', items[0])
        self.assertEquals('Tipo', items[1])

        search.rename('Tipo', 'Typo')
        items = search.list()
        self.assertEqual(2, len(items))
        self.assertEquals('Typo', items[0])
        self.assertEquals('Tree', items[1])
        pass

    def test_performance_tests(self):
        search = nightcrawler.storage.SearchHistory(self._filename, max_items=1000)
        search.clear()
        items = search.list()
        self.assertEqual(0, len(items))

        count = 1000
        start_time = time.time()
        for i in range(count):
            search.update("Entry (%d)" % i)
            pass
        end_time = time.time()

        print end_time-start_time

        items = search.list()
        self.assertEqual(count, len(items))
        pass

    def test_sort_order(self):
        search = nightcrawler.storage.SearchHistory(self._filename)
        search.clear()
        items = search.list()
        self.assertEqual(0, len(items))

        search.update(u'A')
        items = search.list()
        self.assertEqual(1, len(items))
        self.assertEqual(u'A', items[0])

        time.sleep(1)
        search.update(u'B')
        items = search.list()
        self.assertEqual(2, len(items))
        self.assertEqual(u'B', items[0])
        self.assertEqual(u'A', items[1])

        time.sleep(1)
        search.update(u'A')
        items = search.list()
        self.assertEqual(2, len(items))
        self.assertEqual(u'A', items[0])
        self.assertEqual(u'B', items[1])
        pass

    def test_update(self):
        item = u'Bäume'

        search = nightcrawler.storage.SearchHistory(self._filename)
        search.clear()
        items = search.list()
        self.assertEqual(0, len(items))

        search.update(item)
        items = search.list()
        self.assertEqual(1, len(items))
        pass

    def test_clear(self):
        search = nightcrawler.storage.SearchHistory(self._filename)
        search.clear()
        items = search.list()
        self.assertEqual(0, len(items))
        pass

    def test_is_empty(self):
        search = nightcrawler.storage.SearchHistory(self._filename)
        search.clear()
        self.assertEqual(True, search.is_empty())
        pass

    def test_remove(self):
        item = u'Bäume'

        search = nightcrawler.storage.SearchHistory(self._filename)
        search.clear()
        items = search.list()
        self.assertEqual(0, len(items))

        search.update(item)
        items = search.list()
        self.assertEqual(1, len(items))

        search.remove(item)
        items = search.list()
        self.assertEqual(True, search.is_empty())
        self.assertEqual(0, len(items))
        pass

    def test_update_size(self):
        def _create_item(index):
            return "Item_%02d" % index

        search = nightcrawler.storage.SearchHistory(self._filename)
        search.clear()
        items = search.list()
        self.assertEqual(0, len(items))

        for i in range(10):
            item = _create_item(i)
            search.update(item)
            pass

        items = search.list()
        self.assertEqual(10, len(items))

        item11 = _create_item(10)
        search.update(item11)

        items = search.list()
        self.assertEqual(10, len(items))
        pass

    pass