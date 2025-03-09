import React from "react";

import clsx from "clsx";

import { pickTextColor } from "@/libs/color";

import type { Tag } from "@/types/tag";


import "./styles.css";

export type Props = Tag & {
  className?: string;
  onClick?: React.MouseEventHandler<HTMLSpanElement>;
};

export default function ResourceTag({
  label,
  color,
  className,
  onClick,
}: Props): React.ReactNode {
  return (
    <span
      className={clsx("resource-tag", className)}
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
