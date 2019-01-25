from typing import Callable, Any, Awaitable, Union, List, TYPE_CHECKING

from nonebot.helpers import render_expression

if TYPE_CHECKING:
    from nonebot.command import CommandSession

ArgFilter_T = Callable[[Any], Union[Any, Awaitable[Any]]]


class ValidateError(ValueError):
    def __init__(self, message=None):
        self.message = message


async def run_arg_filters(session: 'CommandSession',
                          arg_filters: List[ArgFilter_T]) -> None:
    """
    Run a specific list of argument filters on a command session.

    This will call all argument filter functions successively,
    with `session.current_arg` as the argument.

    If all filters are passed, the final result will be put into
    `session.state` with the key `session.current_key`.

    If some validation failed, the session will be paused and
    failure message will be sent to the user.

    :param session: command session to run on
    :param arg_filters: argument filters
    """
    arg = session.current_arg
    for f in arg_filters:
        try:
            res = f(arg)
            if isinstance(res, Awaitable):
                res = await res
            arg = res
        except ValidateError as e:
            # validation failed
            failure_message = e.message
            if failure_message is None:
                failure_message = render_expression(
                    session.bot.config.DEFAULT_VALIDATION_FAILURE_EXPRESSION
                )
            # noinspection PyProtectedMember
            session.pause(failure_message, **session._current_send_kwargs)

    # passed all filters
    session.state[session.current_key] = arg
