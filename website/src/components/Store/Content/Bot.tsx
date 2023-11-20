import React, { useCallback, useEffect, useState } from "react";

import Translate from "@docusaurus/Translate";
import { usePagination } from "react-use-pagination";

import Admonition from "@theme/Admonition";

import BotForm from "@/components/Form/Bot";
import Modal from "@/components/Modal";
import Paginate from "@/components/Paginate";
import ResourceCard from "@/components/Resource/Card";
import Searcher from "@/components/Searcher";
import StoreToolbar, { type Action } from "@/components/Store/Toolbar";
import { authorFilter, tagFilter } from "@/libs/filter";
import { useSearchControl } from "@/libs/search";
import { fetchRegistryData, loadFailedTitle } from "@/libs/store";
import { useToolbar } from "@/libs/toolbar";
import type { Bot } from "@/types/bot";

export default function PluginPage(): JSX.Element {
  const [bots, setBots] = useState<Bot[] | null>(null);
  const botCount = bots?.length ?? 0;
  const loading = bots === null;

  const [error, setError] = useState<Error | null>(null);
  const [isOpenModal, setIsOpenModal] = useState<boolean>(false);

  const {
    filteredResources: filteredBots,
    searcherTags,
    addFilter,
    onSearchQueryChange,
    onSearchQuerySubmit,
    onSearchBackspace,
    onSearchClear,
    onSearchTagClick,
  } = useSearchControl<Bot>(bots ?? []);
  const filteredBotCount = filteredBots.length;

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
    totalItems: filteredBots.length,
    initialPageSize: 12,
  });
  const currentBots = filteredBots.slice(startIndex, endIndex + 1);

  // load bots asynchronously
  useEffect(() => {
    fetchRegistryData("bot")
      .then(setBots)
      .catch((e) => {
        setError(e);
        console.error(e);
      });
  }, []);

  const { filters: filterTools } = useToolbar({
    resources: bots ?? [],
    addFilter,
  });

  const actionTool: Action = {
    label: "发布机器人",
    icon: ["fas", "plus"],
    onClick: () => {
      setIsOpenModal(true);
    },
  };

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
        {botCount === filteredBotCount ? (
          <Translate
            id="pages.store.bot.info"
            description="Bots info of the bot store page"
            values={{ botCount }}
          >
            {"当前共有 {botCount} 个机器人"}
          </Translate>
        ) : (
          <Translate
            id="pages.store.bot.searchInfo"
            description="Bots search info of the bot store page"
            values={{
              botCount,
              filteredBotCount,
            }}
          >
            {"当前共有 {filteredBotCount} / {botCount} 个机器人"}
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
          {currentBots.map((bot, index) => (
            <ResourceCard
              key={index}
              className="not-prose"
              resource={bot}
              onTagClick={onCardTagClick}
              onAuthorClick={() => onAuthorClick(bot.author)}
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
          title="发布机器人"
          setOpenModal={setIsOpenModal}
        >
          <BotForm />
        </Modal>
      )}
    </>
  );
}
