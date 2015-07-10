# -*- coding: utf-8 -*-
__author__ = 'bromix'

import os
import unittest

from resources.lib.org.bromix import nightcrawler


class TestWatchLater(unittest.TestCase):
    def setUp(self):
        self._filename = os.path.join(nightcrawler.Context().get_data_path(), u'kodion', u'watch_later')
        pass

    def test_add_video(self):
        item = {'type': 'folder',
                'title': u'Crash Games - Jeder Sturz zählt',
                'uri': '/pro7/library/277/',
                'images': {'thumbnail': 'image url',
                           'fanart': 'fanart url'}}

        watch_later = nightcrawler.storage.WatchLaterList(self._filename)
        watch_later.clear()
        watch_later.sync()
        videos = watch_later.list()
        self.assertEqual(0, len(videos))

        # add one fav
        watch_later.add(item)
        videos = watch_later.list()
        self.assertEqual(1, len(videos))

        # add the same fav again
        watch_later.add(item)
        videos = watch_later.list()
        self.assertEqual(1, len(videos))
        pass

    def test_remove_fav(self):
        item = {'type': 'folder',
                'title': u'Crash Games - Jeder Sturz zählt',
                'uri': '/pro7/library/277/',
                'images': {'thumbnail': 'image url',
                           'fanart': 'fanart url'}}

        watch_later = nightcrawler.storage.WatchLaterList(self._filename)
        watch_later.clear()
        videos = watch_later.list()
        self.assertEqual(0, len(videos))

        watch_later.add(item)
        videos = watch_later.list()
        self.assertEqual(1, len(videos))

        watch_later.remove(item)
        videos = watch_later.list()
        self.assertEqual(0, len(videos))
        pass

    pass