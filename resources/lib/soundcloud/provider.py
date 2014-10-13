__author__ = 'bromix'

from resources.lib.kodimon import DirectoryItem
from resources.lib import kodimon


class Provider(kodimon.AbstractProvider):
    def __init__(self):
        kodimon.AbstractProvider.__init__(self)

        from resources.lib import soundcloud
        self._client = soundcloud.Client()
        pass

    def on_search(self, search_text, path, params, re_match):

        return False

    def on_root(self, path, params, re_match):
        result = []

        # search
        search_item = DirectoryItem(self.localize(self.LOCAL_SEARCH),
                                    self.PATH_SEARCH,
                                    image=self.create_resource_path('media', 'search.png'))
        search_item.set_fanart(self.get_plugin().get_fanart())
        result.append(search_item)

        return result

    pass
