# 编写过滤器

## 写法

编写过滤器比较简单，只需要调用 `filter.py` 中的 `add_filter` 函数，传入过滤器函数和优先级，即可。

比如我们需要做一个消息拦截器，当匹配到消息中有不文明词汇，就发送一条警告，并拦截消息不让后续过滤器和命令处理，代码可能如下：

```python
from filter import add_filter
from commands import core


def _interceptor(ctx_msg):
    if 'xxx' in ctx_msg.get('content', ''):
        core.echo('请不要说脏话', ctx_msg)
        return False
    return True


add_filter(_interceptor, 100)
```

一般建议优先级设置为 0～100 之间。

过滤器函数返回 True 表示让消息继续传递，返回 False 表示拦截消息。由于很多情况下可能不需要拦截，因此为了方便起见，将不返回值的情况（返回 None）作为不拦截处理，因此只要返回结果 is not False 就表示不拦截。

## 现有的几个重要过滤器

### 消息日志过滤器

此过滤器用于把收到的消息打印在标准输出，在 `filters/message_logger_1000.py` 中定义，优先级 1000，一般不建议添加其它优先级比它高的过滤器，以确保日志不受任何干扰。

### 分离@开头过滤器

用于分离群组和讨论组中消息开头的 `@CCZU 小开`，优先级 50，在 `filters/split_at_xiaokai_50.py` 中定义。通过此过滤器的消息的 `content` 字段会被更新为分离掉开头的剩余部分，也就是说通过此过滤器的消息，就是确定用户的意图就是和这个 bot 说话的消息。

### 命令分发过滤器

用于处理消息中的命令，优先级 0，在 `filters/command_dispatcher_0.py` 中定义。
