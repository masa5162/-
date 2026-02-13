#!/usr/bin/env python3
"""
曽田香料株式会社（Soda Aromatic Co., Ltd.）企業価値算定レポート
=============================================================

証券コード: 4965（2017年12月25日上場廃止）
親会社: 東レ株式会社（議決権66%）、三井物産株式会社（議決権34%）

算定手法:
  1. 類似企業比較法（マルチプル法）
  2. 純資産法（修正簿価純資産法）
  3. DCF法（簡易）
"""

import json
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 1. データ定義
# ============================================================

@dataclass
class FinancialData:
    """財務データ"""
    name: str
    fiscal_year: str
    revenue: float           # 売上高（百万円）
    operating_income: float  # 営業利益（百万円）
    ordinary_income: float   # 経常利益（百万円）
    net_income: float        # 当期純利益（百万円）
    total_assets: float      # 総資産（百万円）
    net_assets: float        # 純資産（百万円）
    depreciation: Optional[float] = None  # 減価償却費（百万円）
    shares_outstanding: Optional[int] = None  # 発行済株式数


@dataclass
class ValuationMultiples:
    """バリュエーション・マルチプル"""
    name: str
    per: float         # 株価収益率
    pbr: float         # 株価純資産倍率
    ev_ebitda: float   # EV/EBITDA
    ev_sales: float    # EV/売上高
    roe: float         # ROE (%)


# ============================================================
# 2. 入力データ
# ============================================================

# --- 曽田香料の財務データ ---

# 最終公開決算（2017年3月期・連結）
soda_2017 = FinancialData(
    name="曽田香料",
    fiscal_year="2017年3月期（連結）",
    revenue=15250,
    operating_income=525,
    ordinary_income=424,
    net_income=243,
    total_assets=22146,
    net_assets=17397,
    depreciation=700,  # 推定値（有形固定資産規模から推計）
    shares_outstanding=10_586_000,
)

# 2024年3月期（採用ページより判明分、利益は推定）
soda_2024_estimated = FinancialData(
    name="曽田香料",
    fiscal_year="2024年3月期（連結・推定含む）",
    revenue=17562,
    operating_income=700,   # 推定（営業利益率4.0%想定）
    ordinary_income=650,    # 推定
    net_income=420,         # 推定
    total_assets=24000,     # 推定
    net_assets=19500,       # 推定
    depreciation=800,       # 推定
    shares_outstanding=10_586_000,
)

# --- 類似企業データ ---

takasago = ValuationMultiples(
    name="高砂香料工業（4914）",
    per=13.5,
    pbr=1.04,
    ev_ebitda=8.75,
    ev_sales=0.65,  # 時価総額1494億÷売上2292億 ≒ 0.65
    roe=9.2,
)

hasegawa = ValuationMultiples(
    name="長谷川香料（4958）",
    per=16.4,
    pbr=1.04,
    ev_ebitda=10.0,   # 推定
    ev_sales=1.48,    # 時価総額1092億÷売上735億 ≒ 1.49
    roe=5.6,
)

# TOB実績
TOB_PRICE_PER_SHARE = 1140  # 円
TOB_DATE = "2017年8月〜9月"
BPS_AT_TOB = 1642.78  # 1株当たり純資産


# ============================================================
# 3. 算定ロジック
# ============================================================

def comparable_valuation(
    target: FinancialData,
    comps: list[ValuationMultiples],
) -> dict:
    """類似企業比較法（マルチプル法）による企業価値算定"""

    avg_per = sum(c.per for c in comps) / len(comps)
    avg_pbr = sum(c.pbr for c in comps) / len(comps)
    avg_ev_ebitda = sum(c.ev_ebitda for c in comps) / len(comps)
    avg_ev_sales = sum(c.ev_sales for c in comps) / len(comps)

    ebitda = target.operating_income + (target.depreciation or 0)

    # 各マルチプルによる株式価値
    equity_by_per = target.net_income * avg_per
    equity_by_pbr = target.net_assets * avg_pbr
    ev_by_ebitda = ebitda * avg_ev_ebitda
    ev_by_sales = target.revenue * avg_ev_sales

    return {
        "method": "類似企業比較法（マルチプル法）",
        "comparable_companies": [c.name for c in comps],
        "average_multiples": {
            "PER": round(avg_per, 1),
            "PBR": round(avg_pbr, 2),
            "EV/EBITDA": round(avg_ev_ebitda, 2),
            "EV/Sales": round(avg_ev_sales, 2),
        },
        "target_financials": {
            "売上高": f"{target.revenue:,.0f} 百万円",
            "営業利益": f"{target.operating_income:,.0f} 百万円",
            "当期純利益": f"{target.net_income:,.0f} 百万円",
            "純資産": f"{target.net_assets:,.0f} 百万円",
            "EBITDA": f"{ebitda:,.0f} 百万円",
        },
        "valuations": {
            "PER法": {
                "equity_value_mm": round(equity_by_per),
                "description": f"当期純利益 {target.net_income:,.0f} × PER {avg_per:.1f} = {equity_by_per:,.0f} 百万円",
            },
            "PBR法": {
                "equity_value_mm": round(equity_by_pbr),
                "description": f"純資産 {target.net_assets:,.0f} × PBR {avg_pbr:.2f} = {equity_by_pbr:,.0f} 百万円",
            },
            "EV/EBITDA法": {
                "enterprise_value_mm": round(ev_by_ebitda),
                "description": f"EBITDA {ebitda:,.0f} × EV/EBITDA {avg_ev_ebitda:.2f} = {ev_by_ebitda:,.0f} 百万円",
            },
            "EV/Sales法": {
                "enterprise_value_mm": round(ev_by_sales),
                "description": f"売上高 {target.revenue:,.0f} × EV/Sales {avg_ev_sales:.2f} = {ev_by_sales:,.0f} 百万円",
            },
        },
    }


