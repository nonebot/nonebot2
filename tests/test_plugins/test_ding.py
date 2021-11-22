from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.ding import Bot as DingBot
from nonebot.adapters.ding import MessageEvent, MessageSegment
from nonebot.adapters.ding.event import GroupMessageEvent, PrivateMessageEvent

helper = on_command("ding_helper", to_me())


@helper.handle()
async def ding_helper(bot: DingBot, event: MessageEvent):
    message = MessageSegment.markdown(
        "Hello, This is NoneBot",
        """帮助信息如下：\n
[ding_helper](dtmd://dingtalkclient/sendMessage?content=ding_helper) 查看帮助\n
[markdown](dtmd://dingtalkclient/sendMessage?content=markdown) 发送 markdown\n
[actionCardSingleBtn](dtmd://dingtalkclient/sendMessage?content=actionCardSingleBtn)\n
[actionCard](dtmd://dingtalkclient/sendMessage?content=actionCard)\n
[feedCard](dtmd://dingtalkclient/sendMessage?content=feedCard)\n
[atme](dtmd://dingtalkclient/sendMessage?content=atme)\n
[image](dtmd://dingtalkclient/sendMessage?content=image)\n
[t](dtmd://dingtalkclient/sendMessage?content=t)\n
[code](dtmd://dingtalkclient/sendMessage?content=code) 发送代码\n
[test_message](dtmd://dingtalkclient/sendMessage?content=test_message)\n
[hello](dtmd://dingtalkclient/sendMessage?content=hello)\n
[webhook](dtmd://dingtalkclient/sendMessage?content=webhook)""",
    )
    await markdown.finish(message)


markdown = on_command("markdown", to_me())


@markdown.handle()
async def markdown_handler(bot: DingBot):
    message = MessageSegment.markdown(
        "Hello, This is NoneBot",
        "#### NoneBot  \n> Nonebot 是一款高性能的 Python 机器人框架\n> ![screenshot](https://v2.nonebot.dev/logo.png)\n> [GitHub 仓库地址](https://github.com/nonebot/nonebot2) \n",
    )
    await markdown.finish(message)


actionCardSingleBtn = on_command("actionCardSingleBtn", to_me())


@actionCardSingleBtn.handle()
async def actionCardSingleBtn_handler(bot: DingBot):
    message = MessageSegment.actionCardSingleBtn(
        title="打造一间咖啡厅",
        text="![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png) \n #### 乔布斯 20 年前想打造的苹果咖啡厅 \n\n Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
        singleTitle="阅读全文",
        singleURL="https://www.dingtalk.com/",
    )
    await actionCardSingleBtn.finish(message)


actionCard = on_command("actionCard", to_me())


@actionCard.handle()
async def actionCard_handler(bot: DingBot):
    message = MessageSegment.raw(
        {
            "msgtype": "actionCard",
            "actionCard": {
                "title": "乔布斯 20 年前想打造一间苹果咖啡厅，而它正是 Apple Store 的前身",
                "text": "![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png) \n\n #### 乔布斯 20 年前想打造的苹果咖啡厅 \n\n Apple Store 的设计正从原来满满的科技感走向生活化，而其生活化的走向其实可以追溯到 20 年前苹果一个建立咖啡馆的计划",
                "hideAvatar": "0",
                "btnOrientation": "0",
                "btns": [
                    {"title": "内容不错", "actionURL": "https://www.dingtalk.com/"},
                    {"title": "不感兴趣", "actionURL": "https://www.dingtalk.com/"},
                ],
            },
        }
    )
    await actionCard.finish(message, at_sender=True)


feedCard = on_command("feedCard", to_me())


