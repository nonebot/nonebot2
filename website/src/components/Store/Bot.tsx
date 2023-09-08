import React, { useRef, useState } from "react";

import clsx from "clsx";

import { ChromePicker } from "react-color";
import { usePagination } from "react-use-pagination";

import bots from "../../static/bots.json";
import { Tag, useFilteredObjs } from "../libs/store";

import Card from "./Card";
import Modal from "./Modal";
import ModalAction from "./ModalAction";
import ModalContent from "./ModalContent";
import ModalTitle from "./ModalTitle";
import Paginate from "./Paginate";
import TagComponent from "./Tag";

export default function Bot(): JSX.Element {
  const [modalOpen, setModalOpen] = useState<boolean>(false);
  const {
    filter,
    setFilter,
    filteredObjs: filteredBots,
  } = useFilteredObjs(bots);

  const props = usePagination({
    totalItems: filteredBots.length,
    initialPageSize: 10,
  });
  const { startIndex, endIndex } = props;
  const currentBots = filteredBots.slice(startIndex, endIndex + 1);

  const [form, setForm] = useState<{
    name: string;
    desc: string;
    homepage: string;
  }>({ name: "", desc: "", homepage: "" });

  const ref = useRef<HTMLInputElement>(null);
  const [tags, setTags] = useState<Tag[]>([]);
  const [label, setLabel] = useState<string>("");
  const [color, setColor] = useState<string>("#ea5252");

  const urlEncode = (str: string) =>
    encodeURIComponent(str).replace(/%2B/gi, "+");

  const onSubmit = () => {
    setModalOpen(false);
    const queries: { key: string; value: string }[] = [
      { key: "template", value: "bot_publish.yml" },
      { key: "title", value: form.name && `Bot: ${form.name}` },
      { key: "labels", value: "Bot" },
      { key: "name", value: form.name },
      { key: "description", value: form.desc },
      { key: "homepage", value: form.homepage },
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
  const insertTagType = (text: string) => {
    setLabel(text + label);
    ref.current.value = text + label;
  };

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 px-4">
        <input
          className="w-full px-4 py-2 border rounded-full bg-light-nonepress-100 dark:bg-dark-nonepress-100"
          value={filter}
          placeholder="搜索机器人"
          onChange={(event) => setFilter(event.target.value)}
        />
        <button
          className="w-full rounded-lg bg-hero text-white"
          onClick={() => setModalOpen(true)}
        >
          发布机器人
        </button>
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 px-4">
        {currentBots.map((bot, index) => (
          <Card key={index} {...bot} />
        ))}
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <Modal active={modalOpen} setActive={setModalOpen}>
        <ModalTitle title={"机器人信息"} />
        <ModalContent>
          <form onSubmit={onSubmit}>
            <div className="grid grid-cols-1 gap-4 p-4">
              <label className="flex flex-wrap">
                <span className="mr-2">机器人名称:</span>
                <input
                  type="text"
                  name="name"
                  maxLength={20}
                  className="px-2 flex-grow rounded bg-light-nonepress-200 dark:bg-dark-nonepress-200"
                  onChange={onChange}
                />
              </label>
              <label className="flex flex-wrap">
                <span className="mr-2">机器人介绍:</span>
                <input
                  type="text"
                  name="desc"
                  className="px-2 flex-grow rounded bg-light-nonepress-200 dark:bg-dark-nonepress-200"
                  onChange={onChange}
                />
              </label>
              <label className="flex flex-wrap">
                <span className="mr-2">仓库/主页:</span>
                <input
                  type="text"
                  name="homepage"
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
            <div className="flex flex-wrap mt-2 items-center">
              <span className="mr-2">Type:</span>
              <button
                className="px-2 h-9 min-w-[64px] rounded text-hero hover:bg-hero hover:bg-opacity-[.08]"
                onClick={() => insertTagType("a:")}
              >
                Adapter
              </button>
              <button
                className="px-2 h-9 min-w-[64px] rounded text-hero hover:bg-hero hover:bg-opacity-[.08]"
                onClick={() => insertTagType("t:")}
              >
                Topic
              </button>
            </div>
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
