import React, { useEffect, useState } from "react";

import clsx from "clsx";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ChromePicker, type ColorResult } from "react-color";

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
        <span
          className={clsx(
            "px-2 select-none cursor-pointer min-w-[64px] rounded-full text-hero hover:bg-hero hover:bg-opacity-[.08]",
            "flex justify-center items-center border-dashed border-2 border-primary-600",
            { "pointer-events-none opacity-60": !validateTag() },
            { hidden: tags.length >= 3 }
          )}
          onClick={() => newTag()}
        >
          <FontAwesomeIcon className="pr-1" icon={["fas", "plus"]} />
          新建标签
        </span>
      </label>
      <div className="flex items-center mt-2">
        <span className="basis-1/4 label-text">标签类型</span>
        <select
          className="basis-3/4 ml-auto select select-sm select-bordered"
          defaultValue=""
          onChange={onChangeLabelType}
        >
          <option value="">Other</option>
          <option value="a:">Adapter</option>
          <option value="t:">Topic</option>
        </select>
      </div>
      <div className="flex items-center mt-2">
        <span className="basis-1/4 label-text">标签名称</span>
        <input
          type="text"
          className="basis-3/4 ml-auto input input-sm input-bordered"
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
