import React, { useCallback, useEffect, useState } from "react";

import Translate from "@docusaurus/Translate";
import { usePagination } from "react-use-pagination";

import "./styles.css";
import ResourceCard from "@/components/Resource/Card";
import Searcher from "@/components/Searcher";
import {
  fetchRegistryData,
  queryFilter,
  authorFilter,
  tagFilter,
  useFilteredResources,
} from "@/libs/store";
import type { Filter } from "@/libs/store";
import type { Plugin } from "@/types/plugin";

export default function PluginPage(): JSX.Element {
  const [plugins, setPlugins] = useState<Plugin[] | null>(null);
  const pluginCount = plugins?.length ?? 0;
  const loading = plugins === null;

  const [filter, setFilter] = useState<Filter<Plugin> | null>(null);

  const {
    filters,
    addFilter,
    removeFilter,
    filteredResources: filteredPlugins,
  } = useFilteredResources(plugins ?? []);
  const filteredPluginCount = filteredPlugins.length;

  // display tags in searcher (except current filter)
  const searcherFilters = filters.filter((f) => !(filter && f === filter));
  const searcherTags = searcherFilters.map((filter) => filter.displayName);

  const { startIndex, endIndex } = usePagination({
    totalItems: filteredPlugins.length,
    initialPageSize: 12,
  });
  const currentPlugins = filteredPlugins.slice(startIndex, endIndex + 1);

  // load plugins asynchronously
  useEffect(() => {
    fetchRegistryData("plugin").then(setPlugins).catch(console.error);
  }, []);

  const onSearchQueryChange = useCallback(
    (newQuery: string) => {
      // remove filter if query is empty
      if (newQuery === "") {
        filter && removeFilter(filter);
        setFilter(null);
        return;
      }

      const newFilter = queryFilter<Plugin>(newQuery);
      // do nothing if filter is not changed
      if (filter?.id === newFilter.id) return;

      // remove old filter
      filter && removeFilter(filter);
      // add new filter
      setFilter(newFilter);
      addFilter(newFilter);
    },
    [filter, setFilter, addFilter, removeFilter]
  );

  const onSearchSubmit = useCallback(() => {
    setFilter(null);
  }, [setFilter]);

  const onSearchBackspace = useCallback(() => {
    removeFilter(searcherFilters[searcherFilters.length - 1]);
  }, [removeFilter, searcherFilters]);

  const onSearchClear = useCallback(() => {
    searcherFilters.forEach((filter) => removeFilter(filter));
  }, [removeFilter, searcherFilters]);

  const onSearchTagClick = useCallback(
    (index: number) => {
      removeFilter(searcherFilters[index]);
    },
    [removeFilter, searcherFilters]
  );

  const onCardClick = useCallback(() => {
    console.log("card clicked");
  }, []);

  const onCardTagClick = useCallback(
    (tag: string) => {
      addFilter(tagFilter(tag));
    },
    [addFilter]
  );

  const onAuthorClick = useCallback(
    (author: string) => {
      addFilter(authorFilter(author));
    },
    [addFilter]
  );

  return (
    <>
      <p className="store-description">
        {pluginCount === filteredPluginCount ? (
          <Translate
            id="pages.store.plugin.info"
            description="Plugins info of the plugin store page"
            values={{ pluginCount }}
          >
            {"当前共有 {pluginCount} 个插件"}
          </Translate>
        ) : (
          <Translate
            id="pages.store.plugin.searchInfo"
            description="Plugins search info of the plugin store page"
            values={{ pluginCount, filteredPluginCount: filteredPluginCount }}
          >
            {"当前共有 {filteredPluginCount} / {pluginCount} 个插件"}
          </Translate>
        )}
      </p>
      <Searcher
        className="store-searcher not-prose"
        onChange={onSearchQueryChange}
        onSubmit={onSearchSubmit}
        onBackspace={onSearchBackspace}
        onClear={onSearchClear}
        onTagClick={onSearchTagClick}
        tags={searcherTags}
        disabled={loading}
      />
      {loading ? (
        <p className="store-loading-container">
          <span className="loading loading-dots loading-lg store-loading"></span>
        </p>
      ) : (
        <div className="store-container">
          {currentPlugins.map((plugin, index) => (
            <ResourceCard
              key={index}
              className="not-prose"
              resource={plugin}
              onClick={onCardClick}
              onTagClick={onCardTagClick}
              onAuthorClick={() => onAuthorClick(plugin.author)}
            />
          ))}
        </div>
      )}
    </>
  );
}
