from resources.lib.kodion import runner
from resources.lib.com import soundcloud

__provider__ = soundcloud.Provider()
runner.run(__provider__)