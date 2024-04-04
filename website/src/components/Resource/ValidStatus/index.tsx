import React from "react";

import clsx from "clsx";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { ValidStatus, validIcons, getValidStatus } from "./utils";

import { Resource } from "@/libs/store";

export type Props = {
  resource: Resource;
  validLink: string;
  className?: string;
  simple?: boolean;
};

const ValidDisplay = ({ resource, validLink, className, simple }: Props) => {
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
            "mr-1": simple,
            "bg-success/10": !simple && isValid,
            "text-success/90": isValid,
            "bg-error/10": !simple && isInvalid,
            "text-error/90": isInvalid,
            "bg-info/10": !simple && isSkip,
            "text-info/90": isSkip,
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
};

export default ValidDisplay;
