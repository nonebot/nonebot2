import React from "react";

import HomeFeatures from "./Feature";
import HomeHero from "./Hero";
import "./styles.css";

export default function HomeContent(): React.ReactNode {
  return (
    <div className="home-container">
      <HomeHero />
      <HomeFeatures />
    </div>
  );
}
