import functools
import re

from little_shit import get_command_name_separators, get_command_args_separators
from msg_src_adapter import get_adapter_by_ctx

_command_name_seps = get_command_name_separators()
_command_args_seps = get_command_args_separators()


class CommandNotExistsError(Exception):
    pass


class CommandPermissionError(Exception):
    pass


class CommandScopeError(Exception):
    def __init__(self, msg_type):
        self.msg_type = msg_type


class CommandRegistry:
    """
    Represent a map of commands and functions.
    """

    def __init__(self, init_func=None):
        self.init_func = init_func
        self.command_map = {}
        self.alias_map = {}
        self.hidden_command_names = []

    def register(self, command_name, *other_names, hidden=False):
        """
        Register command names and map them to a command function.

        :param command_name: command name to register
        :param other_names: other names of this command
        :param hidden: hide the command name or not
                       NOTE: This is kind of like the 'full_command_only' in restrict(),
                       but only controls ONE command name,
                       while the later controls the whole command.
        """

        def decorator(func):
            if hidden:
                self.hidden_command_names.append(command_name)
            if not hasattr(func, 'restricted'):
                # Apply a default restriction
                func = self.restrict()(func)
            self.command_map[command_name] = func
            for name in other_names:
                self.command_map[name] = func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    # noinspection PyMethodMayBeStatic
    def restrict(self, full_command_only=False, superuser_only=False,
                 group_owner_only=False, group_admin_only=False,
                 allow_private=True, allow_discuss=True, allow_group=True):
        """
        Give a command some restriction.
        This decorator must be put below all register() decorators.
        Example:
            @cr.register('wow', hidden=True)
            @cr.register('another_command_name')
            @cr.restrict(full_command_only=True)
            def wow(_1, _2):
                pass

        :param full_command_only: whether to be called with full command (including registry name)
        :param superuser_only: superuser only
        :param group_owner_only: group owner only when processing group message
        :param group_admin_only: group admin only when processing group message
        :param allow_private: allow private message
        :param allow_discuss: allow discuss message
        :param allow_group: allow group message
        """

        def decorator(func):
            func.restricted = True
            # Visibility
            func.full_command_only = full_command_only
            # Permission
            func.superuser_only = superuser_only
            func.group_owner_only = group_owner_only
            func.group_admin_only = group_admin_only
            # Scope
            func.allow_private = allow_private
            func.allow_discuss = allow_discuss
            func.allow_group = allow_group
            return func

        return decorator

    def call(self, command_name, args_text, ctx_msg, **options):
        """
        Call the command matching the specified command name.

        :param command_name: command name
        :param args_text: arguments as a string
        :param ctx_msg: context message
        :param options: other possible options
        :return: things returned by the command function
        :raises CommandScopeError: the message scope (group or private) is not allowed
        :raises CommandPermissionError: the user is not permitted to call this command
        """
        if command_name in self.command_map:
            func = self.command_map[command_name]
            if not self._check_scope(func, ctx_msg):
                msg_type = ctx_msg.get('msg_type')
                if msg_type == 'group':
                    msg_type_str = '群组消息'
                elif msg_type == 'discuss':
                    msg_type_str = '讨论组消息'
                elif msg_type == 'private':
                    msg_type_str = '私聊消息'
                else:
                    msg_type_str = '未知来源消息'
                raise CommandScopeError(msg_type_str)
            if not self._check_permission(func, ctx_msg):
                raise CommandPermissionError
            return func(args_text, ctx_msg, **options)

    @staticmethod
    def _check_scope(func, ctx_msg):
        """
        Check if current message scope (group or private) is allowed.

        :param func: command function to check
        :param ctx_msg: context message
        :return: allowed or not
        """
        allowed_msg_type = set()
        if func.allow_group:
            allowed_msg_type.add('group')
        if func.allow_discuss:
            allowed_msg_type.add('discuss')
        if func.allow_private:
            allowed_msg_type.add('private')

        if ctx_msg.get('msg_type') in allowed_msg_type:
            return True
        return False

    # noinspection PyTypeChecker
    @staticmethod
    def _check_permission(func, ctx_msg):
        """
        Check if current message sender is permitted to call this command.

        :param func: command function to check
        :param ctx_msg: context message
        :return: permitted or not
        """
        adapter = get_adapter_by_ctx(ctx_msg)
        if adapter.is_sender_superuser(ctx_msg):
            return True  # Superuser is the BIG BOSS

        if func.superuser_only:
            return False

        if ctx_msg.get('msg_type') == 'group':
            # TODO: 在酷 Q 测试一下
            allowed_roles = {'owner', 'admin', 'member'}
            if func.group_admin_only:
                allowed_roles.intersection_update({'owner', 'admin'})
            if func.group_owner_only:
                allowed_roles.intersection_update({'owner'})

            role = adapter.get_sender_group_role(ctx_msg)
            if role not in allowed_roles:
                return False

        # Still alive, let go
        return True

    def has(self, command_name):
        """
        Check if this registry has the specified command name,
        except command names that is hidden and full command only.

        :param command_name: command name
        :return: has or not
        """
        return command_name in self.command_map \
               and command_name not in self.hidden_command_names \
               and not self.command_map.get(command_name).full_command_only

    def has_include_hidden(self, command_name):
        """
        Check if this registry has the specified command name,
        including command names that is hidden and full command only.

        :param command_name: command name
        :return: has or not
        """
        return command_name in self.command_map


