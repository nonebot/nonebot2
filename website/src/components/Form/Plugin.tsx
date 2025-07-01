import React from "react";

import Link from "@docusaurus/Link";

import { Form } from ".";

export default function PluginForm(): React.ReactNode {
  const formItems = [
    {
      name: "包信息",
      items: [
        { type: "text", name: "pypi", labelText: "PyPI 项目名" },
        { type: "text", name: "module", labelText: "插件模块名" },
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
        template: "plugin_publish.yml",
        title: `Plugin: ${result.pypi}`,
        ...result,
      })}`
    );
  };

  const description = (
    <p>
      请在发布前阅读{" "}
      <Link
        className="text-primary"
        href="https://nonebot.dev/docs/developer/plugin-publishing"
      >
        NoneBot 插件发布流程指导
      </Link>
      ，并确保满足其中所述条件。
    </p>
  );

  return (
    <Form
      type="plugin"
      formItems={formItems}
      handleSubmit={handleSubmit}
      description={description}
    />
  );
}
