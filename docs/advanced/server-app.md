# Server App

如果需要对 web 框架进行更详细的控制，可以通过 `bot.server_app` 访问到内部的 Quart 对象，之后可以像使用 Quart 的 app 对象一样添加路由、设置生命周期处理函数等。

## 自定义路由

### 简单的主页

```python
from nonebot import get_bot
bot = get_bot()

@bot.server_app.route('/')
async def hello_world():
    await bot.send_private_msg(1002647525, '你的主页被访问了')
    return '欢迎来到我的主页'
```

启动 nonebot 后访问 <http://127.0.0.1:8080/>，你会看见主页的欢迎词，并收到机器人的提醒。

### 更多应用

Quart 是一个与 Flask 具有相同 API 的异步 web 框架，其用法可以参考[Flask官方文档](https://flask.palletsprojects.com/)或它的[简中翻译版本](http://docs.jinkan.org/docs/flask/)，关于 Quart 可以参考[Quart官方文档](https://pgjones.gitlab.io/quart/)
