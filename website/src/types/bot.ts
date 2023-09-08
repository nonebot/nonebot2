import type { Tag } from "./tag";

export type Bot = {
  name: string;
  desc: string;
  author: string;
  homepage: string;
  tags: Tag[];
  is_official: boolean;
};

export type BotsResponse = Bot[];
