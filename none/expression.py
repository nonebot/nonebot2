import random
from typing import Union, Sequence, Callable

from aiocqhttp import message


def render(expr: Union[str, Sequence[str], Callable], *, escape_args=True,
           **kwargs) -> str:
    if isinstance(expr, Callable):
        expr = expr()
    elif isinstance(expr, Sequence):
        expr = random.choice(expr)
    if escape_args:
        for k, v in kwargs.items():
            if isinstance(v, str):
                kwargs[k] = message.escape(v)
    return expr.format(**kwargs)
