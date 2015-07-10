__author__ = 'bromix'

from resources.lib.org.bromix import nightcrawler
from resources.lib.com import soundcloud

nightcrawler.run(soundcloud.Provider())
