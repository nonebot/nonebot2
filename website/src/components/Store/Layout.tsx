import React from "react";

import { PageMetadata } from "@docusaurus/theme-common";
import { useDocsVersionCandidates } from "@docusaurus/theme-common/internal";
import { useVersionedSidebar } from "@nullbot/docusaurus-plugin-getsidebar/client";
import { SidebarContentFiller } from "@nullbot/docusaurus-theme-nonepress/contexts";

import BackToTopButton from "@theme/BackToTopButton";
import Layout from "@theme/Layout";
import Page from "@theme/Page";

import "./styles.css";

const SIDEBAR_ID = "ecosystem";

type Props = {
  title: string;
  children: React.ReactNode;
};

function StorePage({ title, children }: Props): JSX.Element {
  const sidebarItems = useVersionedSidebar(
    useDocsVersionCandidates()[0].name,
    SIDEBAR_ID
  )!;

  return (
    <Page hideTableOfContents reduceContentWidth={false}>
      <SidebarContentFiller items={sidebarItems} />
      <article className="prose max-w-full">
        <h1 className="store-title">{title}</h1>
        {children}
      </article>
    </Page>
  );
}

export default function StoreLayout({ title, ...props }: Props): JSX.Element {
  return (
    <>
      <PageMetadata title={title} />

      <Layout>
        <BackToTopButton />

        <StorePage title={title} {...props} />
      </Layout>
    </>
  );
}
