# Server App

如果需要对 web 框架进行更详细的控制，可以通过 `bot.server_app` 访问到内部的 Quart 对象，之后可以像使用 Quart 的 app 对象一样添加路由、设置生命周期处理函数等。

:::tip 提示
Quart 是一个与 Flask 具有相同 API 的异步 web 框架，其用法可以参考 [官方文档](https://pgjones.gitlab.io/quart/)。
:::

## 自定义路由

这里以一个简单的管理页面为例：

```python
import nonebot

bot = nonebot.get_bot()  # 在此之前必须已经 init

@bot.server_app.route('/admin')
async def admin():
    await bot.send_private_msg(12345678, '你的主页被访问了')
    return '欢迎来到管理页面'
```

启动 NoneBot 后访问 <http://127.0.0.1:8080/admin>，你会看见管理页面的欢迎词，并收到机器人的提醒。

## 处理生命周期事件

有时可能需要在 NoneBot 启动时初始化数据库连接池，例如：

```python
import nonebot

bot = nonebot.get_bot()  # 在此之前必须已经 init

@bot.server_app.before_serving
async def init_db():
    # 这会在 NoneBot 启动后立即运行
    pass
```
