import clsx from "clsx";
import React from "react";

import Link from "@docusaurus/Link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import type { Obj, Tag as TagType } from "../../libs/store";

function pickTextColor(bgColor, lightColor, darkColor) {
  var color = bgColor.charAt(0) === "#" ? bgColor.substring(1, 7) : bgColor;
  var r = parseInt(color.substring(0, 2), 16); // hexToR
  var g = parseInt(color.substring(2, 4), 16); // hexToG
  var b = parseInt(color.substring(4, 6), 16); // hexToB
  return r * 0.299 + g * 0.587 + b * 0.114 > 186 ? darkColor : lightColor;
}

export function Tag({
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
        "inline-flex px-3 rounded-full items-center align-middle mr-2",
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

export default function Card({
  module_name,
  name,
  desc,
  author,
  homepage,
  tags,
  is_official,
}: Obj): JSX.Element {
  const isGithub = /^https:\/\/github.com\/[^/]+\/[^/]+/.test(homepage);

  return (
    <div className="block max-w-full px-4 border-2 rounded-lg outline-none no-underline bg-light-nonepress-100 dark:bg-dark-nonepress-100 border-light-nonepress-200 dark:border-dark-nonepress-200 shadow-md shadow-light-nonepress-300 dark:shadow-dark-nonepress-300">
      <div className="flex justify-between pt-4 text-lg font-medium">
        <span>
          {name}
          {is_official && (
            <FontAwesomeIcon
              icon={["fas", "check-circle"]}
              className="text-green-600 ml-2"
            />
          )}
        </span>
        {homepage && (
          <Link
            href={homepage}
            className="text-black dark:text-white opacity-60 hover:text-hero hover:opacity-100"
          >
            {isGithub ? (
              <FontAwesomeIcon icon={["fab", "github"]} />
            ) : (
              <FontAwesomeIcon icon={["fas", "link"]} />
            )}
          </Link>
        )}
      </div>
      {tags && (
        <div className="pt-2 pb-4">
          {tags.map((tag, index) => (
            <span
              key={index}
              className="inline-flex px-3 rounded-full items-center align-middle mr-2"
              style={{
                backgroundColor: tag.color,
                color: pickTextColor(tag.color, "#fff", "#000"),
              }}
            >
              {tag.label}
            </span>
          ))}
        </div>
      )}
      {desc && (
        <div className="pb-4 text-sm font-normal opacity-60">{desc}</div>
      )}
      {module_name && (
        <div className="my-2 text-sm font-normal opacity-60 font-mono">
          <FontAwesomeIcon icon={["fas", "fingerprint"]} className="mr-2" />
          {module_name}
        </div>
      )}
      {author && (
        <div className="my-2 text-sm font-normal opacity-60 font-mono">
          <FontAwesomeIcon icon={["fas", "user"]} className="mr-2" />
          {author}
        </div>
      )}
    </div>
  );
}
