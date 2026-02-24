"use client";

import { useState, useEffect } from "react";
import Header from "@/components/Header";
import NewsCard from "@/components/NewsCard";
import FilterBar from "@/components/FilterBar";
import { NewsArticle, Region, NewsCategory } from "@/types";

export default function NewsPage() {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState("");
  const [region, setRegion] = useState<Region | "all">("all");
  const [category, setCategory] = useState<NewsCategory | "all">("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArticles = async () => {
      setLoading(true);
      const params = new URLSearchParams({
        page: page.toString(),
        limit: "20",
      });
      if (search) params.set("q", search);
      if (region !== "all") params.set("region", region);
      if (category !== "all") params.set("category", category);

      try {
        const res = await fetch(`/api/news?${params}`);
        const data = await res.json();
        setArticles(data.articles);
        setTotal(data.total);
        setTotalPages(data.totalPages);
      } catch (error) {
        console.error("Failed to fetch news:", error);
      }
      setLoading(false);
    };

    fetchArticles();
  }, [page, search, region, category]);

  useEffect(() => {
    setPage(1);
  }, [search, region, category]);

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--bg-primary)" }}>
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold" style={{ color: "var(--text-primary)" }}>
              Industry News
            </h2>
            <p className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
              化学業界ニュース一覧 | {total} articles
            </p>
          </div>
        </div>

        <div className="mb-6">
          <FilterBar
            type="news"
            search={search}
            onSearchChange={setSearch}
            region={region}
            onRegionChange={setRegion}
            category={category}
            onCategoryChange={setCategory}
          />
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div
              className="w-8 h-8 border-2 rounded-full animate-spin"
              style={{
                borderColor: "var(--border-color)",
                borderTopColor: "var(--accent-blue)",
              }}
            />
          </div>
        ) : articles.length === 0 ? (
          <div
            className="text-center py-20 rounded-xl"
            style={{
              backgroundColor: "var(--bg-card)",
              border: "1px solid var(--border-color)",
            }}
          >
            <p className="text-sm" style={{ color: "var(--text-muted)" }}>
              該当するニュースが見つかりません / No articles found
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-3">
              {articles.map((article, i) => (
                <div key={article.id} style={{ animationDelay: `${i * 30}ms` }}>
                  <NewsCard article={article} />
                </div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-2 mt-8">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="px-4 py-2 rounded-lg text-sm disabled:opacity-30"
                  style={{
                    backgroundColor: "var(--bg-card)",
                    color: "var(--text-primary)",
                    border: "1px solid var(--border-color)",
                  }}
                >
                  前へ / Prev
                </button>
                <span className="text-sm px-4" style={{ color: "var(--text-muted)" }}>
                  {page} / {totalPages}
                </span>
                <button
                  onClick={() => setPage(Math.min(totalPages, page + 1))}
                  disabled={page === totalPages}
                  className="px-4 py-2 rounded-lg text-sm disabled:opacity-30"
                  style={{
                    backgroundColor: "var(--bg-card)",
                    color: "var(--text-primary)",
                    border: "1px solid var(--border-color)",
                  }}
                >
                  次へ / Next
                </button>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}
