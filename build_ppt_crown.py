# -*- coding: utf-8 -*-
"""乳牙预成冠修复术 · 讲解 PPT（16:9，含备注）。"""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

FIGS = 'figs_crown'
OUT = '乳牙预成冠修复术_讲解PPT.pptx'
EA = '微软雅黑'
DARK = '1F364D'
ACCENT = '0F5C8A'
GREY = '5F6770'
GREEN = '18643E'
RED = 'B03A2B'
BAND = 'EEF4F9'
LINE = 'D6E2EC'


def split(name, out_prefix, cuts):
    img = Image.open(os.path.join(FIGS, name))
    for i, (y0, y1) in enumerate(cuts, 1):
        img.crop((0, y0, img.width, min(y1, img.height))).save(
            os.path.join(FIGS, '%s_%d.png' % (out_prefix, i)))


split('fig01_overview.png', 'c01', [(10, 597), (593, 1180)])
split('fig08_dos_donts.png', 'c08', [(75, 700), (690, 1315)])
split('fig12_cases.png', 'c12', [(80, 632), (626, 1180)])

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
    ft.paragraphs[0].runs[0].text = '乳牙预成冠修复术 · 图解讲解'
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
tf = txbox(s, 0.9, 1.15, 11.5, 1.0)
set_font(tf.paragraphs[0].add_run(), 40, True, DARK)
tf.paragraphs[0].runs[0].text = '乳牙预成冠修复术'
tf = txbox(s, 0.9, 2.15, 11.5, 0.5)
set_font(tf.paragraphs[0].add_run(), 19, False, ACCENT)
tf.paragraphs[0].runs[0].text = '适应证 · 器械材料 · 操作步骤 · 禁忌证 · 病例举例'
tf = txbox(s, 0.9, 2.72, 11.5, 0.4)
set_font(tf.paragraphs[0].add_run(), 13, False, GREY)
tf.paragraphs[0].runs[0].text = '儿童口腔科 · 口腔全科　|　图解讲解版（配套图解手册使用）'
pic(s, 'fig02_ssc_structure.png', 0.9, 3.35, 3.8, 2.6)
pic(s, 'fig06_strip_crown.png', 4.8, 3.35, 3.8, 2.6)
pic(s, 'fig03_ssc_prep.png', 8.7, 3.35, 3.8, 2.6)
notes(s, '开场：预成冠是把乳牙“整体包起来”的保护性修复，本讲覆盖金属预成冠（SSC）、'
         '前牙透明树脂冠（条冠）、预成全瓷冠与 Hall 技术，并配 10 个病例。')

# ============================== 2 导览 ==============================
s = add_slide(); header(s, '内容导览', num=nxt())
bullets(s, ['冠类型总览与选择原则', '金属预成冠备牙标准与尺寸',
            '备牙步骤 · 选冠试戴 · 冠缘成形', '前牙透明树脂冠（条冠）',
            '操作流程与器械材料清单', '适应证与禁忌证（√ / ×）',
            '常见错误对照', '复诊维护、并发症与病例举例'],
        0.9, 1.5, 11.6, 4.5, size=17, gap=12)
takeaway(s, '一句话主线：能包就包、够用最小号、边缘要密合、咬合要调平。')
notes(s, '提醒：所有尺寸、参数为常用参考范围，须个体化。')

