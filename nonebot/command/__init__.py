import asyncio
import re
import shlex
import warnings
from datetime import datetime
from functools import partial
from typing import (
    Tuple, Union, Callable, Iterable, Any, Optional, List, Dict,
    Awaitable
)

from nonebot import NoneBot, permission as perm
from nonebot.command.argfilter import ValidateError
from nonebot.helpers import context_id, send, render_expression
from nonebot.log import logger
from nonebot.message import Message
from nonebot.session import BaseSession
from nonebot.typing import (
    Context_T, CommandName_T, CommandArgs_T, Message_T, State_T,
    Filter_T
)

# key: one segment of command name
# value: subtree or a leaf Command object
_registry = {}  # type: Dict[str, Union[Dict, Command]]

# key: alias
# value: real command name
_aliases = {}  # type: Dict[str, CommandName_T]

# key: context id
# value: CommandSession object
_sessions = {}  # type: Dict[str, CommandSession]

CommandHandler_T = Callable[['CommandSession'], Any]


class Command:
    __slots__ = ('name', 'func',
                 'permission',
                 'only_to_me',
                 'privileged',
                 'args_parser_func')

    def __init__(self, *,
                 name: CommandName_T,
                 func: CommandHandler_T,
                 permission: int,
                 only_to_me: bool,
                 privileged: bool):
        self.name = name
        self.func = func
        self.permission = permission
        self.only_to_me = only_to_me
        self.privileged = privileged
        self.args_parser_func: Optional[CommandHandler_T] = None

    async def run(self, session, *,
                  check_perm: bool = True,
                  dry: bool = False) -> bool:
        """
        Run the command in a given session.

        :param session: CommandSession object
        :param check_perm: should check permission before running
        :param dry: just check any prerequisite, without actually running
        :return: the command is finished (or can be run, given dry == True)
        """
        has_perm = await self._check_perm(session) if check_perm else True
        if self.func and has_perm:
            if dry:
                return True

            if session.current_arg_filters is not None and \
                    session.current_key is not None:
                # argument-level filters are given, use them
                arg = session.current_arg
                config = session.bot.config
                for f in session.current_arg_filters:
                    try:
                        res = f(arg)
                        if isinstance(res, Awaitable):
                            res = await res
                        arg = res
                    except ValidateError as e:
                        # validation failed
                        if config.MAX_VALIDATION_FAILURES > 0:
                            # should check number of validation failures
                            session.state['__validation_failure_num'] = \
                                session.state.get(
                                    '__validation_failure_num', 0) + 1

                            if session.state['__validation_failure_num'] >= \
                                    config.MAX_VALIDATION_FAILURES:
                                # noinspection PyProtectedMember
                                session.finish(render_expression(
                                    config.TOO_MANY_VALIDATION_FAILURES_EXPRESSION
                                ), **session._current_send_kwargs)

                        failure_message = e.message
                        if failure_message is None:
                            failure_message = render_expression(
                                config.DEFAULT_VALIDATION_FAILURE_EXPRESSION
                            )
                        # noinspection PyProtectedMember
                        session.pause(failure_message,
                                      **session._current_send_kwargs)

                # passed all filters
                session.state[session.current_key] = arg
            else:
                # fallback to command-level args_parser_func
                if self.args_parser_func:
                    await self.args_parser_func(session)
                if session.current_key is not None and \
                        session.current_key not in session.state:
                    # args_parser_func didn't set state, here we set it
                    session.state[session.current_key] = session.current_arg

            await self.func(session)
            return True
        return False

    async def _check_perm(self, session) -> bool:
        """
        Check if the session has sufficient permission to
        call the command.

        :param session: CommandSession object
        :return: the session has the permission
        """
        return await perm.check_permission(session.bot, session.ctx,
                                           self.permission)

    def __repr__(self):
        return f'<Command, name={self.name.__repr__()}>'

    def __str__(self):
        return self.__repr__()


class CommandFunc:
    __slots__ = ('cmd', 'func')

    def __init__(self, cmd: Command, func: CommandHandler_T):
        self.cmd = cmd
        self.func = func

    def __call__(self, session: 'CommandSession') -> Any:
        return self.func(session)

    def args_parser(self, parser_func: CommandHandler_T) -> CommandHandler_T:
        """
        Decorator to register a function as the arguments parser of
        the corresponding command.
        """
        self.cmd.args_parser_func = parser_func
        return parser_func


