import React, { useState } from "react";

import clsx from "clsx";

import "./styles.css";

import TagFormItem from "./Items/Tag";

export type FormItemData = {
  type: string;
  name: string;
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

  const handleNextStep = () => {
    const currentStepNames = formItems[currentStep].items.map(
      (item) => item.name
    );
    if (currentStepNames.every((name) => result[name]))
      setCurrentStep(currentStep + 1);
    else return;
  };
  const onPrev = () => currentStep > 0 && setCurrentStep(currentStep - 1);
  const onNext = () =>
    currentStep < formItems.length - 1
      ? handleNextStep()
      : handleSubmit(result);

  return (
    <>
      <ul className="steps">
        {formItems.map((item, index) => (
          <li
            key={index}
            className={clsx("step", currentStep === index && "step-primary")}
          >
            {item.name}
          </li>
        ))}
      </ul>
      <div className="form-control w-full min-h-[300px]">
        {children ||
          formItems[currentStep].items.map((item) => (
            <FormItem
              key={item.name}
              type={item.type}
              name={item.name}
              labelText={item.labelText}
              result={result}
              setResult={setFormValue}
            />
          ))}
      </div>
      <div className="flex justify-between">
        <button
          className={clsx("form-btn form-btn-prev", {
            hidden: currentStep === 0,
          })}
          onClick={onPrev}
        >
          上一步
        </button>
        <button className="form-btn form-btn-next" onClick={onNext}>
          {currentStep === formItems.length - 1 ? "提交" : "下一步"}
        </button>
      </div>
    </>
  );
}

export function FormItem({
  type,
  name,
  labelText,
  result,
  setResult,
}: FormItemData & {
  result: Record<string, string>;
  setResult: (key: string, value: string) => void;
}): JSX.Element {
  return (
    <>
      <label className="label">
        <span className="label-text">{labelText}</span>
      </label>
      {type === "text" && (
        <input
          value={result[name]}
          type="text"
          name={name}
          onChange={(e) => setResult(name, e.target.value)}
          placeholder="请输入"
          className={clsx("form-input", {
            "form-input-error": !result[name],
          })}
        />
      )}
      {type === "text" && !result[name] && (
        <label className="label">
          <span className="form-label form-label-error">请输入{labelText}</span>
        </label>
      )}
      {type === "tag" && (
        <TagFormItem
          onTagUpdate={(tags) => setResult(name, JSON.stringify(tags))}
        />
      )}
    </>
  );
}
