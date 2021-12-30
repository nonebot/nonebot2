import React from "react";

import Link from "@docusaurus/Link";

import type { Obj } from "../../libs/store";

export default function Card({
  name,
  desc,
  author,
  homepage,
}: Obj): JSX.Element {
  return (
    <div className="block max-w-full border rounded-lg outline-none no-underline bg-white shadow">
      <div>
        {name}
        {homepage && <Link href={homepage}></Link>}
      </div>
      <div>{desc}</div>
      <div>{author}</div>
    </div>
  );
}
