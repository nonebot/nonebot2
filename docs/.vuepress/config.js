const path = require("path");

module.exports = context => ({
  title: "NoneBot",
  description: "基于 酷Q 的 Python 异步 QQ 机器人框架",
  markdown: {
    lineNumbers: true
  },
  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ["link", { rel: "icon", href: "/logo.png" }],
    ["link", { rel: "manifest", href: "/manifest.json" }],
    ["meta", { name: "theme-color", content: "#ea5252" }],
    ["meta", { name: "application-name", content: "NoneBot" }],
    ["meta", { name: "apple-mobile-web-app-title", content: "NoneBot" }],
    ["meta", { name: "apple-mobile-web-app-capable", content: "yes" }],
    [
      "meta",
      { name: "apple-mobile-web-app-status-bar-style", content: "black" }
    ],
    [
      "link",
      { rel: "apple-touch-icon", href: "/icons/apple-touch-icon-180x180.png" }
    ],
    [
      "link",
      {
        rel: "mask-icon",
        href: "/icons/safari-pinned-tab.svg",
        color: "#ea5252"
      }
    ],
    [
      "meta",
      {
        name: "msapplication-TileImage",
        content: "/icons/mstile-150x150.png"
      }
    ],
    ["meta", { name: "msapplication-TileColor", content: "#ea5252" }],
    [
      "link",
      {
        rel: "stylesheet",
        href:
          "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5/css/all.min.css"
      }
    ]
  ],
  locales: {
    "/": {
      lang: "zh-CN",
      title: "NoneBot",
      description: "基于 酷Q 的 Python 异步 QQ 机器人框架"
    }
  },

  theme: "nonebot",
  themeConfig: {
    logo: "/logo.png",
    repo: "nonebot/nonebot2",
    docsDir: "docs",
    docsBranch: "dev",
    docsDirVersioned: "archive",
    docsDirPages: "pages",
    editLinks: true,
    smoothScroll: true,

    locales: {
      "/": {
        label: "简体中文",
        selectText: "Languages",
        editLinkText: "在 GitHub 上编辑此页",
        lastUpdated: "上次更新",
        nav: [
          { text: "主页", link: "/" },
          { text: "指南", link: "/guide/" },
          { text: "API", link: "/api/" },
          { text: "插件广场", link: "/plugin-store" }
        ],
        sidebarDepth: 2,
        sidebar: {
          "/guide/": [
            {
              title: "开始",
              collapsable: false,
              sidebar: "auto",
              children: [
                "",
                "installation",
                "getting-started",
                "creating-a-project",
                "basic-configuration"
              ]
            },
            {
              title: "编写插件",
              collapsable: false,
              sidebar: "auto",
              children: [
                "loading-a-plugin",
                "creating-a-plugin",
                "creating-a-matcher",
                "creating-a-handler"
              ]
            }
          ],
          "/api/": [
            {
              title: "NoneBot Api Reference",
              path: "",
              collapsable: false,
              children: [
                {
                  title: "nonebot 模块",
                  path: "nonebot"
                },
                {
                  title: "nonebot.config 模块",
                  path: "config"
                },
                {
                  title: "nonebot.plugin 模块",
                  path: "plugin"
                },
                {
                  title: "nonebot.matcher 模块",
                  path: "matcher"
                },
                {
                  title: "nonebot.rule 模块",
                  path: "rule"
                },
                {
                  title: "nonebot.permission 模块",
                  path: "permission"
                },
                {
                  title: "nonebot.sched 模块",
                  path: "sched"
                },
                {
                  title: "nonebot.log 模块",
                  path: "log"
                },
                {
                  title: "nonebot.utils 模块",
                  path: "utils"
                },
                {
                  title: "nonebot.typing 模块",
                  path: "typing"
                },
                {
                  title: "nonebot.exception 模块",
                  path: "exception"
                },
                {
                  title: "nonebot.drivers 模块",
                  path: "drivers/"
                },
                {
                  title: "nonebot.drivers.fastapi 模块",
                  path: "drivers/fastapi"
                },
                {
                  title: "nonebot.adapters 模块",
                  path: "adapters/"
                },
                {
                  title: "nonebot.adapters.cqhttp 模块",
                  path: "adapters/cqhttp"
                }
              ]
            }
          ]
        }
      }
    }
  },

  plugins: [
    "@vuepress/plugin-back-to-top",
    "@vuepress/plugin-medium-zoom",
    [
      "@vuepress/pwa",
      {
        serviceWorker: true,
        updatePopup: {
          message: "发现新内容",
          buttonText: "刷新"
        }
      }
    ],
    [
      "versioning",
      {
        versionedSourceDir: path.resolve(context.sourceDir, "..", "archive"),
        pagesSourceDir: path.resolve(context.sourceDir, "..", "pages"),
        onNewVersion(version, versionDestPath) {
          console.log(`Created version ${version} in ${versionDestPath}`);
        }
      }
    ],
    [
      "container",
      {
        type: "vue",
        before: '<pre class="vue-container"><code>',
        after: "</code></pre>"
      }
    ]
  ]
});
