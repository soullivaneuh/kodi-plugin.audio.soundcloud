import json
import urllib
import urllib2
import urlparse
from resources.lib.soundcloud.requests.api import post

__author__ = 'bromix'

import requests


class Client(object):
    CLIENT_ID = '40ccfee680a844780a41fbe23ea89934'
    CLIENT_SECRET = '26a5240f7ee0ee2d4fa9956ed80616c2'

    def __init__(self, username='', password='', access_token='', client_id='', client_secret=''):
        self._username = username
        self._password = password
        self._access_token = access_token

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

    def _create_path_based_on_user_id(self, me_or_user_id, path):
        """
        Creates the API path based on 'me' otherwise for the given user id
        :param me_or_user_id:
        :param path:
        :return:
        """
        user_id = unicode(me_or_user_id)
        if user_id == 'me':
            return 'me/%s' % path.strip('/')
        return 'users/%s/%s' % (user_id, path.strip('/'))

    def get_trending(self, category='music', page=1, per_page=20):
        page = int(page)
        per_page = int(per_page)

        path = 'app/mobileapps/suggestions/tracks/popular/%s' % category
        params = {'limit': str(per_page)}
        if page > 1:
            params['offset'] = str((page - 1) * per_page)
            pass
        return self._perform_request(path=path,
                                     headers={'Accept': 'application/json'},
                                     params=params)

    def get_genre(self, genre, page=1, per_page=20):
        page = int(page)
        per_page = int(per_page)

        path = 'app/mobileapps/suggestions/tracks/categories/%s' % genre
        params = {'limit': str(per_page)}
        if page > 1:
            params['offset'] = str((page - 1) * per_page)
            pass
        return self._perform_request(path=path,
                                     headers={'Accept': 'application/json'},
                                     params=params)

    def get_categories(self):
        return self._perform_request(path='app/mobileapps/suggestions/tracks/categories',
                                     headers={'Accept': 'application/json'})

    def get_track_url(self, track_id):
        return self._perform_request(path='tracks/%s/stream' % str(track_id),
                                     headers={'Accept': 'application/json'},
                                     allow_redirects=False)

    def search(self, search_text, page=1, per_page=30):
        page = int(page)
        per_page = int(per_page)

        params = {'limit': str(per_page),
                  'q': search_text}
        if page > 1:
            params['offset'] = str((page - 1) * per_page)
            pass
        return self._perform_request(path='search',
                                     headers={'Accept': 'application/json'},
                                     params=params)

    def get_stream(self, page=1, per_page=100):
        page = int(page)
        per_page = int(per_page)

        params = {'limit': str(per_page)}
        if page > 1:
            params['offset'] = str((page - 1) * per_page)
            pass

        self.update_access_token()
        return self._perform_request(path='e1/me/stream',
                                     headers={'Accept': 'application/json'},
                                     params=params)

    def get_me_posts(self):
        self.update_access_token()
        return self._perform_request(path='me/activities',
                                     headers={'Accept': 'application/json'})

    def get_playlists(self, me_or_user_id):
        self.update_access_token()
        path = self._create_path_based_on_user_id(me_or_user_id, 'playlists')
        return self._perform_request(path=path,
                                         headers={'Accept': 'application/json'})

    def get_me_following(self):
        self.update_access_token()
        return self._perform_request(path='me/followings',
                                     headers={'Accept': 'application/json'})

    def get_me(self):
        self.update_access_token()
        return self._perform_request(path='me',
                                     headers={'Accept': 'application/json'})

    def get_access_token(self):
        return self._access_token

    def _perform_request(self, method='GET', headers=None, path=None, post_data=None, params=None,
                         allow_redirects=True):
        # params
        if not params:
            params = {}
            pass
        if self._client_id:
            params['client_id'] = self._client_id
            pass

        # basic header
        _headers = {'Accept-Encoding': 'gzip',
                    'Host': 'api.soundcloud.com:443',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'SoundCloud-Android/14.10.01-27 (Android 4.4.4; samsung GT-I9100'}
        # set access token
        if self._access_token:
            _headers['Authorization'] = 'OAuth %s' % self._access_token
            pass
        if not headers:
            headers = {}
            pass
        _headers.update(headers)

        # url
        _url = 'https://api.soundcloud.com:443/%s' % path

        result = None
        if method == 'GET':
            result = requests.get(_url, params=params, headers=_headers, verify=False, allow_redirects=allow_redirects)
        elif method == 'POST':
            result = requests.post(_url, data=post_data, params=params, headers=_headers, verify=False,
                                   allow_redirects=allow_redirects)
            pass

        if result is None:
            return {}

        return result.json()

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
            pass

        return self._access_token

    pass