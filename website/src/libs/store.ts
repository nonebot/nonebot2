import { translate } from "@docusaurus/Translate";

import type { Adapter, AdaptersResponse } from "@/types/adapter";
import type { Bot, BotsResponse } from "@/types/bot";
import type { Driver, DriversResponse } from "@/types/driver";
import type { Plugin, PluginsResponse } from "@/types/plugin";

type RegistryDataResponseTypes = {
  adapter: AdaptersResponse;
  bot: BotsResponse;
  driver: DriversResponse;
  plugin: PluginsResponse;
};
type RegistryDataType = keyof RegistryDataResponseTypes;

type ResourceTypes = {
  adapter: Adapter;
  bot: Bot;
  driver: Driver;
  plugin: Plugin;
};

export type Resource = Adapter | Bot | Driver | Plugin;

export async function fetchRegistryData<T extends RegistryDataType>(
  dataType: T
): Promise<ResourceTypes[T][]> {
  const resp = await fetch(
    `https://registry.nonebot.dev/${dataType}s.json`
  ).catch((e) => {
    throw new Error(`Failed to fetch ${dataType}s: ${e}`);
  });
  if (!resp.ok)
    throw new Error(
      `Failed to fetch ${dataType}s: ${resp.status} ${resp.statusText}`
    );
  const data = (await resp.json()) as RegistryDataResponseTypes[T];
  return data.map(
    (resource) => ({ ...resource, resourceType: dataType }) as ResourceTypes[T]
  );
}

export const loadFailedTitle = translate({
  id: "pages.store.loadFailed.title",
  message: "加载失败",
  description: "Title to display when loading content failed",
});
