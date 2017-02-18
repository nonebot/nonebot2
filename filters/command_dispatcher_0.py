import re
import sys

import interactive
from filter import as_filter
from command import CommandNotExistsError, CommandScopeError, CommandPermissionError
from little_shit import *
from commands import core
from command import hub as cmdhub

_fallback_command = get_fallback_command()
_command_start_flags = get_command_start_flags()
_command_args_start_flags = get_command_args_start_flags()


@as_filter(priority=0)
def _dispatch_command(ctx_msg):
    text = ctx_msg.get('text', '').lstrip()
    try:
        if not text:
            raise SkipException
        source = get_source(ctx_msg)
        start_flag = None
        for flag in _command_start_flags:
            # Match the command start flag
            if text.startswith(flag):
                start_flag = flag
                break
        ctx_msg['start_flag'] = start_flag
        if start_flag is None or len(text) <= len(start_flag):
            # Note: use `start_flag is None` here because empty string is allowed to be the start flag
            # No command, check if a session exists
            if interactive.has_session(source):
                command = [interactive.get_session(source).cmd, text]
            else:
                # Use fallback
                if _fallback_command:
                    command = [_fallback_command, text]
                    ctx_msg['is_fallback'] = True
                else:
                    # No fallback
                    raise SkipException
        else:
            # Split command and arguments
            command = re.split('|'.join(_command_args_start_flags),
                               text[len(start_flag):], 1)
            if len(command) == 1:
                # Add an empty argument
                command.append('')
            # Starting a new command, so remove previous command session, if any
            interactive.remove_session(source)

        command[0] = command[0].lower()
        ctx_msg['command'] = command[0]
        cmdhub.call(command[0], command[1], ctx_msg)
    except SkipException:
        # Skip this message
        pass
    except CommandNotExistsError:
        if ctx_msg['start_flag'] == '' and _fallback_command:
            # Empty command start flag is allowed, use fallback
            command = [_fallback_command, text]
            command[0] = command[0].lower()
            ctx_msg['command'] = command[0]
            ctx_msg['is_fallback'] = True
            cmdhub.call(command[0], command[1], ctx_msg)
        else:
            core.echo('暂时还没有这个命令哦～', ctx_msg)
    except CommandPermissionError:
        core.echo('你没有权限使用这个命令哦～', ctx_msg)
    except CommandScopeError as se:
        core.echo('这个命令不支持' + se.msg_type + '哦～', ctx_msg)


def _add_registry_mod_cb(mod):
    mod_name = mod.__name__.split('.')[1]
    try:
        cmdhub.add_registry(mod_name, mod.__registry__)
    except AttributeError:
        print('Failed to load command module "' + mod_name + '.py".', file=sys.stderr)


load_plugins('commands', module_callback=_add_registry_mod_cb)
