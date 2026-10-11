# -*- coding: utf-8 -*-
"""乳牙预成冠修复术 · 示意图生成。"""
import os
import math
from fig_lib import *

OUT = 'figs_crown'
os.makedirs(OUT, exist_ok=True)


def lin(t0, t1, n=80):
    if n <= 1:
        return [t0]
    return [t0 + (t1 - t0) * i / (n - 1) for i in range(n)]


def caption(f, xy, s, size=23, fill=(98, 106, 116), anchor='mm', bold=False):
    f.text(xy, s, size=size, fill=fill, anchor=anchor, bold=bold)


def legend(f, box, items, size=27, gap=45, title=None):
    x0, y0, x1, y1 = box
    if title:
        f.text((x0, y0), title, size=size + 4, bold=True, anchor='la', fill=(31, 54, 77))
        y0 += 52
    y = y0 + 6
    for n, t in items:
        f.text((x0 + 4, y), n, size=size + 3, bold=True, fill=BLUE, anchor='lm', halo=0)
        f.text((x0 + 46, y), t, size=size, anchor='lm', fill=INK, halo=0)
        y += gap


# ------------------------------------------------------------------ 前牙冠形态
def tooth_anterior(f, cx, top, w, h, fill=ENAMEL, edge=ENAMEL_LINE, dashed=False,
                   num=None):
    pts = [(cx - w / 2, top + h * 0.45), (cx + w / 2, top + h * 0.45),
           (cx + w * 0.36, top + h), (cx - w * 0.36, top + h)]
    if dashed:
        f.poly(pts, fill=(248, 249, 251), outline=DASH, width=1.6)
    else:
        f.poly(pts, fill=fill, outline=edge, width=2.4)
    if num:
        f.text((cx, top + h * 0.76), num, size=19, anchor='mm', fill=(118, 126, 136),
               halo=0)


def resin_crown(f, cx, top, w, h):
    """前牙树脂条冠（去套抛光后的树脂面）。"""
    fill, edge = (248, 236, 214), (206, 168, 122)
    pts = [(cx - w / 2, top + h * 0.42), (cx + w / 2, top + h * 0.42),
           (cx + w * 0.40, top + h), (cx - w * 0.40, top + h)]
    f.poly(pts, fill=fill, outline=edge, width=2.4)
    f.line([(cx - w / 2, top + h * 0.42), (cx + w / 2, top + h * 0.42)],
           fill=edge, width=2.2)


def zirconia_crown(f, cx, top, w, h):
    """预成全瓷冠（氧化锆）：牙色、高透。"""
    fill, edge = (250, 250, 248), (168, 178, 188)
    pts = [(cx - w / 2, top + h * 0.42), (cx + w / 2, top + h * 0.42),
           (cx + w * 0.40, top + h), (cx - w * 0.40, top + h)]
    f.poly(pts, fill=fill, outline=edge, width=2.4)
    f.line([(cx - w / 2, top + h * 0.42), (cx + w / 2, top + h * 0.42)],
           fill=edge, width=2.2)
    f.line([(cx, top + h * 0.42), (cx, top + h * 0.86)], fill=(210, 218, 226), width=1.6)


def strip_sleeve(f, cx, top, w, h):
    """透明纤维素冠套（未充填树脂）。"""
    pts = [(cx - w / 2, top + h * 0.42), (cx + w / 2, top + h * 0.42),
           (cx + w * 0.40, top + h), (cx - w * 0.40, top + h)]
    f.poly(pts, fill=(222, 236, 245), outline=(120, 158, 184), width=2.4)


def molar_prepared(f, cx, top, w, h):
    """备牙后的乳磨牙（颊面观）：虚线为原外形，实线为预备后轮廓。"""
    f.poly([(cx - w * 0.54, top + h * 0.30), (cx - w * 0.33, top + h * 0.00),
            (cx - w * 0.08, top + h * 0.18), (cx + w * 0.08, top + h * 0.18),
            (cx + w * 0.33, top + h * 0.00), (cx + w * 0.54, top + h * 0.30),
            (cx + w * 0.54, top + h), (cx - w * 0.54, top + h)],
           fill=None, outline=DASH, width=1.7)
    f.poly([(cx - w * 0.44, top + h * 0.28), (cx + w * 0.44, top + h * 0.28),
            (cx + w * 0.47, top + h), (cx - w * 0.47, top + h)],
           fill=ENAMEL, outline=ENAMEL_LINE, width=2.3)
    f.line([(cx - w * 0.44, top + h * 0.28), (cx + w * 0.44, top + h * 0.28)],
           fill=ENAMEL_LINE, width=2.2)
    f.line([(cx - w * 0.47, top + h * 0.94), (cx + w * 0.47, top + h * 0.94)],
           fill=(168, 176, 186), width=2)


