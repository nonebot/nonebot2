---
sidebar: auto
---

# 更新日志

## v2.0.0a14

- 修改日志等级，支持输出等级自定义
- 修复日志输出模块名错误
- 修改 `Matcher` 属性 `module` 类型
- 新增 `Matcher` 属性 `plugin_name` `module_name` `module_prefix`

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
