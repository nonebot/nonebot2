import React from "react";

import { Form } from ".";

export default function AdapterForm(): JSX.Element {
  const formItems = [
    {
      name: "基本信息",
      items: [
        {
          type: "text",
          name: "name",
          labelText: "适配器名称",
        },
        { type: "text", name: "description", labelText: "适配器描述" },
        {
          type: "text",
          name: "homepage",
          labelText: "适配器项目仓库/主页链接",
        },
      ],
    },
    {
      name: "包信息",
      items: [
        { type: "text", name: "pypi", labelText: "PyPI 项目名" },
        { type: "text", name: "module", labelText: "适配器 import 包名" },
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
        labels: "Adapter",
        projects: "",
        template: "adapter_publish.yml",
        title: `Adapter: ${result.name}`,
        ...result,
      })}`
    );
  };

  return (
    <Form type="adapter" formItems={formItems} handleSubmit={handleSubmit} />
  );
}
