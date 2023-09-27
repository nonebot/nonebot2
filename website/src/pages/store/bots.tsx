import React from "react";

import { translate } from "@docusaurus/Translate";

import BotPageContent from "@/components/Store/Content/Bot";
import StoreLayout from "@/components/Store/Layout";

export default function StoreBots(): JSX.Element {
  const title = translate({
    id: "pages.store.bot.title",
    message: "机器人商店",
    description: "Title for the bot store page",
  });

  return (
    <StoreLayout title={title}>
      <BotPageContent />
    </StoreLayout>
  );
}
