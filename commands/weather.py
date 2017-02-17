import os
import json
import sqlite3
from datetime import datetime, timedelta

import requests

from command import CommandRegistry, split_arguments
from commands import core
from little_shit import get_source, get_db_dir, get_tmp_dir
from interactive import *

__registry__ = cr = CommandRegistry()

_api_key = os.environ.get('HEWEATHER_API_KEY')
_base_api_url = 'https://free-api.heweather.com/v5'
_search_api_url = _base_api_url + '/search'
_detail_api_url = _base_api_url + '/weather'

_cmd_weather = 'weather.weather'
_cmd_suggestion = 'weather.suggestion'

_weekday_string = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']


@cr.register('weather')
@cr.register('天气', '查天气', '天气预报', '查天气预报')
@split_arguments()
def weather(args_text, ctx_msg, argv: list = None, allow_interactive=True):
    source = get_source(ctx_msg)
    if allow_interactive and (not argv or not argv[0].startswith('CN') or has_session(source, _cmd_weather)):
        # Be interactive
        return _do_interactively(_cmd_weather, weather, args_text.strip(), ctx_msg, source)

    city_id = argv[0]
    text = ''

    data = _get_weather(city_id)
    if data:
        text += '%s天气\n更新时间：%s' % (data['basic']['city'], data['basic']['update']['loc'])

        now = data['now']
        aqi = data['aqi']['city']
        text += '\n\n实时：\n\n%s，气温%s°C，体感温度%s°C，%s%s级，' \
                '能见度%skm，空气质量指数：%s，%s，PM2.5：%s，PM10：%s' \
                % (now['cond']['txt'], now['tmp'], now['fl'], now['wind']['dir'], now['wind']['sc'], now['vis'],
                   aqi['aqi'], aqi['qlty'], aqi['pm25'], aqi['pm10'])

        daily_forecast = data['daily_forecast']
        text += '\n\n预报：\n\n'

        for forecast in daily_forecast:
            d = datetime.strptime(forecast['date'], '%Y-%m-%d')
            text += '%d月%d日%s，' % (d.month, d.day, _weekday_string[d.weekday()])

            cond_d = forecast['cond']['txt_d']
            cond_n = forecast['cond']['txt_n']
            text += cond_d + ('转' + cond_n if cond_d != cond_n else '') + '，'

            text += forecast['tmp']['min'] + '~' + forecast['tmp']['max'] + '°C，'
            text += forecast['wind']['dir'] + forecast['wind']['sc'] + '级，'
            text += '降雨概率%s%%' % forecast['pop']
            text += '\n\n'

    text = text.rstrip()
    if text:
        core.echo(text, ctx_msg)
    else:
        core.echo('查询失败了，请稍后再试哦～', ctx_msg)


@cr.register('suggestion', hidden=True)
@cr.register('生活指数', '生活建议', '天气建议')
@split_arguments()
def suggestion(args_text, ctx_msg, argv: list = None, allow_interactive=True):
    source = get_source(ctx_msg)
    if allow_interactive and (len(argv) < 1 or not argv[0].startswith('CN') or has_session(source, _cmd_suggestion)):
        # Be interactive
        return _do_interactively(_cmd_suggestion, suggestion, args_text.strip(), ctx_msg, source)

    city_id = argv[0]
    text = ''

    data = _get_weather(city_id)
    if data:
        data = data['suggestion']
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


def _do_interactively(command_name, func, args_text, ctx_msg, source):
    def ask_for_city(s, a, c):
        if a:
            if search_city(s, a, c):
                return True
        else:
            core.echo('你要查询哪个城市呢？', c)
        s.state += 1

    def search_city(s, a, c):
        if not a:
            core.echo('你输入的城市不正确哦，请重新发送命令～', c)
            return True

        city_list = _get_city_list(a)

        if not city_list:
            core.echo('没有找到你输入的城市哦，请重新发送命令～', c)
            return True

        s.data['city_list'] = city_list

        if len(city_list) == 1:
            # Directly choose the first one
            choose_city(s, '1', c)
            return True

        # Here comes more than one city with the same name
        core.echo(
            '找到 %d 个重名城市，请选择你要查询的那个，发送它的序号：\n\n' % len(city_list)
            + '\n'.join(
                [str(i + 1) + '. ' + c['prov'] + c['city'] for i, c in enumerate(city_list)]
            ),
            c
        )

        s.state += 1

    def choose_city(s, a, c):
        if not a or not a.isdigit():
            core.echo('你输入的序号不正确哦，请重新发送命令～', c)
            return True

        choice = int(a) - 1  # Should be from 0 to len(city_list) - 1
        city_list = s.data['city_list']
        if choice < 0 or choice >= len(city_list):
            core.echo('你输入的序号超出范围了，请重新发送命令～', c)
            return True

        city_id = city_list[choice]['id']
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
    if _state_machines[command_name][sess.state](sess, args_text, ctx_msg):
        # Done
        remove_session(source, command_name)


_weather_db_path = os.path.join(get_db_dir(), 'weather.sqlite')


def _get_city_list(city_name):
    city_name = city_name.lower()
    if not os.path.exists(_weather_db_path):
        resp = requests.get('http://7xo46j.com1.z0.glb.clouddn.com/weather.sqlite', stream=True)
        with resp.raw as s, open(_weather_db_path, 'wb') as d:
            d.write(s.read())

    conn = sqlite3.connect(_weather_db_path)
    cities = list(conn.execute(
        'SELECT code, name, province FROM city WHERE name = ? OR name_en = ? OR province || name = ?',
        (city_name, city_name, city_name)
    ))
    return [{'id': x[0], 'city': x[1], 'prov': x[2]} for x in cities]


_weather_cache_dir = os.path.join(get_tmp_dir(), 'weather')


def _get_weather(city_id):
    if not os.path.exists(_weather_cache_dir):
        os.makedirs(_weather_cache_dir)

    file_name = city_id + '.json'
    file_path = os.path.join(_weather_cache_dir, file_name)
    if os.path.exists(file_path):
        update_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        if (datetime.now() - update_time) < timedelta(hours=1):
            with open(file_path, 'r') as f:
                data = json.load(f)
            data['from_cache'] = True
            return data

    data = requests.get(_detail_api_url, params={'city': city_id, 'key': _api_key}).json()
    if data and 'HeWeather5' in data and data['HeWeather5'][0].get('status') == 'ok':
        data = data['HeWeather5'][0]
        with open(file_path, 'w') as f:
            json.dump(data, f)
        data['from_cache'] = False
        return data

    return None
