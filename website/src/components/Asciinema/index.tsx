import "asciinema-player/dist/bundle/asciinema-player.css";

import "./styles.css";

import React from "react";

import BrowserOnly from "@docusaurus/BrowserOnly";

export default function Asciinema(props): JSX.Element {
  return (
    <BrowserOnly fallback={<div></div>}>
      {() => {
        const AsciinemaContainer = require("./container.tsx").default;
        return <AsciinemaContainer {...props} />;
      }}
    </BrowserOnly>
  );
}
