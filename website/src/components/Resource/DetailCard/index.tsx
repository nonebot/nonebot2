import React, { useEffect, useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { PyPIData } from "./types";

import Tag from "@/components/Resource/Tag";
import type { Resource } from "@/libs/store";

import "./styles.css";

export type Props = {
  resource: Resource;
};

export default function ResourceDetailCard({ resource }: Props) {
  const [pypiData, setPypiData] = useState<PyPIData | null>(null);

  const authorLink = `https://github.com/${resource.author}`;
  const authorAvatar = `${authorLink}.png?size=100`;

  const fetchPypiProject = (projectName: string) =>
    fetch(`https://pypi.org/pypi/${projectName}/json`)
      .then((response) => response.json())
      .then((data) => setPypiData(data));

  useEffect(() => {
    const fetchingTasks: Promise<void>[] = [];
    if (resource.resourceType != "bot" && resource.project_link)
      fetchingTasks.push(fetchPypiProject(resource.project_link));

    Promise.all(fetchingTasks);
  }, [resource]);

  return (
    <>
      <div className="detail-card-header">
        <img
          src={authorAvatar}
          className="detail-card-avatar"
          decoding="async"
        ></img>
        <div className="detail-card-title">
          <span className="detail-card-title-main">{resource.name}</span>
          <span className="detail-card-title-sub">{resource.author}</span>
        </div>
        <button className="detail-card-copy-button detail-card-copy-button-desktop">
          复制安装命令
        </button>
      </div>
      <div className="detail-card-body">
        <div className="detail-card-body-left">
          <span className="h-full">{resource.desc}</span>
          <div className="mb-4">
            {resource.tags.map((tag, index) => (
              <Tag className="align-bottom" key={index} {...tag} />
            ))}
          </div>
        </div>
        <div className="detail-card-body-divider" />
        <div className="detail-card-body-right">
          <div className="detail-card-meta-item">
            <FontAwesomeIcon className="fa-fw" icon={["fas", "file-zipper"]} />{" "}
            {pypiData &&
              pypiData.releases[pypiData.info.version].reduce(
                (acc, curr) => acc + curr.size,
                0
              ) / 1000}
            K
          </div>
          <div className="detail-card-meta-item">
            <span>
              <FontAwesomeIcon
                className="fa-fw"
                icon={["fas", "scale-balanced"]}
              />{" "}
              {pypiData && (pypiData.info.license || "无")}
            </span>
          </div>
          <div className="detail-card-meta-item">
            <FontAwesomeIcon className="fa-fw" icon={["fas", "tag"]} />{" "}
            {pypiData && (pypiData.info.version || "无")}
          </div>
          {resource.resourceType === "plugin" && (
            <div className="detail-card-meta-item">
              <FontAwesomeIcon
                className="fa-fw"
                icon={["fas", "fingerprint"]}
              />{" "}
              <span>{resource.module_name || "无"}</span>
            </div>
          )}
          {resource.resourceType === "plugin" && (
            <div className="detail-card-meta-item">
              <FontAwesomeIcon className="fa-fw" icon={["fas", "cubes"]} />{" "}
              <span>{resource.project_link || "无"}</span>
            </div>
          )}
          <button className="detail-card-copy-button w-full">
            复制安装命令
          </button>
        </div>
      </div>
    </>
  );
}
