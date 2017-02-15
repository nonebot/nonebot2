import importlib
import os
import functools

from config import config


class SkipException(Exception):
    pass


def _mkdir_if_not_exists_and_return_path(path):
    os.makedirs(path, exist_ok=True)
    return path


def get_root_dir():
    return os.path.split(os.path.realpath(__file__))[0]


def get_plugin_dir(plugin_dir_name):
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), plugin_dir_name))


def load_plugins(plugin_dir_name, module_callback=None):
    plugin_dir = get_plugin_dir(plugin_dir_name)
    plugin_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(plugin_dir)
    )
    plugins = [os.path.splitext(file)[0] for file in plugin_files]
    for mod_name in plugins:
        mod = importlib.import_module(plugin_dir_name + '.' + mod_name)
        if module_callback:
            module_callback(mod)


def get_db_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'db'))


def get_default_db_path():
    return os.path.join(get_db_dir(), 'default.sqlite')


def get_tmp_dir():
    return _mkdir_if_not_exists_and_return_path(os.path.join(get_root_dir(), 'data', 'tmp'))


def get_source(ctx_msg):
    from msg_src_adapter import get_adapter_by_ctx
    return get_adapter_by_ctx(ctx_msg).get_source(ctx_msg)


def get_target(ctx_msg):
    from msg_src_adapter import get_adapter_by_ctx
    return get_adapter_by_ctx(ctx_msg).get_target(ctx_msg)


def check_target(func):
    """
    This decorator checks whether there is a target value, and prevent calling the function if not.
    """

    @functools.wraps(func)
    def wrapper(args_text, ctx_msg, *args, **kwargs):
        from msg_src_adapter import get_adapter_by_ctx
        adapter = get_adapter_by_ctx(ctx_msg)
        target = adapter.get_target(ctx_msg)
        if not target:
            adapter.send_message(ctx_msg, '当前语境无法使用这个命令，请尝试发送私聊消息或稍后再试吧～')
            return
        else:
            return func(args_text, ctx_msg, *args, **kwargs)

    return wrapper


def get_command_start_flags():
    return tuple(sorted(config.get('command_start_flags', ('',)), reverse=True))


def get_command_name_separators():
    return tuple(sorted(('\.',) + config.get('command_name_separators', ()), reverse=True))


def get_command_args_start_flags():
    return tuple(sorted(('[ \t\n]+',) + config.get('command_args_start_flags', ()), reverse=True))


def get_command_args_separators():
    return tuple(sorted(('[ \t\n]+',) + config.get('command_args_separators', ()), reverse=True))


def get_fallback_command():
    return config.get('fallback_command')


def get_fallback_command_after_nl_processors():
    return config.get('fallback_command_after_nl_processors')


def get_message_sources():
    return config.get('message_sources', [])