def net_asset_valuation(target: FinancialData) -> dict:
    """純資産法（修正簿価純資産法）"""
    # 含み益の調整は不明のため簿価ベース
    equity_value = target.net_assets

    per_share = None
    if target.shares_outstanding:
        per_share = round(equity_value * 1_000_000 / target.shares_outstanding)

    return {
        "method": "純資産法（簿価純資産法）",
        "equity_value_mm": round(equity_value),
        "description": f"純資産 = {equity_value:,.0f} 百万円（簿価ベース）",
        "per_share": f"{per_share:,} 円/株" if per_share else "N/A",
        "note": "含み損益・のれん等の調整は未反映。実際の修正純資産法では不動産・有価証券等の時価評価が必要。",
    }


def dcf_valuation(
    target: FinancialData,
    revenue_growth: float = 0.02,
    op_margin: float = 0.04,
    tax_rate: float = 0.30,
    capex_ratio: float = 0.03,
    depreciation_ratio: float = 0.04,
    wacc: float = 0.07,
    terminal_growth: float = 0.01,
    projection_years: int = 5,
) -> dict:
    """簡易DCF法による企業価値算定"""

    projections = []
    revenue = target.revenue

    for year in range(1, projection_years + 1):
        revenue = revenue * (1 + revenue_growth)
        op_income = revenue * op_margin
        nopat = op_income * (1 - tax_rate)
        depreciation = revenue * depreciation_ratio
        capex = revenue * capex_ratio
        fcf = nopat + depreciation - capex

        projections.append({
            "year": year,
            "revenue": round(revenue),
            "operating_income": round(op_income),
            "nopat": round(nopat),
            "depreciation": round(depreciation),
            "capex": round(capex),
            "fcf": round(fcf),
        })

    # 現在価値の計算
    pv_fcfs = []
    for p in projections:
        pv = p["fcf"] / ((1 + wacc) ** p["year"])
        pv_fcfs.append(round(pv))

    sum_pv_fcf = sum(pv_fcfs)

    # ターミナルバリュー
    terminal_fcf = projections[-1]["fcf"] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    pv_terminal = terminal_value / ((1 + wacc) ** projection_years)

    enterprise_value = sum_pv_fcf + pv_terminal

    per_share = None
    if target.shares_outstanding:
        per_share = round(enterprise_value * 1_000_000 / target.shares_outstanding)

    return {
        "method": "DCF法（簡易）",
        "assumptions": {
            "売上成長率": f"{revenue_growth:.1%}",
            "営業利益率": f"{op_margin:.1%}",
            "実効税率": f"{tax_rate:.1%}",
            "設備投資/売上高": f"{capex_ratio:.1%}",
            "減価償却/売上高": f"{depreciation_ratio:.1%}",
            "WACC": f"{wacc:.1%}",
            "永久成長率": f"{terminal_growth:.1%}",
            "予測期間": f"{projection_years}年",
        },
        "projections": projections,
        "pv_of_fcfs_mm": sum_pv_fcf,
        "terminal_value_mm": round(terminal_value),
        "pv_of_terminal_mm": round(pv_terminal),
        "enterprise_value_mm": round(enterprise_value),
        "per_share": f"{per_share:,} 円/株" if per_share else "N/A",
    }


# ============================================================
# 4. 実行・レポート出力
# ============================================================

