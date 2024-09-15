const lightTheme = require("daisyui/src/theming/themes")["light"];
const darkTheme = require("daisyui/src/theming/themes")["dark"];

function excludeThemeColor(
  theme: { [key: string]: string },
  exclude: string[]
): { [key: string]: string } {
  /** @type {typeof theme} */
  const newObj: { [key: string]: string } = {};
  for (const key in theme) {
    if (exclude.includes(key)) continue;
    newObj[key] = theme[key]!;
  }
  return newObj;
}

export default {
  darkMode: ["class", '[data-theme="dark"]'],
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