def molar_occl_prepared(f, cx, cy, w, h):
    f.rrect((cx - w * 0.58, cy - h * 0.58, cx + w * 0.58, cy + h * 0.58),
            r=h * 0.30, outline=DASH, width=2)
    f.rrect((cx - w * 0.44, cy - h * 0.44, cx + w * 0.44, cy + h * 0.44),
            r=h * 0.24, fill=ENAMEL, outline=ENAMEL_LINE, width=2.2)
    f.line([(cx - w * 0.20, cy), (cx + w * 0.20, cy)], fill=GROOVE, width=2)


def crown_cervical(f, cx, top, w, h, margin='flush'):
    """冠颈缘局部：flush=密合；overhang=悬突；short=过短。"""
    W = w
    f.rrect((cx - W / 2, top + h * 0.20, cx + W / 2, top + h * 0.94), r=h * 0.18,
            fill=ENAMEL, outline=ENAMEL_LINE, width=2.2)
    if margin == 'overhang':
        f.rrect((cx - W / 2 - 8, top + h * 0.62, cx + W / 2 + 8, top + h * 0.94),
                r=h * 0.12, fill=METAL, outline=METAL_EDGE, width=2.2)
        for dx in (-0.55, -0.40, 0.40, 0.55):
            f.ellipse((cx + dx * W * 0.34 - 7, top + h * 0.94 - 5,
                       cx + dx * W * 0.34 + 7, top + h * 0.94 + 9), fill=(120, 170, 90))
    elif margin == 'short':
        f.rrect((cx - W / 2 - 2, top + h * 0.74, cx + W / 2 + 2, top + h * 0.94),
                r=h * 0.10, fill=METAL, outline=METAL_EDGE, width=2.2)
        f.rrect((cx - W / 2, top + h * 0.56, cx + W / 2, top + h * 0.74),
                fill=(250, 248, 242), outline=(210, 200, 186), width=1.6)
        f.text((cx, top + h * 0.65), '暴露牙体', size=18, anchor='mm', fill=RED)
    else:
        f.rrect((cx - W / 2 - 2, top + h * 0.56, cx + W / 2 + 2, top + h * 0.94),
                r=h * 0.12, fill=METAL, outline=METAL_EDGE, width=2.2)


# ------------------------------------------------------------------ 图1 冠类型总览
def mini_ssc(f, box):
    b = Box(f, box)
    gy = b.Y(0.84)
    f.rect((b.X(0.03), gy, b.X(0.97), b.Y(1.0)), fill=GINGIVA)
    f.line([(b.X(0.03), gy), (b.X(0.97), gy)], fill=GINGIVA_EDGE, width=2)
    top, H, W = b.Y(0.20), b.h * 0.62, b.w * 0.30
    tooth_buccal(f, b.X(0.32), top, W, H, kind='molar', crown=True)
    caption(f, b.P(0.32, 0.93), '金属冠', size=20, fill=(90, 98, 108))
    tooth_buccal(f, b.X(0.72), top, W, H, kind='molar')
    caption(f, b.P(0.72, 0.93), '待修复牙', size=20, fill=(120, 128, 138))
    f.arrow((b.X(0.50), b.Y(0.50)), (b.X(0.64), b.Y(0.50)), BLUE, 4, 14)


def mini_strip(f, box):
    b = Box(f, box)
    gy = b.Y(0.84)
    f.rect((b.X(0.03), gy, b.X(0.97), b.Y(1.0)), fill=GINGIVA)
    f.line([(b.X(0.03), gy), (b.X(0.97), gy)], fill=GINGIVA_EDGE, width=2)
    top, H, W = b.Y(0.22), b.h * 0.60, b.w * 0.26
    tooth_anterior(f, b.X(0.32), top, W, H, dashed=True)
    caption(f, b.P(0.32, 0.93), '待修复', size=19, fill=(120, 128, 138))
    strip_sleeve(f, b.X(0.70), top, W, H)
    f.line([(b.X(0.70) - W * 0.30, top + H * 0.42), (b.X(0.70) - W * 0.30, top + H)],
           fill=(120, 158, 184), width=1.6)
    f.text((b.X(0.70), top + H * 0.78), '树脂', size=19, anchor='mm', fill=(50, 90, 120))
    caption(f, b.P(0.70, 0.93), '透明冠套 + 树脂', size=19, fill=(90, 98, 108))
    f.arrow((b.X(0.50), b.Y(0.50)), (b.X(0.62), b.Y(0.50)), BLUE, 4, 14)


