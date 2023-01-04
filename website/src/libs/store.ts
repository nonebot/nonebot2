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

function fuzzySearch(search: string, ...data: string[]): boolean {
  const reg = new RegExp(search, "i");
  return data.some((str) => reg.test(str));
}

export function filterObjs(filter: string, objs: Obj[]): Obj[] {
  return objs.filter((o) => {
    return (
      fuzzySearch(
        filter,
        o.module_name,
        o.project_link,
        o.name,
        o.desc,
        o.author,
      ) ||
      o.tags.some((t) => fuzzySearch(filter, t.label))
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
