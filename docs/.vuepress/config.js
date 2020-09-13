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
    ["meta", { name: "theme-color", content: "#d32f2f" }],
    ["meta", { name: "application-name", content: "NoneBot" }],
    ["meta", { name: "apple-mobile-web-app-title", content: "NoneBot" }],
    ["meta", { name: "apple-mobile-web-app-capable", content: "yes" }],
    [
      "meta",
      { name: "apple-mobile-web-app-status-bar-style", content: "black" }
    ]
  ],
  locales: {
    "/": {
      lang: "zh-CN",
      title: "NoneBot",
      description: "基于 酷Q 的 Python 异步 QQ 机器人框架"
    }
  },

  theme: "titanium",
  themeConfig: {
    logo: "/logo.png",
    repo: "nonebot/nonebot",
    docsDir: "docs",
    docsBranch: "dev2",
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
          { text: "API", link: "/api/" }
        ],
        sidebar: {
          "/guide/": [
            {
              title: "指南",
              path: "",
              collapsable: false,
              sidebar: "auto",
              children: ["", "installation"]
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
                  title: "nonebot.typing 模块",
                  path: "typing"
                },
                {
                  title: "nonebot.config 模块",
                  path: "config"
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
                  title: "nonebot.rule 模块",
                  path: "rule"
                },
                {
                  title: "nonebot.utils 模块",
                  path: "utils"
                },
                {
                  title: "nonebot.exception 模块",
                  path: "exception"
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
      "versioning",
      {
        versionedSourceDir: path.resolve(context.sourceDir, "..", "archive"),
        pagesSourceDir: path.resolve(context.sourceDir, "..", "pages"),
        onNewVersion(version, versionDestPath) {
          console.log(`Created version ${version} in ${versionDestPath}`);
        }
      }
    ]
  ]
});