def mini_zirconia(f, box):
    b = Box(f, box)
    gy = b.Y(0.84)
    f.rect((b.X(0.03), gy, b.X(0.97), b.Y(1.0)), fill=GINGIVA)
    f.line([(b.X(0.03), gy), (b.X(0.97), gy)], fill=GINGIVA_EDGE, width=2)
    top, H, W = b.Y(0.22), b.h * 0.60, b.w * 0.26
    tooth_anterior(f, b.X(0.32), top, W, H, dashed=True)
    caption(f, b.P(0.32, 0.93), '待修复', size=19, fill=(120, 128, 138))
    zirconia_crown(f, b.X(0.70), top, W, H)
    caption(f, b.P(0.70, 0.93), '全瓷冠（牙色）', size=19, fill=(90, 98, 108))
    f.arrow((b.X(0.50), b.Y(0.50)), (b.X(0.62), b.Y(0.50)), BLUE, 4, 14)


def mini_hall(f, box):
    b = Box(f, box)
    gy = b.Y(0.84)
    f.rect((b.X(0.03), gy, b.X(0.97), b.Y(1.0)), fill=GINGIVA)
    f.line([(b.X(0.03), gy), (b.X(0.97), gy)], fill=GINGIVA_EDGE, width=2)
    top, H, W = b.Y(0.20), b.h * 0.62, b.w * 0.30
    tooth_buccal(f, b.X(0.32), top, W, H, kind='molar', crown=True)
    f.text((b.X(0.32), top + H * 0.40), '×', size=34, bold=True, fill=(150, 170, 190),
           anchor='mm')
    caption(f, b.P(0.32, 0.93), '少 / 不备牙', size=20, fill=(90, 98, 108))
    f.arrow((b.X(0.50), b.Y(0.50)), (b.X(0.64), b.Y(0.50)), BLUE, 4, 14)


def fig01():
    f = Fig(1800, 1190)
    m, gap = 28, 24
    pw = (1800 - 2 * m - 2 * gap) / 3
    ph = (1190 - 2 * m - gap) / 2
    specs = [
        ('① 金属预成冠（SSC）', '乳磨牙多面龋 / 牙髓治疗后首选', mini_ssc),
        ('② 前牙透明树脂冠（条冠）', '前牙龋 / 奶瓶龋 / 外伤', mini_strip),
        ('③ 预成全瓷冠（氧化锆）', '美学要求 / 金属过敏', mini_zirconia),
        ('④ Hall 技术', '少备牙或不备牙直接粘接', mini_hall),
        ('⑤ 基牙用（全冠丝圈式）', '乳磨牙全冠 + 丝圈保持间隙',
         lambda ff, bb: mini_ssc(ff, bb)),
        ('⑥ 多颗一次性修复', '全麻 / 门诊下多象限治疗',
         lambda ff, bb: mini_ssc(ff, bb)),
    ]
    for i, (title, cap, fn) in enumerate(specs):
        r, c = divmod(i, 3)
        x0 = m + c * (pw + gap)
        y0 = m + r * (ph + gap)
        box = (x0, y0, x0 + pw, y0 + ph)
        f.panel(box, title=title)
        fn(f, (x0 + 16, y0 + 52, x0 + pw - 16, y0 + ph - 44))
        caption(f, ((box[0] + box[2]) / 2, box[3] - 22), cap)
    return f.save(os.path.join(OUT, 'fig01_overview.png'))


# ------------------------------------------------------------------ 图2 SSC 结构与备牙标准
def fig02():
    f = Fig(1800, 880)
    f.rrect((40, 40, 1100, 840), r=14, fill=(252, 253, 254), outline=(216, 222, 229),
            width=1.6)
    # 左：颊面观（备牙后 + 戴冠）
    b = Box(f, (70, 70, 640, 800))
    gy = b.Y(0.82)
    f.rect((b.X(0.0), gy, b.X(1.0), b.Y(1.0)), fill=GINGIVA)
    f.line([(b.X(0.0), gy), (b.X(1.0), gy)], fill=GINGIVA_EDGE, width=2)
    top, H, W = b.Y(0.16), b.h * 0.60, b.w * 0.42
    molar_prepared(f, b.X(0.30), top, W, H)
    tooth_buccal(f, b.X(0.72), top, W, H, kind='molar', crown=True)
    f.arrow((b.X(0.48), b.Y(0.40)), (b.X(0.60), b.Y(0.40)), BLUE, 4, 14)
    # 咬合面观
    o = Box(f, (740, 70, 1050, 360))
    molar_occl_prepared(f, o.X(0.5), o.Y(0.52), o.w * 0.34, o.h * 0.30)
    f.text((o.X(0.5), o.Y(0.10)), '咬合面预备', size=22, bold=True, anchor='mm',
           fill=(31, 54, 77))
    # 标注
    def cal(x, y, s):
        f.text((x, y), s, size=27, bold=True, fill=BLUE, halo=3)
    cal(b.X(0.30), b.Y(0.10), '①')
    cal(b.X(0.72), b.Y(0.52), '⑥')
    cal(b.X(0.30), b.Y(0.45), '②')
    cal(b.X(0.30), b.Y(0.70), '③')
    cal(b.X(0.30), b.Y(0.88), '④')
    cal(b.X(0.30), b.Y(0.30), '⑤')
    legend(f, (1140, 110, 1760, 760), [
        ('①', '咬合面预备 1.0–1.5 mm（均匀）'),
        ('②', '邻面打开接触、近远中平行或微内聚'),
        ('③', '颊舌面去倒凹，不需大量预备'),
        ('④', '冠缘位于龈下 0.5–1.0 mm'),
        ('⑤', '线角圆钝、无肩台、无锐利边缘'),
        ('⑥', '选最小能完全就位的冠，修整颈缘'),
    ], size=25, gap=64, title='备牙标准（金属预成冠）')
    return f.save(os.path.join(OUT, 'fig02_ssc_structure.png'))


