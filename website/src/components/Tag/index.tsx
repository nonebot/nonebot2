import React from "react";

import clsx from "clsx";

import "./styles.css";

import { pickTextColor } from "@/libs/color";

import type { Tag as TagType } from "@/types/tag";

export default function Tag({
  label,
  color,
  className,
  onClick,
}: TagType & {
  className?: string;
  onClick?: React.MouseEventHandler<HTMLSpanElement>;
}): React.ReactNode {
  return (
    <span
      className={clsx("tag", className)}
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
