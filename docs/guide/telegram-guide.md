# Telegram Adapter 使用指南

## 配置 Telegram Bot

### 申请一个 Telegram 机器人

首先你需要有一个 Telegram 帐号，添加 [BotFather](https://t.me/botfather) 为好友。

接着，向它发送`/newbot`指令，按要求回答问题即可。

如果你成功创建了一个机器人，BotFather 会发给你机器人的 token：

```plain
1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI
```

将这个 token 填入 Nonebot 的`env`文件：

```dotenv
token = 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI
```

如果你需要让你的 Bot 响应除了 `/` 开头之外的消息，你需要向BotFather 发送 `/setprivacy` 并选择 `Disable`。

## 配置 Nonebot

### 使用代理

如果运行 Nonebot 的服务器位于中国大陆，那么你可能需要使用代理，否则将无法调用 Telegram 提供的任何 API。

```dotenv
proxy = "http://127.0.0.1:10809"
```

### 使用 Long polling 获取更新（推荐）

只要不在`env`文件中设置`url`，默认使用 long polling 模式。

### 使用 Webhook 获取更新

Telegram Bot 的 webhook 必须使用 https 协议，所以我推荐使用 nginx 反向代理。

```conf
server {
        server_name tg.yourdomain.com;
        location / {
                proxy_pass http://127.0.0.1:4000;
                proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        }
    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/tg.yourdomain.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/tg.yourdomain.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}
server {
    if ($host = tg.yourdomain.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
        listen 80;
        server_name tg.yourdomain.com;
    return 404; # managed by Certbot
}
```

如果需要在本地调试，我推荐使用 VSCode 的 Remote - SSH 插件，或者使用 frp 再进行一次反向代理。

最后将域名填入`env`文件：

```dotenv
url = https://tg.yourdomain.com/telegram/http
```

## 第一次对话

```python
from nonebot import on_command
from nonebot.rule import to_me
from nonebot_adapter_telegram import Bot
from nonebot_adapter_telegram.event import MessageEvent


echo = on_command("echo", rule=to_me())


@echo.handle()
async def _(bot: Bot, event: MessageEvent):
    await bot.send(event, event.get_message())
```

以上代码注册了一个对 telegram 适用的 echo 指令，并会提取 /echo 之后的内容发送到事件所对应的群或私聊。

> 查看更多示例：https://github.com/nonebot/adapter-telegram/tree/master/example
