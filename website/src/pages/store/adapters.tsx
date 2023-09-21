import React from "react";

import { translate } from "@docusaurus/Translate";

import AdapterPageContent from "@/components/Store/Content/Adapter";
import StoreLayout from "@/components/Store/Layout";

export default function StoreAdapters(): JSX.Element {
  const title = translate({
    id: "pages.store.adapter.title",
    message: "适配器商店",
    description: "Title for the adapter store page",
  });

  return (
    <StoreLayout title={title}>
      <AdapterPageContent />
    </StoreLayout>
  );
}
