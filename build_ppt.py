# -*- coding: utf-8 -*-
"""把《图解手册》PDF 的内容做成 16:9 讲解 PPT。"""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

FIGS = 'figs'
OUT = '固定式间隙保持器与改良Nance弓_讲解PPT.pptx'
EA = '微软雅黑'
DARK = '1F364D'
ACCENT = '0F5C8A'
GREY = '5F6770'
GREEN = '18643E'
RED = 'B03A2B'
BAND = 'EEF4F9'
LINE = 'D6E2EC'

# ---------- 拆图：总览图拆成上下两半，便于单页展示 ----------
im = Image.open(os.path.join(FIGS, 'fig01_overview.png'))
im.crop((0, 10, im.width, 597)).save(os.path.join(FIGS, 'fig01_top.png'))
im.crop((0, 593, im.width, 1180)).save(os.path.join(FIGS, 'fig01_bottom.png'))


def split(name, out_prefix, cuts):
    """按 (y0, y1) 列表切分图片，输出 out_prefix_1..n.png。"""
    img = Image.open(os.path.join(FIGS, name))
    outs = []
    for i, (y0, y1) in enumerate(cuts, 1):
        p = os.path.join(FIGS, '%s_%d.png' % (out_prefix, i))
        img.crop((0, y0, img.width, min(y1, img.height))).save(p)
        outs.append('%s_%d.png' % (out_prefix, i))
    return outs


split('fig05_modified_nance.png', 'fig05', [(15, 612), (608, 1215)])
split('fig06_decision_flow.png', 'fig06', [(15, 578), (576, 1235)])
split('fig08_dos_donts.png', 'fig08', [(75, 700), (690, 1315)])
split('fig12_cases.png', 'fig12', [(80, 632), (626, 1180)])

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def set_font(run, size=None, bold=None, color=None, name=EA):
    f = run.font
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if color is not None:
        f.color.rgb = RGBColor.from_string(color)
    f.name = name
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = parse_xml('<a:ea xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
        rPr.insert_element_before(ea, 'a:cs', 'a:sym', 'a:hlinkClick',
                                  'a:hlinkMouseOver', 'a:rtl', 'a:extLst')
    ea.set('typeface', name)


def add_slide():
    return prs.slides.add_slide(BLANK)


def txbox(slide, x, y, w, h, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.paragraphs[0].alignment = align
    return tf


def header(slide, title, sub=None, num=None):
    tf = txbox(slide, 0.55, 0.26, 12.2, 0.72, anchor=MSO_ANCHOR.MIDDLE)
    set_font(tf.paragraphs[0].add_run(), 27, True, DARK)
    tf.paragraphs[0].runs[0].text = title
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(1.02),
                                 Inches(12.23), Inches(0.035))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor.from_string(LINE)
    bar.line.fill.background()
    bar.shadow.inherit = False
    if sub:
        t2 = txbox(slide, 0.55, 1.07, 12.2, 0.34)
        set_font(t2.paragraphs[0].add_run(), 13, False, ACCENT)
        t2.paragraphs[0].runs[0].text = sub
    ft = txbox(slide, 0.55, 7.08, 9.0, 0.3)
    set_font(ft.paragraphs[0].add_run(), 9.5, False, GREY)
    ft.paragraphs[0].runs[0].text = '固定式间隙保持器与改良 Nance 弓矫治器 · 图解讲解'
    if num is not None:
        nt = txbox(slide, 11.9, 7.08, 0.9, 0.3, align=PP_ALIGN.RIGHT)
        set_font(nt.paragraphs[0].add_run(), 9.5, False, GREY)
        nt.paragraphs[0].runs[0].text = str(num)


def takeaway(slide, text, color=DARK):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55),
                                 Inches(6.42), Inches(12.23), Inches(0.56))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor.from_string(BAND)
    box.line.fill.background()
    box.shadow.inherit = False
    box.adjustments[0] = 0.16
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = text
    set_font(r, 13.5, True, color)


def pic(slide, name, x, y, w, h):
    """按比例缩放到 (w,h) 框内并居中放置。"""
    path = os.path.join(FIGS, name)
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    slide.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2),
                             Inches(pw), Inches(ph))


def bullets(slide, items, x, y, w, h, size=15, gap=6, color='28323C', bullet='· '):
    tf = txbox(slide, x, y, w, h)
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(gap)
        r = p.add_run()
        r.text = bullet + it
        set_font(r, size, False, color)
    return tf


