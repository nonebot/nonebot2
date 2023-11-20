import React, { useEffect, useState } from "react";

import clsx from "clsx";

import "./styles.css";

export type Props = {
  children?: React.ReactNode;
  className?: string;
  title: string;
  setOpenModal: (isOpen: boolean) => void;
};

export default function Modal({
  setOpenModal,
  className,
  children,
  title,
}: Props): JSX.Element {
  const [transitionClass, setTransitionClass] = useState<string>("");

  const onFadeIn = () => setTransitionClass("fade-in");
  const onFadeOut = () => setTransitionClass("fade-out");
  const onTransitionEnd = () =>
    transitionClass === "fade-out" && setOpenModal(false);

  useEffect(onFadeIn, []);

  return (
    <div className={clsx("modal-root", className)}>
      <div
        className={clsx("modal-backdrop", transitionClass)}
        onTransitionEnd={onTransitionEnd}
      />
      <div className={clsx("modal-container", transitionClass)}>
        <div className="card bg-base-100 shadow-xl">
          <div className="card-body">
            <div className="modal-title">
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
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
