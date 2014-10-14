import re

__author__ = 'bromix'

from resources.lib.kodimon import DirectoryItem, AudioItem, constants
from resources.lib import kodimon


class Provider(kodimon.AbstractProvider):
    def __init__(self):
        kodimon.AbstractProvider.__init__(self)

        from resources.lib import soundcloud
        self._client = soundcloud.Client()
        pass

    def get_fanart(self):
        """
        This will return a darker and (with blur) fanart
        :return:
        """
        return self.create_resource_path('media', 'fanart.jpg')

    def _get_hires_image(self, url):
        return re.sub('(.*)(-large.jpg\.*)(\?.*)?', r'\1-t500x500.jpg', url)

    def _get_track_year(self, collection_item_json):
        # this would be the default info, but is mostly not set :(
        year = collection_item_json.get('release_year', '')
        if year:
            return year

        # we use a fallback.
        # created_at=2013/03/24 00:32:01 +0000
        re_match = re.match('(?P<year>\d{4})(.*)', collection_item_json.get('created_at', ''))
        if re_match:
            year = re_match.group('year')
            if year:
                return year
            pass

        return ''

    @kodimon.RegisterPath('^/play/$')
    def _play(self, path, params, re_match):
        track_id = params.get('id', '')
        if not track_id:
            raise kodimon.KodimonException('Missing if for audio file')

        json_data = self._client.get_track_url(track_id)
        location = json_data.get('location')
        if not location:
            raise kodimon.KodimonException("Could not get url for trask '%s'" % track_id)

        item = kodimon.AudioItem(track_id, location)
        return item

    def _do_collection(self, json_data, path, params):

        self.set_content_type(constants.CONTENT_TYPE_SONGS)

        """
        Helper function to display the items of a collection
        :param json_data:
        :param path:
        :param params:
        :return:
        """
        result = []

        collection = json_data.get('collection', [])
        for item in collection:
            kind = item.get('kind', '')
            if kind == 'user':
                image = self._get_hires_image(item['avatar_url'])
                user_item = DirectoryItem('[B]'+item['username']+'[/B]',
                                          self.create_uri(['user', str(item['id'])]),
                                          image=image)
                user_item.set_fanart(self.get_fanart())
                result.append(user_item)
            elif kind == 'track':
                # some tracks don't provide an artwork so we do it like soundclound and return the avatar of the user
                image = item.get('artwork_url', '')
                if not image:
                    image = item.get('user', {}).get('avatar_url', '')
                    pass
                if image:
                    image = self._get_hires_image(image)
                    pass

                title = item['title']
                audio_item = AudioItem(title,
                                       self.create_uri('play', {'id': unicode(item['id'])}),
                                       image=image)
                audio_item.set_fanart(self.get_fanart())

                # title
                audio_item.set_title(title)

                # genre
                audio_item.set_genre(item.get('genre', ''))

                # duration
                audio_item.set_duration_in_milli_seconds(item.get('duration', 0))

                # artist
                audio_item.set_artist_name(item.get('user', {}).get('username', ''))

                # year
                audio_item.set_year(self._get_track_year(item))

                result.append(audio_item)
                pass
            pass

        # test for next page
        next_href = json_data.get('next_href', '')
        page = int(params.get('page', 1))
        if next_href and len(collection) > 0:
            next_page_item = self.create_next_page_item(page,
                                                        ['raw/collection', next_href])
            result.append(next_page_item)
            pass

        return result

    @kodimon.RegisterPath('^/raw/collection/(?P<url>.*)/$')
    def _on_raw_collection(self, path, params, re_match):
        """
        All collection urls can directly go to this function.
        For example the 'next_href' in collections to get the result of the next page.
        :param path:
        :param params:
        :param re_match:
        :return:
        """
        url = re_match.group('url')
        json_data = self._client.execute_raw(url)
        return self._do_collection(json_data, path, params)

    def on_search(self, search_text, path, params, re_match):
        json_data = self._client.search(search_text)
        return self._do_collection(json_data, path, params)

    def on_root(self, path, params, re_match):
        result = []

        # search
        search_item = DirectoryItem(self.localize(self.LOCAL_SEARCH),
                                    self.create_uri([self.PATH_SEARCH, 'list']),
                                    image=self.create_resource_path('media', 'search.png'))
        search_item.set_fanart(self.get_fanart())
        result.append(search_item)

        return result

    pass
