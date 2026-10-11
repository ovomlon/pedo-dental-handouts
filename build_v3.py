# -*- coding: utf-8 -*-
"""乳牙预成冠修复术 · 图解临床手册（少文字、多图、多举例）。生成 DOCX。"""
import os
import datetime
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BODY_EA = '宋体'
HEAD_EA = '微软雅黑'
BODY_ASCII = 'Times New Roman'
HEAD_ASCII = 'Arial'
DARK = RGBColor(0x1F, 0x36, 0x4D)
ACCENT = RGBColor(0x0F, 0x5C, 0x8A)
GREY = RGBColor(0x5F, 0x67, 0x70)
RED = RGBColor(0xB0, 0x3A, 0x2B)
FIGS = 'figs_crown'
TODAY = datetime.date.today().strftime('%Y-%m-%d')


def set_run(run, size=10.5, ea=BODY_EA, ascii_f=BODY_ASCII, bold=False, color=None):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = ascii_f
    if color is not None:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    for k in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rFonts.set(qn(k), ascii_f)
    rFonts.set(qn('w:eastAsia'), ea)
    return run


def style_font(style, size, ea, ascii_f, bold=False, color=None):
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.name = ascii_f
    if color is not None:
        style.font.color.rgb = color
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    for k in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rFonts.set(qn(k), ascii_f)
    rFonts.set(qn('w:eastAsia'), ea)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)


