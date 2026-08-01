module.exports = {
  extends: ["stylelint-config-standard"],
  rules: {
    "selector-pseudo-class-no-unknown": [
      true,
      {
        // :global is a CSS modules feature to escape from class name hashing
        ignorePseudoClasses: ["global"],
      },
    ],
    "custom-property-empty-line-before": null,
    "selector-id-pattern": null,
    "declaration-empty-line-before": null,
    "comment-empty-line-before": null,
    "value-keyword-case": ["lower", { camelCaseSvgKeywords: true }],
  },
  overrides: [
    {
      files: ["*.css"],
      rules: {
        "function-no-unknown": [true, { ignoreFunctions: ["theme"] }],
        // Tailwind's screen() function in media queries
        "media-query-no-invalid": [true, { ignoreFunctions: ["screen"] }],
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
    // Must come after "*.css" so the camelCase pattern wins for CSS modules
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
