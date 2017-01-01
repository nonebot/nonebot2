import os
import hashlib
from datetime import datetime

import requests

from command import CommandRegistry
from commands import core

__registry__ = cr = CommandRegistry()

_app_id = os.environ.get('BAIDU_FANYI_APP_ID')
_api_key = os.environ.get('BAIDU_FANYI_API_KEY')

_lang_map = {
    '中文': 'zh',
    '繁体中文': 'cht',
    '英语': 'en',
    '粤语': 'yue',
    '文言文': 'wyw',
    '日语': 'jp',
    '韩语': 'kor',
    '法语': 'fra',
    '西班牙语': 'spa',
    '阿拉伯语': 'ara',
    '俄语': 'ru',
    '葡萄牙语': 'pt',
    '德语': 'de',
    '意大利语': 'it',
    '希腊语': 'el',
    '荷兰语': 'nl',
    '波兰语': 'pl',
    '保加利亚语': 'bul',
    '爱沙尼亚语': 'est',
    '丹麦语': 'dan',
    '芬兰语': 'fin',
    '捷克语': 'cs',
    '罗马尼亚语': 'rom',
    '斯洛文尼亚语': 'slo',
    '瑞典语': 'swe',
    '匈牙利语': 'hu',
    '越南语': 'vie'
}

_lang_alias_map = {
    '简体中文': 'zh',
    '汉语': 'zh',
    '英文': 'en',
    '日文': 'jp',
    '韩文': 'kor'
}


@cr.register('translate', '翻译', '翻訳')
def translate(args_text, ctx_msg):
    query = args_text.strip()
    if not query:
        core.echo('请在命令后加上要翻译的内容哦～（命令和要翻译的内容用空格或逗号隔开）', ctx_msg)
        return

    cmd = ctx_msg.get('command')
    if cmd == 'translate':
        return translate_to('英语 ' + args_text, ctx_msg)
    elif cmd == '翻訳':
        return translate_to('日语 ' + args_text, ctx_msg)
    else:
        return translate_to('简体中文 ' + args_text, ctx_msg)


@cr.register('translate_to', 'translate-to', '翻译到', '翻译成')
def translate_to(args_text, ctx_msg):
    args = args_text.strip().split(' ', 1)
    if len(args) < 2 or (args[0] not in _lang_map and args[0] not in _lang_alias_map):
        core.echo(
            '请指定目标语言和要翻译的内容哦～（命令、目标语言、要翻译的内容之间用空格或逗号隔开\n目前支持的语言：'
            + '、'.join(_lang_map.keys()),
            ctx_msg
        )
        return

    core.echo('正在翻译，请稍等……', ctx_msg)

    to_lang = _lang_map.get(args[0]) or _lang_alias_map.get(args[0])
    query = args[1]
    api_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    salt = str(int(datetime.now().timestamp()))
    sign = hashlib.md5((_app_id + query + salt + _api_key).encode('utf-8')).hexdigest()
    resp = requests.post(api_url, data={
        'q': query,
        'from': 'auto',
        'to': to_lang,
        'appid': _app_id,
        'salt': salt,
        'sign': sign
    })
    if resp.status_code == 200:
        data = resp.json()
        print(data)
        if 'trans_result' in data:
            core.echo('翻译结果（百度翻译）：\n' + '\n'.join([x['dst'] for x in data['trans_result']]), ctx_msg)
            return
    core.echo('翻译失败，可能因为后台接口的频率限制或服务器连接不上', ctx_msg)
