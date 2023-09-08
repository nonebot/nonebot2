import React, { useCallback, useState } from "react";

import clsx from "clsx";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { usePagination } from "react-use-pagination";

import { useContentWidth } from "../../libs/width";

import styles from "./styles.module.css";

export default function Paginate({
  totalPages,
  setPreviousPage,
  setNextPage,
  setPage,
  currentPage,
  previousEnabled,
  nextEnabled,
}: ReturnType<typeof usePagination>): JSX.Element {
  const [containerElement, setContainerElement] = useState<HTMLElement | null>(
    null
  );

  const ref = useCallback(
    (element: HTMLElement | null) => {
      setContainerElement(element);
    },
    [setContainerElement]
  );

  const maxWidth = useContentWidth(
    containerElement?.parentElement ?? undefined
  );
  const maxLength = Math.min(
    (maxWidth && Math.floor(maxWidth / 50) - 2) || totalPages,
    totalPages
  );

  const range = useCallback((start: number, end: number) => {
    const result = [];
    start = start > 0 ? start : 1;
    for (let i = start; i <= end; i++) {
      result.push(i);
    }
    return result;
  }, []);

  const pages: (React.ReactNode | number)[] = [];
  const ellipsis = <FontAwesomeIcon icon="ellipsis-h" />;

  const even = maxLength % 2 === 0 ? 1 : 0;
  const left = Math.floor(maxLength / 2);
  const right = totalPages - left + even + 1;
  currentPage = currentPage + 1;

  if (totalPages <= maxLength) {
    pages.push(...range(1, totalPages));
  } else if (currentPage > left && currentPage < right) {
    const firstItem = 1;
    const lastItem = totalPages;
    const start = currentPage - left + 2;
    const end = currentPage + left - 2 - even;
    const secondItem = start - 1 === firstItem + 1 ? 2 : ellipsis;
    const beforeLastItem = end + 1 === lastItem - 1 ? end + 1 : ellipsis;

    pages.push(1, secondItem, ...range(start, end), beforeLastItem, totalPages);
  } else if (currentPage === left) {
    const end = currentPage + left - 1 - even;
    pages.push(...range(1, end), ellipsis, totalPages);
  } else if (currentPage === right) {
    const start = currentPage - left + 1;
    pages.push(1, ellipsis, ...range(start, totalPages));
  } else {
    pages.push(...range(1, left), ellipsis, ...range(right, totalPages));
  }

  return (
    <nav role="navigation" aria-label="Pagination Navigation" ref={ref}>
      <ul className={styles.container}>
        <li
          className={clsx(styles.li, { [styles.disabled]: !previousEnabled })}
        >
          <button className={styles.button} onClick={setPreviousPage}>
            <FontAwesomeIcon icon="chevron-left" />
          </button>
        </li>
        {pages.map((page, index) => (
          <li className={styles.li} key={index}>
            <button
              className={clsx(styles.button, {
                [styles.active]: page === currentPage,
                "pointer-events-none": typeof page !== "number",
              })}
              onClick={() => typeof page === "number" && setPage(page - 1)}
            >
              {page}
            </button>
          </li>
        ))}
        <li className={clsx(styles.li, { [styles.disabled]: !nextEnabled })}>
          <button className={styles.button} onClick={setNextPage}>
            <FontAwesomeIcon icon="chevron-right" />
          </button>
        </li>
      </ul>
    </nav>
  );
}
