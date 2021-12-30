import React from "react";
import { usePagination } from "react-use-pagination";

import plugins from "../../static/plugins.json";
import { useFilteredObjs } from "../libs/store";
import Card from "./Card";
import Paginate from "./Paginate";

export default function Adapter(): JSX.Element {
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

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 px-4">
        <input
          className="w-full px-4 py-2 border rounded-full bg-light-nonepress-100 dark:bg-dark-nonepress-100"
          value={filter}
          placeholder="搜索插件"
          onChange={(event) => setFilter(event.target.value)}
        />
        <button className="w-full rounded-lg bg-hero text-white" disabled>
          发布插件
        </button>
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 px-4">
        {currentPlugins.map((driver, index) => (
          <Card key={index} {...driver} />
        ))}
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
    </>
  );
}
