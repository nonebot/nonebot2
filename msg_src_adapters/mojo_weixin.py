import requests

from msg_src_adapter import Adapter, as_adapter, ConfigurationError


@as_adapter(via='mojo_weixin')
class MojoWeixinAdapter(Adapter):
    def __init__(self, config: dict):
        super().__init__(config)
        if not config.get('api_url'):
            raise ConfigurationError
        self.api_url = config['api_url']

    def unitize_context(self, ctx_msg: dict):
        new_ctx = {'raw_ctx': ctx_msg, 'post_type': ctx_msg['post_type'], 'via': ctx_msg['via'],
                   'login_id': ctx_msg['login_id']}

        if ctx_msg['type'].endswith('group_notice'):
            new_ctx['post_type'] = 'notice'  # Make 'group_notice' a notice but not a message, and ignore it later

        if new_ctx['post_type'] != 'receive_message':
            return new_ctx

        new_ctx['post_type'] = 'message'  # Just handle 'receive_message', and make 'post_type' 'message'
        new_ctx['time'] = ctx_msg['time']
        new_ctx['msg_id'] = str(ctx_msg['id'])
        new_ctx['msg_type'] = ctx_msg['type'].split('_')[0]
        new_ctx['msg_type'] = 'private' if new_ctx['msg_type'] == 'friend' else new_ctx['msg_type']
        new_ctx['format'] = ctx_msg.get('format', 'text')
        new_ctx['content'] = ctx_msg['content']

        new_ctx['receiver'] = ctx_msg.get('receiver', '')
        new_ctx['receiver_name'] = ctx_msg.get('receiver_name', '')
        new_ctx['receiver_id'] = ctx_msg.get('receiver_account', '')
        new_ctx['receiver_tid'] = ctx_msg.get('receiver_id', '')

        new_ctx['sender'] = ctx_msg.get('sender', '')
        new_ctx['sender_name'] = ctx_msg.get('sender_name', '')
        new_ctx['sender_id'] = ctx_msg.get('sender_account', '')
        new_ctx['sender_tid'] = ctx_msg.get('sender_id', '')

        if new_ctx['msg_type'] == 'group':
            new_ctx['group'] = ctx_msg.get('group', '')
            new_ctx['group_id'] = ''  # WeChat does not has a unique group id that won't change after re-login
            new_ctx['group_tid'] = ctx_msg.get('group_id', '')

        # Check if the sender is a massive platform
        friend_list = requests.get(self.api_url + '/search_friend', params={'id': ctx_msg.get('sender_id')}).json()
        if friend_list and len(friend_list) > 0:
            if friend_list[0].get('category') == '公众号':
                new_ctx['is_massive_platform'] = True

        return new_ctx

    def get_login_info(self):
        json = requests.get(self.api_url + '/get_user_info').json()
        if json:
            json['user_tid'] = json.get('id')
            json['user_id'] = json.get('account')
            json['nickname'] = json.get('name')
        return json

    def send_private_message(self, target: dict, content: str):
        params = None
        if target.get('user_id'):
            params = {'account': target.get('user_id')}
        elif target.get('user_tid'):
            params = {'id': target.get('user_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_friend_message', params=params)

    def send_group_message(self, target: dict, content: str):
        params = None
        if target.get('group_tid'):
            params = {'id': target.get('group_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_group_message', params=params)

    def consult(self, account: str, content: str):
        return requests.get(self.api_url + '/consult', params={'account': account, 'content': content}).json()
