import React from "react";

import "./styles.css";
import HomeFeatures from "./Feature";
import HomeHero from "./Hero";

export default function HomeContent(): JSX.Element {
  return (
    <div className="home-container">
      <HomeHero />
      <HomeFeatures />
    </div>
  );
}
