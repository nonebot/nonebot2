import type { Tag } from "./tag";

type BaseDriver = {
  module_name: string;
  project_link: string;
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags: Tag[];
  is_official: boolean;
};

export type Driver = { resourceType: "driver" } & BaseDriver;

export type DriversResponse = BaseDriver[];
