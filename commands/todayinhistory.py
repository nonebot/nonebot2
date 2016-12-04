import requests
from lxml import etree

from command import CommandRegistry
from commands import core

__registry__ = cr = CommandRegistry()


@cr.register('today_in_history', '历史上的今天')
def today_in_history(_, ctx_msg):
    resp = requests.get('http://tool.lu/todayonhistory/')
    ok = False
    if resp.status_code == 200:
        core.echo('历史上的今天：', ctx_msg)
        html = etree.HTML(resp.text)
        li_elems = html.xpath('//ul[@id="tohlis"]/li')
        # reply = reduce(lambda x, y: x.text + '\n' + y.text, li_elems)
        step = 10
        for start in range(0, len(li_elems), step):
            reply = ''
            for item in li_elems[start:start + step]:
                reply += item.text + '\n'
            reply = reply.rstrip()
            core.echo(reply, ctx_msg)
        core.echo('以上～', ctx_msg)
        ok = True
    if not ok:
        core.echo('很抱歉，网络出错了……建议等会儿再试吧～', ctx_msg)
