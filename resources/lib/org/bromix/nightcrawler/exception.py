__author__ = 'bromix'


class NightcrawlerException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        self._message = message
        pass

    def get_message(self):
        return self._message

    pass
