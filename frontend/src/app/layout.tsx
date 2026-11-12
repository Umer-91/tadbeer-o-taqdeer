import type { Metadata } from "next";
import "@fontsource-variable/manrope";
import "@fontsource/noto-nastaliq-urdu/400.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "تدبیر و تقدیر · Tadbeer-o-Taqdeer",
  description:
    "Where Strategy Shapes Destiny. A synthetic research experience exploring quantum-assisted recovery of roads, electricity, and water.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
