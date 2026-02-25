"use client";

import { Region, NewsCategory, DealStatus } from "@/types";

interface FilterBarProps {
  type: "news" | "deals";
  search: string;
  onSearchChange: (value: string) => void;
  region?: Region | "all";
  onRegionChange?: (value: Region | "all") => void;
  category?: NewsCategory | "all";
  onCategoryChange?: (value: NewsCategory | "all") => void;
  status?: DealStatus | "all";
  onStatusChange?: (value: DealStatus | "all") => void;
}

const regionOptions: { value: Region | "all"; label: string }[] = [
  { value: "all", label: "全地域 / All" },
  { value: "north-america", label: "北米 / NA" },
  { value: "europe", label: "欧州 / EU" },
  { value: "asia-pacific", label: "アジア太平洋 / APAC" },
  { value: "middle-east", label: "中東 / ME" },
  { value: "latin-america", label: "中南米 / LATAM" },
  { value: "global", label: "グローバル / Global" },
];

const categoryOptions: { value: NewsCategory | "all"; label: string }[] = [
  { value: "all", label: "全カテゴリ / All" },
  { value: "ma", label: "M&A" },
  { value: "ipo", label: "IPO" },
  { value: "earnings", label: "決算 / Earnings" },
  { value: "regulation", label: "規制 / Regulation" },
  { value: "sustainability", label: "ESG / Sustainability" },
  { value: "innovation", label: "技術革新 / Innovation" },
  { value: "market", label: "市況 / Market" },
];

const statusOptions: { value: DealStatus | "all"; label: string }[] = [
  { value: "all", label: "全ステータス / All" },
  { value: "announced", label: "発表済 / Announced" },
  { value: "pending", label: "審査中 / Pending" },
  { value: "completed", label: "完了 / Completed" },
  { value: "withdrawn", label: "撤回 / Withdrawn" },
  { value: "rumored", label: "観測 / Rumored" },
];

export default function FilterBar({
  type,
  search,
  onSearchChange,
  region,
  onRegionChange,
  category,
  onCategoryChange,
  status,
  onStatusChange,
}: FilterBarProps) {
  return (
    <div
      className="rounded-xl p-4 flex flex-wrap items-center gap-3"
      style={{
        backgroundColor: "var(--bg-card)",
        border: "1px solid var(--border-color)",
      }}
    >
      {/* Search */}
      <div className="relative flex-1 min-w-[200px]">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--text-muted)"
          strokeWidth="2"
        >
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.35-4.35" />
        </svg>
        <input
          type="text"
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="検索 / Search..."
          className="w-full pl-10 pr-4 py-2 rounded-lg text-sm outline-none"
          style={{
            backgroundColor: "var(--bg-secondary)",
            color: "var(--text-primary)",
            border: "1px solid var(--border-color)",
          }}
        />
      </div>

      {/* Region Filter (News) */}
      {type === "news" && onRegionChange && (
        <select
          value={region}
          onChange={(e) => onRegionChange(e.target.value as Region | "all")}
          className="px-3 py-2 rounded-lg text-sm outline-none cursor-pointer"
          style={{
            backgroundColor: "var(--bg-secondary)",
            color: "var(--text-primary)",
            border: "1px solid var(--border-color)",
          }}
        >
          {regionOptions.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      )}

      {/* Category Filter (News) */}
      {type === "news" && onCategoryChange && (
        <select
          value={category}
          onChange={(e) =>
            onCategoryChange(e.target.value as NewsCategory | "all")
          }
          className="px-3 py-2 rounded-lg text-sm outline-none cursor-pointer"
          style={{
            backgroundColor: "var(--bg-secondary)",
            color: "var(--text-primary)",
            border: "1px solid var(--border-color)",
          }}
        >
          {categoryOptions.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      )}

      {/* Status Filter (Deals) */}
      {type === "deals" && onStatusChange && (
        <select
          value={status}
          onChange={(e) =>
            onStatusChange(e.target.value as DealStatus | "all")
          }
          className="px-3 py-2 rounded-lg text-sm outline-none cursor-pointer"
          style={{
            backgroundColor: "var(--bg-secondary)",
            color: "var(--text-primary)",
            border: "1px solid var(--border-color)",
          }}
        >
          {statusOptions.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      )}
    </div>
  );
}
