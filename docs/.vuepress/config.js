module.exports = {
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

  themeConfig: {
    repo: "nonebot/nonebot",
    editLinks: true,
    editLinkText: "在 GitHub 上编辑此页",
    docsDir: "docs",
    lastUpdated: "上次更新",
    nav: [{ text: "API", link: "/api.md" }],
    sidebar: {}
  },

  plugins: ["@vuepress/plugin-back-to-top", "@vuepress/plugin-medium-zoom"]
};
