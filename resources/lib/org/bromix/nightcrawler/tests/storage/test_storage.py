__author__ = 'bromix'

import os
import unittest
import tempfile


from resources.lib.org.bromix.nightcrawler.storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self._filename = os.path.join(tempfile.gettempdir(), 'kodion', '_storage')
        pass

    def test_clear(self):
        storage = Storage(self._filename)
        data = {'name': 'Hellraiser',
                'id': 12345}

        storage._set(12345, data)
        storage.sync()
        storage._clear()
        storage.sync()
        pass

    def test_set_item(self):
        storage = Storage(self._filename)

        data = {'name': 'Hellraiser',
                'id': 12345}

        storage._set(12345, data)

        data2 = storage._get(12345)[0]
        self.assertEqual('Hellraiser', data2['name'])
        self.assertEqual(12345, data2['id'])
        pass

    pass
