import React, { useState } from "react";

import clsx from "clsx";

import type { IconProp } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export type Filter = {
  label: string;
  icon: IconProp;
  choices?: string[];
  onSubmit: (query: string) => void;
};

export type Action = {
  label: string;
  icon: IconProp;
  onClick: () => void;
};

export type Props = {
  filters?: Filter[];
  action?: Action;
  className?: string;
};

function ToolbarFilter({
  label,
  icon,
  choices,
  onSubmit,
}: Filter): JSX.Element {
  const [query, setQuery] = useState<string>("");

  const filteredChoices = choices
    ?.filter((choice) => choice.toLowerCase().includes(query.toLowerCase()))
    ?.slice(0, 5);

  const handleQuerySubmit = () => {
    if (filteredChoices && filteredChoices.length > 0) {
      onSubmit(filteredChoices[0]);
    } else if (choices === null) {
      onSubmit(query);
    }
  };

  const onQueryKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleQuerySubmit();
      e.preventDefault();
    }
  };

  const onChoiceKeyDown = (e: React.KeyboardEvent<HTMLLIElement>) => {
    if (e.key === "Enter") {
      onSubmit(e.currentTarget.innerText);
      e.preventDefault();
    }
  };

  return (
    <div className="dropdown">
      <label
        className="btn btn-sm btn-outline btn-primary no-animation"
        tabIndex={0}
      >
        <FontAwesomeIcon icon={icon} />
        {label}
      </label>
      <div className="dropdown-content store-toolbar-dropdown">
        <input
          type="text"
          placeholder="搜索"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={onQueryKeyDown}
          className="input input-sm input-bordered w-full"
        />
        {filteredChoices && (
          <ul className="menu menu-sm">
            {filteredChoices.map((choice, index) => (
              <li
                key={index}
                onClick={() => onSubmit(choice)}
                onKeyDown={onChoiceKeyDown}
              >
                <a tabIndex={0}>{choice}</a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default function StoreToolbar({
  filters,
  action,
  className,
}: Props): JSX.Element | null {
  if (!(filters && filters.length > 0) && !action) {
    return null;
  }

  return (
    <div className={clsx("store-toolbar", className)}>
      {filters && filters.length > 0 && (
        <div className="store-toolbar-filters">
          {filters.map((filter, index) => (
            <ToolbarFilter key={index} {...filter} />
          ))}
        </div>
      )}
      {action && (
        <div className="store-toolbar-action">
          <button
            className="btn btn-sm btn-primary no-animation"
            onClick={action.onClick}
          >
            <FontAwesomeIcon icon={action.icon} />
            {action.label}
          </button>
        </div>
      )}
    </div>
  );
}
