---
sidebar: auto
---

# 更新日志

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
