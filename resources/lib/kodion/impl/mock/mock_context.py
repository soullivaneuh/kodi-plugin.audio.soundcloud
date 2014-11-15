__author__ = 'bromix'

import tempfile

from ..abstract_context import AbstractContext
from .mock_settings import MockSettings
from .mock_context_ui import MockContextUI
from ...logging import log


class MockContext(AbstractContext):
    def __init__(self, path=u'/', params=None, plugin_name='MOCK Plugin', plugin_id='mock.plugin', ):
        AbstractContext.__init__(self, path, params, plugin_name, plugin_id)

        self._data_path = tempfile.gettempdir()
        self._settings = MockSettings()
        self._dict_localization = {5000: u'Hello World',
                                   5001: u'MOCK Plugin'}

        self._ui = None
        pass

    def get_ui(self):
        if not self._ui:
            self._ui = MockContextUI()
            pass
        return self._ui

    def get_handle(self):
        return 666

    def get_data_path(self):
        return self._data_path

    def get_native_path(self):
        return 'virtual_path'

    def get_settings(self):
        return self._settings

    def localize(self, text_id, default_text=u''):
        return self._dict_localization.get(text_id, default_text)

    def set_content_type(self, content_type):
        log("Set ContentType to '%s'" % content_type)
        pass

    def add_sort_method(self, *sort_methods):
        for sort_method in sort_methods:
            log("add SortMethod '%s'" % (str(sort_method)))
            pass
        pass

    def clone(self, new_path=None, new_params=None):
        if not new_path:
            new_path = self.get_path()
            pass

        if not new_params:
            new_params = self.get_params()
            pass

        return MockContext(path=new_path, params=new_params, plugin_name=self._plugin_name, plugin_id=self._plugin_id)

    pass