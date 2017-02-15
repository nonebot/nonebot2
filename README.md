# XiaoKai Bot 小开机器人

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/CCZU-DEV/xiaokai-bot/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/CCZU-DEV/xiaokai-bot.svg?branch=master)](https://travis-ci.org/CCZU-DEV/xiaokai-bot)
[![Docker Repository](https://img.shields.io/badge/docker-richardchien%2Fxiaokai--bot-blue.svg)](https://hub.docker.com/r/richardchien/xiaokai-bot/)
[![QQ](https://img.shields.io/badge/qq-1647869577-orange.svg)](#)
[![WeChat](https://img.shields.io/badge/wechat-cczu__xiaokai-brightgreen.svg)](#)

用 Python 编写的即时聊天平台机器人，通过适配器模式支持使用多种 bot 框架／平台作为消息源（目前支持 Mojo-Webqq、Mojo-Weixin），支持自定义插件。

请注意区分此程序和其它模拟登录或封装接口的聊天平台**客户端**，此程序不负责登录或维护即时聊天平台的账号的状态，而只负责收到消息之后对消息的分析、处理、回复等逻辑，本程序通过适配器来与所支持的聊天平台客户端进行通讯，通常包括上报数据的统一化、调用接口获取额外信息、发送消息等，而这些聊天平台客户端（很多时候它们的项目名称也是「某某 bot」，相当于机器人的前端）需要你自行运行。

## 如何运行

### 预备

首先你需要了解如何运行你需要的消息源。以 Mojo-Weixin 为例，查看它的 [官方使用文档](https://github.com/sjdy521/Mojo-Weixin#如何使用) 来了解如何运行，其它消息源基本类似。

注意消息源必须已有相应的消息源适配器，消息源的概念解释及目前支持的消息源见 [消息源列表](https://cczu-dev.github.io/xiaokai-bot/#/Message_Sources)。

### 配置

复制 `config.sample.py` 为 `config.py`，然后修改 `config.py` 中的 `message_sources` 字段，定义你需要的消息源，例如：

```python
{
    'via': 'mojo_weixin',
    'login_id': 'your_login_id',
    'superuser_id': 'your_superuser_id',
    'api_url': 'http://127.0.0.1:5001/openwx',
}
```

上面的定义了一个 Mojo-Weixin 消息源，登录号是 `your_login_id`，超级用户 ID 是 `your_superuser_id`，Mojo-Weixin API 地址是 `http://127.0.0.1:5001/openwx`，`via` 和 `login_id` 是必须的，其它字段根据不同消息源适配器可能略有不同，具体请查看 [消息源列表](https://cczu-dev.github.io/xiaokai-bot/#/Message_Sources)。

与此同时，当你决定了本 bot 程序要运行的 IP 和端口之后，要把相应的上报 URL 填写到消息源程序的配置参数中，上报 URL 格式必须为 `http://your_host:your_port/<string:via>/<string:login_id>`，这里可以见到 `via` 和 `login_id`，即为之前定义消息源时必填的项，用来唯一确定一个消息来源。比如如果你使用 Mojo-Weixin 登录一个 bot，微信号为 `my_bot`，而本 bot 程序跑在 `127.0.0.1` 的 `8888` 端口，那么你需要在 Mojo-Weixin 的参数中设置 `post_url` 为 `http://127.0.0.1:8888/mojo_weixin/my_bot`。

### 运行

推荐使用 Docker 运行，因为基本可以一键开启，如果你想手动运行，也可以参考第二个小标题「手动运行」。

#### 使用 Docker 运行

本仓库根目录下的 `docker-compose.yml` 即为 Docker Compose 的配置文件，直接跑就行（某些功能可能需要自行修改一下 `docker-compose.yml` 里的环境变量，例如如果要使用天气功能，需要在里面填上你的和风天气 API KEY）。如果你想对镜像进行修改，可以自行更改 Dockerfile 来构建或者继承已经构建好的镜像。

#### 手动运行

```sh
pip3 install -r requirements.txt
python3 app.py
```

你可以通过设置环境变量来控制程序的某些行为，请参考 `docker-compose.yml` 文件中的最后一个容器的环境变量设置。

## 如何使用

如果不是出于修改程序以适应自己的需求的目的，建议直接使用已经跑起来的小开 bot 即可，使用文档见 [如何使用 CCZU 小开机器人](http://fenkipedia.cn/wiki/%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8CCZU%E5%B0%8F%E5%BC%80%E6%9C%BA%E5%99%A8%E4%BA%BA)。而如果是自行修改，那么使用方式就由你自己的插件决定了。

下面是一个示例的使用截图：

![](https://ww3.sinaimg.cn/large/006tNbRwgw1fb4a75bp2dj30ku1nsaey.jpg)

## 局限性

这里不讨论消息源客户端的局限性，那不是后端所负责的范围。只讨论本程序（聊天机器人后端）的局限性：

- 直接忽略了所有事件类型的上报，比如好友请求、群请求，只接受消息类型
- 目前只能处理文字消息（微信语音消息会通过语音识别转成文字）

## 配置文件

本程序的配置文件（`config.py`）非常简单，重要的配置只有消息源定义、默认命令等，还有一些对标记的定义，如命令开始标记、命令名与参数分割标记等，基本上都是字面义，通过字段名即可明白，这里不再给出具体的文档。

## 消息源适配器

简称「适配器」，用来在消息源和本程序之间进行数据格式的转换，相当于一个驱动程序，通过不同的驱动程序，本程序便可以接入多种聊天平台。用户可以自行开发适配器来适配尚未支持的消息源，见 [编写消息源适配器](https://cczu-dev.github.io/xiaokai-bot/#/Write_Adapter)。

## 插件

程序支持三种插件形式，分别是过滤器／Filter、命令／Command、自然语言处理器／NLProcessor，也即程序的三个处理层次。

用户可以自行编写插件来扩展功能，具体请看 [文档](https://cczu-dev.github.io/xiaokai-bot/)。下面简要介绍三层命令的执行流程。

### 过滤器

收到消息后，依次运行所有过滤器，即按照优先级从大到小顺序运行 `filters` 目录中的 `.py` 文件中指定的过滤器函数，函数返回非 False 即表示不拦截消息，从而消息继续传给下一个过滤器，如果返回了 False，则消息不再进行后续处理，而直接抛弃。

### 命令

命令分发器（`filters/command_dispatcher.py`)是一个预设的优先级为 0 的过滤器，它根据命令的开始标志判断消息中有没有指定命令，如果指定了，则执行指定的命令，如果没指定，则看当前用户有没有开启交互式会话，如果开启了会话，则执行会话指定的命令，否则，使用默认的 fallback 命令（`config.py` 中 `fallback_command` 指定，默认为 `natural_language.process`）。

### 自然语言处理器

程序默认的 fallback 命令是 `natural_language.process`，也即自然语言处理命令，这个命令会通过消息的分词结果寻找注册了相应关键词的 NL 处理器并调用它们，得到一个有可能的等价命令列表，然后选择其中置信度最高且超过 60 的命令作为最佳识别结果执行。如果没有超过 60 的命令，则调用另一个 fallback 命令（`config.py` 中 `fallback_command_after_nl_processors` 指定，默认为 `ai.tuling123`）。