def cell_margins(cell, top=50, bottom=50, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for tag, val in (('top', top), ('start', left), ('bottom', bottom), ('end', right)):
        node = OxmlElement('w:' + tag)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        mar.append(node)
    tcPr.append(mar)


def add_field(paragraph, instr, size=9):
    run = paragraph.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = instr
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    set_run(run, size=size)


def make_styles(doc):
    st = doc.styles
    style_font(st['Normal'], 10.5, BODY_EA, BODY_ASCII)

    def mk(name, size, ea, ascii_f, bold, color, before, after, line=1.35,
           left=0.0, keep_next=False):
        s = st.add_style(name, 1)
        s.base_style = st['Normal']
        style_font(s, size, ea, ascii_f, bold, color)
        pf = s.paragraph_format
        pf.space_before = Pt(before)
        pf.space_after = Pt(after)
        pf.line_spacing = line
        if left:
            pf.left_indent = Cm(left)
        if keep_next:
            s.paragraph_format.keep_with_next = True
        return s

    mk('T-Title', 19, HEAD_EA, HEAD_ASCII, True, DARK, 0, 6, 1.15)
    mk('T-Sub', 12, HEAD_EA, HEAD_ASCII, False, ACCENT, 0, 4, 1.2)
    mk('T-H1', 14.5, HEAD_EA, HEAD_ASCII, True, DARK, 14, 6, 1.2, keep_next=True)
    mk('T-H2', 11.5, HEAD_EA, HEAD_ASCII, True, ACCENT, 9, 4, 1.2, keep_next=True)
    mk('T-Body', 10.5, BODY_EA, BODY_ASCII, False, None, 0, 4, 1.35)
    mk('T-Bul', 10.5, BODY_EA, BODY_ASCII, False, None, 0, 2, 1.3, left=0.7)
    mk('T-Cap', 9, HEAD_EA, HEAD_ASCII, False, GREY, 2, 8, 1.2)
    mk('T-TblHead', 9, HEAD_EA, HEAD_ASCII, True, RGBColor(0xFF, 0xFF, 0xFF), 0, 0, 1.15)
    mk('T-TblCell', 9, BODY_EA, BODY_ASCII, False, None, 0, 0, 1.18)
    mk('T-Note', 9.5, BODY_EA, BODY_ASCII, False, GREY, 3, 5, 1.3, left=0.4)


doc = Document()
make_styles(doc)
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.top_margin = sec.bottom_margin = Cm(1.8)
sec.left_margin = sec.right_margin = Cm(2.0)
sec.header_distance = Cm(1.1)
sec.footer_distance = Cm(0.9)

hp = sec.header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(hp.add_run('乳牙预成冠修复术 · 图解临床手册'), size=8.5, ea=HEAD_EA,
        ascii_f=HEAD_ASCII, color=GREY)
pPr = hp._p.get_or_add_pPr()
pbdr = OxmlElement('w:pBdr')
bot = OxmlElement('w:bottom')
for k, v in (('w:val', 'single'), ('w:sz', '4'), ('w:space', '2'), ('w:color', 'BFBFBF')):
    bot.set(qn(k), v)
pbdr.append(bot)
pPr.insert_element_before(pbdr, 'w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku',
                          'w:wordWrap', 'w:overflowPunct', 'w:topLinePunct',
                          'w:autoSpaceDE', 'w:autoSpaceDN', 'w:bidi',
                          'w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind',
                          'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap',
                          'w:jc', 'w:textDirection', 'w:textAlignment',
                          'w:textboxTightWrap', 'w:outlineLvl', 'w:divId', 'w:cnfStyle',
                          'w:rPr', 'w:sectPr', 'w:pPrChange')
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(fp.add_run('第 '), size=9)
add_field(fp, 'PAGE')
set_run(fp.add_run(' 页 / 共 '), size=9)
add_field(fp, 'NUMPAGES')
set_run(fp.add_run(' 页　|　图解手册 · 临床参考'), size=8.5, color=GREY)


def H1(t):
    p = doc.add_paragraph(style='T-H1')
    set_run(p.add_run(t))
    return p


def H2(t):
    p = doc.add_paragraph(style='T-H2')
    set_run(p.add_run(t))
    return p


def P(t, size=10.5, color=None, bold=False):
    p = doc.add_paragraph(style='T-Body')
    set_run(p.add_run(t), size=size, color=color, bold=bold)
    return p


def BUL(t):
    p = doc.add_paragraph(style='T-Bul')
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.first_line_indent = Cm(-0.35)
    set_run(p.add_run('· ' + t))
    return p


def IMG(path, width_cm=16.6, caption=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(1)
    p.add_run().add_picture(os.path.join(FIGS, path), width=Cm(width_cm))
    if caption:
        c = doc.add_paragraph(style='T-Cap')
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(c.add_run(caption), size=9, ea=HEAD_EA, ascii_f=HEAD_ASCII, color=GREY)


def TABLE(cols, widths, rows, first_bold=False, size=9):
    t = doc.add_table(rows=1, cols=len(cols))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, c in enumerate(cols):
        cell = t.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_run(p.add_run(c), size=size, ea=HEAD_EA, ascii_f=HEAD_ASCII, bold=True,
                color=RGBColor(0xFF, 0xFF, 0xFF))
        shade(cell, '1F364D')
        cell_margins(cell)
    for r in rows:
        cells = t.add_row().cells
        for i, txt in enumerate(r):
            cells[i].text = ''
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            bold = first_bold and i == 0
            col = None
            if txt.startswith('√'):
                col = RGBColor(0x18, 0x64, 0x3E)
            elif txt.startswith('×'):
                col = RED
            set_run(p.add_run(txt), size=size, bold=bold, color=col)
            cell_margins(cells[i])
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ============================== 封面 ==============================
p = doc.add_paragraph(style='T-Title')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run('乳牙预成冠修复术'), size=19, ea=HEAD_EA, ascii_f=HEAD_ASCII,
        bold=True, color=DARK)
p = doc.add_paragraph(style='T-Sub')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run('图解临床手册　·　适应证 / 器械材料 / 操作步骤 / 禁忌证 / 病例举例'),
        size=12, ea=HEAD_EA, ascii_f=HEAD_ASCII, color=ACCENT)
p = doc.add_paragraph(style='T-Cap')
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_run(p.add_run('儿童口腔科 · 口腔全科　|　版本 %s' % TODAY), size=9, ea=HEAD_EA,
        ascii_f=HEAD_ASCII, color=GREY)

