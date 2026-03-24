"""
============================================================
スターフライヤー（9206）A種・B種優先株式
金銭対価取得請求額 & 普通株式転換数の計算
============================================================

前提:
  - 払込期日: 2021年3月9日
  - 21/3期（3/9〜3/31の日割分）の配当は実際にキャッシュで支払済
  - 22/3期〜26/3期の配当は全額未払・累積

計算基準日: 2026年3月31日

情報源:
  - 有価証券届出書（2020年12月25日提出、EDINET: S100KGBQ）
  - 適時開示資料各種
"""

from datetime import date, timedelta
from dataclasses import dataclass

# ============================================================
# パラメータ設定
# ============================================================

# --- A種: 確認済みパラメータ ---
A_SHARES_ISSUED = 5_500          # A種 発行株数
A_PAR_VALUE = 1_000_000          # A種 払込金額相当額（円/株）
A_DIVIDEND_RATE = 0.05           # A種 優先配当率 年率5.0%
A_COMPOUND_RATE = 0.05           # A種 累積未払配当金の複利利率 年利5.0%
A_CONVERSION_PRICE = 1_651.9     # A種 当初取得価額（円）固定
A_CASH_REDEMPTION_AFTER_YEARS = 5  # 金銭対価取得: 払込期日の5年後以降

# --- B種: 配当率=年率1.0%（リサーチ結果）、転換価額=VWAPベース変動型 ---
B_SHARES_ISSUED = 2_500          # B種 発行株数
B_PAR_VALUE = 1_000_000          # B種 払込金額相当額（円/株）
B_DIVIDEND_RATE = 0.01           # B種 優先配当率 年率1.0%
B_COMPOUND_RATE = 0.01           # B種 累積未払配当金の複利利率 年利1.0%（★要確認）
B_CASH_REDEMPTION_AFTER_YEARS = 6  # 金銭対価取得: 払込期日の6年後以降（会社側権利）

# B種の転換価額は「30営業日VWAP平均」ベースの変動型
# 正確な取得価額は取得請求時点のVWAPに依存するため、参考値で計算
B_VWAP_ASSUMED = 2_100           # 参考: 2026年3月時点の普通株式株価（概算）

PAYMENT_DATE = date(2021, 3, 9)     # 払込期日
CALC_DATE = date(2026, 3, 31)       # 計算基準日（26/3月末）


# ============================================================
# 1. 各期の優先配当金の計算（日割計算）
# ============================================================

@dataclass
class FiscalYear:
    """事業年度"""
    label: str
    start: date
    end: date
    paid: bool


fiscal_years = [
    FiscalYear("21/3期", PAYMENT_DATE,   date(2021, 3, 31), paid=True),
    FiscalYear("22/3期", date(2021, 4, 1), date(2022, 3, 31), paid=False),
    FiscalYear("23/3期", date(2022, 4, 1), date(2023, 3, 31), paid=False),
    FiscalYear("24/3期", date(2023, 4, 1), date(2024, 3, 31), paid=False),
    FiscalYear("25/3期", date(2024, 4, 1), date(2025, 3, 31), paid=False),
    FiscalYear("26/3期", date(2025, 4, 1), date(2026, 3, 31), paid=False),
]


def calc_dividend(par_value: int, rate: float, fy: FiscalYear) -> float:
    """1株あたりの優先配当金額を日割計算"""
    actual_days = (fy.end - fy.start).days + 1
    return par_value * rate * actual_days / 365


def calc_accumulated_unpaid(par_value: int, dividend_rate: float,
                            compound_rate: float,
                            fiscal_years: list, calc_date: date) -> list:
    """累積未払配当金相当額を複利計算で算出"""
    results = []

    for fy in fiscal_years:
        dividend = calc_dividend(par_value, dividend_rate, fy)

        if fy.paid:
            results.append({
                "period": fy.label, "days": (fy.end - fy.start).days + 1,
                "base_dividend": dividend, "status": "支払済",
                "compound_years": 0, "accumulated_value": 0.0,
            })
            continue

        if fy.end == calc_date:
            results.append({
                "period": fy.label, "days": (fy.end - fy.start).days + 1,
                "base_dividend": dividend, "status": "当期（日割未払優先配当金）",
                "compound_years": 0, "accumulated_value": dividend,
            })
            continue

        # 複利: 翌事業年度初日(4/1)から計算基準日(3/31)まで
        compound_start = fy.end + timedelta(days=1)
        years_elapsed = calc_date.year - compound_start.year
        accumulated = dividend * (1 + compound_rate) ** years_elapsed

        results.append({
            "period": fy.label, "days": (fy.end - fy.start).days + 1,
            "base_dividend": dividend,
            "status": f"未払（{years_elapsed}年複利@{compound_rate*100:.0f}%）",
            "compound_years": years_elapsed, "accumulated_value": accumulated,
        })

    return results


