import React from "react";

import { useWindowSize } from "@nullbot/docusaurus-theme-nonepress/client";

import type { Props } from "@theme/Page/TOC/Container";
import OriginTOCContainer from "@theme-original/Page/TOC/Container";
import "./styles.css";

export default function TOCContainer({
  children,
  ...props
}: Props): JSX.Element {
  const windowSize = useWindowSize();
  const isClient = windowSize !== "ssr";

  return (
    <OriginTOCContainer {...props}>
      {children}
      {isClient && (
        <div className="toc-ads-container">
          <div className="wwads-cn wwads-vertical toc-ads" data-id="281"></div>
        </div>
      )}
    </OriginTOCContainer>
  );
}
