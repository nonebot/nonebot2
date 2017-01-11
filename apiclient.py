import os

import requests


class ApiClient:
    qq_api_url = os.environ.get('QQ_API_URL')
    wx_api_url = os.environ.get('WX_API_URL')

    def _api_url(self, via):
        if via == 'qq':
            return self.qq_api_url
        elif via == 'wx':
            return self.wx_api_url
        return None

    def send_message(self, content: str, ctx_msg: dict):
        msg_type = ctx_msg.get('type')
        if msg_type == 'group_message':
            return self.send_group_message(content=content, ctx_msg=ctx_msg)
        elif msg_type == 'discuss_message':
            return self.send_discuss_message(content=content, ctx_msg=ctx_msg)
        elif msg_type == 'friend_message':
            return self.send_friend_message(content=content, ctx_msg=ctx_msg)
        return None

    def send_group_message(self, content: str, ctx_msg: dict):
        try:
            if ctx_msg.get('via') == 'qq' and self.qq_api_url:
                params = {'content': content}
                if ctx_msg.get('group_uid'):
                    params['uid'] = ctx_msg.get('group_uid')
                elif ctx_msg.get('group_id'):
                    params['id'] = ctx_msg.get('group_id')
                return requests.get(self.qq_api_url + '/send_group_message', params=params)
            elif ctx_msg.get('via') == 'wx' and self.wx_api_url:
                params = {'content': content}
                if ctx_msg.get('group_id'):
                    params['id'] = ctx_msg.get('group_id')
                return requests.get(self.wx_api_url + '/send_group_message', params=params)
        except requests.exceptions.ConnectionError:
            pass
        return None

    def send_discuss_message(self, content: str, ctx_msg: dict):
        try:
            if ctx_msg.get('via') == 'qq' and self.qq_api_url:
                params = {'content': content}
                if ctx_msg.get('discuss_id'):
                    params['id'] = ctx_msg.get('discuss_id')
                return requests.get(self.qq_api_url + '/send_discuss_message', params=params)
        except requests.exceptions.ConnectionError:
            pass
        return None

    def send_friend_message(self, content: str, ctx_msg: dict):
        try:
            if ctx_msg.get('via') == 'qq' and self.qq_api_url:
                params = {'content': content}
                if ctx_msg.get('sender_uid'):
                    params['uid'] = ctx_msg.get('sender_uid')
                elif ctx_msg.get('sender_id'):
                    params['id'] = ctx_msg.get('sender_id')
                return requests.get(self.qq_api_url + '/send_friend_message', params=params)
            elif ctx_msg.get('via') == 'wx' and self.wx_api_url:
                params = {'content': content}
                if ctx_msg.get('sender_account'):
                    params['account'] = ctx_msg.get('sender_account')
                elif ctx_msg.get('sender_id'):
                    params['id'] = ctx_msg.get('sender_id')
                return requests.get(self.wx_api_url + '/send_friend_message', params=params)
        except requests.exceptions.ConnectionError:
            pass
        return None

    def get_group_info(self, via):
        url = self._api_url(via)
        if url:
            try:
                return requests.get(url + '/get_group_info')
            except requests.exceptions.ConnectionError:
                return None

    def get_user_info(self, via):
        url = self._api_url(via)
        if url:
            try:
                return requests.get(url + '/get_user_info')
            except requests.exceptions.ConnectionError:
                return None


client = ApiClient()
