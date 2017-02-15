import hashlib
import random
from datetime import datetime

from little_shit import get_message_sources

_adapter_classes = {}  # one message source, one adapter class
_adapter_instances = {}  # one login account, one adapter instance


def as_adapter(via):
    def decorator(cls):
        _adapter_classes[via] = cls
        return cls

    return decorator


class Adapter(object):
    def __init__(self, config: dict):
        self.login_id = config.get('login_id')
        self.superuser_id = config.get('superuser_id')

    def unitize_context(self, ctx_msg: dict):
        return None

    def send_message(self, target: dict, content):
        if target is None or content is None:
            return

        msg_type = target.get('msg_type', 'private')
        if msg_type == 'group' and hasattr(self, 'send_group_message'):
            self.send_group_message(target, content)
        elif msg_type == 'discuss' and hasattr(self, 'send_discuss_message'):
            self.send_discuss_message(target, content)
        elif msg_type == 'private' and hasattr(self, 'send_private_message'):
            if 'user_id' not in target and 'sender_id' in target:
                target['user_id'] = target['sender_id']  # compatible with ctx_msg
            elif 'user_tid' not in target and 'sender_tid' in target:
                target['user_tid'] = target.get('sender_tid')  # compatible with ctx_msg

            self.send_private_message(target, content)

            if 'user_id' in target and 'sender_id' in target:
                del target['user_id']
            elif 'user_tid' in target and 'sender_tid' in target:
                del target['user_tid']

    def get_login_info(self, ctx_msg: dict):
        return {'user_id': ctx_msg.get('login_id')}

    def is_sender_superuser(self, ctx_msg: dict):
        return ctx_msg.get('sender_id') == self.superuser_id

    def get_sender_group_role(self, ctx_msg: dict):
        return 'member'

    @staticmethod
    def get_target(ctx_msg: dict):
        """
        Target is used to distinguish the records in database.
        Note: This value will not change after restarting the bot.

        :return: an unique string (account id with some flags) representing a target,
                 or None if there is no persistent unique value
        """
        if ctx_msg.get('msg_type') == 'group' and ctx_msg.get('group_id'):
            return 'g#' + ctx_msg.get('group_id')
        elif ctx_msg.get('msg_type') == 'discuss' and ctx_msg.get('discuss_id'):
            return 'd#' + ctx_msg.get('discuss_id')
        elif ctx_msg.get('msg_type') == 'private' and ctx_msg.get('sender_id'):
            return 'p#' + ctx_msg.get('sender_id')
        return None

    @staticmethod
    def get_source(ctx_msg: dict):
        """
        Source is used to distinguish the interactive sessions.
        Note: This value may change after restarting the bot.

        :return: a 32 character unique string (md5) representing a source, or a random value if something strange happened
        """
        source = None
        if ctx_msg.get('msg_type') == 'group' and ctx_msg.get('group_tid') and ctx_msg.get('sender_tid'):
            source = 'g#' + ctx_msg.get('group_tid') + '#p#' + ctx_msg.get('sender_tid')
        elif ctx_msg.get('msg_type') == 'discuss' and ctx_msg.get('discuss_tid') and ctx_msg.get('sender_tid'):
            source = 'd#' + ctx_msg.get('discuss_tid') + '#p#' + ctx_msg.get('sender_tid')
        elif ctx_msg.get('msg_type') == 'private' and ctx_msg.get('sender_tid'):
            source = 'p#' + ctx_msg.get('sender_tid')
        if not source:
            source = str(int(datetime.now().timestamp())) + str(random.randint(100, 999))
        return hashlib.md5(source.encode('utf-8')).hexdigest()


class ConfigurationError(KeyError):
    pass


def get_adapter_by_ctx(ctx_msg: dict):
    if ctx_msg:
        via = ctx_msg.get('via')
        login_id = ctx_msg.get('login_id')
        return get_adapter(via, login_id)
    return None


def get_adapter(via: str, login_id: str):
    if via == 'default':
        # For the situations where 'via' does not matter, e.g. when we just want 'get_target' (which is universal)
        if 'default' in _adapter_instances:
            return _adapter_instances['default']
        else:
            _adapter_instances['default'] = Adapter({})
            return _adapter_instances['default']

    if not (via and login_id):
        return None

    key = hashlib.md5(via.encode('utf-8') + login_id.encode('utf-8')).hexdigest()
    if key in _adapter_instances:
        return _adapter_instances[key]
    else:
        msg_src_list = list(filter(
            lambda msg_src: msg_src['via'] == via and msg_src['login_id'] == login_id,
            get_message_sources()
        ))
        if len(msg_src_list):
            _adapter_instances[key] = _adapter_classes[via](msg_src_list[0])
            return _adapter_instances[key]
        else:
            return None
