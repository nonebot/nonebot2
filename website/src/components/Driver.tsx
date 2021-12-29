import React from "react";

import drivers from "../../static/drivers.json";
import { useFilteredObjs } from "../libs/store";

export default function Driver() {
  const {
    filter,
    setFilter,
    filteredObjs: filteredDrivers,
  } = useFilteredObjs(drivers);
  return (
    <>
      <div>
        <input
          value={filter}
          onChange={(event) => setFilter(event.target.value)}
        />
      </div>
      <div>{filteredDrivers.toString()}</div>
    </>
  );
}
