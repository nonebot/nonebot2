import React, { useEffect, useState } from "react";

import { clsx } from "clsx";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// @ts-expect-error: we need to make package have type: module
import copy from "copy-text-to-clipboard";

import { PyPIData } from "./types";

import Tag from "@/components/Resource/Tag";
import type { Resource } from "@/libs/store";
import { getValidStatus, validIcons, ValidStatus } from "@/libs/valid";

import "./styles.css";

export type Props = {
  resource: Resource;
};

export default function ResourceDetailCard({ resource }: Props) {
  const [pypiData, setPypiData] = useState<PyPIData | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const authorLink = `https://github.com/${resource.author}`;
  const authorAvatar = `${authorLink}.png?size=100`;

  const getProjectLink = (resource: Resource) => {
    switch (resource.resourceType) {
      case "plugin":
      case "adapter":
      case "driver":
        return resource.project_link;
      default:
        return null;
    }
  };

  const getModuleName = (resource: Resource) => {
    switch (resource.resourceType) {
      case "plugin":
      case "adapter":
        return resource.module_name;
      case "driver":
        return resource.module_name.replace(/~/, "nonebot.drivers.");
      default:
        return null;
    }
  };

  const getHomepageLink = (resource: Resource) => {
    switch (resource.resourceType) {
      case "plugin":
      case "adapter":
      case "driver":
        return resource.homepage;
      default:
        return null;
    }
  };

  const getPypiProjectLink = (resource: Resource) => {
    switch (resource.resourceType) {
      case "plugin":
      case "adapter":
      case "driver":
        return `https://pypi.org/project/${resource.project_link}`;
      default:
        return null;
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

  const fetchPypiProject = (projectName: string) =>
    fetch(`https://pypi.org/pypi/${projectName}/json`)
      .then((response) => response.json())
      .then((data) => setPypiData(data));

  const copyCommand = (resource: Resource) => {
    const projectLink = getProjectLink(resource);
    if (projectLink) {
      copy(`nb ${resource.resourceType} install ${projectLink}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  useEffect(() => {
    const fetchingTasks: Promise<void>[] = [];
    if (resource.resourceType === "bot" || resource.resourceType === "driver")
      return;

    if (resource.project_link)
      fetchingTasks.push(fetchPypiProject(resource.project_link));

    Promise.all(fetchingTasks);
  }, [resource]);

  const projectLink = getProjectLink(resource) || "无";
  const moduleName = getModuleName(resource) || "无";
  const homepageLink = getHomepageLink(resource) || undefined;
  const pypiProjectLink = getPypiProjectLink(resource) || undefined;
  const registryLink = getRegistryLink(resource);

  const validStatus = getValidStatus(resource);

  const ValidDisplay = () => {
    return validStatus !== ValidStatus.MISSING ? (
      <a target="_blank" rel="noreferrer" href={registryLink}>
        <div
          className={clsx({
            "rounded-md text-sm flex items-center gap-x-1 px-2 py-1": true,
            "bg-success/10 text-success/90": ValidStatus.VALID === validStatus,
            "bg-error/10 text-error/90": ValidStatus.INVALID === validStatus,
            "bg-info/10 text-info/90": ValidStatus.SKIP === validStatus,
          })}
        >
          <FontAwesomeIcon icon={validIcons[validStatus]} />
          {
            {
              [ValidStatus.VALID]: <p>插件已通过测试</p>,
              [ValidStatus.INVALID]: <p>插件未通过测试</p>,
              [ValidStatus.SKIP]: <p>插件跳过测试</p>,
            }[validStatus]
          }
        </div>
      </a>
    ) : null;
  };

  return (
    <>
      <div className="detail-card-header">
        <img
          src={authorAvatar}
          className="detail-card-avatar"
          decoding="async"
        />
        <div className="detail-card-title">
          <span className="detail-card-title-main">{resource.name}</span>
          <a
            className="detail-card-title-sub hover:underline hover:text-primary"
            target="_blank"
            rel="noreferrer"
            href={authorLink}
          >
            {resource.author}
          </a>
        </div>
        <div className="detail-card-actions">
          <ValidDisplay />
          <button
            className="detail-card-actions-button detail-card-actions-button-desktop w-28"
            onClick={() => copyCommand(resource)}
          >
            {copied ? "复制成功" : "复制安装命令"}
          </button>
        </div>
      </div>
      <div className="divider detail-card-header-divider"></div>
      <div className="detail-card-body">
        <div className="detail-card-body-left">
          <span className="h-full">{resource.desc}</span>
          <div className="resource-card-footer-tags mb-4">
            {resource.tags.map((tag, index) => (
              <Tag className="align-bottom" key={index} {...tag} />
            ))}
          </div>
        </div>
        <div className="detail-card-body-divider" />
        <div className="detail-card-body-right">
          <div className="detail-card-meta-item">
            <span>
              <FontAwesomeIcon fixedWidth icon={["fab", "python"]} />{" "}
              {(pypiData && pypiData.info.requires_python) || "无"}
            </span>
          </div>
          <div className="detail-card-meta-item">
            <FontAwesomeIcon fixedWidth icon={["fas", "file-zipper"]} />{" "}
            {(pypiData &&
              pypiData.releases[pypiData.info.version] &&
              `${
                pypiData.releases[pypiData.info.version].reduce(
                  (acc, curr) => acc + curr.size,
                  0
                ) / 1000
              }K`) ||
              "无"}
          </div>
          <div className="detail-card-meta-item">
            <span>
              <FontAwesomeIcon fixedWidth icon={["fas", "scale-balanced"]} />{" "}
              {(pypiData && pypiData.info.license) || "无"}
            </span>
          </div>
          <div className="detail-card-meta-item">
            <FontAwesomeIcon fixedWidth icon={["fas", "tag"]} />{" "}
            {(pypiData && pypiData.info.version) || "无"}
          </div>

          <div className="detail-card-meta-item">
            <FontAwesomeIcon fixedWidth icon={["fas", "fingerprint"]} />{" "}
            <a
              href={homepageLink}
              target="_blank"
              rel="noreferrer"
              className={
                homepageLink ? "hover:underline hover:text-primary" : undefined
              }
            >
              {moduleName}
            </a>
          </div>

          <div className="detail-card-meta-item">
            <FontAwesomeIcon fixedWidth icon={["fas", "cubes"]} />{" "}
            <a
              href={pypiProjectLink}
              target="_blank"
              rel="noreferrer"
              className={
                pypiProjectLink
                  ? "hover:underline hover:text-primary"
                  : undefined
              }
            >
              {projectLink}
            </a>
          </div>
          <button
            className="detail-card-actions detail-card-actions-button detail-card-actions-button-mobile w-full"
            onClick={() => copyCommand(resource)}
          >
            {copied ? "复制成功" : "复制安装命令"}
          </button>
        </div>
      </div>
    </>
  );
}
