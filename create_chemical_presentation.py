from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Slide 1: タイトルスライド
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

    # タイトル
    title_box = slide1.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = "主要化学メーカーの事業概要とM&A実績"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)
    p.alignment = PP_ALIGN.CENTER

    # サブタイトル
    subtitle_box = slide1.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "2024-2026年の動向分析"
    p = subtitle_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.color.rgb = RGBColor(102, 102, 102)
    p.alignment = PP_ALIGN.CENTER

    # 背景色
    background = slide1.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 248, 250)

    # Slide 2: 目次
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide2.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide2.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "目次"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    content_box = slide2.shapes.add_textbox(Inches(1.5), Inches(2), Inches(7), Inches(4))
    content_frame = content_box.text_frame

    items = [
        "1. 日本の主要化学メーカー",
        "2. グローバル大手化学メーカー",
        "3. 化学業界のM&A動向",
        "4. 主要M&A事例（2024-2025年）",
        "5. まとめと今後の展望"
    ]

    for i, item in enumerate(items):
        if i > 0:
            content_frame.add_paragraph()
        p = content_frame.paragraphs[i]
        p.text = item
        p.font.size = Pt(24)
        p.space_after = Pt(20)
        p.font.color.rgb = RGBColor(51, 51, 51)

    # Slide 3: 日本の主要化学メーカー
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide3.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide3.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "日本の主要化学メーカー"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    # 三菱ケミカル
    box1 = slide3.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(4.2), Inches(2.2))
    frame1 = box1.text_frame
    frame1.text = "三菱ケミカルグループ"
    p = frame1.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)

    frame1.add_paragraph()
    p = frame1.paragraphs[1]
    p.text = "• 国内最大手の総合化学メーカー"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame1.add_paragraph()
    p = frame1.paragraphs[2]
    p.text = "• M&Aによる成長戦略を推進"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame1.add_paragraph()
    p = frame1.paragraphs[3]
    p.text = "• 2026年3月期：田辺三菱製薬譲渡により純利益3.2倍を見込む"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame1.add_paragraph()
    p = frame1.paragraphs[4]
    p.text = "• 価格政策と資産最適化で560億円増益予想"
    p.font.size = Pt(14)

    # 住友化学
    box2 = slide3.shapes.add_textbox(Inches(5.3), Inches(1.8), Inches(4.2), Inches(2.2))
    frame2 = box2.text_frame
    frame2.text = "住友化学"
    p = frame2.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(204, 0, 0)

    frame2.add_paragraph()
    p = frame2.paragraphs[1]
    p.text = "• 医薬品・農薬事業に強み"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame2.add_paragraph()
    p = frame2.paragraphs[2]
    p.text = "• 医薬品事業が利益の稼ぎ頭"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame2.add_paragraph()
    p = frame2.paragraphs[3]
    p.text = "• 情報電子化学部門も主力事業"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame2.add_paragraph()
    p = frame2.paragraphs[4]
    p.text = "• 構造改革を推進中"
    p.font.size = Pt(14)

    # 旭化成
    box3 = slide3.shapes.add_textbox(Inches(0.5), Inches(4.3), Inches(4.2), Inches(2.2))
    frame3 = box3.text_frame
    frame3.text = "旭化成"
    p = frame3.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 153, 51)

    frame3.add_paragraph()
    p = frame3.paragraphs[1]
    p.text = "• 住宅から医療まで多角経営"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame3.add_paragraph()
    p = frame3.paragraphs[2]
    p.text = "• 引き続き最高益を更新見通し"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame3.add_paragraph()
    p = frame3.paragraphs[3]
    p.text = "• 売上・収益性向上で成長"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame3.add_paragraph()
    p = frame3.paragraphs[4]
    p.text = "• 2026年4月：旭化成エポキシと合併予定"
    p.font.size = Pt(14)

    # その他
    box4 = slide3.shapes.add_textbox(Inches(5.3), Inches(4.3), Inches(4.2), Inches(2.2))
    frame4 = box4.text_frame
    frame4.text = "その他主要メーカー"
    p = frame4.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(102, 51, 153)

    frame4.add_paragraph()
    p = frame4.paragraphs[1]
    p.text = "• 信越化学工業：シリコン・半導体"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame4.add_paragraph()
    p = frame4.paragraphs[2]
    p.text = "• 三井化学：機能性材料に強み"
    p.font.size = Pt(14)
    p.space_after = Pt(8)

    frame4.add_paragraph()
    p = frame4.paragraphs[3]
    p.text = "• カネカ：機能性樹脂・医薬"
    p.font.size = Pt(14)

    # Slide 4: グローバル大手化学メーカー
    slide4 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide4.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide4.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "グローバル大手化学メーカー"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    # BASF
    box1 = slide4.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(9), Inches(1.5))
    frame1 = box1.text_frame
    frame1.text = "BASF（ドイツ）"
    p = frame1.paragraphs[0]
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)

    frame1.add_paragraph()
    p = frame1.paragraphs[1]
    p.text = "• 世界最大級の総合化学メーカー（1865年設立）"
    p.font.size = Pt(16)
    p.space_after = Pt(6)

    frame1.add_paragraph()
    p = frame1.paragraphs[2]
    p.text = "• 2023年度売上高：689億ユーロ（約10.3兆円）"
    p.font.size = Pt(16)
    p.space_after = Pt(6)

    frame1.add_paragraph()
    p = frame1.paragraphs[3]
    p.text = "• 主要事業：サーフェステクノロジー（触媒・コーティング）、マテリアル（先端材料・プラスチック）、農薬"
    p.font.size = Pt(16)

    # Dow
    box2 = slide4.shapes.add_textbox(Inches(0.5), Inches(3.6), Inches(9), Inches(1.3))
    frame2 = box2.text_frame
    frame2.text = "Dow（米国）"
    p = frame2.paragraphs[0]
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(204, 0, 0)

    frame2.add_paragraph()
    p = frame2.paragraphs[1]
    p.text = "• 世界最大級の総合化学メーカー（1897年設立）"
    p.font.size = Pt(16)
    p.space_after = Pt(6)

    frame2.add_paragraph()
    p = frame2.paragraphs[2]
    p.text = "• 2019年にDowDuPontから素材事業として分社化"
    p.font.size = Pt(16)
    p.space_after = Pt(6)

    frame2.add_paragraph()
    p = frame2.paragraphs[3]
    p.text = "• 主要事業：包装材料、インフラストラクチャ、消費財向け材料科学"
    p.font.size = Pt(16)

    # DuPont
    box3 = slide4.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(9), Inches(1.5))
    frame3 = box3.text_frame
    frame3.text = "DuPont（米国）"
    p = frame3.paragraphs[0]
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 153, 51)

    frame3.add_paragraph()
    p = frame3.paragraphs[1]
    p.text = "• 世界最大級の化学メーカー（1802年設立）"
    p.font.size = Pt(16)
    p.space_after = Pt(6)

    frame3.add_paragraph()
    p = frame3.paragraphs[2]
    p.text = "• 2019年にDowDuPontから特殊産業材事業として分社化"
    p.font.size = Pt(16)
    p.space_after = Pt(6)

    frame3.add_paragraph()
    p = frame3.paragraphs[3]
    p.text = "• 2025年8月：ケブラー・ノーメックスを含むアラミド事業を約18億ドルで売却決定（2026年Q1完了予定）"
    p.font.size = Pt(16)

    # Slide 5: M&A動向
    slide5 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide5.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide5.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "化学業界のM&A動向（2024-2025年）"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    content_box = slide5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame

    content_frame.text = "市場環境"
    p = content_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)
    p.space_after = Pt(12)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[1]
    p.text = "• 2024年第3四半期：M&A取引は引き続き減少傾向（マクロ経済の不確実性が影響）"
    p.font.size = Pt(16)
    p.space_after = Pt(10)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[2]
    p.text = "• 2024年通年：短期金利の低下を背景に前年比で取引件数がわずかに増加"
    p.font.size = Pt(16)
    p.space_after = Pt(20)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[3]
    p.text = "主要トレンド"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)
    p.space_after = Pt(12)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[4]
    p.text = "1. 製品ポートフォリオの多角化とグローバル展開の加速"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[5]
    p.text = "2. 現地・地域事業者買収によるローカルサプライチェーンの確立"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[6]
    p.text = "3. サステナビリティ重視：グリーンテクノロジー、リサイクル、再生可能エネルギー"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[7]
    p.text = "4. ノンコア資産売却による事業ポートフォリオの最適化"
    p.font.size = Pt(16)

    # Slide 6: 主要M&A事例（2024年）- Part 1
    slide6 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide6.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide6.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "主要M&A事例（2024年）- 日本企業"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    # 案件1
    box1 = slide6.shapes.add_textbox(Inches(0.5), Inches(1.6), Inches(9), Inches(1.3))
    frame1 = box1.text_frame
    frame1.text = "日本ペイントホールディングス → AOC買収"
    p = frame1.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)

    frame1.add_paragraph()
    p = frame1.paragraphs[1]
    p.text = "• 買収金額：約6,300億円（約435億ドル）"
    p.font.size = Pt(16)

    frame1.add_paragraph()
    p = frame1.paragraphs[2]
    p.text = "• 概要：米国化学メーカーAOCを買収。コーティング材料原料で高シェア、高収益性を実現"
    p.font.size = Pt(16)

    # 案件2
    box2 = slide6.shapes.add_textbox(Inches(0.5), Inches(3.2), Inches(9), Inches(1.1))
    frame2 = box2.text_frame
    frame2.text = "信越化学工業 → 三益半導体工業の完全子会社化"
    p = frame2.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)

    frame2.add_paragraph()
    p = frame2.paragraphs[1]
    p.text = "• 時期：2024年4月"
    p.font.size = Pt(16)

    frame2.add_paragraph()
    p = frame2.paragraphs[2]
    p.text = "• 概要：TOBにより三益半導体工業を完全子会社化"
    p.font.size = Pt(16)

    # 案件3
    box3 = slide6.shapes.add_textbox(Inches(0.5), Inches(4.6), Inches(9), Inches(1.1))
    frame3 = box3.text_frame
    frame3.text = "出光興産 → アグロカネショウ買収"
    p = frame3.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)

    frame3.add_paragraph()
    p = frame3.paragraphs[1]
    p.text = "• 完了：2024年12月24日"
    p.font.size = Pt(16)

    frame3.add_paragraph()
    p = frame3.paragraphs[2]
    p.text = "• 概要：農薬メーカーのアグロカネショウをTOBにより買収"
    p.font.size = Pt(16)

    # 案件4
    box4 = slide6.shapes.add_textbox(Inches(0.5), Inches(6.0), Inches(9), Inches(1.1))
    frame4 = box4.text_frame
    frame4.text = "カネカ → EndoStream Medical買収"
    p = frame4.paragraphs[0]
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)

    frame4.add_paragraph()
    p = frame4.paragraphs[1]
    p.text = "• 完了：2024年12月23日"
    p.font.size = Pt(16)

    frame4.add_paragraph()
    p = frame4.paragraphs[2]
    p.text = "• 概要：イスラエルのEndoStream Medical Ltd.の株式96.8%を取得し子会社化（医療機器分野）"
    p.font.size = Pt(16)

    # Slide 7: 主要M&A事例（2024年）- Part 2
    slide7 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide7.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide7.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "事業売却・構造改革（2024年）"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    content_box = slide7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame

    content_frame.text = "住友化学の構造改革"
    p = content_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(204, 0, 0)
    p.space_after = Pt(12)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[1]
    p.text = "• Pace Internationalを米AgFresh Solutionsに売却（2024年3月）"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[2]
    p.text = "• 中国のLCD偏光フィルム事業を湖北力佑光電科技に譲渡"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[3]
    p.text = "• 住友化学園芸を大日本除虫菊に売却"
    p.font.size = Pt(16)
    p.space_after = Pt(24)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[4]
    p.text = "その他の主要案件"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)
    p.space_after = Pt(12)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[5]
    p.text = "• 田中藍ホールディングス：活材ケミカル（三井化学の子会社）を買収（2024年7月）"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[6]
    p.text = "• 昭光ハイポリマー：高分子商事の全株式を取得（2024年8月）"
    p.font.size = Pt(16)

    # Slide 8: 2025-2026年の展望
    slide8 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide8.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide8.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "2025-2026年の展望"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    content_box = slide8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame

    content_frame.text = "M&A市場の見通し"
    p = content_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)
    p.space_after = Pt(12)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[1]
    p.text = "• 金利のさらなる低下・安定化により、M&Aの急増が期待される"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[2]
    p.text = "• 企業は新製品発売とノンコア資産売却を通じたポートフォリオ再構築を加速"
    p.font.size = Pt(16)
    p.space_after = Pt(24)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[3]
    p.text = "予定されている主要案件"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)
    p.space_after = Pt(12)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[4]
    p.text = "• 大陽日酸：レゾナックグループから排ガス処理装置事業を取得（2025年6月完了予定）"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[5]
    p.text = "• 大日本塗料：神東塗料の株式約46%を取得（TOB終了：2025年3月10日）"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[6]
    p.text = "• 旭化成：旭化成エポキシと合併（2026年4月1日予定）"
    p.font.size = Pt(16)
    p.space_after = Pt(8)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[7]
    p.text = "• DuPont：アラミド事業売却完了（2026年Q1予定、約18億ドル）"
    p.font.size = Pt(16)

    # Slide 9: まとめ
    slide9 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide9.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    title_box = slide9.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "まとめ"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 51, 102)

    content_box = slide9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(8.4), Inches(5))
    content_frame = content_box.text_frame

    content_frame.text = "業界の主要トレンド"
    p = content_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 102, 204)
    p.space_after = Pt(12)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[1]
    p.text = "1. ポートフォリオ最適化：各社がノンコア事業を売却し、成長分野に資源を集中"
    p.font.size = Pt(16)
    p.space_after = Pt(10)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[2]
    p.text = "2. グローバル展開：M&Aを通じた海外市場への進出と現地化の推進"
    p.font.size = Pt(16)
    p.space_after = Pt(10)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[3]
    p.text = "3. サステナビリティ：グリーン技術、再生可能エネルギーへの投資が活発化"
    p.font.size = Pt(16)
    p.space_after = Pt(10)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[4]
    p.text = "4. 構造改革：特に日本企業で石化不況を受けた事業再編が進行中"
    p.font.size = Pt(16)
    p.space_after = Pt(10)

    content_frame.add_paragraph()
    p = content_frame.paragraphs[5]
    p.text = "5. 金利環境の改善：2025年以降、M&A市場の回復・拡大が期待される"
    p.font.size = Pt(16)

    # Save presentation
    prs.save('化学メーカー_事業とM&A実績.pptx')
    print("プレゼンテーションを作成しました: 化学メーカー_事業とM&A実績.pptx")

if __name__ == "__main__":
    create_presentation()