def on_command(name: Union[str, CommandName_T], *,
               aliases: Union[Iterable[str], str] = (),
               permission: int = perm.EVERYBODY,
               only_to_me: bool = True,
               privileged: bool = False,
               shell_like: bool = False) -> Callable:
    """
    Decorator to register a function as a command.

    :param name: command name (e.g. 'echo' or ('random', 'number'))
    :param aliases: aliases of command name, for convenient access
    :param permission: permission required by the command
    :param only_to_me: only handle messages to me
    :param privileged: can be run even when there is already a session
    :param shell_like: use shell-like syntax to split arguments
    """

    def deco(func: CommandHandler_T) -> CommandHandler_T:
        if not isinstance(name, (str, tuple)):
            raise TypeError('the name of a command must be a str or tuple')
        if not name:
            raise ValueError('the name of a command must not be empty')

        cmd_name = (name,) if isinstance(name, str) else name

        cmd = Command(name=cmd_name, func=func, permission=permission,
                      only_to_me=only_to_me, privileged=privileged)
        if shell_like:
            async def shell_like_args_parser(session):
                session.args['argv'] = shlex.split(session.current_arg)

            cmd.args_parser_func = shell_like_args_parser

        current_parent = _registry
        for parent_key in cmd_name[:-1]:
            current_parent[parent_key] = current_parent.get(parent_key) or {}
            current_parent = current_parent[parent_key]
            if not isinstance(current_parent, dict):
                warnings.warn(f'{current_parent} is not a registry dict')
                return func
        if cmd_name[-1] in current_parent:
            warnings.warn(f'There is already a command named {cmd_name}')
            return func
        current_parent[cmd_name[-1]] = cmd

        nonlocal aliases
        if isinstance(aliases, str):
            aliases = (aliases,)
        for alias in aliases:
            _aliases[alias] = cmd_name

        return CommandFunc(cmd, func)

    return deco


def _find_command(name: Union[str, CommandName_T]) -> Optional[Command]:
    cmd_name = (name,) if isinstance(name, str) else name
    if not cmd_name:
        return None

    cmd_tree = _registry
    for part in cmd_name[:-1]:
        if part not in cmd_tree or not isinstance(cmd_tree[part], dict):
            return None
        cmd_tree = cmd_tree[part]

    cmd = cmd_tree.get(cmd_name[-1])
    return cmd if isinstance(cmd, Command) else None


class _PauseException(Exception):
    """
    Raised by session.pause() indicating that the command session
    should be paused to ask the user for some arguments.
    """
    pass


class _FinishException(Exception):
    """
    Raised by session.finish() indicating that the command session
    should be stopped and removed.
    """

    def __init__(self, result: bool = True):
        """
        :param result: succeeded to call the command
        """
        self.result = result


class SwitchException(Exception):
    """
    Raised by session.switch() indicating that the command session
    should be stopped and replaced with a new one (going through
    handle_message() again).

    Since the new context message will go through handle_message()
    again, the later function should be notified. So this exception
    is designed to be propagated to handle_message().
    """

    def __init__(self, new_ctx_message: Message):
        """
        :param new_ctx_message: new message which should be placed in context
        """
        self.new_ctx_message = new_ctx_message