def table(slide, data, widths, x, y, w, size=11, head_size=11, row_h=0.34):
    rows, cols = len(data), len(data[0])
    shape = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w),
                                   Inches(row_h * rows))
    tbl = shape.table
    tbl.first_row = True
    total = sum(widths)
    for i, cw in enumerate(widths):
        tbl.columns[i].width = Inches(w * cw / total)
    for i, row in enumerate(data):
        tbl.rows[i].height = Inches(row_h)
        for j, txt in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run()
            r.text = txt
            if i == 0:
                set_font(r, head_size, True, 'FFFFFF')
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor.from_string(DARK)
            else:
                col = None
                if txt.startswith('√'):
                    col = GREEN
                elif txt.startswith('×'):
                    col = RED
                set_font(r, size, j == 0, col or '28323C')
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor.from_string(
                    'FFFFFF' if i % 2 else 'F5F8FB')
    return tbl


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


N = 0


def nxt():
    global N
    N += 1
    return N


# ============================== 1 封面 ==============================
s = add_slide()
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333),
                         Inches(0.22))
bar.fill.solid(); bar.fill.fore_color.rgb = RGBColor.from_string(ACCENT)
bar.line.fill.background(); bar.shadow.inherit = False

tf = txbox(s, 0.9, 1.15, 11.5, 1.0, align=PP_ALIGN.LEFT)
set_font(tf.paragraphs[0].add_run(), 40, True, DARK)
tf.paragraphs[0].runs[0].text = '固定式间隙保持器与改良 Nance 弓矫治器'
tf = txbox(s, 0.9, 2.15, 11.5, 0.5)
set_font(tf.paragraphs[0].add_run(), 19, False, ACCENT)
tf.paragraphs[0].runs[0].text = '适应证 · 器械材料 · 操作步骤 · 禁忌证 · 病例举例'
tf = txbox(s, 0.9, 2.72, 11.5, 0.4)
set_font(tf.paragraphs[0].add_run(), 13, False, GREY)
tf.paragraphs[0].runs[0].text = '儿童口腔科 · 口腔全科 · 早期矫治　|　图解讲解版（配套图解手册使用）'
pic(s, 'fig02_band_loop.png', 0.9, 3.35, 3.8, 2.6)
pic(s, 'fig03_lingual_arch.png', 4.8, 3.35, 3.8, 2.6)
pic(s, 'fig04_nance.png', 8.7, 3.35, 3.8, 2.6)
notes(s, '开场：本讲围绕两类装置——固定式间隙保持器（带环丝圈式、固定舌弓、Nance 腭弓）'
         '与改良 Nance 弓矫治器，覆盖适应证、器械材料、操作步骤、禁忌证，并配 10 个病例。')

# ============================== 2 导览 ==============================
s = add_slide(); header(s, '内容导览', num=nxt())
bullets(s, ['装置类型总览与选择原则', '结构与关键尺寸（丝径 / 带环 / 腭托 / 距组织距离）',
            '改良 Nance 弓：四种改良形式', '装置怎么选：决策流程 + 速查表',
            '操作步骤与器械材料清单', '适应证与禁忌证（√ / ×）',
            '常见错误对照与质量控制', '复诊维护、并发症与拆除时机',
            '10 个病例举例'], 0.9, 1.35, 11.6, 4.6, size=17, gap=10)
takeaway(s, '一句话主线：先判断“还能不能等”，再决定“单侧还是双侧、要不要加功能部件”。')
notes(s, '提醒学员：全部尺寸、力值、复诊间隔均为常用参考范围，须个体化。')

