import re

from nl_processor import as_processor

_query_lang_matcher = [
    re.compile('[把将]?[ ,.，。]?(.*?)[ ,.，。]?(?:这[个]?(?:词[组]?|句(?:子|话)?|短语))翻译[成为到](\w+?[文语])(?![ :：,，.。])'),
    re.compile('(\w+?)[ ,.，。]?(?:这[个]?(?:词[组]?|句(?:子|话)?|短语))?[的用](\w+?[文语])')
]

_lang_query_matcher = [
    re.compile('[把将]?(?:(?:这[个]?|[下后][面]?)(?:词[组]?|句(?:子|话)?|短语))翻译[成为到](\w+?[文语])[ :：,，.。](.*)'),
    re.compile('[用]?(\w+[文语])\w+?(?:说|讲|表达|表示)(.*)(?:这[个]?(?:词[组]?|句(?:子|话)?|短语))'),
    re.compile('[用]?(\w+[文语])\w+?(?:说|讲|表达|表示)(.*)')
]


@as_processor(keywords=('翻译(为|成|到)?', '.+(文|语)'))
def _processor(sentence, segmentation):
    lang = None
    query = None
    for matcher in _query_lang_matcher + _lang_query_matcher:
        m = matcher.match(sentence)
        if m:
            if matcher in _lang_query_matcher:
                lang, query = m.group(1), m.group(2)
            else:
                lang, query = m.group(2), m.group(1)
            break
    if lang and query:
        return 90, 'translate.translate_to', ' '.join((lang.strip(), query.strip(' ,，'))), None
    return None
