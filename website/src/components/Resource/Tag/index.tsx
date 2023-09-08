import React from "react";

import clsx from "clsx";

import { Tag as TagType } from "../../libs/store";

function pickTextColor(bgColor, lightColor, darkColor) {
  const color = bgColor.charAt(0) === "#" ? bgColor.substring(1, 7) : bgColor;
  const r = parseInt(color.substring(0, 2), 16); // hexToR
  const g = parseInt(color.substring(2, 4), 16); // hexToG
  const b = parseInt(color.substring(4, 6), 16); // hexToB
  return r * 0.299 + g * 0.587 + b * 0.114 > 186 ? darkColor : lightColor;
}

export default function Tag({
  label,
  color,
  className,
  onClick,
}: TagType & {
  className?: string;
  onClick?: React.MouseEventHandler<HTMLSpanElement>;
}): JSX.Element {
  return (
    <span
      className={clsx(
        "font-mono inline-flex px-3 rounded-full items-center align-middle mr-2",
        className
      )}
      style={{
        backgroundColor: color,
        color: pickTextColor(color, "#fff", "#000"),
      }}
      onClick={onClick}
    >
      {label}
    </span>
  );
}
