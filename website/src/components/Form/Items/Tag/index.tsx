import React, { useEffect, useState } from "react";

import clsx from "clsx";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ChromePicker, type ColorResult } from "react-color";

import "./styles.css";

import TagComponent from "@/components/Tag";
import { Tag as TagType } from "@/types/tag";

export type Props = {
  onTagUpdate: (tags: TagType[]) => void;
};

export default function TagFormItem({ onTagUpdate }: Props): JSX.Element {
  const [tags, setTags] = useState<TagType[]>([]);
  const [labelType, setLabelType] = useState<string>("");
  const [label, setLabel] = useState<TagType["label"]>("");
  const [color, setColor] = useState<TagType["color"]>("#ea5252");

  useEffect(() => onTagUpdate(tags), [onTagUpdate, tags]);

  const validateTag = () => {
    return label.length >= 1 && label.length <= 10;
  };
  const newTag = () => {
    if (tags.length >= 3) {
      return;
    }
    if (validateTag()) {
      const tag: TagType = { label: labelType + label, color };
      setTags([...tags, tag]);
    }
  };
  const delTag = (index: number) => {
    setTags(tags.filter((_, i) => i !== index));
  };

  const onChangeLabel = (e: { target: { value: string } }) => {
    setLabel(e.target.value);
  };
  const onChangeColor = (color: ColorResult) => {
    setColor(color.hex as TagType["color"]);
  };
  const onChangeLabelType = (e: { target: { value: string } }) => {
    setLabelType(e.target.value);
  };

  return (
    <>
      <label className="flex flex-wrap">
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
        <span className="form-item form-item-title">标签类型</span>
        <select
          className="form-item form-item-select"
          defaultValue=""
          onChange={onChangeLabelType}
        >
          <option value="">Other</option>
          <option value="a:">Adapter</option>
          <option value="t:">Topic</option>
        </select>
      </div>
      <div className="form-item-container">
        <span className="form-item form-item-title">标签名称</span>
        <input
          type="text"
          className="form-item form-item-input"
          placeholder="请输入"
          onChange={onChangeLabel}
        />
      </div>
      <ChromePicker
        className="my-4"
        color={color}
        disableAlpha={true}
        onChangeComplete={onChangeColor}
      />
    </>
  );
}
