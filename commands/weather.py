import os
from datetime import datetime

import requests
import jieba

from command import CommandRegistry, split_args
from commands import core
from little_shit import get_source
from interactive import *

__registry__ = cr = CommandRegistry()

_api_key = os.environ.get('HEWEATHER_API_KEY')
_base_api_url = 'https://free-api.heweather.com/v5'
_search_api_url = _base_api_url + '/search'
_forecast_api_url = _base_api_url + '/forecast'
_now_api_url = _base_api_url + '/now'
_suggestion_api_url = _base_api_url + '/suggestion'

_cmd_weather = 'weather.weather'
_cmd_suggestion = 'weather.suggestion'

_weekday_string = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']


@cr.register('weather')
@cr.register('天气', '查天气', '天气预报', '查天气预报')
@split_args()
def weather(args, ctx_msg, allow_interactive=True):
    source = get_source(ctx_msg)
    if allow_interactive and (len(args) < 1 or not args[0].startswith('CN') or has_session(source, _cmd_weather)):
        # Be interactive
        return _do_interactively(_cmd_weather, weather, args, ctx_msg, source)

    city_id = args[0]
    session = requests.Session()
    params = {'city': city_id, 'key': _api_key}
    text = ''

    # Get real-time weather
    data_now = session.get(_now_api_url, params=params).json()
    if data_now and 'HeWeather5' in data_now and data_now['HeWeather5'][0].get('status') == 'ok':
        now = data_now['HeWeather5'][0]['now']
        text += '实时：\n%s，气温%s˚C，体感温度%s˚C，%s%s级，能见度%skm' \
                % (now['cond']['txt'], now['tmp'], now['fl'], now['wind']['dir'], now['wind']['sc'], now['vis'])

    # Get forecast
    data_forecast = session.get(_forecast_api_url, params=params).json()
    if data_forecast and 'HeWeather5' in data_forecast and data_forecast['HeWeather5'][0].get('status') == 'ok':
        daily_forecast = data_forecast['HeWeather5'][0]['daily_forecast']
        text += '\n\n预报：\n'

        for forecast in daily_forecast:
            d = datetime.strptime(forecast['date'], '%Y-%m-%d')
            text += '%d月%d日%s，' % (d.month, d.day, _weekday_string[d.weekday()])

            cond_d = forecast['cond']['txt_d']
            cond_n = forecast['cond']['txt_n']
            text += cond_d + ('转' + cond_n if cond_d != cond_n else '') + '，'

            text += forecast['tmp']['min'] + '~' + forecast['tmp']['max'] + '°C，'
            text += forecast['wind']['dir'] + forecast['wind']['sc'] + '级，'
            text += '降雨概率%s%%' % forecast['pop']
            text += '\n'

    text = text.rstrip()
    if text:
        core.echo(text, ctx_msg)
    else:
        core.echo('查询失败了，请稍后再试哦～', ctx_msg)


@cr.register('suggestion')
@cr.register('生活指数', '生活建议', '天气建议')
@split_args()
def suggestion(args, ctx_msg, allow_interactive=True):
    source = get_source(ctx_msg)
    if allow_interactive and (len(args) < 1 or not args[0].startswith('CN') or has_session(source, _cmd_suggestion)):
        # Be interactive
        return _do_interactively(_cmd_suggestion, suggestion, args, ctx_msg, source)

    city_id = args[0]
    session = requests.Session()
    params = {'city': city_id, 'key': _api_key}
    text = ''

    # Get suggestion
    data_suggestion = session.get(_suggestion_api_url, params=params).json()
    if data_suggestion and 'HeWeather5' in data_suggestion and data_suggestion['HeWeather5'][0].get('status') == 'ok':
        data = data_suggestion['HeWeather5'][0]['suggestion']
        text += '生活指数：\n\n' \
                '舒适度：%s\n\n' \
                '洗车指数：%s\n\n' \
                '穿衣指数：%s\n\n' \
                '感冒指数：%s\n\n' \
                '运动指数：%s\n\n' \
                '旅游指数：%s\n\n' \
                '紫外线指数：%s' \
                % tuple([data[k]['txt'] for k in ('comf', 'cw', 'drsg', 'flu', 'sport', 'trav', 'uv')])

    if text:
        core.echo(text, ctx_msg)
    else:
        core.echo('查询失败了，请稍后再试哦～', ctx_msg)


_state_machines = {}


def _do_interactively(command_name, func, args, ctx_msg, source):
    def ask_for_city(s, a, c):
        if len(a) > 0:
            if search_city(s, a, c):
                return True
        else:
            core.echo('你要查询哪个城市呢？', c)
        s.state += 1

    def search_city(s, a, c):
        if len(a) < 1:
            core.echo('你输入的城市不正确哦，请重新发送命令～', c)
            return True

        prov = None
        city = a[0]
        # Try to split province and city if possible
        tmp = jieba.lcut(city)
        if len(tmp) == 2:
            prov, city = tmp

        resp = requests.get(_search_api_url, params={
            'city': city,
            'key': _api_key
        })
        data = resp.json()
        if resp.status_code == 200 and data and 'HeWeather5' in data:
            city_list = data['HeWeather5']
            if city_list[0].get('status') != 'ok':
                core.echo('没有找到你输入的城市哦，请重新发送命令～', c)
                return True

            if prov:
                city_list = list(filter(lambda c: c['basic']['prov'] == prov, city_list))

            s.data['city_list'] = city_list

            if len(city_list) == 1:
                # Directly choose the first one
                choose_city(s, ['1'], c)
                return True

            # Here comes more than one city with the same name
            core.echo(
                '找到 %d 个重名城市，请选择你要查询的那个，发送它的序号：\n\n' % len(city_list)
                + '\n'.join(
                    [str(i + 1) + '. ' + c['basic']['prov'] + c['basic']['city'] for i, c in enumerate(city_list)]
                ),
                c
            )

        s.state += 1

    def choose_city(s, a, c):
        if len(a) != 1 or not a[0].isdigit():
            core.echo('你输入的序号不正确哦，请重新发送命令～', c)
            return True

        choice = int(a[0]) - 1  # Should be from 0 to len(city_list) - 1
        city_list = s.data['city_list']
        if choice < 0 or choice >= len(city_list):
            core.echo('你输入的序号超出范围了，请重新发送命令～', c)
            return True

        city_id = city_list[choice]['basic']['id']
        # sess.data['func']([city_id], c, allow_interactive=False)
        func([city_id], c, allow_interactive=False)
        return True

    if command_name not in _state_machines:
        _state_machines[command_name] = (
            ask_for_city,  # 0
            search_city,  # 1
            choose_city  # 2
        )

    sess = get_session(source, command_name)
    sess.data['func'] = func
    if _state_machines[command_name][sess.state](sess, args, ctx_msg):
        # Done
        remove_session(source, command_name)
