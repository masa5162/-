#!/usr/bin/env python3
"""
上場会社TOB取引分析：他社株TOB + 自己株TOB 組み合わせスキーム
==============================================================

調査対象スキーム:
  ① 大株主と不応募契約を締結した上で、一般株主を対象とした他社株TOBを実施
  ② ①の成立を条件とした、大株主との自己株TOB（対象会社による自己株式の公開買付）

条件:
  - 直近5ヵ年（2021年〜2026年3月）
  - 本件後も対象会社は上場維持
  - 買い手（公開買付者）はマジョリティ（過半数）を獲得

調査方法:
  - Web検索（日経、MARR Online、法律事務所ニュースレター等）
  - EDINET公開買付届出書の分析
  - 参考文献: AMT「公開買付けに関する諸論点⑤ -自己株公開買付け-」(2021年5月)
"""

import json
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 1. スキーム定義
# ============================================================

SCHEME_DESCRIPTION = """
【スキームの概要】

  ┌─────────────────────────────────────────────────────────┐
  │  Step 1: 他社株TOB（公開買付者 → 一般株主）              │
  │    ・公開買付者が対象会社株式を一般株主から取得            │
  │    ・大株主は「不応募契約」を締結（TOBに応じない）         │
  │    ・買付上限を設定し、上場維持を前提とする                │
  │    ・公開買付者はマジョリティ（50%超）を取得               │
  │                                                          │
  │  Step 2: 自己株TOB（対象会社 → 大株主）                   │
  │    ・Step 1の成立を条件として実施                          │
  │    ・対象会社が自己株式の公開買付を実施                    │
  │    ・大株主が応募し、保有株式の全部または一部を売却        │
  │    ・ディスカウント価格（みなし配当の益金不算入を活用）    │
  │    ・自己株取得→消却により、公開買付者の議決権比率が上昇  │
  └─────────────────────────────────────────────────────────┘

【大株主の税務メリット】
  ・内国法人である大株主は、自己株TOBに応募することで「みなし配当」が発生
  ・受取配当等の益金不算入制度の適用により、税引後手取額が有利になりうる
  ・そのため、他社株TOB価格よりディスカウントした価格でも経済的に合理的

【上場維持の要件】
  ・流通株式比率: プライム35%以上、スタンダード25%以上
  ・流通株式時価総額: プライム100億円以上、スタンダード10億円以上
  ・株主数: プライム800人以上、スタンダード400人以上
"""


# ============================================================
# 2. 調査結果
# ============================================================

@dataclass
class TOBTransaction:
    """TOB取引の記録"""
    year: int
    target_company: str                # 対象会社
    target_ticker: str                 # 証券コード
    acquirer: str                      # 公開買付者（買い手）
    major_shareholder: str             # 大株主（不応募・自己株TOBの相手方）
    tob_price: Optional[str] = None    # 他社株TOB価格
    self_tender_price: Optional[str] = None  # 自己株TOB価格
    listing_maintained: bool = True    # 上場維持
    majority_acquired: bool = True     # マジョリティ取得
    scheme_matches: bool = True        # スキーム完全一致
    notes: str = ""                    # 備考
    status: str = ""                   # 案件ステータス
    acquirer_ownership_post: str = ""  # 取得後の議決権比率


# ============================================================
# 3. 調査結果：完全一致案件（直近5年：2021-2026）
# ============================================================

EXACT_MATCH_TRANSACTIONS = []
# ※ 公開情報のWeb検索の範囲では、以下の条件を「全て」満たす案件は
#    確認できませんでした:
#    (1) 大株主と不応募契約を締結
#    (2) 一般株主向けの他社株TOBを実施
#    (3) (2)の成立を条件として自己株TOBを実施
#    (4) 対象会社が上場維持
#    (5) 買い手がマジョリティ取得
#    (6) 2021年〜2026年の案件


# ============================================================
# 4. 参考：類似スキーム案件（条件の一部が異なるもの）
# ============================================================

