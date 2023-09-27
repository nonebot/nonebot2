module.exports = {
  extends: ["stylelint-config-standard", "stylelint-prettier/recommended"],
  overrides: [
    {
      files: ["*.css"],
      rules: {
        "function-no-unknown": [true, { ignoreFunctions: ["theme"] }],
        "selector-class-pattern": [
          "^([a-z][a-z0-9]*)(-[a-z0-9]+)*$",
          {
            resolveNestedSelectors: true,
            message: (selector) =>
              `Expected class selector "${selector}" to be kebab-case`,
          },
        ],
      },
    },
    {
      files: ["*.module.css"],
      rules: {
        "selector-class-pattern": [
          "^[a-z][a-zA-Z0-9]+$",
          {
            message: (selector) =>
              `Expected class selector "${selector}" to be lowerCamelCase`,
          },
        ],
      },
    },
  ],
};
