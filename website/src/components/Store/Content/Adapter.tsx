import React, { useCallback, useEffect, useState } from "react";

import Translate from "@docusaurus/Translate";
import { usePagination } from "react-use-pagination";

import Admonition from "@theme/Admonition";

import AdapterForm from "@/components/Form/Adapter";
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
import type { Adapter } from "@/types/adapter";

export default function AdapterPage(): JSX.Element {
  const [adapters, setAdapters] = useState<Adapter[] | null>(null);
  const adapterCount = adapters?.length ?? 0;
  const loading = adapters === null;

  const [error, setError] = useState<Error | null>(null);
  const [isOpenModal, setIsOpenModal] = useState<boolean>(false);
  const [isOpenCardModal, setIsOpenCardModal] = useState<boolean>(false);
  const [clickedAdapter, setClickedAdapter] = useState<Adapter | null>(null);

  const {
    filteredResources: filteredAdapters,
    searcherTags,
    addFilter,
    onSearchQueryChange,
    onSearchQuerySubmit,
    onSearchBackspace,
    onSearchClear,
    onSearchTagClick,
  } = useSearchControl<Adapter>(adapters ?? []);
  const filteredAdapterCount = filteredAdapters.length;

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
    totalItems: filteredAdapters.length,
    initialPageSize: 12,
  });
  const currentAdapters = filteredAdapters.slice(startIndex, endIndex + 1);

  // load adapters asynchronously
  useEffect(() => {
    fetchRegistryData("adapter")
      .then(setAdapters)
      .catch((e) => {
        setError(e);
        console.error(e);
      });
  }, []);

  const { filters: filterTools } = useToolbar({
    resources: adapters ?? [],
    addFilter,
  });

  const actionTool: Action = {
    label: "发布适配器",
    icon: ["fas", "plus"],
    onClick: () => {
      setIsOpenModal(true);
    },
  };

  const onCardClick = useCallback((adapter: Adapter) => {
    setClickedAdapter(adapter);
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
        {adapterCount === filteredAdapterCount ? (
          <Translate
            id="pages.store.adapter.info"
            description="Adapters info of the adapter store page"
            values={{ adapterCount }}
          >
            {"当前共有 {adapterCount} 个适配器"}
          </Translate>
        ) : (
          <Translate
            id="pages.store.adapter.searchInfo"
            description="Adapters search info of the adapter store page"
            values={{
              adapterCount,
              filteredAdapterCount,
            }}
          >
            {"当前共有 {filteredAdapterCount} / {adapterCount} 个适配器"}
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
          {currentAdapters.map((adapter, index) => (
            <ResourceCard
              key={index}
              className="not-prose"
              resource={adapter}
              onClick={() => onCardClick(adapter)}
              onTagClick={onCardTagClick}
              onAuthorClick={() => onCardAuthorClick(adapter.author)}
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
          title="发布适配器"
          setOpenModal={setIsOpenModal}
        >
          <AdapterForm />
        </Modal>
      )}
      {isOpenCardModal && (
        <Modal
          className="not-prose"
          title="适配器详情"
          backdropExit
          setOpenModal={setIsOpenCardModal}
        >
          {clickedAdapter && <ResourceDetailCard resource={clickedAdapter} />}
        </Modal>
      )}
    </>
  );
}
