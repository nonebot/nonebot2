import React from "react";

import clsx from "clsx";

import { pickTextColor } from "@/libs/color";
import { Tag as TagType } from "@/types/tag";

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
