"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Header() {
  const pathname = usePathname();

  const navItems = [
    { href: "/", label: "Dashboard", labelJa: "ダッシュボード" },
    { href: "/deals", label: "M&A Deals", labelJa: "M&A案件" },
    { href: "/news", label: "News", labelJa: "ニュース" },
  ];

  return (
    <header className="sticky top-0 z-50 border-b"
      style={{ backgroundColor: "var(--bg-secondary)", borderColor: "var(--border-color)" }}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold"
              style={{ backgroundColor: "var(--accent-blue)", color: "white" }}>
              CM
            </div>
            <div>
              <h1 className="text-lg font-bold" style={{ color: "var(--text-primary)" }}>
                Chemical M&A News
              </h1>
              <p className="text-xs" style={{ color: "var(--text-muted)" }}>
                化学業界 M&A・ニュース
              </p>
            </div>
          </div>

          <nav className="flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                  style={{
                    backgroundColor: isActive ? "var(--accent-blue)" : "transparent",
                    color: isActive ? "white" : "var(--text-secondary)",
                  }}
                >
                  <span>{item.label}</span>
                  <span className="hidden sm:inline text-xs ml-1 opacity-70">
                    {item.labelJa}
                  </span>
                </Link>
              );
            })}
          </nav>

          <div className="flex items-center gap-3">
            <FetchButton />
          </div>
        </div>
      </div>
    </header>
  );
}

function FetchButton() {
  const handleFetch = async () => {
    try {
      const res = await fetch("/api/cron", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        window.location.reload();
      } else {
        console.error("Fetch failed:", data.errors);
      }
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };

  return (
    <button
      onClick={handleFetch}
      className="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center gap-1.5"
      style={{
        backgroundColor: "var(--bg-card)",
        color: "var(--accent-green)",
        border: "1px solid var(--border-color)",
      }}
      title="Fetch latest news / 最新ニュースを取得"
    >
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M21 2v6h-6M3 12a9 9 0 0 1 15-6.7L21 8M3 22v-6h6M21 12a9 9 0 0 1-15 6.7L3 16" />
      </svg>
      Update
    </button>
  );
}
