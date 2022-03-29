---
description: Changelog
toc_max_heading_level: 2
---

# 更新日志

## 最近更新

### 🚀 新功能

- Feature: 添加 Rule, Permission 反向位运算支持 [@yanyongyu](https://github.com/yanyongyu) ([#872](https://github.com/nonebot/nonebot2/pull/872))
- Feature: 新增文本完整匹配规则 [@A-kirami](https://github.com/A-kirami) ([#797](https://github.com/nonebot/nonebot2/pull/797))

### 🐛 Bug 修复

- Fix: 修复 event 类型检查会对类型进行自动转换 [@yanyongyu](https://github.com/yanyongyu) ([#876](https://github.com/nonebot/nonebot2/pull/876))
- Fix: 修复 `on_fullmatch` 返回类型错误 [@yanyongyu](https://github.com/yanyongyu) ([#815](https://github.com/nonebot/nonebot2/pull/815))
- Fix: 修复 DataclassEncoder 嵌套 encode 的问题 [@AkiraXie](https://github.com/AkiraXie) ([#812](https://github.com/nonebot/nonebot2/pull/812))

### 📝 文档

- Docs: 修复适配器文档内商店链接 [@yanyongyu](https://github.com/yanyongyu) ([#861](https://github.com/nonebot/nonebot2/pull/861))
- Docs: tips for finding adapters' document link [@StarHeartHunt](https://github.com/StarHeartHunt) ([#860](https://github.com/nonebot/nonebot2/pull/860))
- Docs: 添加对 `fastapi_reload` 在 Windows 平台额外影响的说明 [@CherryGS](https://github.com/CherryGS) ([#830](https://github.com/nonebot/nonebot2/pull/830))
- Docs: 修复 ci/cd action 中错误的版本号 [@Bubbleioa](https://github.com/Bubbleioa) ([#819](https://github.com/nonebot/nonebot2/pull/819))
- Docs: 减小更新日志 toc 最大显示等级 [@yanyongyu](https://github.com/yanyongyu) ([#813](https://github.com/nonebot/nonebot2/pull/813))
- Docs: 修改议题模板中的错误链接 [@he0119](https://github.com/he0119) ([#807](https://github.com/nonebot/nonebot2/pull/807))
- Docs: 修改消息模板文档中错误的样例 [@mnixry](https://github.com/mnixry) ([#806](https://github.com/nonebot/nonebot2/pull/806))
- Docs: 更新贡献指南 [@yanyongyu](https://github.com/yanyongyu) ([#798](https://github.com/nonebot/nonebot2/pull/798))

### 💫 杂项

- CI: 修复发布机器人的意外错误 [@he0119](https://github.com/he0119) ([#892](https://github.com/nonebot/nonebot2/pull/892))
- Docs: 替换和移除部分已经失效的插件 [@MeetWq](https://github.com/MeetWq) ([#879](https://github.com/nonebot/nonebot2/pull/879))
- Docs: 添加 netlify 标签 [@yanyongyu](https://github.com/yanyongyu) ([#816](https://github.com/nonebot/nonebot2/pull/816))
- Fix: 修改错误的插件 PyPI 项目名称 [@Lancercmd](https://github.com/Lancercmd) ([#804](https://github.com/nonebot/nonebot2/pull/804))
- CI: 添加更新日志自动更新 action [@yanyongyu](https://github.com/yanyongyu) ([#799](https://github.com/nonebot/nonebot2/pull/799))

### 🍻 插件发布

- Plugin: 汉兜 Handle [@yanyongyu](https://github.com/yanyongyu) ([#899](https://github.com/nonebot/nonebot2/pull/899))
- Plugin: 多适配器帮助函数 [@yanyongyu](https://github.com/yanyongyu) ([#897](https://github.com/nonebot/nonebot2/pull/897))
- Plugin: 语句抽象化 [@yanyongyu](https://github.com/yanyongyu) ([#894](https://github.com/nonebot/nonebot2/pull/894))
- Plugin: 快速搜索 [@yanyongyu](https://github.com/yanyongyu) ([#889](https://github.com/nonebot/nonebot2/pull/889))
- Plugin: wordle 猜单词 [@yanyongyu](https://github.com/yanyongyu) ([#891](https://github.com/nonebot/nonebot2/pull/891))
- Plugin: MediaWiki 查询 [@yanyongyu](https://github.com/yanyongyu) ([#886](https://github.com/nonebot/nonebot2/pull/886))
- Plugin: HikariSearch [@yanyongyu](https://github.com/yanyongyu) ([#884](https://github.com/nonebot/nonebot2/pull/884))
- Plugin: 第二个 leetcode 查询插件 [@yanyongyu](https://github.com/yanyongyu) ([#882](https://github.com/nonebot/nonebot2/pull/882))
- Plugin: 成分姬 [@yanyongyu](https://github.com/yanyongyu) ([#878](https://github.com/nonebot/nonebot2/pull/878))
- Plugin: Arcaea 查分插件 [@yanyongyu](https://github.com/yanyongyu) ([#875](https://github.com/nonebot/nonebot2/pull/875))
- Plugin: QQ 自动同意好友申请 [@yanyongyu](https://github.com/yanyongyu) ([#871](https://github.com/nonebot/nonebot2/pull/871))
- Plugin: 21 点游戏插件 [@yanyongyu](https://github.com/yanyongyu) ([#865](https://github.com/nonebot/nonebot2/pull/865))
- Plugin: 色图生成 [@yanyongyu](https://github.com/yanyongyu) ([#863](https://github.com/nonebot/nonebot2/pull/863))
- Plugin: bilibili 通知插件 [@yanyongyu](https://github.com/yanyongyu) ([#859](https://github.com/nonebot/nonebot2/pull/859))
- Plugin: 订阅推送管理 [@yanyongyu](https://github.com/yanyongyu) ([#855](https://github.com/nonebot/nonebot2/pull/855))
- Plugin: 动漫新闻 [@yanyongyu](https://github.com/yanyongyu) ([#852](https://github.com/nonebot/nonebot2/pull/852))
- Plugin: 游戏王卡查 [@yanyongyu](https://github.com/yanyongyu) ([#846](https://github.com/nonebot/nonebot2/pull/846))
- Plugin: 二维码识别与发送 [@yanyongyu](https://github.com/yanyongyu) ([#843](https://github.com/nonebot/nonebot2/pull/843))
- Plugin: mockingbird [@yanyongyu](https://github.com/yanyongyu) ([#841](https://github.com/nonebot/nonebot2/pull/841))
- Plugin: QQ 自动续火花 [@yanyongyu](https://github.com/yanyongyu) ([#839](https://github.com/nonebot/nonebot2/pull/839))
- Plugin: 每日一句 [@yanyongyu](https://github.com/yanyongyu) ([#832](https://github.com/nonebot/nonebot2/pull/832))
- Plugin: 原神抽卡记录分析 [@yanyongyu](https://github.com/yanyongyu) ([#829](https://github.com/nonebot/nonebot2/pull/829))
- Plugin: YetAnotherPicSearch [@yanyongyu](https://github.com/yanyongyu) ([#825](https://github.com/nonebot/nonebot2/pull/825))
- Plugin: 60s 读世界小插件 [@yanyongyu](https://github.com/yanyongyu) ([#810](https://github.com/nonebot/nonebot2/pull/810))
- Plugin: pixiv.net p 站查询图片 [@yanyongyu](https://github.com/yanyongyu) ([#803](https://github.com/nonebot/nonebot2/pull/803))

## v2.0.0-beta.2

- 修复 `receive`, `got` 在参数为空消息时依旧会反复询问
- 修复文档商店分页显示错误
- 修复插件导入失败时，依然存在于已导入插件列表中
- 移除 `state` 依赖注入所需的默认值 `State()`
- 增加 `fastapi` 配置项：是否将适配器路由包含在 schema 中
- 修改 `load_builtin_plugins` 函数，使其能够支持加载多个内置插件
- 新增 `load_builtin_plugin` 函数，用于加载单个内置插件
- 修改 `Message` 和 `MessageSegment` 类，完善 typing，转移 Mapping 构建支持至 pydantic validate
- 调整项目结构，分离内部定义与用户接口
- 新增 Bot 连接事件钩子 (如 `driver.on_bot_connect` ) 的依赖注入

## v2.0.0-beta.1

- 新增 `MessageTemplate` 对于 `str` 普通模板的支持
- 移除插件加载的 `NameSpace` 模式
- 修改 toml 加载插件时的键名为 `tool.nonebot` 以符合规范
- 新增 Handler 依赖注入支持，同步/异步支持
- 统一 `Processor`, `Rule`, `Permission`, `Processor` 使用 `Handler`
- 修改内置 `Rule`, `Permission` 如 `startswith`, `command` 等使用 class 实现
- 更换文档框架 (docusaurus) 以及主题 (docusaurus-theme-nonepress)
- 移除 Matcher `state_factory` 支持

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
