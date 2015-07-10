# -*- coding: utf-8 -*-

__author__ = 'bromix'

import unittest

from resources.lib.org.bromix import nightcrawler


class TestStrings(unittest.TestCase):
    def test_to_utf8(self):
        text = 'bäume'
        self.assertEquals(True, isinstance(text, str))
        utf8_text = nightcrawler.utils.strings.to_utf8(text)
        self.assertEquals(True, isinstance(utf8_text, str))

        text = u'bäume'
        self.assertEquals(True, isinstance(text, unicode))
        u_text = nightcrawler.utils.strings.to_utf8(text)
        self.assertEquals(True, isinstance(u_text, str))
        pass

    def test_to_unicode(self):
        text = 'bäume'
        self.assertEquals(True, isinstance(text, str))
        u_text = nightcrawler.utils.strings.to_unicode(text)
        self.assertEquals(True, isinstance(u_text, unicode))

        text = u'bäume'
        self.assertEquals(True, isinstance(text, unicode))
        u_text = nightcrawler.utils.strings.to_unicode(text)
        self.assertEquals(True, isinstance(u_text, unicode))
        pass

    def test_date_time_abbreviated(self):
        date_str = 'Wed, 04 Mar 2015 12:30:35 +0100'
        datetime = nightcrawler.utils.datetime.parse(date_str)

        self.assertEqual(2015, datetime.year)
        self.assertEqual(3, datetime.month)
        self.assertEqual(4, datetime.day)
        self.assertEqual(12, datetime.hour)
        self.assertEqual(30, datetime.minute)
        self.assertEqual(35, datetime.second)
        pass

    def test_date_time_with_delta(self):
        date_str = '2013-02-21 10:04:00 +0100'
        datetime = nightcrawler.utils.datetime.parse(date_str)

        self.assertEqual(2013, datetime.year)
        self.assertEqual(2, datetime.month)
        self.assertEqual(21, datetime.day)
        self.assertEqual(10, datetime.hour)
        self.assertEqual(4, datetime.minute)
        self.assertEqual(0, datetime.second)
        pass

    def test_period(self):
        duration = u'PT47M54S'
        time = nightcrawler.utils.datetime.parse(duration)

        seconds = 47*60+54
        self.assertEqual(seconds, time.seconds)
        pass

    def test_date_time(self):
        date_str = u'2014-09-22 09:18:38'
        datetime = nightcrawler.utils.datetime.parse(date_str)
        self.assertEqual(2014, datetime.year)
        self.assertEqual(9, datetime.month)
        self.assertEqual(22, datetime.day)
        self.assertEqual(9, datetime.hour)
        self.assertEqual(18, datetime.minute)
        self.assertEqual(38, datetime.second)

        date_str = u'2014-09-22T09:18:38'
        datetime = nightcrawler.utils.datetime.parse(date_str)
        self.assertEqual(2014, datetime.year)
        self.assertEqual(9, datetime.month)
        self.assertEqual(22, datetime.day)
        self.assertEqual(9, datetime.hour)
        self.assertEqual(18, datetime.minute)
        self.assertEqual(38, datetime.second)
        pass

    def test_time_only(self):
        time_str = u'00:22:10'
        _time = nightcrawler.utils.datetime.parse(time_str)
        self.assertEqual(0, _time.hour)
        self.assertEqual(22, _time.minute)
        self.assertEqual(10, _time.second)
        pass

    def test_date_only(self):
        date_str = u'2014-09-29'
        date = nightcrawler.utils.datetime.parse(date_str)
        self.assertEqual(2014, date.year)
        self.assertEqual(9, date.month)
        self.assertEqual(29, date.day)
        pass

    pass