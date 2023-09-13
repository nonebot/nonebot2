import React from "react";
import clsx from "clsx";

import TOCItems from "@theme/TOCItems";
import styles from "./styles.module.css";
import type { TOCProps } from "@theme/TOC";

const LINK_CLASS_NAME = styles["toc-link"];
const LINK_ACTIVE_CLASS_NAME = styles["toc-link-active"];

export default function TOC({ className, ...props }: TOCProps): JSX.Element {
  return (
    <div className={clsx(styles.toc, "thin-scrollbar", className)}>
      <TOCItems
        {...props}
        linkClassName={LINK_CLASS_NAME}
        linkActiveClassName={LINK_ACTIVE_CLASS_NAME}
      />
      <div className="sticky bottom-0 w-full max-w-full mt-2">
        <div
          className="wwads-cn wwads-horizontal max-w-full"
          data-id="281"
        ></div>
      </div>
    </div>
  );
}
