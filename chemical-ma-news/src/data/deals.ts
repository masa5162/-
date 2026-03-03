export type DealStatus = "完了" | "進行中" | "検討中" | "中断";
export type DealType = "TOB" | "株式取得" | "合併" | "事業譲渡" | "MBO";

export interface Deal {
  id: string;
  date: string;
  acquirer: string;
  acquirerCode?: string;
  target: string;
  targetCode?: string;
  dealType: DealType;
  status: DealStatus;
  dealValue?: number; // 百万円
  tobPrice?: number; // 円/株
  tobPbr?: number;
  tobPer?: number;
  rationale: string;
  segment: string;
}

export interface CompanyValuation {
  id: string;
  name: string;
  code: string;
  fiscalYear: string;
  revenue: number; // 百万円
  operatingIncome: number;
  netIncome: number;
  netAssets: number;
  totalAssets: number;
  sharesOutstanding: number;
  marketCap?: number; // 百万円
  per?: number;
  pbr?: number;
  evEbitda?: number;
  roe?: number;
}

export const deals: Deal[] = [
  {
    id: "soda-aromatic-2017",
    date: "2017-08",
    acquirer: "東レ・三井物産",
    target: "曽田香料",
    targetCode: "4965",
    dealType: "TOB",
    status: "完了",
    dealValue: 12068,
    tobPrice: 1140,
    tobPbr: 0.69,
    tobPer: 49.7,
    rationale:
      "東レ（議決権66%）・三井物産（議決権34%）による完全子会社化。フレグランス・フレーバー事業の強化と上場コスト削減を目的とする。",
    segment: "香料",
  },
  {
    id: "t-haseko-2024",
    date: "2024-03",
    acquirer: "大阪ソーダ",
    acquirerCode: "4046",
    target: "東ソー子会社（化学品事業）",
    dealType: "事業譲渡",
    status: "完了",
    dealValue: 3500,
    rationale:
      "塩素系溶剤事業の統合によるコスト競争力強化。環境規制対応を見据えた製品ポートフォリオ最適化。",
    segment: "基礎化学品",
  },
  {
    id: "ube-mitsubishi-2022",
    date: "2022-04",
    acquirer: "三菱ケミカルグループ",
    acquirerCode: "4188",
    target: "宇部興産（化学部門）",
    dealType: "合併",
    status: "完了",
    dealValue: 450000,
    rationale:
      "ナイロン・アンモニア・セメント等の統合によるスケールメリット追求。カーボンニュートラル対応の加速。",
    segment: "総合化学",
  },
  {
    id: "kuraray-eval-2024",
    date: "2024-10",
    acquirer: "非公表PE",
    target: "クラレ（特定事業部門）",
    dealType: "事業譲渡",
    status: "検討中",
    rationale:
      "ポバール・イソプレン化学事業の選択と集中。医療・水処理膜事業への資源集中。",
    segment: "機能材料",
  },
  {
    id: "nippon-paint-2021",
    date: "2021-08",
    acquirer: "Wuthelam Holdings",
    target: "日本ペイントHD",
    targetCode: "4612",
    dealType: "株式取得",
    status: "完了",
    dealValue: 1200000,
    tobPrice: 1050,
    tobPbr: 5.2,
    rationale:
      "アジア塗料市場での支配的地位確立。日本・中国・東南アジアの統合販売網構築。",
    segment: "塗料",
  },
  {
    id: "sumitomo-dsm-2023",
    date: "2023-05",
    acquirer: "住友化学",
    acquirerCode: "4005",
    target: "DSM-Firmenich（農業部門）",
    dealType: "株式取得",
    status: "完了",
    dealValue: 280000,
    rationale:
      "農薬・農業ソリューション事業の欧州・北米展開強化。生物農薬ポートフォリオの拡充。",
    segment: "農業化学",
  },
];

export const valuations: CompanyValuation[] = [
  {
    id: "takasago",
    name: "高砂香料工業",
    code: "4914",
    fiscalYear: "2025年3月期",
    revenue: 229200,
    operatingIncome: 13200,
    netIncome: 10800,
    netAssets: 143800,
    totalAssets: 220000,
    sharesOutstanding: 54000000,
    marketCap: 149400,
    per: 13.5,
    pbr: 1.04,
    evEbitda: 8.75,
    roe: 9.2,
  },
  {
    id: "hasegawa",
    name: "長谷川香料",
    code: "4958",
    fiscalYear: "2025年3月期",
    revenue: 73500,
    operatingIncome: 5200,
    netIncome: 4100,
    netAssets: 104900,
    totalAssets: 128000,
    sharesOutstanding: 24000000,
    marketCap: 109200,
    per: 16.4,
    pbr: 1.04,
    evEbitda: 10.0,
    roe: 5.6,
  },
  {
    id: "soda-aromatic",
    name: "曽田香料（非公開）",
    code: "4965",
    fiscalYear: "2024年3月期（推定）",
    revenue: 17562,
    operatingIncome: 700,
    netIncome: 420,
    netAssets: 19500,
    totalAssets: 24000,
    sharesOutstanding: 10586000,
    per: undefined,
    pbr: undefined,
    evEbitda: undefined,
    roe: undefined,
  },
];

export const advisoryReports = [
  {
    id: "rpt-001",
    date: "2026-03-01",
    title: "化学業界M&A動向レポート 2026年Q1",
    category: "マーケットレポート",
    summary:
      "2026年第1四半期の化学業界M&A動向を分析。カーボンニュートラル対応を軸とした事業再編が加速しており、特に基礎化学品・機能材料分野での大型案件が増加。",
    highlights: [
      "国内化学大手3社が事業再編を発表（総額約5,000億円）",
      "PE/ファンドによるカーブアウト案件が前年比40%増",
      "香料・フレーバー分野での海外展開型M&Aが活発化",
    ],
  },
  {
    id: "rpt-002",
    date: "2026-02-15",
    title: "香料業界バリュエーション分析",
    category: "セクターレポート",
    summary:
      "国内香料業界2社（高砂香料・長谷川香料）の最新バリュエーション指標を分析。PBR1倍台前半での安定推移が続く中、グローバル競合との差異を検討。",
    highlights: [
      "国内香料2社の平均PBR: 1.04倍（PER: 約15倍）",
      "IFF、Givaudan等グローバル大手との比較でバリュエーション割安",
      "非公開化後の曽田香料、2024年3月期売上高175億円推定",
    ],
  },
  {
    id: "rpt-003",
    date: "2026-01-20",
    title: "TOB・MBO事例研究：香料セクター",
    category: "ケーススタディ",
    summary:
      "曽田香料（4965）の2017年TOB事例を詳細分析。TOB価格1,140円はPBR0.69倍と純資産割れでの買収となったが、少数株主保護の観点から今後の類似案件への示唆を検討。",
    highlights: [
      "TOB価格1,140円に対し公正価値試算は1,500〜2,000円レンジ",
      "親会社主導TOBにおける少数株主保護の課題",
      "スクイーズアウト後の企業価値向上施策の検討",
    ],
  },
];
