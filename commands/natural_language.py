from command import CommandRegistry
from commands import core
from nl_processor import parse_potential_commands
from little_shit import load_plugins, get_fallback_command_after_nl_processors
from command import hub as cmdhub


def _init():
    load_plugins('nl_processors')


__registry__ = cr = CommandRegistry(init_func=_init)

_fallback_command = get_fallback_command_after_nl_processors()


@cr.register('process')
@cr.restrict(full_command_only=True)
def process(args_text, ctx_msg):
    sentence = args_text.strip()
    if not sentence:
        core.echo('你什么都没说哦～', ctx_msg)
        return

    potential_commands = parse_potential_commands(sentence)
    potential_commands = sorted(filter(lambda x: x[0] > 60, potential_commands), key=lambda x: x[0], reverse=True)
    # If it's a fallback and with empty start flag, then don't send verbose information
    hide_verbose = ctx_msg.get('is_fallback') and ctx_msg.get('start_flag') == ''
    if len(potential_commands) > 0:
        most_possible_cmd = potential_commands[0]
        core.echo(
            '识别出最可能的等价命令：\n' + ' '.join((most_possible_cmd[1], most_possible_cmd[2])),
            ctx_msg,
            internal=hide_verbose
        )
        ctx_msg['parsed_data'] = most_possible_cmd[3]
        cmdhub.call(most_possible_cmd[1], most_possible_cmd[2], ctx_msg)
    else:
        if _fallback_command:
            core.echo('暂时无法理解你的意思，下面将使用备用命令 ' + _fallback_command + '……',
                      ctx_msg,
                      internal=hide_verbose)
            cmdhub.call(_fallback_command, sentence, ctx_msg)
            return
