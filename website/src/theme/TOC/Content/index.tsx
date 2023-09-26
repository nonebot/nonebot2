import React from "react";

import "./styles.css";
import type { Props } from "@theme/TOC/Content";
import OriginTOCContent from "@theme-original/TOC/Content";

export default function TOCContent(props: Props): JSX.Element {
  return (
    <>
      <OriginTOCContent {...props} />
      <div className="toc-ads-container">
        <div className="wwads-cn wwads-horizontal toc-ads" data-id="281"></div>
      </div>
    </>
  );
}
