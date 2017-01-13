import re

from nl_processor import as_processor

_keywords = ('天气', '气温', '空气(质量)?', '温度', '多少度', '风|雨|雪|冰雹|霜|雾|霾')


def _match_keywords(word):
    for regex in _keywords:
        if re.search(regex, word):
            return True
    return False


@as_processor(keywords=_keywords)
def _processor(sentence, segmentation):
    possibility = 100
    location_segs = list(filter(lambda x: x.flag == 'ns', segmentation))
    if not location_segs:
        return None

    if len(location_segs) == 1:
        # Just city name
        city = location_segs[0].word.rstrip('市县区')
    elif len(location_segs) == 2:
        # Maybe has both province and city name
        city = location_segs[0].word.rstrip('省') + location_segs[1].word.rstrip('市县区')
    else:
        # More than 3 location name, use the last one
        city = location_segs[-1].word.rstrip('市县区')

    for seg in location_segs:
        segmentation.remove(seg)

    for seg in segmentation:
        # Scan over all segments and decrease possibility
        if _match_keywords(seg.word):
            continue

        flag = seg.flag
        score_dict = {'v': -10, 'l': -8, 'n': -5, 'p': -3, 't': +3, 'other': -1}
        for k, v in score_dict.items():
            if flag.startswith(k):
                possibility += v
                continue
        possibility += score_dict['other']

    return possibility, 'weather.weather', city, None