# ============================================================
# 表示関数
# ============================================================

def print_separator(char="=", width=80):
    print(char * width)


def analyze_stock(name: str, shares: int, par_value: int,
                  dividend_rate: float, compound_rate: float,
                  conversion_price: float, conversion_is_vwap: bool,
                  cash_after_years: int, notes: list = None):
    """優先株式の金銭対価・転換株数を計算"""

    print_separator()
    print(f"【{name}】")
    if notes:
        for n in notes:
            print(f"  {n}")
    print_separator()

    print(f"\n  ■ 基本条件")
    print(f"    発行株数:         {shares:,}株")
    print(f"    払込金額相当額:   ¥{par_value:,}/株")
    print(f"    優先配当率:       年率{dividend_rate*100:.1f}%")
    print(f"    累積複利利率:     年利{compound_rate*100:.1f}%")
    if conversion_is_vwap:
        print(f"    取得価額:         VWAPベース変動型（30営業日平均）")
        print(f"                      参考計算用: ¥{conversion_price:,.1f}（仮定値）")
    else:
        print(f"    当初取得価額:     ¥{conversion_price:,.1f}（固定）")
    print(f"    金銭対価取得:     払込期日の{cash_after_years}年後以降")
    cash_avail = date(PAYMENT_DATE.year + cash_after_years,
                      PAYMENT_DATE.month, PAYMENT_DATE.day)
    print(f"                      → {cash_avail} 以降", end="")
    if CALC_DATE >= cash_avail:
        print(" → 2026/3/31時点: 行使可能 ✓")
    else:
        print(" → 2026/3/31時点: 未到来 ✗")

    # --- 配当計算 ---
    print(f"\n  ■ 各期の優先配当金（1株あたり、日割計算: 実日数/365）")
    print(f"    {'期':8s} {'日数':>5s} {'基本配当額':>14s}  {'状態':24s} {'累積後金額':>14s}")
    print(f"    {'-'*8} {'-'*5} {'-'*14}  {'-'*24} {'-'*14}")

    results = calc_accumulated_unpaid(par_value, dividend_rate, compound_rate,
                                      fiscal_years, CALC_DATE)

    total_accumulated = 0.0
    current_year_div = 0.0

    for r in results:
        print(f"    {r['period']:8s} {r['days']:>3d}日"
              f"  ¥{r['base_dividend']:>12,.2f}"
              f"  {r['status']:24s}"
              f"  ¥{r['accumulated_value']:>12,.2f}")
        if r["status"] == "支払済":
            continue
        elif "当期" in r["status"]:
            current_year_div = r["accumulated_value"]
        else:
            total_accumulated += r["accumulated_value"]

    total_div_claim = total_accumulated + current_year_div
    print()
    print(f"    累積未払配当金相当額（22/3〜25/3、複利後）: ¥{total_accumulated:>14,.2f}")
    print(f"    日割未払優先配当金額（26/3期、当期分）:     ¥{current_year_div:>14,.2f}")
    print(f"    配当関連請求額 合計:                        ¥{total_div_claim:>14,.2f}")

    # ============================================================
    # A) 金銭対価
    # ============================================================
    print(f"\n  ■ 金銭対価取得請求額（2026/3/31時点）")
    print(f"    計算式: 株数 × (払込金額相当額 + 累積未払配当金相当額 + 日割未払優先配当金額)")
    print()

    per_share_cash = par_value + total_div_claim
    print(f"    【1株あたり】")
    print(f"      払込金額相当額:         ¥{par_value:>14,}")
    print(f"      累積未払配当金相当額:   ¥{total_accumulated:>14,.2f}")
    print(f"      日割未払優先配当金額:   ¥{current_year_div:>14,.2f}")
    print(f"      ─────────────────────────────────────")
    print(f"      合計:                   ¥{per_share_cash:>14,.2f}")
    print()

    total_cash = shares * per_share_cash
    print(f"    【全{shares:,}株の合計】")
    print(f"      {shares:,}株 × ¥{per_share_cash:,.2f}")
    print(f"      = ¥{total_cash:,.0f}")
    print(f"      = 約{total_cash/1e8:.2f}億円")

    # ============================================================
    # B) 普通株式対価
    # ============================================================
    print(f"\n  ■ 普通株式対価取得請求（転換）")
    if conversion_is_vwap:
        print(f"    ※ B種の取得価額は30営業日VWAP平均。以下は仮定値 ¥{conversion_price:,.1f} での計算")
    print(f"    計算式: (株数 × 払込金額相当額) ÷ 取得価額")
    print()

    # パターン1: 元本ベース
    spp = par_value / conversion_price
    total_common = shares * par_value / conversion_price
    print(f"    【パターン1: 払込金額ベース（標準）】")
    print(f"      1優先株 → ¥{par_value:,} ÷ ¥{conversion_price:,.1f} = {spp:,.2f}株")
    print(f"      全{shares:,}株 → {total_common:,.0f}株")
    print()

    # パターン2: 配当込み
    tv = par_value + total_div_claim
    spp2 = tv / conversion_price
    total_common2 = shares * tv / conversion_price
    print(f"    【パターン2: 累積配当込み（参考）】")
    print(f"      1優先株 → ¥{tv:,.2f} ÷ ¥{conversion_price:,.1f} = {spp2:,.2f}株")
    print(f"      全{shares:,}株 → {total_common2:,.0f}株")

    return {
        "per_share_cash": per_share_cash,
        "total_cash": total_cash,
        "total_common_par": total_common,
        "total_common_div": total_common2,
        "accumulated": total_accumulated,
        "current_div": current_year_div,
        "conversion_price": conversion_price,
    }