# ------------------------------------------------------------------ 图3 备牙步骤
def fig03():
    f = Fig(1800, 640)
    f.text((900, 44), '金属预成冠 · 备牙步骤（颊面观）', size=32, bold=True,
           anchor='mm', fill=(31, 54, 77))
    steps = [
        ('1', '去龋 / 牙髓治疗', '去除龋坏，必要时行牙髓治疗'),
        ('2', '咬合面预备', '均匀磨除 1.0–1.5 mm'),
        ('3', '邻面预备', '打开接触，平行或微内聚'),
        ('4', '颊舌面去倒凹', '修整外形，线角圆钝'),
        ('5', '完成', '龈下边缘 0.5–1.0 mm'),
    ]
    w, h, gap = 330, 210, 18
    x = (1800 - (5 * w + 4 * gap)) / 2
    y = 120
    gy_base = y + h * 0.86
    for i, (n, t, s) in enumerate(steps):
        x0 = x + i * (w + gap)
        f.rrect((x0, y, x0 + w, y + h), r=14, fill=(246, 250, 253),
                outline=(206, 216, 226), width=1.6)
        f.ellipse((x0 + w / 2 - 20, y + 12, x0 + w / 2 + 20, y + 52), fill=(31, 54, 77))
        f.text((x0 + w / 2, y + 32), n, size=24, bold=True, anchor='mm', fill=WHITE,
               halo=0)
        f.text((x0 + w / 2, y + 70), t, size=24, bold=True, anchor='mm',
               fill=(28, 60, 92))
        # 牙齿示意
        cx = x0 + w / 2
        top = y + 96
        W = w * 0.42
        H = 96
        f.rect((x0 + 10, y + 104, x0 + w - 10, y + 210), fill=GINGIVA)
        f.line([(x0 + 10, y + 104), (x0 + w - 10, y + 104)], fill=GINGIVA_EDGE, width=2)
        if i == 0:
            tooth_buccal(f, cx, top, W, H * 0.8, kind='molar')
        elif i == 1:
            molar_prepared(f, cx, top - 4, W, H * 0.9)
        elif i == 2:
            molar_prepared(f, cx, top - 4, W, H * 0.9)
            f.line([(cx - W * 0.47, top + H * 0.9), (cx + W * 0.47, top + H * 0.9)],
                   fill=(210, 130, 130), width=2.4)
        elif i == 3:
            molar_prepared(f, cx, top - 4, W, H * 0.9)
            f.arc((cx - W * 0.52, top - 8, cx + W * 0.52, top + H * 0.7), 90, 270,
                  fill=(210, 130, 130), width=2)
        else:
            tooth_buccal(f, cx, top - 4, W, H * 0.9, kind='molar', crown=True)
        if i < 4:
            f.arrow((x0 + w + 2, y + h / 2), (x0 + w + gap - 2, y + h / 2),
                    (140, 152, 166), 5, 15)
        f.text((x0 + w / 2, y + h - 10), s, size=17, anchor='mm', fill=(96, 104, 114))
    f.text((900, 596), '① 无肩台 · ② 无锐边 · ③ 冠缘位于龈下 0.5–1.0 mm', size=24,
           anchor='mm', fill=(150, 110, 20))
    return f.save(os.path.join(OUT, 'fig03_ssc_prep.png'))


