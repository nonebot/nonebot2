import type { Tag } from "./tag";

type BasePlugin = {
  author: string;
  name: string;
  desc: string;
  homepage: string;
  is_official: boolean;
  module_name: string;
  project_link: string;
  skip_test: boolean;
  supported_adapters: string[] | null;
  tags: Array<Tag>;
  time: string;
  type: string;
  valid: boolean;
  version: string;
};

export type Plugin = { resourceType: "plugin" } & BasePlugin;

export type PluginsResponse = BasePlugin[];
