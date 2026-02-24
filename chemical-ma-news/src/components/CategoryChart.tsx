"use client";

import { NewsCategory } from "@/types";

interface CategoryChartProps {
  data: Record<NewsCategory, number>;
}

const categoryLabels: Record<NewsCategory, string> = {
  ma: "M&A",
  ipo: "IPO",
  earnings: "決算",
  regulation: "規制",
  sustainability: "ESG",
  innovation: "技術革新",
  market: "市況",
  other: "その他",
};

const categoryColors: Record<NewsCategory, string> = {
  ma: "var(--accent-green)",
  ipo: "var(--accent-purple)",
  earnings: "var(--accent-blue)",
  regulation: "var(--accent-red)",
  sustainability: "var(--accent-cyan)",
  innovation: "var(--accent-yellow)",
  market: "var(--accent-blue)",
  other: "var(--text-muted)",
};

export default function CategoryChart({ data }: CategoryChartProps) {
  const total = Object.values(data).reduce((a, b) => a + b, 0);
  const entries = Object.entries(data)
    .filter(([, count]) => count > 0)
    .sort(([, a], [, b]) => b - a) as [NewsCategory, number][];

  if (total === 0) {
    return (
      <div
        className="rounded-xl p-5"
        style={{
          backgroundColor: "var(--bg-card)",
          border: "1px solid var(--border-color)",
        }}
      >
        <h3 className="text-sm font-semibold mb-4" style={{ color: "var(--text-primary)" }}>
          カテゴリ別 / By Category
        </h3>
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          データなし / No data
        </p>
      </div>
    );
  }

  return (
    <div
      className="rounded-xl p-5"
      style={{
        backgroundColor: "var(--bg-card)",
        border: "1px solid var(--border-color)",
      }}
    >
      <h3 className="text-sm font-semibold mb-4" style={{ color: "var(--text-primary)" }}>
        カテゴリ別 / By Category
      </h3>

      <div className="grid grid-cols-2 gap-2">
        {entries.map(([cat, count]) => {
          const pct = total > 0 ? (count / total) * 100 : 0;
          return (
            <div
              key={cat}
              className="flex items-center gap-2 p-2 rounded-lg"
              style={{ backgroundColor: "var(--bg-secondary)" }}
            >
              <div
                className="w-3 h-3 rounded-sm flex-shrink-0"
                style={{ backgroundColor: categoryColors[cat] }}
              />
              <div className="flex-1 min-w-0">
                <div className="text-xs font-medium truncate" style={{ color: "var(--text-secondary)" }}>
                  {categoryLabels[cat]}
                </div>
              </div>
              <div className="text-xs font-mono" style={{ color: "var(--text-muted)" }}>
                {count}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
