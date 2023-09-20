// @ts-check

const path = require("path");

/**
 * @returns {import('@docusaurus/types').Plugin}
 */
function webpackPlugin() {
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
}

module.exports = webpackPlugin;
