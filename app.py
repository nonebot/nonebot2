import re
import sys
import importlib

from flask import Flask, request

import interactive
from little_shit import *
from config import config
from command import hub as cmdhub
from command import CommandNotExistsError, CommandScopeError, CommandPermissionError
from apiclient import client as api
from filter import apply_filters

app = Flask(__name__)

_fallback_command = config.get('fallback_command')
_command_start_flags = get_command_start_flags()
_command_args_start_flags = get_command_args_start_flags()


def _send_text(text, ctx_msg):
    msg_type = ctx_msg.get('type')
    if msg_type == 'group_message':
        api.send_group_message(gnumber=ctx_msg.get('gnumber'), content=text)
    elif msg_type == 'message':
        api.send_message(qq=ctx_msg.get('sender_qq'), content=text)


@app.route('/', methods=['POST'])
def _index():
    ctx_msg = request.json
    try:
        if ctx_msg.get('msg_class') != 'recv':
            raise SkipException
        if not apply_filters(ctx_msg):
            raise SkipException
        content = ctx_msg.get('content', '')
        source = get_source(ctx_msg)
        if content.startswith('@'):
            my_group_nick = ctx_msg.get('receiver')
            if not my_group_nick:
                raise SkipException
            at_me = '@' + my_group_nick
            if not content.startswith(at_me):
                my_nick = api.get_user_info().json().get('nick', my_group_nick)
                at_me = '@' + my_nick
                if not content.startswith(at_me):
                    raise SkipException
            content = content[len(at_me):]
        else:
            # Not starts with '@'
            if ctx_msg.get('type') == 'group_message':
                # And it's a group message, so we don't reply
                raise SkipException
        content = content.lstrip()
        start_flag = None
        for flag in _command_start_flags:
            # Match the command start flag
            if content.startswith(flag):
                start_flag = flag
                break
        if not start_flag or len(content) <= len(start_flag):
            # No command, check if a session exists
            if interactive.has_session(source):
                command = [interactive.get_session(source).cmd, content]
            else:
                # Use fallback
                if _fallback_command:
                    command = [_fallback_command, content]
                else:
                    # No fallback
                    raise SkipException
        else:
            # Split command and arguments
            command = re.split('|'.join(_command_args_start_flags),
                               content[len(start_flag):], 1)
            if len(command) == 1:
                # Add an empty argument
                command.append('')
            # Starting a new command, so remove any previous command session
            interactive.remove_session(source)

        cmdhub.call(command[0], command[1], ctx_msg)
    except SkipException:
        # Skip this message
        pass
    except CommandNotExistsError:
        _send_text('暂时还没有这个命令哦～', ctx_msg)
    except CommandPermissionError:
        _send_text('你没有权限使用这个命令哦～', ctx_msg)
    except CommandScopeError as se:
        _send_text('这个命令不支持' + se.msg_type + '哦～', ctx_msg)
    return '', 204


def _load_filters():
    filter_mod_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(get_filters_dir())
    )
    command_mods = [os.path.splitext(file)[0] for file in filter_mod_files]
    for mod_name in command_mods:
        importlib.import_module('filters.' + mod_name)


def _load_commands():
    command_mod_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(get_commands_dir())
    )
    command_mods = [os.path.splitext(file)[0] for file in command_mod_files]
    for mod_name in command_mods:
        cmd_mod = importlib.import_module('commands.' + mod_name)
        try:
            cmdhub.add_registry(mod_name, cmd_mod.__registry__)
        except AttributeError:
            print('Failed to load command module "' + mod_name + '.py".', file=sys.stderr)


if __name__ == '__main__':
    _load_filters()
    _load_commands()
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=os.environ.get('PORT', '8080'))
