# 编写消息源适配器

消息源适配器是用来在消息源和本程序之间进行数据格式的一类程序，相当于一个驱动程序，通过不同的驱动程序，本程序便可以接入多种聊天平台。后文中简称为「适配器」。

通常情况下一个消息源需要能够支持通过 HTTP 来上报消息和调用操作，才能够便于开发适配器，不过实际上如果有需求，你也可以直接在适配器中对程序的 HTTP 服务端进行请求，例如某些直接以模块形式给出的消息平台客户端，通过回调函数来通知事件，此时你可以在这个事件的回调函数中，手动请求本程序的上报地址并发送相应的数据。但这不在此文的讨论范围之内，这属于另一类适配器，与本程序无直接关联。

我们这里讨论在本程序接收到 HTTP 上报消息之后、及内部逻辑中产生了对适配器的接口调用之后，需要将上报数据转换成本程序能够识别的数据格式，或将本程序中发出的接口调用转换成消息源客户端能够识别的接口调用，例如我们调用 `adapter.send_private_message`，相对应的适配器将会在内部通过 HTTP 请求这个消息源客户端的用来发送私聊消息的接口。

为了形象的理解，你可能需要去参考已有的那些适配器的代码。

## 写法

其实写起来非常简单，就和那些 Web 框架的 Handler 一样，继承一个基类，实现某几个固定的函数接口即可，这里需要继承的是 `msg_src_adapter.py` 中的 `Adapter` 类，此基类中已经实现了一些通用的、或默认的逻辑，对于像 `unitize_context`（上报数据统一化）、`send_private_message`（发送私聊消息）、`get_sender_group_role`（获取发送者在群组中的身份）等等接口，通常需要在子类中进行具体的、差异化的操作。

我们直接以 Mojo-Webqq 的适配器 `msg_src_adapters/mojo_webqq.py` 为例，代码如下（可能不是最新）：

```python
import requests

from msg_src_adapter import Adapter, as_adapter, ConfigurationError


@as_adapter(via='mojo_webqq')
class MojoWebqqAdapter(Adapter):
    def __init__(self, config: dict):
        super().__init__(config)
        if not config.get('api_url'):
            raise ConfigurationError
        self.api_url = config['api_url']

    def unitize_context(self, ctx_msg: dict):
        new_ctx = {'raw_ctx': ctx_msg, 'post_type': ctx_msg['post_type'], 'via': ctx_msg['via'],
                   'login_id': ctx_msg['login_id']}
        if new_ctx['post_type'] != 'receive_message':
            return new_ctx
        new_ctx['post_type'] = 'message'  # Just handle 'receive_message', and make 'post_type' 'message'
        new_ctx['time'] = ctx_msg['time']
        new_ctx['msg_id'] = str(ctx_msg['id'])
        new_ctx['msg_type'] = ctx_msg['type'].split('_')[0]
        new_ctx['msg_type'] = 'private' if new_ctx['msg_type'] == 'friend' else new_ctx['msg_type']
        new_ctx['format'] = 'text'
        new_ctx['content'] = ctx_msg['content']

        new_ctx['receiver'] = ctx_msg.get('receiver', '')
        new_ctx['receiver_name'] = (requests.get(self.api_url + '/get_user_info').json() or {}).get('name', '')
        new_ctx['receiver_id'] = str(ctx_msg.get('receiver_uid', ''))
        new_ctx['receiver_tid'] = str(ctx_msg.get('receiver_id', ''))

        new_ctx['sender'] = ctx_msg.get('sender', '')
        friend = list(filter(
            lambda f: f.get('uid') == ctx_msg['sender_uid'],
            requests.get(self.api_url + '/get_friend_info').json() or []
        ))
        new_ctx['sender_name'] = friend[0].get('name', '') if friend else ''
        new_ctx['sender_id'] = str(ctx_msg.get('sender_uid', ''))
        new_ctx['sender_tid'] = str(ctx_msg.get('sender_id', ''))

        if new_ctx['msg_type'] == 'group':
            new_ctx['group'] = ctx_msg.get('group', '')
            new_ctx['group_id'] = str(ctx_msg.get('group_uid', ''))
            new_ctx['group_tid'] = str(ctx_msg.get('group_id', ''))

        if new_ctx['msg_type'] == 'discuss':
            new_ctx['discuss'] = ctx_msg.get('discuss', '')
            new_ctx['discuss_tid'] = str(ctx_msg.get('discuss_id', ''))

        return new_ctx

    def get_login_info(self, ctx_msg: dict):
        json = requests.get(self.api_url + '/get_user_info').json()
        if json:
            json['user_tid'] = json.get('id')
            json['user_id'] = json.get('uid')
            json['nickname'] = json.get('name')
        return json

    def _get_group_info(self):
        return requests.get(self.api_url + '/get_group_info').json()

    def get_sender_group_role(self, ctx_msg: dict):
        groups = list(filter(
            lambda g: str(g.get('id')) == ctx_msg['raw_ctx'].get('group_id'),
            self._get_group_info() or []
        ))
        if len(groups) <= 0 or 'member' not in groups[0]:
            # This is strange, not likely happens
            return 'member'
        members = list(filter(
            lambda m: str(m.get('id')) == ctx_msg['raw_ctx'].get('sender_id'),
            groups[0].get('member')
        ))
        if len(members) <= 0:
            # This is strange, not likely happens
            return 'member'
        return members[0].get('role', 'member')

    def send_private_message(self, target: dict, content: str):
        params = None
        if target.get('user_id'):
            params = {'uid': target.get('user_id')}
        elif target.get('user_tid'):
            params = {'id': target.get('user_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_friend_message', params=params)

    def send_group_message(self, target: dict, content: str):
        params = None
        if target.get('group_id'):
            params = {'uid': target.get('group_id')}
        elif target.get('group_tid'):
            params = {'id': target.get('group_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_group_message', params=params)

    def send_discuss_message(self, target: dict, content: str):
        params = None
        if target.get('discuss_tid'):
            params = {'id': target.get('discuss_tid')}

        if params:
            params['content'] = content
            requests.get(self.api_url + '/send_discuss_message', params=params)
```

