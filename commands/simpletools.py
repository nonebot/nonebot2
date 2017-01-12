import base64

import requests
from lxml import etree

from command import CommandRegistry
from commands import core, ai

__registry__ = cr = CommandRegistry()


@cr.register('money_zh', 'money-zh')
@cr.register('人民币大写', '金额大写', '人民币金额大写')
def money_zh(args_text, ctx_msg):
    query = args_text.strip()
    try:
        _ = float(query)
    except ValueError:
        query = None
    if not query:
        core.echo('请在命令后加上要转换成大写的人民币金额哦～（命令和数字用空格或逗号隔开）', ctx_msg)
        return

    resp = requests.get('http://tool.lu/daxie/ajax.html?number=%s' % query)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('status') and 'text' in data:
            reply = query + ' 的汉字大写是：' + data['text'].strip()
            core.echo(reply, ctx_msg)
            return


@cr.register('short_url', 'short-url')
@cr.register('生成短网址', '生成短链接', '短网址', '短链接')
def short_url(args_text, ctx_msg):
    raw_url = args_text.strip()
    if not raw_url:
        core.echo('请在命令后加上要转换成短链接的网址哦～（命令和网址用空格或逗号隔开）', ctx_msg)
        return

    core.echo('正在生成，请稍等……', ctx_msg)

    session = requests.Session()
    short_urls = []

    resp = session.get(
        'http://dwz.wailian.work/',
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Referer': 'http://dwz.wailian.work/'
        }
    )
    if resp.status_code == 200:
        api_url = 'http://dwz.wailian.work/api.php?url=%s&site=%s'
        encoded_url = base64.b64encode(bytes(raw_url, 'utf-8')).decode('utf-8')
        for site in ('sina', 'googl'):
            resp = session.get(api_url % (encoded_url, site))
            data = resp.json()
            if resp.status_code == 200 and data.get('result') == 'ok':
                short_urls.append(data['data']['short_url'])

    if short_urls:
        core.echo('\n'.join(short_urls), ctx_msg)
    else:
        core.echo('生成失败，可能因为链接格式错误或服务器连接不上', ctx_msg)


# @cr.register('weather')
# @cr.register('天气', '查天气')
def weather(args_text, ctx_msg):
    city = args_text.strip()
    if not city:
        core.echo('请在命令后加上要查的城市哦～（命令和城市用空格或逗号隔开）', ctx_msg)
        return

    data = ai.tuling123(city + '天气', ctx_msg, internal=True)
    core.echo(data.get('text', ''), ctx_msg)


@cr.register('joke')
@cr.register('笑话', '说笑话', '说个笑话')
def weather(_, ctx_msg):
    data = ai.tuling123('说个笑话', ctx_msg, internal=True)
    core.echo(data.get('text', ''), ctx_msg)


@cr.register('baike')
@cr.register('百科', '查百科')
def weather(args_text, ctx_msg):
    query = args_text.strip()
    if not query:
        core.echo('请在命令后加上要查的关键词哦～（命令和关键词用空格或逗号隔开）', ctx_msg)
        return
    data = ai.tuling123('百科 ' + query, ctx_msg, internal=True)
    core.echo(data.get('text', ''), ctx_msg)


@cr.register('today_in_history', 'today-in-history', '历史上的今天')
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
