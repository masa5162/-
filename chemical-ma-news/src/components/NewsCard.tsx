"use client";

import { NewsArticle } from "@/types";
import { formatDistanceToNow } from "date-fns";
import { ja } from "date-fns/locale";

interface NewsCardProps {
  article: NewsArticle;
}

const categoryColors: Record<string, string> = {
  ma: "var(--accent-green)",
  ipo: "var(--accent-purple)",
  earnings: "var(--accent-blue)",
  regulation: "var(--accent-red)",
  sustainability: "var(--accent-cyan)",
  innovation: "var(--accent-yellow)",
  market: "var(--accent-blue)",
  other: "var(--text-muted)",
};

const categoryLabels: Record<string, string> = {
  ma: "M&A",
  ipo: "IPO",
  earnings: "決算",
  regulation: "規制",
  sustainability: "ESG",
  innovation: "技術革新",
  market: "市況",
  other: "その他",
};

const regionFlags: Record<string, string> = {
  "north-america": "NA",
  europe: "EU",
  "asia-pacific": "AP",
  "middle-east": "ME",
  "latin-america": "LA",
  africa: "AF",
  global: "GL",
};

export default function NewsCard({ article }: NewsCardProps) {
  const timeAgo = formatDistanceToNow(new Date(article.publishedAt), {
    addSuffix: true,
    locale: ja,
  });

  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block rounded-xl p-4 transition-all duration-200 animate-fade-in group"
      style={{
        backgroundColor: "var(--bg-card)",
        border: "1px solid var(--border-color)",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = "var(--bg-card-hover)";
        e.currentTarget.style.borderColor = categoryColors[article.category] || "var(--border-color)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = "var(--bg-card)";
        e.currentTarget.style.borderColor = "var(--border-color)";
      }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span
              className="px-2 py-0.5 rounded text-xs font-semibold"
              style={{
                backgroundColor: `color-mix(in srgb, ${categoryColors[article.category]} 15%, transparent)`,
                color: categoryColors[article.category],
              }}
            >
              {categoryLabels[article.category] || article.category}
            </span>
            <span
              className="px-1.5 py-0.5 rounded text-xs font-mono"
              style={{
                backgroundColor: "var(--bg-secondary)",
                color: "var(--text-muted)",
              }}
            >
              {regionFlags[article.sourceRegion]}
            </span>
            {article.dealValue && (
              <span
                className="px-2 py-0.5 rounded text-xs font-semibold"
                style={{
                  backgroundColor: "color-mix(in srgb, var(--accent-yellow) 15%, transparent)",
                  color: "var(--accent-yellow)",
                }}
              >
                {article.dealValue}
              </span>
            )}
          </div>

          <h3
            className="text-sm font-semibold mb-1.5 leading-snug group-hover:underline"
            style={{ color: "var(--text-primary)" }}
          >
            {article.title}
          </h3>

          <p
            className="text-xs leading-relaxed mb-3 line-clamp-2"
            style={{ color: "var(--text-secondary)" }}
          >
            {article.summary}
          </p>

          <div className="flex items-center gap-3 flex-wrap">
            {article.companies && article.companies.length > 0 && (
              <div className="flex items-center gap-1">
                {article.companies.map((company) => (
                  <span
                    key={company}
                    className="px-1.5 py-0.5 rounded text-xs"
                    style={{
                      backgroundColor: "var(--bg-secondary)",
                      color: "var(--text-secondary)",
                    }}
                  >
                    {company}
                  </span>
                ))}
              </div>
            )}
            <div className="flex items-center gap-2 ml-auto">
              <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                {article.source}
              </span>
              <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                {timeAgo}
              </span>
            </div>
          </div>
        </div>
      </div>
    </a>
  );
}
