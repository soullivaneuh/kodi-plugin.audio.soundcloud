__author__ = 'bromix'

from . import BaseItem


class AudioItem(BaseItem):
    INFO_DURATION = 'duration'  # (int)
    INFO_TRACK_NUMBER = 'track_number'  # (int)
    INFO_YEAR = 'year'  # (int)
    INFO_GENRE = 'genre'  # (string)
    INFO_ALBUM = 'album'  # (string)
    INFO_ARTIST = 'artist'  # (string)
    INFO_TITLE = 'title'  # (string)
    INFO_RATING = 'rating'  # (float)

    def __init__(self, name, uri, image=u'', fanart=u''):
        BaseItem.__init__(self, name, uri, image, fanart)
        pass

    def set_rating(self, rating):
        self._info_data[self.INFO_RATING] = float(rating)
        pass

    def get_rating(self):
        return self._info_data.get(self.INFO_RATING, -1.0)

    def set_title(self, title):
        self._info_data[self.INFO_TITLE] = title
        pass

    def get_title(self):
        return self._info_data.get(self.INFO_TITLE, u'')

    def set_artist_name(self, artist_name):
        self._info_data[self.INFO_ARTIST] = artist_name
        pass

    def get_artist_name(self):
        return self._info_data.get(self.INFO_ARTIST, u'')

    def set_album_name(self, album_name):
        self._info_data[self.INFO_ALBUM] = album_name
        pass

    def get_album_name(self):
        return self._info_data.get(self.INFO_ALBUM, u'')

    def set_genre(self, genre):
        self._info_data[self.INFO_GENRE] = genre
        pass

    def get_genre(self):
        return self._info_data.get(self.INFO_GENRE, u'')

    def set_year(self, year):
        self._info_data[self.INFO_YEAR] = int(year)
        pass

    def get_year(self):
        return self._info_data.get(self.INFO_YEAR, -1)

    def set_track_number(self, track_number):
        self._info_data[self.INFO_TRACK_NUMBER] = int(track_number)
        pass

    def get_track_number(self):
        return self._info_data.get(self.INFO_TRACK_NUMBER, -1)

    def set_duration_from_milli_seconds(self, milli_seconds):
        self.set_duration_from_seconds(int(milli_seconds)/1000)
        pass

    def set_duration_from_seconds(self, seconds):
        self._info_data[self.INFO_DURATION] = int(seconds)
        pass

    def set_duration_from_minutes(self, minutes):
        self.set_duration_from_seconds(int(minutes)*60)
        pass

    def get_duration(self):
        return self._info_data.get(self.INFO_DURATION, 0)

    pass
