# base exception for the kodimon framework
from .exceptions import KodimonException

# decorator for registering pathes to navigate
from .register_path import RegisterPath

# items for displaying in kodi/xbmc
from .items import *

from abstract_api import *
try:
    from impl.xbmc.xbmc_api import *
    from impl.xbmc.xbmc_plugin import XbmcPlugin as Plugin
    from impl.xbmc.xbmc_abstract_provider import XbmcAbstractProvider as AbstractProvider
except ImportError, ex:
    from impl.mock.mock_api import *
    from impl.mock.mock_plugin import MockPlugin as Plugin
    from impl.mock.mock_abstract_provider import MockAbstractProvider as AbstractProvider
    pass