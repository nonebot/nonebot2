import React, { useCallback, useEffect, useState } from "react";

import Translate from "@docusaurus/Translate";
import { usePagination } from "react-use-pagination";

import Admonition from "@theme/Admonition";

import Paginate from "@/components/Paginate";
import ResourceCard from "@/components/Resource/Card";
import Searcher from "@/components/Searcher";
import { authorFilter, tagFilter } from "@/libs/filter";
import { useSearchControl } from "@/libs/search";
import { fetchRegistryData, loadFailedTitle } from "@/libs/store";
import type { Plugin } from "@/types/plugin";

export default function PluginPage(): JSX.Element {
  const [plugins, setPlugins] = useState<Plugin[] | null>(null);
  const pluginCount = plugins?.length ?? 0;
  const loading = plugins === null;

  const [error, setError] = useState<Error | null>(null);

  const {
    filteredResources: filteredPlugins,
    searcherTags,
    addFilter,
    onSearchQueryChange,
    onSearchQuerySubmit,
    onSearchBackspace,
    onSearchClear,
    onSearchTagClick,
  } = useSearchControl<Plugin>(plugins ?? []);
  const filteredPluginCount = filteredPlugins.length;

  const {
    startIndex,
    endIndex,
    totalPages,
    currentPage,
    setNextPage,
    setPreviousPage,
    setPage,
    previousEnabled,
    nextEnabled,
  } = usePagination({
    totalItems: filteredPlugins.length,
    initialPageSize: 12,
  });
  const currentPlugins = filteredPlugins.slice(startIndex, endIndex + 1);

  // load plugins asynchronously
  useEffect(() => {
    fetchRegistryData("plugin")
      .then(setPlugins)
      .catch((e) => {
        setError(e);
        console.error(e);
      });
  }, []);

  const onCardClick = useCallback((plugin: Plugin) => {
    // TODO: open plugin modal
    console.log(plugin, "clicked");
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
        onSubmit={onSearchQuerySubmit}
        onBackspace={onSearchBackspace}
        onClear={onSearchClear}
        onTagClick={onSearchTagClick}
        tags={searcherTags}
        disabled={loading}
      />
      {error ? (
        <Admonition type="caution" title={loadFailedTitle}>
          {error.message}
        </Admonition>
      ) : loading ? (
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
              onClick={() => onCardClick(plugin)}
              onTagClick={onCardTagClick}
              onAuthorClick={() => onAuthorClick(plugin.author)}
            />
          ))}
        </div>
      )}
      <Paginate
        className="not-prose"
        totalPages={totalPages}
        currentPage={currentPage}
        setNextPage={setNextPage}
        setPreviousPage={setPreviousPage}
        setPage={setPage}
        nextEnabled={nextEnabled}
        previousEnabled={previousEnabled}
      />
    </>
  );
}
