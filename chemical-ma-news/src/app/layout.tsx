import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Chemical M&A News | 化学業界M&Aニュース",
  description:
    "Global Chemical Industry M&A Deals and News Dashboard - グローバル化学業界M&A案件・ニュースダッシュボード",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
