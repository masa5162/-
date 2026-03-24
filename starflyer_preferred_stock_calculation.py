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

# --- 確認済みパラメータ（有価証券届出書より） ---
A_SHARES_ISSUED = 5_500          # A種 発行株数
A_PAR_VALUE = 1_000_000          # A種 払込金額相当額（円/株）
A_DIVIDEND_RATE = 0.05           # A種 優先配当率 年率5.0%
A_CONVERSION_PRICE = 1_651.9     # A種 当初取得価額（円）
A_CASH_REDEMPTION_AFTER_YEARS = 5  # A種 金銭対価取得条項: 払込期日の5年後以降

B_SHARES_ISSUED = 2_500          # B種 発行株数
B_PAR_VALUE = 1_000_000          # B種 払込金額相当額（円/株）

# --- 要確認パラメータ（有価証券届出書PDF未取得のため推定） ---
# ※ B種の配当率・転換価額は有価証券届出書原本で要確認
B_DIVIDEND_RATE = 0.05           # B種 優先配当率 ★推定値（A種と同率と仮定）
B_CONVERSION_PRICE = 1_651.9     # B種 当初取得価額 ★推定値（A種と同額と仮定）
B_CASH_REDEMPTION_AFTER_YEARS = 6  # B種 金銭対価取得条項: 払込期日の6年後以降

COMPOUND_RATE = 0.05  # 累積未払配当金の複利利率 年利5.0%

PAYMENT_DATE = date(2021, 3, 9)     # 払込期日
CALC_DATE = date(2026, 3, 31)       # 計算基準日（26/3月末）


# ============================================================
# 1. 各期の優先配当金の計算（日割計算）
# ============================================================
# 配当計算ルール:
#   配当基準日の属する事業年度の初日から配当基準日までの実日数
#   1年=365日で日割計算
#   配当額 = 払込金額相当額 × 年率 × 実日数 / 365

@dataclass
class FiscalYear:
    """事業年度"""
    label: str           # 表示名（例: "22/3期"）
    start: date          # 事業年度の初日
    end: date            # 配当基準日（事業年度末）
    paid: bool           # 支払済みか


fiscal_years = [
    FiscalYear("21/3期", PAYMENT_DATE,   date(2021, 3, 31), paid=True),   # 日割（支払済）
    FiscalYear("22/3期", date(2021, 4, 1), date(2022, 3, 31), paid=False),
    FiscalYear("23/3期", date(2022, 4, 1), date(2023, 3, 31), paid=False),
    FiscalYear("24/3期", date(2023, 4, 1), date(2024, 3, 31), paid=False),  # 2024年は閏年
    FiscalYear("25/3期", date(2024, 4, 1), date(2025, 3, 31), paid=False),
    FiscalYear("26/3期", date(2025, 4, 1), date(2026, 3, 31), paid=False),
]


def calc_dividend(par_value: int, rate: float, fy: FiscalYear) -> float:
    """1株あたりの優先配当金額を日割計算"""
    actual_days = (fy.end - fy.start).days + 1  # 初日算入
    return par_value * rate * actual_days / 365


