from aiocqhttp import Error as CQHttpError

from none import on_notice, NoticeSession

GROUP_GREETING = (
    '欢迎新同学 {name}[]！[CQ:face,id=63][CQ:face,id=63][CQ:face,id=63]',
    '[CQ:face,id=99]欢迎新成员～',
    '欢迎 {name}👏👏～',
    '[CQ:at,qq={user_id}] 欢迎欢迎👏',
)


@on_notice('group_increase')
async def _(session: NoticeSession):
    try:
        info = await session.bot.get_group_member_info(**session.ctx,
                                                       no_cache=True)
        name = info['card'] or info['nickname'] or '新成员'
        await session.send_expr(GROUP_GREETING, name=name, **session.ctx)
    except CQHttpError:
        pass
