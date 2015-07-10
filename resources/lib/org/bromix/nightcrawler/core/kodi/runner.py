__author__ = 'bromix'

"""
import xbmc
import xbmcgui
import xbmcplugin

from ..abstract_runner import AbstractRunner
from ...exception import NightcrawlerException

    def _set_resolved_url(self, context, base_item, succeeded=True):
        item = xbmc_items.to_item(context, base_item)
        item.setPath(base_item.get_uri())
        xbmcplugin.setResolvedUrl(context.get_handle(), succeeded=succeeded, listitem=item)


    def _add_video(self, context, video_item, item_count=0):
        item = xbmc_items.to_video_item(context, video_item)

        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=video_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)
        pass

    def _add_image(self, context, image_item, item_count):
        item = xbmcgui.ListItem(label=image_item.get_name(),
                                iconImage=u'DefaultPicture.png',
                                thumbnailImage=image_item.get_image())

        # only set fanart is enabled
        settings = context.get_settings()
        if image_item.get_fanart() and settings.show_fanart():
            item.setProperty(u'fanart_image', image_item.get_fanart())
            pass
        if image_item.get_context_menu() is not None:
            item.addContextMenuItems(image_item.get_context_menu(), replaceItems=image_item.replace_context_menu())
            pass

        item.setInfo(type=u'picture', infoLabels=info_labels.create_from_item(context, image_item))

        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=image_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)
        pass

    def _add_audio(self, context, audio_item, item_count):
        item = xbmc_items.to_audio_item(context, audio_item)

        xbmcplugin.addDirectoryItem(handle=context.get_handle(),
                                    url=audio_item.get_uri(),
                                    listitem=item,
                                    totalItems=item_count)
        pass

    pass
"""