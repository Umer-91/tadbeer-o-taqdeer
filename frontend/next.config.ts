import type { NextConfig } from "next";

const config: NextConfig = {
  transpilePackages: ["three"],
  poweredByHeader: false,
  reactStrictMode: true,
};
export default config;
