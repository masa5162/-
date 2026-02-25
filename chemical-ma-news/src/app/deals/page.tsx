"use client";

import { useState, useEffect } from "react";
import Header from "@/components/Header";
import DealCard from "@/components/DealCard";
import FilterBar from "@/components/FilterBar";
import { MaDeal, DealStatus } from "@/types";

export default function DealsPage() {
  const [deals, setDeals] = useState<MaDeal[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState<DealStatus | "all">("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDeals = async () => {
      setLoading(true);
      const params = new URLSearchParams({
        page: page.toString(),
        limit: "20",
      });
      if (search) params.set("q", search);
      if (status !== "all") params.set("status", status);

      try {
        const res = await fetch(`/api/deals?${params}`);
        const data = await res.json();
        setDeals(data.deals);
        setTotal(data.total);
        setTotalPages(data.totalPages);
      } catch (error) {
        console.error("Failed to fetch deals:", error);
      }
      setLoading(false);
    };

    fetchDeals();
  }, [page, search, status]);

  useEffect(() => {
    setPage(1);
  }, [search, status]);

  // Summary stats
  const completedDeals = deals.filter((d) => d.status === "completed").length;
  const pendingDeals = deals.filter(
    (d) => d.status === "announced" || d.status === "pending"
  ).length;

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--bg-primary)" }}>
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold" style={{ color: "var(--text-primary)" }}>
              M&A Deals
            </h2>
            <p className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
              化学業界M&A案件一覧 | {total} deals
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-center">
              <div className="text-lg font-bold" style={{ color: "var(--accent-green)" }}>
                {completedDeals}
              </div>
              <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                完了 / Done
              </div>
            </div>
            <div className="text-center">
              <div className="text-lg font-bold" style={{ color: "var(--accent-yellow)" }}>
                {pendingDeals}
              </div>
              <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                進行中 / Active
              </div>
            </div>
          </div>
        </div>

        <div className="mb-6">
          <FilterBar
            type="deals"
            search={search}
            onSearchChange={setSearch}
            status={status}
            onStatusChange={setStatus}
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
        ) : deals.length === 0 ? (
          <div
            className="text-center py-20 rounded-xl"
            style={{
              backgroundColor: "var(--bg-card)",
              border: "1px solid var(--border-color)",
            }}
          >
            <p className="text-sm" style={{ color: "var(--text-muted)" }}>
              該当するM&A案件が見つかりません / No deals found
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-4">
              {deals.map((deal, i) => (
                <div key={deal.id} style={{ animationDelay: `${i * 50}ms` }}>
                  <DealCard deal={deal} />
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
