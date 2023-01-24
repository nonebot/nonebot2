---
sidebar_position: 5
description: 控制事件响应器的权限

options:
  menu:
    weight: 60
    category: appendices
---

# 权限控制

**权限控制**是机器人在实际应用中需要解决的重点问题之一，NoneBot 提供了灵活的权限控制机制 —— `Permission`。

## 基础使用

`Permission` 是由非负整数个 `PermissionChecker` 所共同组成的**用于筛选事件**的对象。通常情况下，`Permission` 更侧重于对于**触发事件的机器人用户**的筛选，例如由 NoneBot 自身提供的 `SUPERUSER` 权限，便是筛选出会话发起者是否为超级用户。它可以对输入的用户进行鉴别，如果符合要求则会被认为通过并返回 `True`，反之则返回 `False`。

简单来说，`Permission` 是一个用于筛选出符合要求的用户的机制，可以通过 `Permission` 精确的控制响应对象的覆盖范围，从而拒绝掉我们所不希望的事件。
