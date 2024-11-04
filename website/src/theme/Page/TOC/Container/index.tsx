import React from "react";

import "./styles.css";
import type { Props } from "@theme/Page/TOC/Container";
import OriginTOCContainer from "@theme-original/Page/TOC/Container";

export default function TOCContainer({
  children,
  ...props
}: Props): JSX.Element {
  return (
    <OriginTOCContainer {...props}>
      {children}
      <div className="toc-ads-container">
        <div className="wwads-cn wwads-vertical toc-ads" data-id="281"></div>
      </div>
    </OriginTOCContainer>
  );
}
