import { useState } from "react";
import Link from "@docusaurus/Link";
import clsx from "clsx";

interface Props {
  className?: string;
  authorLink: string;
  authorAvatar: string;
}

export default function Avatar({ authorLink, authorAvatar, className }: Props) {
  const [loaded, setLoaded] = useState(false);
  const onLoad = () => setLoaded(true);

  return (
    <div className="avatar">
      <div className={className}>
        <Link href={authorLink}>
          <div className="relative w-full h-full">
            {!loaded && (
              <div
                className={clsx(
                  "absolute inset-0 rounded-full bg-gray-200",
                  "animate-pulse"
                )}
              />
            )}
            <img
              src={authorAvatar}
              onLoad={onLoad}
              className={clsx(
                "w-full h-full rounded-full object-cover",
                "transition-opacity duration-300",
                loaded ? "opacity-100" : "opacity-0"
              )}
              alt="Avatar"
            />
          </div>
        </Link>
      </div>
    </div>
  );
}
