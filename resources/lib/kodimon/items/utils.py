__author__ = 'bromix'


def convert(item_json_data, to_version=3):
    version = item_json_data['_version']
    current_version = to_version
    converter = [_v1tov2, _v2tov3]

    # make a clean copy of the old json
    _new_item_json_data = {}
    _new_item_json_data.update(item_json_data)

    # convert each version change
    for i in range(version - 1, current_version - 1):
        _new_item_json_data = converter[i](_new_item_json_data)
        pass

    _new_item_json_data = {}
    return _new_item_json_data


def _v2tov3(item_json_data):
    _info_labels = item_json_data['_info_labels']

    from .base_item import BaseItem
    # '01.01.2009' => '2009-01-01'
    if BaseItem.INFO_DATE in _info_labels:
        old_date = _info_labels[BaseItem.INFO_DATE].split('.')
        new_date = '%s-%s-%s' % (old_date[2], old_date[1], old_date[0])
        pass

    from .audio_item import AudioItem
    # '5' => 5
    if AudioItem.INFO_RATING in _info_labels:
        _info_labels[AudioItem.INFO_RATING] = float(_info_labels[AudioItem.INFO_RATING])
        pass

    from .video_item import VideoItem
    if 'code' in _info_labels:
        _info_labels[VideoItem.INFO_IMDB_ID] = _info_labels['code']
        del _info_labels['code']
        pass

    if 'dateadded' in _info_labels:
        _info_labels[VideoItem.INFO_DATE_ADDED] = _info_labels['dateadded']
        pass

    if VideoItem.INFO_DURATION in _info_labels:
        duration = _info_labels[VideoItem.INFO_DURATION]
        if isinstance(duration, basestring):
            old_data = duration.split(':')
            seconds = int(old_data[0])*60
            seconds += int(old_data[1])
            _info_labels[VideoItem.INFO_DURATION] = seconds
            pass
        pass

    # _info_labels => _info_data
    item_json_data['_info_data'] = item_json_data['_info_labels']
    del item_json_data['_info_labels']
    return item_json_data


def _v1tov2(item_json_data):
    return item_json_data