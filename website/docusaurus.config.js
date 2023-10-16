// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

// color mode config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["colorMode"]} */
const colorMode = {
  defaultMode: "light",
  respectPrefersColorScheme: true,
};

// navbar config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["navbar"]} */
const navbar = {
  title: "NoneBot",
  logo: {
    alt: "NoneBot",
    src: "logo.png",
    href: "/",
    target: "_self",
    height: 32,
    width: 32,
  },
  hideOnScroll: false,
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
      type: "doc",
      docId: "api/index",
    },
    {
      label: "更多",
      type: "dropdown",
      to: "/store/plugins",
      items: [
        {
          label: "最佳实践",
          type: "doc",
          docId: "best-practice/scheduler",
        },
        {
          label: "开发者",
          type: "doc",
          docId: "developer/plugin-publishing",
        },
        { label: "社区", type: "doc", docId: "community/contact" },
        { label: "开源之夏", type: "doc", docId: "ospp/2023" },
        { label: "商店", to: "/store/plugins" },
        { label: "更新日志", to: "/changelog" },
        { label: "论坛", href: "https://discussions.nonebot.dev" },
      ],
    },
  ],
};

// footer config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["footer"]} */
const footer = {
  style: "light",
  logo: {
    alt: "NoneBot",
    src: "logo.png",
    href: "/",
    target: "_self",
    height: 32,
    width: 32,
  },
  copyright: `Copyright © ${new Date().getFullYear()} NoneBot. All rights reserved.`,
  links: [
    {
      title: "Learn",
      items: [
        { label: "Introduction", to: "/docs/" },
        { label: "QuickStart", to: "/docs/quick-start" },
        { label: "Changelog", to: "/changelog" },
      ],
    },
    {
      title: "NoneBot Team",
      items: [
        {
          label: "Homepage",
          href: "https://nonebot.dev",
        },
        {
          label: "NoneBot V1",
          href: "https://v1.nonebot.dev",
        },
        { label: "NoneBot CLI", href: "https://cli.nonebot.dev" },
      ],
    },
    {
      title: "Related",
      items: [
        { label: "OneBot", href: "https://onebot.dev/" },
        { label: "go-cqhttp", href: "https://docs.go-cqhttp.org/" },
        { label: "Mirai", href: "https://mirai.mamoe.net/" },
      ],
    },
  ],
};

// prism config
/** @type {import('prism-react-renderer').PrismTheme} */
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line import/order
const lightCodeTheme = require("prism-react-renderer/themes/github");
/** @type {import('prism-react-renderer').PrismTheme} */
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line import/order
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["prism"]} */
const prism = {
  theme: lightCodeTheme,
  darkTheme: darkCodeTheme,
  additionalLanguages: ["docker", "ini"],
};

// algolia config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["algolia"]} */
const algolia = {
  appId: "X0X5UACHZQ",
  apiKey: "ac03e1ac2bd0812e2ea38c0cc1ea38c5",
  indexName: "nonebot",
  contextualSearch: true,
};

// nonepress config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig["nonepress"]} */
const nonepress = {
  tailwindConfig: require("./tailwind.config"),
  navbar: {
    docsVersionDropdown: {
      dropdownItemsAfter: [
        {
          label: "1.x",
          href: "https://v1.nonebot.dev/",
        },
      ],
    },
    socialLinks: [
      {
        icon: ["fab", "github"],
        href: "https://github.com/nonebot/nonebot2",
      },
    ],
  },
  footer: {
    socialLinks: [
      {
        icon: ["fab", "github"],
        href: "https://github.com/nonebot/nonebot2",
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
  },
};

// theme config
/** @type {import('@nullbot/docusaurus-preset-nonepress').ThemeConfig} */
const themeConfig = {
  colorMode,
  navbar,
  footer,
  prism,
  algolia,
  nonepress,
};

/** @type {import('@docusaurus/types').Config} */
const siteConfig = {
  title: "NoneBot",
  tagline: "跨平台 Python 异步机器人框架",
  favicon: "icons/favicon.ico",

  // Set the production url of your site here
  url: "https://nonebot.dev",
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: process.env.BASE_URL || "/",

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "nonebot", // Usually your GitHub org/user name.
  projectName: "nonebot2", // Usually your repo name.

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "zh-Hans",
    locales: ["zh-Hans"],
  },

  scripts: [
    {
      type: "text/javascript",
      charset: "UTF-8",
      src: "https://hm.baidu.com/hm.js?875efa50097818701ee681edd63eaac6",
      async: true,
    },
    {
      type: "text/javascript",
      charset: "UTF-8",
      src: "https://cdn.wwads.cn/js/makemoney.js",
      async: true,
    },
  ],

  presets: [
    [
      "@nullbot/docusaurus-preset-nonepress",
      /** @type {import('@nullbot/docusaurus-preset-nonepress').Options} */
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
          // async sidebarItemsGenerator({
          //   isCategoryIndex: defaultCategoryIndexMatcher,
          //   defaultSidebarItemsGenerator,
          //   ...args
          // }) {
          //   return defaultSidebarItemsGenerator({
          //     ...args,
          //     isCategoryIndex(doc) {
          //       // disable category index convention for generated API docs
          //       if (
          //         doc.directories.length > 0 &&
          //         doc.directories.at(-1) === "api"
          //       ) {
          //         return false;
          //       }
          //       return defaultCategoryIndexMatcher(doc);
          //     },
          //   });
          // },
        },
        // theme: {
        //   customCss: require.resolve("./src/css/custom.css"),
        // },
        sitemap: {
          changefreq: "daily",
          priority: 0.5,
        },
        gtag: {
          trackingID: "G-MRS1GMZG0F",
        },
      }),
    ],
  ],
  plugins: [require("./src/plugins/webpack-plugin.cjs")],

  themeConfig,
};

module.exports = siteConfig;
