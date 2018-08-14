# 开始使用

一切都安装成功后，你就已经做好了进行简单配置以运行一个最小的 NoneBot 实例的准备。

## 最小实例

使用你最熟悉的编辑器或 IDE，创建一个名为 `bot.py` 的文件，内容如下：

```python
# bot.py

import none

if __name__ == '__main__':
    none.init()
    none.load_builtin_plugins()
    none.run(host='127.0.0.1', port=8080)
```

`if __name__ == '__main__'` 语句块的这几行代码将依次：

1. 使用默认配置初始化 NoneBot 包
2. 加载 NoneBot 内置的插件
3. 在地址 `127.0.0.1:8080` 运行 NoneBot

::: tip 提示
这里 `none.run()` 的参数 `host='127.0.0.1'` 表示让 NoneBot 监听本地回环地址，如果你的酷 Q 运行在非本机的其它位置，例如 Docker 容器内、局域网内的另一台机器上等，则这里需要修改 `host` 参数为希望让 CoolQ HTTP API 插件访问的 IP。如果不清楚该使用哪个 IP，或者希望本机的所有 IP 都被监听，可以使用 `0.0.0.0`。
:::

在命令行使用如下命令即可运行这个 NoneBot 实例：

```bash
python bot.py
```

## 配置 CoolQ HTTP API 插件

单纯运行 NoneBot 实例并不会产生任何效果，因为此刻酷 Q 这边还不知道 NoneBot 的存在，也就无法把消息发送给它，因此现在需要对 CoolQ HTTP API 插件做一个简单的配置来让它把消息等事件上报给 NoneBot。

如果你在之前已经按照 [安装](/guide/installation.md) 的建议使用默认配置运行了一次 CoolQ HTTP API 插件，此时酷 Q 的 `app\io.github.richardchien.coolqhttpapi\config\` 目录中应该已经有了一个名为 `<user-id>.json` 的文件（`<user-id>` 为你登录的 QQ 账号）。修改这个文件，**添加**如下配置项：

```json
{
    "ws_reverse_api_url": "ws://127.0.0.1:8080/ws/api/",
    "ws_reverse_event_url": "ws://127.0.0.1:8080/ws/event/",
    "ws_reverse_reconnect_on_code_1000": true,
    "use_ws_reverse": true
}
```

::: tip 提示
这里的 `127.0.0.1:8080` 对应 `none.run()` 中传入的 `host` 和 `port`，如果在 `none.run()` 中传入的 `host` 是 `0.0.0.0`，则插件的配置中需使用任意一个能够访问到 NoneBot 所在环境的 IP。特别地，如果你的酷 Q 运行在 Docker 容器中，NoneBot 运行在宿主机中，则默认情况下这里需使用 `172.17.0.1`（不同机器有可能不同，需使用 `docker inspect bridge` 查看，具体见 Docker 文档的 [Configure networking](https://docs.docker.com/network/)）。
:::

修改之后，在酷 Q 的应用菜单中重启 CoolQ HTTP API 插件，或直接重启酷 Q，以使新的配置文件生效。

## 历史性的第一次对话

一旦新的配置文件正确生效之后，NoneBot 所在的控制台（如果正在运行的话）应该会输出类似下面的内容：

```
[2018-08-14 23:35:35,532] 127.0.0.1:8080 GET /ws/api/ ws 101 - 2736
[2018-08-14 23:35:35,534] 127.0.0.1:8080 GET /ws/event/ ws 101 - 4682
```

这表示 CoolQ HTTP API 插件已经成功地连接上了 NoneBot，与此同时，插件的日志文件中也会输出反向 WebSocket 连接成功的日志。

::: warning 注意
如果到这一步你没有看到上面这样的日志，请注意排查配置中的 IP 和端口是否确实可以访问。
:::

现在，尝试向你的 QQ 机器人账号发送如下内容：

```
/echo 你好，世界
```

到这里如果一切都没有问题，你应该会收到机器人给你回复了 `你好，世界`。这一历史性的对话标志着你已经成功地运行了一个 NoneBot 的最小实例，开始了编写更强大的 QQ 机器人的创意之旅！
