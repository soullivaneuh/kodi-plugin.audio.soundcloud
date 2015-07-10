__author__ = 'bromix'

import re

from resources.lib.org.bromix import nightcrawler
from .client import Client


class Provider(nightcrawler.Provider):
    SOUNDCLOUD_LOCAL_EXPLORE = 30500
    SOUNDCLOUD_LOCAL_RECOMMENDED = 30517
    SOUNDCLOUD_LOCAL_GO_TO_USER = 30516
    SOUNDCLOUD_LOCAL_PLAYLISTS = 30506
    SOUNDCLOUD_LOCAL_PEOPLE = 30515
    SOUNDCLOUD_LOCAL_LIKES = 30510
    SOUNDCLOUD_LOCAL_FOLLOWING = 30507
    SOUNDCLOUD_LOCAL_FOLLOWER = 30509

    SOUNDCLOUD_LOCAL_MUSIC_TRENDING = 30501
    SOUNDCLOUD_LOCAL_AUDIO_TRENDING = 30502
    SOUNDCLOUD_LOCAL_MUSIC_GENRE = 30503
    SOUNDCLOUD_LOCAL_AUDIO_GENRE = 30504

    SETTINGS_USER_ID = 'soundcloud.user.id'

    def __init__(self):
        nightcrawler.Provider.__init__(self)

        self._is_logged_in = False
        self._client = None
        """
        self._local_map.update(
             'soundcloud.stream': 30505,
             'soundcloud.follow': 30508,
             'soundcloud.like': 30511,
             'soundcloud.tracks': 30512,
             'soundcloud.unfollow': 30513,
             'soundcloud.unlike': 30514,
        )
        """
        pass

    def on_setup(self, mode):
        if mode == 'content-type':
            return ['default', 'songs', 'artists', 'albums']

        return None

    def get_client_old(self, context):
        access_manager = context.get_access_manager()
        access_token = access_manager.get_access_token()
        if access_manager.is_new_login_credential() or not access_token:
            access_manager.update_access_token('')  # in case of an old access_token
            self._client = None
            pass

        if not self._client:
            items_per_page = context.get_settings().get_items_per_page()
            if access_manager.has_login_credentials():
                username, password = access_manager.get_login_credentials()
                access_token = access_manager.get_access_token()

                # create a new access_token
                if not access_token:
                    self._client = Client(username=username, password=password, access_token='',
                                          items_per_page=items_per_page)
                    access_token = self._client.update_access_token()
                    access_manager.update_access_token(access_token)
                    pass

                self._is_logged_in = access_token != ''
                self._client = Client(username=username, password=password, access_token=access_token,
                                      items_per_page=items_per_page)
            else:
                self._client = Client(items_per_page=items_per_page)
                pass
            pass

        return self._client

    def handle_exception(self, context, exception_to_handle):
        return None

        if isinstance(exception_to_handle, ClientException):
            if exception_to_handle.get_status_code() == 401:
                context.get_access_manager().update_access_token('')
                context.get_ui().show_notification('Login Failed')
                context.get_ui().open_settings()
                return False
            pass

        return True

    # @kodion.RegisterProviderPath('^/play/$')
    def _on_play(self, context, re_match):
        params = context.get_params()
        url = params.get('url', '')
        audio_id = params.get('audio_id', '')

        client = self.get_client(context)
        result = None
        update_playlist = False
        if url and not audio_id:
            json_data = client.resolve_url(url)
            path = context.get_path()
            result = self._do_item(context, json_data, path, process_playlist=True)
            if isinstance(result, AudioItem):
                audio_id = json_data['id']
                update_playlist = True
                pass
            elif isinstance(result, list):
                playlist = context.get_audio_playlist()
                playlist.clear()
                for track in result:
                    playlist.add(track)
                    pass
                return result[0]
            pass
        elif audio_id:
            json_data = client.get_track(audio_id)
            path = context.get_path()
            result = self._do_item(context, json_data, path, process_playlist=True)
            pass
        else:
            raise kodion.KodionException("Audio ID or URL missing")

        json_data = client.get_track_url(audio_id)
        location = json_data.get('location')
        if not location:
            raise kodion.KodionException("Could not get url for track '%s'" % audio_id)

        result.set_uri(location.encode('utf-8'))
        if update_playlist:
            playlist = context.get_audio_playlist()
            playlist.clear()
            playlist.add(result)
            pass

        return result

    #@kodion.RegisterProviderPath('^\/stream\/$')
    def _on_stream(self, context, re_match):
        result = []

        params = context.get_params()
        cursor = params.get('cursor', None)
        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE * 5, self.get_client(context).get_stream,
                                                     page_cursor=cursor)
        path = context.get_path()
        result = self._do_collection(context, json_data, path, params)
        return result

    #@kodion.RegisterProviderPath('^\/playlist\/(?P<playlist_id>.+)/$')
    def _on_playlist(self, context, re_match):
        context.set_content_type(kodion.constants.content_type.SONGS)
        result = []

        playlist_id = re_match.group('playlist_id')
        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE, self.get_client(context).get_playlist,
                                                     playlist_id)

        path = context.get_path()
        result.extend(self._do_item(context, json_data, path, process_playlist=True))
        return result

    #@kodion.RegisterProviderPath('^\/user/playlists\/(?P<user_id>.+)/$')
    def _on_playlists(self, context, re_match):
        user_id = re_match.group('user_id')
        params = context.get_params()
        page = params.get('page', 1)
        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE, self.get_client(context).get_playlists,
                                                     user_id,
                                                     page=page)
        path = context.get_path()
        return self._do_collection(context, json_data, path, params, content_type=kodion.constants.content_type.ALBUMS)

    #@kodion.RegisterProviderPath('^\/user/following\/(?P<user_id>.+)/$')
    def _on_following(self, context, re_match):
        user_id = re_match.group('user_id')
        params = context.get_params()
        page = params.get('page', 1)
        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE, self.get_client(context).get_following,
                                                     user_id,
                                                     page=page)
        path = context.get_path()
        return self._do_collection(context, json_data, path, params, content_type=kodion.constants.content_type.ARTISTS)

    #@kodion.RegisterProviderPath('^\/user/follower\/(?P<user_id>.+)/$')
    def _on_follower(self, context, re_match):
        user_id = re_match.group('user_id')
        params = context.get_params()
        page = params.get('page', 1)
        json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE, self.get_client(context).get_follower,
                                                     user_id,
                                                     page=page)
        path = context.get_path()
        return self._do_collection(context, json_data, path, params, content_type=kodion.constants.content_type.ARTISTS)

    #@kodion.RegisterProviderPath('^\/follow\/(?P<user_id>.+)/$')
    def _on_follow(self, context, re_match):
        user_id = re_match.group('user_id')
        params = context.get_params()
        follow = params.get('follow', '') == '1'
        json_data = self.get_client(context).follow_user(user_id, follow)

        return True

    #@kodion.RegisterProviderPath('^\/like\/(?P<category>\w+)\/(?P<content_id>.+)/$')
    def _on_like(self, context, re_match):
        content_id = re_match.group('content_id')
        category = re_match.group('category')
        params = context.get_params()
        like = params.get('like', '') == '1'

        if category == 'track':
            json_data = self.get_client(context).like_track(content_id, like)
        elif category == 'playlist':
            json_data = self.get_client(context).like_playlist(content_id, like)
        else:
            raise kodion.KodionException("Unknown category '%s' in 'on_like'" % category)

        if not like:
            context.get_ui().refresh_container()
            pass

        return True

    #@kodion.RegisterProviderPath('^\/user/favorites\/(?P<user_id>.+)/$')
    def _on_favorites(self, context, re_match):
        user_id = re_match.group('user_id')

        # We use an API of th APP, this API only work with an user id. In the case of 'me' we gave to get our own
        # user id to use this function.
        if user_id == 'me':
            json_data = context.get_function_cache().get(FunctionCache.ONE_MINUTE * 10,
                                                         self.get_client(context).get_user,
                                                         'me')
            user_id = json_data['id']
            pass

        params = context.get_params()
        page = params.get('page', 1)
        # do not cache: in case of adding or deleting content
        json_data = self.get_client(context).get_likes(user_id, page=page)
        path = context.get_path()
        return self._do_collection(context, json_data, path, params)

    # ===================================

    def get_fanart(self, context):
        if context.get_settings().get_bool('soundcloud.fanart_dark.show', True):
            return context.create_resource_path('media/fanart_dark.jpg')
        return context.create_resource_path('media/fanart.jpg')

    def get_client(self, context):
        if self._client:
            return self._client

        # TODO: login
        self._client = Client()
        return self._client

    def process_result(self, context, result):
        items = []

        path = context.get_path()
        for item in result['items']:
            # TODO: update context menu based on login and path
            context_menu = []

            if item['type'] == 'audio':
                # recommended tracks
                context_menu.append((context.localize(self.SOUNDCLOUD_LOCAL_RECOMMENDED),
                                     'Container.Update(%s)' % context.create_uri(
                                         '/explore/recommended/tracks/%s' % unicode(item['id']))))

                # like/unlike a track
                """
                if path == '/user/favorites/me/':
                    context_menu.append((context.localize(self._local_map['soundcloud.unlike']),
                                         'RunPlugin(%s)' % context.create_uri(['like/track', unicode(json_item['id'])],
                                                                              {'like': '0'})))
                    pass
                else:
                    context_menu.append((context.localize(self._local_map['soundcloud.like']),
                                         'RunPlugin(%s)' % context.create_uri(['like/track', unicode(json_item['id'])],
                                                                              {'like': '1'})))
                    pass
                """

                # go to user
                username = nightcrawler.utils.strings.to_unicode(item['user']['username'])
                user_id = nightcrawler.utils.strings.to_unicode(item['user']['id'])
                if path != '/user/tracks/%s/' % user_id:
                    context_menu.append((
                        context.localize(self.SOUNDCLOUD_LOCAL_GO_TO_USER) % ('[B]%s[/B]' % username),
                        'Container.Update(%s)' % context.create_uri('/user/tracks/%s/' % user_id)))
                    pass
                pass

            if context_menu:
                item['context-menu'] = {'items': context_menu}
                pass

            # playback uri
            item['uri'] = context.create_uri('play', {'audio_id': unicode(item['id'])})
            item['images']['fanart'] = self.get_fanart(context)
            items.append(item)
            pass

        # TODO: next page for mobile and normal request
        if result.get('continue', False):
            items.append(nightcrawler.items.create_next_page_item(context, fanart=self.get_fanart(context)))
            pass
        return items

    @nightcrawler.register_context_value('category', unicode, default='sounds')
    @nightcrawler.register_context_value('page', int, default=1)
    def on_search(self, context, search_text, category, page):
        result = []

        # first page of search
        if page == 1 and category == 'sounds':
            people_params = {}
            people_params.update(context.get_params())
            people_params['category'] = 'people'
            result.append({'type': 'folder',
                           'title': '[B]%s[/B]' % context.localize(self.SOUNDCLOUD_LOCAL_PEOPLE),
                           'uri': context.create_uri(context.get_path(), people_params),
                           'images': {'thumbnail': context.create_resource_path('media/users.png'),
                                      'fanart': self.get_fanart(context)}})

            playlist_params = {}
            playlist_params.update(context.get_params())
            playlist_params['category'] = 'sets'
            result.append({'type': 'folder',
                           'title': '[B]%s[/B]' % context.localize(self.SOUNDCLOUD_LOCAL_PLAYLISTS),
                           'uri': context.create_uri(context.get_path(), playlist_params),
                           'images': {'thumbnail': context.create_resource_path('media/playlists.png'),
                                      'fanart': self.get_fanart(context)}})

            pass

        search_result = self.get_client(context).search(search_text, category, page=page)
        result.extend(self.process_result(context, search_result))
        return result

    @nightcrawler.register_path('/user/tracks/(?P<user_id>.+)/')
    @nightcrawler.register_path_value('user_id', unicode)
    @nightcrawler.register_context_value('page', int, default=1)
    def on_user_tracks(self, context, user_id, page):
        context.set_content_type(context.CONTENT_TYPE_SONGS)
        result = []

        # on the first page add some extra stuff to navigate to
        # TODO: add Likes, Following and Follower
        if page == 1:
            # TODO: get correct user image
            #json_data = self.get_client(context).get_user(user_id)
            #user_image = json_data.get('avatar_url', '')
            #user_image = self._get_hires_image(user_image)
            user_image = u''

            # playlists
            result.append({'type': 'folder',
                           'title': context.localize(self.SOUNDCLOUD_LOCAL_PLAYLISTS),
                           'uri': context.create_uri('/user/playlists/%s' % user_id),
                           'images': {'thumbnail': user_image,
                                      'fanart': self.get_fanart(context)}})

            # likes
            result.append({'type': 'folder',
                           'title': context.localize(self.SOUNDCLOUD_LOCAL_LIKES),
                           'uri': context.create_uri('/user/favorites/%s' % user_id),
                           'images': {'thumbnail': user_image,
                                      'fanart': self.get_fanart(context)}})

            # following
            result.append({'type': 'folder',
                           'title': context.localize(self.SOUNDCLOUD_LOCAL_FOLLOWING),
                           'uri': context.create_uri('/user/following/%s' % user_id),
                           'images': {'thumbnail': user_image,
                                      'fanart': self.get_fanart(context)}})

            # follower
            result.append({'type': 'folder',
                           'title': context.localize(self.SOUNDCLOUD_LOCAL_FOLLOWER),
                           'uri': context.create_uri('/user/follower/%s' % user_id),
                           'images': {'thumbnail': user_image,
                                      'fanart': self.get_fanart(context)}})
            pass

        tracks_result = self.get_client(context).get_tracks(user_id, page=page)
        result.extend(self.process_result(context, tracks_result))
        return result

    @nightcrawler.register_path('/explore/recommended/tracks\/(?P<track_id>.+)/')
    @nightcrawler.register_path_value('track_id', unicode)
    @nightcrawler.register_context_value('page', int, default=1)
    def on_explore_recommended_tracks(self, context, track_id, page):
        context.set_content_type(context.CONTENT_TYPE_SONGS)

        result = self.get_client(context).get_recommended_for_track(track_id, page=page)
        return self.process_result(context, result)

    @nightcrawler.register_path('/explore/genre/(?P<category>music|audio)/(?P<genre>.*)/')
    @nightcrawler.register_path_value('category', unicode)
    @nightcrawler.register_path_value('genre', unicode)
    @nightcrawler.register_context_value('page', int, default=1)
    def on_explore_genre_sub(self, context, category, genre, page):
        context.set_content_type(context.CONTENT_TYPE_SONGS)

        result = self.get_client(context).get_genre(genre=genre, page=page)
        return self.process_result(context, result)

    @nightcrawler.register_path('/explore/genre/(?P<category>music|audio)/')
    @nightcrawler.register_path_value('category', unicode)
    def on_explore_genre(self, context, category):
        categories = self.get_client(context).get_categories()
        items = categories.get(category, [])
        result = []
        for item in items:
            item.update({'uri': context.create_uri('/explore/genre/%s/%s/' % (category, item['title'])),
                         'images': {'fanart': self.get_fanart(context),
                                    'thumbnail': context.create_resource_path('media/%s.png' % category)}})
            result.append(item)
            pass

        return result

    @nightcrawler.register_path('/explore/trending/(?P<category>music|audio)/')
    @nightcrawler.register_path_value('category', unicode)
    @nightcrawler.register_context_value('page', int, default=1)
    def on_explore_trending(self, context, category, page):
        context.set_content_type(context.CONTENT_TYPE_SONGS)

        result = self.get_client(context).get_trending(category=category, page=page)
        return self.process_result(context, result)

    @nightcrawler.register_path('/explore/')
    def on_explore(self, context):
        result = []

        # trending music
        result.append({'type': 'folder',
                       'title': context.localize(self.SOUNDCLOUD_LOCAL_MUSIC_TRENDING),
                       'uri': context.create_uri('explore/trending/music'),
                       'images': {'thumbnail': context.create_resource_path('media/music.png'),
                                  'fanart': self.get_fanart(context)}})

        # trending audio
        result.append({'type': 'folder',
                       'title': context.localize(self.SOUNDCLOUD_LOCAL_AUDIO_TRENDING),
                       'uri': context.create_uri('explore/trending/audio'),
                       'images': {'thumbnail': context.create_resource_path('media/audio.png'),
                                  'fanart': self.get_fanart(context)}})

        # genre music
        result.append({'type': 'folder',
                       'title': context.localize(self.SOUNDCLOUD_LOCAL_MUSIC_GENRE),
                       'uri': context.create_uri('explore/genre/music'),
                       'images': {'thumbnail': context.create_resource_path('media/music.png'),
                                  'fanart': self.get_fanart(context)}})

        # genre audio
        result.append({'type': 'folder',
                       'title': context.localize(self.SOUNDCLOUD_LOCAL_AUDIO_GENRE),
                       'uri': context.create_uri('explore/genre/audio'),
                       'images': {'thumbnail': context.create_resource_path('media/audio.png'),
                                  'fanart': self.get_fanart(context)}})
        return result

    @nightcrawler.register_path('/')
    def on_root(self, context):
        result = []

        client = self.get_client(context)

        # is logged in?
        """
        if self._is_logged_in:
            # track
            json_data = self.get_client(context).get_user('me')
            me_item = self._do_item(context, json_data, path)
            result.append(me_item)

            # stream
            stream_item = DirectoryItem(context.localize(self._local_map['soundcloud.stream']),
                                        context.create_uri(['stream']),
                                        image=context.create_resource_path('media', 'stream.png'))
            stream_item.set_fanart(self.get_fanart(context))
            result.append(stream_item)
            pass
            """

        # search
        result.append(nightcrawler.items.create_search_item(context, fanart=self.get_fanart(context)))

        # explore
        result.append({'type': 'folder',
                       'title': context.localize(self.SOUNDCLOUD_LOCAL_EXPLORE),
                       'uri': context.create_uri('explore'),
                       'images': {'thumbnail': context.create_resource_path('media/explore.png'),
                                  'fanart': self.get_fanart(context)}})
        return result

    def _do_collection(self, context, json_data, path, params, content_type):
        context.set_content_type(content_type)

        """
            Helper function to display the items of a collection
            :param json_data:
            :param path:
            :param params:
            :return:
            """
        result = []

        collection = json_data.get('collection', [])
        for collection_item in collection:
            # test if we have an 'origin' tag. If so we are in the activities
            item = collection_item.get('origin', collection_item)
            base_item = self._do_item(context, item, path)
            if base_item is not None:
                result.append(base_item)
                pass
            pass

        # test for next page
        next_href = json_data.get('next_href', '')
        if next_href:
            re_match = re.match(r'.*cursor=(?P<cursor>[a-z0-9-]+).*', next_href)
            if re_match:
                params['cursor'] = re_match.group('cursor')
                pass
            pass

        page = int(params.get('page', 1))
        if next_href and len(collection) > 0:
            next_page_item = kodion.items.NextPageItem(context, page)
            next_page_item.set_fanart(self.get_fanart(context))
            result.append(next_page_item)
            pass

        return result

    pass
