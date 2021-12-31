import React from "react";

export default function ModalAction({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return <div className="px-4 py-2 flex justify-end">{children}</div>;
}
