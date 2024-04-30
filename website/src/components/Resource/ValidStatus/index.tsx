import React from "react";

import clsx from "clsx";

import type { IconName } from "@fortawesome/fontawesome-common-types";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { Resource } from "@/libs/store";
import { ValidStatus } from "@/libs/valid";

export const getValidStatus = (resource: Resource) => {
  switch (resource.resourceType) {
    case "plugin":
      if (resource.skip_test) return ValidStatus.SKIP;
      if (resource.valid) return ValidStatus.VALID;
      return ValidStatus.INVALID;
    default:
      return ValidStatus.MISSING;
  }
};

export const validIcons: {
  [key in ValidStatus]: IconName;
} = {
  [ValidStatus.VALID]: "plug-circle-check",
  [ValidStatus.INVALID]: "plug-circle-xmark",
  [ValidStatus.SKIP]: "plug-circle-exclamation",
  [ValidStatus.MISSING]: "plug-circle-exclamation",
};

export type Props = {
  resource: Resource;
  validLink: string;
  className?: string;
  simple?: boolean;
};

export default function ValidDisplay({
  resource,
  validLink,
  className,
  simple,
}: Props) {
  const validStatus = getValidStatus(resource);

  const isValid = validStatus === ValidStatus.VALID;
  const isInvalid = validStatus === ValidStatus.INVALID;
  const isSkip = validStatus === ValidStatus.SKIP;

  return (
    validStatus !== ValidStatus.MISSING && (
      <a
        target="_blank"
        rel="noreferrer"
        href={validLink}
        className={className}
      >
        <div
          className={clsx({
            "rounded-md text-sm flex items-center gap-x-1 px-2 py-1 whitespace-nowrap":
              !simple,
            "bg-green-400/10": !simple && isValid,
            "text-green-600 dark:text-green-400": isValid,
            "bg-red-400/10": !simple && isInvalid,
            "text-red-600 dark:text-red-400": isInvalid,
            "bg-blue-400/10": !simple && isSkip,
            "text-blue-600 dark:text-blue-400": isSkip,
          })}
        >
          <FontAwesomeIcon icon={validIcons[validStatus]} />
          {!simple && (
            <>
              {isValid && <p>插件已通过测试</p>}
              {isInvalid && <p>插件未通过测试</p>}
              {isSkip && <p>插件跳过测试</p>}
            </>
          )}
        </div>
      </a>
    )
  );
}
