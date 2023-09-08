import React, { useEffect, useRef } from "react";

import * as AsciinemaPlayer from "asciinema-player";

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

export type Props = {
  url: string;
  options?: Partial<AsciinemaOptions>;
};

export default function AsciinemaContainer({
  url,
  options = {},
}: Props): JSX.Element {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    AsciinemaPlayer.create(url, ref.current, options);
  }, [url, options]);

  return <div ref={ref} className="not-prose ap-container"></div>;
}
