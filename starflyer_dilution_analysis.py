"""
スターフライヤー（9206）A種・B種種類株式の希薄化分析
=======================================================

前提条件（公開情報から）:
- A種種類株式: 5,500株 × 100万円/株 = 55億円 → 2022年4月に普通株180万株と交換済み・消却済み
- B種種類株式: 2,500株 × 100万円/株 = 25億円 → 2024年5月に一部取得・消却
- 現在の普通株式発行済株式数: 約3,784,076株 (2026年3月時点)
- 現在の株価: 約2,100円 (2026年3月時点)
- A種優先配当率: 年率5.0%

注意: 有価証券届出書PDFにアクセスできなかったため、一部推計値を含む
"""

# ==============================================================================
# 1. A種種類株式の転換価額の逆算（実績値から）
# ==============================================================================
# A種: 5,500株 → 普通株1,800,000株（2022年4月実績）
a_shares = 5_500
a_par_value = 1_000_000  # 1株100万円
a_common_shares_issued = 1_800_000

# A種の払込期日: 2021年3月9日、転換日: 2022年4月12日 → 約13ヶ月
# 累積配当: 5.0% × 13/12 ≈ 5.42%
a_dividend_rate = 0.05
a_months_accrued = 13
a_accrued_dividend_per_share = a_par_value * a_dividend_rate * a_months_accrued / 12
a_total_value_per_share = a_par_value + a_accrued_dividend_per_share

# 転換価額の逆算
# 交付普通株式数 = A種株数 × (払込金額 + 累積配当) / 転換価額
# 転換価額 = A種株数 × (払込金額 + 累積配当) / 交付普通株式数
a_conversion_price = a_shares * a_total_value_per_share / a_common_shares_issued
a_conversion_price_ex_dividend = a_shares * a_par_value / a_common_shares_issued

print("=" * 70)
print("【1】A種種類株式の転換価額（実績から逆算）")
print("=" * 70)
print(f"  A種発行株数:           {a_shares:,}株")
print(f"  払込金額:              ¥{a_par_value:,}/株")
print(f"  累積配当（約13ヶ月）:  ¥{a_accrued_dividend_per_share:,.0f}/株")
print(f"  交付普通株式数:        {a_common_shares_issued:,}株")
print(f"  転換価額（配当込み）:  ¥{a_conversion_price:,.1f}")
print(f"  転換価額（配当除き）:  ¥{a_conversion_price_ex_dividend:,.1f}")
print(f"  1 A種 → 普通株 {a_common_shares_issued/a_shares:.1f}株")

# ==============================================================================
# 2. B種種類株式の転換シミュレーション
# ==============================================================================
b_shares_original = 2_500
b_par_value = 1_000_000

# B種は2024年5月に一部取得・消却 → 残存株数不明のため、2パターンで計算
# パターン1: 全2,500株残存の場合
# パターン2: 1,500株（ANAHD分）残存の場合（推計）
# パターン3: 1,000株残存の場合（推計）

# B種の累積配当: 2021年3月～2026年3月 = 約5年
# B種の配当率はA種と同程度と仮定（年率5%前後、有報未確認のため推計）
b_dividend_rate_assumed = 0.05
b_years_accrued = 5
b_accrued_dividend_per_share = b_par_value * b_dividend_rate_assumed * b_years_accrued
b_total_value_per_share = b_par_value + b_accrued_dividend_per_share

# 転換価額はA種と同水準と仮定（有報で正確な値は要確認）
b_conversion_price = a_conversion_price_ex_dividend  # ¥3,055.56

print()
print("=" * 70)
print("【2】B種種類株式の転換シミュレーション")
print("=" * 70)
print(f"  B種発行株数（当初）:   {b_shares_original:,}株")
print(f"  払込金額:              ¥{b_par_value:,}/株")
print(f"  推定累積配当（5年）:   ¥{b_accrued_dividend_per_share:,.0f}/株")
print(f"  想定転換価額:          ¥{b_conversion_price:,.1f}（A種実績準用、要有報確認）")
print()

for scenario_name, b_remaining in [("全2,500株残存", 2_500), ("1,500株残存（推計）", 1_500), ("1,000株残存（推計）", 1_000)]:
    # 転換時の交付普通株式数 = B種株数 × (払込金額 + 累積配当) / 転換価額
    b_common_from_conversion = b_remaining * b_total_value_per_share / b_conversion_price
    print(f"  [{scenario_name}]")
    print(f"    交付普通株式数: {b_common_from_conversion:,.0f}株")

# ==============================================================================
# 3. 希薄化率の計算（仮に両方とも今転換した場合）
# ==============================================================================
current_common_shares = 3_784_076
current_stock_price = 2_100  # 概算

# A種は既に転換済みなので、現在の発行済株式数に含まれている
# 転換前のベース株数を逆算
base_shares_before_a = current_common_shares - a_common_shares_issued  # ≈ 1,984,076

print()
print("=" * 70)
print("【3】希薄化分析（仮に全種類株式を今普通株式に転換した場合）")
print("=" * 70)
print(f"  現在の発行済普通株式数:       {current_common_shares:,}株")
print(f"  種類株式発行前のベース株数:   {base_shares_before_a:,}株（推計）")
print(f"  A種転換で増加した普通株式数:  {a_common_shares_issued:,}株（転換済み）")
print()

