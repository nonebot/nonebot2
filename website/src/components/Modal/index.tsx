import clsx from "clsx";
import React from "react";

export default function Modal({
  active,
  setActive,
  children,
}: {
  active: boolean;
  setActive: (active: boolean) => void;
  children: React.ReactNode;
}): JSX.Element {
  return (
    <>
      {/* overlay */}
      <div
        className={clsx(
          "fixed top-0 bottom-0 left-0 right-0 flex items-center justify-center transition z-[200]",
          {
            hidden: !active,
            "pointer-events-auto": active,
          }
        )}
        onClick={() => setActive(false)}
      >
        <div className="absolute top-0 bottom-0 left-0 right-0 h-full w-full bg-gray-800 opacity-[.46]"></div>
      </div>
      {/* modal */}
      <div
        className={clsx(
          "fixed top-0 left-0 flex items-center justify-center h-full w-full transition z-[201] pointer-events-none",
          { hidden: !active }
        )}
      >
        <div className="w-full max-w-[600px] max-h-[90%] overflow-y-auto rounded shadow-lg m-6 origin-center transition z-[inherit] pointer-events-auto thin-scrollbar">
          <div className="bg-light-nonepress-100 dark:bg-dark-nonepress-100">
            {children}
          </div>
        </div>
      </div>
    </>
  );
}
