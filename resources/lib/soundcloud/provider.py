import re

__author__ = 'bromix'

from resources.lib.kodimon import DirectoryItem
from resources.lib import kodimon


class Provider(kodimon.AbstractProvider):
    def __init__(self):
        kodimon.AbstractProvider.__init__(self)

        from resources.lib import soundcloud
        self._client = soundcloud.Client()
        pass

    def _get_hires_image(self, url):
        return re.sub('(.*)(-large.jpg\?.*)', r'\1-t500x500.jpg', url)

    def _do_collection(self, json_collection):
        result = []

        for item in json_collection:
            kind = item.get('kind', '')
            if kind == 'user':
                image = self._get_hires_image(item['avatar_url'])
                user_item = DirectoryItem('[B]'+item['username']+'[/B]',
                                          self.create_uri(['user', str(item['id'])]),
                                          image=image)
                user_item.set_fanart(self.get_fanart())
                result.append(user_item)
                pass
            pass

        return result

    @kodimon.RegisterPath('^/raw/collection/(?P<url>.*)/$')
    def _on_raw_collection(self, path, params, re_match):
        url = re_match.group('url')
        json_data = self._client.execute_raw(url)
        collection = json_data.get('collection', [])

        result = self._do_collection(collection)

        # test for next page
        next_href = json_data.get('next_href', '')
        page = int(params.get('page', 1))
        if next_href:
            next_page_item = self.create_next_page_item(page,
                                                        ['raw/collection', next_href])
            result.append(next_page_item)
            pass

        return result

    def on_search(self, search_text, path, params, re_match):
        json_data = self._client.search(search_text)
        collection = json_data.get('collection', [])

        result = self._do_collection(collection)

        # test for next page
        page = 1
        next_href = json_data.get('next_href', '')
        if next_href:
            next_page_item = self.create_next_page_item(page,
                                                        ['raw/collection', next_href])
            result.append(next_page_item)
            pass
        return result

    def on_root(self, path, params, re_match):
        result = []

        # search
        search_item = DirectoryItem(self.localize(self.LOCAL_SEARCH),
                                    self.create_uri([self.PATH_SEARCH, 'list']),
                                    image=self.create_resource_path('media', 'search.png'))
        search_item.set_fanart(self.get_plugin().get_fanart())
        result.append(search_item)

        return result

    pass
