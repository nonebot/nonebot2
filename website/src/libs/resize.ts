import { useLayoutEffect, useRef } from "react";

import ResizeObserver from "resize-observer-polyfill";

export function useResizeNotifier(
  element: HTMLElement | undefined,
  callback: () => void
) {
  const callBackRef = useRef(callback);
  useLayoutEffect(() => {
    callBackRef.current = callback;
  }, [callback]);

  useLayoutEffect(() => {
    if (!element) return;

    const resizeObserver = new ResizeObserver(
      withResizeLoopDetection(() => {
        callBackRef.current!();
      })
    );

    resizeObserver.observe(element);

    return () => {
      resizeObserver.disconnect();
    };
  }, [element]);
}

function withResizeLoopDetection(callback: () => void) {
  return (entries: ResizeObserverEntry[], resizeObserver: ResizeObserver) => {
    const elements = entries.map((entry) => entry.target);

    const rectsBefore = elements.map((element) =>
      element.getBoundingClientRect()
    );

    callback();

    const rectsAfter = elements.map((element) =>
      element.getBoundingClientRect()
    );

    const changedElements = elements.filter(
      (_, i) => !areRectSizesEqual(rectsBefore[i], rectsAfter[i])
    );

    changedElements.forEach((element) =>
      unobserveUntilNextFrame(element, resizeObserver)
    );
  };
}

function unobserveUntilNextFrame(
  element: Element,
  resizeObserver: ResizeObserver
) {
  resizeObserver.unobserve(element);

  requestAnimationFrame(() => {
    resizeObserver.observe(element);
  });
}

function areRectSizesEqual(rect1: DOMRect, rect2: DOMRect) {
  return rect1.width === rect2.width && rect1.height === rect2.height;
}
