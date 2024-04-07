import React, { useEffect, useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// @ts-expect-error: we need to make package have type: module
import copy from "copy-text-to-clipboard";

import { PyPIData } from "./types";

import Tag from "@/components/Resource/Tag";
import ValidStatus from "@/components/Resource/ValidStatus";
import type { Resource } from "@/libs/store";

import "./styles.css";

export type Props = {
  resource: Resource;
};

export default function ResourceDetailCard({ resource }: Props) {
  const [pypiData, setPypiData] = useState<PyPIData | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const authorLink = `https://github.com/${resource.author}`;
  const authorAvatar = `${authorLink}.png?size=100`;

  const isPlugin = resource.resourceType === "plugin";
  const registryLink =
    isPlugin &&
    `https://registry.nonebot.dev/plugin/${resource.project_link}:${resource.module_name}`;

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
        return `https://pypi.org/project/${resource.project_link}`;
      default:
        return null;
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

  return (
    <>
      <div className="detail-card-header">
        <img
          src={authorAvatar}
          className="detail-card-avatar"
          decoding="async"
        />
        <div className="detail-card-title">
          <span className="detail-card-title-main flex items-center gap-x-1">
            {resource.name}
            {resource.is_official && (
              <div className="rounded-md text-sm bg-green-400/10 text-green-600 px-1 py-0.5">
                官方
              </div>
            )}
          </span>
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
          <ValidStatus
            resource={resource}
            validLink={registryLink as string}
            className="detail-card-actions-desktop"
          />
          <button
            className="detail-card-actions-button detail-card-actions-desktop w-28"
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
              className={homepageLink && "hover:underline hover:text-primary"}
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
                pypiProjectLink && "hover:underline hover:text-primary"
              }
            >
              {projectLink}
            </a>
          </div>
          <div className="detail-card-actions">
            <ValidStatus
              resource={resource}
              validLink={registryLink as string}
              className="detail-card-actions-mobile"
            />
            <button
              className="detail-card-actions detail-card-actions-button detail-card-actions-mobile w-28"
              onClick={() => copyCommand(resource)}
            >
              {copied ? "复制成功" : "复制安装命令"}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
