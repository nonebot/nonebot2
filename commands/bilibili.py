import re
import math
from datetime import datetime, timedelta

import requests
import pytz

from command import CommandRegistry, split_arguments
from commands import core

__registry__ = cr = CommandRegistry()


@cr.register('anime_index', 'anime-index', '番剧索引', '番剧', '新番')
@split_arguments()
def anime_index(_, ctx_msg, argv=None):
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    year = now.year
    month = now.month
    if len(argv) == 2 and re.fullmatch('(?:20)?\d{2}', argv[0]) and re.fullmatch('\d{1,2}', argv[1]):
        year = int(argv[0]) if len(argv[0]) > 2 else 2000 + int(argv[0])
        month = int(argv[1])
    elif len(argv) == 1 and re.fullmatch('\d{1,2}', argv[0]):
        month = int(argv[0])
    elif len(argv) == 1 and re.fullmatch('(?:20)?\d{2}-\d{1,2}', argv[0]):
        year, month = [int(x) for x in argv[0].split('-')]
        year = 2000 + year if year < 100 else year
    elif len(argv):
        core.echo('抱歉无法识别的输入的参数，下面将给出本季度的番剧～', ctx_msg)

    quarter = math.ceil(month / 3)
    json = requests.get('http://bangumi.bilibili.com/web_api/season/index_global'
                        '?page=1&page_size=20&version=0&is_finish=0'
                        '&start_year=%d&quarter=%d&tag_id=&index_type=1&index_sort=0' % (year, quarter)).json()
    if json and json.get('result') and int(json['result'].get('count', 0)) > 0:
        anime_list = json['result'].get('list', [])
        reply = '%d年%d月番剧\n按追番人数排序，前20部如下：\n\n' % (year, 1 + (quarter - 1) * 3)
        reply += '\n'.join([anime.get('title', '未知动画') + '  '
                            + ('未开播' if anime.get('total_count', -1) < 0
                               else ('全%d话' % anime['total_count']
                                     if anime['newest_ep_index'] == str(anime['total_count'])
                                     else '更新至%s' % anime['newest_ep_index']
                                          + ('话' if anime['newest_ep_index'].isdigit() else '')))
                            for anime in anime_list])

        reply += '\n\n更多详细资料见 bilibili 官网 ' \
                 'http://bangumi.bilibili.com/anime/index' \
                 '#p=1&v=0&area=&stat=0&y=%d&q=%d&tag=&t=1&sort=0' % (year, quarter)
    else:
        reply = '没有查询到%d年%d月开播的番剧……' % (year, 1 + (quarter - 1) * 3)

    core.echo(reply, ctx_msg)


@cr.register('anime_timeline', 'anime-timeline', '番剧时间表', '新番时间表')
@split_arguments(maxsplit=1)
def anime_timeline(args_text, ctx_msg, internal=False, argv=None):
    if len(argv) == 0:
        core.echo('请指定要查询的日期或番剧名称，例如下面（主要看参数，你的命令是对的～）：\n\n'
                  '/新番时间表 02-21\n'
                  '/新番时间表 0\n'
                  '/新番时间表 小林家的龙女仆\n'
                  '/新番时间表 02-21 小林家的龙女仆\n\n'
                  '上面第二个例子的「0」代表和今天相差的天数，0表示今天，1表示明天，-1表示昨天，以此类推\n'
                  '参数中间记得用用空格隔开哦～', ctx_msg, internal)
        return None

    json = requests.get('http://bangumi.bilibili.com/web_api/timeline_v4').json()
    if not json or 'result' not in json:
        return None

    timeline_list = json['result'] or []

    date_str = None
    anime_name = None

    if re.fullmatch('\d{1,2}-\d{1,2}', argv[0]):
        # month-day
        date_str = '%02d-%02d' % tuple(map(lambda x: int(x), argv[0].split('-')))
        argv = argv[1:]
    elif re.fullmatch('-?\d', argv[0]):
        # timedelta (days)
        delt = timedelta(days=int(argv[0]))
        dt = datetime.now() + delt
        date_str = dt.strftime('%m-%d')
        argv = argv[1:]

    if len(argv) > 1:
        anime_name = args_text.strip()
    elif len(argv) == 1:
        anime_name = argv[0].rstrip()

    if date_str:
        timeline_list = list(filter(lambda item: item.get('pub_date', '').endswith(date_str), timeline_list))
    if anime_name:
        timeline_list = list(filter(
            lambda item: anime_name.lower() in item.get('title', '').lower()
                         and len(anime_name) > len(item.get('title', '')) / 4,
            timeline_list
        ))

    if internal:
        return timeline_list

    if date_str and anime_name:
        if not timeline_list:
            reply = '没更新'
        else:
            reply = ''
            for item in timeline_list:
                reply += '\n' + ('更新了' if item['is_published'] else '将在%s更新' % item['ontime']) \
                         + '第%s话' % item['ep_index'] if item['ep_index'].isdigit() else item['ep_index']
            reply = reply.lstrip()

        core.echo(reply, ctx_msg, internal)
        return

    if not timeline_list:
        core.echo('没有找到符合条件的时间表……', ctx_msg, internal)
        return

    if date_str and not anime_name:
        month, day = [int(x) for x in date_str.split('-')]
        reply = '在%d月%d日更新的番剧有：\n\n' % (month, day)
        reply += '\n'.join([item.get('title', '未知动画') + '  '
                            + item.get('ontime', '未知时间') + '  '
                            + ('第%s话' % item.get('ep_index')
                               if item.get('ep_index', '').isdigit()
                               else item.get('ep_index', ''))
                            for item in timeline_list])
        core.echo(reply, ctx_msg, internal)
    elif anime_name and not date_str:
        anime_dict = {}
        for item in timeline_list:
            k = item.get('title', '未知动画')
            if k not in anime_dict:
                anime_dict[k] = []
            anime_dict[k].append(item)

        for name, items in anime_dict.items():
            reply = name + '\n'
            for item in items:
                _, month, day = [int(x) for x in item['pub_date'].split('-')]
                reply += '\n' + ('已' if item['is_published'] else '将') \
                         + '在%d月%d日%s更新' % (month, day, item['ontime']) \
                         + '第%s话' % item['ep_index'] if item['ep_index'].isdigit() else item['ep_index']
            core.echo(reply, ctx_msg, internal)
