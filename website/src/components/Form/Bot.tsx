import React from "react";

import { Form } from ".";

export default function BotForm(): JSX.Element {
  const formItems = [
    {
      name: "基本信息",
      items: [
        {
          type: "text",
          inputName: "name",
          labelText: "机器人名称",
        },
        { type: "text", inputName: "description", labelText: "机器人描述" },
        {
          type: "text",
          inputName: "homepage",
          labelText: "机器人项目仓库/主页链接",
        },
      ],
    },
    {
      name: "其他信息",
      items: [{ type: "tag", inputName: "tags", labelText: "标签" }],
    },
  ];
  const handleSubmit = (result: Record<string, string>) => {
    window.open(
      `https://github.com/nonebot/nonebot2/issues/new?${new URLSearchParams({
        assignees: "",
        labels: "Bot",
        projects: "",
        template: "bot_publish.yml",
        title: `Bot: ${result.name}`,
        ...result,
      })}`
    );
  };

  return <Form formItems={formItems} handleSubmit={handleSubmit} />;
}
