# -*- coding: utf-8 -*-
__author__ = 'bromix'

import os
import unittest

from resources.lib.org.bromix import nightcrawler


class TestFavList(unittest.TestCase):
    def setUp(self):
        self._filename = os.path.join(nightcrawler.Context().get_data_path(), u'kodion', u'favorites')
        pass

    def test_add_fav(self):
        item = {'type': 'folder',
                'title': u'Crash Games - Jeder Sturz zählt',
                'uri': '/pro7/library/277/',
                'images': {'thumbnail': 'image url',
                           'fanart': 'fanart url'}}

        fav_list = nightcrawler.storage.FavoriteList(self._filename)
        # remove any existing favs
        fav_list.clear()
        favs = fav_list.list()
        self.assertEqual(0, len(favs))

        # add one fav
        fav_list.add(item)
        favs = fav_list.list()
        self.assertEqual(1, len(favs))

        # add the same fav again
        fav_list.add(item)
        favs = fav_list.list()
        self.assertEqual(1, len(favs))
        pass

    def test_remove_fav(self):
        item = {'type': 'folder',
                'title': u'Crash Games - Jeder Sturz zählt',
                'uri': '/pro7/library/277/',
                'images': {'thumbnail': 'image url',
                           'fanart': 'fanart url'}}

        fav_list = nightcrawler.storage.FavoriteList(self._filename)
        # remove any existing favs
        fav_list.clear()
        favs = fav_list.list()
        self.assertEqual(0, len(favs))

        # add one fav
        fav_list.add(item)
        favs = fav_list.list()
        self.assertEqual(1, len(favs))

        # remove the fav from before
        fav_list.remove(item)
        favs = fav_list.list()
        self.assertEqual(0, len(favs))
        pass

    def test_sort(self):
        item = {'type': 'folder',
                'title': u'Crash Games - Jeder Sturz zählt',
                'uri': '/pro7/library/277/',
                'images': {'thumbnail': 'image url',
                           'fanart': 'fanart url'}}

        item2 = {'type': 'folder',
                 'title': u'Ärash Games - Jeder Sturz zählt',
                 'uri': '/pro7/library/278/',
                 'images': {'thumbnail': 'image url',
                            'fanart': 'fanart url'}}

        fav_list = nightcrawler.storage.FavoriteList(self._filename)
        # remove any existing favs
        fav_list.clear()
        favs = fav_list.list()
        self.assertEqual(0, len(favs))

        # add one fav
        fav_list.add(item)
        fav_list.add(item2)
        favs = fav_list.list()
        self.assertEqual(2, len(favs))

        # remove the fav from before
        fav_list.remove(item)
        favs = fav_list.list()
        self.assertEqual(1, len(favs))
        pass

    pass