import { useCallback, useState } from "react";

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

export async function fetchRegistryData<T extends RegistryDataType>(
  dataType: T
): Promise<RegistryDataResponseTypes[T]> {
  const resp = await fetch(`https://registry.nonebot.dev/${dataType}s.json`);
  return await resp.json();
}

export type Resource = Adapter | Bot | Driver | Plugin;

type Filter<T extends Resource = Resource> = {
  name: string;
  filter: (resource: T) => boolean;
};

export const tagFilter = (tag: string) => ({
  name: "tag",
  filter: (resource: Resource): boolean =>
    resource.tags.map((tag) => tag.label).includes(tag),
});
export const officialFilter = (official: boolean = true) => ({
  name: "official",
  filter: (resource: Resource): boolean => resource.is_official === official,
});
export const authorFilter = (author: string): Filter => ({
  name: "author",
  filter: (resource: Resource): boolean => resource.author === author,
});
export const queryFilter = (query: string): Filter => ({
  name: "query",
  filter: (resource: Resource): boolean => {
    const queryLower = query.toLowerCase();
    return (
      // resource.module_name?.toLowerCase().includes(queryLower) ||
      // resource.project_link?.toLowerCase().includes(queryLower) ||
      resource.name.toLowerCase().includes(queryLower) ||
      resource.desc.toLowerCase().includes(queryLower) ||
      resource.author.toLowerCase().includes(queryLower) ||
      resource.tags.filter((t) => t.label.toLowerCase().includes(queryLower))
        .length > 0
    );
  },
});

export function filterResources<T extends Resource>(
  resources: T[],
  filters: Filter[]
): T[] {
  return resources.filter((resource) =>
    filters.every((filter) => filter.filter(resource))
  );
}

type useFilteredResourcesReturn<T extends Resource> = {
  filters: Filter<T>[];
  addFilter: (filter: Filter<T>) => void;
  removeFilter: (filter: Filter<T>) => void;
  filteredResources: T[];
};

export function useFilteredResources<T extends Resource>(
  resources: T[]
): useFilteredResourcesReturn<T> {
  const [filters, setFilters] = useState<Filter[]>([]);

  const addFilter = useCallback(
    (filter: Filter) => {
      setFilters((filters) => [...filters, filter]);
    },
    [setFilters]
  );
  const removeFilter = useCallback(
    (filter: Filter) => {
      setFilters((filters) => filters.filter((f) => f.name !== filter.name));
    },
    [setFilters]
  );

  return {
    filters,
    addFilter,
    removeFilter,
    filteredResources: filterResources(resources, filters),
  };
}