class CommandSession(BaseSession):
    __slots__ = ('cmd',
                 'current_key', 'current_arg_filters', '_current_send_kwargs',
                 'current_arg', '_current_arg_text', '_current_arg_images',
                 '_state', '_last_interaction', '_running', '_run_future')

    def __init__(self, bot: NoneBot, ctx: Context_T, cmd: Command, *,
                 current_arg: str = '', args: Optional[CommandArgs_T] = None):
        super().__init__(bot, ctx)
        self.cmd = cmd  # Command object

        # unique key of the argument that is currently requesting (asking)
        self.current_key: Optional[str] = None

        # initialize current argument filters
        self.current_arg_filters: Optional[List[Filter_T]] = None

        self._current_send_kwargs: Dict[str, Any] = {}

        # initialize current argument
        self.current_arg: str = ''  # with potential CQ codes
        self._current_arg_text = None
        self._current_arg_images = None
        self.refresh(ctx, current_arg=current_arg)  # fill the above

        self._run_future = partial(asyncio.run_coroutine_threadsafe,
                                   loop=bot.loop)

        self._state: State_T = {}
        if args:
            self._state.update(args)

        self._last_interaction = None  # last interaction time of this session
        self._running = False

    @property
    def state(self) -> State_T:
        """
        State of the session.

        This contains all named arguments and
        other session scope temporary values.
        """
        return self._state

    @property
    def args(self) -> CommandArgs_T:
        """Deprecated. Use `session.state` instead."""
        return self.state

    @property
    def running(self) -> bool:
        return self._running

    @running.setter
    def running(self, value) -> None:
        if self._running is True and value is False:
            # change status from running to not running, record the time
            self._last_interaction = datetime.now()
        self._running = value

    @property
    def is_valid(self) -> bool:
        """Check if the session is expired or not."""
        if self.bot.config.SESSION_EXPIRE_TIMEOUT and \
                self._last_interaction and \
                datetime.now() - self._last_interaction > \
                self.bot.config.SESSION_EXPIRE_TIMEOUT:
            return False
        return True

    @property
    def is_first_run(self) -> bool:
        return self._last_interaction is None

    @property
    def current_arg_text(self) -> str:
        """
        Plain text part in the current argument, without any CQ codes.
        """
        if self._current_arg_text is None:
            self._current_arg_text = Message(
                self.current_arg).extract_plain_text()
        return self._current_arg_text

    @property
    def current_arg_images(self) -> List[str]:
        """
        Images (as list of urls) in the current argument.
        """
        if self._current_arg_images is None:
            self._current_arg_images = [
                s.data['url'] for s in Message(self.current_arg)
                if s.type == 'image' and 'url' in s.data
            ]
        return self._current_arg_images

    @property
    def argv(self) -> List[str]:
        """
        Shell-like argument list, similar to sys.argv.
        Only available while shell_like is True in on_command decorator.
        """
        return self.state.get('argv', [])

    def refresh(self, ctx: Context_T, *, current_arg: str = '') -> None:
        """
        Refill the session with a new message context.

        :param ctx: new message context
        :param current_arg: new command argument as a string
        """
        self.ctx = ctx
        self.current_arg = current_arg
        self._current_arg_text = None
        self._current_arg_images = None

    def get(self, key: str, *,
            prompt: Optional[Message_T] = None,
            arg_filters: Optional[List[Filter_T]] = None,
            **kwargs) -> Any:
        """
        Get an argument with a given key.

        If the argument does not exist in the current session,
        a pause exception will be raised, and the caller of
        the command will know it should keep the session for
        further interaction with the user.

        :param key: argument key
        :param prompt: prompt to ask the user
        :param arg_filters: argument filters for the next user input
        :return: the argument value
        """
        if key in self.state:
            return self.state[key]

        self.current_key = key
        self.current_arg_filters = arg_filters
        self._current_send_kwargs = kwargs
        self.pause(prompt, **kwargs)

    def get_optional(self, key: str,
                     default: Optional[Any] = None) -> Optional[Any]:
        """
        Simply get a argument with given key.

        Deprecated. Use `session.state.get()` instead.
        """
        return self.state.get(key, default)

    def pause(self, message: Optional[Message_T] = None, **kwargs) -> None:
        """Pause the session for further interaction."""
        if message:
            self._run_future(self.send(message, **kwargs))
        raise _PauseException

    def finish(self, message: Optional[Message_T] = None, **kwargs) -> None:
        """Finish the session."""
        if message:
            self._run_future(self.send(message, **kwargs))
        raise _FinishException

    def switch(self, new_ctx_message: Message_T) -> None:
        """
        Finish the session and switch to a new (fake) message context.

        The user may send another command (or another intention as natural
        language) when interacting with the current session. In this case,
        the session may not understand what the user is saying, so it
        should call this method and pass in that message, then NoneBot will
        handle the situation properly.
        """
        if self.is_first_run:
            # if calling this method during first run,
            # we think the command is not handled
            raise _FinishException(result=False)

        if not isinstance(new_ctx_message, Message):
            new_ctx_message = Message(new_ctx_message)
        raise SwitchException(new_ctx_message)


