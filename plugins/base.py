import none


@none.on_command('echo', aliases=('say',))
async def _(bot, ctx, session):
    await bot.send(ctx, session.arg)
