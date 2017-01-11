"""
This filter recognizes speech in voice message and stores it in 'text' field of context message.
"""

import re
import os
import sys
import base64

import requests
from pydub import AudioSegment
import speech_recognition as sr

from filter import as_filter
from commands import core


def _recognize_baidu(wav_path, unique_id, api_key, secret_key, language='zh'):
    api_url = 'http://vop.baidu.com/server_api'
    auth_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' \
               % (api_key, secret_key)
    resp = requests.get(auth_url)
    if resp.status_code == 200:
        data = resp.json()
        if data and 'access_token' in data:
            token = data['access_token']
            with open(wav_path, 'rb') as f:
                audio_data = f.read()
            audio_data_b64 = base64.b64encode(audio_data).decode('utf-8')
            json = {
                'format': 'wav',
                'rate': 8000,
                'channel': 1,
                'cuid': unique_id,
                'token': token,
                'lan': language,
                'speech': audio_data_b64,
                'len': len(audio_data)
            }
            resp = requests.post(api_url, json=json)
            if resp.status_code == 200:
                data = resp.json()
                if data and 'result' in data:
                    return ''.join(data['result']).strip('，。？！')
    return None


def _recognize_bing(wav_path, api_key, language='zh-CN'):
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_bing(audio, key=api_key, language=language)
        return text
    except (sr.UnknownValueError, sr.RequestError):
        return None


@as_filter(priority=90)
def _filter(ctx_msg):
    if ctx_msg.get('format') == 'media' and ctx_msg.get('media_type') == 'voice':
        m = re.match('\[语音\]\(([/_A-Za-z0-9]+\.mp3)\)', ctx_msg.get('content'))
        if m:
            core.echo('正在识别语音内容，请稍等……', ctx_msg)
            mp3_path = m.group(1)
            wav_path = os.path.splitext(mp3_path)[0] + '.wav'
            voice = AudioSegment.from_mp3(mp3_path)
            voice.export(wav_path, format='wav')

            service = os.environ.get('SPEECH_RECOGNITION_SERVICE', '').lower()
            text = None
            service_full_name = None
            if service == 'baidu':
                service_full_name = '百度语音识别'
                text = _recognize_baidu(
                    wav_path,
                    ctx_msg.get('sender_id')[-60:],
                    os.environ.get('BAIDU_SPEECH_API_KEY'),
                    os.environ.get('BAIDU_SPEECH_SECRET_KEY'),
                    language='zh'
                )
            elif service == 'bing':
                service_full_name = '必应语音识别'
                text = _recognize_bing(
                    wav_path,
                    os.environ.get('BING_SPEECH_API_KEY'),
                    language='zh-CN'
                )
            else:
                print('Unknown speech recognition service name.', file=sys.stderr)

            if text:
                reply = '识别结果（' + service_full_name + '）：\n%s\n\n下面将把识别到的内容作为文字消息处理……' % text
                ctx_msg['text'] = text
                ctx_msg['from_voice'] = True
            else:
                reply = '抱歉哦，没有识别出你说的是什么'
            core.echo(reply, ctx_msg)
            os.remove(wav_path)
