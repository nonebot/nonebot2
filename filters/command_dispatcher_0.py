import re
import sys
import importlib

import interactive
from filter import as_filter
from command import CommandNotExistsError, CommandScopeError, CommandPermissionError
from little_shit import *
from commands import core
from command import hub as cmdhub

_fallback_command = get_fallback_command()
_command_start_flags = get_command_start_flags()
_command_args_start_flags = get_command_args_start_flags()


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


@as_filter(priority=0)
def _dispatch_command(ctx_msg):
    try:
        text = ctx_msg.get('text', '').lstrip()
        if not text:
            raise SkipException
        source = get_source(ctx_msg)
        start_flag = None
        for flag in _command_start_flags:
            # Match the command start flag
            if text.startswith(flag):
                start_flag = flag
                break
        if start_flag is None or len(text) <= len(start_flag):
            # Note: use `start_flag is None` here because empty string is allowed to be the start flag
            # No command, check if a session exists
            if interactive.has_session(source):
                command = [interactive.get_session(source).cmd, text]
            else:
                # Use fallback
                if _fallback_command:
                    command = [_fallback_command, text]
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
        core.echo('暂时还没有这个命令哦～', ctx_msg)
    except CommandPermissionError:
        core.echo('你没有权限使用这个命令哦～', ctx_msg)
    except CommandScopeError as se:
        core.echo('这个命令不支持' + se.msg_type + '哦～', ctx_msg)


_load_commands()