# ============================================================
# メイン
# ============================================================

if __name__ == "__main__":
    print()
    print_separator("━")
    print("  スターフライヤー（9206）優先株式 金銭対価・普通株転換 計算シート")
    print(f"  計算基準日: {CALC_DATE}")
    print(f"  払込期日:   {PAYMENT_DATE}")
    print_separator("━")
    print()
    print("  【前提条件】")
    print("  ・21/3期（3/9〜3/31）の配当は実際にキャッシュで支払済")
    print("  ・22/3期〜26/3期の配当は全額未払・累積")
    print("  ・A種累積複利: 年利5.0%、B種累積複利: 年利1.0%（★要確認）")
    print("  ・日割計算: 実日数 / 365")
    print()

    # --- A種 ---
    a = analyze_stock(
        name="A種優先株式",
        shares=A_SHARES_ISSUED, par_value=A_PAR_VALUE,
        dividend_rate=A_DIVIDEND_RATE, compound_rate=A_COMPOUND_RATE,
        conversion_price=A_CONVERSION_PRICE, conversion_is_vwap=False,
        cash_after_years=A_CASH_REDEMPTION_AFTER_YEARS,
    )
    print("\n")

    # --- B種 ---
    b = analyze_stock(
        name="B種優先株式",
        shares=B_SHARES_ISSUED, par_value=B_PAR_VALUE,
        dividend_rate=B_DIVIDEND_RATE, compound_rate=B_COMPOUND_RATE,
        conversion_price=B_VWAP_ASSUMED, conversion_is_vwap=True,
        cash_after_years=B_CASH_REDEMPTION_AFTER_YEARS,
        notes=[
            "配当率: 年率1.0%（A種の5.0%と異なる）",
            "転換価額: VWAPベース変動型（30営業日平均）",
            "金銭対価: 会社側の強制取得権（株主からの請求権なし）",
        ],
    )

    # ============================================================
    # B種 VWAP感応度テーブル
    # ============================================================
    print("\n")
    print_separator()
    print("【B種 転換株数のVWAP感応度テーブル】")
    print_separator()
    print("  ※ B種の取得価額は請求時のVWAP（30営業日平均）に連動")
    print("  ※ 下記はパターン1（払込金額ベース）での計算")
    print()
    print(f"    {'VWAP':>10s}  {'1株→普通株':>12s}  {'全2,500株→普通株':>16s}")
    print(f"    {'-'*10}  {'-'*12}  {'-'*16}")
    for vwap in [1500, 1800, 2000, 2100, 2500, 3000, 3500]:
        per = B_PAR_VALUE / vwap
        total = B_SHARES_ISSUED * B_PAR_VALUE / vwap
        print(f"    ¥{vwap:>8,}  {per:>10,.2f}株  {total:>14,.0f}株")

    # ============================================================
    # サマリー
    # ============================================================
    print("\n")
    print_separator("━")
    print("  【総合サマリー】")
    print_separator("━")

    print()
    print("  ┌──────────────────┬─────────────────────┬─────────────────────┐")
    print("  │                  │   A種優先株式        │   B種優先株式        │")
    print("  ├──────────────────┼─────────────────────┼─────────────────────┤")
    print(f"  │ 発行株数         │ {A_SHARES_ISSUED:>11,}株     │ {B_SHARES_ISSUED:>11,}株     │")
    print(f"  │ 払込総額         │        55億円       │        25億円       │")
    print(f"  │ 配当率           │      年率5.0%       │      年率1.0%       │")
    print(f"  │ 累積複利         │      年利5.0%       │    年利1.0%（★）    │")
    if A_CONVERSION_PRICE == B_VWAP_ASSUMED:
        print(f"  │ 転換価額         │   ¥{A_CONVERSION_PRICE:>8,.1f}（固定） │ VWAP変動型（参考{B_VWAP_ASSUMED:,}）│")
    else:
        print(f"  │ 転換価額         │   ¥{A_CONVERSION_PRICE:>8,.1f}（固定） │ VWAP変動型（参考{B_VWAP_ASSUMED:,}）│")
    print("  ├──────────────────┼─────────────────────┼─────────────────────┤")
    print(f"  │ 金銭対価(1株)    │ ¥{a['per_share_cash']:>14,.0f}    │ ¥{b['per_share_cash']:>14,.0f}    │")
    print(f"  │ 金銭対価(全株)   │    約{a['total_cash']/1e8:>7.2f}億円    │    約{b['total_cash']/1e8:>7.2f}億円    │")
    print("  ├──────────────────┼─────────────────────┼─────────────────────┤")
    print(f"  │ 転換株数(元本)   │  {a['total_common_par']:>13,.0f}株    │  {b['total_common_par']:>13,.0f}株    │")
    print(f"  │ 転換株数(配当込) │  {a['total_common_div']:>13,.0f}株    │  {b['total_common_div']:>13,.0f}株    │")
    print("  └──────────────────┴─────────────────────┴─────────────────────┘")
    print()

    tc = a["total_cash"] + b["total_cash"]
    tp = a["total_common_par"] + b["total_common_par"]
    td = a["total_common_div"] + b["total_common_div"]
    print(f"  A種+B種 金銭対価合計:         約{tc/1e8:.2f}億円")
    print(f"  A種+B種 転換株数合計(元本):   {tp:,.0f}株")
    print(f"  A種+B種 転換株数合計(配当込): {td:,.0f}株")

    print()
    print_separator()
    print("【重要な注意事項】")
    print_separator()
    print("""
  1. A種とB種で配当率が大きく異なる（A種5.0% vs B種1.0%）。
     B種の累積未払配当金の複利利率（1.0%と仮定）は有価証券届出書で要確認。

  2. B種の転換価額はVWAPベース変動型（30営業日平均）。
     上記のB種転換株数は仮定値¥{vwap_note:,}での計算。
     感応度テーブルも参照のこと。

  3. 本計算は発行時の全株数を前提。実際には一部転換・消却済み:
     ・A種: 一部が普通株1,800,000株と交換・消却済み
     ・B種: 2024年5月に一部取得・消却、普通株式を交付済み
     残存株数は最新の有価証券報告書で要確認。

  4. A種の金銭対価取得請求権は株主が行使可能（2026/3/9以降）。
     B種の金銭対価は会社側の強制取得権（2027/3/9以降）であり、
     2026/3/31時点では未到来。B種株主は普通株転換のみ請求可能。

  5. 金銭対価にはVWAP/取得価額に基づく調整条項がある可能性あり
     （30日VWAP平均÷取得価額×払込金額相当額、下限=払込金額相当額）。
     上記計算は最低保証額（払込金額+累積配当）ベース。

  6. 21/3期の日割配当（23日分）は支払済みのため累積に含めず。
""".format(vwap_note=B_VWAP_ASSUMED))

    print("参考資料:")
    print("  - 有価証券届出書: https://irbank.net/E26084/etc?f=S100KGBQ")
    print("  - 有価証券届出書PDF: https://f.irbank.net/pdf/E26084/etc/S100KGBQ.pdf")
    print("  - プルータス評価: https://www.plutuscon.jp/caseleads/10087")
