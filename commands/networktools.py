import json

import requests
from lxml import etree

from command import CommandRegistry
from commands import core

__registry__ = cr = CommandRegistry()


@cr.register('ip')
def ip(args_text, ctx_msg):
    query = args_text.strip()
    if not query:
        core.echo('请指定要查询的 IP 或域名', ctx_msg)
        return

    core.echo('正在查询，请稍等……', ctx_msg)

    chinaz_url = 'http://ip.chinaz.com/%s'
    ipcn_url = 'http://ip.cn/?ip=%s'
    ipipnet_url = 'http://freeapi.ipip.net/%s'

    found = False

    # Get data from ChinaZ.com
    resp = requests.get(chinaz_url % query)
    if resp.status_code == 200:
        html = etree.HTML(resp.text)
        p_elems = html.xpath('//p[@class="WhwtdWrap bor-b1s col-gray03"]')
        if len(p_elems) > 0:
            reply = 'ChinaZ.com:'
            for p_elem in p_elems:
                span_elems = p_elem.getchildren()
                reply += '\n' + span_elems[1].text + ', ' + span_elems[3].text
            core.echo(reply, ctx_msg)
            found = True

    # Get data from ip.cn
    resp = requests.get(ipcn_url % query, headers={'User-Agent': 'curl/7.47.0'})
    if resp.status_code == 200:
        # Example: 'IP：123.125.114.144 来自：北京市 联通'
        items = resp.text.strip().split('：')
        if len(items) == 3:
            reply = 'IP.cn:\n' + items[1].split(' ')[0] + ', ' + items[2]
            core.echo(reply, ctx_msg)
            found = True

    # Get data from ipip.net
    resp = requests.get(ipipnet_url % query, headers={'User-Agent': 'curl/7.47.0'})
    if resp.status_code == 200 and resp.text.strip():
        # Example: '["中国","江苏","常州","","教育网"]'
        parts = json.loads(resp.text)
        reply = 'IPIP.net\n' + query + ' ' + ''.join(parts)
        core.echo(reply, ctx_msg)
        found = True

    core.echo('以上' if found else '查询失败', ctx_msg)
