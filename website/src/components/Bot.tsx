import React from "react";
import { usePagination } from "react-use-pagination";

import bots from "../../static/bots.json";
import { useFilteredObjs } from "../libs/store";
import Paginate from "./Paginate";

export default function Adapter(): JSX.Element {
  const {
    filter,
    setFilter,
    filteredObjs: filteredBots,
  } = useFilteredObjs(bots);

  const props = usePagination({
    totalItems: filteredBots.length,
    initialPageSize: 10,
  });
  const { startIndex, endIndex } = props;
  const currentBots = filteredBots.slice(startIndex, endIndex + 1);

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4 px-4">
        <input
          className="w-full px-4 py-2 border rounded-full bg-light-nonepress-100 dark:bg-dark-nonepress-100"
          value={filter}
          placeholder="搜索机器人"
          onChange={(event) => setFilter(event.target.value)}
        />
        <button className="w-full rounded-lg bg-hero text-white" disabled>
          发布机器人
        </button>
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
      <div>
        {currentBots.map((driver, index) => (
          <p key={index}>{driver.name}</p>
        ))}
      </div>
      <div className="grid grid-cols-1 p-4">
        <Paginate {...props} />
      </div>
    </>
  );
}
