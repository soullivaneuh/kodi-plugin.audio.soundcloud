import json
import urllib
import urllib2

__author__ = 'bromix'


class Client(object):
    CLIENT_ID = '40ccfee680a844780a41fbe23ea89934'
    CLIENT_SECRET = '26a5240f7ee0ee2d4fa9956ed80616c2'

    def __init__(self, username=None, password=None, client_id=None, client_secret=None, access_token=None):
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

    def get_access_token(self):
        return self._access_token

    def _perform_request(self, path, query=None, post_data=None):
        url = 'https://api.soundcloud.com:443/%s' % path

        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Host': 'api.soundcloud.com:443',
                   'Connection': 'Keep-Alive',
                   'User-Agent': 'SoundCloud-Android/14.10.01-27 (Android 4.4.4; samsung GT-I9100)'}

        # set the token
        if self._access_token:
            headers['Authorization'] = 'OAuth %s' % self._access_token
            headers['Accept'] = 'application/json'
            pass

        if not query:
            query = {}
            pass

        # set client id if exists and token also exists
        if self._access_token and self._client_id:
            query['client_id'] = self._client_id
            pass

        # add query to url
        if len(query) > 0:
            url = url + '?' + urllib.urlencode(query)
            pass


        # prepare post data
        _post_data = None
        if post_data is not None:
            _post_data = urllib.urlencode(post_data)
            pass

        # create request
        request = urllib2.Request(url, _post_data, headers=headers)
        response = urllib2.urlopen(request)

        return response

    def _perform_request_json(self, path, query=None, post_data=None):
        content = self._perform_request(path, query, post_data)
        return json.load(content, encoding='utf-8')

    def update_access_token(self):
        if self._access_token is None and self._username and self._password:
            post_data = {'grant_type': 'password',
                         'client_id': self._client_id,
                         'client_secret': self._client_secret,
                         'username': self._username.encode('utf-8'),
                         'password': self._password.encode('utf-8'),
                         'scope': 'non-expiring'}

            json_data = self._perform_request_json('oauth2/token', query=None, post_data=post_data)
            self._access_token = json_data.get('access_token', None)
            pass

        return self._access_token

    def get_me(self):
        self.update_access_token()
        return self._perform_request_json('me')

    pass