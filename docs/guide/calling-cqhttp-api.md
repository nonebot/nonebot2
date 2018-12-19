# 主动调用 CQHTTP 接口

到目前为止，我们都在调用 `CommandSession` 类的 `send()` 方法，而这个方法只能回复给消息的发送方，不能手动指定发送者，因此当我们需要实现将收到的消息经过处理后转发给另一个接收方这样的功能时，这个方法就用不了了。

幸运的是，`NoneBot` 类是继承自 [python-aiocqhttp] 的 `CQHttp` 类的，而这个类实现了一个 `__getattr__()` 方法，由此提供了直接通过 bot 对象调用 CQHTTP 的 API 的能力，如下：

[python-aiocqhttp]: https://github.com/richardchien/python-aiocqhttp

```python
await bot.send_private_msg(user_id=12345678, message='你好～')
```

这里，`send_private_msg` 实际上对应 CQHTTP 的 [`/send_private_msg` 接口](https://cqhttp.cc/docs/#/API?id=send_private_msg-%E5%8F%91%E9%80%81%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)，其它接口同理。

通过这种方式调用 API 时，需要注意两点：

1. **所有参数必须为命名参数（keyword argument）**，否则无法正确调用
2. 这种调用全都是异步调用，因此需要适当 `await`
2. **调用失败时（没有权限、对方不是好友、无 API 连接等）可能抛出 `none.CQHttpError` 异常**，注意捕获

另外，在需要动态性的场合，除了使用 `getattr()` 方法外，还可以直接调用 `bot.call_action()` 方法，传入 `action` 和 `params` 即可，例如上例中，`action` 为 `'send_private_msg'`，`params` 为 `{'user_id': 12345678, 'message': '你好～'}`。

下面举出一些主动发送消息和调用 API 的例子：

```python
await bot.send_private_msg(user_id=12345678, message='你好～')
await bot.send_group_msg(group_id=123456, message='大家好～')

ctx = session.ctx.copy()
del ctx['message']
await bot.send_msg(**ctx, message='喵～')

await bot.delete_msg(**session.ctx)
await bot.set_group_card(**session.ctx, card='新人请改群名片')
self_info = await bot.get_login_info()
group_member_info = await bot.get_group_member_info(group_id=123456, user_id=12345678, no_cache=True)
```

其它更多接口请自行参考 CQHTTP 的 [API 列表](https://cqhttp.cc/docs/#/API?id=api-列表)。