代码逻辑上很简单，首先调用 `@as_adapter(via='mojo_webqq')` 把类注册为适配器，`via` 就是配置文件里定义消息源时候要填的那个 `via`，同时也是上报消息路径里的那个 `via`。初始化函数里面要求配置文件中的消息源定义里必须有 `api_url`。

`unitize_context` 函数是用来统一上报消息上下文的，这个上下文（Context）是一个字典类型，在整个程序中起核心作用，此函数需要将消息源发送来的数据转换成本程序能够理解的格式，也就是对字段进行翻译，需要翻译成一个统一的格式，这个格式见 [统一消息上下文](https://cczu-dev.github.io/xiaokai-bot/#/Context)。

其它的函数就是对调用操作的翻译，例如把 `send_group_message` 的调用翻译成对 `self.api_url + '/send_group_message'` 的 HTTP 请求。

### 消息发送目标的定义

由于发送消息使用一个统一接口，插件中调用时并不知道是哪个适配器接收到调用，所以发送消息的目标同样是需要统一的，也即 `send_message` 函数的 `target` 参数，此参数应当和消息上下文兼容，也就是说，当调用发送消息的接口时，直接把消息上下文传入，就应当能正确发送到此消息上下文所在的语境（比如和某个用户的私聊消息或某个群组中）。

它主要应当接受如下字段：

| 字段名                        | 说明                                       |
| -------------------------- | ---------------------------------------- |
| `user_id`／`user_tid`       | 消息要发送的对象（私聊用户）的 ID                       |
| `group_id`／`group_tid`     | 要发送的群组 ID                                |
| `discuss_id`／`discuss_tid` | 要发送的讨论组 ID                               |
| `content`                  | 消息内容，通常是 str 类型，目前所有适配器只支持发送文本消息（str 类型） |

以上所有 `xxx_id` 和 `xxx_tid` 分别表示固定 ID 和临时 ID，这和消息上下文中的定义一样，即，固定 ID（`xxx_id`）表示重新登录不会变的 ID，通常即为该消息平台的账号（微信 ID、QQ 号），临时 ID（`xxx_tid`）表示在消息源的此次登录中不会变的 ID，但下次登录可能同一个用户的 ID 和上次不同，对于某些平台（如微信），可能有时完全无法获取到固定 ID，此时临时 ID 将成为发送消息时的重要依据。

### 其它

对于需要对群组中用户身份进行区分的情况，例如某些命令只允许群组管理员运行，要实现 `get_sender_group_role` 函数，此函数返回的成员身份应为 `member`、`admin`、`owner` 三者之一。