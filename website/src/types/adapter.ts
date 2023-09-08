import type { Tag } from "./tag";

export type Adapter = {
  module_name: string;
  project_link: string;
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags: Tag[];
  is_official: boolean;
};

export type AdaptersResponse = Adapter[];
