from typing import Literal, Callable

Scope = Literal["PRIVATE", "DISCUSS", "GROUP", "ALL"]
Handler = Callable[["Event", dict], None]