# ------------------------------------------------------------------ 图4 选冠试戴
def fig04():
    f = Fig(1800, 640)
    f.text((900, 44), '选冠与试戴：三个关键判断', size=32, bold=True, anchor='mm',
           fill=(31, 54, 77))
    items = [
        ('太大：不能就位 / 边缘悬于龈上', '需换小一号', RED),
        ('合适：完全就位，边缘龈下 0.5–1.0 mm', '贴合、有“回弹”手感', GREEN),
        ('太小：过松、无固位', '换大一号或调整', RED),
    ]
    w, gap = 540, 24
    x = (1800 - (3 * w + 2 * gap)) / 2
    y = 110
    for i, (t, s, col) in enumerate(items):
        x0 = x + i * (w + gap)
        f.rrect((x0, y, x0 + w, y + 470), r=14, fill=(252, 253, 254),
                outline=(216, 222, 229), width=1.6)
        f.text((x0 + w / 2, y + 26), t, size=22, bold=True, anchor='mm', fill=col)
        gy = y + 430
        f.rect((x0 + 30, gy, x0 + w - 30, y + 466), fill=GINGIVA)
        f.line([(x0 + 30, gy), (x0 + w - 30, gy)], fill=GINGIVA_EDGE, width=2)
        cx = x0 + w / 2
        top = y + 90
        W = w * 0.40
        H = 340
        if i == 0:
            tooth_buccal(f, cx, top + 34, W, H * 0.8, kind='molar', crown=True)
            f.text((cx, top + 12), '未就位', size=20, anchor='mm', fill=RED)
        elif i == 1:
            tooth_buccal(f, cx, top + 30, W, H * 0.84, kind='molar', crown=True)
            f.arrow((cx + W * 0.7, gy - 30), (cx + W * 0.7, gy - 66), GREEN, 3, 12)
            f.arrow((cx + W * 0.7, gy - 66), (cx + W * 0.7, gy - 30), GREEN, 3, 12)
            f.text((cx + W * 0.86, gy - 48), '0.5–1.0 mm', size=20, anchor='lm',
                   fill=GREEN)
        else:
            tooth_buccal(f, cx, top + 30, W, H * 0.84, kind='molar', crown=True)
            f.text((cx, top + 12), '过松', size=20, anchor='mm', fill=RED)
        f.text((x0 + w / 2, y + 466 - 14), s, size=20, anchor='mm', fill=(96, 104, 114))
    return f.save(os.path.join(OUT, 'fig04_tryin.png'))


# ------------------------------------------------------------------ 图5 冠缘成形
def fig05():
    f = Fig(1800, 680)
    f.text((900, 44), '冠缘成形与修整（crimping）', size=32, bold=True, anchor='mm',
           fill=(31, 54, 77))
    lx = (70, 100, 870, 640)
    rx = (930, 100, 1730, 640)
    f.rrect(lx, r=14, fill=(244, 251, 246), outline=(198, 226, 210), width=1.6)
    f.rrect(rx, r=14, fill=(253, 244, 244), outline=(238, 206, 206), width=1.6)
    f.text(((lx[0] + lx[2]) / 2, lx[1] + 24), '√ 冠缘成形后', size=26, bold=True,
           anchor='mm', fill=GREEN)
    f.text(((rx[0] + rx[2]) / 2, rx[1] + 24), '× 未成形 / 悬突', size=26, bold=True,
           anchor='mm', fill=RED)
    crown_cervical(f, (lx[0] + lx[2]) / 2, lx[1] + 70, 300, 480, margin='flush')
    crown_cervical(f, (rx[0] + rx[2]) / 2, rx[1] + 70, 300, 480, margin='overhang')
    f.text(((lx[0] + lx[2]) / 2, lx[3] - 16), '冠缘内收、贴紧牙颈部，无悬突', size=21,
           anchor='mm', fill=(24, 100, 62))
    f.text(((rx[0] + rx[2]) / 2, rx[3] - 16), '边缘外翻悬突 → 菌斑滞留、牙龈炎', size=21,
           anchor='mm', fill=(160, 50, 50))
    return f.save(os.path.join(OUT, 'fig05_crimp.png'))