def parse_command(bot: NoneBot,
                  cmd_string: str) -> Tuple[Optional[Command], Optional[str]]:
    """
    Parse a command string (typically from a message).

    :param bot: NoneBot instance
    :param cmd_string: command string
    :return: (Command object, current arg string)
    """
    logger.debug(f'Parsing command: {cmd_string}')

    matched_start = None
    for start in bot.config.COMMAND_START:
        # loop through COMMAND_START to find the longest matched start
        curr_matched_start = None
        if isinstance(start, type(re.compile(''))):
            m = start.search(cmd_string)
            if m and m.start(0) == 0:
                curr_matched_start = m.group(0)
        elif isinstance(start, str):
            if cmd_string.startswith(start):
                curr_matched_start = start

        if curr_matched_start is not None and \
                (matched_start is None or
                 len(curr_matched_start) > len(matched_start)):
            # a longer start, use it
            matched_start = curr_matched_start

    if matched_start is None:
        # it's not a command
        logger.debug('It\'s not a command')
        return None, None

    logger.debug(f'Matched command start: '
                 f'{matched_start}{"(empty)" if not matched_start else ""}')
    full_command = cmd_string[len(matched_start):].lstrip()

    if not full_command:
        # command is empty
        return None, None

    cmd_name_text, *cmd_remained = full_command.split(maxsplit=1)
    cmd_name = _aliases.get(cmd_name_text)

    if not cmd_name:
        for sep in bot.config.COMMAND_SEP:
            # loop through COMMAND_SEP to find the most optimized split
            curr_cmd_name = None
            if isinstance(sep, type(re.compile(''))):
                curr_cmd_name = tuple(sep.split(cmd_name_text))
            elif isinstance(sep, str):
                curr_cmd_name = tuple(cmd_name_text.split(sep))

            if curr_cmd_name is not None and \
                    (not cmd_name or len(curr_cmd_name) > len(cmd_name)):
                # a more optimized split, use it
                cmd_name = curr_cmd_name

        if not cmd_name:
            cmd_name = (cmd_name_text,)

    logger.debug(f'Split command name: {cmd_name}')
    cmd = _find_command(cmd_name)
    if not cmd:
        logger.debug(f'Command {cmd_name} not found')
        return None, None

    logger.debug(f'Command {cmd.name} found, function: {cmd.func}')
    return cmd, ''.join(cmd_remained)


async def handle_command(bot: NoneBot, ctx: Context_T) -> bool:
    """
    Handle a message as a command.

    This function is typically called by "handle_message".

    :param bot: NoneBot instance
    :param ctx: message context
    :return: the message is handled as a command
    """
    cmd, current_arg = parse_command(bot, str(ctx['message']).lstrip())
    is_privileged_cmd = cmd and cmd.privileged
    if is_privileged_cmd and cmd.only_to_me and not ctx['to_me']:
        is_privileged_cmd = False
    disable_interaction = is_privileged_cmd

    if is_privileged_cmd:
        logger.debug(f'Command {cmd.name} is a privileged command')

    ctx_id = context_id(ctx)

    if not is_privileged_cmd:
        # wait for 1.5 seconds (at most) if the current session is running
        retry = 5
        while retry > 0 and \
                _sessions.get(ctx_id) and _sessions[ctx_id].running:
            retry -= 1
            await asyncio.sleep(0.3)

    check_perm = True
    session = _sessions.get(ctx_id) if not is_privileged_cmd else None
    if session:
        if session.running:
            logger.warning(f'There is a session of command '
                           f'{session.cmd.name} running, notify the user')
            asyncio.ensure_future(send(
                bot, ctx,
                render_expression(bot.config.SESSION_RUNNING_EXPRESSION)
            ))
            # pretend we are successful, so that NLP won't handle it
            return True

        if session.is_valid:
            logger.debug(f'Session of command {session.cmd.name} exists')
            # since it's in a session, the user must be talking to me
            ctx['to_me'] = True
            session.refresh(ctx, current_arg=str(ctx['message']))
            # there is no need to check permission for existing session
            check_perm = False
        else:
            # the session is expired, remove it
            logger.debug(f'Session of command {session.cmd.name} is expired')
            if ctx_id in _sessions:
                del _sessions[ctx_id]
            session = None

    if not session:
        if not cmd:
            logger.debug('Not a known command, ignored')
            return False
        if cmd.only_to_me and not ctx['to_me']:
            logger.debug('Not to me, ignored')
            return False
        session = CommandSession(bot, ctx, cmd, current_arg=current_arg)
        logger.debug(f'New session of command {session.cmd.name} created')

    return await _real_run_command(session, ctx_id, check_perm=check_perm,
                                   disable_interaction=disable_interaction)


