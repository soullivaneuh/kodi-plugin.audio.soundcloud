import xbmc
import xbmcgui
import xbmcplugin

"""
BASE
INFO_DATE = ('date', unicode) (CONVERT)

AUDIO
INFO_DURATION = ('duration', int)
INFO_TRACKNUMBER = ('tracknumber', int) (CONVERT)
INFO_YEAR = ('year', int)
INFO_GENRE = ('genre', unicode)
INFO_ALBUM = ('album', unicode)
INFO_ARTIST = ('artist', unicode)
INFO_TITLE = ('title', unicode)
INFO_RATING = ('rating', unicode) (CONVERT)

VIDEO
INFO_GENRE = ('genre', unicode)
INFO_AIRED = ('aired', unicode)
INFO_DURATION = ('duration', unicode) (CONVERT)
INFO_DIRECTOR = ('director', unicode)
INFO_PREMIERED = ('premiered', unicode)
INFO_EPISODE = ('episode', int)
INFO_SEASON = ('season', int)
INFO_YEAR = ('year', int)
INFO_PLOT = ('plot', unicode)
INFO_TITLE = ('title', unicode)
INFO_CODE = ('code', unicode) (CONVERT)
INFO_CAST = ('cast', list)
INFO_RATING = ('rating', float)
"""


def run(provider):
    from ... import KodimonException, VideoItem, AudioItem, DirectoryItem, AbstractProvider

    plugin = provider.get_plugin()

    results = None
    try:
        results = provider.navigate(plugin.get_path(), plugin.get_params())
    except KodimonException, ex:
        if provider.handle_exception(ex):
            from ... import constants
            provider.log(ex.message, constants.LOG_ERROR)
            xbmcgui.Dialog().ok("Exception in ContentProvider", ex.__str__())
            pass
        return

    result = results[0]
    options = {}
    options.update(results[1])

    if isinstance(result, bool) and not result:
        xbmcplugin.endOfDirectory(plugin.get_handle(), succeeded=False)
    elif isinstance(result, VideoItem) or isinstance(result, AudioItem):
        _set_resolved_url(plugin, result)
    elif isinstance(result, DirectoryItem):
        _add_directory(plugin, result)
    elif isinstance(result, list):
        item_count = len(result)
        for item in result:
            if isinstance(item, DirectoryItem):
                _add_directory(plugin, item, item_count)
            elif isinstance(item, VideoItem):
                _add_video(plugin, item, item_count)
            elif isinstance(item, AudioItem):
                _add_audio(plugin, item, item_count)
            pass

        xbmcplugin.endOfDirectory(
            plugin.get_handle(), succeeded=True, cacheToDisc=options.get(AbstractProvider.RESULT_CACHE_TO_DISC, True))
        pass
    else:
        # handle exception
        pass

    provider.shut_down()
    pass


def log(text, log_level=2):
    xbmc.log(msg=text, level=log_level)
    pass


def _set_resolved_url(plugin, base_item, succeeded=True):
    list_item = xbmcgui.ListItem(path=base_item.get_uri())
    xbmcplugin.setResolvedUrl(plugin.get_handle(), succeeded=succeeded, listitem=list_item)

    """
    # just to be sure :)
    if not isLiveStream:
        tries = 100
        while tries>0:
            xbmc.sleep(50)
            if xbmc.Player().isPlaying() and xbmc.getCondVisibility("Player.Paused"):
                xbmc.Player().pause()
                break
            tries-=1
    """

