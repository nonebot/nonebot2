import React, { useCallback, useEffect, useState } from "react";

import Translate from "@docusaurus/Translate";
import { usePagination } from "react-use-pagination";

import Admonition from "@theme/Admonition";

import Modal from "@/components/Modal";
import Paginate from "@/components/Paginate";
import ResourceCard from "@/components/Resource/Card";
import ResourceDetailCard from "@/components/Resource/DetailCard";
import Searcher from "@/components/Searcher";
import { authorFilter, tagFilter } from "@/libs/filter";
import { useSearchControl } from "@/libs/search";
import { fetchRegistryData, loadFailedTitle } from "@/libs/store";
import type { Driver } from "@/types/driver";

export default function DriverPage(): JSX.Element {
  const [drivers, setDrivers] = useState<Driver[] | null>(null);
  const driverCount = drivers?.length ?? 0;
  const loading = drivers === null;

  const [error, setError] = useState<Error | null>(null);
  const [isOpenCardModal, setIsOpenCardModal] = useState<boolean>(false);
  const [clickedDriver, setClickedDriver] = useState<Driver | null>(null);

  const {
    filteredResources: filteredDrivers,
    searcherTags,
    addFilter,
    onSearchQueryChange,
    onSearchQuerySubmit,
    onSearchBackspace,
    onSearchClear,
    onSearchTagClick,
  } = useSearchControl<Driver>(drivers ?? []);
  const filteredDriverCount = filteredDrivers.length;

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
    totalItems: filteredDrivers.length,
    initialPageSize: 12,
  });
  const currentDrivers = filteredDrivers.slice(startIndex, endIndex + 1);

  // load drivers asynchronously
  useEffect(() => {
    fetchRegistryData("driver")
      .then(setDrivers)
      .catch((e) => {
        setError(e);
        console.error(e);
      });
  }, []);

  const onCardClick = useCallback((driver: Driver) => {
    setClickedDriver(driver);
    setIsOpenCardModal(true);
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
        {driverCount === filteredDriverCount ? (
          <Translate
            id="pages.store.driver.info"
            description="Drivers info of the driver store page"
            values={{ driverCount }}
          >
            {"当前共有 {driverCount} 个驱动器"}
          </Translate>
        ) : (
          <Translate
            id="pages.store.driver.searchInfo"
            description="Drivers search info of the driver store page"
            values={{
              driverCount,
              filteredDriverCount,
            }}
          >
            {"当前共有 {filteredDriverCount} / {driverCount} 个驱动器"}
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
          {currentDrivers.map((driver, index) => (
            <ResourceCard
              key={index}
              className="not-prose"
              resource={driver}
              onClick={() => onCardClick(driver)}
              onTagClick={onCardTagClick}
              onAuthorClick={() => onAuthorClick(driver.author)}
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
      {isOpenCardModal && (
        <Modal
          className="not-prose"
          useCustomTitle
          backdropExit
          title="驱动器详情"
          setOpenModal={setIsOpenCardModal}
        >
          {clickedDriver && <ResourceDetailCard resource={clickedDriver} />}
        </Modal>
      )}
    </>
  );
}