# ------------------------------------------------------------------ 图6 前牙条冠
def fig06():
    f = Fig(1800, 640)
    f.text((900, 44), '前牙透明树脂冠（条冠）· 操作步骤', size=32, bold=True,
           anchor='mm', fill=(31, 54, 77))
    steps = [
        ('1', '预备', '切端 / 邻面预备，去龋'),
        ('2', '选冠套', '透明纤维素冠套，修整颈缘'),
        ('3', '充填就位', '冠套内充树脂，就位'),
        ('4', '去套抛光', '去除冠套，调合抛光'),
    ]
    w, h, gap = 400, 210, 20
    x = (1800 - (4 * w + 3 * gap)) / 2
    y = 110
    for i, (n, t, s) in enumerate(steps):
        x0 = x + i * (w + gap)
        f.rrect((x0, y, x0 + w, y + h), r=14, fill=(246, 250, 253),
                outline=(206, 216, 226), width=1.6)
        f.ellipse((x0 + w / 2 - 20, y + 12, x0 + w / 2 + 20, y + 52), fill=(31, 54, 77))
        f.text((x0 + w / 2, y + 32), n, size=24, bold=True, anchor='mm', fill=WHITE,
               halo=0)
        f.text((x0 + w / 2, y + 70), t, size=24, bold=True, anchor='mm', fill=(28, 60, 92))
        cx = x0 + w / 2
        top = y + 92
        W = w * 0.30
        H = 96
        f.rect((x0 + 12, y + 100, x0 + w - 12, y + 210), fill=GINGIVA)
        f.line([(x0 + 12, y + 100), (x0 + w - 12, y + 100)], fill=GINGIVA_EDGE, width=2)
        if i == 0:
            tooth_anterior(f, cx, top, W, H, dashed=True)
        elif i == 1:
            tooth_anterior(f, cx, top, W, H, dashed=True)
            strip_sleeve(f, cx + W * 1.4, top, W, H)
        elif i == 2:
            strip_sleeve(f, cx, top, W, H)
            f.text((cx, top + H * 0.78), '树脂', size=18, anchor='mm', fill=(50, 90, 120))
        else:
            resin_crown(f, cx, top, W, H)
        if i < 3:
            f.arrow((x0 + w + 2, y + h / 2), (x0 + w + gap - 2, y + h / 2),
                    (140, 152, 166), 5, 15)
        f.text((x0 + w / 2, y + h - 10), s, size=17, anchor='mm', fill=(96, 104, 114))
    f.text((900, 596), '切端预备 1.0–1.5 mm · 邻面去倒凹 · 切角圆钝 · 龈下边缘 0.5–1.0 mm',
           size=24, anchor='mm', fill=(150, 110, 20))
    return f.save(os.path.join(OUT, 'fig06_strip_crown.png'))


# ------------------------------------------------------------------ 图7 操作流程
def fig07():
    f = Fig(1800, 660)
    f.text((900, 46), '预成冠修复 · 操作流程', size=34, bold=True, anchor='mm',
           fill=(31, 54, 77))
    steps = [
        ('1', '评估·麻醉', '适应证 · 麻醉'),
        ('2', '橡皮障·去龋', '隔湿 · 去龋'),
        ('3', '牙髓治疗', '必要时'),
        ('4', '备牙', '按标准预备'),
        ('5', '选冠·试戴', '最小号能就位'),
        ('6', '冠缘成形', 'crimping · 磨光'),
        ('7', '粘接', '玻璃离子水门汀'),
        ('8', '医嘱·复查', '咬合 · 复查'),
    ]
    w, h, gap = 200, 200, 22
    x = (1800 - (8 * w + 7 * gap)) / 2
    y = 130
    for i, (n, t, s) in enumerate(steps):
        x0 = x + i * (w + gap)
        f.rrect((x0, y, x0 + w, y + h), r=14, fill=(240, 246, 252),
                outline=(150, 175, 205), width=2)
        f.ellipse((x0 + w / 2 - 22, y + 14, x0 + w / 2 + 22, y + 58), fill=(31, 54, 77))
        f.text((x0 + w / 2, y + 36), n, size=26, bold=True, anchor='mm', fill=WHITE,
               halo=0)
        f.text((x0 + w / 2, y + 88), t, size=22, bold=True, anchor='mm',
               fill=(28, 60, 92))
        f.text((x0 + w / 2, y + 128), s, size=17, anchor='mm', fill=(96, 104, 114))
        if i < 7:
            f.arrow((x0 + w + 3, y + h / 2), (x0 + w + gap - 3, y + h / 2),
                    (140, 152, 166), 5, 15)
    f.rrect((150, 390, 1650, 610), r=14, fill=(253, 250, 240),
            outline=(226, 208, 160), width=1.8)
    f.text((900, 428), 'Hall 技术', size=25, bold=True, anchor='mm', fill=(150, 110, 20))
    f.text((900, 474), '乳磨牙龋损、无牙髓 / 根尖症状、可隔湿时：不备牙或极少备牙，'
           '直接选合适预成冠粘接。', size=22, anchor='mm', fill=(90, 80, 50))
    f.text((900, 520), '关键：完全就位 · 无悬突 · 咬合无干扰 · 邻接恢复 · 去净多余粘接剂',
           size=22, anchor='mm', fill=(90, 80, 50))
    return f.save(os.path.join(OUT, 'fig07_workflow.png'))


