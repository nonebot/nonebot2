# Server App

如果需要对 web 框架进行更详细的控制，可以通过 `bot.server_app` 访问到内部的 Quart 对象，之后可以像使用 Quart 的 app 对象一样添加路由、设置生命周期处理函数等。

## 自定义路由
