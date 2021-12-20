from typing import Union


async def exc(e: Exception, x: Union[ValueError, TypeError]) -> Exception:
    assert e == x
    return e
