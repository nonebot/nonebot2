# Mirai-API-HTTP 协议使用指南

::: warning

Mirai-API-HTTP 的适配现在仍然处于早期阶段, 可能没有进行过充分的测试

在生产环境中请谨慎使用

:::

::: tip

为了你的使用之旅更加顺畅, 我们建议您在配置之前具有以下的前置知识

- 对服务端/客户端(C/S)模型的基本了解
- 对 Web 服务配置基础的认知
- 对`YAML`语法的一点点了解

:::

::: danger

Mirai-API-HTTP 的适配器以 [AGPLv3 许可](https://opensource.org/licenses/AGPL-3.0) 单独开源

这意味着在使用该适配器时需要 **以该许可开源您的完整程序代码**

:::

**为了便捷起见, 以下内容均以缩写 `MAH` 代替 `mirai-api-http`**

## 安装 NoneBot Mirai 适配器

```bash
pip install nonebot-adapter-mirai
```

## 配置 MAH 客户端

正如你可能刚刚在[CQHTTP 协议使用指南](./cqhttp-guide.md)中所读到的:

> 单纯运行 NoneBot 实例并不会产生任何效果，因为此刻 QQ 这边还不知道 NoneBot 的存在，也就无法把消息发送给它，因此现在需要使用一个无头 QQ 来把消息等事件上报给 NoneBot。

这次, 我们将采用在实现上有别于 OneBot（CQHTTP）协议的另外一种无头 QQ API 协议, 即 MAH

为了配置 MAH 端, 我们现在需要移步到[MAH 的项目地址](https://github.com/project-mirai/mirai-api-http), 来看看它是如何配置的

根据[项目提供的 README](https://github.com/project-mirai/mirai-api-http/blob/056beedba31d6ad06426997a1d3fde861a7f8ba3/README.md),配置 MAH 大概需要以下几步

1. 下载并安装 Java 运行环境, 你可以有以下几种选择:

   - [由 Oracle 提供的 Java 运行环境](https://java.com/zh-CN/download/manual.jsp) **在没有特殊需求的情况下推荐**
   - [由 Zulu 编译的 OpenJRE 环境](https://www.azul.com/downloads/zulu-community/?version=java-8-lts&architecture=x86-64-bit&package=jre)

2. 下载[Mirai Console Loader](https://github.com/iTXTech/mirai-console-loader)

   - 请按照文档 README 中的步骤下载并安装

3. 安装 MAH:

   - 在 Mirai Console Loader 目录下执行该指令

   - ```shell
     ./mcl --update-package net.mamoe:mirai-api-http --channel stable --type plugin
     ```

     注意: 该指令的前缀`./mcl`可能根据操作系统以及使用 java 环境的不同而变化

4. 修改配置文件

   ::: warning
   
   由于NoneBot2的架构设计等原因, 部分功能的支持可能需要推迟到MAH 2.0正式发布后再完成
   
   :::

   ::: tip

   在此之前, 你可能需要了解我们为 MAH 设计的两种通信方式

   - 正向 Websocket
     - NoneBot 作为纯粹的客户端,通过 websocket 监听事件下发
     - 优势
       1. 网络配置简单, 特别是在使用 Docker 等网络隔离的容器时
       2. 在初步测试中连接性较好
     - 劣势
       1. 与 NoneBot 本身的架构不同, 可能稳定性较差
       2. 需要在注册 adapter 时显式指定 qq, 对于需要开源的程序来讲不利
   - POST 消息上报
     - NoneBot 在接受消息上报时作为服务端, 发送消息时作为客户端
     - 优势
       1. 与 NoneBot 本身架构相符, 性能和稳定性较强
       2. 无需在任何地方指定 QQ, 即插即用
     - 劣势
       1. 由于同时作为客户端和服务端, 配置较为复杂
       2. 在测试中网络连接性较差 (未确认原因)

   :::

   - 这是当使用正向 Websocket 时的配置举例
     
     ::: warning
     
     在默认情况下, NoneBot和MAH会同时监听8080端口, 这会导致端口冲突的错误
     请确保二者配置不在同一端口下
     
     :::

     - MAH 的`setting.yml`文件

     - ```yaml
       # 省略了部分无需修改的部分

       host: "0.0.0.0" # 监听地址
       port: 8080 # 监听端口
       authKey: 1234567890 # 访问密钥, 最少八位
       enableWebsocket: true # 必须为true
       ```

     - `.env`文件

     - ```shell
       PORT=2333
       
       MIRAI_AUTH_KEY=1234567890
       MIRAI_HOST=127.0.0.1 # 当MAH运行在本机时
       MIRAI_PORT=8080 # MAH的监听端口
       PORT=2333 # 防止与MAH接口冲突
       ```

     - `bot.py`文件

     - ```python
       import nonebot
       from nonebot.adapters.mirai import WebsocketBot

       nonebot.init()
       nonebot.get_driver().register_adapter('mirai-ws', WebsocketBot, qq=12345678) # qq参数需要填在mah中登录的qq
       nonebot.load_builtin_plugins() # 加载 nonebot 内置插件
       nonebot.run()
       ```

   - 这是当使用 POST 消息上报时的配置文件

     - MAH 的`setting.yml`文件

     - ```yaml
       # 省略了部分无需修改的部分

       host: '0.0.0.0' # 监听地址
       port: 8080 # 监听端口
       authKey: 1234567890 # 访问密钥, 最少八位

       ## 消息上报
       report:
         enable: true # 必须为true
         groupMessage:
           report: true  # 群消息上报
         friendMessage:
           report: true # 好友消息上报
         tempMessage:
           report: true # 临时会话上报
         eventMessage:
           report: true # 事件上报
         destinations:
         	- 'http://127.0.0.1:2333/mirai/http' #上报地址, 请按照实际情况修改
         # 上报时的额外Header
         extraHeaders: {}
       ```

     - `.env`文件

     - ```shell
       HOST=127.0.0.1 # 当MAH运行在本机时
       PORT=2333 # 防止与MAH接口冲突

       MIRAI_AUTH_KEY=1234567890
       MIRAI_HOST=127.0.0.1 # 当MAH运行在本机时
       MIRAI_PORT=8080 # MAH的监听端口
       ```

     - `bot.py`文件

     - ```python
       import nonebot
       from nonebot.adapters.mirai import Bot

       nonebot.init()
       nonebot.get_driver().register_adapter('mirai', Bot)
       nonebot.load_builtin_plugins() # 加载 nonebot 内置插件
       nonebot.run()
       ```

## 历史性的第一次对话

现在, 先启动 NoneBot, 再启动 MAH

如果你的配置文件一切正常, 你将在控制台看到类似于下列的日志

```log
02-01 18:25:12 [INFO] nonebot | NoneBot is initializing...
02-01 18:25:12 [INFO] nonebot | Current Env: prod
02-01 18:25:12 [DEBUG] nonebot | Loaded Config: {'driver': 'nonebot.drivers.fastapi', 'host': IPv4Address('127.0.0.1'), 'port': 8080, 'debug': True, 'api_root': {}, 'api_timeout': 30.0, 'access_token': None, 'secret': None, 'superusers': set(), 'nickname': set(), 'command_start': {'/'}, 'command_sep': {'.'}, 'session_expire_timeout': datetime.timedelta(seconds=120), 'mirai_port': 8080, 'environment': 'prod', 'mirai_auth_key': 12345678, 'mirai_host': '127.0.0.1'}
02-01 18:25:12 [DEBUG] nonebot | Succeeded to load adapter "mirai"
02-01 18:25:12 [INFO] nonebot | Succeeded to import "nonebot.plugins.echo"
02-01 18:25:12 [INFO] nonebot | Running NoneBot...
02-01 18:25:12 [DEBUG] nonebot | Loaded adapters: mirai
02-01 18:25:12 [INFO] uvicorn | Started server process [183155]
02-01 18:25:12 [INFO] uvicorn | Waiting for application startup.
02-01 18:25:12 [INFO] uvicorn | Application startup complete.
02-01 18:25:12 [INFO] uvicorn | Uvicorn running on http://127.0.0.1:2333 (Press CTRL+C to quit)
02-01 18:25:14 [INFO] uvicorn | 127.0.0.1:37794 - "POST /mirai/http HTTP/1.1" 204
02-01 18:25:14 [DEBUG] nonebot | MIRAI | received message {'type': 'BotOnlineEvent', 'qq': 1234567}
02-01 18:25:14 [INFO] nonebot | MIRAI 1234567 | [BotOnlineEvent]: {'self_id': 1234567, 'type': 'BotOnlineEvent', 'qq': 1234567}
02-01 18:25:14 [DEBUG] nonebot | Checking for matchers in priority 1...
```

恭喜你, 你的配置已经成功!

现在, 我们可以写一个简单的插件来测试一下

```python
from nonebot.plugin import on_keyword, on_command
from nonebot.rule import to_me
from nonebot.adapters.mirai import Bot, MessageEvent

message_test = on_keyword({'reply'}, rule=to_me())


@message_test.handle()
async def _message(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, text, at_sender=True)


command_test = on_command('miecho')


@command_test.handle()
async def _echo(bot: Bot, event: MessageEvent):
    text = event.get_plaintext()
    await bot.send(event, text, at_sender=True)
```

它具有两种行为

- 在指定机器人，即私聊、群聊内@机器人、群聊内称呼机器人昵称的情况下 (即 [Rule: to_me](../api/rule.md#to-me)), 如果消息内包含 `reply` 字段, 则该消息会被机器人重复一次

- 在执行指令`miecho xxx`时, 机器人会发送回参数`xxx`

至此, 你已经初步掌握了如何使用 Mirai Adapter
