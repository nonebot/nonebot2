from nonebot import on_request, RequestSession
from nonebot import on_notice, NoticeSession


# 将函数注册为群请求处理器
@on_request('group')
async def _(session: RequestSession):
    # 判断验证信息是否符合要求
    if session.ctx['comment'] == '暗号':
        # 验证信息正确，同意入群
        await session.approve()
        return
    # 验证信息错误，拒绝入群
    await session.reject('请说暗号')


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    await session.send('欢迎新朋友～')