# ============================== 3-4 总览 ==============================
s = add_slide(); header(s, '装置类型总览（一）', '单侧缺隙与恒磨牙未萌的处理', num=nxt())
pic(s, 'fig01_top.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '① 带环丝圈式最常用　② 基牙条件差改全冠　③ 恒磨牙未萌用远端靴式')
notes(s, '带环丝圈式适用于单侧 1 个牙缺失、恒牙 6 个月内不能萌出；'
         '全冠丝圈式用于基牙大面积缺损或已做全冠；'
         '远端靴式用于第一恒磨牙未萌而第二乳磨牙早失，需引导恒磨牙萌出。')

s = add_slide(); header(s, '装置类型总览（二）', '双侧缺隙与需要早期矫治的情形', num=nxt())
pic(s, 'fig01_bottom.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '④ 双侧下颌→舌弓　⑤ 双侧上颌→Nance 腭弓　⑥ 需早期矫治→改良 Nance 弓')
notes(s, '舌弓与 Nance 腭弓解决跨中线、多牙缺失的间隙保持；'
         '改良 Nance 弓在保持基础上叠加推磨牙、前牵引或扩弓功能。')

# ============================== 5 类型速查表 ==============================
s = add_slide(); header(s, '装置类型速查', num=nxt())
table(s, [['类型', '一句话适应证', '支抗牙'],
          ['① 带环丝圈式', '单侧 1 个牙缺失，恒牙 6 个月内不能萌出', '缺隙远中邻牙'],
          ['② 全冠丝圈式', '基牙大面积缺损或已做全冠', '全冠修复的基牙'],
          ['③ 远端靴式', '第一恒磨牙未萌时第二乳磨牙早失', '第一乳磨牙'],
          ['④ 固定舌弓', '双侧下颌乳磨牙早失', '下颌第一恒磨牙'],
          ['⑤ Nance 腭弓', '双侧上颌乳磨牙早失', '上颌第一恒磨牙'],
          ['⑥ 改良 Nance 弓', '保持 + 早期矫治（推磨牙 / 前牵引 / 扩弓）',
           '上颌第一恒磨牙（可加骨支抗）']],
      [3.0, 6.4, 3.6], 0.8, 1.45, 11.7, size=12.5, row_h=0.66)
takeaway(s, '选择三要素：缺隙是单侧还是双侧、恒磨牙萌出程度、有无早期矫治目标。')
notes(s, '把这张表和后面的决策流程图对照讲，学员最容易记住。')

# ============================== 6-8 结构 ==============================
s = add_slide(); header(s, '带环丝圈式：结构要点', '颊面观 · 关键尺寸', num=nxt())
pic(s, 'fig02_band_loop.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '带环 0.12–0.18 mm　丝圈 0.8–0.9 mm　距牙龈 0.5–1.0 mm　近中端抵邻牙邻面')
notes(s, '① 带环完全就位、边缘密合无悬突；② 丝圈跨过缺隙、近中端抵于邻牙邻面外形高点，'
         '不进入倒凹；③ U 形曲提供调整余地；④ 丝圈距牙龈 0.5–1.0 mm，避免压龈与滞留菌斑。')

s = add_slide(); header(s, '固定舌弓：结构要点', '下颌 · 合面观', num=nxt())
pic(s, 'fig03_lingual_arch.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '带环 36 / 46　舌弓距舌侧牙龈 0.5–1.0 mm　U 形曲用于调整与适应生长')
notes(s, '双侧下颌乳磨牙早失的首选；舌弓中段的 U 形曲是后续调整间隙、适应牙弓生长的关键结构；'
         '避免压迫舌体与进入倒凹。')

s = add_slide(); header(s, 'Nance 腭弓：结构要点', '合面观 + 腭部矢状剖面', num=nxt())
pic(s, 'fig04_nance.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '腭弓 0.9–1.0 mm　距腭黏膜 0.5–1.0 mm　前腭托厚 2–3 mm、边缘圆钝、均匀贴合')
notes(s, '腭托组织面必须与腭黏膜均匀贴合、无高点；剖面图说明“距黏膜 0.5–1.0 mm”'
         '是腭弓钢丝与黏膜之间的距离，而腭托是贴合在黏膜上的。')

# ============================== 9 尺寸速查 ==============================
s = add_slide(); header(s, '常用尺寸与参数速查', num=nxt())
table(s, [['部位 / 环节', '常用范围', '要点'],
          ['带环厚度', '0.12–0.18 mm', '边缘密合、无悬突'],
          ['丝圈 / 舌弓钢丝', '0.8–0.9 mm', '刚性足够、便于调整'],
          ['腭弓钢丝', '0.9–1.0 mm', '贴合腭穹窿走行'],
          ['腭托厚度', '2–3 mm', '边缘圆钝、组织面均匀贴合'],
          ['装置距牙龈 / 黏膜', '0.5–1.0 mm', '不压迫、不进入倒凹'],
          ['推磨牙加力', '0.5–1.0 mm / 次', '每 4–6 周复诊'],
          ['前方牵引', '300–500 g/侧，向前下 15°–30°', '12–14 h/日'],
          ['保持型复查间隔', '3–6 个月', '间隙测量 + 装置检查']],
      [3.4, 4.4, 4.4], 0.8, 1.45, 11.7, size=12.5, row_h=0.53)
takeaway(s, '所有数字都是“常用范围”，必须结合年龄、牙列阶段与影像学表现个体化。')
notes(s, '强调力值过大可致牙根吸收、支抗丧失与装置脱落；力值不足则疗程延长、依从性下降。')

# ============================== 10-11 改良 Nance 弓 ==============================
s = add_slide(); header(s, '改良 Nance 弓（一）', '推磨牙向远中 · 前方牵引支抗', num=nxt())
pic(s, 'fig05_1.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '推簧 / 圈曲推磨牙向远中；带环焊颊面管或牵引钩配合面具前牵引')
notes(s, '① 推磨牙向远中：腭弓加圈曲或推簧，用于上颌第一恒磨牙异位萌出、早期 II 类；'
         '② 前方牵引支抗：带环焊颊面管或牵引钩，腭托分散反作用力，'
         '前牵引 300–500 g/侧、向前下 15°–30°、12–14 h/日。')

s = add_slide(); header(s, '改良 Nance 弓（二）', '扩弓—保持型 · 骨支抗 / 固位改良型', num=nxt())
pic(s, 'fig05_2.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '横向不足加螺旋扩弓器；需绝对支抗或基牙条件差时加微种植钉 / 改全冠')
notes(s, '③ 扩弓—保持：腭中缝加螺旋扩弓器，扩弓与间隙保持同步，注意加力节奏与腭中缝反应；'
         '④ 骨支抗 / 固位改良：腭部微种植钉提供绝对支抗，基牙大面积缺损时改全冠固位。')

s = add_slide(); header(s, '改良形式对照', num=nxt())
table(s, [['改良形式', '结构变化', '主要目的'],
          ['① 推磨牙向远中', '腭弓加圈曲 / 推簧，或焊远中向牵引臂',
           '上颌第一恒磨牙异位萌出、早期 II 类'],
          ['② 前方牵引支抗', '带环焊颊面管 / 牵引钩，腭托加大',
           '安氏 III 类上颌后缩的腭部支抗'],
          ['③ 扩弓—保持', '腭中缝加螺旋扩弓器', '横向不足合并间隙丧失'],
          ['④ 骨支抗 / 固位改良', '腭部微种植钉；基牙改全冠、加邻牙支托',
           '需绝对支抗或基牙条件差']],
      [3.2, 5.0, 4.0], 0.8, 1.6, 11.7, size=12.5, row_h=0.85)
takeaway(s, '改良的前提是“有明确的早期矫治目标”，否则用经典 Nance 腭弓即可。')
notes(s, '适应证把握：异位萌出越早干预越好；前牵引需能保证每日佩戴时间；'
         '扩弓要注意加力节奏与腭中缝反应。')

# ============================== 12 决策流程 ==============================
s = add_slide(); header(s, '装置怎么选（一）', '决策流程：能否等待 · 能否戴带环 · 单侧缺隙', num=nxt())
pic(s, 'fig06_1.png', 0.55, 1.30, 12.23, 5.0)
takeaway(s, '恒牙 6 个月内萌出 → 观察；第一恒磨牙未萌 → 远端靴式')
notes(s, '前两问：① 继承恒牙 6 个月内是否萌出？是则定期观察；'
         '② 第一恒磨牙是否已萌出、能否戴带环？否则改用远端靴式引导萌出。')

s = add_slide(); header(s, '装置怎么选（二）', '决策流程：双侧缺隙 · 早期矫治目标 · 卫生依从性', num=nxt())
pic(s, 'fig06_2.png', 0.55, 1.30, 12.23, 5.0)
takeaway(s, '单侧→丝圈式；双侧上颌→Nance 腭弓；双侧下颌→舌弓；有早期矫治目标→改良 Nance 弓')
notes(s, '后三问：③ 缺隙是单侧还是双侧（上颌 / 下颌）？④ 有无异位萌出、推磨牙、前牵引、'
         '扩弓等早期矫治目标？⑤ 口腔卫生与依从性能否达标？不达标先治龋、必要时改活动式。')

# ============================== 13 选择速查表 ==============================
s = add_slide(); header(s, '装置选择速查', num=nxt())
table(s, [['临床情形', '首选', '关键点'],
          ['单侧下颌第一乳磨牙早失，第二乳磨牙完好', '带环丝圈式', '带环于第二乳磨牙'],
          ['单侧第二乳磨牙早失，第一恒磨牙未萌', '远端靴式', '引导恒磨牙萌出，时机要求高'],
          ['双侧下颌乳磨牙早失', '固定舌弓', '支抗牙 36 / 46'],
          ['双侧上颌乳磨牙早失', 'Nance 腭弓', '腭托需均匀贴合'],
          ['上颌第一恒磨牙异位萌出', '改良 Nance 弓 + 推簧', '尽早干预，评估可否复位'],
          ['上颌后缩拟行前方牵引', '改良 Nance 弓 + 面具', '需保证每日佩戴时间'],
          ['上颌横向不足合并缺隙', '改良 Nance 弓 + 扩弓器', '扩弓与保持同步'],
          ['口腔卫生极差、龋病未控制', '先治龋 / 暂缓固定装置', '必要时改活动式']],
      [6.2, 3.2, 3.4], 0.8, 1.45, 11.7, size=11.5, row_h=0.55)
takeaway(s, '同一情形可能有多个可选方案，最终取决于基牙条件、卫生与依从性。')
notes(s, '可以用现场提问方式：给出情形，让学员说出选择与理由。')

# ============================== 14 操作流程 ==============================
s = add_slide(); header(s, '操作流程与关键点', '固定式保持器 / 改良 Nance 弓通用', num=nxt())
pic(s, 'fig07_steps.png', 0.55, 1.45, 12.23, 4.60)
takeaway(s, '隔湿是粘接成功的关键；丝圈与腭弓距组织 0.5–1.0 mm；腭托边缘圆钝、均匀贴合')
notes(s, '八步：术前评估 → 试带环 → 取模灌模 → 技工制作 → 试戴调整 → 粘接 → 医嘱宣教 → '
         '定期复查。加力型 4–6 周复诊，保持型 3–6 个月复查。')

# ============================== 15-16 步骤表与材料 ==============================
s = add_slide(); header(s, '操作步骤要点', num=nxt())
table(s, [['步骤', '操作要点'],
          ['1 术前评估', '影像判断恒牙发育阶段与萌出通道；测缺隙；查基牙与口腔卫生'],
          ['2 试带环', '就位、边缘密合无悬突、邻接恢复、咬合无干扰'],
          ['3 取模灌模', '带环随印模取出并牢固复位；超硬石膏灌制'],
          ['4 技工制作', '丝圈 / 舌弓 / 腭弓弯制 → 焊接带环 → 制作腭托 → 抛光'],
          ['5 试戴调整', '丝圈与腭弓距组织 0.5–1.0 mm；腭托均匀贴合；咬合无干扰'],
          ['6 粘接', '严格隔湿；完全就位；去净多余粘接剂；复查咬合'],
          ['7 医嘱宣教', '避免硬黏食物；重点清洁带环边缘、丝圈下方、腭托边缘'],
          ['8 定期复查', '保持型 3–6 个月；加力型 4–6 周；记录间隙测量值']],
      [2.8, 8.9], 0.8, 1.45, 11.7, size=12.5, row_h=0.55)
takeaway(s, '每一步都要能回答：“怎么确认做对了？”——就位、密合、避让、无干扰、隔湿。')
notes(s, '强调取模时带环必须牢固嵌于印模内，否则整个装置作废。')

s = add_slide(); header(s, '器械与材料清单', num=nxt())
table(s, [['环节', '材料与器械'],
          ['检查与取模', '检查盘、间隙测量尺、儿童托盘、藻酸盐印模材、超硬石膏、咬合蜡'],
          ['固位与粘接', '预成不锈钢带环、预成不锈钢全冠、玻璃离子 / 树脂加强玻璃离子、'
           '正畸粘接剂、开口器与吸唾器'],
          ['技工制作', '不锈钢丝 0.8 / 0.9 / 1.0 mm、梯形钳、三喙钳、断丝钳、点焊机、'
           '银焊与焊媒、腭托树脂、打磨抛光器材'],
          ['改良部件', '螺旋扩弓器、颊面管、牵引钩、推簧、镍钛丝、前方牵引面具与橡皮圈、'
           '（可选）腭部微种植钉'],
          ['防护与随访', '氟保护漆 / 含氟涂料、根尖片与曲面体层片、复诊记录表、宣教资料']],
      [2.8, 8.9], 0.8, 1.55, 11.7, size=12.5, row_h=0.9)
takeaway(s, '材料清单可直接作为科室备物核对表使用。')
notes(s, '如需院内标准化，可把这张表改成科室备物卡，标注型号与供应商。')

# ============================== 17 适应证 / 禁忌证 ==============================
s = add_slide(); header(s, '适应证与禁忌证', num=nxt())
for x, w, title, col, bg, items in [
    (0.55, 6.0, '√ 适应证', GREEN, 'EAF6EF',
     ['乳磨牙早失，恒牙 6 个月内不能萌出',
      '单侧 1 牙缺失（带环 / 全冠丝圈式）',
      '双侧缺隙（舌弓 / Nance 腭弓）',
      '第一恒磨牙未萌 + 第二乳磨牙早失（远端靴式）',
      '先天缺牙需维持间隙',
      '依从性差，不宜活动式装置',
      '需加强支抗（推磨牙 / 前牵引 / 扩弓）',
      '磨牙异位萌出的早期阻断']),
    (6.85, 5.93, '× 禁忌证 / 慎用', RED, 'FCF0EF',
     ['继承恒牙即将萌出（牙根 > 2/3）',
      '龋病、牙髓病未控制',
      '口腔卫生极差、高龋活性',
      '基牙牙冠高度 / 形态不足',
      '腭穹窿过浅、腭部瘢痕或感觉障碍',
      '对镍铬 / 不锈钢过敏',
      '无法定期复诊',
      '需综合正畸 / 拔牙矫治；面具佩戴时间无法保证'])]:
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.35),
                             Inches(w), Inches(4.9))
    box.fill.solid(); box.fill.fore_color.rgb = RGBColor.from_string(bg)
    box.line.color.rgb = RGBColor.from_string(col)
    box.line.width = Pt(1.0)
    box.shadow.inherit = False
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.22); tf.margin_right = Inches(0.16)
    tf.margin_top = Inches(0.16)
    p = tf.paragraphs[0]
    p.space_after = Pt(8)
    r = p.add_run(); r.text = title
    set_font(r, 17, True, col)
    for it in items:
        p = tf.add_paragraph()
        p.space_after = Pt(5)
        r = p.add_run(); r.text = '· ' + it
        set_font(r, 12, False, '28323C')
takeaway(s, '禁忌证多半是“先处理再评估”：先把龋病与卫生问题解决，再谈装置。')
notes(s, '重点强调：恒牙即将萌出时上装置会阻碍萌出；卫生极差者优先改活动式或暂缓。')

# ============================== 18 常见错误 ==============================
s = add_slide(); header(s, '常见错误对照（一）', '丝圈距龈 · 腭托贴合　（左对 · 右错）', num=nxt())
pic(s, 'fig08_1.png', 0.55, 1.30, 12.23, 5.0)
takeaway(s, '丝圈距牙龈 0.5–1.0 mm；腭托组织面均匀贴合、无高点')
notes(s, '第一组：丝圈压龈会引起牙龈红肿、退缩；第二组：腭托局部高点会造成压迫性溃疡、'
         '发音不适与患儿拒戴，需缓冲调磨或重做。')

s = add_slide(); header(s, '常见错误对照（二）', '丝圈与邻牙 · 带环边缘　（左对 · 右错）', num=nxt())
pic(s, 'fig08_2.png', 0.55, 1.30, 12.23, 5.0)
takeaway(s, '丝圈抵于邻面外形高点，不进入倒凹；带环边缘密合、无悬突')
notes(s, '第三组：丝圈进入倒凹不仅压龈，还无法就位、易变形；'
         '第四组：带环悬突是菌斑滞留与带环下脱矿的主要来源。')

# ============================== 19 复诊时间轴 ==============================
s = add_slide(); header(s, '复诊与维护时间轴', num=nxt())
pic(s, 'fig09_timeline.png', 0.55, 1.55, 12.23, 3.6)
bullets(s, ['戴入后 1 周：装置稳定性、组织反应、咬合与卫生',
            '1 个月：适应情况、基牙与软组织',
            '保持型：每 3–6 个月复查；加力型：每 4–6 周复诊加力',
            '每次复诊记录间隙测量值、装置状态与处理措施'],
        0.9, 5.05, 11.6, 1.2, size=13.5, gap=4)
takeaway(s, '脱落后未及时处理，是间隙保持失败最常见的原因。')
notes(s, '向家长强调：装置松动、变形、压牙龈要尽快复诊，不要自己掰。')

# ============================== 20 并发症 ==============================
s = add_slide(); header(s, '常见并发症与处理', num=nxt())
table(s, [['并发症', '常见原因', '处理'],
          ['带环松动 / 脱落', '隔湿不良、咬合力过大、基牙条件差',
           '重新粘固；反复脱落改全冠或换设计'],
          ['丝圈变形、压龈', '外力、制作不当、邻牙萌出', '口内调整或重做，解除压迫'],
          ['腭托压迫溃疡', '组织面不贴合、树脂过多', '缓冲调磨；必要时重做腭托'],
          ['牙龈炎、带环下脱矿', '卫生维护差、滞留区', '洁治 + 用氟 + 强化宣教；必要时拆除'],
          ['牙髓症状 / 牙根吸收', '矫治力过大、移动过快', '停止加力或拆除，评估牙髓'],
          ['间隙保持失败', '脱落未复诊、设计不当', '重新评估，必要时正畸会诊']],
      [3.0, 4.6, 5.0], 0.8, 1.5, 11.7, size=12, row_h=0.72)
takeaway(s, '并发症的共同源头：适应证把握、隔湿质量、组织避让与随访依从性。')
notes(s, '带环下脱矿是固定式装置最需要预防的医源性损害，氟化物与菌斑控制是关键。')

# ============================== 21 家长沟通 ==============================
s = add_slide(); header(s, '家长沟通要点（可直接照读）', num=nxt())
bullets(s, ['这个装置是“占位”的：乳牙早掉，旁边的牙会倒过来占掉恒牙的位置。',
            '不要咬硬糖、冰块、黏性食物；刷牙要重点刷装置边缘和金属圈下面。',
            '装置松动、变形、牙龈被压红或孩子喊疼，请尽快来医院，不要自己掰。',
            '按预约复查；恒牙长到位置或开始做矫正时，就把它取下来。'],
        0.9, 1.8, 11.6, 3.6, size=17, gap=16)
takeaway(s, '把“为什么戴、戴多久、什么时候来、出问题怎么办”四件事讲清楚即可。')
notes(s, '建议把这段做成知情同意附页，家长签字前逐条讲解。')

# ============================== 22 拆除时机 ==============================
s = add_slide(); header(s, '拆除时机', '影像学 + 临床', num=nxt())
pic(s, 'fig11_removal.png', 0.55, 1.40, 12.23, 4.9)
takeaway(s, '牙根形成 ≥ 2/3、骨覆盖消失、邻接建立 → 拆除；否则继续戴')
notes(s, '拆除前拍摄影像确认继承恒牙位置与萌出状态，避免过早拆除导致间隙再度丧失；'
         '拆除后仍需定期随访。')

# ============================== 23-25 病例 ==============================
s = add_slide(); header(s, '病例举例（一）', '典型病例示意：病例 1—2', num=nxt())
pic(s, 'fig12_1.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '红圈 = 缺隙；病例 1 单侧缺隙 → 带环丝圈式；病例 2 双侧缺隙 → Nance 腭弓')
notes(s, '病例 1：6 岁 4 个月，74 因龋拔除、75 完好 → 带环于 75，丝圈抵 73；'
         '病例 2：7 岁 1 个月，55、65 早失 → Nance 腭弓，跨中线同时保持双侧。')

s = add_slide(); header(s, '病例举例（二）', '典型病例示意：病例 3—4', num=nxt())
pic(s, 'fig12_2.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '红箭头 = 加力方向；异位萌出用推簧，上颌后缩用前牵引')
notes(s, '病例 3：7 岁 8 个月，16 异位萌出（可复性）→ 改良 Nance 弓 + 推簧；'
         '病例 4：8 岁 2 个月，上颌后缩、安氏 III 类 → 改良 Nance 弓 + 颊面管 + 面具。')

s = add_slide(); header(s, '病例举例（三）', '病例 1—5 速查', num=nxt())
table(s, [['病例', '年龄 / 情况', '影像与检查', '装置选择', '理由与要点'],
          ['1', '6 岁 4 个月，男；74 因龋拔除', '75 完好；恒牙距萌出 > 1 年',
           '带环丝圈式（带环于 75）', '单侧单牙缺失；丝圈抵 73'],
          ['2', '7 岁 1 个月，女；55、65 早失', '腭穹窿较深；16、26 已萌',
           'Nance 腭弓', '跨中线保持双侧；腭托提供支抗'],
          ['3', '7 岁 8 个月，男；16 异位萌出', '可复性嵌顿，牙根约 1/2',
           '改良 Nance 弓 + 推簧', '早期阻断，避免间隙进一步丧失'],
          ['4', '8 岁 2 个月，女；上颌后缩、反合', 'ANB < 0°，上颌后缩',
           '改良 Nance 弓 + 颊面管 + 面具', '腭部支抗 + 前牵引 300–500 g/侧'],
          ['5', '5 岁 10 个月，女；85 早失', '46 尚未萌出，骨覆盖完整',
           '远端靴式', '引导 46 萌出；拔牙前取模']],
      [0.8, 3.0, 2.7, 2.9, 3.2], 0.65, 1.45, 11.8, size=10.5, row_h=0.83)
takeaway(s, '病例 1—5：单侧、双侧、异位萌出、骨性因素、恒磨牙未萌，覆盖四类适应证。')
notes(s, '每个病例讲一句：为什么不是别的装置？')

s = add_slide(); header(s, '病例举例（四）', '病例 6—10 速查', num=nxt())
table(s, [['病例', '年龄 / 情况', '影像与检查', '装置选择', '理由与要点'],
          ['6', '6 岁 8 个月，男；75、85 早失', '36、46 已萌，牙冠条件好',
           '固定舌弓', '下颌多牙缺失，保持牙弓长度'],
          ['7', '9 岁，女；上颌横向不足 + 55 早失', '后牙反合，上颌宽度不足',
           '改良 Nance 弓 + 螺旋扩弓器', '扩弓与保持同步，注意加力节奏'],
          ['8', '8 岁 6 个月，男；75 早失，36 已萌', '36 完全萌出，牙冠高度足够',
           '带环丝圈式（带环于 36）', '恒磨牙已萌，固位可靠、制作简单'],
          ['9', '7 岁 3 个月，男；74 早失、多牙龋坏', '口腔卫生极差，多牙需治疗',
           '先治龋 + 卫生指导，暂缓固定装置', '卫生与依从性不达标，必要时改活动式'],
          ['10', '6 岁 2 个月，女；65 早失 + 腭部瘢痕', '腭穹窿浅，腭部术后瘢痕',
           '改带环丝圈式（单侧）', 'Nance 腭托易压迫、脱位，应回避']],
      [0.8, 3.0, 2.7, 2.9, 3.2], 0.65, 1.45, 11.8, size=10.5, row_h=0.83)
takeaway(s, '病例 9、10 是“反例”：装置选择之前，先解决卫生、龋病与解剖条件。')
notes(s, '病例 9 提示口腔卫生是固定式装置的前提；病例 10 提示腭部条件决定 Nance 系列能否使用。')

# ============================== 26 小结 ==============================
s = add_slide(); header(s, '小结：术前 / 术中 / 术后', num=nxt())
bullets(s, ['术前：影像确认恒牙发育阶段；测量缺隙；评估基牙与菌斑；完成龋病治疗；知情同意。',
            '术中：带环完全就位无悬突；焊点牢固；丝圈 / 腭弓距组织 0.5–1.0 mm；'
            '腭托贴合；咬合无干扰；隔湿充分。',
            '术后：清洁方法示范并让家长复述；交代饮食禁忌；预约复查；病历记录材料规格。',
            '改良 Nance 弓：目标明确才加部件，加力后按期复诊并影像随访。',
            '拆除：牙根 ≥ 2/3、骨覆盖消失、邻接建立时拆除，拆除后仍需随访。'],
        0.9, 1.6, 11.6, 4.0, size=16, gap=14)
takeaway(s, '参考依据：儿童间隙保持器临床应用指南、儿童口腔医学与口腔正畸学教材、AAPD 相关规范。')
notes(s, '结束语：装置本身不难，难在“选对人、做密合、盯得住”。')

prs.save(OUT)
print('slides =', len(prs.slides.__iter__.__self__._sldIdLst))
print('saved', OUT)
