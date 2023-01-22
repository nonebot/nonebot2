import { useState } from "react";

export type Tag = {
  label: string;
  color: string;
};

export type Obj = {
  module_name?: string;
  project_link?: string;
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags: Tag[];
  is_official: boolean;
};

export function filterObjs(filter: string, objs: Obj[]): Obj[] {
  let filterLower = filter.toLowerCase();
  return objs.filter((o) => {
    return (
      o.module_name?.toLowerCase().includes(filterLower) ||
      o.project_link?.toLowerCase().includes(filterLower) ||
      o.name.toLowerCase().includes(filterLower) ||
      o.desc.toLowerCase().includes(filterLower) ||
      o.author.toLowerCase().includes(filterLower) ||
      o.tags.filter((t) => t.label.toLowerCase().includes(filterLower)).length >
        0
    );
  });
}

type useFilteredObjsReturn = {
  filter: string;
  setFilter: (filter: string) => void;
  filteredObjs: Obj[];
};

export function useFilteredObjs(objs: Obj[]): useFilteredObjsReturn {
  const [filter, setFilter] = useState<string>("");
  const filteredObjs = filterObjs(filter, objs);
  return {
    filter,
    setFilter,
    filteredObjs,
  };
}
