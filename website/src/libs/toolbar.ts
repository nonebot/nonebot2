import { authorFilter, tagFilter, type Filter } from "./filter";
import type { Resource } from "./store";

import type { Filter as FilterTool } from "@/components/Store/Toolbar";

type Props<T extends Resource = Resource> = {
  resources: T[];
  addFilter: (filter: Filter<T>) => void;
};

type useToolbarReturns = {
  filters: FilterTool[];
};

export function useToolbar<T extends Resource = Resource>({
  resources,
  addFilter,
}: Props<T>): useToolbarReturns {
  const authorFilterTool: FilterTool = {
    label: "作者",
    icon: ["fas", "user"],
    choices: Array.from(new Set(resources.map((resource) => resource.author))),
    onSubmit: (author: string) => {
      addFilter(authorFilter(author));
    },
  };

  const tagFilterTool: FilterTool = {
    label: "标签",
    icon: ["fas", "tag"],
    choices: Array.from(
      new Set(
        resources.flatMap((resource) => resource.tags.map((tag) => tag.label))
      )
    ),
    onSubmit: (tag: string) => {
      addFilter(tagFilter(tag));
    },
  };

  return {
    filters: [authorFilterTool, tagFilterTool],
  };
}
