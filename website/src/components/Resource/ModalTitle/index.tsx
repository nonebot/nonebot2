import React from "react";

export default function ModalTitle({ title }: { title: string }): JSX.Element {
  return (
    <div className="px-6 pt-4 pb-2 font-medium text-xl">
      <span>{title}</span>
    </div>
  );
}
