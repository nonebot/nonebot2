// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "NoneBot",
  tagline: "跨平台 Python 异步机器人框架",
  url: "https://nonebot.dev",
  baseUrl: process.env.BASE_URL || "/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "icons/favicon.ico",
  organizationName: "nonebot", // Usually your GitHub org/user name.
  projectName: "nonebot2", // Usually your repo name.
  i18n: {
    defaultLocale: "zh-Hans",
    locales: ["zh-Hans"],
    localeConfigs: {
      "zh-Hans": { label: "简体中文" },
    },
  },

  scripts: [
    {
      type: "text/javascript",
      charset: "UTF-8",
      src: "https://cdn.wwads.cn/js/makemoney.js",
      async: true,
    },
  ],

  presets: [
    [
      "docusaurus-preset-nonepress",
      /** @type {import('docusaurus-preset-nonepress').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl: "https://github.com/nonebot/nonebot2/edit/master/website/",
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
          // exclude: [
          //   "**/_*.{js,jsx,ts,tsx,md,mdx}",
          //   "**/_*/**",
          //   "**/*.test.{js,jsx,ts,tsx}",
          //   "**/__tests__/**",
          // ],
        },
        sitemap: {
          changefreq: "daily",
          priority: 0.5,
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('docusaurus-preset-nonepress').ThemeConfig} */
    ({
      colorMode: {
        defaultMode: "light",
      },
      logo: {
        alt: "",
        src: "logo.png",
        href: "/",
        target: "_self",
      },
      navbar: {
        hideOnScroll: true,
        items: [
          {
            label: "指南",
            type: "docsMenu",
            category: "tutorial",
          },
          {
            label: "深入",
            type: "docsMenu",
            category: "appendices",
          },
          {
            label: "进阶",
            type: "docsMenu",
            category: "advanced",
          },
          {
            label: "API",
            type: "docLink",
            docId: "api/index",
          },
          {
            label: "更多",
            type: "dropdown",
            to: "/store",
            items: [
              {
                label: "最佳实践",
                type: "docLink",
                docId: "best-practice/scheduler",
              },
              {
                label: "开发者",
                type: "docLink",
                docId: "developer/plugin-publishing",
              },
              { label: "社区", type: "docLink", docId: "community/contact" },
              { label: "开源之夏", type: "docLink", docId: "ospp/2023" },
              { label: "商店", to: "/store" },
              { label: "更新日志", to: "/changelog" },
              { label: "论坛", href: "https://discussions.nonebot.dev" },
            ],
          },
          {
            icon: ["fab", "github"],
            href: "https://github.com/nonebot/nonebot2",
          },
        ],
        docsVersionItemAfter: [
          {
            label: "2.0.0a16",
            href: "https://61d3d9dbcadf413fd3238e89--nonebot2.netlify.app/",
          },
          {
            label: "1.x",
            href: "https://v1.nonebot.dev/",
          },
        ],
      },
      hideableSidebar: true,
      footer: {
        copyright: `Copyright © ${new Date().getFullYear()} NoneBot. All rights reserved.`,
        iconLinks: [
          {
            icon: ["fab", "github"],
            href: "https://github.com/nonebot/nonebot2",
            description: "GitHub",
          },
          {
            icon: ["fab", "qq"],
            href: "https://jq.qq.com/?_wv=1027&k=5OFifDh",
          },
          {
            icon: ["fab", "telegram"],
            href: "https://t.me/botuniverse",
          },
          {
            icon: ["fab", "discord"],
            href: "https://discord.gg/VKtE6Gdc4h",
          },
        ],
        links: [
          {
            title: "Learn",
            icon: ["fas", "book"],
            items: [
              { label: "Introduction", to: "/docs/" },
              // { label: "QuickStart", to: "/docs/quick-start" },
              { label: "Changelog", to: "/changelog" },
            ],
          },
          {
            title: "NoneBot Team",
            icon: ["fas", "user-friends"],
            items: [
              {
                label: "Homepage",
                href: "https://nonebot.dev",
              },
              {
                label: "NoneBot V1",
                href: "https://docs.nonebot.dev",
              },
              { label: "NoneBot CLI", href: "https://cli.nonebot.dev" },
            ],
          },
          {
            title: "Related",
            icon: ["fas", "external-link-alt"],
            items: [
              { label: "OneBot", href: "https://onebot.dev/" },
              { label: "go-cqhttp", href: "https://docs.go-cqhttp.org/" },
              { label: "Mirai", href: "https://mirai.mamoe.net/" },
            ],
          },
        ],
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ["docker", "ini"],
      },
      algolia: {
        appId: "X0X5UACHZQ",
        apiKey: "ac03e1ac2bd0812e2ea38c0cc1ea38c5",
        indexName: "nonebot",
        contextualSearch: true,
      },
      tailwindConfig: require("./tailwind.config"),
      customCss: [require.resolve("./src/css/custom.css")],
    }),
};

module.exports = config;
