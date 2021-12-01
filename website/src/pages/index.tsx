import Hero, { HeroFeatureSingle } from "@theme/Hero";

import CodeBlock from "@theme/CodeBlock";
import Layout from "@theme/Layout";
import React from "react";
import clsx from "clsx";
import styles from "./index.module.css";

export default function Home() {
  const feature = {
    title: "Develop",
    tagline: "fast to code",
    description: "仅需两步，即可开始编写你的机器人",
  };

  return (
    <Layout>
      <Hero />
      <HeroFeatureSingle {...feature}>
        <CodeBlock
          title="Installation"
          className={clsx("inline-block", styles.homeCodeBlock)}
          metastring="bash"
        >
          {"pip install nb-cli\nnb create"}
        </CodeBlock>
      </HeroFeatureSingle>
    </Layout>
  );
}
