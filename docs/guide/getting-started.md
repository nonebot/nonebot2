# 开始使用

一切都安装成功后，你就已经做好了进行简单配置以运行一个最小的 NoneBot 实例的准备。

## 最小实例

如果你已经按照推荐方式安装了 `nb-cli`，使用脚手架创建一个空项目：

```bash
nb create
```

根据脚手架引导，将在当前目录下创建一个项目目录，项目目录内包含 `bot.py`。

如果未安装 `nb-cli`，使用你最熟悉的编辑器或 IDE，创建一个名为 `bot.py` 的文件，内容如下：

```python{3,4,7}
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()

if __name__ == "__main__":
    nonebot.run()
```

## 解读

在上方 `bot.py` 中，这几行高亮代码将依次：

1. 使用默认配置初始化 NoneBot
2. 加载 NoneBot 内置的插件
3. 在地址 `127.0.0.1:8080` 运行 NoneBot

在命令行使用如下命令即可运行这个 NoneBot 实例：

```bash
# nb-cli
nb run
# 其他
python bot.py
```

运行后会产生如下日志：

```plain
09-14 21:02:00 [INFO] nonebot | Succeeded to import "nonebot.plugins.base"
09-14 21:02:00 [INFO] nonebot | Running NoneBot...
09-14 21:02:00 [INFO] uvicorn | Started server process [1234]
09-14 21:02:00 [INFO] uvicorn | Waiting for application startup.
09-14 21:02:00 [INFO] uvicorn | Application startup complete.
09-14 21:02:00 [INFO] uvicorn | Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

## 配置 QQ 协议端

单纯运行 NoneBot 实例并不会产生任何效果，因为此刻 QQ 这边还不知道 NoneBot 的存在，也就无法把消息发送给它，因此现在需要使用一个无头 QQ 来把消息等事件上报给 NoneBot。

目前支持的协议有:

- [OneBot(CQHTTP)](https://github.com/howmanybots/onebot/blob/master/README.md)

QQ 协议端举例:

- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) (基于 [MiraiGo](https://github.com/Mrs4s/MiraiGo))
- [cqhttp-mirai-embedded](https://github.com/yyuueexxiinngg/cqhttp-mirai/tree/embedded)
- [Mirai](https://github.com/mamoe/mirai) + [cqhttp-mirai](https://github.com/yyuueexxiinngg/cqhttp-mirai)
- [Mirai](https://github.com/mamoe/mirai) + [Mirai Native](https://github.com/iTXTech/mirai-native) + [CQHTTP](https://github.com/richardchien/coolq-http-api)
- [OICQ-http-api](https://github.com/takayama-lily/onebot) (基于 [OICQ](https://github.com/takayama-lily/oicq))

这里以 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 为例

1. 下载 go-cqhttp 对应平台的 release 文件，[点此前往](https://github.com/Mrs4s/go-cqhttp/releases)
2. 运行 exe 文件或者使用 `./go-cqhttp` 启动
3. 生成默认配置文件并修改默认配置

```json{2,3,35-36,42}
{
  "uin": 你的QQ号,
  "password": "你的密码",
  "encrypt_password": false,
  "password_encrypted": "",
  "enable_db": true,
  "access_token": "",
  "relogin": {
    "enabled": true,
    "relogin_delay": 3,
    "max_relogin_times": 0
  },
  "_rate_limit": {
    "enabled": false,
    "frequency": 0,
    "bucket_size": 0
  },
  "ignore_invalid_cqcode": false,
  "force_fragmented": true,
  "heartbeat_interval": 0,
  "http_config": {
    "enabled": false,
    "host": "0.0.0.0",
    "port": 5700,
    "timeout": 0,
    "post_urls": {}
  },
  "ws_config": {
    "enabled": false,
    "host": "0.0.0.0",
    "port": 6700
  },
  "ws_reverse_servers": [
    {
      "enabled": true,
      "reverse_url": "ws://127.0.0.1:8080/cqhttp/ws",
      "reverse_api_url": "",
      "reverse_event_url": "",
      "reverse_reconnect_interval": 3000
    }
  ],
  "post_message_format": "array",
  "use_sso_address": false,
  "debug": false,
  "log_level": "",
  "web_ui": {
    "enabled": true,
    "host": "0.0.0.0",
    "web_ui_port": 9999,
    "web_input": false
  }
}
```

其中 `ws://127.0.0.1:8080/cqhttp/ws` 中的 `127.0.0.1` 和 `8080` 应分别对应 nonebot 配置的 HOST 和 PORT

## 历史性的第一次对话

一旦新的配置文件正确生效之后，NoneBot 所在的控制台（如果正在运行的话）应该会输出类似下面的内容（两条访问日志）：

```default
09-14 21:31:16 [INFO] uvicorn | ('127.0.0.1', 12345) - "WebSocket /cqhttp/ws" [accepted]
09-14 21:31:16 [INFO] nonebot | WebSocket Connection from CQHTTP Bot 你的QQ号 Accepted!
```

这表示 QQ 协议端已经成功地使用 CQHTTP 协议连接上了 NoneBot。

:::warning 注意
如果到这一步你没有看到上面这样的成功日志，CQHTTP 的日志中在不断地重连或无反应，请注意检查配置中的 IP 和端口是否确实可以访问。比较常见的出错点包括：

- NoneBot 监听 `0.0.0.0`，然后在 CQHTTP 配置中填了 `ws://0.0.0.0:8080/cqhttp/ws`
- 在 Docker 容器内运行 CQHTTP，并通过 `127.0.0.1` 访问宿主机上的 NoneBot
- 想从公网访问，但没有修改云服务商的安全组策略或系统防火墙
- NoneBot 所监听的端口存在冲突，已被其它程序占用
- 弄混了 NoneBot 的 `host`、`port` 参数与 CQHTTP 配置中的 `host`、`port` 参数
- 使用了 `ws_reverse_api_url` 和 `ws_reverse_event_url` 而非 universal client
- `ws://` 错填为 `http://`
- CQHTTP 或 NoneBot 启动时遭到外星武器干扰

请尝试重启 CQHTTP、重启 NoneBot、更换端口、修改防火墙、重启系统、仔细阅读前面的文档及提示、更新 CQHTTP 和 NoneBot 到最新版本等方式来解决。
:::

现在，尝试向你的 QQ 机器人账号发送如下内容：

```default
/echo 你好，世界
```

到这里如果一切 OK，你应该会收到机器人给你回复了 `你好，世界`。这一历史性的对话标志着你已经成功地运行了一个 NoneBot 的最小实例，开始了编写更强大的 QQ 机器人的创意之旅！

<ClientOnly>
  <Messenger :messages="[{ position: 'right', msg: '/echo 你好，世界' }, { position: 'left', msg: '你好，世界' }]"/>
</ClientOnly>
