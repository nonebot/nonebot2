import re

import jieba.posseg

_processors = []
_processors_without_keyword = []


def as_processor(keywords=None):
    def decorator(func):
        if keywords:
            _processors.append((keywords, func))
        else:
            _processors_without_keyword.append(func)
        return func

    return decorator


def parse_potential_commands(sentence):
    segmentation = list(jieba.posseg.cut(sentence=sentence))
    print('分词结果:', segmentation)
    potential_commands = []
    for processor in _processors:
        processed = False
        for regex in processor[0]:
            for word, flag in segmentation:
                if re.match(regex, word):
                    potential_commands.append(processor[1](sentence, segmentation))
                    processed = True
                    # A word matched, skip the rest of words
                    break
            if processed:
                # Current processor has processed, skip the rest of keywords
                break
    for func in _processors_without_keyword:
        potential_commands.append(func(sentence, segmentation))
    return potential_commands