# ------------------------------------------------------------------ 图8 对错对照
def fig08():
    f = Fig(1800, 1320)
    f.text((900, 40), '常见错误对照（左侧正确 · 右侧错误）', size=34, bold=True,
           anchor='mm', fill=(31, 54, 77))
    rows = [
        ('冠颈缘', lambda ff, bx, ok: crown_cervical(ff, bx.X(0.5), bx.Y(0.18),
         bx.w * 0.40, bx.h * 0.72, 'flush' if ok else 'overhang'),
         '边缘密合、龈下 0.5–1.0 mm', '悬突 → 菌斑、牙龈炎'),
        ('冠缘长度', lambda ff, bx, ok: crown_cervical(ff, bx.X(0.5), bx.Y(0.18),
         bx.w * 0.40, bx.h * 0.72, 'flush' if ok else 'short'),
         '覆盖至龈下 0.5–1.0 mm', '过短 → 暴露牙体、继发龋'),
        ('邻接关系', lambda ff, bx, ok: frag_proximal(ff, bx, ok),
         '邻接恢复、无食物嵌塞', '邻接不良 → 食物嵌塞'),
        ('咬合', lambda ff, bx, ok: frag_occlusal(ff, bx, ok),
         '咬合均匀、无早接触', '咬合过高 → 早接触'),
    ]
    y = 90
    ph = 292
    for i, (title, fn, gt, bt) in enumerate(rows):
        y0 = y + i * (ph + 14)
        box = (60, y0, 1740, y0 + ph)
        f.rrect(box, r=14, fill=(252, 253, 254), outline=(222, 228, 234), width=1.5)
        f.text(((box[0] + box[2]) / 2, y0 + 26), title, size=27, bold=True,
               anchor='mm', fill=(31, 54, 77))
        lx = (100, y0 + 54, 880, y0 + ph - 16)
        rx = (920, y0 + 54, 1700, y0 + ph - 16)
        f.rrect(lx, r=12, fill=(244, 251, 246), outline=(198, 226, 210), width=1.6)
        f.rrect(rx, r=12, fill=(253, 244, 244), outline=(238, 206, 206), width=1.6)
        fn(f, Box(f, lx), True)
        fn(f, Box(f, rx), False)
        f.text((lx[0] + 30, (lx[1] + lx[3]) / 2), '√', size=44, bold=True, fill=GREEN,
               anchor='mm')
        f.text((rx[0] + 30, (rx[1] + rx[3]) / 2), '×', size=44, bold=True, fill=RED,
               anchor='mm')
        f.text(((lx[0] + lx[2]) / 2 + 20, lx[3] - 24), gt, size=22, anchor='mm',
               fill=(24, 100, 62))
        f.text(((rx[0] + rx[2]) / 2 + 20, rx[3] - 24), bt, size=22, anchor='mm',
               fill=(160, 50, 50))
    return f.save(os.path.join(OUT, 'fig08_dos_donts.png'))


def frag_proximal(f, box, ok=True):
    b = box
    W, H = b.w * 0.30, b.h * 0.60
    for cx in (b.X(0.34), b.X(0.66)):
        f.rrect((cx - W / 2, b.Y(0.20), cx + W / 2, b.Y(0.20) + H), r=14,
                fill=METAL if cx < b.X(0.5) else ENAMEL, outline=METAL_EDGE if cx < b.X(0.5) else ENAMEL_LINE,
                width=2.2)
    if ok:
        f.text((b.X(0.5), b.Y(0.12)), '邻接贴合', size=21, anchor='mm', fill=GREEN)
    else:
        f.text((b.X(0.5), b.Y(0.12)), '有间隙', size=21, anchor='mm', fill=RED)
        f.arrow((b.X(0.42), b.Y(0.52)), (b.X(0.50), b.Y(0.52)), RED, 3, 12)
        f.arrow((b.X(0.58), b.Y(0.52)), (b.X(0.50), b.Y(0.52)), RED, 3, 12)


def frag_occlusal(f, box, ok=True):
    b = box
    W = b.w * 0.44
    f.rrect((b.X(0.5) - W / 2, b.Y(0.34), b.X(0.5) + W / 2, b.Y(0.86)), r=16,
            fill=METAL, outline=METAL_EDGE, width=2.2)
    f.line([(b.X(0.5) - W * 0.40, b.Y(0.34)), (b.X(0.5) + W * 0.40, b.Y(0.34))],
           fill=METAL_EDGE, width=2.4)
    if ok:
        f.text((b.X(0.5), b.Y(0.16)), '均匀接触', size=21, anchor='mm', fill=GREEN)
    else:
        f.ellipse((b.X(0.5) - 14, b.Y(0.30), b.X(0.5) + 14, b.Y(0.56)),
                  fill=(240, 170, 170))
        f.text((b.X(0.5), b.Y(0.16)), '早接触点', size=21, anchor='mm', fill=RED)
        f.arrow((b.X(0.80), b.Y(0.20)), (b.X(0.62), b.Y(0.42)), RED, 3, 12)


