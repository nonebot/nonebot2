import re

from nl_processor import as_processor


@as_processor(keywords=('番', '动漫', '动画'))
def _processor_anime_index(sentence, segmentation):
    m = re.search('(?:(?P<year>\d{2})\s*年\s*)?(?P<month>\d{1,2})\s*月', sentence)
    year, month = None, None
    if m:
        year = m.group('year')
        month = m.group('month')

    args_text = month if month else ''
    args_text = (str(year) + ' ' + args_text) if year else args_text

    possibility = 90
    if '哪些' in sentence or '什么' in sentence:
        possibility += 3
    if not re.search('b\s*站', sentence.lower()):
        possibility -= 10

    return possibility, 'bilibili.anime_index', args_text, None


@as_processor(keywords=('更新',))
def _processor_anime_timeline(sentence, segmentation):
    m = re.match('(?:b\s*站)?(?P<day_str>(?:前|昨|今|明|大?后)天)?(?P<name>.+?)'
                 '(?P<day_str2>(?:前|昨|今|明|大?后)天)?(?:会|有)?更(?:不更)?新',
                 sentence.lower())
    day_str, name = None, None
    if m:
        day_str = m.group('day_str') or m.group('day_str2')
        name = m.group('name')

    if not name:
        return None

    possibility = 90
    if not day_str:
        possibility -= 5
    if '吗' in sentence:
        possibility += 5
    if not re.search('b\s*站', sentence.lower()):
        possibility -= 10

    delta_day_dict = {'前天': -2, '昨天': -1, '今天': 0, '明天': 1, '后天': 2, '大后天': 3}
    delta_day = delta_day_dict.get(day_str, 0)

    return possibility, 'bilibili.anime_timeline', str(delta_day) + ' ' + name, None


@as_processor(keywords=('更新',))
def _processor_anime_timeline_2(sentence, segmentation):
    m = re.match('(?:b\s*站)?(?P<name>.+?)(?:(?:什么|啥)时候)?(?:会|有)?更新', sentence.lower())
    name = m.group('name') if m else None

    if not name:
        return None

    possibility = 90
    if not re.search('b\s*站', sentence.lower()):
        possibility -= 10

    return possibility, 'bilibili.anime_timeline', name, None