def calc_accumulated_unpaid(par_value: int, rate: float,
                            fiscal_years: list, calc_date: date) -> dict:
    """
    累積未払配当金相当額を複利計算で算出

    ルール: 未払配当金は翌事業年度の初日以降、実際に支払われる日まで
            年利5.0%で1年毎の複利計算により累積
    """
    results = []
    total_accumulated = 0.0

    for fy in fiscal_years:
        dividend = calc_dividend(par_value, rate, fy)

        if fy.paid:
            results.append({
                "period": fy.label,
                "days": (fy.end - fy.start).days + 1,
                "base_dividend": dividend,
                "status": "支払済",
                "compound_years": 0,
                "accumulated_value": 0.0,
            })
            continue

        # 26/3期（当期）の配当は「日割未払優先配当金」として別計上
        if fy.end == calc_date:
            results.append({
                "period": fy.label,
                "days": (fy.end - fy.start).days + 1,
                "base_dividend": dividend,
                "status": "当期（日割未払優先配当金）",
                "compound_years": 0,
                "accumulated_value": dividend,  # 複利なし
            })
            continue

        # 複利計算: 翌事業年度初日から計算基準日まで何年経過したか
        # 複利は各事業年度末（3/31）に適用される
        # 例: 22/3期未払 → 4/1/2022から累積開始 → 3/31/2023, 3/31/2024, 3/31/2025, 3/31/2026 で4回複利
        compound_start = fy.end + timedelta(days=1)  # 翌事業年度初日
        years_elapsed = calc_date.year - compound_start.year
        if calc_date.month < compound_start.month or \
           (calc_date.month == compound_start.month and calc_date.day < compound_start.day):
            years_elapsed -= 1
        # 3/31→3/31なので、4/1開始に対して3/31到達は丁度1年弱だが
        # 事業年度末ベースでの複利適用のため、4/1/YYYY → 3/31/(YYYY+1) で1回複利
        # 従って compound_start(4/1) → calc_date(3/31) の場合、年度末ベースで正しい回数
        years_elapsed = calc_date.year - compound_start.year

        accumulated = dividend * (1 + COMPOUND_RATE) ** years_elapsed
        total_accumulated += accumulated

        results.append({
            "period": fy.label,
            "days": (fy.end - fy.start).days + 1,
            "base_dividend": dividend,
            "status": f"未払（{years_elapsed}年複利）",
            "compound_years": years_elapsed,
            "accumulated_value": accumulated,
        })

    return results


# ============================================================
# 2. 計算実行 & 結果表示
# ============================================================

def print_separator(char="=", width=80):
    print(char * width)


