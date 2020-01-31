# CQHTTP 事件和 API

到目前为止，我们都在使用 NoneBot 显式提供的接口，但实际上 CQHTTP 插件还提供了更多的事件数据和 API，可能利用这些它们实现更加自由的逻辑。

## 事件数据

在 [发生了什么？](./whats-happened.md) 中我们提到，收到 酷Q 事件后，CQHTTP 通过反向 WebSocket 给 NoneBot 发送事件数据。这些数据被 NoneBot 放在了 `session.ctx` 中，是一个字典，你可以通过断点调试或打印等方式查看它的内容，其中的字段名和含义见 CQHTTP 的 [事件列表](https://cqhttp.cc/docs/#/Post?id=事件列表) 中的「上报数据」。

## API 调用

前面我们已经多次调用 `CommandSession` 类的 `send()` 方法，而这个方法只能回复给消息的发送方，不能手动指定发送者，因此当我们需要实现将收到的消息经过处理后转发给另一个接收方这样的功能时，这个方法就用不了了。

幸运的是，`NoneBot` 类是继承自 [python-aiocqhttp] 的 `CQHttp` 类的，而这个类实现了 `__getattr__()` 魔术方法，由此提供了直接通过 bot 对象调用 CQHTTP 的 API 的能力。

[python-aiocqhttp]: https://github.com/cqmoe/python-aiocqhttp

::: tip 提示
如果你在使用 HTTP 通信，要调用 CQHTTP API 要在 `config.py` 中添加：

```python
API_ROOT = 'http://127.0.0.1:5700'  # 这里 IP 和端口应与 CQHTTP 配置中的 `host` 和 `port` 对应
```
:::

要获取 bot 对象，可以通过如下两种方式：

```python
bot = session.bot
bot = nonebot.get_bot()
```

Bot 对象的使用方式如下：

```python
await bot.send_private_msg(user_id=12345678, message='你好～')
```

这里，`send_private_msg` 实际上对应 CQHTTP 的 [`/send_private_msg` 接口](https://cqhttp.cc/docs/#/API?id=send_private_msg-%E5%8F%91%E9%80%81%E7%A7%81%E8%81%8A%E6%B6%88%E6%81%AF)，其它接口同理。

通过这种方式调用 API 时，需要注意下面几点：

- **所有参数必须为命名参数（keyword argument）**，否则无法正确调用
- 这种调用**全都是异步调用**，因此需要适当 `await`
- **调用失败时（没有权限、对方不是好友、无 API 连接等）可能抛出 `nonebot.CQHttpError` 异常**，注意捕获，例如：
  ```python
  try:
      info = await bot.get_group_list()
  except CQHttpError:
      pass
  ```
- **当多个机器人使用同一个 NoneBot 后端时**，可能需要加上参数 `self_id=<机器人QQ号>`，例如：
  ```python
  info = await bot.get_group_list(self_id=ctx['self_id'])
  ```

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
