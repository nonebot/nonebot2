# go-cqhttp 协议使用指南

::: warning

go-cqhttp 协议为 CQHTTP 协议的拓展，不兼容其他 CQHTTP 协议端

本适配器尚在开发中，目前与 CQHTTP 适配器的差别并不是很大

如果你想获得更稳定的支持，请使用官方维护的 [CQHTTP 适配器](./cqhttp-guide.md)

:::

## 安装 NoneBot GOCQ 适配器

```bash
pip install nonebot-adapter-gocq
```

为了便捷起见, 以下内容均以缩写 GOCQ 代替 go-cqhttp

## 从 CQHTTP 迁移到 GOCQ

如果你之前使用的是 CQHTTP 适配器，现在想迁移到 GOCQ 适配器。你只需要把 import 的包名从 `nonebot.adapters.cqhttp` 更改为 `nonebot_adapter_gocq` 即可，无需改动其他。

## 配置 GOCQ

::: warning

本教程根据 GOCQ 的 dev 分支编写，master 分支可能还未更新到此版本

如果你使用的是 release 版本的 GOCQ，请参考 [CQHTTP 协议使用指南](./cqhttp-guide.md)

:::

1. 下载 go-cqhttp 对应平台的 release 文件，[点此前往](https://github.com/Mrs4s/go-cqhttp/releases)
2. 运行 exe 文件或者使用 `./go-cqhttp` 启动
3. 生成默认配置文件时选择 3 并修改默认配置

```yml{4,5,25,83}
# go-cqhttp 默认配置文件

account: # 账号相关
  uin: 1233456 # QQ账号
  password: '' # 密码为空时使用扫码登录
  encrypt: false  # 是否开启密码加密
  status: 0      # 在线状态 请参考 https://github.com/Mrs4s/go-cqhttp/blob/dev/docs/config.md#在线状态
  relogin: # 重连设置
    delay: 3   # 首次重连延迟, 单位秒
    interval: 3   # 重连间隔
    max-times: 0  # 最大重连次数, 0为无限制

  # 是否使用服务器下发的新地址进行重连
  # 注意, 此设置可能导致在海外服务器上连接情况更差
  use-sso-address: true

heartbeat:
  # 心跳频率, 单位秒
  # -1 为关闭心跳
  interval: 5

message:
  # 上报数据类型
  # 可选: string,array
  post-format: array
  # 是否忽略无效的CQ码, 如果为假将原样发送
  ignore-invalid-cqcode: false
  # 是否强制分片发送消息
  # 分片发送将会带来更快的速度
  # 但是兼容性会有些问题
  force-fragment: false
  # 是否将url分片发送
  fix-url: false
  # 下载图片等请求网络代理
  proxy-rewrite: ''
  # 是否上报自身消息
  report-self-message: false
  # 移除服务端的Reply附带的At
  remove-reply-at: false
  # 为Reply附加更多信息
  extra-reply-data: false

output:
  # 日志等级 trace,debug,info,warn,error
  log-level: warn
  # 是否启用 DEBUG
  debug: false # 开启调试模式

# 默认中间件锚点
default-middlewares: &default
  # 访问密钥, 强烈推荐在公网的服务器设置
  access-token: ''
  # 事件过滤器文件目录
  filter: ''
  # API限速设置
  # 该设置为全局生效
  # 原 cqhttp 虽然启用了 rate_limit 后缀, 但是基本没插件适配
  # 目前该限速设置为令牌桶算法, 请参考:
  # https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95/6597000?fr=aladdin
  rate-limit:
    enabled: false # 是否启用限速
    frequency: 1  # 令牌回复频率, 单位秒
    bucket: 1     # 令牌桶大小

database: # 数据库相关设置
  leveldb:
    # 是否启用内置leveldb数据库
    # 启用将会增加10-20MB的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: true

# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  # 反向WS设置
  - ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://127.0.0.1:8080/gocq/ws
      # 反向WS API 地址
      api: ws://your_websocket_api.server
      # 反向WS Event 地址
      event: ws://your_websocket_event.server
      # 重连间隔 单位毫秒
      reconnect-interval: 3000
      middlewares:
        <<: *default # 引用默认中间件

```

其中 `ws://127.0.0.1:8080/gocq/ws` 中的 `127.0.0.1` 和 `8080` 应分别对应 nonebot 配置的 HOST 和 PORT。

`gocq` 是前述 `register_adapter` 时传入的第一个参数，代表设置的 `GOCQBot` 适配器的路径，你可以对不同的适配器设置不同路径以作区别。

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
