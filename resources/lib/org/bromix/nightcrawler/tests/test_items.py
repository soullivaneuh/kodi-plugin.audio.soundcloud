from resources.lib.org.bromix import nightcrawler

__author__ = 'bromix'

import unittest


class TestItems(unittest.TestCase):
    def test_next_page_item(self):
        context = nightcrawler.Context()
        item = nightcrawler.items.create_next_page_item(context)
        self.assertEquals(item['uri'], 'plugin://mock.plugin/?page=2')

        context = nightcrawler.Context(params={'page': '10'})
        item = nightcrawler.items.create_next_page_item(context)
        self.assertEquals(item['uri'], 'plugin://mock.plugin/?page=11')

        context = nightcrawler.Context(path='format/a', params={'filter': '1'})
        item = nightcrawler.items.create_next_page_item(context)
        self.assertEquals(item['uri'], 'plugin://mock.plugin/format/a/?filter=1&page=2')
        pass
    pass
