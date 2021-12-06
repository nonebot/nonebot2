# 更新日志

## v2.0.0b1

- 新增 `MessageTemplate` 对于 `str` 普通模板的支持
- 移除插件加载的 `NameSpace` 模式
- 修改 toml 加载插件时的键名为 `tool.nonebot` 以符合规范
- 新增 Handler 依赖注入支持，同步/异步支持
- 统一 `Processor`, `Rule`, `Permission`, `Processor` 使用 `Handler`
- 修改内置 `Rule`, `Permission` 如 `startswith`, `command` 等使用 class 实现
- 更换文档框架 (docusaurus) 以及主题 (docusaurus-theme-nonepress)

## v2.0.0a16

- 新增 `MessageTemplate` 可用于 `Message` 的模板生成
- 新增 `matcher.got` `matcher.send` `matcher.pause` `matcher.reject` `matcher.finish` 支持 `MessageTemplate`
- 移除 `matcher.got` 原本的 `state format` 支持，由 `MessageTemplate` template 替代
- `adapter` 基类拆分为单独文件
- 修复 `fastapi` Driver Websocket 未能正确提供请求头部
- 新增 `fastapi` Driver 更多的 uvicorn 相关配置项
- 新增 `quart` Driver 更多的 uvicorn 相关配置项
- 修复 `endswith` Rule 错误的正则匹配
- 修复 `cqhttp` Adapter `image`, `record`, `video` 对 `BytesIO` 不正常的读取操作

## v2.0.0a15

- 修复 `fastapi` Driver 未能正确进行 reconnect
- 修复 `MessageSegment` 错误的 Mapping 映射

## v2.0.0a14

- 修改日志等级，支持输出等级自定义
- 修复日志输出模块名错误
- 修改 `Matcher` 属性 `module` 类型
- 新增 `Matcher` 属性 `plugin_name` `module_name` `module_prefix`
- 移除 `bot.call_api` 参数 `self_id` 切换机器人支持
- 修复 `type_updater` `permission_updater` 未传递的错误
- 修复 `type_updater` `permission_updater` 参数 `state` 错误
- 修复使用 `state_factory` 后导致无法在 session 内传递 `state`
- 重构 `Driver` 及连接信息抽象
- 新增正向 Driver(Client) 支持
- 新增 `aiohttp` 正向 Driver
- `fastapi` Driver 新增正向支持

## v2.0.0a13.post1

- 分离 `handler` 与 `matcher`
- 修复 `cqhttp` secret 校验出错
- 修复 `pydantic 1.8` 导致的 `alias` 问题
- 修改 `cqhttp` `ding` `session id`，不再允许跨群
- 修改 `shell_command` 存储 message
- 修复 `cqhttp` 检查 reply 失败退出
- 新增 `call_api` hook 接口
- 优化 `import hook`

## v2.0.0a11

- 修改 `nonebot` 项目结构，分离所有 `adapter`
- 修改插件加载逻辑，使用 `import hook` (PEP 302)
- 新增插件加载方式: `json`, `toml`
- 适配 `pydantic` ~1.8
- 移除 4 种内置事件类型限制，允许自定义事件类型
- 新增会话权限更新自定义，会话中断时更新权限以做到多人会话

## v2.0.0a10

- 新增 `Quart Driver` 支持
- 修复 `mirai` 协议适配命令处理以及消息转义

## v2.0.0a9

- 修复 `Message` 消息为 `None` 时的处理错误
- 修复 `Message.extract_plain_text` 返回为转义字符串的问题
- 修复命令处理错误地删除了后续空格
- 增加好友添加和加群请求事件 `approve`, `reject` 方法
- 新增 `mirai-api-http` 协议适配
- 修复 rule 运行时 state 覆盖问题，隔离 state
- 新增 `shell like command` 支持

## v2.0.0a8

- 修改 typing 类型注释
- 修改 event 基类接口
- 修复部分非法 CQ 码被识别导致报错
- 修复非 text 类型 CQ 码 data 未进行去转义
- 修复内置插件未进行去转义，修改内置插件为 cqhttp 定制
- 修复 `load_plugins` 加载不合法的包时出现 `spec` 为 `None` 的问题
- 出于**CQ 码安全性考虑**，使用 cqhttp 的 `bot.send` 或者 `matcher.send` 时默认对字符串进行转义
- 移动 cqhttp 相关 `Permission` 至 `nonebot.adapters.cqhttp` 包内

## v2.0.0a7

- 修复 cqhttp 检查 to me 时出现 IndexError
- 修复已失效的事件响应器仍会运行一次的 bug
- 修改 cqhttp 检查 reply 时未去除后续 at 以及空格
- 添加 get_plugin 获取插件函数
- 添加插件 export, require 方法
- **移除**内置 apscheduler 定时任务支持
- **移除**内置协议适配默认加载
- 新增**钉钉**协议适配
- 移除原有共享型 `MatcherGroup` 改为默认型 `MatcherGroup`

## v2.0.0a6

- 修复 block 失效问题 (hotfix)

## v2.0.0a5

- 更新插件指南文档
- 修复临时事件响应器运行后删除造成的多次响应问题
