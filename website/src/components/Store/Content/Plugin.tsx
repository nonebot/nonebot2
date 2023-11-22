import React, { useCallback, useEffect, useState } from "react";

import Translate from "@docusaurus/Translate";
import { usePagination } from "react-use-pagination";

import Admonition from "@theme/Admonition";

import PluginForm from "@/components/Form/Plugin";
import Modal from "@/components/Modal";
import Paginate from "@/components/Paginate";
import ResourceCard from "@/components/Resource/Card";
import ResourceDetailCard from "@/components/Resource/DetailCard";
import Searcher from "@/components/Searcher";
import StoreToolbar, { type Action } from "@/components/Store/Toolbar";
import { authorFilter, tagFilter } from "@/libs/filter";
import { useSearchControl } from "@/libs/search";
import { fetchRegistryData, loadFailedTitle } from "@/libs/store";
import { useToolbar } from "@/libs/toolbar";
import type { Plugin } from "@/types/plugin";

export default function PluginPage(): JSX.Element {
  const [plugins, setPlugins] = useState<Plugin[] | null>(null);
  const pluginCount = plugins?.length ?? 0;
  const loading = plugins === null;

  const [error, setError] = useState<Error | null>(null);
  const [isOpenModal, setIsOpenModal] = useState<boolean>(false);
  const [isOpenCardModal, setIsOpenCardModal] = useState<boolean>(false);
  const [clickedPlugin, setClickedPlugin] = useState<Plugin | null>(null);

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

  const { filters: filterTools } = useToolbar({
    resources: plugins ?? [],
    addFilter,
  });

  const actionTool: Action = {
    label: "发布插件",
    icon: ["fas", "plus"],
    onClick: () => {
      setIsOpenModal(true);
    },
  };

  const onCardClick = useCallback((plugin: Plugin) => {
    setClickedPlugin(plugin);
    setIsOpenCardModal(true);
  }, []);

  const onCardTagClick = useCallback(
    (tag: string) => {
      addFilter(tagFilter(tag));
    },
    [addFilter]
  );

  const onCardAuthorClick = useCallback(
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

      <StoreToolbar
        className="not-prose"
        filters={filterTools}
        action={actionTool}
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
              onAuthorClick={() => onCardAuthorClick(plugin.author)}
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
      {isOpenModal && (
        <Modal
          className="not-prose"
          title="发布插件"
          setOpenModal={setIsOpenModal}
        >
          <PluginForm />
        </Modal>
      )}
      {isOpenCardModal && (
        <Modal
          className="not-prose"
          useCustomTitle
          backdropExit
          title="插件详情"
          setOpenModal={setIsOpenCardModal}
        >
          {clickedPlugin && <ResourceDetailCard resource={clickedPlugin} />}
        </Modal>
      )}
    </>
  );
}
