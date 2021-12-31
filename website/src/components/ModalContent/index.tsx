import React from "react";

export default function ModalContent({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return <div className="px-6 pb-5 w-full">{children}</div>;
}