def analyze_preferred_stock(name: str, shares: int, par_value: int,
                            dividend_rate: float, conversion_price: float,
                            cash_after_years: int, is_estimated: bool = False):
    """優先株式の金銭対価・転換株数を計算"""

    print_separator()
    print(f"【{name}】")
    if is_estimated:
        print("  ★ 配当率・転換価額は推定値（有価証券届出書原本で要確認）")
    print_separator()

    print(f"\n  ■ 基本条件")
    print(f"    発行株数:         {shares:,}株")
    print(f"    払込金額相当額:   ¥{par_value:,}/株")
    print(f"    優先配当率:       年率{dividend_rate*100:.1f}%")
    print(f"    当初取得価額:     ¥{conversion_price:,.1f}")
    print(f"    金銭対価取得:     払込期日の{cash_after_years}年後以降")
    cash_available_date = date(PAYMENT_DATE.year + cash_after_years,
                               PAYMENT_DATE.month, PAYMENT_DATE.day)
    print(f"                      → {cash_available_date} 以降")
    if CALC_DATE >= cash_available_date:
        print(f"                      → 2026/3/31時点: 行使可能 ✓")
    else:
        print(f"                      → 2026/3/31時点: 行使不可 ✗（会社側の強制取得は不可）")

    # --- 配当計算 ---
    print(f"\n  ■ 各期の優先配当金（1株あたり、日割計算）")
    print(f"    {'期':8s} {'日数':>6s} {'基本配当額':>14s} {'状態':16s} {'複利年数':>8s} {'累積後金額':>16s}")
    print(f"    {'-'*8} {'-'*6} {'-'*14} {'-'*16} {'-'*8} {'-'*16}")

    results = calc_accumulated_unpaid(par_value, dividend_rate,
                                      fiscal_years, CALC_DATE)

    total_accumulated_dividends = 0.0  # 22/3〜25/3の累積未払配当金
    current_year_dividend = 0.0         # 26/3の日割未払優先配当金

    for r in results:
        print(f"    {r['period']:8s} {r['days']:>4d}日"
              f"  ¥{r['base_dividend']:>12,.2f}"
              f"  {r['status']:16s}"
              f"  {r['compound_years']:>6d}年"
              f"  ¥{r['accumulated_value']:>14,.2f}")

        if r["status"] == "支払済":
            continue
        elif "当期" in r["status"]:
            current_year_dividend = r["accumulated_value"]
        else:
            total_accumulated_dividends += r["accumulated_value"]

    print()
    print(f"    累積未払配当金相当額（22/3〜25/3、複利後）: ¥{total_accumulated_dividends:>14,.2f}")
    print(f"    日割未払優先配当金額（26/3期）:             ¥{current_year_dividend:>14,.2f}")
    total_dividend_claim = total_accumulated_dividends + current_year_dividend
    print(f"    配当関連請求額 合計:                        ¥{total_dividend_claim:>14,.2f}")

    # ============================================================
    # A) 金銭対価取得請求の場合
    # ============================================================
    print(f"\n  ■ 金銭対価取得請求額（2026/3/31時点）")
    print(f"    計算式: 株数 × (払込金額相当額 + 累積未払配当金相当額 + 日割未払優先配当金額)")
    print()

    per_share_cash = par_value + total_dividend_claim
    print(f"    【1株あたり】")
    print(f"      払込金額相当額:         ¥{par_value:>14,}")
    print(f"      累積未払配当金相当額:   ¥{total_accumulated_dividends:>14,.2f}")
    print(f"      日割未払優先配当金額:   ¥{current_year_dividend:>14,.2f}")
    print(f"      ─────────────────────────────────────")
    print(f"      合計:                   ¥{per_share_cash:>14,.2f}")
    print()

    total_cash = shares * per_share_cash
    print(f"    【全{shares:,}株の合計】")
    print(f"      {shares:,}株 × ¥{per_share_cash:,.2f}")
    print(f"      = ¥{total_cash:,.0f}")
    print(f"      = 約{total_cash/100_000_000:.2f}億円")

    # ============================================================
    # B) 普通株式対価取得請求の場合
    # ============================================================
    print(f"\n  ■ 普通株式対価取得請求（転換）")
    print(f"    計算式: (優先株式数 × 払込金額相当額) ÷ 取得価額")
    print(f"    ※ 累積未払配当金は転換対価に含まれない前提（金銭+普通株式対価の場合は別途現金精算）")
    print()

    # パターン1: 普通株式のみ（払込金額相当額ベース）
    shares_per_preferred = par_value / conversion_price
    total_common_shares = shares * par_value / conversion_price

    print(f"    【パターン1: 普通株式のみ対価（払込金額ベース）】")
    print(f"      1優先株 → ¥{par_value:,} ÷ ¥{conversion_price:,.1f} = {shares_per_preferred:,.2f}株")
    print(f"      全{shares:,}株 → {shares:,} × {shares_per_preferred:,.2f} = {total_common_shares:,.0f}株")
    print()

    # パターン2: 累積配当込みで転換（仮に配当も株式化される場合）
    total_value_per_share = par_value + total_dividend_claim
    shares_per_preferred_with_div = total_value_per_share / conversion_price
    total_common_with_div = shares * total_value_per_share / conversion_price

    print(f"    【パターン2: 累積配当込みで転換する場合（参考）】")
    print(f"      1優先株 → ¥{total_value_per_share:,.2f} ÷ ¥{conversion_price:,.1f} = {shares_per_preferred_with_div:,.2f}株")
    print(f"      全{shares:,}株 → {total_common_with_div:,.0f}株")

    return {
        "per_share_cash": per_share_cash,
        "total_cash": total_cash,
        "total_common_par_only": total_common_shares,
        "total_common_with_div": total_common_with_div,
        "accumulated_dividends": total_accumulated_dividends,
        "current_year_dividend": current_year_dividend,
    }


