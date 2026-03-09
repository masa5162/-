#!/usr/bin/env python3
"""
M&Aアドバイザリー 練習問題集 PDF生成スクリプト
=============================================

曽田香料（4965）のTOB事例をベースにした
M&Aアドバイザリー業務の練習問題と解答を生成します。
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ============================================================
# フォント設定
# ============================================================
FONT_PATH = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
FONT_PATH_P = "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"
pdfmetrics.registerFont(TTFont("IPAGothic", FONT_PATH))
pdfmetrics.registerFont(TTFont("IPAPGothic", FONT_PATH_P))

# ============================================================
# カラーパレット
# ============================================================
COLOR_PRIMARY = HexColor("#1a365d")
COLOR_SECONDARY = HexColor("#2c5282")
COLOR_ACCENT = HexColor("#e53e3e")
COLOR_LIGHT_BG = HexColor("#edf2f7")
COLOR_TABLE_HEADER = HexColor("#2d3748")
COLOR_TABLE_EVEN = HexColor("#f7fafc")
COLOR_BORDER = HexColor("#cbd5e0")

# ============================================================
# スタイル定義
# ============================================================
STYLES = {
    "title": ParagraphStyle(
        "Title", fontName="IPAGothic", fontSize=22, leading=30,
        textColor=COLOR_PRIMARY, alignment=TA_CENTER, spaceAfter=6*mm,
    ),
    "subtitle": ParagraphStyle(
        "Subtitle", fontName="IPAPGothic", fontSize=11, leading=16,
        textColor=COLOR_SECONDARY, alignment=TA_CENTER, spaceAfter=10*mm,
    ),
    "h1": ParagraphStyle(
        "H1", fontName="IPAGothic", fontSize=16, leading=22,
        textColor=COLOR_PRIMARY, spaceBefore=8*mm, spaceAfter=4*mm,
    ),
    "h2": ParagraphStyle(
        "H2", fontName="IPAGothic", fontSize=13, leading=18,
        textColor=COLOR_SECONDARY, spaceBefore=6*mm, spaceAfter=3*mm,
    ),
    "h3": ParagraphStyle(
        "H3", fontName="IPAGothic", fontSize=11, leading=16,
        textColor=COLOR_SECONDARY, spaceBefore=4*mm, spaceAfter=2*mm,
    ),
    "body": ParagraphStyle(
        "Body", fontName="IPAPGothic", fontSize=10, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=2*mm,
    ),
    "body_indent": ParagraphStyle(
        "BodyIndent", fontName="IPAPGothic", fontSize=10, leading=16,
        alignment=TA_JUSTIFY, leftIndent=8*mm, spaceAfter=2*mm,
    ),
    "question": ParagraphStyle(
        "Question", fontName="IPAGothic", fontSize=10.5, leading=16,
        textColor=COLOR_PRIMARY, leftIndent=6*mm, spaceAfter=2*mm,
    ),
    "answer": ParagraphStyle(
        "Answer", fontName="IPAPGothic", fontSize=10, leading=15,
        leftIndent=6*mm, spaceAfter=2*mm,
    ),
    "note": ParagraphStyle(
        "Note", fontName="IPAPGothic", fontSize=9, leading=14,
        textColor=HexColor("#718096"), leftIndent=6*mm, spaceAfter=2*mm,
    ),
    "table_header": ParagraphStyle(
        "TableHeader", fontName="IPAGothic", fontSize=9, leading=13,
        textColor=HexColor("#ffffff"), alignment=TA_CENTER,
    ),
    "table_cell": ParagraphStyle(
        "TableCell", fontName="IPAPGothic", fontSize=9, leading=13,
        alignment=TA_CENTER,
    ),
    "table_cell_left": ParagraphStyle(
        "TableCellLeft", fontName="IPAPGothic", fontSize=9, leading=13,
        alignment=TA_LEFT,
    ),
}


# ============================================================
# ヘルパー関数
# ============================================================

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER,
                       spaceAfter=3*mm, spaceBefore=3*mm)


def spacer(h=4):
    return Spacer(1, h * mm)


def make_table(headers, rows, col_widths=None):
    """テーブルを作成"""
    header_cells = [Paragraph(h, STYLES["table_header"]) for h in headers]
    data = [header_cells]
    for row in rows:
        data.append([
            Paragraph(str(c), STYLES["table_cell_left"] if i == 0 else STYLES["table_cell"])
            for i, c in enumerate(row)
        ])

    if col_widths is None:
        col_widths = [170 * mm / len(headers)] * len(headers)

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_TABLE_HEADER),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ])
    # 偶数行に背景色
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.add("BACKGROUND", (0, i), (-1, i), COLOR_TABLE_EVEN)

    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(style)
    return t


def question_block(num, text):
    return Paragraph(f"<b>問{num}.</b>　{text}", STYLES["question"])


def answer_block(text):
    return Paragraph(f"<b>【解答】</b>　{text}", STYLES["answer"])


def note_block(text):
    return Paragraph(f"※ {text}", STYLES["note"])


# ============================================================
# PDF コンテンツ構築
# ============================================================

def build_content():
    """全コンテンツを構築"""
    story = []

    # ------ 表紙 ------
    story.append(Spacer(1, 30 * mm))
    story.append(Paragraph("M&Aアドバイザリー", STYLES["title"]))
    story.append(Paragraph("実践問題集", ParagraphStyle(
        "Title2", fontName="IPAGothic", fontSize=28, leading=36,
        textColor=COLOR_PRIMARY, alignment=TA_CENTER, spaceAfter=8*mm,
    )))
    story.append(hr())
    story.append(Paragraph(
        "曽田香料（4965）TOB事例をベースにした<br/>"
        "企業価値算定・M&Aプロセスの練習問題",
        STYLES["subtitle"],
    ))
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph(
        "本問題集は、2017年に実施された曽田香料株式会社のTOB（株式公開買付け）事例を素材として、"
        "M&Aアドバイザリー業務に必要な企業価値算定やプロセスの知識を実践的に学ぶためのものです。",
        ParagraphStyle("Intro", fontName="IPAPGothic", fontSize=10, leading=16,
                       alignment=TA_CENTER, leftIndent=15*mm, rightIndent=15*mm),
    ))
    story.append(Spacer(1, 15 * mm))

    # 目次
    toc_items = [
        ("第1章", "ケーススタディ概要 — 曽田香料のTOB"),
        ("第2章", "企業価値算定の基礎問題"),
        ("第3章", "類似企業比較法（マルチプル法）"),
        ("第4章", "純資産法（修正簿価純資産法）"),
        ("第5章", "DCF法（ディスカウンテッド・キャッシュフロー法）"),
        ("第6章", "TOBプロセス・法規制"),
        ("第7章", "総合演習 — バリュエーション・レンジ分析"),
        ("付録", "解答一覧"),
    ]
    story.append(Paragraph("<b>目 次</b>", ParagraphStyle(
        "TOCTitle", fontName="IPAGothic", fontSize=14, leading=20,
        textColor=COLOR_PRIMARY, alignment=TA_CENTER, spaceAfter=6*mm,
    )))
    for ch, title in toc_items:
        story.append(Paragraph(
            f"<b>{ch}</b>　{title}",
            ParagraphStyle("TOCItem", fontName="IPAPGothic", fontSize=10.5,
                           leading=18, leftIndent=20*mm),
        ))
    story.append(PageBreak())

    # ==================== 第1章: ケーススタディ概要 ====================
    story.append(Paragraph("第1章　ケーススタディ概要", STYLES["h1"]))
    story.append(Paragraph("— 曽田香料株式会社（4965）のTOB —", STYLES["h3"]))
    story.append(hr())

    story.append(Paragraph("<b>1.1 会社概要</b>", STYLES["h2"]))
    company_info = [
        ("会社名", "曽田香料株式会社（Soda Aromatic Co., Ltd.）"),
        ("証券コード", "4965（2017年12月25日上場廃止）"),
        ("設立", "1915年（大正4年）"),
        ("本社", "大阪府大阪市"),
        ("事業内容", "フレグランス、フレーバー、合成香料、ファインケミカル等の製造販売"),
        ("親会社", "東レ（議決権66%）、三井物産（議決権34%）"),
    ]
    for label, value in company_info:
        story.append(Paragraph(f"<b>{label}:</b>　{value}", STYLES["body_indent"]))

    story.append(Paragraph("<b>1.2 財務データ（2017年3月期・連結）</b>", STYLES["h2"]))
    story.append(make_table(
        ["項目", "金額（百万円）", "備考"],
        [
            ("売上高", "15,250", ""),
            ("営業利益", "525", "営業利益率 3.4%"),
            ("経常利益", "424", ""),
            ("当期純利益", "243", ""),
            ("総資産", "22,146", ""),
            ("純資産", "17,397", ""),
            ("減価償却費", "700", "推定値"),
            ("発行済株式数", "10,586,000株", ""),
        ],
        col_widths=[50*mm, 40*mm, 80*mm],
    ))
    story.append(spacer(4))

    story.append(Paragraph("<b>1.3 TOBの概要</b>", STYLES["h2"]))
    tob_info = [
        ("買付者", "東レ株式会社・三井物産株式会社"),
        ("TOB価格", "1,140円/株"),
        ("TOB時BPS", "1,642.78円/株"),
        ("TOB時PBR", "0.69倍"),
        ("実施時期", "2017年8月〜9月"),
        ("上場廃止日", "2017年12月25日"),
        ("株式時価総額（TOB価格ベース）", "約12,068百万円（約121億円）"),
    ]
    for label, value in tob_info:
        story.append(Paragraph(f"<b>{label}:</b>　{value}", STYLES["body_indent"]))

    story.append(spacer(4))
    story.append(Paragraph(
        "本TOBは、既に親会社であった東レ・三井物産が残りの少数株主持分を取得し、"
        "完全子会社化を実現した事例です。TOB価格1,140円は当時のBPS 1,642.78円を下回っており"
        "（PBR 0.69倍）、少数株主にとっての価格の公正性が論点となりました。",
        STYLES["body"],
    ))

    story.append(Paragraph("<b>1.4 類似企業データ（参考）</b>", STYLES["h2"]))
    story.append(make_table(
        ["企業名", "PER", "PBR", "EV/EBITDA", "EV/Sales", "ROE"],
        [
            ("高砂香料工業（4914）", "13.5x", "1.04x", "8.75x", "0.65x", "9.2%"),
            ("長谷川香料（4958）", "16.4x", "1.04x", "10.0x", "1.48x", "5.6%"),
            ("2社平均", "14.95x", "1.04x", "9.38x", "1.07x", "7.4%"),
        ],
        col_widths=[42*mm, 22*mm, 22*mm, 26*mm, 26*mm, 22*mm],
    ))

    story.append(PageBreak())

    # ==================== 第2章: 企業価値算定の基礎 ====================
    story.append(Paragraph("第2章　企業価値算定の基礎問題", STYLES["h1"]))
    story.append(hr())

    story.append(question_block(1,
        "企業価値（Enterprise Value: EV）と株式価値（Equity Value）の違いを説明し、"
        "両者の関係式を示しなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(2,
        "M&Aにおける企業価値算定の主要3手法を挙げ、それぞれの概要と適用場面を説明しなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(3,
        "曽田香料の2017年3月期データを用いて、以下を計算しなさい。<br/>"
        "（a）EBITDA<br/>"
        "（b）営業利益率<br/>"
        "（c）ROE<br/>"
        "（d）1株当たり純資産（BPS）"
    ))
    story.append(spacer(2))

    story.append(question_block(4,
        "TOB（株式公開買付け）とは何か。通常のM&A（株式譲渡、事業譲渡等）との違いを説明し、"
        "TOBが選択される典型的な状況を3つ挙げなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(5,
        "曽田香料のTOB価格1,140円/株は、BPS 1,642.78円に対してPBR 0.69倍でした。"
        "このような簿価を下回るTOB価格が設定される理由を3つ説明しなさい。"
    ))

    story.append(PageBreak())

    # ==================== 第3章: 類似企業比較法 ====================
    story.append(Paragraph("第3章　類似企業比較法（マルチプル法）", STYLES["h1"]))
    story.append(hr())

    story.append(Paragraph(
        "類似企業比較法は、類似する上場企業の株式市場での評価（マルチプル）を参考に、"
        "対象企業の価値を算定する手法です。以下の問題に取り組んでください。",
        STYLES["body"],
    ))
    story.append(spacer(2))

    story.append(question_block(6,
        "類似企業を選定する際の基準を5つ挙げなさい。"
        "また、高砂香料工業と長谷川香料が曽田香料の類似企業として適切かどうか論じなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(7,
        "以下のデータを使って、PER法による曽田香料の株式価値を算定しなさい。<br/>"
        "・曽田香料の当期純利益: 243百万円<br/>"
        "・類似企業平均PER: 14.95倍<br/>"
        "算定結果を1株当たり価値に換算し、TOB価格1,140円と比較しなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(8,
        "以下のデータを使って、EV/EBITDA法による曽田香料の企業価値を算定しなさい。<br/>"
        "・曽田香料のEBITDA: 1,225百万円（営業利益525 + 減価償却費700）<br/>"
        "・類似企業平均EV/EBITDA: 9.38倍<br/>"
        "ネットデットを仮に0と仮定した場合の株式価値も算出しなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(9,
        "PER法とEV/EBITDA法で算定結果が異なる場合、その原因として考えられる要因を3つ挙げ、"
        "どちらの手法がより信頼性が高いか、状況に応じた判断基準を述べなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(10,
        "マルチプル法には「トレーディング・マルチプル」と「トランザクション・マルチプル」の"
        "2種類があります。それぞれの定義・特徴・適用場面を比較し、曽田香料の評価において"
        "どちらが適切か理由とともに述べなさい。"
    ))

    story.append(PageBreak())

    # ==================== 第4章: 純資産法 ====================
    story.append(Paragraph("第4章　純資産法（修正簿価純資産法）", STYLES["h1"]))
    story.append(hr())

    story.append(question_block(11,
        "簿価純資産法と修正簿価純資産法の違いを説明しなさい。"
        "また、修正簿価純資産法で調整が必要な項目を5つ具体的に挙げなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(12,
        "曽田香料の2017年3月期の純資産17,397百万円を用いて、簿価純資産法による"
        "株式価値と1株当たり価値を算定しなさい。TOB価格1,140円との乖離を説明しなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(13,
        "純資産法が主に適用される企業の特徴を3つ挙げなさい。"
        "曽田香料のような製造業に純資産法を適用する場合の留意点を述べなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(14,
        "仮に曽田香料が以下の含み損益を有していた場合、修正純資産を計算しなさい。<br/>"
        "・不動産含み益: +2,000百万円<br/>"
        "・有価証券含み益: +500百万円<br/>"
        "・退職給付債務の簿外債務: △800百万円<br/>"
        "・繰延税金負債の追加計上: △510百万円<br/>"
        "修正後の1株当たり価値はいくらになるか。"
    ))

    story.append(PageBreak())

    # ==================== 第5章: DCF法 ====================
    story.append(Paragraph("第5章　DCF法", STYLES["h1"]))
    story.append(Paragraph("（ディスカウンテッド・キャッシュフロー法）", STYLES["h3"]))
    story.append(hr())

    story.append(question_block(15,
        "DCF法の基本的な考え方を説明し、算定の手順を5つのステップに分けて述べなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(16,
        "フリー・キャッシュフロー（FCF）の計算式を示し、各構成要素を説明しなさい。"
        "曽田香料の以下の前提条件でYear 1のFCFを計算しなさい。<br/>"
        "・売上高: 17,913百万円（17,562 × 1.02）<br/>"
        "・営業利益率: 4.0%<br/>"
        "・実効税率: 30%<br/>"
        "・設備投資/売上高: 3.0%<br/>"
        "・減価償却/売上高: 4.0%"
    ))
    story.append(spacer(2))

    story.append(question_block(17,
        "WACC（加重平均資本コスト）の計算式を示し、各構成要素を説明しなさい。"
        "曽田香料のような非上場企業のWACCを推定する際の課題と対処法を述べなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(18,
        "ターミナルバリュー（TV）とは何か説明し、永久成長モデルの計算式を示しなさい。"
        "以下の条件でTVを計算しなさい。<br/>"
        "・Year 5のFCF: 約720百万円<br/>"
        "・永久成長率: 1.0%<br/>"
        "・WACC: 7.0%<br/>"
        "TVが企業価値全体に占める割合が高くなる傾向について、その問題点と対処法を述べなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(19,
        "DCF法の感度分析を行います。以下の3ケースについてそれぞれ企業価値を算定し、"
        "結果を比較しなさい。<br/>"
        "【ベースケース】売上成長率2%、営業利益率4%、WACC 7%<br/>"
        "【楽観ケース】売上成長率3%、営業利益率5%、WACC 6%<br/>"
        "【悲観ケース】売上成長率1%、営業利益率3%、WACC 8%"
    ))

    story.append(PageBreak())

    # ==================== 第6章: TOBプロセス・法規制 ====================
    story.append(Paragraph("第6章　TOBプロセス・法規制", STYLES["h1"]))
    story.append(hr())

    story.append(question_block(20,
        "日本のTOB（公開買付け）制度の法的根拠を示し、TOBが義務化される条件を3つ挙げなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(21,
        "TOBにおける「公正な価格」の算定方法について、金融庁のガイドラインや"
        "裁判例を踏まえて説明しなさい。曽田香料のTOB価格がPBR 0.69倍であったことの"
        "法的リスクについても検討しなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(22,
        "MBO（マネジメント・バイアウト）とTOBの違いを説明しなさい。"
        "曽田香料のケースはMBOではなく親会社によるTOBですが、"
        "利益相反の観点からどのような問題が生じうるか論じなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(23,
        "TOBにおける「特別委員会」の役割と構成要件を説明しなさい。"
        "曽田香料のケースで特別委員会が検討すべき事項を3つ挙げなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(24,
        "スクイーズアウト（少数株主の強制排除）の手続きを説明しなさい。"
        "2017年当時と現行の会社法における手続きの違いがあれば指摘しなさい。"
    ))

    story.append(PageBreak())

    # ==================== 第7章: 総合演習 ====================
    story.append(Paragraph("第7章　総合演習", STYLES["h1"]))
    story.append(Paragraph("— バリュエーション・レンジ分析 —", STYLES["h3"]))
    story.append(hr())

    story.append(Paragraph(
        "以下は各算定手法による曽田香料の企業価値/株式価値の一覧です（2024年3月期推定ベース）。"
        "これを用いて総合的な分析を行ってください。",
        STYLES["body"],
    ))
    story.append(spacer(2))

    story.append(make_table(
        ["算定手法", "企業/株式価値\n（百万円）", "概算（億円）"],
        [
            ("PER法", "6,279", "63"),
            ("PBR法", "20,280", "203"),
            ("EV/EBITDA法", "14,063", "141"),
            ("EV/Sales法", "18,741", "187"),
            ("純資産法", "19,500", "195"),
            ("DCF法（ベース）", "15,236", "152"),
            ("DCF法（楽観）", "23,840", "238"),
            ("DCF法（悲観）", "9,498", "95"),
        ],
        col_widths=[55*mm, 55*mm, 40*mm],
    ))
    story.append(spacer(4))

    story.append(question_block(25,
        "上記の各手法による算定結果のばらつきの原因を分析し、"
        "どの手法の結果を重視すべきか、理由とともにランキング形式で述べなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(26,
        "あなたが曽田香料の少数株主側のファイナンシャル・アドバイザーだとした場合、"
        "TOB価格について買付者側にどのような主張を行うか。具体的な算定根拠と"
        "交渉戦略を述べなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(27,
        "あなたが買付者（東レ・三井物産）側のファイナンシャル・アドバイザーだとした場合、"
        "TOB価格1,140円の妥当性をどのように説明するか。防御的な論拠を3つ以上挙げなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(28,
        "バリュエーション・レンジに基づき、あなたが考える「公正な買付価格」のレンジを"
        "提示しなさい。レンジの上限・下限の設定根拠を明示すること。"
    ))
    story.append(spacer(2))

    story.append(question_block(29,
        "曽田香料が上場廃止後、2024年3月期に売上高17,562百万円を達成しています。"
        "TOB後の企業成長を踏まえ、2017年のTOB価格が少数株主にとって適正であったか"
        "事後的に評価しなさい。"
    ))
    story.append(spacer(2))

    story.append(question_block(30,
        "曽田香料のケースから得られるM&Aアドバイザリーとしての教訓を5つ挙げ、"
        "それぞれについて具体的に説明しなさい。"
    ))

    story.append(PageBreak())

    # ==================== 付録: 解答一覧 ====================
    story.append(Paragraph("付録　解答一覧", STYLES["h1"]))
    story.append(hr())

    answers = [
        # 問1
        (1, "企業価値（EV）は事業全体の価値を表し、株式価値（Equity Value）は株主に帰属する価値を表す。"
            "関係式: EV = 株式価値 + 有利子負債 − 現金及び現金同等物（ネットデット）。"
            "つまり「EV = Equity Value + Net Debt」。EVは資本構成に依存しない事業の本源的価値であり、"
            "株式価値はEVからデットホルダーへの返済分を差し引いた残余価値である。"),
        # 問2
        (2, "①インカム・アプローチ（DCF法等）: 将来のキャッシュフローを現在価値に割り引く。"
            "継続企業を前提とした本源的価値の算定に適する。"
            "②マーケット・アプローチ（類似企業比較法等）: 市場の取引価格を参照。客観性が高く、"
            "市場での相対的な位置づけを把握するのに適する。"
            "③コスト・アプローチ（純資産法等）: 資産の再調達原価や清算価値に着目。"
            "資産保有型企業や清算局面に適する。"),
        # 問3
        (3, "（a）EBITDA = 営業利益525 + 減価償却費700 = 1,225百万円<br/>"
            "（b）営業利益率 = 525 / 15,250 = 3.44%<br/>"
            "（c）ROE = 243 / 17,397 = 1.40%<br/>"
            "（d）BPS = 17,397百万円 × 1,000,000 / 10,586,000株 = 1,643円/株"),
        # 問4
        (4, "TOBは不特定多数の株主から市場外で株式を買い集める公開買付けのこと。"
            "金融商品取引法に基づく手続き・開示が必要。"
            "典型的な状況: ①上場子会社の完全子会社化、②敵対的買収、③MBO。"),
        # 問5
        (5, "①市場株価がBPSを下回っていた（低PBR状態）ため、市場価格にプレミアムを付しても"
            "BPS以下となった。②純資産の大部分が事業用資産であり、清算価値としての意味が薄い。"
            "③非上場化後の支配権プレミアムと少数株主ディスカウントの関係。"),
        # 問6
        (6, "基準: ①業種・事業内容の類似性、②企業規模（売上高・時価総額）、"
            "③収益性（利益率・ROE）、④成長性、⑤資本構成。"
            "高砂香料・長谷川香料はいずれも香料メーカーで事業内容は近い。"
            "ただし規模は高砂が大幅に大きく、長谷川も曽田より大きいため、"
            "サイズ・ディスカウントの考慮が必要。"),
        # 問7
        (7, "株式価値 = 243百万円 × 14.95 = 3,633百万円<br/>"
            "1株当たり = 3,633百万円 × 1,000,000 / 10,586,000株 = 343円/株<br/>"
            "TOB価格1,140円と比較すると、PER法による値は大幅に低い。"
            "これは曽田香料の利益水準が類似企業対比で低いことを示唆する。"),
        # 問8
        (8, "EV = 1,225百万円 × 9.38 = 11,490百万円<br/>"
            "ネットデット=0とすると株式価値 = 11,490百万円<br/>"
            "1株当たり = 11,490百万円 × 1,000,000 / 10,586,000株 = 1,085円/株<br/>"
            "TOB価格1,140円に近い水準となり、EV/EBITDA法がTOB価格算定の参考になった可能性がある。"),
        # 問9
        (9, "要因: ①資本構成の違い（PERは純利益ベース、EV/EBITDAは営業ベース）、"
            "②特別損益の影響（PERに影響するがEBITDAには影響しない）、"
            "③減価償却方針の違い。"
            "一般にEV/EBITDAは資本構成・税制の影響を受けにくく、"
            "クロスボーダーや資本構成が異なる企業間の比較に適する。"),
        # 問10
        (10, "トレーディング・マルチプル: 上場企業の現在の市場株価をベースとしたマルチプル。"
             "常時観測可能で客観性が高い。"
             "トランザクション・マルチプル: 過去のM&A取引価格をベースとしたマルチプル。"
             "支配権プレミアムが含まれるため、TOBの価格算定に適する。"
             "曽田香料のケースではTOB（支配権取得）のため、"
             "トランザクション・マルチプルがより適切。"),
        # 問11
        (11, "簿価純資産法: 貸借対照表の純資産をそのまま使用。"
             "修正簿価純資産法: 資産・負債を時価で再評価した上で純資産を算定。"
             "調整項目: ①不動産（時価評価）、②有価証券（時価評価）、③退職給付債務（実際の債務）、"
             "④繰延税金資産/負債の見直し、⑤のれん・無形資産の再評価。"),
        # 問12
        (12, "株式価値 = 17,397百万円<br/>"
             "1株当たり = 17,397百万円 × 1,000,000 / 10,586,000株 = 1,643円/株<br/>"
             "TOB価格1,140円との乖離: △503円（△30.6%）<br/>"
             "簿価純資産はBPSそのものであり、TOB価格がこれを下回ることは"
             "「解散価値以下での買収」と批判されうる。"),
        # 問13
        (13, "適用される企業: ①不動産保有企業、②投資会社・持株会社、③清算予定の企業。"
             "製造業への適用では、事業用資産の帳簿価額と時価の乖離、"
             "のれんや技術等の無形資産が反映されない点、"
             "収益力が反映されない点に留意が必要。"),
        # 問14
        (14, "修正純資産 = 17,397 + 2,000 + 500 − 800 − 510 = 18,587百万円<br/>"
             "1株当たり = 18,587百万円 × 1,000,000 / 10,586,000株 = 1,756円/株<br/>"
             "簿価BPS 1,643円から約7%増加。TOB価格1,140円との乖離はさらに拡大する。"),
        # 問15
        (15, "DCF法は将来のフリー・キャッシュフローを現在価値に割り引いて企業価値を算定する手法。"
             "手順: ①事業計画に基づくFCFの予測、②割引率（WACC）の算定、"
             "③予測期間のFCFの現在価値合計、④ターミナルバリューの算定と現在価値化、"
             "⑤事業価値（FCF現在価値合計＋TV現在価値）の算出。"),
        # 問16
        (16, "FCF = NOPAT + 減価償却費 − 設備投資 − 運転資本増加額<br/>"
             "Year 1: 売上高17,913、営業利益 = 17,913 × 4% = 717、"
             "NOPAT = 717 × 0.7 = 502、減価償却 = 17,913 × 4% = 717、"
             "設備投資 = 17,913 × 3% = 537<br/>"
             "FCF = 502 + 717 − 537 = 681百万円"),
        # 問17
        (17, "WACC = E/(D+E) × Re + D/(D+E) × Rd × (1−T)<br/>"
             "Re: 株主資本コスト（CAPM: Rf + β × MRP）、Rd: 負債コスト、T: 実効税率。"
             "非上場企業の課題: ①βが直接観測できない→類似上場企業のβをアンレバー→リレバー、"
             "②サイズプレミアムの加算が必要、③流動性ディスカウントの考慮。"),
        # 問18
        (18, "TV = FCF(n+1) / (WACC − g) = 720 × 1.01 / (0.07 − 0.01) = 727.2 / 0.06 = 12,120百万円<br/>"
             "TVが全体の70-80%を占めることが多く、前提条件への感応度が非常に高い。"
             "対処法: ①永久成長率の保守的な設定、②EV/EBITDAマルチプルによるクロスチェック、"
             "③感度分析の実施。"),
        # 問19
        (19, "ベースケース: 約15,236百万円（約152億円）<br/>"
             "楽観ケース: 約23,840百万円（約238億円）<br/>"
             "悲観ケース: 約9,498百万円（約95億円）<br/>"
             "レンジは約95〜238億円と広く、前提条件の僅かな違いが大きな差を生む。"
             "これがDCF法の限界であり、複数手法によるクロスチェックが重要。"),
        # 問20
        (20, "法的根拠: 金融商品取引法第27条の2以下。"
             "義務化条件: ①市場外で株券等を5%超取得する場合、"
             "②60日間で10名超から市場外で取得し保有割合が1/3超となる場合、"
             "③市場内外の取引で1/3超を超える場合（急速な買付け）。"),
        # 問21
        (21, "経産省「公正なM&Aの在り方に関する指針」（2019年）が重要な参考文献。"
             "公正な価格は①独立当事者間取引としての手続きの公正性、"
             "②合理的な算定手法による価格の相当性で判断される。"
             "PBR 0.69倍は簿価割れであり、株主から価格決定申立て（会社法172条）の"
             "リスクがあるが、市場株価にプレミアムが付されていれば認容される傾向にある。"),
        # 問22
        (22, "MBOは経営陣が自ら買収者となるもの。利益相反が構造的に内在する。"
             "本件は親会社によるTOBだが、親会社取締役が子会社取締役を兼務する場合等、"
             "利益相反が生じる。対処: 特別委員会の設置、独立したFA・法律事務所の起用、"
             "マジョリティ・オブ・マイノリティ条件の設定。"),
        # 問23
        (23, "特別委員会は独立社外取締役等で構成し、TOBの条件の公正性を審議する。"
             "検討事項: ①TOB価格の妥当性（独立した第三者算定機関の評価との整合性）、"
             "②TOBに賛同する取締役会決議の適切性、"
             "③少数株主の利益が適切に保護されているか。"),
        # 問24
        (24, "スクイーズアウトの主な手法: ①株式等売渡請求（会社法179条〜）、"
             "②株式併合。2017年当時は全部取得条項付種類株式を用いる方法も一般的であった。"
             "2019年会社法改正により株式交付制度が創設され、組織再編の選択肢が拡大した。"),
        # 問25
        (25, "ばらつきの原因: 各手法が異なる価値の側面を捉えている。PER法は利益水準が低いため過小評価、"
             "PBR法・純資産法は資産ベースで高評価、DCF法は前提条件次第で大きく変動。"
             "重視すべき順: ①DCF法（本源的価値）、②EV/EBITDA法（市場整合性）、"
             "③純資産法（フロア価格）、④PER法（利益の正常化が必要）。"),
        # 問26
        (26, "少数株主側FAとして: DCF楽観ケース（238億円）と修正純資産法の結果を根拠に、"
             "TOB価格の引き上げを主張。具体的にはBPS以上（1,643円〜1,756円/株）を要求。"
             "マジョリティ・オブ・マイノリティ条件の設定、独立した株式価値算定書の取得、"
             "交渉が決裂した場合の価格決定申立ての可能性を示唆することで交渉力を確保。"),
        # 問27
        (27, "買付者側の論拠: ①市場株価に対する十分なプレミアム（市場株価が低PBR）、"
             "②PER法に基づく株式価値は343円/株であり1,140円は大幅に上回る、"
             "③EV/EBITDA法では1,085円/株でありTOB価格はこれを上回る、"
             "④非公開化による流動性喪失を考慮してもプレミアムが存在。"),
        # 問28
        (28, "公正な買付価格レンジ: 1,100〜1,800円/株。"
             "下限根拠: EV/EBITDA法による1,085円に約1%のプレミアムを付加。"
             "上限根拠: 修正BPS約1,756円に少数株主プレミアムを考慮。"
             "中央値: 約1,450円/株が妥当な水準と考えられる。"),
        # 問29
        (29, "2024年3月期売上高17,562百万円は2017年の15,250百万円から約15%成長。"
             "年平均成長率約2%。非公開化によりM&A・事業再編の柔軟性が向上した可能性がある。"
             "事後的に見れば、TOB価格は成長ポテンシャルを十分に反映しておらず、"
             "少数株主にとって有利とは言い難い。"),
        # 問30
        (30, "教訓: ①複数の算定手法を用いたクロスチェックの重要性、"
             "②支配株主によるTOBでは利益相反への対処が不可欠、"
             "③簿価割れTOBでは少数株主保護が特に重要、"
             "④将来の成長性をバリュエーションに適切に織り込む必要性、"
             "⑤独立した特別委員会と第三者算定機関の役割の重要性。"),
    ]

    for num, text in answers:
        story.append(KeepTogether([
            Paragraph(f"<b>問{num}の解答</b>", STYLES["h3"]),
            answer_block(text),
            spacer(2),
        ]))

    # フッター情報
    story.append(PageBreak())
    story.append(Paragraph("免責事項", STYLES["h2"]))
    story.append(Paragraph(
        "本問題集は教育目的で作成されたものであり、投資助言や専門的なアドバイスを構成するものではありません。"
        "実際のM&Aアドバイザリー業務においては、公認会計士・弁護士等の専門家の助言を得てください。"
        "使用しているデータには推定値が含まれており、正確性を保証するものではありません。",
        STYLES["body"],
    ))
    story.append(spacer(4))
    story.append(Paragraph(
        "データソース: 曽田香料 最終有価証券報告書（2017年3月期）、マイナビ2026 曽田香料会社概要、"
        "高砂香料工業・長谷川香料 各種IR資料",
        STYLES["note"],
    ))

    return story


# ============================================================
# PDF生成
# ============================================================

def generate_pdf(output_path="ma_advisory_problems.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=20*mm,
        bottomMargin=20*mm,
        leftMargin=20*mm,
        rightMargin=20*mm,
        title="M&Aアドバイザリー 実践問題集",
        author="Valuation Analysis",
    )

    story = build_content()
    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    generate_pdf()
