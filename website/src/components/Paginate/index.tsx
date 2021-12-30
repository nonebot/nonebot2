import React, { useCallback, useRef } from "react";
import ReactPaginate from "react-paginate";
import { usePagination } from "react-use-pagination";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { useContentWidth } from "../../libs/width";
import styles from "./styles.module.css";

export default function Paginate({
  totalPages,
  setPage,
  currentPage,
}: ReturnType<typeof usePagination>): JSX.Element {
  const ref = useRef<HTMLElement>();
  const maxWidth = useContentWidth(ref.current?.parentElement ?? undefined);

  const onPageChange = useCallback(
    (selectedItem: { selected: number }) => {
      setPage(selectedItem.selected);
    },
    [setPage]
  );

  // FIXME: responsive width
  return (
    <nav role="navigation" aria-label="Pagination Navigation" ref={ref}>
      <ReactPaginate
        pageCount={totalPages}
        forcePage={currentPage}
        onPageChange={onPageChange}
        containerClassName={styles.container}
        pageClassName={styles.li}
        pageLinkClassName={styles.a}
        previousClassName={styles.li}
        previousLinkClassName={styles.a}
        nextClassName={styles.li}
        nextLinkClassName={styles.a}
        activeLinkClassName={styles.active}
        disabledLinkClassName={styles.disabled}
        breakLabel={<FontAwesomeIcon icon="ellipsis-h" />}
        previousLabel={<FontAwesomeIcon icon="chevron-left" />}
        nextLabel={<FontAwesomeIcon icon="chevron-right" />}
      ></ReactPaginate>
    </nav>
  );
}
