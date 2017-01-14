# XiaoKai Bot 小开机器人

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/CCZU-DEV/xiaokai-bot/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/CCZU-DEV/xiaokai-bot.svg?branch=master)](https://travis-ci.org/CCZU-DEV/xiaokai-bot)
[![Docker Repository](https://img.shields.io/badge/docker-richardchien%2Fxiaokai--bot-blue.svg)](https://hub.docker.com/r/richardchien/xiaokai-bot/)
[![QQ](https://img.shields.io/badge/qq-1647869577-orange.svg)](#)
[![WeChat](https://img.shields.io/badge/wechat-cczu__xiaokai-brightgreen.svg)](#)

基于 [sjdy521/Mojo-Webqq](https://github.com/sjdy521/Mojo-Webqq) 和 [sjdy521/Mojo-Weixin](https://github.com/sjdy521/Mojo-Weixin) 实现的自动处理 QQ 和微信消息的机器人，支持自定义插件。

## 快速开始

### 部署

推荐使用 Docker 部署，因为基本可以一键开启，如果你想手动运行，也可以参考第二个小标题「手动部署」。

#### 使用 Docker

本仓库根目录下的 `docker-compose.yml` 即为 Docker Compose 的配置文件，直接跑就行（某些功能可能需要自行修改一下 `docker-compose.yml` 里的环境变量，例如如果要使用天气功能，需要在里面填上你的和风天气 API KEY）。如果你想对镜像进行修改，可以自行更改 Dockerfile 来构建或者继承已经构建好的镜像。

#### 手动运行

首先需要运行 sjdy521/Mojo-Webqq 或 sjdy521/Mojo-Webqq，具体见它们的 GitHub 仓库的使用教程。然后运行：

```sh
pip install -r requirements.txt
python app.py
```

注意要求 Python 3.x。

你可以通过设置环境变量来控制程序的某些行为，请参考 `docker-compose.yml` 文件中的最后一个容器的环境变量设置。

## 使用

![](https://ww3.sinaimg.cn/large/006tNbRwgw1fb4a75bp2dj30ku1nsaey.jpg)

## 局限性

由于 QQ 的限制，现有下列问题：

- 可能无法连续在线较长时间，因此需要频繁重启服务（大约一到两天一次）
- 无法处理临时消息
- 无法接受图片、语音消息等非文字消息
- 单条消息无法发送很长的内容
- 有时候群消息会被屏蔽，私聊消息则正常

目前看来微信相比 QQ 要更稳定一些，并且也可以接收图片、语音、视频等，不过有时候需要多次扫码才能登录成功。

## 插件

程序支持三种插件形式，分别是过滤器／Filter、命令／Command、自然语言处理器／NLProcessor，也即程序的三个处理层次。

用户可以自行编写插件来扩展功能，具体请看 [文档](https://cczu-dev.github.io/xiaokai-bot/)。下面简要介绍三层命令的执行流程。

### 过滤器

收到消息后，依次运行所有过滤器，即按照优先级从大到小顺序运行 `filters` 目录中的 `.py` 文件中指定的过滤器函数，函数返回非 False 即表示不拦截消息，从而消息继续传给下一个过滤器，如果返回了 False，则消息不再进行后续处理，而直接抛弃。

### 命令

命令分发器（`filters/command_dispatcher.py`)是一个预设的优先级为 0 的过滤器，它根据命令的开始标志判断消息中有没有指定命令，如果指定了，则执行指定的命令，如果没指定，则看当前用户有没有开启交互式会话，如果开启了会话，则执行会话指定的命令，否则，使用默认的 fallback 命令（`config.py` 中 `fallback_command` 指定，默认为 `natural_language.process`）。

### 自然语言处理器

程序默认的 fallback 命令是 `natural_language.process`，也即自然语言处理命令，这个命令会通过消息的分词结果寻找注册了相应关键词的 NL 处理器并调用它们，得到一个有可能的等价命令列表，然后选择其中置信度最高且超过 60 的命令作为最佳识别结果执行。如果没有超过 60 的命令，则调用另一个 fallback 命令（`config.py` 中 `fallback_command_after_nl_processors` 指定，默认为 `ai.tuling123`）。