# A種からの希薄化（既に発生済み）
a_dilution_pct = a_common_shares_issued / (base_shares_before_a + a_common_shares_issued) * 100
print(f"  ■ A種転換による希薄化率（発生済み）")
print(f"    = {a_common_shares_issued:,} / ({base_shares_before_a:,} + {a_common_shares_issued:,})")
print(f"    = {a_dilution_pct:.1f}%")

# B種からの希薄化（仮に今転換した場合）
print()
for scenario_name, b_remaining in [("全2,500株残存", 2_500), ("1,500株残存（推計）", 1_500), ("1,000株残存（推計）", 1_000)]:
    b_common = b_remaining * b_total_value_per_share / b_conversion_price
    total_after = current_common_shares + b_common
    b_dilution_from_current = b_common / total_after * 100
    b_dilution_from_base = b_common / (base_shares_before_a + b_common) * 100

    print(f"  ■ B種転換による希薄化率（{scenario_name}）")
    print(f"    現在ベース:  {b_common:,.0f} / {total_after:,.0f} = {b_dilution_from_current:.1f}%")
    print(f"    発行前ベース: {b_common:,.0f} / {base_shares_before_a + b_common:,.0f} = {b_dilution_from_base:.1f}%")
    print()

# A種 + B種 合計の希薄化（発行前ベース）
b_common_full = b_shares_original * b_total_value_per_share / b_conversion_price
total_new_shares = a_common_shares_issued + b_common_full
total_post_conversion = base_shares_before_a + total_new_shares
total_dilution = total_new_shares / total_post_conversion * 100

print(f"  ■ A種＋B種 合計の希薄化率（発行前ベース、B種全量）")
print(f"    A種: {a_common_shares_issued:,}株 + B種: {b_common_full:,.0f}株 = 合計 {total_new_shares:,.0f}株")
print(f"    = {total_new_shares:,.0f} / {total_post_conversion:,.0f} = {total_dilution:.1f}%")

# ==============================================================================
# 4. ITM / OTM 判定
# ==============================================================================
print()
print("=" * 70)
print("【4】イン・ザ・マネー（ITM）/ アウト・オブ・ザ・マネー（OTM）判定")
print("=" * 70)
print(f"  現在の普通株式の株価: ¥{current_stock_price:,}")
print(f"  推定転換価額:         ¥{b_conversion_price:,.1f}")
print()

# 転換の経済合理性判定
# ITM = 転換で得られる普通株式の時価 > 優先株式の清算価値（払込金額＋累積配当）

# A種（既に転換済みだが仮に判定）
a_common_per_share = a_total_value_per_share / b_conversion_price
a_conversion_value = a_common_per_share * current_stock_price
a_liquidation_value = a_total_value_per_share

print(f"  ■ A種種類株式（参考、既に転換済み）")
print(f"    1 A種 → 普通株 {a_common_per_share:.1f}株")
print(f"    転換で得られる普通株の時価: ¥{a_conversion_value:,.0f}")
print(f"    保有継続の清算価値:         ¥{a_liquidation_value:,.0f}")
if a_conversion_value > a_liquidation_value:
    print(f"    → ITM（イン・ザ・マネー）: 転換した方が有利（差額 +¥{a_conversion_value - a_liquidation_value:,.0f}）")
else:
    print(f"    → OTM（アウト・オブ・ザ・マネー）: 転換すると不利（差額 -¥{a_liquidation_value - a_conversion_value:,.0f}）")

# 株価がいくらならITMになるか
a_breakeven_price = a_liquidation_value / a_common_per_share
print(f"    ITMになる株価: ¥{a_breakeven_price:,.0f}以上")

print()

# B種（現時点で仮に転換した場合）
b_common_per_share = b_total_value_per_share / b_conversion_price
b_conversion_value = b_common_per_share * current_stock_price
b_liquidation_value = b_total_value_per_share

print(f"  ■ B種種類株式")
print(f"    1 B種 → 普通株 {b_common_per_share:.1f}株")
print(f"    転換で得られる普通株の時価: ¥{b_conversion_value:,.0f}")
print(f"    保有継続の清算価値:         ¥{b_liquidation_value:,.0f}")
if b_conversion_value > b_liquidation_value:
    print(f"    → ITM（イン・ザ・マネー）: 転換した方が有利（差額 +¥{b_conversion_value - b_liquidation_value:,.0f}）")
else:
    print(f"    → OTM（アウト・オブ・ザ・マネー）: 転換すると不利（差額 -¥{b_liquidation_value - b_conversion_value:,.0f}）")

b_breakeven_price = b_liquidation_value / b_common_per_share
print(f"    ITMになる株価: ¥{b_breakeven_price:,.0f}以上")

print()
print("=" * 70)
print("【注意事項】")
print("=" * 70)
print("  ・転換価額はA種の実績（5,500株→180万株）から逆算した推計値です")
print("  ・B種の配当率・転換価額は有価証券届出書で要確認（A種準用で推計）")
print("  ・B種の残存株数は2024年5月の一部取得・消却後の正確な値が不明")
print("  ・A種は2022年4月に全量転換・消却済みで現存しません")
print("  ・正確な分析には有価証券届出書原文の確認が必要です")
print("    → https://f.irbank.net/pdf/E26084/etc/S100KGBQ.pdf")