IMG('fig01_overview.png', 16.6, '图 1　乳牙预成冠的主要类型与适用场景（①—⑥）')

TABLE(['类型', '一句话适应证', '常用位置'],
      [3.6, 9.4, 3.6],
      [['① 金属预成冠（SSC）', '乳磨牙多面龋、牙髓治疗后、高龋风险', '乳磨牙'],
       ['② 前牙透明树脂冠（条冠）', '前牙龋、奶瓶龋、外伤冠折', '乳前牙'],
       ['③ 预成全瓷冠（氧化锆）', '美学要求、金属过敏', '乳前牙 / 乳磨牙'],
       ['④ Hall 技术', '无牙髓 / 根尖症状、可隔湿，少备牙', '乳磨牙'],
       ['⑤ 全冠丝圈式', '乳磨牙全冠 + 丝圈，兼作间隙保持', '乳磨牙'],
       ['⑥ 多颗一次性修复', '全麻 / 门诊下多象限、多颗同时修复', '全口']],
      first_bold=True)

# ============================== 1 备牙标准 ==============================
doc.add_page_break()
H1('1　金属预成冠 · 备牙标准')
IMG('fig02_ssc_structure.png', 16.6, '图 2　金属预成冠结构要点与备牙标准（颊面观 + 咬合面观）')
H2('备牙尺寸速查')
TABLE(['部位 / 环节', '标准', '要点'],
      [4.0, 6.2, 6.4],
      [['咬合面预备', '1.0–1.5 mm', '均匀磨除，按解剖形态'],
       ['邻面预备', '打开接触，平行或微内聚', '避免形成倒凹'],
       ['颊舌面', '去倒凹即可', '不需大量预备'],
       ['冠缘位置', '龈下 0.5–1.0 mm', '不压龈、无悬突'],
       ['线角', '圆钝、无肩台', '无锐利边缘'],
       ['选冠', '最小能完全就位者', '有“回弹”手感']],
      first_bold=True)

# ============================== 2 备牙步骤 ==============================
H1('2　金属预成冠 · 备牙步骤')
IMG('fig03_ssc_prep.png', 16.6, '图 3　备牙五步：去龋 / 牙髓治疗 → 咬合面 → 邻面 → 颊舌面 → 完成')

# ============================== 3 选冠与试戴 / 冠缘成形 ==============================
H1('3　选冠、试戴与冠缘成形')
IMG('fig04_tryin.png', 16.6, '图 4　选冠与试戴：太大 / 合适 / 太小三个判断')
IMG('fig05_crimp.png', 16.6, '图 5　冠缘成形（crimping）与修整：避免悬突')

# ============================== 4 前牙条冠 ==============================
H1('4　前牙透明树脂冠（条冠）')
IMG('fig06_strip_crown.png', 16.6, '图 6　条冠四步：预备 → 选冠套 → 充填树脂就位 → 去套抛光')
P('切端预备 1.0–1.5 mm；邻面去倒凹；切角圆钝；冠缘位于龈下 0.5–1.0 mm。'
  '树脂充填后光照固化（或自固化），去除纤维素冠套后调合、抛光。', size=10.5)

# ============================== 5 操作流程与材料 ==============================
doc.add_page_break()
H1('5　操作流程与器械材料')
IMG('fig07_workflow.png', 16.6, '图 7　预成冠修复操作流程（含 Hall 技术）')
TABLE(['步骤', '操作要点'],
      [3.4, 13.2],
      [['1 评估 · 麻醉', '确认适应证、排除禁忌；局部麻醉'],
       ['2 橡皮障 · 去龋', '隔湿；去净龋坏、必要时行牙髓治疗'],
       ['3 牙髓治疗', '露髓或深龋近髓者，先行牙髓治疗'],
       ['4 备牙', '按图 2 标准预备（Hall 技术可不备牙）'],
       ['5 选冠 · 试戴', '选最小能完全就位的冠；检查边缘、咬合、邻接'],
       ['6 冠缘成形', '成形钳内收颈缘，磨光边缘去悬突'],
       ['7 粘接', '玻璃离子 / 树脂加强玻璃离子水门汀，去净多余'],
       ['8 医嘱 · 复查', '检查咬合；清洁与饮食指导；每 6 个月复查']],
      first_bold=True)
