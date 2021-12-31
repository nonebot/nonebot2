import React from "react";

import Link from "@docusaurus/Link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import type { Obj } from "../../libs/store";
import Tag from "../Tag";

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
            <Tag key={index} {...tag} />
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
