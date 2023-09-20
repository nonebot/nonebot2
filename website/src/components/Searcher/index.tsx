import React, { useRef } from "react";

import clsx from "clsx";

import "./styles.css";
import { translate } from "@docusaurus/Translate";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export type Props = {
  onChange: (value: string) => void;
  onSubmit: (value: string) => void;
  onBackspace: () => void;
  onClear: () => void;
  onTagClick: (index: number) => void;
  tags?: string[];
  className?: string;
  placeholder?: string;
  disabled?: boolean;
};

export default function Searcher({
  onChange,
  onSubmit,
  onBackspace,
  onClear,
  onTagClick,
  tags = [],
  className,
  placeholder,
  disabled = false,
}: Props): JSX.Element {
  const ref = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent<HTMLInputElement>) => {
    onSubmit(e.currentTarget.value);
    e.currentTarget.value = "";
    e.preventDefault();
  };

  const handleEscape = (e: React.KeyboardEvent<HTMLInputElement>) => {
    e.currentTarget.value = "";
  };

  const handleBackspace = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.currentTarget.value === "") {
      onBackspace();
      e.preventDefault();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    switch (e.key) {
      case "Enter": {
        handleSubmit(e);
        break;
      }
      case "Escape": {
        handleEscape(e);
        break;
      }
      case "Backspace": {
        handleBackspace(e);
        break;
      }
      default:
        break;
    }
  };

  const handleClear = () => {
    if (ref.current) {
      ref.current.value = "";
      ref.current.focus();
    }
    onClear();
  };

  return (
    <div className={clsx("searcher-box", className)}>
      <div className="searcher-container">
        {tags.map((tag, index) => (
          <div
            key={index}
            className="badge badge-primary searcher-tag"
            onClick={() => onTagClick(index)}
          >
            {tag}
          </div>
        ))}
        <input
          ref={ref}
          className="searcher-input"
          placeholder={
            placeholder ??
            translate({
              id: "theme.searcher.input.placeholder",
              description: "Search input placeholder",
              message: "搜索",
            })
          }
          onChange={(e) => onChange(e.currentTarget.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
        />
      </div>
      <div className="searcher-action" onClick={handleClear}>
        <FontAwesomeIcon
          className="searcher-action-icon search"
          icon={["fas", "magnifying-glass"]}
        />
        <FontAwesomeIcon
          className="searcher-action-icon close"
          icon={["fas", "xmark"]}
        />
      </div>
    </div>
  );
}
