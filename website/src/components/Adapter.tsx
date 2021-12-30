import React from "react";
import { usePagination } from "react-use-pagination";

import adapters from "../../static/adapters.json";
import { useFilteredObjs } from "../libs/store";
import Card from "./Card";
import Paginate from "./Paginate";

export default function Adapter(): JSX.Element {
  const {
    filter,
    setFilter,
    filteredObjs: filteredAdapters,
  } = useFilteredObjs(adapters);

  const props = usePagination({
    totalItems: filteredAdapters.length,
    initialPageSize: 10,
  });
  const { startIndex, endIndex } = props;
  const currentAdapters = filteredAdapters.slice(startIndex, endIndex + 1);

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 px-4">
        <input
          className="w-full px-4 py-2 border rounded-full bg-light-nonepress-100 dark:bg-dark-nonepress-100"
          value={filter}
          placeholder="搜索适配器"
          onChange={(event) => setFilter(event.target.value)}
        />
        <button className="w-full rounded-lg bg-hero text-white">
          发布适配器
        </button>
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 px-4">
        {currentAdapters.map((adapter, index) => (
          <Card key={index} {...adapter} />
        ))}
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
    </>
  );
}
