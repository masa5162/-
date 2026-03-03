import { deals, Deal } from "@/data/deals";

const STATUS_COLORS: Record<string, string> = {
  完了: "bg-green-100 text-green-800",
  進行中: "bg-blue-100 text-blue-800",
  検討中: "bg-yellow-100 text-yellow-800",
  中断: "bg-gray-100 text-gray-600",
};

const DEAL_TYPE_COLORS: Record<string, string> = {
  TOB: "bg-red-100 text-red-700",
  株式取得: "bg-purple-100 text-purple-700",
  合併: "bg-indigo-100 text-indigo-700",
  事業譲渡: "bg-orange-100 text-orange-700",
  MBO: "bg-pink-100 text-pink-700",
};

function DealRow({ deal }: { deal: Deal }) {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition">
      <div className="flex flex-wrap items-start justify-between gap-2 mb-3">
        <div className="flex items-center gap-2">
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${DEAL_TYPE_COLORS[deal.dealType] ?? "bg-gray-100 text-gray-600"}`}>
            {deal.dealType}
          </span>
          <span className={`text-xs px-2 py-0.5 rounded-full ${STATUS_COLORS[deal.status]}`}>
            {deal.status}
          </span>
          <span className="text-xs bg-gray-50 text-gray-500 px-2 py-0.5 rounded-full border border-gray-200">
            {deal.segment}
          </span>
        </div>
        <span className="text-xs text-gray-400">{deal.date}</span>
      </div>

      <div className="mb-3">
        <p className="text-sm text-gray-500 mb-0.5">買収者 → 対象会社</p>
        <p className="font-semibold text-base">
          {deal.acquirer}
          {deal.acquirerCode && <span className="text-gray-400 font-normal text-sm ml-1">({deal.acquirerCode})</span>}
          {" → "}
          {deal.target}
          {deal.targetCode && <span className="text-gray-400 font-normal text-sm ml-1">({deal.targetCode})</span>}
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
        {deal.dealValue && (
          <div className="bg-gray-50 rounded-lg p-2 text-center">
            <p className="text-xs text-gray-500">取引総額</p>
            <p className="font-bold text-sm">{(deal.dealValue / 10000).toFixed(0)}億円</p>
          </div>
        )}
        {deal.tobPrice && (
          <div className="bg-gray-50 rounded-lg p-2 text-center">
            <p className="text-xs text-gray-500">TOB価格</p>
            <p className="font-bold text-sm">{deal.tobPrice.toLocaleString()}円</p>
          </div>
        )}
        {deal.tobPbr && (
          <div className="bg-gray-50 rounded-lg p-2 text-center">
            <p className="text-xs text-gray-500">TOB時PBR</p>
            <p className="font-bold text-sm">{deal.tobPbr}倍</p>
          </div>
        )}
        {deal.tobPer && (
          <div className="bg-gray-50 rounded-lg p-2 text-center">
            <p className="text-xs text-gray-500">TOB時PER</p>
            <p className="font-bold text-sm">{deal.tobPer}倍</p>
          </div>
        )}
      </div>

      <p className="text-sm text-gray-600">{deal.rationale}</p>
    </div>
  );
}

export default function DealsPage() {
  const completed = deals.filter((d) => d.status === "完了");
  const inProgress = deals.filter((d) => d.status !== "完了");

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold mb-1">M&Aディール一覧</h1>
        <p className="text-gray-500 text-sm">化学業界の主要M&A・TOB・事業再編案件データベース</p>
      </div>

      {/* Summary stats */}
      <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
        {(["TOB", "株式取得", "合併", "事業譲渡", "MBO"] as const).map((type) => {
          const count = deals.filter((d) => d.dealType === type).length;
          return (
            <div key={type} className={`rounded-lg p-3 text-center ${DEAL_TYPE_COLORS[type] ?? "bg-gray-100"}`}>
              <p className="text-lg font-bold">{count}</p>
              <p className="text-xs">{type}</p>
            </div>
          );
        })}
      </div>

      {inProgress.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold mb-3 text-blue-700">進行中・検討中</h2>
          <div className="space-y-4">
            {inProgress.map((deal) => (
              <DealRow key={deal.id} deal={deal} />
            ))}
          </div>
        </section>
      )}

      <section>
        <h2 className="text-lg font-semibold mb-3">完了案件</h2>
        <div className="space-y-4">
          {completed.map((deal) => (
            <DealRow key={deal.id} deal={deal} />
          ))}
        </div>
      </section>
    </div>
  );
}
