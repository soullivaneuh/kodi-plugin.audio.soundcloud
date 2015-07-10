__author__ = 'bromix'

import unittest

from resources.lib.org.bromix import nightcrawler


class TestContextSettings(unittest.TestCase):
    def test_video_quality(self):
        settings = nightcrawler.Context().get_settings()

        settings.set_int(settings.VIDEO_QUALITY, 0)
        self.assertEquals(settings.get_video_quality([360, 720]), 360)

        settings.set_int(settings.VIDEO_QUALITY, 0)
        self.assertEquals(settings.get_video_quality(['medium', 'high']), 'medium')

        settings.set_int(settings.VIDEO_QUALITY, 1)
        self.assertEquals(settings.get_video_quality([360, 720]), 720)

        settings.set_int(settings.VIDEO_QUALITY, 1)
        self.assertEquals(settings.get_video_quality(['medium', 'high']), 'high')

        settings.set_int(settings.VIDEO_QUALITY, 2)
        self.assertEquals(settings.get_video_quality([360, 720, 1080]), 1080)
        pass

    def test_string(self):
        settings = nightcrawler.Context().get_settings()
        settings.set_string('name', 'value')
        value = settings.get_string('name', 'failed')
        self.assertEquals(value, 'value')

        value = settings.get_string('name2', 'default')
        self.assertEquals(value, 'default')
        pass

    def test_int(self):
        settings = nightcrawler.Context().get_settings()
        settings.set_int('number', 10)
        value = settings.get_int('number', 'failed')
        self.assertEquals(value, 10)

        value = settings.get_int('number2', 11)
        self.assertEquals(value, 11)

        value = settings.get_int('number2', 'ssjdkfjsd')
        self.assertEquals(value, -1)

        value = settings.get_int('number', 10, converter=lambda x: x * 2)
        self.assertEquals(value, 20)
        pass

    def test_bool(self):
        settings = nightcrawler.Context().get_settings()
        settings.set_bool('enabled', True)
        value = settings.get_bool('enabled', False)
        self.assertEquals(value, True)

        value = settings.get_bool('enabled2', False)
        self.assertEquals(value, False)

        value = settings.get_bool('enabled2', 'Failed')
        self.assertEquals(value, False)
        pass

    pass