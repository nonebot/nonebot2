import React from "react";

import "asciinema-player/dist/bundle/asciinema-player.css";
import BrowserOnly from "@docusaurus/BrowserOnly";

import "./styles.css";
import type { Props } from "./container";

export type { Props } from "./container";

export default function Asciinema(props: Props): JSX.Element {
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
