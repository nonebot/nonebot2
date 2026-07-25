import { defineConfig, globalIgnores } from "eslint/config";
import tseslint from "typescript-eslint";
import globals from "globals";
import js from "@eslint/js";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import importPlugin from "eslint-plugin-import";
// @ts-expect-error: no types provided
import jsxA11y from "eslint-plugin-jsx-a11y";
import docusaurus from "@docusaurus/eslint-plugin";
import regexp from "eslint-plugin-regexp";
import prettier from "eslint-config-prettier/flat";

import rules from "./eslint.rules";

const plugins = defineConfig([
  js.configs.recommended,
  tseslint.configs.recommended,
  react.configs.flat.recommended,
  reactHooks.configs.flat.recommended,
  importPlugin.flatConfigs.recommended,
  jsxA11y.flatConfigs.recommended,
  regexp.configs["flat/recommended"],
  prettier,

  // The published @docusaurus/eslint-plugin doesn't provide a flat config yet
  // This adapts its legacy "all" config to flat config
  {
    plugins: {
      "@docusaurus": docusaurus,
    },
    rules: docusaurus.configs.all.rules,
  },
]);

const ignores = globalIgnores([
  "**/dist/**",
  "**/lib/**",
  "**/build/**",
  "**/.docusaurus/**",
  "node_modules",
  ".yarn",
  ".history",
  "coverage",
]);

export default defineConfig(plugins, rules, ignores, {
  languageOptions: {
    ecmaVersion: 2022,
    sourceType: "module",
    globals: {
      ...globals.browser,
      ...globals.node,
      ...globals.commonjs,
      JSX: true,
    },
  },

  settings: {
    "import/resolver": {
      node: {
        extensions: [".js", ".jsx", ".ts", ".tsx"],
      },
    },
    react: {
      version: "19",
    },
  },

  linterOptions: {
    reportUnusedDisableDirectives: true,
  },
});
