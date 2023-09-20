import React from "react";

import { translate } from "@docusaurus/Translate";
import { PageMetadata } from "@docusaurus/theme-common";
import { useDocsVersionCandidates } from "@docusaurus/theme-common/internal";
import { useVersionedSidebar } from "@nullbot/docusaurus-plugin-getsidebar/client";
import { SidebarContentFiller } from "@nullbot/docusaurus-theme-nonepress/contexts";

import BackToTopButton from "@theme/BackToTopButton";
import Layout from "@theme/Layout";
import Page from "@theme/Page";

import PluginPageContent from "@/components/Store/Plugin";

function PluginPage({ title }: { title: string }): JSX.Element {
  const sidebarItems = useVersionedSidebar(
    useDocsVersionCandidates()[0].name,
    "ecosystem"
  )!;

  return (
    <Page hideTableOfContents reduceContentWidth={false}>
      <SidebarContentFiller items={sidebarItems} />
      <article className="prose max-w-full">
        <h1 className="text-center">{title}</h1>
        <PluginPageContent />
      </article>
    </Page>
  );
}

export default function StorePlugins(): JSX.Element {
  const title = translate({
    id: "pages.store.plugins.title",
    message: "插件商店",
    description: "Title for the plugin store page",
  });

  return (
    <>
      <PageMetadata title={title} />

      <Layout>
        <BackToTopButton />

        <PluginPage title={title} />
      </Layout>
    </>
  );
}
