#!/usr/bin/env python3
"""Generate PDF from advisory_proposal.md using reportlab with CJK support."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# Register CJK font
FONT_PATH = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
pdfmetrics.registerFont(TTFont('CJK', FONT_PATH, subfontIndex=0))

# Colors
DARK_BLUE = HexColor('#1a3a5c')
MID_BLUE = HexColor('#2c5f8a')
LIGHT_BLUE = HexColor('#e8f0f8')
ACCENT = HexColor('#c0392b')
LIGHT_GRAY = HexColor('#f5f5f5')
BORDER_GRAY = HexColor('#cccccc')
TABLE_HEADER_BG = HexColor('#2c5f8a')
TABLE_ALT_ROW = HexColor('#f0f4f8')

# Page setup
PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

doc = SimpleDocTemplate(
    '/home/user/-/advisory_proposal.pdf',
    pagesize=A4,
    leftMargin=MARGIN,
    rightMargin=MARGIN,
    topMargin=MARGIN,
    bottomMargin=20 * mm,
)

# Styles
styles = getSampleStyleSheet()

s_title = ParagraphStyle('Title_CJK', fontName='CJK', fontSize=22, leading=28,
                         textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=6*mm)
s_subtitle = ParagraphStyle('Subtitle_CJK', fontName='CJK', fontSize=11, leading=16,
                            textColor=MID_BLUE, alignment=TA_CENTER, spaceAfter=3*mm)
s_h1 = ParagraphStyle('H1_CJK', fontName='CJK', fontSize=16, leading=22,
                       textColor=DARK_BLUE, spaceBefore=8*mm, spaceAfter=4*mm)
s_h2 = ParagraphStyle('H2_CJK', fontName='CJK', fontSize=13, leading=18,
                       textColor=MID_BLUE, spaceBefore=6*mm, spaceAfter=3*mm)
s_h3 = ParagraphStyle('H3_CJK', fontName='CJK', fontSize=11, leading=15,
                       textColor=DARK_BLUE, spaceBefore=4*mm, spaceAfter=2*mm)
s_body = ParagraphStyle('Body_CJK', fontName='CJK', fontSize=9, leading=14,
                         spaceAfter=2*mm)
s_bullet = ParagraphStyle('Bullet_CJK', fontName='CJK', fontSize=9, leading=14,
                           leftIndent=12, spaceAfter=1*mm, bulletIndent=0)
s_bold = ParagraphStyle('Bold_CJK', fontName='CJK', fontSize=9, leading=14,
                         spaceAfter=2*mm)
s_small = ParagraphStyle('Small_CJK', fontName='CJK', fontSize=8, leading=11,
                          textColor=HexColor('#666666'))
s_table_header = ParagraphStyle('TH', fontName='CJK', fontSize=8, leading=11,
                                 textColor=white, alignment=TA_LEFT)
s_table_cell = ParagraphStyle('TC', fontName='CJK', fontSize=8, leading=11)
s_table_cell_bold = ParagraphStyle('TCB', fontName='CJK', fontSize=8, leading=11)
s_footer = ParagraphStyle('Footer', fontName='CJK', fontSize=7, leading=10,
                           textColor=HexColor('#999999'), alignment=TA_CENTER)


def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    avail = PAGE_W - 2 * MARGIN
    if col_widths is None:
        n = len(headers)
        col_widths = [avail / n] * n

    data = [[Paragraph(h, s_table_header) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), s_table_cell) for c in row])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), TABLE_HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, -1), 'CJK'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style_cmds.append(('BACKGROUND', (0, i), (-1, i), TABLE_ALT_ROW))
    t.setStyle(TableStyle(style_cmds))
    return t


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER_GRAY, spaceAfter=3*mm, spaceBefore=2*mm)


def build():
    story = []
    avail = PAGE_W - 2 * MARGIN

    # ====== COVER PAGE ======
    story.append(Spacer(1, 40*mm))
    story.append(Paragraph('アドバイザリー提案書', s_title))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="60%", thickness=2, color=DARK_BLUE, spaceAfter=8*mm))
    story.append(Paragraph(
        'カナデビア欧州バイオメタン資産会社への<br/>マイノリティ出資に関するアドバイザリー業務のご提案',
        s_subtitle))
    story.append(Spacer(1, 15*mm))

    cover_data = [
        ['提出先', '[商社名] 御中'],
        ['提出日', '2026年3月14日'],
        ['提出者', '[アドバイザリーファーム名]'],
    ]
    cover_table = Table(
        [[Paragraph(r[0], s_table_cell_bold), Paragraph(r[1], s_table_cell)] for r in cover_data],
        colWidths=[avail*0.25, avail*0.45]
    )
    cover_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'CJK'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER_GRAY),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # ====== EXECUTIVE SUMMARY ======
    story.append(Paragraph('エグゼクティブサマリー', s_h1))
    story.append(hr())
    story.append(Paragraph(
        'カナデビア株式会社（旧日立造船）が100%子会社Kanadevia Inova AGを通じて保有する欧州バイオメタン資産群について、'
        '当該資産を新設SPVにカーブアウトした上で、貴社が20〜25%のマイノリティ出資を検討されるにあたり、'
        '弊社はフィナンシャルアドバイザリー（FA）、財務デューディリジェンス（財務DD）、税務デューディリジェンス（税務DD）、'
        'およびバリュエーションモデリングの各業務を一体的にご提供いたします。', s_body))

    story.append(Paragraph('対象事業の概要', s_h3))
    story.append(make_table(
        ['項目', '内容'],
        [
            ['売り手', 'カナデビア株式会社（Kanadevia Inova AG経由）'],
            ['対象資産', '欧州バイオメタン・バイオガス事業（英国・オランダ・イタリア・スイス・ドイツ等）'],
            ['中核子会社', 'Iona Capital Ltd（英国）＋グループ3社、Groengas Cothen B.V.（オランダ）、Schmackグループ（ドイツ・イタリア）、Kompogas関連資産（スイス）'],
            ['想定ストラクチャー', 'カナデビアが新設SPV（想定：オランダ法人）に対象資産をカーブアウト → 貴社がSPVに20〜25%出資'],
            ['想定取得価額', '非公開（本提案では100〜300百万ユーロのレンジを想定）'],
        ],
        [avail*0.22, avail*0.78]
    ))

    story.append(Paragraph('本案件の戦略的意義', s_h3))
    story.append(Paragraph('1. REPowerEU目標（2030年・350億m³）を背景とした欧州バイオメタン市場の構造的成長', s_bullet))
    story.append(Paragraph('2. カナデビアのEPC技術＋アセットマネジメント（Iona Capital）の垂直統合モデルへの参画', s_bullet))
    story.append(Paragraph('3. 貴社の既存エネルギーポートフォリオとのシナジー創出（トレーディング、オフテイク、グリーン証書）', s_bullet))
    story.append(Paragraph('4. リカーリング収益型事業への投資（EPCの一括売上からユーティリティ型収益への転換）', s_bullet))

    story.append(PageBreak())

    # ====== PART 1: FA ======
    story.append(Paragraph('第1部：フィナンシャルアドバイザリー（FA）業務', s_h1))
    story.append(hr())

    story.append(Paragraph('1.1 業務スコープ', s_h2))

    # Phase 1
    story.append(Paragraph('フェーズ1：案件初期評価・ストラクチャリング（2〜3ヶ月）', s_h3))
    story.append(make_table(
        ['業務項目', '内容'],
        [
            ['市場分析', '欧州バイオメタン市場の需給動向、価格見通し、規制環境（REPowerEU、RED III、各国FIT/FIP制度）の整理'],
            ['対象事業の初期評価', '公開情報ベースでのカナデビア欧州バイオメタン事業のプロファイリング（資産規模、稼働状況、開発パイプライン、収益構造）'],
            ['ストラクチャー設計', 'SPV所在国の選定（オランダが最有力）、出資比率の最適化（20% vs 25%の税務インパクト分析）、SHL活用の要否検討'],
            ['初期バリュエーション', '類似取引・類似企業ベースのインディカティブバリュエーションレンジの策定'],
            ['NBO支援', 'LOI/NBO文書の作成支援、主要条件の交渉方針策定'],
        ],
        [avail*0.22, avail*0.78]
    ))

    # Phase 2
    story.append(Paragraph('フェーズ2：DD・バリュエーション・交渉（3〜4ヶ月）', s_h3))
    story.append(make_table(
        ['業務項目', '内容'],
        [
            ['DD統括（PMO）', '財務DD・税務DD・法務DD・技術DD・環境DD・保険DDの全体統括。データルーム管理、Q&Aプロセスの運営'],
            ['バリュエーション確定', 'DDの結果を反映した最終バリュエーション。DCF・マルチプル・LBOの3手法による企業価値レンジの確定'],
            ['SPA交渉支援', '株式譲渡契約（SPA）/株主間契約（SHA）の主要条件交渉。価格調整メカニズム、表明保証、補償条項'],
            ['ファイナンシング支援', '貴社側の資金調達（社内決裁・投資委員会向け資料作成支援）、SPV側のプロジェクトファイナンス構造の分析'],
        ],
        [avail*0.22, avail*0.78]
    ))

    # Phase 3
    story.append(Paragraph('フェーズ3：クロージング・PMI準備（1〜2ヶ月）', s_h3))
    story.append(make_table(
        ['業務項目', '内容'],
        [
            ['CP充足支援', '独禁法届出（EU・各国）、外為法届出（日本）、FDI規制対応（英国NSI Act等）の各種前提条件充足の管理'],
            ['クロージングメカニズム', '価格調整計算、Completion Accountsの作成・レビュー支援'],
            ['PMI初期計画', 'ガバナンス体制（取締役指名権、情報権、拒否権）の設計、100日プランの策定支援'],
        ],
        [avail*0.22, avail*0.78]
    ))

    story.append(PageBreak())

    # Key issues
    story.append(Paragraph('1.2 FA業務の主要論点（本案件固有）', s_h2))

    story.append(Paragraph('論点A：出資比率の最適化', s_h3))
    story.append(Paragraph(
        '弊社推奨：25%出資が税務上のIRR改善効果が大きく、追加5%の投資額増に見合う蓋然性が高い。'
        'ただし、カナデビア側の意向（マイノリティの上限）を交渉で確認する必要あり。', s_body))
    story.append(make_table(
        ['項目', '20%出資', '25%出資'],
        [
            ['持分法適用', '適用可', '適用可'],
            ['外国子会社配当益金不算入', '適用不可（配当に日本で全額課税）', '適用可（配当の95%非課税）'],
            ['ストラクチャーの複雑さ', 'SHLでの節税を模索する必要あり', 'エクイティでシンプルに税務メリット享受'],
        ],
        [avail*0.22, avail*0.39, avail*0.39]
    ))

    story.append(Paragraph('論点B：SHL（シェアホルダーローン）の活用判断', s_h3))
    story.append(make_table(
        ['シナリオ', 'SHLの要否', '理由'],
        [
            ['20%出資の場合', '活用推奨', '益金不算入が使えないため、SPV側の利息損金算入でトータル税負担を軽減'],
            ['25%出資の場合', '不要', 'エクイティで益金不算入＋事業リターンをフルに享受する方が効率的'],
        ],
        [avail*0.2, avail*0.15, avail*0.65]
    ))

    story.append(Paragraph('論点C：SPV所在国', s_h3))
    story.append(make_table(
        ['候補国', '法人税率', '租税条約（対日本）', 'PE制度', '推奨度'],
        [
            ['オランダ', '25.8%', '配当源泉税0〜5%', 'あり（充実）', '最有力'],
            ['英国', '25%', '配当源泉税0%', 'なし', '既存構造次第'],
            ['ルクセンブルク', '24.94%', '配当源泉税5%', 'あり', 'BEPS厳格化'],
            ['スイス', '11.9〜21.6%', '配当源泉税5〜10%', 'なし', '重複リスク'],
        ],
        [avail*0.15, avail*0.13, avail*0.25, avail*0.2, avail*0.27]
    ))

    story.append(Paragraph('論点D：株主間契約（SHA）の重要条項', s_h3))
    story.append(make_table(
        ['権利', '内容'],
        [
            ['取締役指名権', '1名以上のBoard Seat（5名中1名等）'],
            ['情報権', '月次財務報告、年次監査報告、事業計画の事前共有'],
            ['重要事項拒否権', '一定金額以上の投資・借入・資産処分、関連当事者取引、定款変更等'],
            ['Tag-Along権', 'カナデビアが持分を売却する場合に同条件で売却に参加する権利'],
            ['Drag-Along権', '第三者への一括売却時の巻き込み条項（最低価格条件で保護）'],
            ['プットオプション', '一定条件（CoC、重大な契約違反等）発生時の売却権'],
            ['Anti-Dilution', '増資時の希薄化防止（プリエンプティブライト）'],
            ['デッドロック解消', 'Russian Roulette / Texas Shoot-Out等の最終手段'],
        ],
        [avail*0.22, avail*0.78]
    ))

    story.append(PageBreak())

    # Schedule
    story.append(Paragraph('1.3 想定スケジュール', s_h2))
    story.append(make_table(
        ['期間', '主要マイルストーン'],
        [
            ['Month 1-2', '初期評価、市場分析、ストラクチャー設計'],
            ['Month 3', 'NBO提出、交渉開始'],
            ['Month 4-5', 'DD実施、バリュエーション確定'],
            ['Month 6-7', 'SPA/SHA交渉・締結'],
            ['Month 8-9', 'クロージング、CP充足、PMI準備'],
        ],
        [avail*0.2, avail*0.8]
    ))

    story.append(Paragraph('1.4 FA報酬体系（案）', s_h2))
    story.append(make_table(
        ['項目', '金額'],
        [
            ['リテイナーフィー', '月額 [●] 百万円 × 最大9ヶ月'],
            ['サクセスフィー', '取引金額の [●]%（Lehmanフォーミュラベース）'],
            ['実費', '出張費・外部専門家費用等は別途実費精算'],
        ],
        [avail*0.3, avail*0.7]
    ))

    story.append(PageBreak())

    # ====== PART 2: FINANCIAL DD ======
    story.append(Paragraph('第2部：財務デューディリジェンス（財務DD）', s_h1))
    story.append(hr())

    story.append(Paragraph('2.1 対象期間・対象法人', s_h2))
    story.append(Paragraph('対象期間：直近3〜5会計年度の実績（FY2021〜FY2025）＋直近管理会計月次データ＋事業計画', s_body))
    story.append(make_table(
        ['法人', '所在国', '分析の重点'],
        [
            ['Iona Capital Ltd', '英国', 'AM事業のフィー収入構造、AUM'],
            ['Iona Capital Investments Ltd', '英国', '直接保有プラントの収益性'],
            ['Iona Capital Asset Management Ltd', '英国', 'O&M収入構造'],
            ['Iona Capital Development Ltd', '英国', '開発パイプラインの進捗・コスト'],
            ['Groengas Cothen B.V.', 'オランダ', 'バイオメタン生産・販売実績'],
            ['Schmackグループ各社', 'ドイツ・イタリア', '湿式メタン発酵事業の収益性'],
            ['Kompogas関連資産', 'スイス', '乾式メタン発酵事業の収益性'],
        ],
        [avail*0.3, avail*0.15, avail*0.55]
    ))

    story.append(Paragraph('2.2 分析項目', s_h2))

    story.append(Paragraph('A. 収益の質（Quality of Earnings）', s_h3))
    story.append(make_table(
        ['項目', '分析内容'],
        [
            ['収益ドライバー分解', 'プラント別の売上構成（バイオメタン販売、GoO収入、ゲート手数料、FIT/FIP補助金、O&Mフィー、AM手数料）'],
            ['リカーリング vs ワンタイム', '安定的なリカーリング収益とワンタイム収益（プラント売却益、開発フィー）の峻別'],
            ['オフテイク契約の分析', '販売先、契約期間、価格決定メカニズム（固定 vs インデックスリンク）、Take-or-Pay条項の有無'],
            ['補助金依存度', '各国のFIT/FIP制度への依存度、制度改定リスク'],
            ['GoO収入', 'グリーンガス証書の発行・販売実績、価格推移、制度変更リスク'],
            ['非経常項目の調整', '一時的なコスト・収益の正規化'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(Paragraph('B. 運転資本・設備投資・ネットデット', s_h3))
    story.append(make_table(
        ['項目', '分析内容'],
        [
            ['NWC水準と季節性', 'プラント運営に必要な正常運転資本の算定、季節変動の分析'],
            ['既存プラントCapEx', '維持更新投資と成長投資の区分、今後の大規模修繕計画'],
            ['プラント稼働率・性能', '設計容量 vs 実稼働率、メタン収率、ダウンタイム分析'],
            ['開発パイプライン評価', '新規プラント建設の進捗状況、必要投資額、許認可ステータス'],
            ['有利子負債明細', 'プロジェクトファイナンス（プラント別）、リボルビングファシリティ、既存SHL'],
            ['デットライクアイテム', '未払退職給付、訴訟引当金、環境浄化義務、リース負債（IFRS16）'],
            ['CoC条項', '既存借入契約のChange of Control条項の有無'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(Paragraph('C. 事業計画の検証', s_h3))
    story.append(make_table(
        ['項目', '分析内容'],
        [
            ['過去実績との整合性', '経営陣の事業計画の前提が過去実績と整合的かの検証'],
            ['ボトムアップ検証', 'プラント別の生産量予測 × 単価予測でのクロスチェック'],
            ['感度分析の前提確認', 'バイオメタン価格、TTF、GoO価格、原料コスト等の主要変数の蓋然性'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(Paragraph('2.3 成果物', s_h2))
    story.append(Paragraph('1. 財務DDレポート（100〜150ページ）', s_bullet))
    story.append(Paragraph('2. Quality of Earnings分析表', s_bullet))
    story.append(Paragraph('3. 正規化EBITDA算定表（Adjusted EBITDA Bridge）', s_bullet))
    story.append(Paragraph('4. ネットデット算定表', s_bullet))
    story.append(Paragraph('5. NWC分析表', s_bullet))
    story.append(Paragraph('6. 経営陣の事業計画に対するコメントレポート', s_bullet))

    story.append(PageBreak())

    # ====== PART 3: TAX DD ======
    story.append(Paragraph('第3部：税務デューディリジェンス（税務DD）', s_h1))
    story.append(hr())

    story.append(Paragraph('3.1 対象法人・対象国', s_h2))
    story.append(make_table(
        ['国', '対象法人', '主要論点'],
        [
            ['英国', 'Iona Capital Ltd＋グループ3社', '法人税（25%）、キャピタルゲイン税、印紙税、利息制限（CIR）'],
            ['オランダ', 'Groengas Cothen B.V.、新設SPV', '法人税（25.8%）、PE、EARLE、源泉税、移転価格'],
            ['ドイツ', 'Schmack Biogas GmbH等', '法人税＋営業税（実効約30%）、CFC規制'],
            ['イタリア', 'Schmack Biogas Srl', 'IRES（24%）＋IRAP（3.9%）、バイオメタンFIT制度'],
            ['スイス', 'Kompogas関連', 'カーブアウト時の移転課税、州法人税'],
            ['日本', '貴社', '外国子会社配当益金不算入、CFC税制、過少資本税制、移転価格'],
        ],
        [avail*0.1, avail*0.35, avail*0.55]
    ))

    story.append(Paragraph('3.2 分析項目', s_h2))

    story.append(Paragraph('A. タックスストラクチャーの最適化', s_h3))
    story.append(make_table(
        ['項目', '分析内容'],
        [
            ['出資比率と日本側課税', '20% vs 25%での外国子会社配当益金不算入制度の適用可否とIRRインパクト'],
            ['中間持株会社の設計', 'オランダHoldCoの設立要否、PEの活用、実体要件の充足'],
            ['SHL vs エクイティ', 'SHLを用いた場合のトータル税負担シミュレーション'],
            ['配当還流ルートの設計', '各国プラントSPV → 中間HoldCo → 日本本社の配当還流における源泉税・PE・CFC税制の分析'],
            ['Exit時の税務', '持分売却時のキャピタルゲイン課税（各国）、PE非課税措置の適用可否'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(Paragraph('B. 対象会社の税務リスク', s_h3))
    story.append(make_table(
        ['項目', '分析内容'],
        [
            ['過去の税務申告レビュー', '直近3〜5年の法人税申告書・税務調査の履歴・更正リスク'],
            ['繰越欠損金', '各法人の繰越欠損金の金額・使用制限（株主変更ルール）'],
            ['移転価格ポジション', 'グループ間取引の移転価格ポリシー、TP文書化の状況'],
            ['VAT/GST', 'バイオメタン販売・GoO取引のVAT処理'],
            ['補助金の税務処理', 'FIT/FIP、SDE++補助金の課税タイミング・処理方法'],
            ['印紙税・不動産取引税', '株式取得時の印紙税（英国SDRT：0.5%）、不動産保有法人の場合のSDLT/RETT'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(Paragraph('C. カーブアウト固有の税務論点', s_h3))
    story.append(make_table(
        ['項目', '分析内容'],
        [
            ['カーブアウト時の移転課税', 'カナデビアが既存構造から新設SPVに資産移管する際の課税関係（各国）'],
            ['ステップアップの可否', '取得価額のステップアップ（時価洗替え）が可能か、将来の減価償却費増加効果'],
            ['グループ通算制度の離脱', 'カナデビアのタックスグループ（英国Group Relief等）から離脱する場合の影響'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(Paragraph('D. 日本側の税務（インバウンド分析）', s_h3))
    story.append(make_table(
        ['項目', '分析内容'],
        [
            ['外国子会社配当益金不算入', '適用要件の充足確認（25%以上・6ヶ月保有）、間接保有の場合の取扱い'],
            ['CFC税制', 'SPVが経済活動基準を満たすかの検証'],
            ['過少資本税制', 'SHL拠出時の負債・資本比率3:1ルールの適用シミュレーション'],
            ['移転価格税制', 'SHL利率の独立企業間価格の算定、ベンチマーク分析'],
            ['外国税額控除', '各国で課税された法人税・源泉税の外国税額控除枠の試算'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(Paragraph('3.3 成果物', s_h2))
    story.append(Paragraph('1. 税務DDレポート（各国別セクション＋クロスボーダー分析）', s_bullet))
    story.append(Paragraph('2. タックスストラクチャーメモランダム（推奨ストラクチャーの比較分析）', s_bullet))
    story.append(Paragraph('3. 税務リスク一覧表（リスク金額・発生可能性のマトリクス）', s_bullet))
    story.append(Paragraph('4. 繰越欠損金・税務属性の整理表', s_bullet))
    story.append(Paragraph('5. 配当還流シミュレーション（ストラクチャー別の実効税率比較）', s_bullet))
    story.append(Paragraph('6. SPA税務条項ドラフト（税務表明保証・補償条項の推奨文言）', s_bullet))

    story.append(PageBreak())

    # ====== PART 4: VALUATION ======
    story.append(Paragraph('第4部：バリュエーションモデリング', s_h1))
    story.append(hr())

    story.append(Paragraph('4.1 採用手法', s_h2))
    story.append(make_table(
        ['手法', '位置づけ', '概要'],
        [
            ['DCF法', 'メイン', 'プラント別のFCF予測 → WACC割引 → 企業価値算定'],
            ['類似企業比較法', 'クロスチェック', '欧州バイオメタン・リニューアブルユーティリティのEV/EBITDA、P/E等'],
            ['類似取引比較法', 'クロスチェック', '欧州バイオガス・バイオメタンM&A取引のマルチプル'],
            ['LBOモデル', '参考', 'PEバイヤーのリターン水準との比較'],
        ],
        [avail*0.18, avail*0.17, avail*0.65]
    ))

    story.append(Paragraph('4.2 DCFモデルの主要前提条件', s_h2))
    story.append(make_table(
        ['パラメータ', 'ベースケース', '感度分析レンジ'],
        [
            ['バイオメタン単価（EUR/MWh）', 'TTFリンク＋プレミアム', '±20%'],
            ['GoO価格（EUR/MWh）', '直近3年平均', '±30%'],
            ['プラント稼働率', '85〜90%', '75〜95%'],
            ['新規プラント完工確率', 'FID済100%/許認可済70%/初期30%', 'ケース別'],
            ['WACC', '7〜9%（ユーティリティベース）', '6〜10%'],
            ['ターミナル成長率', '1.5〜2.0%', '0.5〜2.5%'],
            ['FIT/FIP制度存続', '現行制度を前提', '制度打切りシナリオ'],
        ],
        [avail*0.3, avail*0.35, avail*0.35]
    ))

    story.append(Paragraph('4.3 類似企業（想定Comp Set）', s_h2))
    story.append(make_table(
        ['企業', '所在国', '事業内容'],
        [
            ['Scandinavian Biogas Fuels', 'スウェーデン', 'バイオガス・バイオメタン製造'],
            ['Envitec Biogas', 'ドイツ', 'バイオガスプラント運営・O&M'],
            ['Greenvolt Energias Renováveis', 'ポルトガル', '再エネ（バイオマス含む）'],
            ['Infinis Energy', '英国', '埋立ガス・バイオガス発電'],
        ],
        [avail*0.3, avail*0.2, avail*0.5]
    ))

    story.append(Paragraph('想定マルチプルレンジ', s_h3))
    story.append(make_table(
        ['マルチプル', 'レンジ', '備考'],
        [
            ['EV/EBITDA', '8〜12x', 'ユーティリティ型は高め、EPC型は低め'],
            ['EV/MW（発電容量ベース）', '2〜4M EUR/MW', 'バイオメタン換算の発電等価容量'],
            ['EV/Nm³（年間生産量）', '3〜6 EUR/Nm³', '生産能力ベース'],
        ],
        [avail*0.25, avail*0.2, avail*0.55]
    ))

    story.append(Paragraph('4.4 成果物', s_h2))
    story.append(Paragraph('1. バリュエーションモデル（Excel、200〜300行のタブ構成）', s_bullet))
    story.append(Paragraph('   - 前提条件シート / プラント別収益モデル / 連結P&L・BS・CF / FCF・DCF算定 / 感度分析・シナリオ分析 / マルチプル比較 / サマリー（フットボールチャート）', s_bullet))
    story.append(Paragraph('2. バリュエーションレポート（PowerPoint、30〜50ページ）', s_bullet))
    story.append(Paragraph('3. 投資委員会向けサマリー資料（PowerPoint、10〜15ページ）', s_bullet))

    story.append(PageBreak())

    # ====== PART 5: TEAM ======
    story.append(Paragraph('第5部：チーム体制', s_h1))
    story.append(hr())

    story.append(Paragraph('5.1 プロジェクトチーム構成', s_h2))
    story.append(make_table(
        ['役割', '人数', '担当領域'],
        [
            ['プロジェクトリーダー（MD/Partner）', '1名', '全体統括、交渉リード、投資委員会対応'],
            ['FA チーム', '2〜3名', 'ストラクチャリング、SPA/SHA交渉、PMI'],
            ['財務DD チーム', '3〜4名', 'QoE分析、NWC、ネットデット、事業計画検証'],
            ['税務DD チーム', '3〜4名', '日本税務1名＋欧州各国税務2〜3名（現地提携ファーム含む）'],
            ['バリュエーション チーム', '2〜3名', 'DCFモデル構築、マルチプル分析、感度分析'],
            ['合計', '11〜15名', ''],
        ],
        [avail*0.3, avail*0.1, avail*0.6]
    ))

    story.append(Paragraph('5.2 チーム間の主要連携ポイント', s_h2))
    story.append(make_table(
        ['連携', '内容'],
        [
            ['財務DD → バリュエーション', '正規化EBITDA、NWC水準、ネットデットをモデルに反映'],
            ['税務DD → バリュエーション', '各国の実効税率、繰越欠損金の使用可能額、源泉税率をモデルに反映'],
            ['税務DD → FA', 'タックスストラクチャーの推奨結果をSPA/SHA条件に反映'],
            ['FA → 全チーム', '交渉の進捗に応じたスコープ調整、追加分析の指示'],
            ['バリュエーション → FA', 'バリュエーションレンジを交渉ポジションに反映、BBO策定'],
        ],
        [avail*0.25, avail*0.75]
    ))

    story.append(PageBreak())

    # ====== PART 6: FEES ======
    story.append(Paragraph('第6部：報酬総括・契約条件', s_h1))
    story.append(hr())

    story.append(Paragraph('6.1 報酬サマリー', s_h2))
    story.append(make_table(
        ['業務', '報酬体系', '金額（税別）'],
        [
            ['FA（リテイナー）', '月額固定 × 最大9ヶ月', '[●] 百万円'],
            ['FA（サクセスフィー）', '取引金額の [●]%', '[●] 百万円（想定）'],
            ['財務DD', '固定報酬', '[●] 百万円'],
            ['税務DD', '固定報酬', '[●] 百万円'],
            ['バリュエーション', 'FA報酬に含む', '─'],
        ],
        [avail*0.25, avail*0.4, avail*0.35]
    ))

    story.append(Paragraph('6.2 契約条件', s_h2))
    story.append(make_table(
        ['項目', '条件'],
        [
            ['契約期間', '業務委託契約締結日〜クロージング日＋3ヶ月'],
            ['独占条項', '本案件に関するFA業務は弊社が独占的に受任'],
            ['利益相反', 'カナデビアおよびその関係者へのアドバイザリー業務は受任しない'],
            ['秘密保持', 'NDA締結済みの前提（別途NDAを締結）'],
            ['準拠法', '日本法'],
            ['紛争解決', '東京地方裁判所を第一審の専属的合意管轄裁判所とする'],
        ],
        [avail*0.2, avail*0.8]
    ))

    story.append(Spacer(1, 15*mm))
    story.append(hr())

    # ====== APPENDIX ======
    story.append(Paragraph('付録A：想定タイムライン（詳細）', s_h2))
    story.append(make_table(
        ['時期', '主要マイルストーン'],
        [
            ['2026年4月', 'アドバイザリー契約締結、NDA締結・初期情報収集'],
            ['2026年5月', '市場分析・初期バリュエーション、ストラクチャー設計'],
            ['2026年6月', 'NBO提出、カナデビアとの条件交渉開始'],
            ['2026年7月', 'DD開始（データルームアクセス）、財務DD・税務DD・技術DD並行実施'],
            ['2026年8月', 'DD中間報告、マネジメントインタビュー・サイトビジット'],
            ['2026年9月', 'DD最終報告、バリュエーション確定、BBO提出'],
            ['2026年10月', 'SPA/SHA交渉、投資委員会付議'],
            ['2026年11月', 'SPA/SHA締結（サイニング）、CP充足プロセス開始'],
            ['2026年12月', '独禁法・FDI届出'],
            ['2027年1月', 'クロージング、PMI開始'],
        ],
        [avail*0.18, avail*0.82]
    ))

    story.append(Paragraph('付録B：関連制度一覧', s_h2))
    story.append(make_table(
        ['制度', '概要', '本案件への影響'],
        [
            ['REPowerEU', '2030年・350億m³目標', '市場成長の根拠'],
            ['RED III', '再エネ指令、GoO発行義務', 'GoO収入の制度的裏付け'],
            ['英国GGSS', 'Green Gas Support Scheme', '英国プラントの補助金収入'],
            ['オランダSDE++', '再エネ補助金制度', 'オランダプラントの補助金収入'],
            ['外国子会社配当益金不算入', '25%以上保有で配当95%非課税', '出資比率の決定に直結'],
            ['過少資本税制', 'D/E 3:1超の利息は損金不算入', 'SHL設計時の上限'],
            ['EARLE（オランダ）', '利息がEBITDA 20%超で損金不算入', 'SPV側の利息制限'],
        ],
        [avail*0.25, avail*0.35, avail*0.4]
    ))

    story.append(Spacer(1, 20*mm))
    story.append(Paragraph('以上', ParagraphStyle('End', fontName='CJK', fontSize=11, alignment=TA_CENTER)))
    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        '本提案に関するご質問・ご要望がございましたら、お気軽にお申し付けください。',
        ParagraphStyle('EndNote', fontName='CJK', fontSize=9, alignment=TA_CENTER, textColor=HexColor('#666666'))))

    doc.build(story)
    print('PDF generated successfully.')


if __name__ == '__main__':
    build()