def _item_to_info_labels(base_item):
    info_labels = {}
    info_labels.update(base_item.get_info())

    date_string = info_labels.get('date', u'')
    if date_string:
        # '2014-11-12' => '12.11.2014'
        from ...abstract_api import parse_iso_8601
        date = parse_iso_8601(date_string)
        date = '%02d.%02d.%04d' % (date['day'], date['month'], date['year'])
        info_labels['date'] = date
        pass

    from ...items import AudioItem
    if isinstance(base_item, AudioItem):
        # 'track_number' => 'tracknumber'
        if AudioItem.INFO_TRACK_NUMBER in info_labels:
            info_labels['tracknumber'] = info_labels[AudioItem.INFO_TRACK_NUMBER]
            del info_labels[AudioItem.INFO_TRACK_NUMBER]
            pass

        # 1.0 = '1' (0-5)
        if AudioItem.INFO_RATING in info_labels:
            rating = int(base_item.get_rating())
            if rating > 5:
                rating = 5
                pass
            info_labels['rating'] = '%d' % rating
            pass
        pass

    from ...items import VideoItem
    if isinstance(base_item, VideoItem):
        # 'imdb_id' => 'code'
        if VideoItem.INFO_IMDB_ID in info_labels:
            info_labels['code'] = info_labels[VideoItem.INFO_IMDB_ID]
            del info_labels[VideoItem.INFO_IMDB_ID]
            pass

        # 120 => '2:00'
        duration = base_item.get_duration()
        if duration:
            minutes = duration / 60
            seconds = duration % 60
            duration = '%02d:%02d' % (minutes, seconds)
            info_labels['duration'] = duration
            pass
        pass

    return info_labels

def _add_directory(plugin, directory_item, item_count=0):
    item = xbmcgui.ListItem(label=directory_item.get_name(),
                            iconImage=u'DefaultFolder.png',
                            thumbnailImage=directory_item.get_image())

    # only set fanart is enabled
    settings = plugin.get_settings()
    from ... import constants

    if directory_item.get_fanart() and settings.get_bool(constants.SETTING_SHOW_FANART, True):
        item.setProperty(u'fanart_image', directory_item.get_fanart())
        pass
    if directory_item.get_context_menu() is not None:
        item.addContextMenuItems(directory_item.get_context_menu())
        pass

    xbmcplugin.addDirectoryItem(handle=plugin.get_handle(),
                                url=directory_item.get_uri(),
                                listitem=item,
                                isFolder=True,
                                totalItems=item_count)
    pass


def _add_video(plugin, video_item, item_count=0):
    item = xbmcgui.ListItem(label=video_item.get_name(),
                            iconImage=u'DefaultVideo.png',
                            thumbnailImage=video_item.get_image())

    # only set fanart is enabled
    settings = plugin.get_settings()
    from ... import constants

    if video_item.get_fanart() and settings.get_bool(constants.SETTING_SHOW_FANART, True):
        item.setProperty(u'fanart_image', video_item.get_fanart())
        pass
    if video_item.get_context_menu() is not None:
        item.addContextMenuItems(video_item.get_context_menu())
        pass

    item.setProperty(u'IsPlayable', u'true')

    item.setInfo(type=u'video', infoLabels=_item_to_info_labels(video_item))

    xbmcplugin.addDirectoryItem(handle=plugin.get_handle(),
                                url=video_item.get_uri(),
                                listitem=item,
                                totalItems=item_count)
    pass


def _add_audio(plugin, audio_item, item_count):
    item = xbmcgui.ListItem(label=audio_item.get_name(),
                            iconImage=u'DefaultAudio.png',
                            thumbnailImage=audio_item.get_image())

    # only set fanart is enabled
    settings = plugin.get_settings()
    from ... import constants

    if audio_item.get_fanart() and settings.get_bool(constants.SETTING_SHOW_FANART, True):
        item.setProperty(u'fanart_image', audio_item.get_fanart())
        pass
    if audio_item.get_context_menu() is not None:
        item.addContextMenuItems(audio_item.get_context_menu())
        pass

    item.setProperty(u'IsPlayable', u'true')

    item.setInfo(type=u'music', infoLabels=_item_to_info_labels(audio_item))

    xbmcplugin.addDirectoryItem(handle=plugin.get_handle(),
                                url=audio_item.get_uri(),
                                listitem=item,
                                totalItems=item_count)
    pass