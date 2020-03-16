# 处理通知和请求

除了聊天消息，酷Q 还提供了加群请求、加好友请求、出入群通知、管理员变动通知等很多其它事件，很多时候我们需要利用这些事件来实现群管功能，这也是 QQ 机器人除聊天之外的另一个很重要的应用之一。

本章将介绍如何在插件中处理通知和请求。

:::tip 提示
本章的完整代码可以在 [awesome-bot-5](https://github.com/richardchien/nonebot/tree/master/docs/guide/code/awesome-bot-5) 查看。
:::

## 自动同意加群请求

首先我们可能需要机器人根据条件自动同意加群请求，从而不再需要管理员手动操作。

新建 `awesome/plugins/group_admin.py`，编写代码如下：

```python
from nonebot import on_request, RequestSession


# 将函数注册为群请求处理器
@on_request('group')
async def _(session: RequestSession):
    # 判断验证信息是否符合要求
    if session.event.comment == '暗号':
        # 验证信息正确，同意入群
        await session.approve()
        return
    # 验证信息错误，拒绝入群
    await session.reject('请说暗号')
```

这里首先 `on_request` 装饰器将函数注册为一个请求处理器，`group` 参数表示只处理群请求，这里各请求对应的参数值可以参考 [CQHTTP 插件的事件上报](https://cqhttp.cc/docs/#/Post?id=%E5%8A%A0%E5%A5%BD%E5%8F%8B%E8%AF%B7%E6%B1%82) 的 `request_type` 字段，目前有 `group` 和 `friend` 两种。

接着判断 `session.event.comment` 是否是正确的暗号，这里 `session.event` 是一个 `aiocqhttp.Event` 对象，即 CQHTTP 上报来的事件的简单包装，`comment` 属性用于获取加群或加好友事件中的验证信息。

最后 `session.approve()` 和 `session.reject()` 分别用于同意和拒绝加群请求，如果都不调用，则忽略请求（其它管理员仍然可以处理请求）。

## 欢迎新成员

新成员入群之后，为了活跃气氛，我们可能希望机器人发一段欢迎消息。只需下面的代码即可实现：

```python
from nonebot import on_notice, NoticeSession


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    await session.send('欢迎新朋友～')
```

:::warning 注意
这里最好预先判断一下是不是你想发送的群（通过 `session.event.group_id`），否则机器人所在的任何群有新成员进入它都会欢迎。
:::

总的来说这些 `on_*` 装饰器用起来都是差不多的，这里的 `group_increase` 表示群成员增加，其它的通知类型可以参考 [CQHTTP 插件的事件上报](https://cqhttp.cc/docs/#/Post?id=%E7%BE%A4%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0) 的 `notice_type`。
