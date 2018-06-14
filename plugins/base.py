import none


@none.on_command('echo', aliases=('say',))
async def _(bot, ctx, cmd):
    await bot.send(ctx, cmd.arg)