# ------------------------------------------------------------------ 图9 复诊时间轴
def fig09():
    f = Fig(1800, 560)
    f.text((900, 44), '预成冠 · 复诊与维护', size=34, bold=True, anchor='mm',
           fill=(31, 54, 77))
    y = 300
    f.line([(120, y), (1700, y)], fill=(150, 162, 176), width=6)
    nodes = [
        ('戴入当天', '医嘱 + 清洁示范', 200, 1),
        ('1 周', '咬合、组织、边缘', 520, -1),
        ('每 6 个月', '复查 · 检查松动 / 悬突', 900, 1),
        ('替换期', '随乳牙自然脱落', 1300, -1),
        ('异常', '穿孔 / 松动 / 继发龋 → 更换', 1660, 1),
    ]
    for label, sub, x, side in nodes:
        f.ellipse((x - 17, y - 17, x + 17, y + 17), fill=(31, 54, 77))
        ty = y - 62 if side > 0 else y + 62
        f.text((x, ty), label, size=26, bold=True, anchor='mm', fill=(28, 60, 92))
        f.text((x, ty + (36 if side > 0 else -36)), sub, size=20, anchor='mm',
               fill=(96, 104, 114))
        f.line([(x, y - 20 if side > 0 else y + 20), (x, ty + (20 if side > 0 else -20))],
               fill=(180, 188, 198), width=1.6)
    return f.save(os.path.join(OUT, 'fig09_timeline.png'))


# ------------------------------------------------------------------ 图12 病例
def fig12():
    f = Fig(1800, 1240)
    f.text((900, 40), '典型病例示意', size=34, bold=True, anchor='mm',
           fill=(31, 54, 77))
    m, gap = 26, 22
    pw = (1800 - 2 * m - gap) / 2
    ph = (1240 - 120 - 2 * m - gap) / 2
    y0base = 96

    def panel(i, title, sub, fn, tag):
        r, c = divmod(i, 2)
        x0 = m + c * (pw + gap)
        y0 = y0base + r * (ph + gap)
        box = (x0, y0, x0 + pw, y0 + ph)
        f.panel(box, title=title)
        fn(f, (x0 + 20, y0 + 56, x0 + pw - 20, y0 + ph - 84))
        caption(f, ((box[0] + box[2]) / 2, box[3] - 56), sub, size=23, bold=True,
                fill=(31, 54, 77))
        caption(f, ((box[0] + box[2]) / 2, box[3] - 24), tag, size=22)

    def c1(f, box):
        b = Box(f, box)
        top, H, W = b.Y(0.22), b.h * 0.56, b.w * 0.26
        tooth_buccal(f, b.X(0.28), top, W, H, kind='molar')
        f.ellipse((b.X(0.28) - 16, top - 14, b.X(0.28) + 16, top + 10),
                  fill=(240, 170, 170))
        tooth_buccal(f, b.X(0.72), top, W, H, kind='molar', crown=True)
        f.arrow((b.X(0.46), b.Y(0.46)), (b.X(0.60), b.Y(0.46)), BLUE, 4, 14)

    def c2(f, box):
        b = Box(f, box)
        top, H, W = b.Y(0.24), b.h * 0.54, b.w * 0.24
        for i, cx in enumerate((0.22, 0.48, 0.74)):
            tooth_anterior(f, b.X(cx), top, W, H, dashed=True)
        for cx in (0.48, 0.74):
            resin_crown(f, b.X(cx), top, W, H)

    def c3(f, box):
        b = Box(f, box)
        top, H, W = b.Y(0.24), b.h * 0.54, b.w * 0.24
        for cx in (0.22, 0.48, 0.74):
            tooth_anterior(f, b.X(cx), top, W, H, dashed=True)
        for cx in (0.48, 0.74):
            zirconia_crown(f, b.X(cx), top, W, H)

    def c4(f, box):
        b = Box(f, box)
        top, H, W = b.Y(0.22), b.h * 0.56, b.w * 0.26
        tooth_buccal(f, b.X(0.30), top, W, H, kind='molar', crown=True)
        f.text((b.X(0.30), top + H * 0.40), '×', size=36, bold=True, fill=(150, 170, 190),
               anchor='mm')
        f.text((b.X(0.66), b.Y(0.5)), '不备牙', size=22, anchor='mm', fill=GREEN)
        f.arrow((b.X(0.48), b.Y(0.5)), (b.X(0.58), b.Y(0.5)), BLUE, 4, 14)

    panel(0, '病例 1　5 岁 7 个月 · 男', '85 多面龋，无牙髓症状', c1,
          '金属预成冠（SSC）')
    panel(1, '病例 2　3 岁 6 个月 · 女', '奶瓶龋，51、61 广泛龋坏', c2,
          '前牙透明树脂冠（条冠）')
    panel(2, '病例 3　6 岁 2 个月 · 女', '釉质发育不全，前牙美学修复', c3,
          '预成全瓷冠（氧化锆）')
    panel(3, '病例 4　5 岁 11 个月 · 男', '74 近中邻面龋，可隔湿', c4,
          'Hall 技术（不备牙直接粘接）')
    return f.save(os.path.join(OUT, 'fig12_cases.png'))


if __name__ == '__main__':
    for fn in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig12):
        print(fn())
