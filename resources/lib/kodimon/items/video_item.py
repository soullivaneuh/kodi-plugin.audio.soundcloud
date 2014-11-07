import re

from . import BaseItem
import datetime


class VideoItem(BaseItem):
    INFO_GENRE = 'genre'  # (string)
    INFO_AIRED = 'aired'  # (string)
    INFO_DURATION = 'duration'  # (int) seconds
    INFO_DIRECTOR = 'director'  # (string)
    INFO_PREMIERED = 'premiered'  # (string) iso 8601
    INFO_EPISODE = 'episode'  # (int)
    INFO_SEASON = 'season'  # (int)
    INFO_YEAR = 'year'  # (int)
    INFO_PLOT = 'plot'  # (string)
    INFO_TITLE = 'title'  # (string)
    INFO_IMDB_ID = 'imdb_id'  # (string)
    INFO_CAST = 'cast'  # (list of string)
    INFO_RATING = 'rating'  # float
    INFO_DATE_ADDED = 'date_added'  # string

    def __init__(self, name, uri, image=u'', fanart=u''):
        BaseItem.__init__(self, name, uri, image, fanart)
        pass

    def set_title(self, title):
        self._info_data[self.INFO_TITLE] = title
        pass

    def get_title(self):
        return self._info_data.get(self.INFO_TITLE, u'')

    def set_date_added(self, year, month, day, hour, minute, second=0):
        date = datetime.datetime(year, month, day, hour, minute, second)
        date = date.isoformat(sep=' ')
        self._info_data[self.INFO_DATE_ADDED] = date
        pass

    def get_date_added(self):
        return self._info_data.get(self.INFO_DATE_ADDED, u'')

    def set_year(self, year):
        self._info_data[self.INFO_YEAR] = int(year)
        pass

    def get_year(self):
        return self._info_data.get(self.INFO_YEAR, -1)

    def set_premiered(self, year, month, day):
        date = datetime.date(year, month, day)
        date = date.isoformat()
        self._info_data[self.INFO_PREMIERED] = date
        pass

    def get_premiered(self):
        return self._info_data.get(self.INFO_PREMIERED, u'')

    def set_plot(self, plot):
        self._info_data[self.INFO_PLOT] = plot
        pass

    def get_plot(self):
        return self._info_data.get(self.INFO_PLOT, u'')

    def set_rating(self, rating):
        self._info_data[self.INFO_RATING] = float(rating)
        pass

    def get_rating(self):
        return self._info_data.get(self.INFO_RATING, -1.0)

    def set_director(self, director_name):
        self._info_data[self.INFO_DIRECTOR] = director_name
        pass

    def get_director(self):
        return self._info_data.get(self.INFO_DIRECTOR, u'')

    def add_cast(self, cast):
        cast_list = self._info_data.get(self.INFO_CAST, [])
        cast_list.append(cast)
        self._info_data[self.INFO_CAST] = cast_list
        pass

    def get_cast(self):
        return self._info_data.get(self.INFO_CAST, [])

    def set_imdb_id(self, url_or_id):
        re_match = re.match('(http\:\/\/)?www.imdb.(com|de)\/title\/(?P<imdbid>[t0-9]+)(\/)?', url_or_id)
        if re_match:
            self._info_data[self.INFO_IMDB_ID] = re_match.group('imdbid')
        else:
            self._info_data[self.INFO_IMDB_ID] = url_or_id
        pass

    def get_imdb_id(self):
        return self._info_data.get(self.INFO_IMDB_ID, u'')

    def set_episode(self, episode):
        self._info_data[self.INFO_EPISODE] = int(episode)
        pass

    def get_episode(self):
        return self._info_data.get(self.INFO_EPISODE, -1)

    def set_season(self, season):
        self._info_data[self.INFO_SEASON] = int(season)
        pass

    def get_season(self):
        return self._info_data.get(self.INFO_SEASON, -1)

    def set_duration(self, hours, minutes, seconds=0):
        _seconds = seconds
        _seconds += minutes * 60
        _seconds += hours * 60 * 60
        self.set_duration_from_seconds(_seconds)
        pass

    def set_duration_from_minutes(self, minutes):
        self.set_duration_from_seconds(int(minutes) * 60)
        pass

    def set_duration_from_seconds(self, seconds):
        self._info_data[self.INFO_DURATION] = seconds
        pass

    def get_duration(self):
        return self._info_data.get(self.INFO_DURATION, 0)

    def set_aired(self, year, month, day):
        date = datetime.date(year, month, day)
        date = date.isoformat()
        self._info_data[self.INFO_AIRED] = date
        pass

    def get_aired(self):
        return self._info_data.get(self.INFO_AIRED, u'')

    def set_genre(self, genre):
        self._info_data[self.INFO_GENRE] = genre
        pass

    def get_genre(self):
        return self._info_data.get(self.INFO_GENRE, u'')

    pass