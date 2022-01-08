import clsx from "clsx";
import React from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Logo from "@theme/Logo";

import styles from "./styles.module.css";

export type Message = {
  position?: "left" | "right";
  msg: string;
};

function MessageBox({
  msg,
  isRight,
}: {
  msg: string;
  isRight: boolean;
}): JSX.Element {
  return (
    <div
      className={clsx(styles.message, {
        [styles.messageRight]: isRight,
      })}
    >
      {isRight ? (
        <div className={clsx("bg-cyan-600 text-base", styles.messageAvatar)}>
          <FontAwesomeIcon icon={["fas", "user"]} />
        </div>
      ) : (
        <div className={clsx("transparent", styles.messageAvatar)}>
          <Logo imageClassName="h-full w-full" disabled />
        </div>
      )}
      <div
        className={clsx(styles.messageBox, { "order-first": isRight })}
        dangerouslySetInnerHTML={{
          __html: msg.replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;"),
        }}
      ></div>
    </div>
  );
}

export default function Messenger({
  msgs = [],
}: {
  msgs?: Message[];
}): JSX.Element {
  const isRight = (msg: Message): boolean => msg.position === "right";

  return (
    <div className="block w-full max-w-full my-4 rounded shadow-md outline-none no-underline bg-light-nonepress-100 dark:bg-dark-nonepress-100">
      <header className="flex items-center h-12 px-4 bg-blue-500 text-white rounded-t-[inherit]">
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
      <div className="p-3 min-h-[150px]">
        {msgs.map((msg, i) => (
          <MessageBox msg={msg.msg} isRight={isRight(msg)} key={i} />
        ))}
      </div>
      <div className="px-3">
        <div className="flex flex-row items-center">
          <div className="flex-1 p-1 max-w-full">
            <input className="w-full rounded bg-light dark:bg-dark" />
          </div>
          <div className="flex-initial grow-0 w-fit">
            <button className="h-7 px-3 rounded-full bg-blue-500 text-white">
              <span>发送</span>
            </button>
          </div>
        </div>
        <div className="flex flex-row items-center text-center text-base text-gray-600">
          <div className="p-1 shrink-0 grow-0 basis-1/6">
            <FontAwesomeIcon icon={["fas", "microphone"]} />
          </div>
          <div className="p-1 shrink-0 grow-0 basis-1/6">
            <FontAwesomeIcon icon={["fas", "image"]} />
          </div>
          <div className="p-1 shrink-0 grow-0 basis-1/6">
            <FontAwesomeIcon icon={["fas", "camera"]} />
          </div>
          <div className="p-1 shrink-0 grow-0 basis-1/6">
            <FontAwesomeIcon icon={["fas", "wallet"]} />
          </div>
          <div className="p-1 shrink-0 grow-0 basis-1/6">
            <FontAwesomeIcon icon={["fas", "smile-wink"]} />
          </div>
          <div className="p-1 shrink-0 grow-0 basis-1/6">
            <FontAwesomeIcon icon={["fas", "plus-circle"]} />
          </div>
        </div>
      </div>
    </div>
  );
}
