import React from "react";

import clsx from "clsx";

import "./styles.css";
import { pickTextColor } from "@/libs/color";
import type { Tag } from "@/types/tag";

export type Props = Tag & {
  className?: string;
  onClick?: React.MouseEventHandler<HTMLSpanElement>;
};

export default function ResourceTag({
  label,
  color,
  className,
  onClick,
}: Props): JSX.Element {
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
