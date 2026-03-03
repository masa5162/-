import { valuations, deals } from "@/data/deals";

function fmt(n: number | undefined, suffix = "") {
  if (n === undefined) return "N/A";
  return `${n.toLocaleString()}${suffix}`;
}

function fmtBil(n: number | undefined) {
  if (n === undefined) return "N/A";
  return `${(n / 10000).toFixed(1)}億円`;
}

function ValuationCard({ v }: { v: typeof valuations[0] }) {
  const isPrivate = !v.marketCap;
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className={`px-6 py-4 ${isPrivate ? "bg-gray-700" : "bg-blue-900"} text-white`}>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold text-lg">{v.name}</h3>
            <p className="text-xs opacity-80">{v.code} ／ {v.fiscalYear}</p>
          </div>
          {isPrivate && (
            <span className="text-xs bg-white/20 px-2 py-1 rounded-full">非公開会社</span>
          )}
        </div>
      </div>

      <div className="p-6">
        {/* Financial summary */}
        <h4 className="text-sm font-semibold text-gray-500 mb-3">財務指標</h4>
        <div className="grid grid-cols-2 gap-3 mb-5">
          {[
            { label: "売上高", value: fmtBil(v.revenue) },
            { label: "営業利益", value: fmtBil(v.operatingIncome) },
            { label: "当期純利益", value: fmtBil(v.netIncome) },
            { label: "純資産", value: fmtBil(v.netAssets) },
            { label: "総資産", value: fmtBil(v.totalAssets) },
            { label: "時価総額", value: v.marketCap ? fmtBil(v.marketCap) : "非公開" },
          ].map((item) => (
            <div key={item.label} className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-500">{item.label}</p>
              <p className="font-semibold text-sm">{item.value}</p>
            </div>
          ))}
        </div>

        {/* Multiples */}
        <h4 className="text-sm font-semibold text-gray-500 mb-3">バリュエーション指標</h4>
        <div className="grid grid-cols-2 gap-3 mb-5">
          {[
            { label: "PER", value: fmt(v.per, "倍") },
            { label: "PBR", value: fmt(v.pbr, "倍") },
            { label: "EV/EBITDA", value: fmt(v.evEbitda, "倍") },
            { label: "ROE", value: fmt(v.roe, "%") },
          ].map((item) => (
            <div
              key={item.label}
              className={`rounded-lg p-3 text-center ${
                item.value === "N/A" ? "bg-gray-50" : "bg-blue-50 border border-blue-100"
              }`}
            >
              <p className="text-xs text-gray-500">{item.label}</p>
              <p className={`font-bold text-base ${item.value === "N/A" ? "text-gray-400" : "text-blue-900"}`}>
                {item.value}
              </p>
            </div>
          ))}
        </div>

        {/* Per-share */}
        <div className="bg-amber-50 border border-amber-100 rounded-lg p-3">
          <p className="text-xs text-gray-500 mb-1">1株当たり純資産（BPS）</p>
          <p className="font-bold text-base text-amber-800">
            {fmt(Math.round((v.netAssets * 1_000_000) / v.sharesOutstanding), "円")}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function ValuationPage() {
  // Comparable multiples for Soda Aromatic
  const listed = valuations.filter((v) => v.marketCap);
  const avgPer = listed.reduce((s, v) => s + (v.per ?? 0), 0) / listed.length;
  const avgPbr = listed.reduce((s, v) => s + (v.pbr ?? 0), 0) / listed.length;
  const avgEvEbitda = listed.reduce((s, v) => s + (v.evEbitda ?? 0), 0) / listed.length;

  const soda = valuations.find((v) => v.id === "soda-aromatic")!;
  const sodaBps = Math.round((soda.netAssets * 1_000_000) / soda.sharesOutstanding);
  const sodaEbitdaMm = soda.operatingIncome + 800; // estimated depreciation

  const impliedByPbr = Math.round((soda.netAssets * avgPbr) / 10000);
  const impliedByPer = Math.round((soda.netIncome * avgPer) / 10000);
  const impliedByEvEbitda = Math.round((sodaEbitdaMm * avgEvEbitda) / 10000);
  const tobEquityBil = Math.round((1140 * soda.sharesOutstanding) / 1_000_000 / 10000);

  const sodaDeal = deals.find((d) => d.id === "soda-aromatic-2017")!;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold mb-1">バリュエーション分析</h1>
        <p className="text-gray-500 text-sm">香料業界の主要企業バリュエーション指標と類似会社比較分析</p>
      </div>

      {/* Company cards */}
      <section>
        <h2 className="text-lg font-semibold mb-4">企業別バリュエーション</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {valuations.map((v) => (
            <ValuationCard key={v.id} v={v} />
          ))}
        </div>
      </section>

      {/* Comparable analysis for Soda */}
      <section className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-lg font-semibold mb-1">曽田香料 類似会社比較バリュエーション</h2>
        <p className="text-xs text-gray-500 mb-5">
          高砂香料・長谷川香料の平均マルチプルを適用した試算（2024年3月期推定ベース）
        </p>

        {/* Avg multiples */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          {[
            { label: "平均 PER", value: avgPer.toFixed(1) + "倍" },
            { label: "平均 PBR", value: avgPbr.toFixed(2) + "倍" },
            { label: "平均 EV/EBITDA", value: avgEvEbitda.toFixed(1) + "倍" },
          ].map((item) => (
            <div key={item.label} className="bg-blue-50 border border-blue-100 rounded-lg p-3 text-center">
              <p className="text-xs text-gray-500">{item.label}</p>
              <p className="font-bold text-blue-900">{item.value}</p>
            </div>
          ))}
        </div>

        {/* Implied values table */}
        <table className="w-full text-sm mb-6">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-2 text-gray-500 font-medium">算定手法</th>
              <th className="text-right py-2 text-gray-500 font-medium">算定根拠</th>
              <th className="text-right py-2 text-gray-500 font-medium">推定株式価値</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            <tr>
              <td className="py-2 font-medium">PBR法</td>
              <td className="py-2 text-right text-gray-600">
                純資産 {(soda.netAssets / 100).toFixed(0)}億円 × PBR {avgPbr.toFixed(2)}倍
              </td>
              <td className="py-2 text-right font-bold text-blue-900">約 {impliedByPbr}億円</td>
            </tr>
            <tr>
              <td className="py-2 font-medium">PER法</td>
              <td className="py-2 text-right text-gray-600">
                純利益 {(soda.netIncome / 100).toFixed(1)}億円 × PER {avgPer.toFixed(1)}倍
              </td>
              <td className="py-2 text-right font-bold text-blue-900">約 {impliedByPer}億円</td>
            </tr>
            <tr>
              <td className="py-2 font-medium">EV/EBITDA法</td>
              <td className="py-2 text-right text-gray-600">
                EBITDA {(sodaEbitdaMm / 100).toFixed(0)}億円 × {avgEvEbitda.toFixed(1)}倍
              </td>
              <td className="py-2 text-right font-bold text-blue-900">約 {impliedByEvEbitda}億円</td>
            </tr>
          </tbody>
        </table>

        {/* TOB comparison */}
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
          <h3 className="font-semibold text-amber-900 mb-2">2017年TOB実績との比較</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
            <div>
              <p className="text-xs text-gray-500">TOB価格</p>
              <p className="font-bold">{sodaDeal.tobPrice?.toLocaleString()}円/株</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">TOB時PBR</p>
              <p className="font-bold text-red-600">{sodaDeal.tobPbr}倍（純資産割れ）</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">TOB時株式時価</p>
              <p className="font-bold">約 {tobEquityBil}億円</p>
            </div>
            <div>
              <p className="text-xs text-gray-500">TOB時1株BPS</p>
              <p className="font-bold">1,642円</p>
            </div>
          </div>
          <p className="text-xs text-amber-800 mt-3">
            ※ TOB価格1,140円はBPS 1,642円を下回る「純資産割れ」での買収。
            類似会社比較法では現在の時価ベースで200〜250億円レンジが試算されるが、
            2017年時点の類似会社マルチプルや非流動性ディスカウントを考慮すると価格は低下する可能性あり。
          </p>
        </div>
      </section>

      {/* Disclaimer */}
      <div className="text-xs text-gray-400 p-4 bg-gray-50 rounded-lg">
        <strong>注意:</strong>{" "}
        本分析は公開情報に基づく試算であり、投資助言ではありません。
        曽田香料の2018年3月期以降の財務データは非公開であり、推定値を含みます。
        正確な企業価値算定には詳細な財務データおよび事業計画が必要です。
      </div>
    </div>
  );
}
