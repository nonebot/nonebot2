import React, { useState } from "react";

import clsx from "clsx";

import "./styles.css";
import TagFormItem from "./TagFormItem";

export type FormItemData = {
  type: string;
  inputName: string;
  labelText: string;
};

export type FormItemGroup = {
  name: string;
  items: FormItemData[];
};

export type Props = {
  children?: React.ReactNode;
  formItems: FormItemGroup[];
  handleSubmit: (result: Record<string, string>) => void;
};

export function Form({
  children,
  formItems,
  handleSubmit,
}: Props): JSX.Element {
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [result, setResult] = useState<Record<string, string>>({});
  const setFormValue = (key: string, value: string) => {
    setResult({ ...result, [key]: value });
  };

  const onPrev = () => currentStep > 0 && setCurrentStep(currentStep - 1);
  const onNext = () =>
    currentStep < formItems.length - 1
      ? setCurrentStep(currentStep + 1)
      : handleSubmit(result);

  return (
    <>
      <ul className="steps">
        {formItems.map((item, index) => (
          <li
            key={index}
            className={clsx("step", currentStep == index && "step-primary")}
          >
            {item.name}
          </li>
        ))}
      </ul>
      <div className="form-control w-full max-w-xs min-h-[300px]">
        {children ||
          formItems[currentStep].items.map((item) => (
            <FormItem
              key={item.inputName}
              type={item.type}
              inputName={item.inputName}
              labelText={item.labelText}
              setResult={setFormValue}
            />
          ))}
      </div>
      <div className="flex justify-between">
        <button
          className={clsx(
            "mr-auto btn btn-sm btn-primary no-animation",
            currentStep === 0 && "hidden"
          )}
          onClick={onPrev}
        >
          上一步
        </button>
        <button
          className="ml-auto btn btn-sm btn-primary no-animation"
          onClick={onNext}
        >
          {currentStep === formItems.length - 1 ? "提交" : "下一步"}
        </button>
      </div>
    </>
  );
}

export function FormItem({
  type,
  inputName,
  labelText,
  setResult,
}: FormItemData & {
  setResult: (key: string, value: string) => void;
}): JSX.Element {
  return (
    <>
      <label className="label">
        <span className="label-text">{labelText}</span>
      </label>
      {type === "text" && (
        <input
          type="text"
          name={inputName}
          onChange={(e) => setResult(inputName, e.target.value)}
          placeholder="请输入"
          className="input input-bordered w-full max-w-xs"
        />
      )}
      {type === "tag" && (
        <TagFormItem
          onTagUpdate={(tags) => setResult(inputName, JSON.stringify(tags))}
        />
      )}
    </>
  );
}
