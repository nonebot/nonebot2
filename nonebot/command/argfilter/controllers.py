import re

from nonebot import CommandSession
from nonebot.helpers import render_expression


def handle_cancellation(session: CommandSession):
    """
    If the input is a string of cancellation word, finish the command session.
    """

    def control(value):
        if _is_cancellation(value) is True:
            session.finish(render_expression(
                session.bot.config.SESSION_CANCEL_EXPRESSION))
        return value

    return control


def _is_cancellation(sentence: str) -> bool:
    for kw in ('算', '别', '不', '停', '取消'):
        if kw in sentence:
            # a keyword matches
            break
    else:
        # no keyword matches
        return False

    if re.match(r'^那?[算别不停]\w{0,3}了?吧?$', sentence) or \
            re.match(r'^那?(?:[给帮]我)?取消了?吧?$', sentence):
        return True

    return False
