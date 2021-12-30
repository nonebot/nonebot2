import { useLayoutEffect, useState } from "react";

import { useResizeNotifier } from "./resize";

export function getElementWidth(element: HTMLElement) {
  const style = getComputedStyle(element);

  return (
    styleMetricToInt(style.marginLeft) +
    getWidth(element) +
    styleMetricToInt(style.marginRight)
  );
}

export function getContentWidth(element: HTMLElement) {
  const style = getComputedStyle(element);

  return (
    element.getBoundingClientRect().width -
    styleMetricToInt(style.borderLeftWidth) -
    styleMetricToInt(style.paddingLeft) -
    styleMetricToInt(style.paddingRight) -
    styleMetricToInt(style.borderRightWidth)
  );
}

export function getNonContentWidth(element: HTMLElement) {
  const style = getComputedStyle(element);

  return (
    styleMetricToInt(style.marginLeft) +
    styleMetricToInt(style.borderLeftWidth) +
    styleMetricToInt(style.paddingLeft) +
    styleMetricToInt(style.paddingRight) +
    styleMetricToInt(style.borderRightWidth) +
    styleMetricToInt(style.marginRight)
  );
}

export function getWidth(element: HTMLElement) {
  return element.getBoundingClientRect().width;
}

function styleMetricToInt(styleAttribute: string | null) {
  return styleAttribute ? parseInt(styleAttribute) : 0;
}

export function useContentWidth(element: HTMLElement | undefined) {
  const [width, setWidth] = useState<number>();

  function syncWidth() {
    const newWidth = element ? getContentWidth(element) : undefined;

    if (width !== newWidth) {
      setWidth(newWidth);
    }
  }

  useResizeNotifier(element, syncWidth);

  useLayoutEffect(syncWidth);

  return width;
}
