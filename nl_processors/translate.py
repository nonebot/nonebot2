import re

from nl_processor import as_processor

_query_lang_matcher = [
    re.compile('(?:(?:要|[应]?该)?怎么|怎样|如何)?[把将]?[\s,.，。]?(?P<query>.*?)[\s,.，。]?'
               '(?:这[个]?(?:词[组]?|句(?:子|话)?|短语))?翻译[成为到](?P<lang>\w+?[文语])(?![\s:：,，.。])'),
    re.compile('(?P<query>.+?)[\s,.，。]?(?:这[个]?(?:词[组]?|句(?:子|话)?|短语))?的(?P<lang>\w+?[文语])'),
    re.compile('.*?[把将]?(?:(?:[下后][面])?(?:这[个]?|[下后][面]?)(?:词[组]?|句(?:子|话)?|短语))?'
               '翻译[成为到]\s*(?P<lang>\w+?[文语])[\s:：,，](?P<query>.*)'),
    re.compile('.*[用]?(?P<lang>\w+?[文语])\w*?(?:说|讲|表达|表示)'
               '(?P<query>.*)(?:这[个]?(?:词[组]?|句(?:子|话)?|短语))'),
    re.compile('.*[用]?(?P<lang>\w+?[文语])\w*?(?:说|讲|表达|表示)[\s:：,，]?(?P<query>.*)'),
]


@as_processor(keywords=('翻译(为|成|到)?', '.+(文|语)'))
def _processor(sentence, segmentation):
    lang = None
    query = None
    for matcher in _query_lang_matcher:
        m = matcher.match(sentence)
        if m:
            lang, query = m.group('lang'), m.group('query')
            break
    if lang and query:
        print('翻译: 目标语言:', lang, ', 待翻译文本:', query)
        return 90, 'translate.translate_to', ' '.join((lang.strip(), query.strip(' ,，'))), None
    return None
