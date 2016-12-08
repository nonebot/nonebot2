# QQBot

此 QQBot 非彼 QQBot，不是对 SmartQQ 的封装，而是基于开源的 [sjdy521/Mojo-Webqq](https://github.com/sjdy521/Mojo-Webqq) 实现的对消息的自动处理程序，支持自定义插件。

## 如何部署

推荐使用 Docker 部署，因为基本可以一键开启，如果你想手动运行，也可以参考第二个小标题「手动部署」。

### 使用 Docker

本仓库根目录下的 `docker-compose.yml` 即为 Docker Compose 的配置文件，直接跑就行。如果你想对镜像进行修改，可以自行更改 Dockerfile 来构建或者继承已经构建好的镜像。

### 手动运行

首先需要运行 sjdy521/Mojo-Webqq，具体见它的 GitHub 仓库的使用教程。然后运行：

```sh
pip install -r requirements.txt
python app.py
```

注意要求 Python 3.x。

## 插件

程序支持两种插件形式，一种是过滤器／Filter，一种是命令／Command。

本质上程序主体是一个 web app，接受 sjdy521/Mojo-Webqq 的 POST 请求，从而收到消息。收到消息后，首先运行过滤器，按照优先级从大到小顺序运行 `filters` 目录中的 `.py` 文件中指定的过滤器函数，函数返回非 False 即表示不拦截消息，从而消息继续传给下一个过滤器，如果返回了 False，则消息不再进行后续处理，而直接抛弃。过滤器运行完之后，会开始按照命令执行，首先根据命令的开始标志判断有没有消息中有没有指定命令，如果指定了，则执行指定的命令，如果没指定，则看当前用户有没有开启交互式会话，如果开启了会话，则执行会话指定的命令，否则，使用默认的 fallback 命令。

过滤器和命令的使用场景区别：

- 过滤器：可用于消息的后台日志、频率控制、关键词分析，一般在使用者无意识的情况下进行；
- 命令：使用者有意识地想要使用某个给定的命令的功能。

关于过滤器和命令的细节，请参考 [编写过滤器](Write_Filter.md) 和 [编写命令](Write_Command.md)。
