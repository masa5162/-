"use client";

import { Region } from "@/types";

interface RegionChartProps {
  data: Record<Region, number>;
}

const regionLabels: Record<Region, string> = {
  "north-america": "北米",
  europe: "欧州",
  "asia-pacific": "APAC",
  "middle-east": "中東",
  "latin-america": "中南米",
  africa: "アフリカ",
  global: "グローバル",
};

const regionColors: Record<Region, string> = {
  "north-america": "var(--accent-blue)",
  europe: "var(--accent-green)",
  "asia-pacific": "var(--accent-yellow)",
  "middle-east": "var(--accent-purple)",
  "latin-america": "var(--accent-cyan)",
  africa: "var(--accent-red)",
  global: "var(--text-muted)",
};

export default function RegionChart({ data }: RegionChartProps) {
  const total = Object.values(data).reduce((a, b) => a + b, 0);
  const entries = Object.entries(data)
    .filter(([, count]) => count > 0)
    .sort(([, a], [, b]) => b - a) as [Region, number][];

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
          地域別分布 / By Region
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
        地域別分布 / By Region
      </h3>

      {/* Bar chart */}
      <div className="space-y-3">
        {entries.map(([region, count]) => {
          const pct = total > 0 ? (count / total) * 100 : 0;
          return (
            <div key={region}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-medium" style={{ color: "var(--text-secondary)" }}>
                  {regionLabels[region]}
                </span>
                <span className="text-xs font-mono" style={{ color: "var(--text-muted)" }}>
                  {count} ({pct.toFixed(0)}%)
                </span>
              </div>
              <div
                className="h-2 rounded-full overflow-hidden"
                style={{ backgroundColor: "var(--bg-secondary)" }}
              >
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${pct}%`,
                    backgroundColor: regionColors[region],
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
