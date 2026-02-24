"use client";

import { DashboardStats } from "@/types";

interface StatsCardsProps {
  stats: DashboardStats;
}

export default function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      label: "Total News",
      labelJa: "ニュース総数",
      value: stats.totalNews,
      accent: "var(--accent-blue)",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2" />
        </svg>
      ),
    },
    {
      label: "M&A Deals",
      labelJa: "M&A案件数",
      value: stats.totalDeals,
      accent: "var(--accent-green)",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
        </svg>
      ),
    },
    {
      label: "Today's Updates",
      labelJa: "本日の更新",
      value: stats.todayNews + stats.todayDeals,
      accent: "var(--accent-yellow)",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 6v6l4 2" />
        </svg>
      ),
    },
    {
      label: "Deal Volume",
      labelJa: "取引総額",
      value: stats.totalDealValue,
      accent: "var(--accent-purple)",
      icon: (
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="12" y1="1" x2="12" y2="23" />
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
        </svg>
      ),
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, i) => (
        <div
          key={i}
          className="rounded-xl p-4 animate-fade-in"
          style={{
            backgroundColor: "var(--bg-card)",
            border: "1px solid var(--border-color)",
            animationDelay: `${i * 50}ms`,
          }}
        >
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>
              {card.label}
            </span>
            <div style={{ color: card.accent }}>{card.icon}</div>
          </div>
          <div className="text-2xl font-bold" style={{ color: card.accent }}>
            {card.value}
          </div>
          <div className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
            {card.labelJa}
          </div>
        </div>
      ))}
    </div>
  );
}
