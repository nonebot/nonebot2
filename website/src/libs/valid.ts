import type { IconName } from "@fortawesome/fontawesome-common-types";

import { Resource } from "./store";

export enum ValidStatus {
  VALID = "valid",
  INVALID = "invalid",
  SKIP = "skip",
  MISSING = "missing",
}

export const getValidStatus = (resource: Resource) => {
  switch (resource.resourceType) {
    case "plugin":
      if (resource.skip_test) return ValidStatus.SKIP;
      if (resource.valid) return ValidStatus.VALID;
      return ValidStatus.INVALID;
    default:
      return ValidStatus.MISSING;
  }
};

export const validIcons: {
  [key in ValidStatus]: IconName;
} = {
  [ValidStatus.VALID]: "plug-circle-check",
  [ValidStatus.INVALID]: "plug-circle-xmark",
  [ValidStatus.SKIP]: "plug-circle-exclamation",
  [ValidStatus.MISSING]: "plug-circle-exclamation",
};
