import React, { useState } from "react";

import clsx from "clsx";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ChromePicker, type ColorResult } from "react-color";

import "./styles.css";

import TagComponent from "@/components/Tag";
import { Tag as TagType } from "@/types/tag";

export type Props = {
  allowTags: TagType[];
  onTagUpdate: (tags: TagType[]) => void;
};

export default function TagFormItem({
  allowTags,
  onTagUpdate,
}: Props): JSX.Element {
  const [tags, setTags] = useState<TagType[]>([]);
  const [label, setLabel] = useState<TagType["label"]>("");
  const [color, setColor] = useState<TagType["color"]>("#ea5252");
  const slicedTags = Array.from(
    new Set(
      allowTags
        .filter((tag) => tag.label.toLocaleLowerCase().includes(label))
        .map((e) => e.label)
    )
  ).slice(0, 5);

  const validateTag = () => {
    return label.length >= 1 && label.length <= 10;
  };
  const newTag = () => {
    if (tags.length >= 3) {
      return;
    }
    if (validateTag()) {
      const tag: TagType = { label, color };
      setTags([...tags, tag]);
      onTagUpdate(tags);
    }
  };
  const delTag = (index: number) => {
    setTags(tags.filter((_, i) => i !== index));
    onTagUpdate(tags);
  };
  const onChangeColor = (color: ColorResult) => {
    setColor(color.hex as TagType["color"]);
  };

  return (
    <>
      <label className="flex flex-wrap gap-x-1 gap-y-1">
        {tags.map((tag, index) => (
          <TagComponent
            key={index}
            {...tag}
            className="cursor-pointer"
            onClick={() => delTag(index)}
          />
        ))}
        {tags.length < 3 && (
          <span
            className={clsx("add-btn", { "add-btn-disabled": !validateTag() })}
            onClick={() => newTag()}
          >
            <FontAwesomeIcon className="pr-1" icon={["fas", "plus"]} />
            新建标签
          </span>
        )}
      </label>
      <div className="form-item-container">
        <span className="form-item-title">标签名称</span>
        <div className="dropdown dropdown-bottom w-full">
          <input
            type="text"
            value={label}
            className="form-item form-item-input"
            placeholder="请输入"
            onChange={(e) => setLabel(e.target.value)}
          />
          {slicedTags.length > 0 && (
            <ul
              tabIndex={0}
              className="dropdown-content z-10 menu p-2 shadow bg-base-100 rounded-box w-52"
            >
              {slicedTags.map((tag) => (
                <li key={tag}>
                  <a onClick={() => setLabel(tag)}>{tag}</a>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      <div className="form-item-container">
        <span className="form-item-title">标签颜色</span>
        <ChromePicker
          className="my-4 fix-input-color"
          color={color}
          disableAlpha={true}
          onChangeComplete={onChangeColor}
        />
      </div>
    </>
  );
}
