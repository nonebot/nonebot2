import requests
from flask import request as flask_req

from msg_src_adapter import Adapter, as_adapter, ConfigurationError


@as_adapter(via='coolq_http_api')
class CoolQHttpApiAdapter(Adapter):
    def __init__(self, config: dict):
        super().__init__(config)
        if not config.get('api_url'):
            raise ConfigurationError
        self.api_url = config['api_url']
        self.token = config.get('token')
        self.session = requests.Session()
        if self.token:
            self.session.headers['Authorization'] = 'token ' + self.token

    def unitize_context(self, ctx_msg: dict):
        # Check token
        if self.token:
            if flask_req.headers.get('Authorization', '') != 'token ' + self.token:
                return None

        new_ctx = {'raw_ctx': ctx_msg, 'post_type': ctx_msg['post_type'], 'via': ctx_msg['via'],
                   'login_id': ctx_msg['login_id']}
        if new_ctx['post_type'] != 'message':
            return new_ctx

        new_ctx['time'] = ctx_msg['time']
        new_ctx['msg_type'] = ctx_msg['message_type']
        new_ctx['format'] = 'text'
        new_ctx['content'] = ctx_msg['message']

        login_info = self.get_login_info()
        new_ctx['receiver_name'] = login_info['nickname']
        new_ctx['receiver_id'] = login_info['user_id']
        new_ctx['receiver_tid'] = login_info['user_id']

        new_ctx['sender_id'] = str(ctx_msg.get('user_id', ''))
        new_ctx['sender_tid'] = new_ctx['sender_id']
        json = self.session.get(self.api_url + '/get_stranger_info',
                                params={'user_id': new_ctx['sender_id']}).json()
        if json and json.get('data'):
            new_ctx['sender_name'] = json['data']['nickname']

        if new_ctx['msg_type'] == 'group':
            new_ctx['group_id'] = str(ctx_msg.get('group_id', ''))
            new_ctx['group_tid'] = new_ctx['group_id']

        if new_ctx['msg_type'] == 'discuss':
            new_ctx['discuss_id'] = str(ctx_msg.get('discuss_id', ''))
            new_ctx['discuss_tid'] = new_ctx['discuss_id']

        import re
        if re.search('\\[CQ:at,qq=%s\\]' % new_ctx['receiver_id'], new_ctx['content']):
            new_ctx['content'] = re.sub('\\[CQ:at,qq=%s\\]' % new_ctx['receiver_id'], '', new_ctx['content']).lstrip()
            new_ctx['is_at_me'] = True

        return new_ctx

    def get_login_info(self):
        json = self.session.get(self.api_url + '/get_login_info').json()
        if json and json.get('data'):
            json['user_id'] = str(json['data'].get('user_id', ''))
            json['user_tid'] = json['data']['user_id']
            json['nickname'] = json['data'].get('nickname', '')
        return json

    def get_sender_group_role(self, ctx_msg: dict):
        json = self.session.get(
            self.api_url + '/get_group_member_info',
            params={'group_id': ctx_msg.get('group_id'), 'user_id': ctx_msg.get('sender_id')}
        ).json()
        if json and json.get('data'):
            return json['data']['role']
        return 'member'

    def send_private_message(self, target: dict, content: str):
        params = None
        if target.get('user_id'):
            params = {'user_id': target.get('user_id')}

        if params:
            params['message'] = content
            params['is_raw'] = True
            self.session.get(self.api_url + '/send_private_msg', params=params)

    def send_group_message(self, target: dict, content: str):
        params = None
        if target.get('group_id'):
            params = {'group_id': target.get('group_id')}

        if params:
            params['message'] = content
            params['is_raw'] = True
            self.session.get(self.api_url + '/send_group_msg', params=params)

    def send_discuss_message(self, target: dict, content: str):
        params = None
        if target.get('discuss_id'):
            params = {'discuss_id': target.get('discuss_id')}

        if params:
            params['message'] = content
            params['is_raw'] = True
            self.session.get(self.api_url + '/send_discuss_msg', params=params)
