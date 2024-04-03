import React from "react";

import clsx from "clsx";

import Link from "@docusaurus/Link";
import type { IconName } from "@fortawesome/fontawesome-common-types";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import "./styles.css";
import Tag from "@/components/Resource/Tag";
import type { Resource } from "@/libs/store";

export type Props = {
  resource: Resource;
  onClick?: () => void;
  onTagClick: (tag: string) => void;
  onAuthorClick: () => void;
  className?: string;
};

export default function ResourceCard({
  resource,
  onClick,
  onTagClick,
  onAuthorClick,
  className,
}: Props): JSX.Element {
  const isGithub = /^https:\/\/github.com\/[^/]+\/[^/]+/.test(
    resource.homepage
  );

  const isPlugin = resource.resourceType === "plugin";

  const authorLink = `https://github.com/${resource.author}`;
  const authorAvatar = `${authorLink}.png?size=80`;

  enum ValidStatus {
    VALID = "valid",
    INVALID = "invalid",
    SKIP = "skip",
    MISSING = "missing",
  }

  const getValid = (resource: Resource) => {
    switch (resource.resourceType) {
      case "plugin":
        if (resource.skip_test) return ValidStatus.SKIP;
        if (resource.valid) return ValidStatus.VALID;
        return ValidStatus.INVALID;
      default:
        return ValidStatus.MISSING;
    }
  };

  const getRegistryLink = (resource: Resource) => {
    switch (resource.resourceType) {
      case "plugin":
        return `https://registry.nonebot.dev/plugin/${resource.project_link}:${resource.module_name}`;
      default:
        return undefined;
    }
  };

  const validIcons: {
    [key in ValidStatus]: IconName;
  } = {
    [ValidStatus.VALID]: "plug-circle-check",
    [ValidStatus.INVALID]: "plug-circle-xmark",
    [ValidStatus.SKIP]: "plug-circle-exclamation",
    [ValidStatus.MISSING]: "plug-circle-exclamation",
  };

  const validStatus = getValid(resource);
  const registryLink = getRegistryLink(resource);

  const ValidDisplay = () => {
    return validStatus !== ValidStatus.MISSING ? (
      <a target="_blank" rel="noreferrer" href={registryLink}>
        <FontAwesomeIcon
          className={clsx({
            "mr-1": true,
            "text-success": ValidStatus.VALID === validStatus,
            "text-error": ValidStatus.INVALID === validStatus,
            "text-warning": ValidStatus.SKIP === validStatus,
          })}
          icon={["fas", validIcons[validStatus]]}
        />
      </a>
    ) : null;
  };

  return (
    <div className={clsx("resource-card-container", className)}>
      <div className="resource-card-header">
        <div className="resource-card-header-title">
          <ValidDisplay />
          {resource.name}
          {resource.is_official && (
            <FontAwesomeIcon
              className="resource-card-header-check"
              icon={["fas", "circle-check"]}
            />
          )}
        </div>
        <div className="resource-card-header-expand" onClick={onClick}>
          <FontAwesomeIcon icon={["fas", "expand"]} />
        </div>
      </div>
      <div className="resource-card-desc">{resource.desc}</div>
      <div className="resource-card-footer">
        <div className="resource-card-footer-tags">
          {resource.tags.map((tag, index) => (
            <Tag
              className="resource-card-footer-tag"
              key={index}
              {...tag}
              onClick={() => onTagClick(tag.label)}
            />
          ))}
        </div>
        <div className="divider resource-card-footer-divider"></div>
        <div className="resource-card-footer-info">
          <div className="resource-card-footer-group">
            <Link href={resource.homepage}>
              {isGithub ? (
                <FontAwesomeIcon
                  className="resource-card-footer-icon"
                  icon={["fab", "github"]}
                />
              ) : (
                <FontAwesomeIcon
                  className="resource-card-footer-icon"
                  icon={["fas", "link"]}
                />
              )}
            </Link>
            {isPlugin && (
              <Link href={registryLink}>
                <FontAwesomeIcon
                  className="resource-card-footer-icon"
                  icon={["fas", "cube"]}
                />
              </Link>
            )}
          </div>
          <div className="resource-card-footer-group">
            <div className="avatar">
              <div className="resource-card-footer-avatar">
                <Link href={authorLink}>
                  <img src={authorAvatar} key={resource.author} />
                </Link>
              </div>
            </div>
            <span
              className="resource-card-footer-author"
              onClick={onAuthorClick}
            >
              {resource.author}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