H2('器械与材料清单')
TABLE(['环节', '材料与器械'],
      [3.4, 13.2],
      [['检查与麻醉', '检查盘、口镜 / 探针 / 镊子、麻醉注射器'],
       ['隔湿与去龋', '橡皮障、开口器、吸唾器、高速 / 低速手机、球钻、挖匙'],
       ['备牙', '金刚砂车针、裂钻、抛光车针'],
       ['冠与修整', '预成金属冠（各型号）、前牙透明冠套、预成全瓷冠、'
        '冠剪、成形钳、去冠器、咬合纸'],
       ['充填与粘接', '复合树脂（前牙）、玻璃离子 / 树脂加强玻璃离子水门汀'],
       ['防护与随访', '氟保护漆、抛光杯、复诊记录表、宣教资料']],
      first_bold=True)

# ============================== 6 适应证 / 禁忌证 ==============================
doc.add_page_break()
H1('6　适应证与禁忌证')
TABLE(['√ 适应证', '× 禁忌证 / 慎用'],
      [8.3, 8.3],
      [['√ 乳磨牙多面龋（≥ 2 个牙面）', '× 牙根吸收超过 1/3（接近替换）'],
       ['√ 乳牙牙髓治疗（根管治疗）后', '× 牙髓 / 根尖病变未控制'],
       ['√ 釉质发育不全、奶瓶龋广泛缺损', '× 无法隔湿、龈下缺损过深无法就位'],
       ['√ 高龋风险儿童、需长期保护', '× 对金属过敏（改全瓷冠）'],
       ['√ 间隙保持器的基牙', '× 临床冠高度不足、萌出不足'],
       ['√ 外伤后牙体缺损', '× 需拔牙序列 / 综合正畸'],
       ['√ Hall 技术：无牙髓症状、可隔湿', '× 全身状况不允许（相对，可全麻）'],
       ['√ 全麻下多颗一次性修复', '× 家长拒绝、无法配合复查']],
      size=9)
IMG('fig08_dos_donts.png', 16.6, '图 8　常见错误对照（左列正确 · 右列错误）')

# ============================== 7 复诊与并发症 ==============================
H1('7　复诊、维护与并发症')
IMG('fig09_timeline.png', 16.6, '图 9　复诊与维护时间轴')
TABLE(['并发症', '常见原因', '处理'],
      [3.4, 6.2, 7.0],
      [['冠脱落', '固位不足、粘接面污染、咬合过高', '重新粘接或调整咬合'],
       ['悬突、牙龈炎', '未做冠缘成形', '修整边缘、洁治'],
       ['咬合过高', '未调合', '调合至均匀接触'],
       ['邻接不良、食物嵌塞', '选冠不当 / 未成形', '更换或调整冠'],
       ['继发龋', '冠缘过短、粘接剂溶解', '更换、充填'],
       ['冠穿孔 / 磨损', '咬合力量大、使用过久', '更换']],
      first_bold=True)
H2('家长沟通要点（可直接照读）')
BUL('这个金属套是把整颗牙包起来，保护到换牙，防止再蛀。')
BUL('刷牙照常，重点刷冠和牙龈交界的地方；不要咬特别硬的东西。')
BUL('冠松了、掉了、牙龈肿了要及时回来；换牙时冠会跟着乳牙一起掉。')

