import React, { useCallback, useEffect, useRef, useState } from "react";

import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useNonepressThemeConfig } from "@nullbot/docusaurus-theme-nonepress/client";
// @ts-expect-error: we need to make package have type: module
import copy from "copy-text-to-clipboard";

import IconCopy from "@theme/Icon/Copy";
import IconSuccess from "@theme/Icon/Success";

function HomeHeroInstallButton(): JSX.Element {
  const code = "pipx run nb-cli create";

  const [isCopied, setIsCopied] = useState(false);
  const copyTimeout = useRef<number | undefined>(undefined);

  const handleCopyCode = useCallback(() => {
    copy(code);
    setIsCopied(true);
    copyTimeout.current = window.setTimeout(() => {
      setIsCopied(false);
    }, 1500);
  }, [code]);

  useEffect(() => () => window.clearTimeout(copyTimeout.current), []);

  return (
    <button
      className="btn no-animation home-hero-copy"
      onClick={handleCopyCode}
    >
      <code>$ {code}</code>
      {isCopied ? <IconSuccess className="text-success" /> : <IconCopy />}
    </button>
  );
}

function HomeHero(): JSX.Element {
  const {
    siteConfig: { tagline },
  } = useDocusaurusContext();
  const {
    navbar: { logo },
  } = useNonepressThemeConfig();

  return (
    <div className="home-hero">
      <img src={logo!.src} alt={logo!.alt} className="home-hero-logo" />
      <h1 className="home-hero-title">
        <span className="text-primary">None</span>
        Bot
      </h1>
      <p className="home-hero-tagline">{tagline}</p>
      <div className="home-hero-actions">
        <Link to="/docs/" className="btn btn-primary">
          开始使用 <FontAwesomeIcon icon={["fas", "chevron-right"]} />
        </Link>
        <HomeHeroInstallButton />
      </div>
      <div className="home-hero-next">
        <FontAwesomeIcon icon={["fas", "angle-down"]} />
      </div>
    </div>
  );
}

export default React.memo(HomeHero);
