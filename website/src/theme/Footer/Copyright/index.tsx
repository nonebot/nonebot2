import React from "react";

import Link from "@docusaurus/Link";
import Translate, { translate } from "@docusaurus/Translate";

import type { Props } from "@theme/Footer/Copyright";
import IconCloudflare from "@theme/Icon/Cloudflare";
import IconNetlify from "@theme/Icon/Netlify";
import OriginCopyright from "@theme-original/Footer/Copyright";

export default function FooterCopyright(props: Props) {
  return (
    <>
      <OriginCopyright {...props} />
      <div className="footer-support">
        <Translate
          id="theme.FooterCopyright.deployBy"
          description="The deploy by message."
        >
          Deployed by
        </Translate>
        <Link
          to="https://www.netlify.com/"
          title={translate({
            id: "theme.FooterCopyright.netlifyLinkTitle",
            message: "Go to the Netlify website",
            description: "The title attribute for the Netlify logo link",
          })}
        >
          <IconNetlify className="footer-support-icon" />
        </Link>
        <Link
          to="https://www.cloudflare.com/"
          title={translate({
            id: "theme.FooterCopyright.cloudflareLinkTitle",
            message: "Go to the Cloudflare website",
            description: "The title attribute for the Cloudflare logo link",
          })}
        >
          <IconCloudflare className="footer-support-icon" />
        </Link>
      </div>
    </>
  );
}
