import "asciinema-player/dist/bundle/asciinema-player.css";

import "./styles.css";

import * as AsciinemaPlayer from "asciinema-player";
import React, { useEffect, useRef } from "react";

export type AsciinemaOptions = {
  cols: number;
  rows: number;
  autoPlay: boolean;
  preload: boolean;
  loop: boolean;
  startAt: number | string;
  speed: number;
  idleTimeLimit: number;
  theme: string;
  poster: string;
  fit: string;
  fontSize: string;
};

export type AsciinemaProps = {
  url: string;
  options?: Partial<AsciinemaOptions>;
};

export default function Asciinema({
  url,
  options = {},
}: AsciinemaProps): JSX.Element {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    AsciinemaPlayer.create(url, ref.current, options);
  }, []);

  return <div ref={ref} className="not-prose w-full max-w-full my-4"></div>;
}
