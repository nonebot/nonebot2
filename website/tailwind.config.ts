import typography from "@tailwindcss/typography";
import daisyui from "daisyui";
import themes from "daisyui/src/theming/themes";

const lightTheme = themes.light;
const darkTheme = themes.dark;

function excludeThemeColor(
  theme: { [key: string]: string },
  exclude: string[]
): { [key: string]: string } {
  const newObj: { [key: string]: string } = {};
  for (const key in theme) {
    if (exclude.includes(key)) continue;
    newObj[key] = theme[key]!;
  }
  return newObj;
}

export default {
  plugins: [typography, daisyui],
  daisyui: {
    base: false,
    themes: [
      {
        light: {
          ...excludeThemeColor(lightTheme, [
            "primary-content",
            "secondary-content",
            "accent-content",
          ]),
          primary: "#ea5252",
          "primary-content": "#ffffff",
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
          "primary-content": "#ffffff",
          secondary: "#ef9fbc",
          accent: "#65c3c8",
        },
      },
    ],
    darkTheme: false,
  },
  darkMode: ["class", '[data-theme="dark"]'],
};
