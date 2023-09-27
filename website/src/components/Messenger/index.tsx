import React from "react";

import clsx from "clsx";

import useBaseUrl from "@docusaurus/useBaseUrl";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useNonepressThemeConfig } from "@nullbot/docusaurus-theme-nonepress/client";

import "./styles.css";
import ThemedImage from "@theme/ThemedImage";

export type Message = {
  msg: string;
  position?: "left" | "right";
  monospace?: boolean;
};

function MessageBox({
  msg,
  position = "left",
  monospace = false,
}: Message): JSX.Element {
  const {
    navbar: { logo },
  } = useNonepressThemeConfig();
  const sources = {
    light: useBaseUrl(logo!.src),
    dark: useBaseUrl(logo!.srcDark || logo!.src),
  };

  const isRight = position === "right";

  return (
    <div className={clsx("chat", isRight ? "chat-end" : "chat-start")}>
      <div className="chat-image avatar">
        <div
          className={clsx(
            "messenger-chat-avatar",
            isRight && "messenger-chat-avatar-user"
          )}
        >
          {isRight ? (
            <FontAwesomeIcon icon={["fas", "user"]} />
          ) : (
            <ThemedImage sources={sources} />
          )}
        </div>
      </div>
      <div
        className={clsx(
          "chat-bubble messenger-chat-bubble",
          monospace && "font-mono"
        )}
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
  return (
    <div className="messenger-container">
      <header className="messenger-title">
        <div className="messenger-title-back">
          <FontAwesomeIcon icon={["fas", "chevron-left"]} />
        </div>
        <div className="messenger-title-name">
          <span>NoneBot</span>
        </div>
        <div className="messenger-title-more">
          <FontAwesomeIcon icon={["fas", "bars"]} />
        </div>
      </header>
      <div className="messenger-chat">
        {msgs.map((msg, i) => (
          <MessageBox {...msg} key={i} />
        ))}
      </div>
      <div className="messenger-footer">
        <div className="messenger-footer-action">
          <div className="messenger-footer-action-input">
            <input
              className="input input-xs input-bordered input-info w-full"
              readOnly
            />
          </div>
          <div className="messenger-footer-action-send">
            <button className="btn btn-xs btn-info no-animation text-white">
              发送
            </button>
          </div>
        </div>
        <div className="messenger-footer-tools">
          <div>
            <FontAwesomeIcon icon={["fas", "microphone"]} />
          </div>
          <div>
            <FontAwesomeIcon icon={["fas", "image"]} />
          </div>
          <div>
            <FontAwesomeIcon icon={["fas", "camera"]} />
          </div>
          <div>
            <FontAwesomeIcon icon={["fas", "wallet"]} />
          </div>
          <div>
            <FontAwesomeIcon icon={["fas", "smile-wink"]} />
          </div>
          <div>
            <FontAwesomeIcon icon={["fas", "plus-circle"]} />
          </div>
        </div>
      </div>
    </div>
  );
}