# ============================== 8 病例举例 ==============================
doc.add_page_break()
H1('8　病例举例')
IMG('fig12_cases.png', 16.6, '图 10　四个典型病例示意')
TABLE(['病例', '年龄 / 情况', '检查要点', '修复方式', '理由与要点'],
      [1.5, 3.4, 3.6, 3.4, 4.7],
      [['1', '5 岁 7 个月，男；85 多面龋', '无牙髓 / 根尖症状',
        '金属预成冠（SSC）', '多面龋首选，全冠保护至替换'],
       ['2', '3 岁 6 个月，女；奶瓶龋', '51、61 广泛龋坏',
        '前牙透明树脂冠（条冠）', '前牙美学 + 功能恢复'],
       ['3', '6 岁 2 个月，女；釉质发育不全', '前牙形态 / 色泽异常',
        '预成全瓷冠（氧化锆）', '美学要求高、需牙色修复'],
       ['4', '5 岁 11 个月，男；74 邻面龋', '无牙髓症状，可隔湿',
        'Hall 技术', '不备牙，直接粘接，患儿配合好'],
       ['5', '6 岁 5 个月，男；64 牙髓治疗后', '根管治疗完成、根尖无异常',
        '金属预成冠（SSC）', '牙髓治疗后常规全冠保护'],
       ['6', '4 岁 8 个月，女；高龋风险', '多牙面龋、口腔卫生一般',
        '多颗 SSC 一次性修复', '高龋风险，考虑全麻下完成'],
       ['7', '7 岁 2 个月，男；55 早失', '54 完好可作基牙',
        '全冠丝圈式', '全冠 + 丝圈，兼作间隙保持'],
       ['8', '5 岁 3 个月，女；61 外伤冠折', '未露髓、无根折',
        '前牙透明树脂冠（条冠）', '外伤后恢复外形与功能'],
       ['9', '6 岁 9 个月，男；金属过敏', '既往金属修复过敏史',
        '预成全瓷冠（氧化锆）', '金属过敏的替代方案'],
       ['10', '8 岁 1 个月，女；85 牙根吸收 >1/3', '接近替换期',
        '不做冠，观察 / 拔除', '禁忌证：冠无保留价值']],
      first_bold=True, size=8.5)

# ============================== 9 附录 ==============================
H1('9　附录')
H2('术前 / 术中 / 术后核对清单')
BUL('术前：排除禁忌（牙根吸收、根尖病变、金属过敏）；确认可隔湿；知情同意。')
BUL('术中：备牙标准（咬合面 1.0–1.5 mm、邻面平行、去倒凹、线角圆钝）；'
    '冠缘成形；粘接前隔湿；去净多余粘接剂；检查咬合。')
BUL('术后：清洁与饮食指导；预约复查；病历记录冠型号与粘接材料。')
H2('主要参考依据')
for i, r in enumerate([
    '中华口腔医学会儿童口腔医学专业委员会相关指南 / 专家共识.',
    '葛立宏, 主编. 儿童口腔医学. 人民卫生出版社.',
    '秦满, 主编. 儿童口腔科临床操作教程. 人民卫生出版社.',
    'American Academy of Pediatric Dentistry. Guideline on Pediatric Restorative '
    'Dentistry. The AAPD Reference Manual.',
    'Innes NPT, et al. The Hall Technique. (International Journal of Paediatric '
    'Dentistry).',
], 1):
    p = doc.add_paragraph(style='T-Note')
    p.paragraph_format.left_indent = Cm(1.15)
    p.paragraph_format.first_line_indent = Cm(-0.7)
    set_run(p.add_run('[%d] ' % i), size=9, bold=True)
    set_run(p.add_run(r), size=9)

p = doc.add_paragraph(style='T-Note')
set_run(p.add_run('说明：图中尺寸与操作参数均为临床常用参考范围，须结合患儿牙列阶段、'
                  '影像学表现、龋风险与配合度个体化调整；具体产品以说明书与注册证为准。'),
        size=9, color=GREY)

doc.save('乳牙预成冠修复术_图解手册.docx')
print('OK saved')
