import path from "path";

import type { PluginConfig } from "@docusaurus/types";

export default (function webpackPlugin() {
  return {
    name: "webpack-plugin",
    configureWebpack() {
      return {
        resolve: {
          alias: {
            "@": path.resolve(__dirname, "../"),
          },
        },
      };
    },
  };
} satisfies PluginConfig);
