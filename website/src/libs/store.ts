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
  return objs.filter((o) => {
    return (
      o.module_name?.includes(filter) ||
      o.project_link?.includes(filter) ||
      o.name.includes(filter) ||
      o.desc.includes(filter) ||
      o.author.includes(filter) ||
      o.tags.filter((t) => t.label.includes(filter)).length > 0
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