SIMILAR_TRANSACTIONS = [

    # -------------------------------------------------------
    # 参考1: ティーガイア（2024年）
    # 他社株TOB + 自己株TOB + 不応募契約 → 但し上場「廃止」
    # -------------------------------------------------------
    TOBTransaction(
        year=2024,
        target_company="ティーガイア",
        target_ticker="3738",
        acquirer="BCJ-82-1（ベインキャピタル系SPC）",
        major_shareholder="住友商事（41.80%）、光通信グループ",
        tob_price="2,670円/株（ディスカウントTOB、終値3,635円比△26.55%）",
        self_tender_price="自己株TOB①: 2,045円（住友商事13.61%分）、"
                         "自己株TOB②: 2,473円（光通信全株分）",
        listing_maintained=False,  # ★ 上場廃止
        majority_acquired=True,
        scheme_matches=False,  # 上場維持の条件を満たさない
        notes=(
            "住友商事が「不応募合意」を締結。他社株TOB＋自己株TOBの組み合わせ。"
            "但し最終的に非公開化（上場廃止）を企図。"
            "住友商事の残余株式はベインキャピタルが相対取得。"
            "分配可能額の制約（577億円）から、自己株TOBを2回に分けて実施。"
        ),
        status="2024年9月30日公表、2025年3月上場廃止",
        acquirer_ownership_post="非公開化（ベインキャピタル100%）",
    ),

    # -------------------------------------------------------
    # 参考2: ソフトバンク → ヤフー/Zホールディングス（2018-2019年）
    # 第三者割当増資 + 自己株TOB → 上場維持、マジョリティ取得
    # 但し5ヵ年外 & 他社株TOBではなく第三者割当増資
    # -------------------------------------------------------
    TOBTransaction(
        year=2019,
        target_company="ヤフー（現Zホールディングス）",
        target_ticker="4689",
        acquirer="ソフトバンク（携帯事業会社）",
        major_shareholder="ソフトバンクグループジャパン（SBGJ）",
        tob_price="N/A（他社株TOBではなく第三者割当増資 @302円/株）",
        self_tender_price="287円/株（ディスカウントTOB）",
        listing_maintained=True,  # ★ 上場維持
        majority_acquired=True,   # ★ ソフトバンクが44.64%→連結子会社化
        scheme_matches=False,  # 他社株TOBではなく第三者割当増資
        notes=(
            "第三者割当増資（約4,565億円）＋自己株TOBの組み合わせ。"
            "SBGJが自己株TOBに応募（ディスカウント価格）。"
            "みなし配当の益金不算入を活用した税務メリットあり。"
            "ヤフーは上場を維持したままソフトバンクの連結子会社に。"
            "但し「他社株TOB」ではなく「第三者割当増資」を使用しているため、"
            "ご質問のスキームとは厳密には異なる。"
        ),
        status="2019年5月公表、同年6月完了",
        acquirer_ownership_post="ソフトバンク 約44.64%（連結子会社）",
    ),

    # -------------------------------------------------------
    # 参考3: KDDI → ローソン（2024年）
    # 他社株TOB + 大株主（三菱商事）不応募 → 但し上場「廃止」
    # 自己株TOBの組み合わせはなし
    # -------------------------------------------------------
    TOBTransaction(
        year=2024,
        target_company="ローソン",
        target_ticker="2651",
        acquirer="KDDI",
        major_shareholder="三菱商事（50.06%→不応募）",
        tob_price="10,360円/株（プレミアム18.79%）",
        self_tender_price="N/A（自己株TOBの組み合わせなし）",
        listing_maintained=False,  # ★ 上場廃止
        majority_acquired=True,
        scheme_matches=False,  # 上場廃止 & 自己株TOBなし
        notes=(
            "三菱商事が不応募合意。KDDIがTOBで一般株主から取得後、"
            "スクイーズアウトにより上場廃止。"
            "最終的にKDDI 50%・三菱商事 50%の共同経営体制。"
            "自己株TOBの組み合わせは使用していない。"
        ),
        status="2024年2月公表、2024年7月上場廃止",
        acquirer_ownership_post="KDDI 50%、三菱商事 50%",
    ),

    # -------------------------------------------------------
    # 参考4: W&Dインベストメントデザイン → ライトオン（2024年）
    # ディスカウントTOB + 上場維持 + マジョリティ取得
    # 但し大株主は「応募」側（不応募ではない）& 自己株TOBなし
    # -------------------------------------------------------
    TOBTransaction(
        year=2024,
        target_company="ライトオン",
        target_ticker="7445",
        acquirer="W&Dインベストメントデザイン（ワールド・DBJ系）",
        major_shareholder="藤原興産（創業家資産管理会社）→ TOBに応募",
        tob_price="110円/株（ディスカウントTOB、終値311円比△64.63%）",
        self_tender_price="N/A（自己株TOBなし）",
        listing_maintained=True,   # ★ 上場維持
        majority_acquired=True,    # ★ 約52%取得
        scheme_matches=False,  # 大株主が「応募」側 & 自己株TOBなし
        notes=(
            "大株主（創業家）がTOBに全株応募するスキーム。"
            "第三者割当増資後の大株主持分を全量取得。"
            "上場維持＋マジョリティ取得だが、"
            "不応募契約＋自己株TOBの組み合わせではない。"
        ),
        status="2024年12月TOB成立、上場維持（東証スタンダード）",
        acquirer_ownership_post="約52%（連結子会社）",
    ),

    # -------------------------------------------------------
    # 参考5: LINEヤフー 自己株TOB（2024年・2025年）
    # 上場維持目的の自己株TOB
    # 但し他社株TOBとの組み合わせではない
    # -------------------------------------------------------
    TOBTransaction(
        year=2024,
        target_company="LINEヤフー",
        target_ticker="4689",
        acquirer="N/A（他社株TOBなし）",
        major_shareholder="Aホールディングス（SB・ネイバー系、64.42%→応募）",
        tob_price="N/A（他社株TOBなし）",
        self_tender_price="388円/株（2024年）、533円/株（2025年）",
        listing_maintained=True,   # ★ 上場維持
        majority_acquired=False,   # 既にAHDが過半数保有
        scheme_matches=False,  # 他社株TOBとの組み合わせなし
        notes=(
            "上場維持基準（流通株式比率35%）を満たすための自己株TOB。"
            "Aホールディングスが応募契約を締結。"
            "他社株TOBとの組み合わせスキームではない。"
        ),
        status="2024年8月実施完了、2025年5月第2回発表",
        acquirer_ownership_post="N/A",
    ),

    # -------------------------------------------------------
    # 参考6: 黒田電気（2017-2018年）
    # 他社株TOB + 自己株TOB → 但し上場廃止 & 5ヵ年外
    # -------------------------------------------------------
    TOBTransaction(
        year=2018,
        target_company="黒田電気",
        target_ticker="7517",
        acquirer="KMホールディングス（MBKパートナーズ系SPC）",
        major_shareholder="（旧村上ファンド系等）",
        tob_price="2,720円/株",
        self_tender_price="自己株TOBで発行済24%を取得",
        listing_maintained=False,  # ★ 上場廃止
        majority_acquired=True,
        scheme_matches=False,  # 上場廃止 & 5ヵ年外
        notes=(
            "他社株TOB後に自己株TOBを実施。"
            "自己株TOBにより発行済株式数が減少し、"
            "KMHDの議決権比率が91.3%に上昇→スクイーズアウト→上場廃止。"
            "他社株TOB＋自己株TOBの典型的な組み合わせ事例。"
            "但し最終目的は完全子会社化・非公開化。"
        ),
        status="2017年他社株TOB、2018年2月自己株TOB、同年3月上場廃止",
        acquirer_ownership_post="MBKパートナーズ100%（完全子会社化）",
    ),
]