# ============================== 3-5 类型总览 ==============================
s = add_slide(); header(s, '冠类型总览（一）', '金属预成冠 · 前牙条冠 · 全瓷冠', num=nxt())
pic(s, 'c01_1.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '① SSC 乳磨牙首选　② 条冠前牙首选　③ 全瓷冠用于美学 / 金属过敏')
notes(s, 'SSC 用于乳磨牙多面龋、牙髓治疗后、高龋风险；条冠用于前牙龋、奶瓶龋、外伤；'
         '氧化锆全瓷冠用于美学要求或金属过敏。')

s = add_slide(); header(s, '冠类型总览（二）', 'Hall 技术 · 全冠丝圈式 · 多颗一次性修复', num=nxt())
pic(s, 'c01_2.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '④ Hall 不备牙直接粘　⑤ 全冠可作间隙保持基牙　⑥ 多颗可一次性完成')
notes(s, 'Hall 技术适用于乳磨牙龋损、无牙髓 / 根尖症状、可隔湿者；'
         '全冠丝圈式把“修复”与“间隙保持”合并；多颗一次性修复常在门诊镇静或全麻下完成。')

s = add_slide(); header(s, '冠类型速查', num=nxt())
table(s, [['类型', '一句话适应证', '常用位置'],
          ['① 金属预成冠（SSC）', '乳磨牙多面龋、牙髓治疗后、高龋风险', '乳磨牙'],
          ['② 前牙透明树脂冠（条冠）', '前牙龋、奶瓶龋、外伤冠折', '乳前牙'],
          ['③ 预成全瓷冠（氧化锆）', '美学要求、金属过敏', '乳前牙 / 乳磨牙'],
          ['④ Hall 技术', '无牙髓 / 根尖症状、可隔湿，少备牙', '乳磨牙'],
          ['⑤ 全冠丝圈式', '乳磨牙全冠 + 丝圈，兼作间隙保持', '乳磨牙'],
          ['⑥ 多颗一次性修复', '全麻 / 门诊下多象限、多颗同时修复', '全口']],
      [3.6, 6.4, 2.9], 0.8, 1.5, 11.7, size=13, row_h=0.72)
takeaway(s, '选型三要素：牙位（前 / 后）、有无牙髓症状、美学与过敏需求。')
notes(s, '把这张表和适应证 / 禁忌证对照讲，学员最容易记住。')

# ============================== 6-7 备牙标准 ==============================
s = add_slide(); header(s, '金属预成冠 · 备牙标准', '颊面观 + 咬合面观', num=nxt())
pic(s, 'fig02_ssc_structure.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '咬合面 1.0–1.5 mm · 邻面平行 / 微内聚 · 去倒凹 · 龈下 0.5–1.0 mm · 线角圆钝无肩台')
notes(s, '① 咬合面均匀预备 1.0–1.5 mm；② 邻面打开接触、平行或微内聚；'
         '③ 颊舌面去倒凹即可；④ 冠缘位于龈下 0.5–1.0 mm；⑤ 线角圆钝、无肩台；'
         '⑥ 选最小能完全就位的冠并修整颈缘。')

s = add_slide(); header(s, '备牙尺寸速查', num=nxt())
table(s, [['部位 / 环节', '标准', '要点'],
          ['咬合面预备', '1.0–1.5 mm', '均匀磨除，按解剖形态'],
          ['邻面预备', '打开接触，平行或微内聚', '避免形成倒凹'],
          ['颊舌面', '去倒凹即可', '不需大量预备'],
          ['冠缘位置', '龈下 0.5–1.0 mm', '不压龈、无悬突'],
          ['线角', '圆钝、无肩台', '无锐利边缘'],
          ['选冠', '最小能完全就位者', '有“回弹”手感']],
      [3.6, 4.6, 4.4], 0.8, 1.5, 11.7, size=13, row_h=0.72)
takeaway(s, '乳牙牙体小、牙髓腔大，备牙量不可过度，以“去倒凹 + 均匀磨除”为准。')
notes(s, '强调：乳牙牙髓腔大、角高，备牙过深易穿髓，应“宁少勿多”。')

# ============================== 8-10 步骤与试戴 ==============================
s = add_slide(); header(s, '备牙五步', num=nxt())
pic(s, 'fig03_ssc_prep.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '去龋 / 牙髓治疗 → 咬合面 → 邻面 → 颊舌面 → 完成（戴冠）')
notes(s, '五步：① 去龋、必要时牙髓治疗；② 咬合面预备 1.0–1.5 mm；③ 邻面打开接触；'
         '④ 颊舌面去倒凹、线角圆钝；⑤ 完成，冠缘位于龈下 0.5–1.0 mm。')

s = add_slide(); header(s, '选冠与试戴', '三个关键判断', num=nxt())
pic(s, 'fig04_tryin.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '太大不能就位 → 换小号；合适有“回弹”手感；太小过松 → 换大号')
notes(s, '选冠原则：选“最小能完全就位”的冠；完全就位后边缘位于龈下 0.5–1.0 mm、'
         '有弹性回抱感。')

s = add_slide(); header(s, '冠缘成形（crimping）', num=nxt())
pic(s, 'fig05_crimp.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '冠缘成形后贴紧牙颈、无悬突；未成形会悬突 → 菌斑、牙龈炎')
notes(s, '用成形钳把颈缘向内收、贴合牙颈部，再磨光边缘；悬突是带冠后牙龈炎最常见原因。')

# ============================== 11 前牙条冠 ==============================
s = add_slide(); header(s, '前牙透明树脂冠（条冠）', '操作四步', num=nxt())
pic(s, 'fig06_strip_crown.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '预备 → 选透明冠套 → 充填树脂就位 → 去套调合抛光')
notes(s, '切端预备 1.0–1.5 mm、邻面去倒凹、切角圆钝、龈下边缘 0.5–1.0 mm；'
         '树脂光照 / 自固化后去除纤维素冠套，调合、抛光。')

# ============================== 12 操作流程 ==============================
s = add_slide(); header(s, '操作流程', '含 Hall 技术', num=nxt())
pic(s, 'fig07_workflow.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '隔湿是成功关键；完全就位 · 无悬突 · 咬合无干扰 · 邻接恢复 · 去净多余粘接剂')
notes(s, '八步：评估麻醉 → 橡皮障去龋 → 牙髓治疗（必要时）→ 备牙 → 选冠试戴 → 冠缘成形 → '
         '粘接 → 医嘱复查。Hall 技术：不备牙 / 极少备牙直接粘接。')

# ============================== 13-14 步骤表与材料 ==============================
s = add_slide(); header(s, '操作步骤要点', num=nxt())
table(s, [['步骤', '操作要点'],
          ['1 评估 · 麻醉', '确认适应证、排除禁忌；局部麻醉'],
          ['2 橡皮障 · 去龋', '隔湿；去净龋坏、必要时行牙髓治疗'],
          ['3 牙髓治疗', '露髓或深龋近髓者，先行牙髓治疗'],
          ['4 备牙', '按备牙标准预备（Hall 技术可不备牙）'],
          ['5 选冠 · 试戴', '选最小能完全就位的冠；检查边缘、咬合、邻接'],
          ['6 冠缘成形', '成形钳内收颈缘，磨光边缘去悬突'],
          ['7 粘接', '玻璃离子 / 树脂加强玻璃离子，去净多余'],
          ['8 医嘱 · 复查', '检查咬合；清洁与饮食指导；每 6 个月复查']],
      [2.8, 8.9], 0.8, 1.45, 11.7, size=12.5, row_h=0.55)
takeaway(s, '每一步都能回答“怎么确认做对了”：就位、密合、无悬突、咬合调平、隔湿充分。')
notes(s, '强调：乳牙牙髓腔大，备牙“宁少勿多”；粘接前必须隔湿。')

s = add_slide(); header(s, '器械与材料清单', num=nxt())
table(s, [['环节', '材料与器械'],
          ['检查与麻醉', '检查盘、口镜 / 探针 / 镊子、麻醉注射器'],
          ['隔湿与去龋', '橡皮障、开口器、吸唾器、高速 / 低速手机、球钻、挖匙'],
          ['备牙', '金刚砂车针、裂钻、抛光车针'],
          ['冠与修整', '预成金属冠（各型号）、前牙透明冠套、预成全瓷冠、冠剪、成形钳、'
           '去冠器、咬合纸'],
          ['充填与粘接', '复合树脂（前牙）、玻璃离子 / 树脂加强玻璃离子水门汀'],
          ['防护与随访', '氟保护漆、抛光杯、复诊记录表、宣教资料']],
      [2.8, 8.9], 0.8, 1.5, 11.7, size=12.5, row_h=0.85)
takeaway(s, '材料清单可直接作为科室备物核对表使用。')
notes(s, '如需院内标准化，可把这张表改成科室备物卡，标注型号与供应商。')

# ============================== 15 适应证 / 禁忌证 ==============================
s = add_slide(); header(s, '适应证与禁忌证', num=nxt())
for x, w, title, col, bg, items in [
    (0.55, 6.0, '√ 适应证', GREEN, 'EAF6EF',
     ['乳磨牙多面龋（≥ 2 个牙面）',
      '乳牙牙髓治疗（根管治疗）后',
      '釉质发育不全、奶瓶龋广泛缺损',
      '高龋风险儿童、需长期保护',
      '间隙保持器的基牙',
      '外伤后牙体缺损',
      'Hall 技术：无牙髓症状、可隔湿',
      '全麻下多颗一次性修复']),
    (6.85, 5.93, '× 禁忌证 / 慎用', RED, 'FCF0EF',
     ['牙根吸收超过 1/3（接近替换）',
      '牙髓 / 根尖病变未控制',
      '无法隔湿、龈下缺损过深无法就位',
      '对金属过敏（改全瓷冠）',
      '临床冠高度不足、萌出不足',
      '需拔牙序列 / 综合正畸',
      '全身状况不允许（相对，可全麻）',
      '家长拒绝、无法配合复查'])]:
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
takeaway(s, '关键禁忌：牙根吸收 > 1/3、牙髓 / 根尖病变未控制、无法隔湿。')
notes(s, '重点强调：接近替换期（牙根吸收 >1/3）不做冠；牙髓病变未控制先治疗。')

# ============================== 16-17 常见错误 ==============================
s = add_slide(); header(s, '常见错误对照（一）', '冠颈缘 · 冠缘长度　（左对 · 右错）', num=nxt())
pic(s, 'c08_1.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '冠缘密合、龈下 0.5–1.0 mm；不悬突、不过短')
notes(s, '第一组：冠颈缘悬突是菌斑滞留与牙龈炎的主要来源；'
         '第二组：冠缘过短暴露牙体颈部 → 继发龋风险。')

s = add_slide(); header(s, '常见错误对照（二）', '邻接关系 · 咬合　（左对 · 右错）', num=nxt())
pic(s, 'c08_2.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '邻接恢复、无食物嵌塞；咬合均匀、无早接触')
notes(s, '第三组：邻接不良导致食物嵌塞；第四组：咬合过高造成早接触、'
         '冠脱落与对颌牙创伤。')

# ============================== 18 复诊时间轴 ==============================
s = add_slide(); header(s, '复诊与维护时间轴', num=nxt())
pic(s, 'fig09_timeline.png', 0.55, 1.55, 12.23, 3.6)
bullets(s, ['戴入后 1 周：咬合、组织、冠缘',
            '此后每 6 个月：检查松动、悬突、边缘密合与口腔卫生',
            '替换期：预成冠随乳牙自然脱落，一般不需常规拆除',
            '异常：穿孔、松动、继发龋 → 及时更换'],
        0.9, 5.05, 11.6, 1.2, size=13.5, gap=4)
takeaway(s, '预成冠一般“一戴到底”，随乳牙替换自然脱落；异常才更换。')
notes(s, '向家长强调：冠松动、脱落、牙龈红肿要复诊；换牙时冠会跟着乳牙一起掉。')

# ============================== 19 并发症 ==============================
s = add_slide(); header(s, '常见并发症与处理', num=nxt())
table(s, [['并发症', '常见原因', '处理'],
          ['冠脱落', '固位不足、粘接面污染、咬合过高', '重新粘接或调整咬合'],
          ['悬突、牙龈炎', '未做冠缘成形', '修整边缘、洁治'],
          ['咬合过高', '未调合', '调合至均匀接触'],
          ['邻接不良、食物嵌塞', '选冠不当 / 未成形', '更换或调整冠'],
          ['继发龋', '冠缘过短、粘接剂溶解', '更换、充填'],
          ['冠穿孔 / 磨损', '咬合力量大、使用过久', '更换']],
      [3.0, 4.6, 5.0], 0.8, 1.5, 11.7, size=12.5, row_h=0.72)
takeaway(s, '并发症的共同源头：适应证把握、隔湿、冠缘成形、调合与随访。')
notes(s, '预成冠本身成功率很高；多数并发症来自“边缘”和“咬合”两个环节。')

# ============================== 20 家长沟通 ==============================
s = add_slide(); header(s, '家长沟通要点（可直接照读）', num=nxt())
bullets(s, ['这个金属套是把整颗牙包起来，保护到换牙，防止再蛀。',
            '刷牙照常，重点刷冠和牙龈交界的地方；不要咬特别硬的东西。',
            '冠松了、掉了、牙龈肿了要及时回来；换牙时冠会跟着乳牙一起掉。'],
        0.9, 1.8, 11.6, 3.6, size=17, gap=16)
takeaway(s, '把“为什么包、怎么维护、出问题怎么办、什么时候掉”四件事讲清楚即可。')
notes(s, '建议把这段做成知情同意附页，家长签字前逐条讲解。')

# ============================== 21-24 病例 ==============================
s = add_slide(); header(s, '病例举例（一）', '典型病例示意：病例 1—2', num=nxt())
pic(s, 'c12_1.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '病例 1：乳磨牙多面龋 → SSC；病例 2：奶瓶龋前牙 → 条冠')
notes(s, '病例 1：5 岁 7 个月，85 多面龋、无牙髓症状 → 金属预成冠；'
         '病例 2：3 岁 6 个月，奶瓶龋、51/61 广泛龋坏 → 前牙透明树脂冠。')

s = add_slide(); header(s, '病例举例（二）', '典型病例示意：病例 3—4', num=nxt())
pic(s, 'c12_2.png', 0.55, 1.35, 12.23, 4.95)
takeaway(s, '病例 3：釉质发育不全 → 全瓷冠；病例 4：可隔湿邻面龋 → Hall 技术')
notes(s, '病例 3：6 岁 2 个月，釉质发育不全、前牙美学修复 → 氧化锆全瓷冠；'
         '病例 4：5 岁 11 个月，74 邻面龋、无牙髓症状、可隔湿 → Hall 技术不备牙直接粘接。')

s = add_slide(); header(s, '病例举例（三）', '病例 1—5 速查', num=nxt())
table(s, [['病例', '年龄 / 情况', '检查要点', '修复方式', '理由与要点'],
          ['1', '5 岁 7 个月，男；85 多面龋', '无牙髓 / 根尖症状', '金属预成冠（SSC）',
           '多面龋首选，全冠保护至替换'],
          ['2', '3 岁 6 个月，女；奶瓶龋', '51、61 广泛龋坏', '前牙透明树脂冠（条冠）',
           '前牙美学 + 功能恢复'],
          ['3', '6 岁 2 个月，女；釉质发育不全', '前牙形态 / 色泽异常', '预成全瓷冠（氧化锆）',
           '美学要求高、需牙色修复'],
          ['4', '5 岁 11 个月，男；74 邻面龋', '无牙髓症状，可隔湿', 'Hall 技术',
           '不备牙，直接粘接，患儿配合好'],
          ['5', '6 岁 5 个月，男；64 牙髓治疗后', '根管治疗完成、根尖无异常', '金属预成冠（SSC）',
           '牙髓治疗后常规全冠保护']],
      [0.8, 2.9, 2.7, 3.0, 3.2], 0.65, 1.45, 11.8, size=10.5, row_h=0.83)
takeaway(s, '病例 1—5：多面龋、奶瓶龋、发育不全、Hall 技术、牙髓治疗后。')
notes(s, '每个病例讲一句：为什么选这种冠？')

s = add_slide(); header(s, '病例举例（四）', '病例 6—10 速查', num=nxt())
table(s, [['病例', '年龄 / 情况', '检查要点', '修复方式', '理由与要点'],
          ['6', '4 岁 8 个月，女；高龋风险', '多牙面龋、口腔卫生一般', '多颗 SSC 一次性修复',
           '高龋风险，考虑全麻下完成'],
          ['7', '7 岁 2 个月，男；55 早失', '54 完好可作基牙', '全冠丝圈式',
           '全冠 + 丝圈，兼作间隙保持'],
          ['8', '5 岁 3 个月，女；61 外伤冠折', '未露髓、无根折', '前牙透明树脂冠（条冠）',
           '外伤后恢复外形与功能'],
          ['9', '6 岁 9 个月，男；金属过敏', '既往金属修复过敏史', '预成全瓷冠（氧化锆）',
           '金属过敏的替代方案'],
          ['10', '8 岁 1 个月，女；85 牙根吸收 >1/3', '接近替换期', '不做冠，观察 / 拔除',
           '禁忌证：冠无保留价值']],
      [0.8, 2.9, 2.7, 3.0, 3.2], 0.65, 1.45, 11.8, size=10.5, row_h=0.83)
takeaway(s, '病例 9、10 是“反例”：金属过敏改全瓷；牙根吸收 >1/3 不做冠。')
notes(s, '病例 9 提示金属过敏的替代方案；病例 10 提示接近替换期是预成冠的禁忌。')

# ============================== 25 小结 ==============================
s = add_slide(); header(s, '小结：术前 / 术中 / 术后', num=nxt())
bullets(s, ['术前：排除禁忌（牙根吸收 >1/3、根尖病变、金属过敏）；确认可隔湿；知情同意。',
            '术中：备牙宁少勿多；选最小能就位的冠；冠缘成形；粘接前隔湿；'
            '去净多余粘接剂；调合。',
            '术后：清洁与饮食指导；预约复查；病历记录冠型号与粘接材料。',
            'Hall 技术：无牙髓症状、可隔湿时可少备牙 / 不备牙。',
            '预成冠一般“一戴到底”，随乳牙替换自然脱落。'],
        0.9, 1.6, 11.6, 4.0, size=16, gap=14)
takeaway(s, '参考：儿童口腔医学与儿童口腔科临床操作教程、AAPD 儿童修复治疗指南、Hall 技术文献。')
notes(s, '结束语：预成冠本身不难，难在“选对人、备牙到位、边缘密合、咬合调平、随访到位”。')

prs.save(OUT)
print('slides =', len(prs.slides._sldIdLst))
print('saved', OUT)