async def call_command(bot: NoneBot, ctx: Context_T,
                       name: Union[str, CommandName_T], *,
                       current_arg: str = '',
                       args: Optional[CommandArgs_T] = None,
                       check_perm: bool = True,
                       disable_interaction: bool = False) -> bool:
    """
    Call a command internally.

    This function is typically called by some other commands
    or "handle_natural_language" when handling NLPResult object.

    Note: If disable_interaction is not True, after calling this function,
    any previous command session will be overridden, even if the command
    being called here does not need further interaction (a.k.a asking
    the user for more info).

    :param bot: NoneBot instance
    :param ctx: message context
    :param name: command name
    :param current_arg: command current argument string
    :param args: command args
    :param check_perm: should check permission before running command
    :param disable_interaction: disable the command's further interaction
    :return: the command is successfully called
    """
    cmd = _find_command(name)
    if not cmd:
        return False
    session = CommandSession(bot, ctx, cmd, current_arg=current_arg, args=args)
    return await _real_run_command(session, context_id(session.ctx),
                                   check_perm=check_perm,
                                   disable_interaction=disable_interaction)


async def _real_run_command(session: CommandSession,
                            ctx_id: str,
                            disable_interaction: bool = False,
                            **kwargs) -> bool:
    if not disable_interaction:
        # override session only when interaction is not disabled
        _sessions[ctx_id] = session
    try:
        logger.debug(f'Running command {session.cmd.name}')
        session.running = True
        future = asyncio.ensure_future(session.cmd.run(session, **kwargs))
        timeout = None
        if session.bot.config.SESSION_RUN_TIMEOUT:
            timeout = session.bot.config.SESSION_RUN_TIMEOUT.total_seconds()

        try:
            await asyncio.wait_for(future, timeout)
            handled = future.result()
        except asyncio.TimeoutError:
            handled = True
        except (_PauseException, _FinishException, SwitchException) as e:
            raise e
        except Exception as e:
            logger.error(f'An exception occurred while '
                         f'running command {session.cmd.name}:')
            logger.exception(e)
            handled = True
        raise _FinishException(handled)
    except _PauseException:
        session.running = False
        if disable_interaction:
            # if the command needs further interaction, we view it as failed
            return False
        logger.debug(f'Further interaction needed for '
                     f'command {session.cmd.name}')
        # return True because this step of the session is successful
        return True
    except (_FinishException, SwitchException) as e:
        session.running = False
        logger.debug(f'Session of command {session.cmd.name} finished')
        if not disable_interaction and ctx_id in _sessions:
            # the command is finished, remove the session,
            # but if interaction is disabled during this command call,
            # we leave the _sessions untouched.
            del _sessions[ctx_id]

        if isinstance(e, _FinishException):
            return e.result
        elif isinstance(e, SwitchException):
            # we are guaranteed that the session is not first run here,
            # which means interaction is definitely enabled,
            # so we can safely touch _sessions here.
            if ctx_id in _sessions:
                # make sure there is no session waiting
                del _sessions[ctx_id]
            logger.debug(f'Session of command {session.cmd.name} switching, '
                         f'new context message: {e.new_ctx_message}')
            raise e  # this is intended to be propagated to handle_message()


def kill_current_session(ctx: Context_T) -> None:
    """
    Force kill current session of the given context,
    despite whether it is running or not.

    :param ctx: message context
    """
    ctx_id = context_id(ctx)
    if ctx_id in _sessions:
        del _sessions[ctx_id]


from nonebot.command.group import CommandGroup
