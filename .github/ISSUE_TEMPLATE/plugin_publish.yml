name: 发布插件
title: "Plugin: {name}"
description: 发布插件到 NoneBot 官方商店
labels: ["Plugin"]
body:
  - type: input
    id: pypi
    attributes:
      label: PyPI 项目名
      description: PyPI 项目名
      placeholder: e.g. nonebot-plugin-xxx
    validations:
      required: true

  - type: input
    id: module
    attributes:
      label: 插件 import 包名
      description: 插件 import 包名
      placeholder: e.g. nonebot_plugin_xxx
    validations:
      required: true

  - type: input
    id: tags
    attributes:
      label: 标签
      description: 标签
      placeholder: 'e.g. [{"label": "标签名", "color": "#ea5252"}]'
      value: "[]"
    validations:
      required: true

  - type: textarea
    id: config
    attributes:
      label: 插件配置项
      description: 插件配置项
      render: dotenv
      placeholder: |
        # e.g.
        # KEY=VALUE
        # KEY2=VALUE2
