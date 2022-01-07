import React from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export type Message = {
  position?: "left" | "right";
  msg: string;
};

export default function Messenger() {
  return (
    <div className="block w-full max-w-full rounded shadow-md outline-none no-underline bg-light-nonepress-100 dark:bg-dark-nonepress-100">
      <header className="flex items-center h-12 px-4 bg-blue-500 text-white">
        <div className="text-left text-base grow">
          <FontAwesomeIcon icon={["fas", "chevron-left"]} />
        </div>
        <div className="flex-initial grow-0">
          <span className="text-xl font-bold">NoneBot</span>
        </div>
        <div className="text-right text-base grow">
          <FontAwesomeIcon icon={["fas", "user"]} />
        </div>
      </header>
    </div>
  );
}
