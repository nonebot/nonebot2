import { translate } from "@docusaurus/Translate";

import type { Filter as FilterTool } from "@/components/Store/Toolbar";

import {
  authorFilter,
  tagFilter,
  validStatusFilter,
  type Filter,
} from "./filter";
import { ValidStatus } from "./valid";

import type { Resource } from "./store";

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

  const validateStatusFilterMapping: Record<string, ValidStatus> = {
    [translate({
      id: "pages.store.filter.validateStatusDisplayName.valid",
      description: "The display name of validateStatus filter",
      message: "通过",
    })]: ValidStatus.VALID,
    [translate({
      id: "pages.store.filter.validateStatusDisplayName.invalid",
      description: "The display name of validateStatus filter",
      message: "未通过",
    })]: ValidStatus.INVALID,
    [translate({
      id: "pages.store.filter.validateStatusDisplayName.skip",
      description: "The display name of validateStatus filter",
      message: "跳过",
    })]: ValidStatus.SKIP,
    [translate({
      id: "pages.store.filter.validateStatusDisplayName.missing",
      description: "The display name of validateStatus filter",
      message: "缺失",
    })]: ValidStatus.MISSING,
  };

  const validStatusFilterTool: FilterTool = {
    label: "状态",
    icon: ["fas", "plug"],
    choices: Object.keys(validateStatusFilterMapping),
    onSubmit: (type: string) => {
      const validStatus = validateStatusFilterMapping[type];
      if (!validStatus) {
        return;
      }
      addFilter(validStatusFilter(validStatus));
    },
  };

  return {
    filters: [authorFilterTool, tagFilterTool, validStatusFilterTool],
  };
}