# ============================================================
# メイン実行
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
    print("  ・21/3期（3/9〜3/31の22日間）の配当は実際にキャッシュで支払済")
    print("  ・22/3期〜26/3期の配当は全額未払・累積")
    print("  ・累積未払配当金は年利5.0%で1年毎の複利計算により累積")
    print("  ・日割計算: 実日数 / 365")
    print()

    # A種
    a_result = analyze_preferred_stock(
        name="A種優先株式",
        shares=A_SHARES_ISSUED,
        par_value=A_PAR_VALUE,
        dividend_rate=A_DIVIDEND_RATE,
        conversion_price=A_CONVERSION_PRICE,
        cash_after_years=A_CASH_REDEMPTION_AFTER_YEARS,
        is_estimated=False,
    )

    print()
    print()

    # B種
    b_result = analyze_preferred_stock(
        name="B種優先株式",
        shares=B_SHARES_ISSUED,
        par_value=B_PAR_VALUE,
        dividend_rate=B_DIVIDEND_RATE,
        conversion_price=B_CONVERSION_PRICE,
        cash_after_years=B_CASH_REDEMPTION_AFTER_YEARS,
        is_estimated=True,
    )

    # ============================================================
    # サマリー
    # ============================================================
    print()
    print()
    print_separator("━")
    print("  【総合サマリー】")
    print_separator("━")

    print()
    print("  ┌──────────────────┬────────────────────┬────────────────────┐")
    print("  │                  │   A種優先株式       │   B種優先株式       │")
    print("  ├──────────────────┼────────────────────┼────────────────────┤")
    print(f"  │ 発行株数         │ {A_SHARES_ISSUED:>10,}株     │ {B_SHARES_ISSUED:>10,}株     │")
    print(f"  │ 払込総額         │ {A_SHARES_ISSUED * A_PAR_VALUE / 1e8:>10.0f}億円    │ {B_SHARES_ISSUED * B_PAR_VALUE / 1e8:>10.0f}億円    │")
    print(f"  │ 配当率           │ {'年率5.0%':>14s}    │ {'年率5.0%★':>14s}   │")
    print(f"  │ 転換価額         │ ¥{A_CONVERSION_PRICE:>10,.1f}    │ ¥{B_CONVERSION_PRICE:>10,.1f}★  │")
    print("  ├──────────────────┼────────────────────┼────────────────────┤")
    print(f"  │ 金銭対価(1株)    │ ¥{a_result['per_share_cash']:>13,.0f}   │ ¥{b_result['per_share_cash']:>13,.0f}   │")
    print(f"  │ 金銭対価(全株)   │ {a_result['total_cash']/1e8:>10.2f}億円    │ {b_result['total_cash']/1e8:>10.2f}億円    │")
    print("  ├──────────────────┼────────────────────┼────────────────────┤")
    print(f"  │ 転換株数(元本)   │ {a_result['total_common_par_only']:>12,.0f}株   │ {b_result['total_common_par_only']:>12,.0f}株   │")
    print(f"  │ 転換株数(配当込) │ {a_result['total_common_with_div']:>12,.0f}株   │ {b_result['total_common_with_div']:>12,.0f}株   │")
    print("  └──────────────────┴────────────────────┴────────────────────┘")
    print()
    total_cash_all = a_result["total_cash"] + b_result["total_cash"]
    total_common_par = a_result["total_common_par_only"] + b_result["total_common_par_only"]
    total_common_div = a_result["total_common_with_div"] + b_result["total_common_with_div"]
    print(f"  A種+B種 金銭対価合計:         約{total_cash_all/1e8:.2f}億円")
    print(f"  A種+B種 転換株数合計(元本):   {total_common_par:,.0f}株")
    print(f"  A種+B種 転換株数合計(配当込): {total_common_div:,.0f}株")

    print()
    print_separator()
    print("【重要な注意事項】")
    print_separator()
    print("""
  1. ★印のパラメータは推定値です。B種の配当率・転換価額は
     有価証券届出書（S100KGBQ）の原本で確認が必要です。

  2. 本計算は発行時の全株数を前提としています。
     実際には以下の一部転換・消却が行われています:
     ・A種: 一部が普通株1,800,000株と交換・消却済み
     ・B種: 2024年5月に一部取得・消却、普通株式を交付済み
     残存株数は最新の有価証券報告書で要確認。

  3. A種の金銭対価取得請求権は株主が行使可能（払込期日の5年後以降）。
     B種の金銭対価取得条項は会社側の強制取得権（払込期日の6年後=2027/3/9以降）
     であり、2026/3/31時点では会社はまだ行使できません。
     B種株主には金銭対価の取得請求権はなく、普通株式対価のみです。

  4. 転換（普通株式対価取得請求）の際、累積未払配当金が対価に含まれるか
     否かは取得請求権の種類によります:
     ・「普通株式対価」のみ → 通常は払込金額ベース（パターン1）
     ・「金銭及び普通株式対価」→ 累積配当は現金、元本は株式（A種のみ）

  5. 21/3期の日割配当（22日分、約3,014円/株）は支払済みのため
     累積未払配当金には含めていません。
""")

    print()
    print("参考資料:")
    print("  - 有価証券届出書: https://irbank.net/E26084/etc?f=S100KGBQ")
    print("  - 有価証券届出書PDF: https://f.irbank.net/pdf/E26084/etc/S100KGBQ.pdf")
    print("  - プルータス評価: https://www.plutuscon.jp/caseleads/10087")
