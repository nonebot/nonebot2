import React, { useCallback } from "react";
import ReactPaginate from "react-paginate";
import { usePagination } from "react-use-pagination";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export default function Paginate({
  totalPages,
  setPage,
}: ReturnType<typeof usePagination>): JSX.Element {
  const onPageChange = useCallback(
    (selectedItem: { selected: number }) => {
      setPage(selectedItem.selected);
    },
    [setPage]
  );

  return (
    <nav role="navigation" aria-label="Pagination Navigation">
      <ReactPaginate
        pageCount={totalPages}
        onPageChange={onPageChange}
        containerClassName="w-full m-w-full inline-flex justify-center align-center m-0 pl-0 list-none"
        breakLabel={<FontAwesomeIcon icon="ellipsis-h" />}
        previousLabel={<FontAwesomeIcon icon="chevron-left" />}
        nextLabel={<FontAwesomeIcon icon="chevron-right" />}
      ></ReactPaginate>
    </nav>
  );
}
