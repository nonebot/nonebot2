# CQHTTP 协议使用指南

## 安装 NoneBot CQHTTP 适配器

```bash
pip install nonebot-adapter-cqhttp
```

## 配置 CQHTTP 协议端（以 QQ 为例）

单纯运行 NoneBot 实例并不会产生任何效果，因为此刻 QQ 这边还不知道 NoneBot 的存在，也就无法把消息发送给它，因此现在需要使用一个无头 QQ 来把消息等事件上报给 NoneBot。

QQ 协议端举例:

- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) (基于 [MiraiGo](https://github.com/Mrs4s/MiraiGo))
- [onebot-kotlin](https://github.com/yyuueexxiinngg/onebot-kotlin)
- [Mirai](https://github.com/mamoe/mirai) + [onebot-mirai](https://github.com/yyuueexxiinngg/onebot-kotlin)
- [Mirai](https://github.com/mamoe/mirai) + [Mirai Native](https://github.com/iTXTech/mirai-native) + [CQHTTP](https://github.com/richardchien/coolq-http-api)
- [node-onebot](https://github.com/takayama-lily/node-onebot) (基于 [abot](https://github.com/takayama-lily/abot), [OICQ](https://github.com/takayama-lily/oicq))

这里以 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 为例

1. 下载 go-cqhttp 对应平台的 release 文件，[点此前往](https://github.com/Mrs4s/go-cqhttp/releases)
2. 运行 exe 文件或者使用 `./go-cqhttp` 启动
3. 生成默认配置文件并修改默认配置

```yml{2,3,18,57,58}
account:
  uin: 机器人QQ号
  password: "机器人密码"
  encrypt: false
  relogin:
    disabled: false
    delay: 3
    interval: 0
    max-times: 0

  use-sso-address: true

heartbeat:
  disabled: false
  interval: 5

message:
  post-format: array
  ignore-invalid-cqcode: false
  force-fragment: false
  fix-url: false
  proxy-rewrite: ""
  report-self-message: false
  remove-reply-at: false
  extra-reply-data: false

output:
  log-level: warn
  debug: false

default-middlewares: &default
  access-token: ""
  filter: ""
  rate-limit:
    enabled: false
    frequency: 1
    bucket: 1

servers:
  - http:
      disabled: true
      host: 127.0.0.1
      port: 5700
      timeout: 5
      middlewares:
        <<: *default
      post:

  - ws:
      disabled: true
      host: 127.0.0.1
      port: 6700
      middlewares:
        <<: *default

  - ws-reverse:
      disabled: false
      universal: ws://127.0.0.1:8080/cqhttp/ws
      api: ws://your_websocket_api.server
      event: ws://your_websocket_event.server
      reconnect-interval: 3000
      middlewares:
        <<: *default

database:
  leveldb:
    enable: true
```

其中 `ws://127.0.0.1:8080/cqhttp/ws` 中的 `127.0.0.1` 和 `8080` 应分别对应 nonebot 配置的 HOST 和 PORT。

`cqhttp` 是前述 `register_adapter` 时传入的第一个参数，代表设置的 `CQHTTPBot` 适配器的路径，你可以对不同的适配器设置不同路径以作区别。

## 历史性的第一次对话

一旦新的配置文件正确生效之后，NoneBot 所在的控制台（如果正在运行的话）应该会输出类似下面的内容（两条访问日志）：

```default
09-14 21:31:16 [INFO] uvicorn | ('127.0.0.1', 12345) - "WebSocket /cqhttp/ws" [accepted]
09-14 21:31:16 [INFO] nonebot | WebSocket Connection from CQHTTP Bot 你的QQ号 Accepted!
```

这表示 CQHTTP 协议端已经成功地使用 CQHTTP 协议连接上了 NoneBot。

现在，尝试向你的机器人账号发送如下内容：

```default
/echo 你好，世界
```

到这里如果一切 OK，你应该会收到机器人给你回复了 `你好，世界`。这一历史性的对话标志着你已经成功地运行了一个 NoneBot 的最小实例，开始了编写更强大的 QQ 机器人的创意之旅！

<ClientOnly>
  <Messenger :messages="[{ position: 'right', msg: '/echo 你好，世界' }, { position: 'left', msg: '你好，世界' }]"/>
</ClientOnly>
