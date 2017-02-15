import requests

from msg_src_adapter import Adapter, as_adapter, ConfigurationError


@as_adapter(via='mojo_webqq')
class MojoWebqqAdapter(Adapter):
    def __init__(self, config: dict):
        super().__init__(config)
        if not config.get('api_url'):
            raise ConfigurationError
        self.api_url = config['api_url']

    def unitize_context(self, ctx_msg: dict):
        new_ctx = {'raw_ctx': ctx_msg, 'post_type': ctx_msg['post_type'], 'via': ctx_msg['via'],
                   'login_id': ctx_msg['login_id']}
        if new_ctx['post_type'] != 'receive_message':
            return new_ctx
        new_ctx['post_type'] = 'message'  # Just handle 'receive_message', and make 'post_type' 'message'
        new_ctx['time'] = ctx_msg['time']
        new_ctx['msg_id'] = str(ctx_msg['id'])
        new_ctx['msg_type'] = ctx_msg['type'].split('_')[0]
        new_ctx['msg_type'] = 'private' if new_ctx['msg_type'] == 'friend' else new_ctx['msg_type']
        new_ctx['format'] = 'text'
        new_ctx['content'] = ctx_msg['content']

        new_ctx['receiver'] = ctx_msg.get('receiver', '')
        new_ctx['receiver_name'] = (requests.get(self.api_url + '/get_user_info').json() or {}).get('name', '')
        new_ctx['receiver_id'] = str(ctx_msg.get('receiver_uid', ''))
        new_ctx['receiver_tid'] = str(ctx_msg.get('receiver_id', ''))

        new_ctx['sender'] = ctx_msg.get('sender', '')
        friend = list(filter(
            lambda f: f.get('uid') == ctx_msg['sender_uid'],
            requests.get(self.api_url + '/get_friend_info').json() or []
        ))
        new_ctx['sender_name'] = friend[0].get('name', '') if friend else ''
        new_ctx['sender_id'] = str(ctx_msg.get('sender_uid', ''))
        new_ctx['sender_tid'] = str(ctx_msg.get('sender_id', ''))

        if new_ctx['msg_type'] == 'group':
            new_ctx['group'] = ctx_msg.get('group', '')
            new_ctx['group_id'] = str(ctx_msg.get('group_uid', ''))
            new_ctx['group_tid'] = str(ctx_msg.get('group_id', ''))

        if new_ctx['msg_type'] == 'discuss':
            new_ctx['discuss'] = ctx_msg.get('discuss', '')
            new_ctx['discuss_tid'] = str(ctx_msg.get('discuss_id', ''))

        return new_ctx

    def get_login_info(self):
        json = requests.get(self.api_url + '/get_user_info').json()
        if json:
            json['user_tid'] = json.get('id')
            json['user_id'] = json.get('uid')
            json['nickname'] = json.get('name')
        return json

    def _get_group_info(self):
        return requests.get(self.api_url + '/get_group_info').json()

    def get_sender_group_role(self, ctx_msg: dict):
        groups = list(filter(
            lambda g: str(g.get('id')) == ctx_msg['raw_ctx'].get('group_id'),
            self._get_group_info() or []
        ))
        if len(groups) <= 0 or 'member' not in groups[0]:
            # This is strange, not likely happens
            return 'member'
        members = list(filter(
            lambda m: str(m.get('id')) == ctx_msg['raw_ctx'].get('sender_id'),
            groups[0].get('member')
        ))
        if len(members) <= 0:
            # This is strange, not likely happens
            return 'member'
        return members[0].get('role', 'member')

    def send_private_message(self, target: dict, content: str):
        params = None
        if target.get('user_id'):
            params = {'uid': target.get('user_id')}
        elif target.get('user_tid'):
            params = {'id': target.get('user_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_friend_message', params=params)

    def send_group_message(self, target: dict, content: str):
        params = None
        if target.get('group_id'):
            params = {'uid': target.get('group_id')}
        elif target.get('group_tid'):
            params = {'id': target.get('group_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_group_message', params=params)

    def send_discuss_message(self, target: dict, content: str):
        params = None
        if target.get('discuss_tid'):
            params = {'id': target.get('discuss_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_discuss_message', params=params)
