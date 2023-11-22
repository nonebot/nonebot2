import React, { useEffect, useState } from "react";

import clsx from "clsx";

import "./styles.css";

export type Props = {
  children?: React.ReactNode;
  className?: string;
  title: string;
  useCustomTitle?: boolean;
  backdropExit?: boolean;
  setOpenModal: (isOpen: boolean) => void;
};

export default function Modal({
  setOpenModal,
  className,
  children,
  useCustomTitle,
  backdropExit,
  title,
}: Props): JSX.Element {
  const [transitionClass, setTransitionClass] = useState<string>("");

  const onFadeIn = () => setTransitionClass("fade-in");
  const onFadeOut = () => setTransitionClass("fade-out");
  const onTransitionEnd = () =>
    transitionClass === "fade-out" && setOpenModal(false);

  useEffect(onFadeIn, []);

  return (
    <div className={clsx("nb-modal-root", className)}>
      <div
        className={clsx("nb-modal-backdrop", transitionClass)}
        onTransitionEnd={onTransitionEnd}
        onClick={() => backdropExit && onFadeOut()}
      />
      <div className={clsx("nb-modal-container", transitionClass)}>
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            {!useCustomTitle && (
              <div className="nb-modal-title">
                {title}
                <div className="card-actions ml-auto">
                  <button className="btn btn-square btn-sm" onClick={onFadeOut}>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-6 w-6"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            )}
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
