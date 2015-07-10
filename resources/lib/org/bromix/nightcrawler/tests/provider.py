__author__ = 'bromix'

import unittest

from resources.lib.org.bromix import nightcrawler


class DummyProvider(nightcrawler.Provider):
    def __init__(self):
        nightcrawler.Provider.__init__(self)
        pass

    pass


class TestProvider(unittest.TestCase):
    def test_select_video_stream(self):
        context = nightcrawler.Context()
        provider = DummyProvider()

        video_streams = stream_data = [
            {
                'title': '720p@5000',
                'sort': [720, 5000],
                'video': {'height': 720, 'width': 1280, 'bandwidth': 5000},
                'uri': '720p@5000'
            },
            {
                'title': '720p@10000',
                'sort': [720, 10000],
                'video': {'height': 720, 'width': 1280, 'bandwidth': 10000},
                'uri': '720p@10000'
            },
            {
                'title': '480p@5000',
                'sort': [480, 5000],
                'video': {'height': 480, 'width': 640, 'bandwidth': 5000},
                'uri': '480p@5000'
            },
            {
                'title': '1080p@5000', 'sort': [1080, 5000],
                'video': {'height': 1080, 'width': 1920, 'bandwidth': 5000},
                'uri': '1080p@5000'
            },
            {
                'title': '1080p@10000', 'sort': [1080, 10000],
                'video': {'height': 1080, 'width': 1920, 'bandwidth': 10000},
                'uri': '1080p@10000'
            }
        ]

        settings = context.get_settings()
        settings.set_int(settings.VIDEO_QUALITY, 0)
        video_stream = provider.select_video_stream(context, video_streams, video_quality_index=[360, 480, 720, 1080])
        self.assertEquals(video_stream['uri'], '480p@5000')

        settings.set_int(settings.VIDEO_QUALITY, 1)
        video_stream = provider.select_video_stream(context, video_streams, video_quality_index=[360, 480, 720, 1080])
        self.assertEquals(video_stream['uri'], '480p@5000')

        settings.set_int(settings.VIDEO_QUALITY, 2)
        video_stream = provider.select_video_stream(context, video_streams, video_quality_index=[360, 480, 720, 1080])
        self.assertEquals(video_stream['uri'], '720p@10000')

        settings.set_int(settings.VIDEO_QUALITY, 3)
        video_stream = provider.select_video_stream(context, video_streams, video_quality_index=[360, 480, 720, 1080])
        self.assertEquals(video_stream['uri'], '1080p@10000')
        pass

    pass
