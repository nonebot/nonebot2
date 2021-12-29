import { useState } from "react";

type Tag = {
  label: string;
  color: string;
};

type Obj = {
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
      o.module_name?.indexOf(filter) != -1 ||
      o.project_link?.indexOf(filter) != -1 ||
      o.name.indexOf(filter) != -1 ||
      o.desc.indexOf(filter) != -1 ||
      o.author.indexOf(filter) != -1
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
