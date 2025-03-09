import React from "react";

import BrowserOnly from "@docusaurus/BrowserOnly";

import "asciinema-player/dist/bundle/asciinema-player.css";

import type { Props } from "./container";

import "./styles.css";

export type { Props } from "./container";

export default function Asciinema(props: Props): React.ReactNode {
  return (
    <BrowserOnly
      fallback={
        <a href={props.url} title="Asciinema video player">
          Asciinema cast
        </a>
      }
    >
      {() => {
        // eslint-disable-next-line @typescript-eslint/no-var-requires
        const AsciinemaContainer = require("./container.tsx").default;
        return <AsciinemaContainer {...props} />;
      }}
    </BrowserOnly>
  );
}
