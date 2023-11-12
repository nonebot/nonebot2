import React from "react";

import CodeBlock from "@theme/CodeBlock";

export type Feature = {
  title: string;
  tagline?: string;
  description?: string;
  annotaion?: string;
  children?: React.ReactNode;
};

export function HomeFeature({
  title,
  tagline,
  description,
  annotaion,
  children,
}: Feature): JSX.Element {
  return (
    <div className="flex flex-col items-center justify-center p-4">
      <p className="text-sm text-base-content/70 font-medium tracking-wide uppercase">
        {tagline}
      </p>
      <h1 className="mt-3 font-mono font-light text-4xl tracking-tight sm:text-5xl md:text-5xl text-primary">
        {title}
      </h1>
      <p className="mt-10 mb-6">{description}</p>
      {children}
      <p className="text-sm italic text-base-content/70">{annotaion}</p>
    </div>
  );
}

function HomeFeatureSingleColumn(props: Feature): JSX.Element {
  return (
    <div className="grid grid-cols-1 px-4 py-8 md:px-16 mx-auto">
      <HomeFeature {...props} />
    </div>
  );
}

function HomeFeatureDoubleColumn({
  features: [feature1, feature2],
  children,
}: {
  features: [Feature, Feature];
  children?: [React.ReactNode, React.ReactNode];
}): JSX.Element {
  const [children1, children2] = children ?? [];

  return (
    <div className="grid gap-x-6 gap-y-8 grid-cols-1 lg:grid-cols-2 max-w-7xl px-4 py-8 md:px-16 mx-auto">
      <HomeFeature {...feature1}>{children1}</HomeFeature>
      <HomeFeature {...feature2}>{children2}</HomeFeature>
    </div>
  );
}

function HomeFeatures(): JSX.Element {
  return (
    <>
      <HomeFeatureSingleColumn
        title="开箱即用"
        tagline="out of box"
        description="使用 NB-CLI 快速构建属于你的机器人"
      >
        <CodeBlock
          title="Installation"
          language="bash"
          className="home-codeblock"
        >
          {[
            "$ pipx install nb-cli",
            "$ nb",
            // "d8b   db  .d88b.  d8b   db d88888b d8888b.  .d88b.  d888888b",
            // "888o  88 .8P  Y8. 888o  88 88'     88  `8D .8P  Y8. `~~88~~'",
            // "88V8o 88 88    88 88V8o 88 88ooooo 88oooY' 88    88    88",
            // "88 V8o88 88    88 88 V8o88 88~~~~~ 88~~~b. 88    88    88",
            // "88  V888 `8b  d8' 88  V888 88.     88   8D `8b  d8'    88",
            // "VP   V8P  `Y88P'  VP   V8P Y88888P Y8888P'  `Y88P'     YP",
            "[?] What do you want to do?",
            "❯ Create a NoneBot project.",
            "  Run the bot in current folder.",
            "  Manage bot driver.",
            "  Manage bot adapters.",
            "  Manage bot plugins.",
            "  ...",
          ].join("\n")}
        </CodeBlock>
      </HomeFeatureSingleColumn>
      <HomeFeatureDoubleColumn
        features={[
          {
            title: "插件系统",
            tagline: "plugin system",
            description: "插件化开发，模块化管理",
          },
          {
            title: "跨平台支持",
            tagline: "cross-platform support",
            description: "支持多种平台，以及多样的事件响应方式",
          },
        ]}
      >
        <CodeBlock title="" language="python" className="home-codeblock">
          {[
            "import nonebot",
            "# 加载一个插件",
            'nonebot.load_plugin("path.to.your.plugin")',
            "# 从文件夹加载插件",
            'nonebot.load_plugins("plugins")',
            "# 从配置文件加载多个插件",
            'nonebot.load_from_json("plugins.json")',
            'nonebot.load_from_toml("pyproject.toml")',
          ].join("\n")}
        </CodeBlock>
        <CodeBlock title="" language="python" className="home-codeblock">
          {[
            "import nonebot",
            "# OneBot",
            "from nonebot.adapters.onebot.v11 import Adapter as OneBotAdapter",
            "# QQ 机器人",
            "from nonebot.adapters.qq import Adapter as QQAdapter",
            "driver = nonebot.get_driver()",
            "driver.register_adapter(OneBotAdapter)",
            "driver.register_adapter(QQAdapter)",
          ].join("\n")}
        </CodeBlock>
      </HomeFeatureDoubleColumn>
      <HomeFeatureDoubleColumn
        features={[
          {
            title: "异步开发",
            tagline: "asynchronous first",
            description: "异步优先式开发，提高运行效率",
          },
          {
            title: "依赖注入",
            tagline: "builtin dependency injection system",
            description: "简单清晰的依赖注入系统，内置依赖函数减少用户代码",
          },
        ]}
      >
        <CodeBlock title="" language="python" className="home-codeblock">
          {[
            "from nonebot import on_message",
            "# 注册一个消息响应器",
            "matcher = on_message()",
            "# 注册一个消息处理器",
            "# 并重复收到的消息",
            "@matcher.handle()",
            "async def handler(event: Event) -> None:",
            "    await matcher.send(event.get_message())",
          ].join("\n")}
        </CodeBlock>
        <CodeBlock title="" language="python" className="home-codeblock">
          {[
            "from nonebot import on_command",
            "# 注册一个命令响应器",
            'matcher = on_command("help", alias={"帮助"})',
            "# 注册一个命令处理器",
            "# 通过依赖注入获得命令名以及参数",
            "@matcher.handle()",
            "async def handler(cmd = Command(), arg = CommandArg()) -> None:",
            "    await matcher.finish()",
          ].join("\n")}
        </CodeBlock>
      </HomeFeatureDoubleColumn>
    </>
  );
}

export default React.memo(HomeFeatures);