# ============================================================
# 5. 分析・考察
# ============================================================

ANALYSIS = """
【調査結果の総括】

■ 結論:
  公開情報のWeb検索の範囲において、以下の条件を「全て」満たす案件は
  2021年〜2026年3月の期間では確認できませんでした:

  (1) 大株主と不応募契約を締結
  (2) 一般株主向けの他社株TOBを実施し、買い手がマジョリティ取得
  (3) (2)の成立を条件として対象会社が自己株TOBを実施
  (4) 自己株TOBで大株主が保有株を売却
  (5) 対象会社が上場を維持

■ 理由の考察:
  1. 近年の「他社株TOB＋自己株TOB」の組み合わせは、ほぼ全て
     「完全子会社化・非公開化」を最終目的としており、上場維持を
     前提とするケースは極めて稀
     → ティーガイア(2024)、黒田電気(2017-2018) 等

  2. 「上場維持＋マジョリティ取得」目的のTOBでは、
     部分的TOB（買付上限設定）や第三者割当増資が主流であり、
     自己株TOBとの組み合わせは一般的でない
     → ZホールディングスのZOZO子会社化(2019)はTOB単独
     → ソフトバンクのヤフー子会社化(2019)は第三者割当+自己株TOB

  3. 上場維持を前提とする場合、自己株TOBを組み合わせると
     発行済株式数が減少し、流通株式基準への抵触リスクが高まるため、
     スキームとしての合理性が限定的

  4. 2024年以降のTOB急増（年間100件超）においても、
     大半はMBO・完全子会社化型であり、上場維持型の組み合わせ
     スキームは確認できず

■ 確認のための追加調査手段:
  1. EDINET書類全文検索
     https://disclosure2.edinet-fsa.go.jp/weee0070.aspx
     → 「自己株式の公開買付」「不応募」「上場廃止を企図するものではなく」
        で検索

  2. レコフM&Aデータベース（MARR Pro）（有料）
     → TOB案件の詳細検索・フィルタリングが可能
     → 「自己株TOB」「他社株TOB」の組み合わせで絞込み

  3. TDnet適時開示情報
     https://www.release.tdnet.info/inbs/I_main_00.html
     → 「自己株式の公開買付」で検索

  4. 法律事務所ニュースレター
     → AMT「公開買付けに関する諸論点⑤」(2021年5月)
        https://www.amt-law.com/asset/pdf/bulletins1_pdf/210525.pdf
     → AMT「公開買付けに関する諸論点⑥ 親会社による子会社に対する
        公開買付けと子会社による自己株公開買付けを組み合わせた取引」
        https://www.amt-law.com/asset/pdf/bulletins1_pdf/210531.pdf
"""


