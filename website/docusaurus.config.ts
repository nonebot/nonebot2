import type { Config } from "@docusaurus/types";
import type { Options as ChangelogOptions } from "@nullbot/docusaurus-plugin-changelog";
import type * as Preset from "@nullbot/docusaurus-preset-nonepress";
import { themes } from "prism-react-renderer";

// By default, we use Docusaurus Faster
// DOCUSAURUS_SLOWER=true is useful for benchmarking faster against slower
// hyperfine --prepare 'yarn clear:website' --runs 3 'DOCUSAURUS_SLOWER=true yarn build:website:fast' 'yarn build:website:fast'
const isSlower = process.env.DOCUSAURUS_SLOWER === "true";
if (isSlower) {
  console.log("🐢 Using slower Docusaurus build");
}

// color mode config
const colorMode: Preset.ThemeConfig["colorMode"] = {
  defaultMode: "light",
  respectPrefersColorScheme: true,
};

// navbar config
const navbar: Preset.ThemeConfig["navbar"] = {
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
        { label: "开源之夏", type: "doc", docId: "ospp/2024" },
        { label: "商店", to: "/store/plugins" },
        { label: "更新日志", to: "/changelog/" },
        { label: "论坛", href: "https://discussions.nonebot.dev" },
      ],
    },
  ],
};

// footer config
const footer: Preset.ThemeConfig["footer"] = {
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
        { label: "Changelog", to: "/changelog/" },
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
const lightCodeTheme = themes.github;
const darkCodeTheme = themes.dracula;

const prism: Preset.ThemeConfig["prism"] = {
  theme: lightCodeTheme,
  darkTheme: darkCodeTheme,
  additionalLanguages: ["docker", "ini"],
};

// algolia config
const algolia: Preset.ThemeConfig["algolia"] = {
  appId: "X0X5UACHZQ",
  apiKey: "ac03e1ac2bd0812e2ea38c0cc1ea38c5",
  indexName: "nonebot",
  contextualSearch: true,
};

// nonepress config
const nonepress: Preset.ThemeConfig["nonepress"] = {
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
const themeConfig: Preset.ThemeConfig = {
  colorMode,
  navbar,
  footer,
  prism,
  algolia,
  nonepress,
};

export default async function createConfigAsync() {
  return {
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

    headTags: [
      // 百度搜索资源平台
      // https://ziyuan.baidu.com/
      {
        tagName: "meta",
        attributes: {
          name: "baidu-site-verification",
          content: "codeva-0GTZpDnDrW",
        },
      },
    ],
    scripts: [
      // 百度统计
      // https://tongji.baidu.com/
      {
        type: "text/javascript",
        charset: "UTF-8",
        src: "https://hm.baidu.com/hm.js?875efa50097818701ee681edd63eaac6",
        async: true,
      },
      // 万维广告
      // https://wwads.cn/
      {
        type: "text/javascript",
        charset: "UTF-8",
        src: "https://cdn.wwads.cn/js/makemoney.js",
        async: true,
      },
      // uwu logo
      {
        type: "text/javascript",
        charset: "UTF-8",
        src: "/uwu.js",
      },
    ],

    presets: [
      [
        "@nullbot/docusaurus-preset-nonepress",
        /** @type {import('@nullbot/docusaurus-preset-nonepress').Options} */
        {
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
        },
      ],
    ],

    future: {
      experimental_faster: true,
    },

    plugins: [
      require("./src/plugins/webpack-plugin.ts"),
      [
        "@nullbot/docusaurus-plugin-changelog",
        {
          changelogPath: "src/changelog/changelog.md",
          changelogHeader: `description: Changelog
toc_max_heading_level: 2
sidebar_custom_props:
  sidebar_id: changelog
  sidebar_version: current`,
        } satisfies ChangelogOptions,
      ],
    ],

    markdown: {
      mdx1Compat: {
        headingIds: true,
      },
    },

    themeConfig,
  } satisfies Config;
}
