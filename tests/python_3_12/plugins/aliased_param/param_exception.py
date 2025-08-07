type AliasedException = Exception


async def aliased_exc(e: AliasedException) -> Exception:
    return e
