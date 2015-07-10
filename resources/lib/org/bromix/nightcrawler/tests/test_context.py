# -*- coding: utf-8 -*-
__author__ = 'bromix'

import unittest

from resources.lib.org.bromix import nightcrawler


class TestContext(unittest.TestCase):
    def test_add_item(self):
        item = {'type': 'folder',
                'title': u'Crash Games - Jeder Sturz zählt',
                'uri': '/pro7/library/277/',
                'images': {'thumbnail': 'image url',
                           'fanart': 'fanart url'}}

        context = nightcrawler.Context()
        context.add_item(item)
        pass

    def test_get_python_version(self):
        context = nightcrawler.Context()
        py_version = context.get_python_version()

        if (2, 7, 5) < py_version <= (2, 7, 8):
            x = 0
            pass

        self.assertIsInstance(py_version, tuple)
        pass

    def test_logging(self):
        context = nightcrawler.Context()

        context.log_debug('Hello World')
        context.log_info('Hello World')
        context.log_warning('Hello World')
        context.log_error('Hello World')
        pass

    def test_create_uri(self):
        context = nightcrawler.Context()
        uri = context.create_uri(path='/browse/now/', params={'video_id': '121234'})
        self.assertEquals('plugin://mock.plugin/browse/now/?video_id=121234', uri)

        uri = context.create_uri(path='/browse//now/', params={'video_id': '121234'})
        self.assertEquals('plugin://mock.plugin/browse/now/?video_id=121234', uri)

        uri = context.create_uri(path='browse//now', params={'video_id': '121234'})
        self.assertEquals('plugin://mock.plugin/browse/now/?video_id=121234', uri)

        uri = context.create_uri(path=u'/Bäume/Äpfel/', params={'video_id': '121234'})
        self.assertEquals('plugin://mock.plugin/B%C3%A4ume/%C3%84pfel/?video_id=121234', uri)
        pass

    def test_create_resource_path(self):
        context = nightcrawler.Context()
        resource_path = context.create_resource_path('/media/search.png')
        self.assertEquals('\\user\\x\\data\\resources\\media\\search.png', resource_path)
        pass

    pass
