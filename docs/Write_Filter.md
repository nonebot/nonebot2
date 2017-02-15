# 编写过滤器

`filters` 目录中所有不以 `_` 开头的 `.py` 文件会被加载进程序，一般把过滤器放在这个目录里。对于临时不需要的过滤器，可以通过在文件名前加 `_` 来屏蔽掉。

## 写法

编写过滤器比较简单，只需要调用 `filter.py` 中的 `add_filter` 函数或 `as_filter` 装饰器，传入过滤器函数和优先级，即可。

比如我们需要做一个消息拦截器，当匹配到消息中有不文明词汇，就发送一条警告，并拦截消息不让后续过滤器和命令处理，代码可能如下：

```python
from filter import add_filter, as_filter
from commands import core


def _interceptor(ctx_msg):
    if 'xxx' in ctx_msg.get('content', ''):
        core.echo('请不要说脏话', ctx_msg)
        return False
    return True

add_filter(_interceptor, priority=100)

# 或下面这样

@as_filter(priority=100)
def _interceptor(ctx_msg):
    if 'xxx' in ctx_msg.get('content', ''):
        core.echo('请不要说脏话', ctx_msg)
        return False
    return True
```

一般建议优先级设置为 0～100 之间。

过滤器函数返回 True 表示让消息继续传递，返回 False 表示拦截消息。由于很多情况下可能不需要拦截，因此为了方便起见，将不返回值的情况（返回 None）作为不拦截处理，因此只要返回结果 is not False 就表示不拦截。

## 现有的几个重要过滤器

| 文件                                    | 优先级  | 作用                                       | 备注                                     |
| ------------------------------------- | ---- | ---------------------------------------- | -------------------------------------- |
| message_logger_1000.py                | 1000 | 把收到的消息打印在标准输出                            | 不建议添加比它优先级更高的过滤器                       |
| intercept_some_message_formats_100.py | 100  | 拦截某些不支持的消息类型，对于文本消息，会把 `content` 字段复制到 `text` 字段 | 如果要自己编写插件，这里可以按需修改                     |
| speech_recognition_90.py              | 90   | 对语音消息进行语音识别（仅私聊消息），并把识别出的文字放到 `text` 字段，并标记 `from_voice` 字段为 True | 此过滤器只对 Mojo-Weixin 消息源生效，如果不需要可以删掉     |
| split_at_xiaokai_50.py                | 50   | 分离群组和讨论组中消息开头的 `@CCZU 小开`，并更新 `text` 字段为剩余部分 | 也就是说通过此过滤器的消息，就是确定用户的意图就是和这个 bot 说话的消息 |
| command_dispatcher_0.py               | 0    | 识别消息中的命令，并进行相应的调用                        |                                        |