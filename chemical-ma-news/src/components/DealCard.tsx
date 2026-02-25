"use client";

import { MaDeal } from "@/types";
import { formatDistanceToNow } from "date-fns";
import { ja } from "date-fns/locale";

interface DealCardProps {
  deal: MaDeal;
}

const statusColors: Record<string, string> = {
  announced: "var(--accent-blue)",
  pending: "var(--accent-yellow)",
  completed: "var(--accent-green)",
  withdrawn: "var(--accent-red)",
  rumored: "var(--accent-purple)",
};

const statusLabels: Record<string, string> = {
  announced: "発表済",
  pending: "審査中",
  completed: "完了",
  withdrawn: "撤回",
  rumored: "観測",
};

export default function DealCard({ deal }: DealCardProps) {
  const timeAgo = formatDistanceToNow(new Date(deal.announcedDate), {
    addSuffix: true,
    locale: ja,
  });

  return (
    <a
      href={deal.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block rounded-xl p-5 transition-all duration-200 animate-fade-in group"
      style={{
        backgroundColor: "var(--bg-card)",
        border: "1px solid var(--border-color)",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = "var(--bg-card-hover)";
        e.currentTarget.style.borderColor = statusColors[deal.status] || "var(--border-color)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = "var(--bg-card)";
        e.currentTarget.style.borderColor = "var(--border-color)";
      }}
    >
      {/* Status & Value Row */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span
            className="w-2 h-2 rounded-full"
            style={{ backgroundColor: statusColors[deal.status] }}
          />
          <span
            className="text-xs font-semibold uppercase tracking-wide"
            style={{ color: statusColors[deal.status] }}
          >
            {statusLabels[deal.status]}
          </span>
          {deal.subsector && (
            <span
              className="px-2 py-0.5 rounded text-xs"
              style={{
                backgroundColor: "var(--bg-secondary)",
                color: "var(--text-muted)",
              }}
            >
              {deal.subsector}
            </span>
          )}
        </div>
        {deal.dealValue && (
          <span
            className="text-lg font-bold"
            style={{ color: "var(--accent-yellow)" }}
          >
            {deal.dealValue}
          </span>
        )}
      </div>

      {/* Title */}
      <h3
        className="text-sm font-semibold mb-3 group-hover:underline"
        style={{ color: "var(--text-primary)" }}
      >
        {deal.title}
      </h3>

      {/* Acquirer -> Target Flow */}
      <div
        className="flex items-center gap-3 mb-3 p-3 rounded-lg"
        style={{ backgroundColor: "var(--bg-secondary)" }}
      >
        <div className="flex-1 text-center">
          <div className="text-xs mb-1" style={{ color: "var(--text-muted)" }}>
            Acquirer / 買い手
          </div>
          <div className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
            {deal.acquirer}
          </div>
          <div className="text-xs" style={{ color: "var(--text-muted)" }}>
            {deal.acquirerCountry}
          </div>
        </div>
        <div style={{ color: "var(--accent-blue)" }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </div>
        <div className="flex-1 text-center">
          <div className="text-xs mb-1" style={{ color: "var(--text-muted)" }}>
            Target / 売り手
          </div>
          <div className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
            {deal.target}
          </div>
          <div className="text-xs" style={{ color: "var(--text-muted)" }}>
            {deal.targetCountry}
          </div>
        </div>
      </div>

      {/* Summary */}
      <p
        className="text-xs leading-relaxed mb-3 line-clamp-2"
        style={{ color: "var(--text-secondary)" }}
      >
        {deal.summary}
      </p>

      {/* Footer */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 flex-wrap">
          {deal.tags.slice(0, 3).map((tag) => (
            <span
              key={tag}
              className="px-1.5 py-0.5 rounded text-xs"
              style={{
                backgroundColor: "var(--bg-secondary)",
                color: "var(--text-muted)",
              }}
            >
              #{tag}
            </span>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs" style={{ color: "var(--text-muted)" }}>
            {deal.source}
          </span>
          <span className="text-xs" style={{ color: "var(--text-muted)" }}>
            {timeAgo}
          </span>
        </div>
      </div>
    </a>
  );
}
