import React, { useState } from "react";

import clsx from "clsx";

import Link from "@docusaurus/Link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import type { Resource } from "@/libs/store";

export type Props = {
  resource: Resource;
  onClick: () => void;
};

export default function Card({ resource, onClick }: Props): JSX.Element {
  const isGithub = /^https:\/\/github.com\/[^/]+\/[^/]+/.test(
    resource.homepage
  );

  return <div></div>;
}
