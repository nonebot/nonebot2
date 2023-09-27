import type { Tag } from "./tag";

type BaseAdapter = {
  module_name: string;
  project_link: string;
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags: Tag[];
  is_official: boolean;
};

export type Adapter = { resourceType: "adapter" } & BaseAdapter;

export type AdaptersResponse = BaseAdapter[];