@feedCard.handle()
async def feedCard_handler(bot: DingBot):
    message = MessageSegment.raw(
        {
            "msgtype": "feedCard",
            "feedCard": {
                "links": [
                    {
                        "title": "时代的火车向前开1",
                        "messageURL": "https://www.dingtalk.com/",
                        "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png",
                    },
                    {
                        "title": "时代的火车向前开2",
                        "messageURL": "https://www.dingtalk.com/",
                        "picURL": "https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png",
                    },
                ]
            },
        }
    )
    await feedCard.finish(message)


atme = on_command("atme", to_me())


@atme.handle()
async def atme_handler(bot: DingBot, event: MessageEvent):
    message = f"@{event.senderId} manually at you" + MessageSegment.atDingtalkIds(
        event.senderId
    )
    await atme.send("matcher send auto at you", at_sender=True)
    await bot.send(event, "bot send auto at you", at_sender=True)
    await atme.finish(message)


image = on_command("image", to_me())


@image.handle()
async def image_handler(bot: DingBot, event: MessageEvent):
    message = MessageSegment.image(
        "https://static-aliyun-doc.oss-accelerate.aliyuncs.com/assets/img/zh-CN/0634199951/p158167.png"
    )
    await image.finish(message)


textAdd = on_command("t", to_me())


@textAdd.handle()
async def textAdd_handler(bot: DingBot, event: MessageEvent):
    message = "第一段消息\n" + MessageSegment.text("asdawefaefa\n")
    await textAdd.send(message)

    message = message + MessageSegment.text("第二段消息\n")
    await textAdd.send(message)

    message = (
        message + MessageSegment.text("\n第三段消息\n") + "adfkasfkhsdkfahskdjasdashdkjasdf"
    )
    message = message + MessageSegment.extension(
        {"text_type": "code_snippet", "code_language": "C#"}
    )
    await textAdd.send(message)


code = on_command("code", to_me())


@code.handle()
async def code_handler(bot: DingBot, event: MessageEvent):
    raw = MessageSegment.code("Python", 'print("hello world")')
    await code.send(raw)
    message = MessageSegment.text(
        """using System;

namespace HelloWorld
{
  class Program
  {
    static void Main(string[] args)
    {
      Console.WriteLine("Hello World!");
    }
  }
}"""
    )
    message += MessageSegment.extension(
        {"text_type": "code_snippet", "code_language": "C#"}
    )
    await code.finish(message)


test_message = on_command("test_message", to_me())


@test_message.handle()
async def test_message_handler1(bot: DingBot, event: PrivateMessageEvent):
    await test_message.finish("PrivateMessageEvent")


@test_message.handle()
async def test_message_handler2(bot: DingBot, event: GroupMessageEvent):
    await test_message.finish("GroupMessageEvent")


hello = on_command("hello", to_me())


@hello.handle()
async def hello_handler(bot: DingBot, event: MessageEvent):
    message = MessageSegment.raw(
        {
            "msgtype": "text",
            "text": {"content": "hello "},
        }
    )
    message += MessageSegment.atDingtalkIds(event.senderId)
    await hello.send(message)

    message = MessageSegment.text(f"@{event.senderId}，你好")
    message += MessageSegment.atDingtalkIds(event.senderId)
    await hello.finish(message)


hello = on_command("webhook", to_me())


@hello.handle()
async def webhook_handler(bot: DingBot, event: MessageEvent):
    print(event)
    message = MessageSegment.raw(
        {
            "msgtype": "text",
            "text": {"content": "hello from webhook,一定要注意安全方式的鉴权哦，否则可能发送失败的"},
        }
    )
    message += MessageSegment.atDingtalkIds(event.senderId)
    await hello.send(
        message,
        webhook="https://oapi.dingtalk.com/robot/send?access_token=XXXXXXXXXXXXXX",
        secret="SECXXXXXXXXXXXXXXXXXXXXXXXXX",
    )

    message = MessageSegment.text("TEST 123123  S")
    await hello.send(
        message,
        webhook="https://oapi.dingtalk.com/robot/send?access_token=XXXXXXXXXXXXXX",
    )