def print_section(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_subsection(title: str):
    print(f"\n--- {title} ---\n")


def main():
    print("=" * 70)
    print("  曽田香料株式会社 企業価値算定レポート")
    print("  Soda Aromatic Co., Ltd. - Valuation Report")
    print("=" * 70)

    # -------------------------------------------------------
    # 会社概要
    # -------------------------------------------------------
    print_section("1. 会社概要")
    print("  会社名:     曽田香料株式会社")
    print("  証券コード: 4965（2017年12月25日上場廃止）")
    print("  設立:       1915年（大正4年）")
    print("  本社:       大阪府大阪市")
    print("  事業内容:   フレグランス、フレーバー、合成香料、")
    print("              ファインケミカル等の製造販売")
    print("  親会社:     東レ（議決権66%）、三井物産（議決権34%）")
    print(f"  2024/3期 連結売上高: {soda_2024_estimated.revenue:,} 百万円（約175億円）")
    print(f"  2017/3期 連結売上高: {soda_2017.revenue:,} 百万円（最終公開決算）")

    # -------------------------------------------------------
    # TOB実績の確認
    # -------------------------------------------------------
    print_section("2. TOB実績（2017年）")
    tob_equity = TOB_PRICE_PER_SHARE * soda_2017.shares_outstanding / 1_000_000
    print(f"  TOB価格:           {TOB_PRICE_PER_SHARE:,} 円/株")
    print(f"  TOB時BPS:          {BPS_AT_TOB:,.2f} 円/株")
    print(f"  TOB時PBR:          {TOB_PRICE_PER_SHARE / BPS_AT_TOB:.2f} 倍")
    print(f"  TOB時の株式時価:    {tob_equity:,.0f} 百万円（約{tob_equity/100:.0f}億円）")
    print(f"  TOB時PER:          {tob_equity / soda_2017.net_income:.1f} 倍")
    print(f"  買付者:            東レ・三井物産")
    print(f"  上場廃止日:        2017年12月25日")

    # -------------------------------------------------------
    # 手法1: 類似企業比較法（2017年3月期ベース）
    # -------------------------------------------------------
    print_section("3. 類似企業比較法（マルチプル法）")

    print_subsection("A. 2017年3月期ベース")
    comp_2017 = comparable_valuation(soda_2017, [takasago, hasegawa])
    print(f"  類似企業: {', '.join(comp_2017['comparable_companies'])}")
    print(f"  平均マルチプル:")
    for k, v in comp_2017["average_multiples"].items():
        print(f"    {k}: {v}")
    print(f"\n  ターゲット財務指標:")
    for k, v in comp_2017["target_financials"].items():
        print(f"    {k}: {v}")
    print(f"\n  算定結果:")
    for method, detail in comp_2017["valuations"].items():
        print(f"    【{method}】")
        print(f"      {detail['description']}")

    print_subsection("B. 2024年3月期ベース（推定値含む）")
    comp_2024 = comparable_valuation(soda_2024_estimated, [takasago, hasegawa])
    print(f"  ※ 売上高以外は推定値を含む\n")
    print(f"  ターゲット財務指標:")
    for k, v in comp_2024["target_financials"].items():
        print(f"    {k}: {v}")
    print(f"\n  算定結果:")
    for method, detail in comp_2024["valuations"].items():
        print(f"    【{method}】")
        print(f"      {detail['description']}")

    # -------------------------------------------------------
    # 手法2: 純資産法
    # -------------------------------------------------------
    print_section("4. 純資産法")

    print_subsection("2017年3月期ベース")
    nav_2017 = net_asset_valuation(soda_2017)
    print(f"  {nav_2017['description']}")
    print(f"  1株当たり: {nav_2017['per_share']}")
    print(f"  ※ {nav_2017['note']}")

    print_subsection("2024年3月期ベース（推定）")
    nav_2024 = net_asset_valuation(soda_2024_estimated)
    print(f"  {nav_2024['description']}")
    print(f"  1株当たり: {nav_2024['per_share']}")

    # -------------------------------------------------------
    # 手法3: DCF法
    # -------------------------------------------------------
    print_section("5. DCF法（簡易）")

    # ベースケース
    print_subsection("ベースケース")
    dcf_base = dcf_valuation(soda_2024_estimated)
    print("  前提条件:")
    for k, v in dcf_base["assumptions"].items():
        print(f"    {k}: {v}")
    print(f"\n  FCF予測:")
    print(f"    {'Year':>4}  {'売上高':>10}  {'営業利益':>10}  {'FCF':>10}")
    for p in dcf_base["projections"]:
        print(f"    {p['year']:>4}  {p['revenue']:>10,}  {p['operating_income']:>10,}  {p['fcf']:>10,}")
    print(f"\n  FCF現在価値合計:   {dcf_base['pv_of_fcfs_mm']:>10,} 百万円")
    print(f"  ターミナルバリュー: {dcf_base['terminal_value_mm']:>10,} 百万円")
    print(f"  TV現在価値:        {dcf_base['pv_of_terminal_mm']:>10,} 百万円")
    print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  企業価値（EV）:    {dcf_base['enterprise_value_mm']:>10,} 百万円（約{dcf_base['enterprise_value_mm']/100:.0f}億円）")
    print(f"  1株当たり:         {dcf_base['per_share']}")

    # 楽観ケース
    print_subsection("楽観ケース（成長率3%、利益率5%）")
    dcf_bull = dcf_valuation(
        soda_2024_estimated,
        revenue_growth=0.03,
        op_margin=0.05,
        wacc=0.06,
    )
    print(f"  企業価値（EV）:    {dcf_bull['enterprise_value_mm']:>10,} 百万円（約{dcf_bull['enterprise_value_mm']/100:.0f}億円）")
    print(f"  1株当たり:         {dcf_bull['per_share']}")

    # 悲観ケース
    print_subsection("悲観ケース（成長率1%、利益率3%）")
    dcf_bear = dcf_valuation(
        soda_2024_estimated,
        revenue_growth=0.01,
        op_margin=0.03,
        wacc=0.08,
    )
    print(f"  企業価値（EV）:    {dcf_bear['enterprise_value_mm']:>10,} 百万円（約{dcf_bear['enterprise_value_mm']/100:.0f}億円）")
    print(f"  1株当たり:         {dcf_bear['per_share']}")

    # -------------------------------------------------------
    # 総合まとめ
    # -------------------------------------------------------
    print_section("6. 企業価値レンジ（総合）")

    # 各手法の結果をまとめる
    results = {
        "PER法（2024推定）": comp_2024["valuations"]["PER法"]["equity_value_mm"],
        "PBR法（2024推定）": comp_2024["valuations"]["PBR法"]["equity_value_mm"],
        "EV/EBITDA法（2024推定）": comp_2024["valuations"]["EV/EBITDA法"]["enterprise_value_mm"],
        "EV/Sales法（2024推定）": comp_2024["valuations"]["EV/Sales法"]["enterprise_value_mm"],
        "純資産法（2024推定）": nav_2024["equity_value_mm"],
        "DCF法（ベース）": dcf_base["enterprise_value_mm"],
        "DCF法（楽観）": dcf_bull["enterprise_value_mm"],
        "DCF法（悲観）": dcf_bear["enterprise_value_mm"],
    }

    print(f"  {'算定手法':<25} {'企業/株式価値（百万円）':>20}  {'（億円）':>8}")
    print(f"  {'-'*60}")
    for method, value in results.items():
        print(f"  {method:<25} {value:>18,}    {value/100:>6.0f}")

    values = list(results.values())
    min_val = min(values)
    max_val = max(values)
    median_val = sorted(values)[len(values) // 2]

    print(f"\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  レンジ下限:   {min_val:>10,} 百万円（約{min_val/100:.0f}億円）")
    print(f"  中央値:       {median_val:>10,} 百万円（約{median_val/100:.0f}億円）")
    print(f"  レンジ上限:   {max_val:>10,} 百万円（約{max_val/100:.0f}億円）")
    print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    print(f"\n  参考: 2017年TOB時の株式時価: {tob_equity:,.0f} 百万円（約{tob_equity/100:.0f}億円）")

    # -------------------------------------------------------
    # 注意事項
    # -------------------------------------------------------
    print_section("7. 注意事項・免責")
    print("""  1. 本レポートは公開情報に基づく試算であり、投資助言ではありません。
  2. 曽田香料は2017年12月に上場廃止しており、2018年3月期以降の
     詳細な財務データは非公開です。
  3. 2024年3月期のデータは売上高のみ確認可能であり、利益・資産
     等は業界平均等から推定した値を使用しています。
  4. 類似企業のマルチプルは2025年〜2026年時点の値を使用して
     おり、2017年TOB時とは市場環境が異なります。
  5. DCF法の前提条件（成長率・WACC等）は仮定値であり、実際の
     企業価値は大きく異なる可能性があります。
  6. 正確な企業価値算定には、非公開の詳細財務データ、事業計画、
     資産の時価評価等が必要です。

  データソース:
  - 曽田香料 最終有価証券報告書（2017年3月期）
  - マイナビ2026 曽田香料会社概要（2024年3月期売上高）
  - 高砂香料工業・長谷川香料 各種IR資料（2025-2026年）
  """)


if __name__ == "__main__":
    main()
