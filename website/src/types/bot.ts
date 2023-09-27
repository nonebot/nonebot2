import type { Tag } from "./tag";

type BaseBot = {
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags: Tag[];
  is_official: boolean;
};

export type Bot = { resourceType: "bot" } & BaseBot;

export type BotsResponse = BaseBot[];
