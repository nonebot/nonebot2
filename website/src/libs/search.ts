import { useCallback, useEffect, useState } from "react";

import { type Filter, useFilteredResources, queryFilter } from "./filter";
import type { Resource } from "./store";

type useSearchControlReturn<T extends Resource> = {
  filteredResources: T[];
  searcherTags: string[];
  addFilter: (filter: Filter<T>) => void;
  onSearchQueryChange: (query: string) => void;
  onSearchQuerySubmit: () => void;
  onSearchBackspace: () => void;
  onSearchClear: () => void;
  onSearchTagClick: (index: number) => void;
};

export function useSearchControl<T extends Resource>(
  resources: T[]
): useSearchControlReturn<T> {
  const [currentFilter, setCurrentFilter] = useState<Filter<T> | null>(null);

  const { filters, addFilter, removeFilter, filteredResources } =
    useFilteredResources(resources);

  // display tags in searcher (except current filter)
  const [searcherFilters, setSearcherFilters] = useState<Filter<T>[]>([]);

  useEffect(() => {
    setSearcherFilters(
      filters.filter((f) => !(currentFilter && f === currentFilter))
    );
  }, [filters, currentFilter]);

  const onSearchQueryChange = useCallback(
    (newQuery: string) => {
      // remove current filter if query is empty
      if (newQuery === "") {
        currentFilter && removeFilter(currentFilter);
        setCurrentFilter(null);
        return;
      }

      const newFilter = queryFilter<T>(newQuery);
      // do nothing if filter is not changed
      if (currentFilter?.id === newFilter.id) return;

      // remove old currentFilter
      currentFilter && removeFilter(currentFilter);
      // add new filter
      setCurrentFilter(newFilter);
      addFilter(newFilter);
    },
    [currentFilter, setCurrentFilter, addFilter, removeFilter]
  );

  const onSearchQuerySubmit = useCallback(() => {
    // set current filter to null to make filter permanent
    setCurrentFilter(null);
  }, [setCurrentFilter]);

  const onSearchBackspace = useCallback(() => {
    // remove last filter
    removeFilter(searcherFilters[searcherFilters.length - 1]);
  }, [removeFilter, searcherFilters]);

  const onSearchClear = useCallback(() => {
    // remove all filters
    searcherFilters.forEach((filter) => removeFilter(filter));
  }, [removeFilter, searcherFilters]);

  const onSearchTagClick = useCallback(
    (index: number) => {
      removeFilter(searcherFilters[index]);
    },
    [removeFilter, searcherFilters]
  );

  return {
    filteredResources,
    searcherTags: searcherFilters.map((filter) => filter.displayName),
    addFilter,
    onSearchQueryChange,
    onSearchQuerySubmit,
    onSearchBackspace,
    onSearchClear,
    onSearchTagClick,
  };
}
