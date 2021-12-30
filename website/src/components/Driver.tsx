import React from "react";
import { usePagination } from "react-use-pagination";

import drivers from "../../static/drivers.json";
import { useFilteredObjs } from "../libs/store";
import Paginate from "./Paginate";

export default function Driver(): JSX.Element {
  const {
    filter,
    setFilter,
    filteredObjs: filteredDrivers,
  } = useFilteredObjs(drivers);

  const props = usePagination({
    totalItems: filteredDrivers.length,
    initialPageSize: 10,
  });
  const { startIndex, endIndex } = props;
  const currentDrivers = filteredDrivers.slice(startIndex, endIndex);

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 px-4">
        <input
          className="w-full px-4 py-2 border rounded-full bg-light-nonepress-100 dark:bg-dark-nonepress-100"
          value={filter}
          placeholder="搜索驱动器"
          onChange={(event) => setFilter(event.target.value)}
        />
        <button className="w-full rounded bg-hero text-white" disabled>
          发布驱动器
        </button>
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <div>
        {currentDrivers.map((driver, index) => (
          <p key={index}>{driver.name}</p>
        ))}
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
    </>
  );
}
