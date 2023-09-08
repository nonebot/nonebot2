const lightTheme = require("daisyui/src/theming/themes")["[data-theme=light]"];
const darkTheme = require("daisyui/src/theming/themes")["[data-theme=dark]"];

/**
 * @param {{[key: string]: string}} theme
 * @param {string[]} exclude
 * @returns {{[key: string]: string}}
 */
function excludeThemeColor(theme, exclude) {
  /** @type {typeof theme} */
  const newObj = {};
  for (const key in theme) {
    if (exclude.includes(key)) continue;
    newObj[key] = theme[key];
  }
  return newObj;
}

module.exports = {
  daisyui: {
    themes: [
      {
        light: {
          ...excludeThemeColor(lightTheme, [
            "primary-content",
            "secondary-content",
            "accent-content",
          ]),
          primary: "#ea5252",
          secondary: "#ef9fbc",
          accent: "#65c3c8",
        },
      },
      {
        dark: {
          ...excludeThemeColor(darkTheme, [
            "primary-content",
            "secondary-content",
            "accent-content",
          ]),
          primary: "#ea5252",
          secondary: "#ef9fbc",
          accent: "#65c3c8",
        },
      },
    ],
  },
};
