export type Downloads = {
  last_day: number;
  last_month: number;
  last_week: number;
};

export type Info = {
  author: string;
  author_email: string;
  bugtrack_url: null;
  classifiers: string[];
  description: string;
  description_content_type: string;
  docs_url: null;
  download_url: string;
  downloads: Downloads;
  home_page: string;
  keywords: string;
  license: string;
  maintainer: string;
  maintainer_email: string;
  name: string;
  package_url: string;
  platform: null;
  project_url: string;
  release_url: string;
  requires_dist: string[];
  requires_python: string;
  summary: string;
  version: string;
  yanked: boolean;
  yanked_reason: null;
};

export interface Digests {
  blake2b_256: string;
  md5: string;
  sha256: string;
}

export type Releases = {
  comment_text: string;
  digests: Digests;
  downloads: number;
  filename: string;
  has_sig: boolean;
  md5_digest: string;
  packagetype: string;
  python_version: string;
  requires_python: string;
  size: number;
  upload_time: Date;
  upload_time_iso_8601: Date;
  url: string;
  yanked: boolean;
  yanked_reason: null;
};
export type PyPIData = {
  info: Info;
  last_serial: number;
  releases: { [key: string]: Releases[] };
  urls: URL[];
  vulnerabilities: unknown[];
};
