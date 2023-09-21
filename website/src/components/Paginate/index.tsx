import React, { useCallback } from "react";

import clsx from "clsx";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { usePagination } from "react-use-pagination";

import "./styles.css";

const MAX_LENGTH = 7;

export type Props = Pick<
  ReturnType<typeof usePagination>,
  | "totalPages"
  | "currentPage"
  | "setNextPage"
  | "setPreviousPage"
  | "setPage"
  | "previousEnabled"
  | "nextEnabled"
> & {
  className?: string;
};

export default function Paginate({
  className,
  totalPages,
  currentPage,
  setPreviousPage,
  setNextPage,
  setPage,
  previousEnabled,
  nextEnabled,
}: Props): JSX.Element {
  // const [containerElement, setContainerElement] = useState<HTMLElement | null>(
  //   null
  // );

  // const ref = useCallback(
  //   (element: HTMLElement | null) => {
  //     setContainerElement(element);
  //   },
  //   [setContainerElement]
  // );

  // const maxWidth = useContentWidth(
  //   containerElement?.parentElement ?? undefined
  // );
  // const maxLength = Math.min(
  //   (maxWidth && Math.floor(maxWidth / 50) - 2) || totalPages,
  //   totalPages
  // );

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

  const even = MAX_LENGTH % 2 === 0 ? 1 : 0;
  const left = Math.floor(MAX_LENGTH / 2);
  const right = totalPages - left + even + 1;
  currentPage = currentPage + 1;

  if (totalPages <= MAX_LENGTH) {
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
    <nav
      className={clsx("paginate-container", className)}
      role="navigation"
      aria-label="Pagination Navigation"
    >
      <button
        className="paginate-button"
        onClick={setPreviousPage}
        disabled={!previousEnabled}
      >
        <FontAwesomeIcon icon={["fas", "chevron-left"]} />
      </button>
      <ul className="paginate-pager">
        {pages.map((page, index) => (
          <li
            key={index}
            className={clsx(
              "paginate-button",
              typeof page !== "number" && "ellipsis",
              currentPage === page && "active"
            )}
            onClick={() =>
              typeof page === "number" &&
              currentPage !== page &&
              setPage(page - 1)
            }
          >
            {page}
          </li>
        ))}
      </ul>
      <button
        className="paginate-button"
        onClick={setNextPage}
        disabled={!nextEnabled}
      >
        <FontAwesomeIcon icon={["fas", "chevron-right"]} />
      </button>
    </nav>
  );
}
