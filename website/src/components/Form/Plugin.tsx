import React from "react";

import { Form } from ".";

export default function PluginForm(): JSX.Element {
  const formItems = [
    {
      name: "包信息",
      items: [
        { type: "text", name: "pypi", labelText: "PyPI 项目名" },
        { type: "text", name: "module", labelText: "插件 import 包名" },
      ],
    },
    {
      name: "其他信息",
      items: [{ type: "tag", name: "tags", labelText: "标签" }],
    },
  ];
  const handleSubmit = (result: Record<string, string>) => {
    window.open(
      `https://github.com/nonebot/nonebot2/issues/new?${new URLSearchParams({
        assignees: "",
        labels: "Plugin",
        projects: "",
        template: "plugin_publish.yml",
        title: `Plugin: ${result.pypi}`,
        ...result,
      })}`
    );
  };

  return (
    <Form type="plugin" formItems={formItems} handleSubmit={handleSubmit} />
  );
}
