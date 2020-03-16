# 接入图灵机器人

::: danger 重要
本章内容可能已经过时，即将更新。
:::

到目前为止我们已经编写了一个相对完整的天气查询插件，包括命令和自然语言处理器，除此之外，使用同样的方法，还可以编写更多功能的插件。

但这样的套路存在一个问题，如果我们不是专业的 NLP 工程师，开放话题的智能聊天仍然是我们无法自己完成的事情，用户只能通过特定插件所支持的句式来使用相应的功能，当用户试图使用我们暂时没有开发的功能时，我们的机器人显得似乎有些无能为力。

不过还是有解决方案的，市面上有一些提供智能聊天机器人接口的厂商，本章我们以 [图灵机器人](http://www.tuling123.com/) 为例，因为它的使用比较广泛，接入也比较简单，不过缺点是免费调用次数比较少。

::: tip 提示
本章的完整代码可以在 [awesome-bot-4](https://github.com/richardchien/nonebot/tree/master/docs/guide/code/awesome-bot-4) 查看。
:::

## 注册图灵机器人账号

首先前往 [图灵机器人官网](http://www.tuling123.com/) 注册账号，然后在「机器人管理」页根据它的提示创建机器人，可以设置机器人名字、属性、技能、语料库等。

::: warning 注意
图灵机器人的免费套餐现在需要实名认证后才可使用。
:::

注册完成后先放一边，或者如果有兴趣的话，在网页上的聊天窗口和它聊几句看看效果。

## 编写图灵机器人插件

新建 `awesome/plugins/tuling.py` 文件，编写如下内容：

```python
import json
from typing import Optional

import aiohttp
from aiocqhttp.message import escape
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression

# 定义无法获取图灵回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)


# 注册一个仅内部使用的命令，不需要 aliases
@on_command('tuling')
async def tuling(session: CommandSession):
    # 获取可选参数，这里如果没有 message 参数，命令不会被中断，message 变量会是 None
    message = session.state.get('message')

    # 通过封装的函数获取图灵机器人的回复
    reply = await call_tuling_api(session, message)
    if reply:
        # 如果调用图灵机器人成功，得到了回复，则转义之后发送给用户
        # 转义会把消息中的某些特殊字符做转换，以避免 酷Q 将它们理解为 CQ 码
        await session.send(escape(reply))
    else:
        # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取图灵回复时的「表达」
        # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))


@on_natural_language
async def _(session: NLPSession):
    # 以置信度 60.0 返回 tuling 命令
    # 确保任何消息都在且仅在其它自然语言处理器无法理解的时候使用 tuling 命令
    return IntentCommand(60.0, 'tuling', args={'message': session.msg_text})


async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
    # 调用图灵机器人的 API 获取回复

    if not text:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    # 构造请求数据
    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': session.bot.config.TULING_API_KEY,
            'userId': context_id(session.ctx, use_hash=True)
        }
    }

    group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
    if group_unique_id:
        payload['userInfo']['groupId'] = group_unique_id

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                resp_payload = json.loads(await response.text())
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            # 返回文本类型的回复
                            return result['values']['text']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None
```

上面这段代码比较长，而且有一些新出现的函数和概念，我们后面会慢慢地详解，不过现在先在 `config.py` 中添加一项：

```python
TULING_API_KEY = ''
```

`TULING_API_KEY` 的值填图灵机器人的「机器人设置」页面最下方提供的 API Key。

配置完成后来运行 NoneBot，尝试给机器人随便发送一条消息，看看它是不是正确地获取了图灵机器人的回复。

## 理解自然语言处理器

我们先来理解代码中最简单的部分：

```python {3}
@on_natural_language
async def _(session: NLPSession):
    return IntentCommand(60.0, 'tuling', args={'message': session.msg_text})
```

根据我们前面一章中已经知道的用法，这里就是直接返回置信度为 60.0 的 `tuling` 命令。之所以返回置信度 60.0，是因为自然语言处理器所返回的结果最终会按置信度排序，取置信度最高且大于等于 60.0 的结果来执行。把置信度设为 60.0 可以保证一条消息无法被其它自然语言处理器理解的时候 fallback 到 `tuling` 命令。

## 理解图灵机器人接口的 HTTP 调用

图灵机器人接口的调用也非常简单，虽然看起来代码挺多，但新的概念并不多。

```python {7-23,26-37}
async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
    if not text:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    # 构造请求数据
    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': session.bot.config.TULING_API_KEY,
            'userId': context_id(session.ctx, use_hash=True)
        }
    }

    group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
    if group_unique_id:
        payload['userInfo']['groupId'] = group_unique_id

    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                resp_payload = json.loads(await response.text())
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            # 返回文本类型的回复
                            return result['values']['text']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None
```

这里的代码主要需要参考 [图灵机器人的官方 API 文档](https://www.kancloud.cn/turing/www-tuling123-com/718227)。

### 构造请求数据

第一段高亮部分是根据图灵机器人的文档构造请求数据，其中有几个需要注意的地方：第 16、17 和 21 行。

第 16 行通过 `session.bot.config` 访问了 NoneBot 的配置对象，`session.bot` 就是当前正在运行的 NoneBot 对象，你在其它任何地方都可以这么用（前提是已经调用过 `nonebot.init()`）。

第 17 和 21 行调用了 `context_id()` 函数，这是 `nonebot.helpers` 模块中提供的一个函数，用于计算 Context 的独特 ID，有三种模式可以选择（通过 `mode` 参数传入）：`default`、`group`、`user`，默认 `default`，它们的效果如下表：

| 模式 | 效果 |
| ------------ | --- |
| `default` | 每个用户在每个群、讨论组和私聊都对应不同的 ID |
| `group` | 每个群或讨论组内的成员共用一个 ID，私聊仍按用户区分 |
| `user` | 每个用户对应不同的 ID，但不区分用户是在私聊还是群或讨论组 |

`context_id()` 函数还提供 `use_hash` 参数可选地将计算出的 ID 进行 MD5 哈希，以适应某些应用场景。

### 发送请求

第二段高亮的代码是使用 [aiohttp](https://aiohttp.readthedocs.io/en/stable/) 发送 HTTP POST 请求给图灵机器人，并获取它的回复，这段其实没有什么跟 NoneBot 有关的东西，请参考前面给出的图灵机器人的官方 API 文档，里面详细解释了每个返回字段的含义。

## 理解命令处理器

命令处理器这部分虽然代码比较少，但引入了不少新的概念。

```python {1,3-8,13,16,18}
from aiocqhttp.message import escape

EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～'
)


@on_command('tuling')
async def tuling(session: CommandSession):
    message = session.state.get('message')
    reply = await call_tuling_api(session, message)
    if reply:
        await session.send(escape(reply))
    else:
        await session.send(render_expression(EXPR_DONT_UNDERSTAND))
```

### 可选参数

首先看第 13 行，`session.state.get()` 可用于获取命令的可选参数，也就是说，从 `session.state` 中尝试获取一个参数（还记得 `IntentCommand` 的 `args` 参数内容会全部进入 `CommandSession` 的 `state` 吗），如果没有，返回 `None`，但并不会中断命令的执行。其实这就是 `dict.get()` 方法。

### 消息转义

再看第 16 行，在调用 `session.send()` 之前先对 `reply` 调用了 `escape()`，这个 `escape()` 函数是 `aiocqhttp.message` 模块提供的，用于将字符串中的某些特殊字符进行转义。具体来说，这些特殊字符是 酷Q 看作是 CQ 码的一部分的那些字符，包括 `&`、`[`、`]`、`,`。

CQ 码是 酷Q 用来表示非文本消息的一种表示方法，形如 `[CQ:image,file=ABC.jpg]`。具体的格式规则，请参考 酷Q 文档的 [CQ 码](https://d.cqp.me/Pro/CQ%E7%A0%81) 和 CoolQ HTTP API 插件文档的 [CQ 码](https://cqhttp.cc/docs/#/CQCode)。

### 发送 Expression

第 18 行使用了 NoneBot 中 Expression 这个概念，或称为「表达」。

Expression 可以是一个 `str`、元素类型是 `str` 的序列（一般为 `list` 或 `tuple`）或返回类型为 `str` 的 `Callable`。

`render_expression()` 函数用于将 Expression 渲染成字符串。它首先判断 Expression 的类型，如果 Expression 是一个序列，则首先随机取其中的一个元素，如果是一个 `Callable`，则调用函数获取返回值。拿到最终的 `str` 类型的 Expression 之后，对它调用 `str.format()` 方法，格式化参数传入 `render_expression()` 函数的命名参数（`**kwargs`），最后返回格式化后的结果。特别地，如果 Expression 是个 `Callable`，在调用它获取返回值的时候，也会传入 `**kwargs`，以便函数根据参数来构造字符串。

你可以通过使用序列或 `Callable` 类型的 Expression 来让机器人的回复显得更加自然，甚至，可以利用更高级的人工智能技术来生成对话。
