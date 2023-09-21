import React from "react";

import { translate } from "@docusaurus/Translate";

import PluginPageContent from "@/components/Store/Content/Plugin";
import StoreLayout from "@/components/Store/Layout";

export default function StorePlugins(): JSX.Element {
  const title = translate({
    id: "pages.store.plugin.title",
    message: "插件商店",
    description: "Title for the plugin store page",
  });

  return (
    <StoreLayout title={title}>
      <PluginPageContent />
    </StoreLayout>
  );
}
