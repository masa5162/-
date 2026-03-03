import { advisoryReports } from "@/data/deals";

const CATEGORY_COLORS: Record<string, string> = {
  マーケットレポート: "bg-blue-100 text-blue-700",
  セクターレポート: "bg-green-100 text-green-700",
  ケーススタディ: "bg-purple-100 text-purple-700",
};

export default function ReportsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold mb-1">アドバイザリレポート</h1>
        <p className="text-gray-500 text-sm">化学業界M&Aの最新動向・バリュエーション・ケーススタディ</p>
      </div>

      <div className="space-y-6">
        {advisoryReports.map((report) => (
          <div key={report.id} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center gap-2 mb-3">
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${CATEGORY_COLORS[report.category] ?? "bg-gray-100 text-gray-600"}`}>
                {report.category}
              </span>
              <span className="text-xs text-gray-400">{report.date}</span>
            </div>

            <h2 className="text-xl font-bold mb-2">{report.title}</h2>
            <p className="text-sm text-gray-600 mb-4">{report.summary}</p>

            <div>
              <h3 className="text-sm font-semibold text-gray-500 mb-2">主要ポイント</h3>
              <ul className="space-y-2">
                {report.highlights.map((highlight, i) => (
                  <li key={i} className="flex gap-2 text-sm">
                    <span className="text-blue-500 font-bold mt-0.5">→</span>
                    <span className="text-gray-700">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100 text-xs text-gray-400">
              本レポートは公開情報に基づく分析であり、投資助言ではありません。
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
