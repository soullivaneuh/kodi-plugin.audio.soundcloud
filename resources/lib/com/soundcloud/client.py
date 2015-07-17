__author__ = 'bromix'

from resources.lib.org.bromix import nightcrawler
from resources.lib.org.bromix.nightcrawler.exception import NightcrawlerException
from . import items

"""
class ClientException(kodion.KodionException):
    def __init__(self, status_code, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
        self._status_code = status_code
        pass

    def get_status_code(self):
        return self._status_code

    pass
"""


class Client(nightcrawler.HttpClient):
    CLIENT_ID = '40ccfee680a844780a41fbe23ea89934'
    CLIENT_SECRET = '26a5240f7ee0ee2d4fa9956ed80616c2'

    def __init__(self, username='', password='', access_token='', client_id='', client_secret='', items_per_page=50):
        nightcrawler.HttpClient.__init__(self, default_header={'Accept-Encoding': 'gzip',
                                                               'Host': 'api.soundcloud.com:443',
                                                               'Connection': 'Keep-Alive',
                                                               'User-Agent': 'SoundCloud-Android/14.10.01-27 (Android 4.4.4; samsung GT-I9100'})
        self._username = username
        self._password = password
        self._access_token = access_token
        self._items_per_page = items_per_page

        # set client id with fallback
        self._client_id = self.CLIENT_ID
        if client_id:
            self._client_id = client_id
            pass

        # set client secret with fallback
        self._client_secret = self.CLIENT_SECRET
        if client_secret:
            self._client_secret = client_secret
            pass
        pass

    def _create_url(self, path, user_id=None):
        if user_id:
            if user_id == 'me':
                path = 'me/%s' % path.strip('/')
                pass
            else:
                path = 'users/%s/%s' % (user_id, path.strip('/'))
                pass
            pass

        return 'https://api.soundcloud.com:443/%s' % path

    def _create_params(self, page=1):
        params = {'limit': str(self._items_per_page)}
        if page > 1:
            params['offset'] = str((page - 1) * self._items_per_page)
            pass
        return params

    def _handle_error(self, response):
        pass

    def resolve_url(self, url):
        params = {'url': url}
        response = self._request(self._create_url('resolve'),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_item(response.json())

    def get_user(self, user_id):
        #self.update_access_token()
        response = self._request(self._create_url('', user_id=user_id),
                                 headers={'Accept': 'application/json'})
        self._handle_error(response)
        return items.convert_to_item(response.json())

    def get_track(self, track_id):
        response = self._request(self._create_url('tracks/%s' % unicode(track_id)),
                                 headers={'Accept': 'application/json'})
        self._handle_error(response)
        return items.convert_to_item(response.json())

    def get_track_url(self, track_id):
        response = self._request(self._create_url('tracks/%s/stream' % unicode(track_id)),
                                 headers={'Accept': 'application/json'}, allow_redirects=False)
        self._handle_error(response)
        if response.status_code == 302:
            return response.headers['location']

        return response.url

    def get_trending(self, category='music', page=1):
        if not category.lower() in ['music', 'audio']:
            raise NightcrawlerException('Unknown category "%s"' % category)

        params = self._create_params(page)
        response = self._request(self._create_url('app/mobileapps/suggestions/tracks/popular/%s' % category),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json(), mobile_conversion=True)

    def get_genre(self, genre, page=1):
        params = self._create_params(page)
        response = self._request(self._create_url('app/mobileapps/suggestions/tracks/categories/%s' % genre),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json(), mobile_conversion=True)

    def get_categories(self):
        def _process_category(_category, _result, _json_data):
            for _item in _json_data:
                _result.append({'type': 'folder',
                                'title': _item['title']})
                pass
            pass

        response = self._request(self._create_url('app/mobileapps/suggestions/tracks/categories'),
                                 headers={'Accept': 'application/json'})
        self._handle_error(response)

        json_data = response.json()
        result = {'audio': [], 'music': []}
        for key in result:
            _process_category(key, result[key], json_data.get(key, []))
            pass

        return result

    def get_recommended_for_track(self, track_id, page=1):
        params = self._create_params(page)
        params['linked_partitioning'] = '1'
        response = self._request(self._create_url('tracks/%s/related' % str(track_id)),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    def get_tracks(self, user_id, page=1):
        params = self._create_params(page)
        params['linked_partitioning'] = '1'
        response = self._request(self._create_url('tracks', user_id=user_id),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    def get_favorites(self, user_id, page=1):
        params = self._create_params(page)
        params['linked_partitioning'] = '1'
        response = self._request(self._create_url('favorites', user_id=user_id),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    def get_following(self, user_id, page=1):
        params = self._create_params(page)
        params['linked_partitioning'] = '1'
        response = self._request(self._create_url('followings', user_id=user_id),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    def get_follower(self, user_id, page=1):
        params = self._create_params(page)
        params['linked_partitioning'] = '1'
        response = self._request(self._create_url('followers', user_id=user_id),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    def get_playlist(self, playlist_id):
        response = self._request(self._create_url('playlists/%s' % unicode(playlist_id)),
                                 headers={'Accept': 'application/json'})
        self._handle_error(response)
        json_result = response.json()

        # we transform the result of the playlist, so we can use the common method
        json_result['collection'] = json_result['tracks']
        return items.convert_to_items(json_result, process_tracks_of_playlist=True)

    def get_playlists(self, user_id, page=1):
        params = self._create_params(page)
        params['linked_partitioning'] = '1'
        response = self._request(self._create_url('playlists', user_id=user_id),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    def get_likes(self, user_id, page=1):
        params = self._create_params(page)
        params['linked_partitioning'] = '1'
        if page > 1:
            params['page_size'] = params['offset']
            params['page_number'] = unicode(page)
            pass

        response = self._request(self._create_url('e1/users/%s/likes' % unicode(user_id)),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    def search(self, search_text, category='sounds', page=1):

        if not category in ['sounds', 'people', 'sets']:
            raise NightcrawlerException('Unknown category "%s"' % category)

        params = {'limit': str(self._items_per_page),
                  'q': search_text}
        if page > 1:
            params['offset'] = str((page - 1) * self._items_per_page)
            pass

        response = self._request(self._create_url('search/%s' % category),
                                 headers={'Accept': 'application/json'},
                                 params=params)
        self._handle_error(response)
        return items.convert_to_items(response.json())

    # ===============================================================

    def get_stream(self, page_cursor=None):
        params = {'limit': unicode(self._items_per_page)}
        if page_cursor is not None:
            params['cursor'] = page_cursor

        return self._perform_request(path='me/activities/tracks/affiliated',
                                     headers={'Accept': 'application/json'},
                                     params=params)

    def like_track(self, track_id, like=True):
        method = 'PUT'
        if not like:
            method = 'DELETE'
            pass

        return self._perform_request(method=method,
                                     path='e1/me/track_likes/%s' % unicode(track_id),
                                     headers={'Accept': 'application/json'})

    def like_playlist(self, playlist_id, like=True):
        method = 'PUT'
        if not like:
            method = 'DELETE'
            pass

        return self._perform_request(method=method,
                                     path='e1/me/playlist_likes/%s' % unicode(playlist_id),
                                     headers={'Accept': 'application/json'})

    def follow_user(self, user_id, follow=True):
        method = 'PUT'
        if not follow:
            method = 'DELETE'
            pass

        return self._perform_request(method=method,
                                     path='me/followings/%s' % unicode(user_id),
                                     headers={'Accept': 'application/json'})

    def get_access_token(self):
        return self._access_token

    def _request(self, url, method='GET', headers=None, post_data=None, params=None, allow_redirects=True):
        if not params:
            params = {}
            pass

        if self._client_id:
            params['client_id'] = self._client_id
            pass

        if not headers:
            headers = {}
            pass

        if self._access_token:
            headers['Authorization'] = 'OAuth %s' % self._access_token
            pass

        return super(Client, self)._request(url, method, headers, post_data, params, allow_redirects)

    def update_access_token(self):
        if not self._access_token and self._username and self._password:
            post_data = {'grant_type': 'password',
                         'client_id': self._client_id,
                         'client_secret': self._client_secret,
                         'username': self._username.encode('utf-8'),
                         'password': self._password.encode('utf-8'),
                         'scope': 'non-expiring'}

            json_data = self._perform_request(method='POST', path='oauth2/token', post_data=post_data)
            self._access_token = json_data.get('access_token', None)
            return self._access_token

        return ''

    pass