# ============================================================
# 6. 出力
# ============================================================

def print_section(title: str):
    print(f"\n{'='*72}")
    print(f"  {title}")
    print(f"{'='*72}\n")


def print_subsection(title: str):
    print(f"\n--- {title} ---\n")


def main():
    print("=" * 72)
    print("  上場会社TOB取引分析")
    print("  他社株TOB + 大株主不応募契約 + 自己株TOB 組み合わせスキーム")
    print("  対象期間: 2021年〜2026年3月")
    print("  条件: 上場維持 & マジョリティ取得")
    print("=" * 72)

    # スキーム概要
    print_section("1. 調査対象スキームの概要")
    print(SCHEME_DESCRIPTION)

    # 完全一致案件
    print_section("2. 条件完全一致案件（2021-2026年）")
    if not EXACT_MATCH_TRANSACTIONS:
        print("  ★ 公開情報の範囲では、条件を全て満たす案件は確認できませんでした。")
        print()
        print("  条件:")
        print("    ① 大株主と不応募契約を締結")
        print("    ② 一般株主を対象とした他社株TOBを実施（マジョリティ取得）")
        print("    ③ ②の成立を条件とした自己株TOBを実施（大株主が応募）")
        print("    ④ 対象会社は上場維持")
        print("    ⑤ 直近5ヵ年（2021年〜2026年3月）")
    else:
        for t in EXACT_MATCH_TRANSACTIONS:
            _print_transaction(t)

    # 類似案件（参考）
    print_section("3. 参考：類似スキーム案件（条件の一部が異なるもの）")
    print("  以下は、スキームの一部が類似するものの、全条件を満たさない案件です。\n")

    for i, t in enumerate(SIMILAR_TRANSACTIONS, 1):
        print(f"  {'─'*68}")
        print(f"  【参考{i}】 {t.target_company}（{t.target_ticker}）── {t.year}年")
        print(f"  {'─'*68}")
        _print_transaction(t)

    # 分析・考察
    print_section("4. 分析・考察")
    print(ANALYSIS)

    # 条件別マトリクス
    print_section("5. 条件充足マトリクス")
    print(f"  {'案件名':<20} {'不応募':>6} {'他社株TOB':>9} {'自己株TOB':>9} "
          f"{'上場維持':>8} {'ﾏｼﾞｮﾘﾃｨ':>8} {'5年内':>5}")
    print(f"  {'─'*68}")

    all_transactions = EXACT_MATCH_TRANSACTIONS + SIMILAR_TRANSACTIONS
    for t in all_transactions:
        has_non_tender = "不応募" in t.notes or "不応募" in t.major_shareholder
        has_third_party_tob = t.tob_price and "N/A" not in t.tob_price
        has_self_tender = t.self_tender_price and "N/A" not in t.self_tender_price
        within_5y = 2021 <= t.year <= 2026

        print(f"  {t.target_company:<20} "
              f"{'○' if has_non_tender else '×':>4}   "
              f"{'○' if has_third_party_tob else '×':>6}    "
              f"{'○' if has_self_tender else '×':>6}    "
              f"{'○' if t.listing_maintained else '×':>5}    "
              f"{'○' if t.majority_acquired else '×':>5}  "
              f"{'○' if within_5y else '×':>3}")

    print(f"\n  ※ 全条件（○が6つ）を満たす案件は確認できず")

    # 補足
    print_section("6. 補足：2026年改正TOB規制の影響")
    print("""
  2026年5月1日施行の改正金融商品取引法により、以下の変更が予定されています:

  1. 「3分の1ルール」→「30%ルール」への引き下げ
     → TOB義務の閾値が低下し、TOB実施の必要性が増加

  2. 株券等所有割合50%超の者による買増し（2/3未満）の適用除外廃止
     → 親会社による上場子会社株式の買増しにもTOBが必要に

  3. 立会市場内買付けも規制対象に
     → 市場内での大量買付けにもTOB義務が発生

  これらの改正により、今後「上場維持＋マジョリティ取得」型のTOBや、
  自己株TOBとの組み合わせスキームが増加する可能性があります。
""")


def _print_transaction(t: TOBTransaction):
    """取引の詳細を出力"""
    print(f"    対象会社:     {t.target_company}（{t.target_ticker}）")
    print(f"    公開買付者:   {t.acquirer}")
    print(f"    大株主:       {t.major_shareholder}")
    print(f"    他社株TOB:    {t.tob_price}")
    print(f"    自己株TOB:    {t.self_tender_price}")
    print(f"    上場維持:     {'○' if t.listing_maintained else '× （上場廃止）'}")
    print(f"    ﾏｼﾞｮﾘﾃｨ取得: {'○' if t.majority_acquired else '×'}")
    print(f"    ステータス:   {t.status}")
    print(f"    取得後比率:   {t.acquirer_ownership_post}")
    print(f"    備考:")
    for line in t.notes.split("。"):
        if line.strip():
            print(f"      ・{line.strip()}。")
    print()


if __name__ == "__main__":
    main()
