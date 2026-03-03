import { deals, advisoryReports } from "@/data/deals";

const STATUS_COLORS: Record<string, string> = {
  完了: "bg-green-100 text-green-800",
  進行中: "bg-blue-100 text-blue-800",
  検討中: "bg-yellow-100 text-yellow-800",
  中断: "bg-gray-100 text-gray-600",
};

export default function Home() {
  const recentDeals = deals.slice(0, 4);
  const latestReport = advisoryReports[0];

  return (
    <div className="space-y-10">
      {/* Hero */}
      <section className="bg-gradient-to-r from-blue-900 to-blue-700 rounded-2xl p-10 text-white">
        <h1 className="text-3xl font-bold mb-3">化学業界 M&A アドバイザリ</h1>
        <p className="text-blue-100 text-lg mb-6">
          国内化学業界のM&A動向・企業価値算定・アドバイザリレポートをワンストップで提供します。
        </p>
        <div className="flex gap-4">
          <a
            href="/deals"
            className="bg-white text-blue-900 px-5 py-2 rounded-lg font-semibold text-sm hover:bg-blue-50 transition"
          >
            M&Aディール一覧
          </a>
          <a
            href="/valuation"
            className="border border-white text-white px-5 py-2 rounded-lg font-semibold text-sm hover:bg-white/10 transition"
          >
            バリュエーション分析
          </a>
        </div>
      </section>

      {/* Stats */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "登録ディール数", value: `${deals.length}件` },
          { label: "追跡企業数", value: "12社" },
          { label: "発行レポート数", value: `${advisoryReports.length}本` },
          { label: "対象セグメント", value: "6分野" },
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-xl p-5 text-center shadow-sm border border-gray-100">
            <p className="text-2xl font-bold text-blue-900">{stat.value}</p>
            <p className="text-sm text-gray-500 mt-1">{stat.label}</p>
          </div>
        ))}
      </section>

      {/* Recent Deals */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">最新M&Aディール</h2>
          <a href="/deals" className="text-sm text-blue-600 hover:underline">すべて見る →</a>
        </div>
        <div className="grid md:grid-cols-2 gap-4">
          {recentDeals.map((deal) => (
            <div key={deal.id} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <div className="flex items-start justify-between mb-2">
                <span className="text-xs text-gray-400">{deal.date}</span>
                <div className="flex gap-2">
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                    {deal.dealType}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${STATUS_COLORS[deal.status]}`}>
                    {deal.status}
                  </span>
                </div>
              </div>
              <p className="font-semibold text-sm">
                {deal.acquirer} → {deal.target}
                {deal.targetCode && (
                  <span className="text-gray-400 font-normal ml-1">({deal.targetCode})</span>
                )}
              </p>
              {deal.dealValue && (
                <p className="text-xs text-gray-500 mt-1">
                  取引総額: {(deal.dealValue / 10000).toFixed(0)}億円
                </p>
              )}
              <p className="text-xs text-gray-600 mt-2 line-clamp-2">{deal.rationale}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Latest Report */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">最新アドバイザリレポート</h2>
          <a href="/reports" className="text-sm text-blue-600 hover:underline">すべて見る →</a>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full font-medium">
              {latestReport.category}
            </span>
            <span className="text-xs text-gray-400">{latestReport.date}</span>
          </div>
          <h3 className="font-bold text-lg mb-2">{latestReport.title}</h3>
          <p className="text-sm text-gray-600 mb-4">{latestReport.summary}</p>
          <ul className="space-y-1">
            {latestReport.highlights.map((h, i) => (
              <li key={i} className="text-sm text-gray-700 flex gap-2">
                <span className="text-blue-500 mt-0.5">•</span>
                {h}
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
