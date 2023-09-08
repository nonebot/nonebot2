import React, { useRef, useState } from "react";

import clsx from "clsx";

import { ChromePicker } from "react-color";
import { usePagination } from "react-use-pagination";

import plugins from "../../../static/plugins.json";
import { Tag, useFilteredObjs } from "../../libs/store";
import Card from "../Card/index";
import Modal from "../Modal/index";
import ModalAction from "../ModalAction/index";
import ModalContent from "../ModalContent/index";
import ModalTitle from "../ModalTitle/index";
import Paginate from "../Paginate/index";
import TagComponent from "../Tag/index";

export default function Plugin(): JSX.Element {
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const {
    filter,
    setFilter,
    filteredObjs: filteredPlugins,
  } = useFilteredObjs(plugins);

  const props = usePagination({
    totalItems: filteredPlugins.length,
    initialPageSize: 10,
  });
  const { startIndex, endIndex } = props;
  const currentPlugins = filteredPlugins.slice(startIndex, endIndex + 1);

  const [form, setForm] = useState<{
    projectLink: string;
    moduleName: string;
  }>({ projectLink: "", moduleName: "" });

  const ref = useRef<HTMLInputElement>(null);
  const [tags, setTags] = useState<Tag[]>([]);
  const [label, setLabel] = useState<string>("");
  const [color, setColor] = useState<string>("#ea5252");

  const urlEncode = (str: string) =>
    encodeURIComponent(str).replace(/%2B/gi, "+");

  const onSubmit = () => {
    setModalOpen(false);
    const queries: { key: string; value: string }[] = [
      { key: "template", value: "plugin_publish.yml" },
      {
        key: "title",
        value: form.projectLink && `Plugin: ${form.projectLink}`,
      },
      { key: "labels", value: "Plugin" },
      { key: "pypi", value: form.projectLink },
      { key: "module", value: form.moduleName },
      { key: "tags", value: JSON.stringify(tags) },
    ];
    const urlQueries = queries
      .filter((query) => !!query.value)
      .map((query) => `${query.key}=${urlEncode(query.value)}`)
      .join("&");
    window.open(`https://github.com/nonebot/nonebot2/issues/new?${urlQueries}`);
  };
  const onChange = (event) => {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;

    setForm({
      ...form,
      [name]: value,
    });
    event.preventDefault();
  };
  const onChangeLabel = (event) => {
    setLabel(event.target.value);
  };
  const onChangeColor = (color) => {
    setColor(color.hex);
  };
  const validateTag = () => {
    return label.length >= 1 && label.length <= 10;
  };
  const newTag = () => {
    if (tags.length >= 3) {
      return;
    }
    if (validateTag()) {
      const tag = { label, color };
      setTags([...tags, tag]);
    }
  };
  const delTag = (index: number) => {
    setTags(tags.filter((_, i) => i !== index));
  };

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 px-4">
        <input
          className="w-full px-4 py-2 border rounded-full bg-light-nonepress-100 dark:bg-dark-nonepress-100"
          value={filter}
          placeholder="搜索插件"
          onChange={(event) => setFilter(event.target.value)}
        />
        <button
          className="w-full rounded-lg bg-hero text-white"
          onClick={() => setModalOpen(true)}
        >
          发布插件
        </button>
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 px-4">
        {currentPlugins.map((plugin, index) => (
          <Card
            key={index}
            {...plugin}
            action={`nb plugin install ${plugin.project_link}`}
            actionDisabled={!plugin.project_link}
          />
        ))}
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <Modal active={modalOpen} setActive={setModalOpen}>
        <ModalTitle title={"插件信息"} />
        <ModalContent>
          <form onSubmit={onSubmit}>
            <div className="grid grid-cols-1 gap-4 p-4">
              <label className="flex flex-wrap">
                <span className="mr-2">PyPI 项目名:</span>
                <input
                  type="text"
                  name="projectLink"
                  className="px-2 flex-grow rounded bg-light-nonepress-200 dark:bg-dark-nonepress-200"
                  onChange={onChange}
                />
              </label>
              <label className="flex flex-wrap">
                <span className="mr-2">import 包名:</span>
                <input
                  type="text"
                  name="moduleName"
                  className="px-2 flex-grow rounded bg-light-nonepress-200 dark:bg-dark-nonepress-200"
                  onChange={onChange}
                />
              </label>
            </div>
          </form>
          <div className="px-4">
            <label className="flex flex-wrap">
              <span className="mr-2">标签:</span>
              {tags.map((tag, index) => (
                <TagComponent
                  key={index}
                  {...tag}
                  className="cursor-pointer"
                  onClick={() => delTag(index)}
                />
              ))}
            </label>
          </div>
          <div className="px-4 pt-4">
            <input
              ref={ref}
              type="text"
              className="px-2 flex-grow rounded bg-light-nonepress-200 dark:bg-dark-nonepress-200"
              onChange={onChangeLabel}
            />
            <ChromePicker
              className="mt-2"
              color={color}
              disableAlpha={true}
              onChangeComplete={onChangeColor}
            />

            <div className="flex mt-2">
              <TagComponent label={label} color={color} />
              <button
                className={clsx(
                  "px-2 h-9 min-w-[64px] rounded text-hero hover:bg-hero hover:bg-opacity-[.08]",
                  { "pointer-events-none opacity-60": !validateTag() }
                )}
                onClick={newTag}
              >
                添加标签
              </button>
            </div>
          </div>
        </ModalContent>
        <ModalAction>
          <button
            className="px-2 h-9 min-w-[64px] rounded text-hero hover:bg-hero hover:bg-opacity-[.08]"
            onClick={() => setModalOpen(false)}
          >
            关闭
          </button>
          <button
            className="ml-2 px-2 h-9 min-w-[64px] rounded text-hero hover:bg-hero hover:bg-opacity-[.08]"
            onClick={onSubmit}
          >
            发布
          </button>
        </ModalAction>
      </Modal>
    </>
  );
}
