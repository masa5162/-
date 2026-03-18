#!/usr/bin/env python3
"""Generate a beginner-friendly PDF guide on biomethane business, KVI, and Mitsubishi Corp."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon
from reportlab.graphics import renderPDF

# Register CJK font
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
pdfmetrics.registerFont(TTFont('CJK', FONT_PATH, subfontIndex=0))

# Colors
DARK_GREEN = HexColor('#1a5c3a')
MID_GREEN = HexColor('#2d8a5f')
LIGHT_GREEN = HexColor('#e8f8f0')
ACCENT_GREEN = HexColor('#27ae60')
DARK_BLUE = HexColor('#1a3a5c')
MID_BLUE = HexColor('#2c5f8a')
LIGHT_BLUE = HexColor('#e8f0f8')
ACCENT_ORANGE = HexColor('#e67e22')
ACCENT_RED = HexColor('#c0392b')
LIGHT_GRAY = HexColor('#f5f5f5')
BORDER_GRAY = HexColor('#cccccc')
DARK_GRAY = HexColor('#333333')
MID_GRAY = HexColor('#666666')
TABLE_HEADER_BG = HexColor('#2d8a5f')
TABLE_ALT_ROW = HexColor('#f0f8f4')
BOX_BG = HexColor('#f0f8f4')
WARN_BG = HexColor('#fff8e8')
WARN_BORDER = HexColor('#f39c12')

# Page setup
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

doc = SimpleDocTemplate(
    '/home/user/-/biomethane_guide.pdf',
    pagesize=A4,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=MARGIN,
    bottomMargin=18 * mm,
)

avail = PAGE_W - 2 * MARGIN

# Styles
s_title = ParagraphStyle('Title', fontName='CJK', fontSize=24, leading=32,
                         textColor=DARK_GREEN, alignment=TA_CENTER, spaceAfter=6*mm)
s_subtitle = ParagraphStyle('Subtitle', fontName='CJK', fontSize=12, leading=18,
                            textColor=MID_GREEN, alignment=TA_CENTER, spaceAfter=3*mm)
s_cover_sub = ParagraphStyle('CoverSub', fontName='CJK', fontSize=10, leading=14,
                              textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=2*mm)
s_h1 = ParagraphStyle('H1', fontName='CJK', fontSize=18, leading=24,
                       textColor=DARK_GREEN, spaceBefore=6*mm, spaceAfter=4*mm)
s_h2 = ParagraphStyle('H2', fontName='CJK', fontSize=14, leading=20,
                       textColor=MID_GREEN, spaceBefore=5*mm, spaceAfter=3*mm)
s_h3 = ParagraphStyle('H3', fontName='CJK', fontSize=11, leading=16,
                       textColor=DARK_GREEN, spaceBefore=4*mm, spaceAfter=2*mm)
s_body = ParagraphStyle('Body', fontName='CJK', fontSize=9.5, leading=15,
                         spaceAfter=2.5*mm)
s_body_large = ParagraphStyle('BodyLarge', fontName='CJK', fontSize=10.5, leading=16,
                               spaceAfter=3*mm)
s_bullet = ParagraphStyle('Bullet', fontName='CJK', fontSize=9.5, leading=15,
                           leftIndent=14, spaceAfter=1.5*mm, bulletIndent=0)
s_bullet2 = ParagraphStyle('Bullet2', fontName='CJK', fontSize=9, leading=14,
                            leftIndent=28, spaceAfter=1*mm, bulletIndent=14)
s_small = ParagraphStyle('Small', fontName='CJK', fontSize=8, leading=11,
                          textColor=MID_GRAY)
s_th = ParagraphStyle('TH', fontName='CJK', fontSize=8.5, leading=12,
                       textColor=white, alignment=TA_LEFT)
s_tc = ParagraphStyle('TC', fontName='CJK', fontSize=8.5, leading=12)
s_tc_center = ParagraphStyle('TCC', fontName='CJK', fontSize=8.5, leading=12, alignment=TA_CENTER)
s_tc_bold = ParagraphStyle('TCB', fontName='CJK', fontSize=8.5, leading=12)
s_box_title = ParagraphStyle('BoxTitle', fontName='CJK', fontSize=10, leading=14,
                              textColor=DARK_GREEN, spaceAfter=1.5*mm)
s_box_body = ParagraphStyle('BoxBody', fontName='CJK', fontSize=9, leading=14)
s_caption = ParagraphStyle('Caption', fontName='CJK', fontSize=8, leading=11,
                            textColor=MID_GRAY, alignment=TA_CENTER, spaceBefore=1*mm, spaceAfter=3*mm)
s_num_large = ParagraphStyle('NumLarge', fontName='CJK', fontSize=22, leading=28,
                              textColor=ACCENT_GREEN, alignment=TA_CENTER)
s_num_label = ParagraphStyle('NumLabel', fontName='CJK', fontSize=8, leading=11,
                              textColor=DARK_GRAY, alignment=TA_CENTER)
s_quote = ParagraphStyle('Quote', fontName='CJK', fontSize=10, leading=15,
                          textColor=DARK_GREEN, leftIndent=10, rightIndent=10,
                          borderPadding=5, spaceBefore=2*mm, spaceAfter=2*mm)

def make_table(headers, rows, col_widths=None, header_bg=TABLE_HEADER_BG):
    if col_widths is None:
        n = len(headers)
        col_widths = [avail / n] * n
    data = [[Paragraph(h, s_th) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), s_tc) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), header_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'CJK'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT_ROW))
    t.setStyle(TableStyle(style_cmds))
    return t


def info_box(title, body_text, bg=BOX_BG, border=ACCENT_GREEN):
    """Create a colored info box."""
    inner = []
    if title:
        inner.append(Paragraph(title, s_box_title))
    inner.append(Paragraph(body_text, s_box_body))
    inner_table = Table([[inner]], colWidths=[avail - 12])
    inner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX', (0, 0), (-1, -1), 1.5, border),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return inner_table


def stat_boxes(stats):
    """Create a row of statistic boxes. stats = [(number, label), ...]"""
    cells = []
    for num, label in stats:
        cell_content = [
            Paragraph(str(num), s_num_large),
            Paragraph(label, s_num_label),
        ]
        cells.append(cell_content)
    n = len(cells)
    w = avail / n
    t = Table([cells], colWidths=[w] * n)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GREEN),
        ('BOX', (0, 0), (-1, -1), 1, ACCENT_GREEN),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, ACCENT_GREEN),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def flow_diagram(steps, arrow_color=ACCENT_GREEN):
    """Create a simple horizontal flow diagram using a table."""
    cells = []
    for i, step in enumerate(steps):
        cells.append(Paragraph(step, ParagraphStyle('FlowCell', fontName='CJK', fontSize=8,
                                                     leading=11, alignment=TA_CENTER, textColor=white)))
        if i < len(steps) - 1:
            cells.append(Paragraph('>>>', ParagraphStyle('Arrow', fontName='CJK', fontSize=12,
                                                          leading=14, alignment=TA_CENTER, textColor=arrow_color)))
    n = len(cells)
    widths = []
    step_w = avail * 0.17
    arrow_w = avail * 0.06
    for i in range(n):
        widths.append(step_w if i % 2 == 0 else arrow_w)
    t = Table([cells], colWidths=widths)
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'CJK'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(0, n, 2):
        style_cmds.append(('BACKGROUND', (i, 0), (i, 0), MID_GREEN))
        style_cmds.append(('ROUNDEDCORNERS', [4, 4, 4, 4]))
    t.setStyle(TableStyle(style_cmds))
    return t


def vertical_flow(steps, colors=None):
    """Create a vertical flow diagram."""
    if colors is None:
        colors = [MID_GREEN] * len(steps)
    rows = []
    for i, (step, desc) in enumerate(steps):
        step_p = Paragraph(step, ParagraphStyle('VFStep', fontName='CJK', fontSize=9,
                                                 leading=13, textColor=white, alignment=TA_CENTER))
        desc_p = Paragraph(desc, ParagraphStyle('VFDesc', fontName='CJK', fontSize=8.5,
                                                 leading=12))
        rows.append([step_p, desc_p])
        if i < len(steps) - 1:
            arrow_p = Paragraph('▼', ParagraphStyle('VFArrow', fontName='CJK', fontSize=14,
                                                      leading=16, alignment=TA_CENTER, textColor=colors[min(i+1, len(colors)-1)]))
            rows.append([arrow_p, ''])

    w1 = avail * 0.25
    w2 = avail * 0.75
    t = Table(rows, colWidths=[w1, w2])
    style_cmds = [
        ('FONTNAME', (0, 0), (-1, -1), 'CJK'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (1, 0), (1, -1), 10),
    ]
    row_idx = 0
    for i in range(len(steps)):
        style_cmds.append(('BACKGROUND', (0, row_idx), (0, row_idx), colors[min(i, len(colors)-1)]))
        row_idx += 2
    t.setStyle(TableStyle(style_cmds))
    return t


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER_GRAY, spaceAfter=3*mm, spaceBefore=2*mm)


def section_header_bar(text, bg=DARK_GREEN):
    """Full-width section header bar."""
    p = Paragraph(text, ParagraphStyle('SectionBar', fontName='CJK', fontSize=14,
                                        leading=20, textColor=white, alignment=TA_LEFT))
    t = Table([[p]], colWidths=[avail])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


def comparison_table(title_left, title_right, items_left, items_right, color_left=MID_GREEN, color_right=MID_BLUE):
    """Side-by-side comparison."""
    header = [
        Paragraph(title_left, ParagraphStyle('CL', fontName='CJK', fontSize=10, leading=14, textColor=white, alignment=TA_CENTER)),
        Paragraph(title_right, ParagraphStyle('CR', fontName='CJK', fontSize=10, leading=14, textColor=white, alignment=TA_CENTER)),
    ]
    max_len = max(len(items_left), len(items_right))
    rows = [header]
    for i in range(max_len):
        l = Paragraph(items_left[i] if i < len(items_left) else '', s_tc)
        r = Paragraph(items_right[i] if i < len(items_right) else '', s_tc)
        rows.append([l, r])
    t = Table(rows, colWidths=[avail * 0.5, avail * 0.5])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), color_left),
        ('BACKGROUND', (1, 0), (1, 0), color_right),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


def build():
    story = []

    # =========================================
    # COVER PAGE
    # =========================================
    story.append(Spacer(1, 35*mm))
    story.append(Paragraph('欧州バイオメタンガス事業', s_title))
    story.append(Paragraph('入門ガイド', ParagraphStyle('TitleSub', fontName='CJK', fontSize=20, leading=28,
                                                        textColor=ACCENT_GREEN, alignment=TA_CENTER, spaceAfter=8*mm)))
    story.append(HRFlowable(width="50%", thickness=2, color=DARK_GREEN, spaceAfter=8*mm))
    story.append(Paragraph(
        '三菱商事のエネルギー事業 × カナデビア（KVI）の欧州展開<br/>'
        'M&Aの特徴と商社にとっての魅力を徹底解説',
        s_subtitle))
    story.append(Spacer(1, 20*mm))

    cover_data = [
        ['作成日', '2026年3月18日'],
        ['対象読者', 'バイオメタン事業に初めて触れる方'],
        ['想定用途', '社内検討・勉強会資料'],
    ]
    cover_table = Table(
        [[Paragraph(r[0], s_tc_bold), Paragraph(r[1], s_tc)] for r in cover_data],
        colWidths=[avail*0.25, avail*0.45]
    )
    cover_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'CJK'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER_GRAY),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # =========================================
    # TABLE OF CONTENTS
    # =========================================
    story.append(Paragraph('目次', s_h1))
    story.append(hr())
    toc_items = [
        ('第1章', 'そもそもバイオメタンガスとは？', '生ゴミが都市ガスに変わる仕組み'),
        ('第2章', '三菱商事のエネルギー事業', '何をやっている会社なのか'),
        ('第3章', 'カナデビア（KVI）とは何者か？', '旧日立造船の欧州グリーンテック事業'),
        ('第4章', 'KVIの欧州バイオメタン事業の特徴', '17か所のプラント群と成長戦略'),
        ('第5章', '三菱商事はなぜ興味を持つのか？', '商社にとっての投資妙味'),
        ('第6章', 'バイオメタンM&Aの特徴', '他のM&Aとここが違う'),
        ('第7章', 'まとめ', '全体像の整理'),
    ]
    for num, title, desc in toc_items:
        row = Table(
            [[Paragraph(num, ParagraphStyle('TOCNum', fontName='CJK', fontSize=10, leading=14, textColor=ACCENT_GREEN)),
              Paragraph(f'{title}<br/><font size=8 color="#666666">{desc}</font>',
                       ParagraphStyle('TOCTitle', fontName='CJK', fontSize=10, leading=14))]],
            colWidths=[avail*0.12, avail*0.88]
        )
        row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, HexColor('#e0e0e0')),
        ]))
        story.append(row)

    story.append(PageBreak())

    # =========================================
    # CHAPTER 1: What is Biomethane?
    # =========================================
    story.append(section_header_bar('第1章　そもそもバイオメタンガスとは？'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('1.1 一言でいうと', s_h2))
    story.append(info_box(
        '「バイオメタン」＝ 生ゴミや農業廃棄物から作る「再生可能な天然ガス」',
        '家庭やレストランの生ゴミ、牛糞や豚糞、食品工場の残りカスなどを微生物に分解させると、ガスが出ます。<br/>'
        'このガスを精製すると、都市ガスや天然ガスとほぼ同じ成分になります。<br/>'
        'これが「バイオメタン」です。既存のガスパイプラインにそのまま注入できるのが最大の特徴です。'
    ))

    story.append(Paragraph('1.2 製造の仕組み（4ステップ）', s_h2))

    story.append(vertical_flow([
        ('Step 1\n原料の収集', '農業廃棄物（牛糞・豚糞・作物残渣）、食品廃棄物（生ゴミ・食品工場残渣）、'
         '下水汚泥などを集めます。ゴミ処理業者や農家がプラントに原料を持ち込み、'
         '受入手数料（ゲートフィー）を支払います。つまり、原料をもらうのにお金がもらえる。'),
        ('Step 2\n嫌気性発酵', '巨大なタンク（消化槽）の中に原料を入れ、酸素を遮断します。'
         '微生物が有機物を分解し、メタン（約60%）とCO2（約40%）の混合ガス＝「バイオガス」を生成します。'
         '発酵期間は約20～40日。温度は35～55℃に維持。'),
        ('Step 3\nガスの精製', 'バイオガスからCO2、硫化水素、水分を除去し、メタン濃度を97%以上に高めます。'
         'これで「バイオメタン」の完成です。品質は天然ガスとほぼ同じ。'),
        ('Step 4\nガスグリッド注入', '精製したバイオメタンを、既存の天然ガスパイプライン（ガスグリッド）に注入します。'
         '家庭の暖房や工場のボイラーの燃料として使われます。'),
    ], colors=[HexColor('#8e44ad'), HexColor('#2980b9'), ACCENT_GREEN, HexColor('#e67e22')]))
    story.append(s_caption and Paragraph('図1：バイオメタン製造の4ステップ', s_caption))

    story.append(Paragraph('1.3 なぜ「すごい」のか？', s_h2))

    story.append(make_table(
        ['特徴', '解説', '比較対象'],
        [
            ['カーボンニュートラル', '植物由来の炭素を循環させるだけ。化石燃料のように新たなCO2を排出しない', '天然ガス（化石燃料）'],
            ['既存インフラが使える', 'ガスパイプラインにそのまま注入可能。新しいインフラ投資が不要', '水素（専用パイプライン必要）'],
            ['24時間365日発電', '天候に左右されない安定供給。太陽光や風力の弱点を補完', '太陽光・風力（天候依存）'],
            ['廃棄物処理と一石二鳥', 'ゴミ処理＋エネルギー生産を同時に実現。ゲートフィーという追加収入', '焼却処分（エネルギー回収効率低い）'],
            ['肥料も副産物', '発酵残渣（消化液）は高品質な有機肥料として農地に還元', 'なし（追加の収入源）'],
        ],
        [avail*0.18, avail*0.52, avail*0.30]
    ))

    story.append(Paragraph('1.4 ヨーロッパのバイオメタン市場', s_h2))

    story.append(stat_boxes([
        ('35 bcm', 'EU 2030年目標\n（年間生産量）'),
        ('1,620', '稼働中プラント数\n（2024年末時点）'),
        ('284億EUR', '2030年までの\nコミット済み民間投資'),
        ('5.2 bcm', '2024年の\nバイオメタン生産量'),
    ]))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph('出典：European Biogas Association、REPowerEU計画', s_small))

    story.append(info_box(
        'なぜヨーロッパで急成長？',
        '<b>1. エネルギー安全保障：</b>2022年のロシア-ウクライナ戦争でロシア産天然ガスへの依存リスクが顕在化。'
        '自国で作れるバイオメタンが「エネルギー自給」の切り札に。<br/>'
        '<b>2. 気候変動対策：</b>EUの「Fit for 55」で2030年までに温室効果ガス55%削減目標。'
        'ガス部門の脱炭素化にバイオメタンが不可欠。<br/>'
        '<b>3. REPowerEU：</b>EU委員会が2022年に発表した計画。2030年までにバイオメタン生産を年間35 bcm（現在の約10倍）に拡大する目標。',
        WARN_BG, WARN_BORDER
    ))

    story.append(PageBreak())

    # =========================================
    # CHAPTER 2: Mitsubishi Corp Energy Business
    # =========================================
    story.append(section_header_bar('第2章　三菱商事のエネルギー事業'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('2.1 三菱商事って何の会社？', s_h2))
    story.append(info_box(
        '日本最大の「総合商社」',
        '三菱商事は「モノを売る」だけの会社ではありません。<br/>'
        '世界中で<b>エネルギー、金属、食料、化学品、インフラ</b>など幅広い分野で<b>事業投資</b>を行い、<br/>'
        '自ら事業を「経営」する会社です。連結純利益は約1兆円規模。<br/>'
        'いわば「投資ファンド＋事業会社」のハイブリッドです。'
    ))

    story.append(Paragraph('2.2 エネルギー事業の全体像', s_h2))
    story.append(Paragraph('三菱商事のエネルギー事業は大きく4つの柱で構成されています。', s_body))

    story.append(make_table(
        ['事業領域', '概要', '規模感'],
        [
            ['天然ガス・LNG', 'LNG（液化天然ガス）の生産・輸送・販売。世界13のLNGプロジェクトに参画。2026年1月には米国Aethon Energyのシェールガス資産を75.3億ドルで取得', '年間約1,500万トンの生産能力\n日本のLNG輸入量の約20%に関与\n2030年目標：2,000万トン/年'],
            ['石油・石油化学', '原油トレーディング、精製事業。石炭権益は完全撤退済み', '縮小・転換中'],
            ['再生可能エネルギー', 'Eneco（オランダ）を軸に洋上風力・太陽光・蓄電池を展開。再エネ容量3.9GW（2024年9月時点）→2030年に6.6GW目標', 'Eneco：約2.8GWの再エネ資産\n欧州最大級の再エネ事業者'],
            ['次世代エネルギー', '水素（Eneco Diamond Hydrogen：ロッテルダムに800MW電解装置、年間8万トンのグリーン水素）、アンモニア、CCUS', 'ロッテルダム水素：690百万ドル投資\nNortH2：25億EUR投資計画'],
            ['バイオガス（新規）', '2025年11月にKIS Group（シンガポール）にマイノリティ出資。東南アジア・インド・欧州でバイオガス事業を共同展開', '2030年までに10億ドルの共同投資計画\n70以上のプロジェクト実績（KIS）'],
        ],
        [avail*0.15, avail*0.55, avail*0.30]
    ))

    story.append(Paragraph('2.3 エネルギートランジション戦略', s_h2))

    story.append(info_box(
        '「2050年ネットゼロ」に向けた経営シフト',
        '三菱商事は「経営戦略2027」（2025年4月～）で<b>「EX（エネルギートランスフォーメーション）」</b>を最重要テーマに掲げています。<br/>'
        'EX関連投資に3年間で約<b>1.2兆円</b>を投下する計画です。<br/><br/>'
        '具体的には：<br/>'
        '・化石燃料から再エネ・次世代エネルギーへの投資シフト（石炭は完全撤退済み）<br/>'
        '・2030年までに再エネ容量を6.6GWに倍増<br/>'
        '・Enecoを軸に欧州でグリーン水素・再エネ事業を大規模展開<br/>'
        '・2026年4月にエネルギー関連2グループを統合 →「エネルギー&パワーソリューショングループ」新設<br/>'
        '・<b>2025年11月にKIS Groupへ出資し、バイオガス市場に初参入</b>'
    ))

    story.append(Paragraph('2.4 欧州でのプレゼンス', s_h2))
    story.append(make_table(
        ['投資先', '国', '事業内容', '三菱商事の役割'],
        [
            ['Eneco', 'オランダ・ベルギー・独', '電力・ガス小売、洋上風力、太陽光。再エネ資産約2.8GW', '80%出資（中部電力20%）\n2020年に約41億EURで買収'],
            ['Eneco Diamond\nHydrogen', 'オランダ（ロッテルダム）', '800MW電解装置で年間8万トンのグリーン水素を生産。2029年稼働予定', '合弁会社（MC+Eneco）\n投資額690百万ドル'],
            ['NortH2', 'オランダ（北海）', '洋上風力4GW → グリーン水素年間100万トン。Shell等と共同', 'Eneco経由で参画\n投資額25億EUR'],
            ['LNG Canada', 'カナダ（BC州）', '2025年7月に初出荷。生産能力拡張を検討中', '15%出資'],
            ['蓄電池事業', '英国・欧州各国', '大型蓄電池（BESS）の開発・運営', '事業投資'],
        ],
        [avail*0.16, avail*0.20, avail*0.37, avail*0.27]
    ))

    story.append(Spacer(1, 3*mm))
    story.append(info_box(
        'ポイント：バイオメタンは「始まったばかり」の領域',
        '三菱商事は2025年11月にKIS Groupに出資し、バイオガス市場に<b>初参入</b>しました。<br/>'
        'しかしKIS Groupは<b>東南アジア・インドが中心</b>で、<b>欧州バイオメタン事業は手薄</b>です。<br/>'
        'カナデビア（KVI）との協業は、三菱商事のバイオガス戦略を<b>「欧州」に拡張する絶好の機会</b>です。<br/>'
        'Enecoとのシナジー（ガス販売先）が加われば、KIS Group以上に戦略的価値が高い可能性があります。',
        WARN_BG, WARN_BORDER
    ))

    story.append(PageBreak())

    # =========================================
    # CHAPTER 3: Who is KVI?
    # =========================================
    story.append(section_header_bar('第3章　カナデビア（KVI）とは何者か？'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('3.1 会社の成り立ち', s_h2))

    story.append(make_table(
        ['項目', '内容'],
        [
            ['正式名称', 'カナデビア株式会社（Kanadevia Corporation）'],
            ['旧社名', '日立造船株式会社（Hitachi Zosen Corporation）'],
            ['社名変更', '2024年10月1日に改称'],
            ['証券コード', '7004（東証プライム）'],
            ['社名の由来', '「奏でる」（日本語）＋「Via」（ラテン語：道）＝ 調和の道'],
            ['創業', '1881年（明治14年） ※造船業から出発'],
        ],
        [avail*0.22, avail*0.78]
    ))

    story.append(Paragraph('3.2 「日立造船」なのに船を作っていない？', s_h2))
    story.append(info_box(
        '意外な事実',
        '日立造船は<b>2002年に造船事業を分離</b>しています（現・ジャパンマリンユナイテッド）。<br/>'
        '現在の主力は<b>環境プラント事業</b>（ごみ焼却・廃棄物処理）と<b>バイオメタン・バイオガス事業</b>です。<br/>'
        '「船」とは無関係の環境テクノロジー企業に完全に変貌しています。<br/>'
        'このミスマッチを解消するために「カナデビア」に改称しました。'
    ))

    story.append(Paragraph('3.3 KVI（Kanadevia Inova）とは？', s_h2))
    story.append(Paragraph(
        'カナデビアの<b>最大の子会社</b>がスイス・チューリッヒに本社を置く<b>Kanadevia Inova AG（KVI）</b>です。', s_body))

    story.append(stat_boxes([
        ('3,000+人', '従業員数'),
        ('17か国', '事業展開国'),
        ('2,500億円', '年間売上高\n（2025年度見込み）'),
        ('4,000億円', '2030年度\n売上目標'),
    ]))
    story.append(Spacer(1, 2*mm))

    story.append(make_table(
        ['事業領域', '内容', '技術・ブランド'],
        [
            ['Waste-to-X (WtX)', 'ごみ焼却発電プラントの設計・建設・運営。欧州を中心に世界的リーダー', 'Kanadevia Inova WtX'],
            ['リニューアブルガス (RG)', 'バイオガス・バイオメタンプラントの技術提供・建設・運営・投資', 'Kompogas（乾式）\nSchmack（湿式）\nBioMethan（ガス精製）'],
            ['アセットマネジメント', 'Iona Capital経由でバイオガスプラント群を保有・運営・投資管理', 'Kanadevia Inova Capital\n（旧Iona Capital）'],
        ],
        [avail*0.17, avail*0.48, avail*0.35]
    ))

    story.append(Paragraph('3.4 KVIの欧州拡大の歴史', s_h2))
    story.append(make_table(
        ['年', '出来事', '意味'],
        [
            ['2014', 'Kompogas技術を買収', '乾式メタン発酵技術を獲得。バイオガス事業に参入'],
            ['2021', 'Schmackグループ（独）の技術を買収', '湿式メタン発酵技術を追加。乾式＋湿式の両方をカバー'],
            ['2024.3', 'Schmack Biogas Srl（伊）の過半数株式取得', 'イタリア市場への本格参入。約70基のプラント実績'],
            ['2024.12', 'Iona Capital Ltd（英）を買収', '英国のバイオガスファンドマネージャー。11か所のプラント＋開発パイプライン'],
            ['2025.2', 'Groengas Cothen B.V.（蘭）の過半数株式取得', 'オランダ市場参入。年間100GWh規模のバイオメタン施設'],
            ['2025.10', '英国で2つのバイオガスプラント追加買収', 'Wardley / Lower Drayton。英国ポートフォリオ拡大'],
        ],
        [avail*0.08, avail*0.37, avail*0.55]
    ))

    story.append(PageBreak())

    # =========================================
    # CHAPTER 4: KVI's European Biomethane Business
    # =========================================
    story.append(section_header_bar('第4章　KVIの欧州バイオメタン事業の特徴'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('4.1 圧倒的な特徴：バリューチェーンの垂直統合', s_h2))
    story.append(info_box(
        '他社にない最大の強み',
        '通常のバイオメタン事業者は、「技術だけ」「運営だけ」「投資だけ」のどれか一つに特化しています。<br/>'
        'KVIは<b>技術開発 → EPC（設計・建設） → 保有・運営 → アセットマネジメント → ガス販売</b>の<br/>'
        '<b>全てを一社で行える世界でも稀有な存在</b>です。'
    ))

    story.append(Spacer(1, 2*mm))
    # Value chain visualization
    vc_steps = [
        ('技術開発', 'Kompogas（乾式）\nSchmack（湿式）\nBioMethan（精製）', MID_GREEN),
        ('EPC\n設計・建設', '世界100基以上の\nプラント建設実績', HexColor('#2980b9')),
        ('保有・運営\n（BOO）', '17か所のプラントを\n自社で保有・運営', HexColor('#8e44ad')),
        ('アセット\nマネジメント', 'Iona Capital経由\n機関投資家の資金運用', HexColor('#e67e22')),
        ('ガス製造\n・販売', 'Gas-to-Grid\nガスパイプラインへ供給', ACCENT_RED),
    ]
    vc_cells = []
    for title, desc, color in vc_steps:
        cell = [
            Paragraph(title, ParagraphStyle('VCT', fontName='CJK', fontSize=9, leading=12, textColor=white, alignment=TA_CENTER)),
            Paragraph(desc, ParagraphStyle('VCD', fontName='CJK', fontSize=7, leading=10, textColor=white, alignment=TA_CENTER)),
        ]
        vc_cells.append(cell)
    vc_w = avail / 5
    vc_table = Table([vc_cells], colWidths=[vc_w]*5)
    vc_style = [
        ('FONTNAME', (0,0), (-1,-1), 'CJK'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]
    for i, (_, _, color) in enumerate(vc_steps):
        vc_style.append(('BACKGROUND', (i, 0), (i, 0), color))
    vc_table.setStyle(TableStyle(vc_style))
    story.append(vc_table)
    story.append(Paragraph('図2：KVIのバリューチェーン垂直統合モデル', s_caption))

    story.append(Paragraph('4.2 プラントポートフォリオ', s_h2))

    story.append(stat_boxes([
        ('17か所', '保有プラント数'),
        ('4か国', '英国・蘭・伊・瑞'),
        ('100+ GWh', '年間バイオメタン\n生産能力'),
        ('Gas-to-Grid', '主要ビジネスモデル'),
    ]))
    story.append(Spacer(1, 2*mm))

    story.append(make_table(
        ['国', 'プラント', 'タイプ', '特徴'],
        [
            ['英国', 'Iona Capital経由 13か所', 'Gas-to-Grid\n農業CHP', '年金基金の資金で建設。農業廃棄物ベースが中心'],
            ['オランダ', 'Groengas Cothen', 'Gas-to-Grid', '年間100GWh。ベネルクス拡大の足がかり'],
            ['イタリア', 'Schmack Biogas 約70基', 'バイオガス発電\nバイオメタン', '北イタリア中心。FIT制度を活用'],
            ['スイス', 'Kompogas 関連', '乾式メタン発酵', '技術の発祥地。食品廃棄物処理'],
        ],
        [avail*0.10, avail*0.25, avail*0.18, avail*0.47]
    ))

    story.append(Paragraph('4.3 収益構造（5つの収入源）', s_h2))
    story.append(Paragraph('KVIのバイオメタン事業は、1つのプラントから<b>5つの収入</b>が得られるのが特徴です。', s_body))

    rev_data = [
        ['1. バイオメタン販売', 'ガスグリッドへ注入したバイオメタンの売上。TTF（欧州天然ガス指標）にリンク。', '最大の収入源'],
        ['2. GoO（グリーンガス証書）', 'バイオメタン1MWh生産につき1枚発行される「グリーン証書」の販売収入', 'プレミアム収入'],
        ['3. ゲートフィー', '原料（廃棄物）を持ち込む業者から受け取る処理手数料', '安定的な収入'],
        ['4. FIT/FIP補助金', '各国の固定価格買取制度（FIT）や市場プレミアム制度（FIP）からの補助金', '制度依存'],
        ['5. 消化液（肥料）販売', '発酵後の残渣を有機肥料として農家に販売', '副次的な収入'],
    ]
    story.append(make_table(
        ['収入源', '内容', '性格'],
        rev_data,
        [avail*0.20, avail*0.55, avail*0.25]
    ))

    story.append(Paragraph('4.4 「アセットリサイクル」構想', s_h2))
    story.append(info_box(
        'KVIのビジネスモデルの進化 ─ EPCからBOOへ',
        'かつてのKVIは「プラントを作って納品する」（EPC）だけの会社でした。<br/>'
        '今は「作って、自分で持って、運営して、稼ぐ」（BOO = Build-Own-Operate）に転換中。<br/><br/>'
        'さらに進化形として<b>「アセットリサイクル」</b>を構想しています：<br/>'
        '1. 自社でプラントを開発・建設・運営し、安定稼働を実績として示す<br/>'
        '2. 安定稼働後に外部投資家（年金基金、商社など）にセルダウン（一部売却）<br/>'
        '3. 回収した資金で新しいプラントを開発<br/>'
        '4. 売却後もO&M（運営管理）受託で長期的なフィー収入を確保<br/><br/>'
        'このモデルは<b>商社がマイノリティ出資する絶好の受け皿</b>になります。'
    ))

    story.append(PageBreak())

    # =========================================
    # CHAPTER 5: Why Mitsubishi Corp would be interested
    # =========================================
    story.append(section_header_bar('第5章　三菱商事はなぜ興味を持つのか？'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('5.1 投資の魅力マトリックス', s_h2))

    story.append(make_table(
        ['魅力ポイント', '具体的な内容', '三菱商事にとっての意味'],
        [
            ['1. 政策追い風\n（構造的成長）',
             'REPowerEUで2030年までにバイオメタン生産10倍の目標。各国政府が補助金・義務化で支援',
             '政策リスクが低い。成長が「読める」投資'],
            ['2. 安定キャッシュフロー\n（インフラ型）',
             'ガス販売＋GoO＋ゲートフィー＋FITの複数収入源。長期オフテイク契約あり',
             'LNGプロジェクトに似た安定的リターン。配当利回り型の投資'],
            ['3. Enecoとのシナジー',
             '三菱商事100%子会社のEneco（オランダ）はガス小売事業を展開。バイオメタンのオフテイク先として最適',
             'グループ内でバイオメタンの「供給」と「販売」を完結できる'],
            ['4. バリューチェーン\n参画機会',
             'KVIの技術力＋商社のファイナンス力・ネットワーク力の組み合わせ',
             '共同でプラント開発を加速。商社はキャピタルとオフテイクを提供'],
            ['5. ESG・脱炭素\nクレデンシャル',
             'バイオメタンはScope 1/2排出削減に直接貢献。グリーンガス証書の取扱い',
             'ESG投資家への説明材料。グリーン調達ニーズへの対応'],
            ['6. 既存LNG知見の活用',
             'ガスの品質管理、トレーディング、オフテイク交渉は天然ガス/LNG事業の知見が転用可能',
             '既存人材・ノウハウのレバレッジ'],
        ],
        [avail*0.17, avail*0.45, avail*0.38]
    ))

    story.append(Paragraph('5.2 Enecoとの具体的シナジー', s_h2))

    # Synergy diagram
    syn_data = [
        [Paragraph('<b>KVI（カナデビア）</b>\nバイオメタン製造\n技術・EPC\nプラント運営',
                   ParagraphStyle('Syn', fontName='CJK', fontSize=8, leading=12, textColor=white, alignment=TA_CENTER)),
         Paragraph('バイオメタン供給 >>>\n<<< 運営管理委託\nGoO発行 >>>\n<<< 開発資金',
                   ParagraphStyle('SynArrow', fontName='CJK', fontSize=7.5, leading=11, alignment=TA_CENTER, textColor=DARK_GREEN)),
         Paragraph('<b>Eneco（三菱商事）</b>\nガス小売\n電力販売\nカーボンクレジット取引',
                   ParagraphStyle('Syn2', fontName='CJK', fontSize=8, leading=12, textColor=white, alignment=TA_CENTER))],
    ]
    syn_table = Table(syn_data, colWidths=[avail*0.35, avail*0.30, avail*0.35])
    syn_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), MID_GREEN),
        ('BACKGROUND', (2, 0), (2, 0), MID_BLUE),
        ('BACKGROUND', (1, 0), (1, 0), LIGHT_GREEN),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 1, DARK_GREEN),
    ]))
    story.append(syn_table)
    story.append(Paragraph('図3：KVI × Eneco（三菱商事）のシナジーイメージ', s_caption))

    story.append(Paragraph('5.3 KIS Group出資との比較 ─ なぜKVIも必要か？', s_h2))
    story.append(Paragraph(
        '三菱商事は2025年11月にKIS Group（シンガポール）に出資済みです。ではなぜKVIにも出資する意味があるのか？', s_body))

    story.append(comparison_table(
        'KIS Group（既存投資）',
        'KVI/カナデビア（追加投資候補）',
        [
            '・東南アジア・インドが主戦場',
            '・パーム油工場廃液（POME）が主原料',
            '・BioLNG・BioCNG中心',
            '・新興国市場。規制・補助金が未成熟',
            '・プラント開発＋O&M',
        ],
        [
            '・欧州（英国・蘭・伊・瑞）が主戦場',
            '・農業廃棄物・食品廃棄物が主原料',
            '・Gas-to-Grid（パイプライン注入）中心',
            '・EU規制＋補助金が充実した成熟市場',
            '・技術→EPC→BOO→AM→販売の垂直統合',
        ],
        HexColor('#e67e22'), ACCENT_GREEN
    ))
    story.append(Spacer(1, 2*mm))
    story.append(info_box(
        '補完関係：「KIS（アジア）＋ KVI（欧州）」で世界をカバー',
        'KIS GroupとKVI/カナデビアは<b>地域も原料も事業モデルも異なり、競合しません。</b><br/>'
        '両方に出資することで、三菱商事はバイオガス/バイオメタン事業を<b>アジアと欧州の両方でカバー</b>でき、<br/>'
        'グローバルなバイオメタンプレーヤーとしての地位を確立できます。',
        LIGHT_GREEN, DARK_GREEN
    ))

    story.append(Paragraph('5.4 他の商社の動向 ─ 競合は既に動いている', s_h2))
    story.append(Paragraph(
        '欧州バイオガス/バイオメタン領域への日本の商社の参入は<b>既に始まっています</b>。', s_body))
    story.append(make_table(
        ['商社', '欧州バイオメタン関連の具体的動き', '参入度'],
        [
            ['住友商事',
             '2025年：デンマークSkovgaard Energyと<b>JV（North Sky A/S）設立</b>。バイオガス生産＋e-SAF開発。\n'
             '2024年：北欧Inherit Carbon Solutionsに出資（バイオガスからのCO2回収・貯留）',
             '先行（デンマーク）'],
            ['三井物産',
             '2023年：デンマークEuropean Energyの子会社に<b>49%出資</b>。世界初の商用e-メタノールプラント（Kasso、年4.2万トン）。\n'
             '2024年：ポルトガルGalpのバイオ燃料プラントに<b>25%出資</b>（400百万EUR規模）',
             '先行（デンマーク・ポルトガル）'],
            ['三菱商事',
             '2025年：KIS Group（アジアバイオガス）に出資。<b>欧州バイオメタン特化の投資はまだなし</b>。\n'
             'Enecoで欧州ガス小売基盤あり → 最も強力なシナジー基盤を保有',
             'ポテンシャル最大'],
            ['伊藤忠商事',
             '2023-25年：TES（ベルギー）と大阪ガス・東邦ガスとともにe-メタン事業で提携。\n'
             'デンマークEverfuelに出資（グリーン水素）',
             '間接的参入'],
            ['双日',
             'インドでバイオメタン生産に参入（2027年までに30プラント目標）。欧州は未参入',
             'アジア中心'],
        ],
        [avail*0.10, avail*0.62, avail*0.28]
    ))
    story.append(Spacer(1, 2*mm))
    story.append(info_box(
        '三菱商事の「遅れ」と「強み」',
        '住友商事・三井物産はデンマークで先行しています。しかし三菱商事には<b>他社にない決定的な強み</b>があります：<br/>'
        '<b>Eneco（オランダ・ベルギー・独）</b>という欧州最大級のガス小売基盤です。<br/>'
        'バイオメタンの「出口（販売先）」を自社グループ内に持つ商社は三菱商事だけ。<br/>'
        'KVIに出資すれば「製造（KVI）→ 販売（Eneco）」の垂直統合が完成し、<br/>'
        '住友商事・三井物産の個別プロジェクト投資とは<b>次元の異なるポジション</b>を構築できます。',
        WARN_BG, WARN_BORDER
    ))

    story.append(PageBreak())

    # =========================================
    # CHAPTER 6: M&A Characteristics
    # =========================================
    story.append(section_header_bar('第6章　バイオメタンM&Aの特徴'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('6.1 一般的なM&Aとの違い', s_h2))

    story.append(comparison_table(
        '一般的な企業M&A',
        'バイオメタンプラントM&A',
        [
            '・事業全体を一括で評価',
            '・DCF＋マルチプルで企業価値算定',
            '・無形資産（ブランド等）が重要',
            '・過去の財務実績が中心',
            '・M&A完了後はPMI（統合）',
        ],
        [
            '・プラント1基ごとに個別評価が必要',
            '・DCF＋MW単価＋Nm3単価で多面評価',
            '・有形資産（プラント設備）が中心',
            '・将来のキャッシュフロー予測が重要',
            '・M&A後もO&M委託で売り手と関係継続',
        ],
        MID_BLUE, MID_GREEN
    ))

    story.append(Paragraph('6.2 バイオメタンM&A特有の論点', s_h2))

    story.append(make_table(
        ['論点', '内容', 'なぜ重要か'],
        [
            ['プラント技術DD\n（テクニカルDD）',
             '各プラントの消化槽の状態、メタン収率、稼働率、残存耐用年数、大規模修繕の必要性を個別に評価',
             'プラントの「健康診断」。不良プラントが混ざるとバリュエーションが大きく下がる'],
            ['原料の長期確保',
             '廃棄物や農業残渣の安定供給契約の有無。原料が途絶えるとプラントが止まる',
             '「燃料の確保」が事業の生命線。契約期間・価格条件の確認が必須'],
            ['オフテイク契約',
             'バイオメタンの販売先との長期契約の有無。Take-or-Pay条項があれば収益が安定',
             '収益の予見可能性を決定づける。契約期間・価格算定式・相手方の信用力'],
            ['補助金制度リスク',
             '各国のFIT/FIP/SDE++等の制度が将来変更・廃止されるリスク',
             '補助金収入が全収入の20-40%を占めることも。制度変更は致命的'],
            ['GoO（証書）市場リスク',
             'グリーンガス証書の価格変動リスク。EU RED III改正の影響',
             '近年価格が大きく変動。バリュエーションの感度分析で重要'],
            ['環境・許認可リスク',
             '排出規制、臭気規制、環境影響評価の遵守状況。許認可の更新リスク',
             '許認可が取り消されるとプラントが操業停止。DDで必ず確認'],
            ['マルチ法域（Multi-Jurisdiction）',
             '英国・オランダ・イタリア・スイス等、複数国にまたがるDD・税務分析が必要',
             '各国で法制度・税制・補助金が異なる。専門家チームが大規模になりコスト増'],
        ],
        [avail*0.17, avail*0.45, avail*0.38]
    ))

    story.append(Paragraph('6.3 バリュエーション手法', s_h2))

    story.append(make_table(
        ['手法', '指標', '一般的なレンジ', '使い方'],
        [
            ['DCF法', 'WACC 7～9%\n割引率 約9%が業界標準', '─', 'メインの評価手法。プラント別CFを積み上げ'],
            ['EV/EBITDA\nマルチプル', 'EV/EBITDA', '10～12x（稼働資産）\n※戦略プレミアム付きは更に高い', 'EnviTec Biogas：約10.5x\nShell/Nature Energy：約62x（異常値）'],
            ['MW単価', 'GBP/MW\n（設備容量ベース）', 'GBP 8～10M/MW（中央値）\nGBP 2～12M/MW（全レンジ）', 'プラントの年齢・原料契約・補助金で大きく変動'],
            ['生産コスト', 'LCOE\n（EUR/MWh）', '54～130 EUR/MWh\n（規模による）', '大規模：54 EUR/MWh\n小規模：84 EUR/MWh'],
        ],
        [avail*0.14, avail*0.20, avail*0.30, avail*0.36]
    ))

    story.append(Paragraph('6.4 直近の主要M&A事例', s_h2))

    story.append(make_table(
        ['時期', '買い手', '対象', '国', '概要'],
        [
            ['2023.2', 'Shell', 'Nature Energy', 'デンマーク', '約19億EUR。業界史上最大。EV/EBITDA約62x（戦略プレミアム）'],
            ['2023', 'Verdalia\n(Goldman Sachs)', 'プラットフォーム構築', 'スペイン・伊', '10億EUR+。150GWhパイプライン'],
            ['2023', 'TotalEnergies', 'PGB（バイオガス）', 'ポーランド', '欧州4位のバイオガスポテンシャル市場に参入'],
            ['2024.5', 'Verdalia', '7プラント買収', 'イタリア', '671百万EURファイナンスの一環'],
            ['2024.10', 'Byont/Asterion', 'Arbio + Biofer', 'ベネルクス', 'CHP→バイオメタン転換戦略'],
            ['2024.12', 'Meridiam', 'Evergaz過半数', '仏・ベルギー・独', '14プラント、57百万EUR出資'],
            ['2025.1', 'KVI（カナデビア）', 'Iona Capital', '英国', '11プラント＋開発パイプライン'],
            ['2025', 'Partners Group', 'Energiedenker', 'ドイツ', '35バイオガス＋10バイオメタンプラント（60MW）'],
            ['2025.10', 'CIP', 'Northwichプラント', '英国', 'Orstedから取得。バイオメタン＋CO2回収に転換'],
        ],
        [avail*0.07, avail*0.13, avail*0.18, avail*0.15, avail*0.47]
    ))

    story.append(Spacer(1, 2*mm))
    story.append(info_box(
        'トレンド：石油メジャーがバイオメタンに殺到',
        'Shell、TotalEnergies、bp、ENI等の石油メジャーが2022年以降、欧州バイオメタン事業を大量に買収しています。<br/>'
        '理由は、バイオメタンが天然ガスの「脱炭素版」として既存事業との親和性が極めて高いため。<br/>'
        '<b>石油メジャーが大量に資金を投入する = 市場の成長性と事業性が高い証拠</b>です。<br/>'
        '日本の商社にとっても「乗り遅れないこと」が重要になっています。',
        WARN_BG, WARN_BORDER
    ))

    story.append(PageBreak())

    # =========================================
    # CHAPTER 7: Summary
    # =========================================
    story.append(section_header_bar('第7章　まとめ ─ 全体像の整理'))
    story.append(Spacer(1, 4*mm))

    story.append(Paragraph('7.1 全体のストーリー', s_h2))

    story.append(vertical_flow([
        ('市場環境',
         'EUのREPowerEU計画で2030年までにバイオメタン生産10倍目標。年間35 bcm。各国政府が補助金・義務化で後押し。'),
        ('KVIの強み',
         'カナデビアのKVIは技術→建設→運営→投資管理の全バリューチェーンを持つ世界でも稀有な存在。17か所のプラントを保有。'),
        ('三菱商事の\nフィット',
         'Enecoとのシナジー、LNG知見の転用、バイオメタン空白地帯の穴埋め。安定キャッシュフロー型のインフラ投資。'),
        ('M&Aの要点',
         'プラント個別DD、原料確保契約、オフテイク契約、補助金リスク、マルチ法域対応が鍵。EV/EBITDA 8-12xが目安。'),
    ], colors=[MID_BLUE, MID_GREEN, HexColor('#e67e22'), HexColor('#8e44ad')]))

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('7.2 想定される投資ストラクチャー', s_h2))

    # Structure diagram
    struct_rows = [
        [Paragraph('<b>三菱商事</b>\n（日本）', ParagraphStyle('S1', fontName='CJK', fontSize=9, leading=13, alignment=TA_CENTER, textColor=white)),
         '',
         Paragraph('<b>カナデビア</b>\n（日本）', ParagraphStyle('S2', fontName='CJK', fontSize=9, leading=13, alignment=TA_CENTER, textColor=white))],
        [Paragraph('20~25%出資', ParagraphStyle('S3', fontName='CJK', fontSize=8, leading=11, alignment=TA_CENTER, textColor=MID_GRAY)),
         '',
         Paragraph('75~80%保有', ParagraphStyle('S4', fontName='CJK', fontSize=8, leading=11, alignment=TA_CENTER, textColor=MID_GRAY))],
        ['', Paragraph('<b>新設SPV</b>\n（欧州・アイルランド or 英国）\nバイオメタン資産管理会社',
                      ParagraphStyle('S5', fontName='CJK', fontSize=9, leading=13, alignment=TA_CENTER, textColor=white)), ''],
        ['', Paragraph('▼ 保有', ParagraphStyle('S6', fontName='CJK', fontSize=8, leading=11, alignment=TA_CENTER, textColor=MID_GRAY)), ''],
        [Paragraph('<b>Iona Capital</b>\n英国プラント群', ParagraphStyle('S7', fontName='CJK', fontSize=8, leading=11, alignment=TA_CENTER, textColor=white)),
         Paragraph('<b>Groengas</b>\nオランダプラント', ParagraphStyle('S8', fontName='CJK', fontSize=8, leading=11, alignment=TA_CENTER, textColor=white)),
         Paragraph('<b>Schmack</b>\nイタリアプラント群', ParagraphStyle('S9', fontName='CJK', fontSize=8, leading=11, alignment=TA_CENTER, textColor=white))],
    ]
    struct_table = Table(struct_rows, colWidths=[avail*0.33, avail*0.34, avail*0.33])
    struct_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), MID_BLUE),
        ('BACKGROUND', (2, 0), (2, 0), MID_GREEN),
        ('BACKGROUND', (1, 2), (1, 2), HexColor('#8e44ad')),
        ('BACKGROUND', (0, 4), (0, 4), HexColor('#2980b9')),
        ('BACKGROUND', (1, 4), (1, 4), HexColor('#2980b9')),
        ('BACKGROUND', (2, 4), (2, 4), HexColor('#2980b9')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('INNERGRID', (0, 4), (-1, 4), 0.5, white),
    ]))
    story.append(struct_table)
    story.append(Paragraph('図4：想定投資ストラクチャー', s_caption))

    story.append(Paragraph('7.3 出資比率の選択（結論）', s_h2))

    story.append(comparison_table(
        '20%出資の場合',
        '25%出資の場合（推奨）',
        [
            '・配当は日本で全額課税（約30%）',
            '・株主ローン（SHL）を活用して節税',
            '・実効税率：31〜36%',
            '・ストラクチャーがやや複雑',
            '・SPV所在国：アイルランドが最有力',
        ],
        [
            '・配当の95%が日本で非課税',
            '・全額エクイティでシンプル',
            '・実効税率：14〜27%',
            '・ストラクチャーがシンプル',
            '・SPV所在国：英国 or アイルランド',
        ],
        HexColor('#e67e22'), ACCENT_GREEN
    ))

    story.append(Spacer(1, 4*mm))
    story.append(info_box(
        '最後に ─ なぜ「今」なのか',
        '<b>1. 競合が動いている：</b>Shell、TotalEnergies、bp等の石油メジャーが欧州バイオメタンを大量買収中。<br/>'
        '<b>2. KVIが「受け皿」を用意している：</b>アセットリサイクル構想により、外部投資家の受入体制が整いつつある。<br/>'
        '<b>3. Enecoとのシナジーが活きる：</b>三菱商事だからこそ実現できる「供給＋販売」の垂直統合。<br/>'
        '<b>4. 先行者利益：</b>日本の商社で欧州バイオメタンに本格参入した例はまだない。最初に動いた商社が最良のパートナーシップを得る。',
        LIGHT_GREEN, DARK_GREEN
    ))

    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="40%", thickness=1, color=DARK_GREEN, spaceAfter=5*mm))
    story.append(Paragraph('以上', ParagraphStyle('End', fontName='CJK', fontSize=12, alignment=TA_CENTER, textColor=DARK_GREEN)))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        '本資料は社内検討用です。外部への配布はお控えください。',
        ParagraphStyle('Disc', fontName='CJK', fontSize=8, alignment=TA_CENTER, textColor=MID_GRAY)))

    doc.build(story)
    print('PDF generated: /home/user/-/biomethane_guide.pdf')


if __name__ == '__main__':
    build()