class CommandHub:
    """
    Represent series of command registries,
    which means it's used as a collection of different registries
    and allows same command names.
    """

    def __init__(self):
        self.registry_map = {}

    def add_registry(self, registry_name, registry):
        """
        Add a registry to the hub, running the init function of the registry.

        :param registry_name: registry name
        :param registry: registry object
        """
        if registry.init_func:
            registry.init_func()
        self.registry_map[registry_name] = registry

    def call(self, command_name, args_text, ctx_msg, **options):
        """
        Call the commands matching the specified command name.

        :param command_name: command name
        :param args_text: arguments as a string
        :param ctx_msg: context message
        :param options: other possible options
        :return: things returned by the command function
                 (list of things if more than one matching command)
        :raises CommandNotExistsError: no command exists
        :raises CommandScopeError: the message scope is disallowed by all commands
        :raises CommandPermissionError: the user is baned by all commands
        """
        if not command_name:
            # If the command name is empty, we just return
            return None

        command = re.split('|'.join(_command_name_seps), command_name, 1)
        if len(command) == 2 and command[0] in self.registry_map:
            registry = self.registry_map.get(command[0])
            if registry.has_include_hidden(command[1]):
                return registry.call(command[1], args_text, ctx_msg, **options)
            else:
                raise CommandNotExistsError
        else:
            results = []
            cmd_exists = False
            permitted = False
            for registry in self.registry_map.values():
                # Trying to call all commands with the name
                if registry.has(command_name):
                    cmd_exists = True
                    try:
                        results.append(
                            registry.call(command_name, args_text, ctx_msg, **options))
                        permitted = True  # If it's permitted, this will be set
                    except CommandPermissionError:
                        pass
            if not cmd_exists:
                raise CommandNotExistsError
            if not permitted:
                # No command was permitted
                raise CommandPermissionError
            return results


hub = CommandHub()


class CommandArgumentError(Exception):
    pass


def split_arguments(maxsplit=0):
    """
    To use this decorator, you should add a parameter exactly named 'argv' to the function of the command,
    which will be set to the split argument list when called.

    However, the first parameter, typically 'args_text', will remain to be the whole argument string, like before.

    :param maxsplit: max split time
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(argument, *args, **kwargs):
            if argument is None:
                raise CommandArgumentError
            if kwargs.get('argv') is not None:
                argv = kwargs['argv']
                del kwargs['argv']
            elif isinstance(argument, (list, tuple)):
                argv = list(argument)
            else:
                argv = list(filter(lambda arg: arg, re.split('|'.join(_command_args_seps), argument, maxsplit)))
            return func(argument, argv=argv, *args, **kwargs)

        return wrapper

    return decorator
