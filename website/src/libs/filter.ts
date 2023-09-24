import { useCallback, useState } from "react";

import { translate } from "@docusaurus/Translate";

import type { Resource } from "./store";

export type Filter<T extends Resource = Resource> = {
  type: string;
  id: string;
  displayName: string;
  filter: (resource: T) => boolean;
};

export const tagFilter = <T extends Resource = Resource>(
  tag: string
): Filter<T> => ({
  type: "tag",
  id: `tag-${tag}`,
  displayName: translate(
    {
      id: "pages.store.filter.tagDisplayName",
      description: "The display name of tag filter",
      message: "标签: {tag}",
    },
    { tag }
  ),
  filter: (resource: Resource): boolean =>
    resource.tags.map((tag) => tag.label).includes(tag),
});
export const officialFilter = <T extends Resource = Resource>(
  official: boolean = true
): Filter<T> => ({
  type: "official",
  id: `official-${official}`,
  displayName: translate({
    id: "pages.store.filter.officialDisplayName",
    description: "The display name of official filter",
    message: "非官方|官方",
  }).split("|")[Number(official)],
  filter: (resource: Resource): boolean => resource.is_official === official,
});
export const authorFilter = <T extends Resource = Resource>(
  author: string
): Filter<T> => ({
  type: "author",
  id: `author-${author}`,
  displayName: translate(
    {
      id: "pages.store.filter.authorDisplayName",
      description: "The display name of author filter",
      message: "作者: {author}",
    },
    { author }
  ),
  filter: (resource: Resource): boolean => resource.author === author,
});
export const queryFilter = <T extends Resource = Resource>(
  query: string
): Filter<T> => ({
  type: "query",
  id: `query-${query}`,
  displayName: query,
  filter: (resource: Resource): boolean => {
    if (!query) return true;
    const queryLower = query.toLowerCase();
    const pluginMatch =
      resource.resourceType === "plugin" &&
      (resource.module_name?.toLowerCase().includes(queryLower) ||
        resource.project_link?.toLowerCase().includes(queryLower));
    const commonMatch =
      resource.name.toLowerCase().includes(queryLower) ||
      resource.desc.toLowerCase().includes(queryLower) ||
      resource.author.toLowerCase().includes(queryLower) ||
      resource.tags.filter((t) => t.label.toLowerCase().includes(queryLower))
        .length > 0;
    return pluginMatch || commonMatch;
  },
});

export function filterResources<T extends Resource>(
  resources: T[],
  filters: Filter<T>[]
): T[] {
  return resources.filter((resource) =>
    filters.every((filter) => filter.filter(resource))
  );
}

type useFilteredResourcesReturn<T extends Resource> = {
  filters: Filter<T>[];
  addFilter: (filter: Filter<T>) => void;
  removeFilter: (filter: Filter<T> | string) => void;
  filteredResources: T[];
};

export function useFilteredResources<T extends Resource>(
  resources: T[]
): useFilteredResourcesReturn<T> {
  const [filters, setFilters] = useState<Filter<T>[]>([]);

  const addFilter = useCallback(
    (filter: Filter<T>) => {
      if (filters.some((f) => f.id === filter.id)) return;
      setFilters((filters) => [...filters, filter]);
    },
    [filters, setFilters]
  );
  const removeFilter = useCallback(
    (filter: Filter<T> | string) => {
      setFilters((filters) =>
        filters.filter((f) =>
          typeof filter === "string" ? f.id !== filter : f !== filter
        )
      );
    },
    [setFilters]
  );

  const filteredResources = useCallback(
    () => filterResources(resources, filters),
    [resources, filters]
  );

  return {
    filters,
    addFilter,
    removeFilter,
    filteredResources: filteredResources(),
  };
}
