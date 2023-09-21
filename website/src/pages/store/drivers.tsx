import React from "react";

import { translate } from "@docusaurus/Translate";

import DriverPageContent from "@/components/Store/Content/Driver";
import StoreLayout from "@/components/Store/Layout";

export default function StoreDrivers(): JSX.Element {
  const title = translate({
    id: "pages.store.driver.title",
    message: "驱动器商店",
    description: "Title for the driver store page",
  });

  return (
    <StoreLayout title={title}>
      <DriverPageContent />
    </StoreLayout>
  );
}
