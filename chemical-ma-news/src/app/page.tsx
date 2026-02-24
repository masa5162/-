import { getNews, getDeals, getStats, getMeta } from "@/lib/store";
import Header from "@/components/Header";
import StatsCards from "@/components/StatsCards";
import NewsCard from "@/components/NewsCard";
import DealCard from "@/components/DealCard";
import RegionChart from "@/components/RegionChart";
import CategoryChart from "@/components/CategoryChart";
import Link from "next/link";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const [news, deals, stats, meta] = await Promise.all([
    getNews(),
    getDeals(),
    getStats(),
    getMeta(),
  ]);

  const latestNews = news.slice(0, 6);
  const latestDeals = deals.slice(0, 4);
  const maNews = news.filter((n) => n.category === "ma").slice(0, 5);

  return (
    <div className="min-h-screen" style={{ backgroundColor: "var(--bg-primary)" }}>
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Last Updated */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold" style={{ color: "var(--text-primary)" }}>
              Dashboard
            </h2>
            <p className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
              化学業界M&A・ニュース ダッシュボード
            </p>
          </div>
          {meta.lastFetched && (
            <div
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg"
              style={{
                backgroundColor: "var(--bg-card)",
                border: "1px solid var(--border-color)",
              }}
            >
              <div
                className="w-2 h-2 rounded-full pulse-glow"
                style={{ backgroundColor: "var(--accent-green)" }}
              />
              <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                Last updated: {new Date(meta.lastFetched).toLocaleString("ja-JP")}
              </span>
            </div>
          )}
        </div>

        {/* Stats Cards */}
        <StatsCards stats={stats} />

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          {/* Left Column: News Feed */}
          <div className="lg:col-span-2 space-y-4">
            {/* M&A Highlights */}
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
                M&A ハイライト / M&A Highlights
              </h3>
              <Link
                href="/deals"
                className="text-xs font-medium"
                style={{ color: "var(--accent-blue)" }}
              >
                View All →
              </Link>
            </div>

            <div className="space-y-3">
              {latestDeals.map((deal) => (
                <DealCard key={deal.id} deal={deal} />
              ))}
            </div>

            {/* Latest News */}
            <div className="flex items-center justify-between mt-6">
              <h3 className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
                最新ニュース / Latest News
              </h3>
              <Link
                href="/news"
                className="text-xs font-medium"
                style={{ color: "var(--accent-blue)" }}
              >
                View All →
              </Link>
            </div>

            <div className="space-y-3">
              {latestNews.map((article) => (
                <NewsCard key={article.id} article={article} />
              ))}
            </div>
          </div>

          {/* Right Column: Charts & M&A News */}
          <div className="space-y-4">
            <RegionChart data={stats.regionBreakdown} />
            <CategoryChart data={stats.categoryBreakdown} />

            {/* M&A News Sidebar */}
            <div
              className="rounded-xl p-5"
              style={{
                backgroundColor: "var(--bg-card)",
                border: "1px solid var(--border-color)",
              }}
            >
              <h3 className="text-sm font-semibold mb-4" style={{ color: "var(--text-primary)" }}>
                M&A ニュース速報
              </h3>
              <div className="space-y-3">
                {maNews.map((article) => (
                  <a
                    key={article.id}
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block p-3 rounded-lg transition-colors"
                    style={{ backgroundColor: "var(--bg-secondary)" }}
                  >
                    <h4
                      className="text-xs font-medium leading-snug mb-1"
                      style={{ color: "var(--text-primary)" }}
                    >
                      {article.title}
                    </h4>
                    <div className="flex items-center gap-2">
                      {article.dealValue && (
                        <span
                          className="text-xs font-semibold"
                          style={{ color: "var(--accent-yellow)" }}
                        >
                          {article.dealValue}
                        </span>
                      )}
                      <span className="text-xs" style={{ color: "var(--text-muted)" }}>
                        {article.source}
                      </span>
                    </div>
                  </a>
                ))}
              </div>
            </div>

            {/* Data Sources Info */}
            <div
              className="rounded-xl p-5"
              style={{
                backgroundColor: "var(--bg-card)",
                border: "1px solid var(--border-color)",
              }}
            >
              <h3 className="text-sm font-semibold mb-3" style={{ color: "var(--text-primary)" }}>
                データソース / Sources
              </h3>
              <div className="space-y-2">
                {[
                  "C&EN / ICIS / Chemical Week",
                  "化学工業日報 / 日本経済新聞",
                  "CHEManager / CEFIC",
                  "Reuters / Bloomberg",
                  "Asian Chemical News",
                ].map((source) => (
                  <div
                    key={source}
                    className="flex items-center gap-2"
                  >
                    <div
                      className="w-1.5 h-1.5 rounded-full"
                      style={{ backgroundColor: "var(--accent-green)" }}
                    />
                    <span className="text-xs" style={{ color: "var(--text-secondary)" }}>
                      {source}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer
        className="border-t mt-8 py-4"
        style={{ borderColor: "var(--border-color)" }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-xs" style={{ color: "var(--text-muted)" }}>
            Chemical M&A News Dashboard | 化学業界M&Aニュースダッシュボード | Daily auto-update enabled
          </p>
        </div>
      </footer>
    </div>
  );
}
