import os
import importlib

from command import CommandRegistry
from commands import core
from nl_processor import parse_potential_commands
from little_shit import get_nl_processors_dir
from command import hub as cmdhub


def _init():
    _load_processors()


__registry__ = cr = CommandRegistry(init_func=_init)


@cr.register('process')
@cr.restrict(full_command_only=True)
def process(sentence, ctx_msg, internal=False):
    sentence = sentence.strip()
    potential_commands = parse_potential_commands(sentence)
    potential_commands = sorted(filter(lambda x: x[0] > 60, potential_commands), key=lambda x: x[0], reverse=True)
    if len(potential_commands) > 0:
        most_possible_cmd = potential_commands[0]
        ctx_msg['parsed_data'] = most_possible_cmd[3]
        cmdhub.call(most_possible_cmd[1], most_possible_cmd[2], ctx_msg)
    else:
        core.echo('我暂时不理解你在说什么哦～', ctx_msg, internal)


def _load_processors():
    processor_mod_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(get_nl_processors_dir())
    )
    command_mods = [os.path.splitext(file)[0] for file in processor_mod_files]
    for mod_name in command_mods:
        importlib.import_module('nl_processors.' + mod_name)
