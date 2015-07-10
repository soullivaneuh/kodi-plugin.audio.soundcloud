import re

__author__ = 'bromix'

from resources.lib.org.bromix import nightcrawler
from resources.lib.org.bromix.nightcrawler.exception import NightcrawlerException


def _get_hires_image(url):
    return re.sub('(.*)(-large.jpg\.*)(\?.*)?', r'\1-t300x300.jpg', url)


def _get_thumbnail(json_data):
    image_url = json_data.get('artwork_url', '')

    # test avatar image
    if not image_url:
        image_url = json_data.get('avatar_url', '')

    # test tracks (used for playlists)
    if not image_url:
        tracks = json_data.get('tracks', [])
        if len(tracks) > 0:
            return _get_thumbnail(tracks[0])

        # fall back is the user avatar (at least)
        image_url = json_data.get('user', {}).get('avatar_url', '')
        pass

    return _get_hires_image(image_url)


def _convert_to_track_item(json_item):
    def _get_track_year(_item_json):
        # this would be the default info, but is mostly not set :(
        year = _item_json.get('release_year', '')
        if year:
            return year

        # we use a fallback.
        # created_at=2013/03/24 00:32:01 +0000
        re_match = re.match('(?P<year>\d{4})(.*)', _item_json.get('created_at', ''))
        if re_match:
            year = re_match.group('year')
            if year:
                return year
            pass

        return ''

    item = {'type': 'audio',
            'title': nightcrawler.utils.strings.to_unicode(json_item['title']),
            'id': json_item['id'],
            'genre': json_item.get('genre', ''),
            'duration': int(json_item['duration']) / 1000,
            'artist': json_item['user']['username'],
            'user': json_item['user'],
            'year': _get_track_year(json_item),
            'images': {'thumbnail': _get_thumbnail(json_item)}}

    return item


def convert_to_item(json_item):
    kind = json_item.get('kind', '')
    if kind == 'track':
        return _convert_to_track_item(json_item)

    raise NightcrawlerException('Unknown kind of item "%s"' % kind)

    def _get_track_year(collection_item_json):
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

    def _get_image(json_data):
        image_url = json_data.get('artwork_url', '')

        # test avatar image
        if not image_url:
            image_url = json_data.get('avatar_url', '')

        # test tracks (used for playlists)
        if not image_url:
            tracks = json_data.get('tracks', [])
            if len(tracks) > 0:
                return _get_image(tracks[0])

            # fall back is the user avatar (at least)
            image_url = json_data.get('user', {}).get('avatar_url', '')
            pass

        return self._get_hires_image(image_url)


    if kind == 'playlist':
        if process_playlist:
            result = []
            tracks = json_item['tracks']
            track_number = 1
            for track in tracks:
                path = context.get_path()
                track_item = self._do_item(context, track, path)

                # set the name of the playlist for the albumname
                track_item.set_album_name(json_item['title'])

                # based on the position in the playlist we add a track number
                track_item.set_track_number(track_number)
                result.append(track_item)
                track_number += 1
                pass
            return result
        else:
            playlist_item = DirectoryItem(json_item['title'],
                                          context.create_uri(['playlist', unicode(json_item['id'])]),
                                          image=_get_image(json_item))
            playlist_item.set_fanart(self.get_fanart(context))

            if path == '/user/favorites/me/':
                context_menu = [(context.localize(self._local_map['soundcloud.unlike']),
                                 'RunPlugin(%s)' % context.create_uri(['like/playlist', unicode(json_item['id'])],
                                                                      {'like': '0'}))]
            else:
                context_menu = [(context.localize(self._local_map['soundcloud.like']),
                                 'RunPlugin(%s)' % context.create_uri(['like/playlist', unicode(json_item['id'])],
                                                                      {'like': '1'}))]

            playlist_item.set_context_menu(context_menu)
            return playlist_item
        pass
    elif kind == 'user':
        username = json_item['username']
        user_id = unicode(json_item['id'])
        if path == '/':
            user_id = 'me'
            username = '[B]' + username + '[/B]'
            pass
        user_item = DirectoryItem(username,
                                  context.create_uri(['user/tracks', user_id]),
                                  image=_get_image(json_item))
        user_item.set_fanart(self.get_fanart(context))

        if path == '/user/following/me/':
            context_menu = [(context.localize(self._local_map['soundcloud.unfollow']),
                             'RunPlugin(%s)' % context.create_uri(['follow', unicode(json_item['id'])],
                                                                  {'follow': '0'}))]
            pass
        else:
            context_menu = [(context.localize(self._local_map['soundcloud.follow']),
                             'RunPlugin(%s)' % context.create_uri(['follow', unicode(json_item['id'])],
                                                                  {'follow': '1'}))]
            pass
        user_item.set_context_menu(context_menu)
        return user_item
    elif kind == 'like':
        # A like has 'playlist' or 'track' so we find one of them and call this routine again, because the
        # data is same.
        test_playlist = json_item.get('playlist', None)
        if test_playlist is not None:
            return self._do_item(context, test_playlist, path)

        test_track = json_item.get('track', None)
        if test_track is not None:
            return self._do_item(context, test_track, path)
        pass
    elif kind == 'group':
        # at the moment we don't support groups
        """
        group_item = DirectoryItem('Group-Dummy',
                                   '')
        return group_item
        """
        return None


def convert_to_items(json_result, mobile_conversion=False):
    result = {'items': []}

    collection = json_result.get('collection', [])
    for item in collection:
        if mobile_conversion:
            # simple conversion to use the common convert_to_item() method
            user = item.get('_embedded', {}).get('user', {})
            user_id = user['urn'].split(':')[2]
            item['user'] = {'username': user['username'],
                            'id': user_id}

            # create track id of urn
            track_id = item['urn'].split(':')[2]
            item['id'] = track_id

            # is always a track
            item['kind'] = 'track'
            pass

        # test if we have an 'origin' tag. If so we are in the activities
        item = item.get('origin', item)
        result['items'].append(convert_to_item(item))
        pass

    next_href = json_result.get('_links', {}).get('next', {}).get('href', '')
    if next_href and len(result['items']) > 0:
        result['continue'] = True
        pass

    return result