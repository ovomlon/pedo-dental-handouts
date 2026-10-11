# -*- coding: utf-8 -*-
"""生成 12 张临床示意图（PNG）。"""
import os
import math
from fig_lib import *

OUT = 'figs'
os.makedirs(OUT, exist_ok=True)


def lin(t0, t1, n=80):
    if n <= 1:
        return [t0]
    return [t0 + (t1 - t0) * i / (n - 1) for i in range(n)]


def arch_curve(cx, cy, a, b, k, t0, t1, n=90):
    return [(cx + a * k * math.sin(t), cy - b * k * math.cos(t)) for t in lin(t0, t1, n)]


def wire_circle(f, cx, cy, rx, ry=None, width=6):
    ry = ry or rx
    pts = [(cx + rx * math.cos(t), cy + ry * math.sin(t))
           for t in lin(0, 2 * math.pi, 46)]
    pts.append(pts[0])
    f.wire(pts, width=width)


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


def caption(f, xy, s, size=23, fill=(98, 106, 116), anchor='mm', bold=False):
    f.text(xy, s, size=size, fill=fill, anchor=anchor, bold=bold)


# ------------------------------------------------------------------ 小示意图
def mini_band_loop(f, box, crown=False):
    b = Box(f, box)
    gy = b.Y(0.86)
    f.rect((b.X(0.02), gy, b.X(0.98), b.Y(1.0)), fill=GINGIVA)
    f.line([(b.X(0.02), gy), (b.X(0.98), gy)], fill=GINGIVA_EDGE, width=2)
    top, H, W = b.Y(0.20), b.h * 0.64, b.w * 0.21
    tooth_buccal(f, b.X(0.18), top, W * 0.88, H, kind='canine')
    missing_tooth(f, b.X(0.48), top, W, H, label='')
    tooth_buccal(f, b.X(0.79), top, W * 1.06, H, kind='molar', crown=crown)
    if not crown:
        band(f, b.X(0.79), top, W * 1.06, H, h_frac=0.44)
    f.wire([(b.X(0.72), b.Y(0.60)), (b.X(0.66), b.Y(0.68)), (b.X(0.56), b.Y(0.71)),
            (b.X(0.48), b.Y(0.71)), (b.X(0.44), b.Y(0.71)), (b.X(0.44), b.Y(0.77)),
            (b.X(0.38), b.Y(0.77)), (b.X(0.38), b.Y(0.71)), (b.X(0.33), b.Y(0.68)),
            (b.X(0.29), b.Y(0.64))], width=6)
    return b


def mini_distal_shoe(f, box):
    b = Box(f, box)
    gy = b.Y(0.72)
    f.rect((b.X(0.02), gy, b.X(0.98), b.Y(1.0)), fill=GINGIVA)
    f.line([(b.X(0.02), gy), (b.X(0.98), gy)], fill=GINGIVA_EDGE, width=2)
    top, H, W = b.Y(0.16), b.h * 0.56, b.w * 0.21
    tooth_buccal(f, b.X(0.17), top, W * 0.98, H, kind='molar')
    band(f, b.X(0.17), top, W * 0.98, H, h_frac=0.40)
    missing_tooth(f, b.X(0.45), top, W, H, label='')
    # 尚未萌出的第一恒磨牙（虚线，位于龈下）
    tooth_buccal(f, b.X(0.79), b.Y(0.74), W * 1.02, H * 0.62, kind='molar', dashed=True)
    # 靴形板：由带环向远中延伸后向下伸入龈下
    f.wire([(b.X(0.24), b.Y(0.52)), (b.X(0.42), b.Y(0.42)), (b.X(0.60), b.Y(0.42)),
            (b.X(0.63), b.Y(0.46))], width=6)
    f.rrect((b.X(0.625), b.Y(0.42), b.X(0.675), b.Y(0.86)), r=4, fill=METAL,
            outline=METAL_EDGE, width=2)


def mini_lingual(f, box, numbers=False, scale=0.90):
    info, (cx, cy, a, b) = draw_arch(f, box, arch=ARCH_MAND, a_frac=0.40,
                                     b_frac=0.40, cy_frac=0.56, numbers=numbers,
                                     bands=('36', '46'), scale=scale, mirror_sgn=-1)
    pts = arch_curve(cx, cy, a, b, 0.77, -1.72, 1.72)
    f.wire(pts, width=6)
    for sgn in (-1, 1):
        t = 1.10 * sgn
        p = arch_curve(cx, cy, a, b, 0.77, t, t, 1)[0]
        wire_circle(f, p[0], p[1], 15, 15, width=6)
    return info, (cx, cy, a, b)


def mini_nance(f, box, numbers=False, scale=0.90):
    info, (cx, cy, a, b) = draw_arch(f, box, arch=ARCH_MAX, a_frac=0.40,
                                     b_frac=0.40, cy_frac=0.56, numbers=numbers,
                                     bands=('16', '26'), scale=scale)
    pts = arch_curve(cx, cy, a, b, 0.70, -1.70, 1.70)
    f.wire(pts, width=6)
    btn = (cx - a * 0.42, cy - b * 0.78, cx + a * 0.42, cy - b * 0.06)
    f.hatch(btn, shape='ellipse', spacing=12)
    return info, (cx, cy, a, b)


# ------------------------------------------------------------------ 图 1 总览
def fig01():
    f = Fig(1800, 1190)
    m, gap = 28, 24
    pw = (1800 - 2 * m - 2 * gap) / 3
    ph = (1190 - 2 * m - gap) / 2
    specs = [
        ('① 带环丝圈式', '单侧 1 个牙缺失 · 最常用',
         lambda ff, bb: mini_band_loop(ff, bb)),
        ('② 全冠丝圈式', '基牙大面积缺损 / 已做全冠',
         lambda ff, bb: mini_band_loop(ff, bb, crown=True)),
        ('③ 远端靴式', '第一恒磨牙未萌 + 第二乳磨牙早失',
         lambda ff, bb: mini_distal_shoe(ff, bb)),
        ('④ 固定舌弓', '双侧下颌乳磨牙早失',
         lambda ff, bb: mini_lingual(ff, bb)),
        ('⑤ Nance 腭弓', '双侧上颌乳磨牙早失',
         lambda ff, bb: mini_nance(ff, bb)),
        ('⑥ 改良 Nance 弓', '保持 + 早期矫治（推簧 / 牵引 / 扩弓）',
         lambda ff, bb: mini_modified(ff, bb, 'spring')),
    ]
    for i, (title, cap, fn) in enumerate(specs):
        r, c = divmod(i, 3)
        x0 = m + c * (pw + gap)
        y0 = m + r * (ph + gap)
        box = (x0, y0, x0 + pw, y0 + ph)
        f.panel(box, title=title)
        inner = (x0 + 16, y0 + 52, x0 + pw - 16, y0 + ph - 44)
        fn(f, inner)
        caption(f, ((box[0] + box[2]) / 2, box[3] - 22), cap)
    return f.save(os.path.join(OUT, 'fig01_overview.png'))


def mini_modified(f, box, kind='spring'):
    info, (cx, cy, a, b) = mini_nance(f, box)
    if kind == 'spring':
        for sgn in (-1, 1):
            pts = arch_curve(cx, cy, a, b, 0.74, 1.18 * sgn, 1.86 * sgn, 8)
            f.curved_arrow(pts, RED, 5, 16)
            q = arch_curve(cx, cy, a, b, 0.74, 1.05 * sgn, 1.05 * sgn, 1)[0]
            wire_circle(f, q[0], q[1], 14, 14, width=5)
    return info


# ------------------------------------------------------------------ 图 2 带环丝圈式
def fig02():
    f = Fig(1780, 820)
    f.rrect((40, 40, 1080, 780), r=14, fill=(252, 253, 254), outline=(216, 222, 229),
            width=1.6)
    b = mini_band_loop(f, (90, 100, 1030, 740))

    def cal(u, v, s, anchor='la'):
        f.text(b.P(u, v), s, size=27, bold=True, fill=BLUE, halo=3, anchor=anchor)

    cal(0.80, 0.63, '①')
    cal(0.55, 0.60, '②')
    cal(0.50, 0.80, '③')
    cal(0.48, 0.38, '⑤')
    cal(0.10, 0.13, '⑥')
    f.line([(b.X(0.115), b.Y(0.17)), (b.X(0.27), b.Y(0.62))], fill=(150, 158, 168),
           width=1.6)
    # ④ 丝圈距牙龈的双向标注
    f.arrow((b.X(0.63), b.Y(0.78)), (b.X(0.63), b.Y(0.71)), BLUE, 3, 12)
    f.arrow((b.X(0.63), b.Y(0.78)), (b.X(0.63), b.Y(0.85)), BLUE, 3, 12)
    cal(0.64, 0.76, '④')
    f.text((b.X(0.5), b.Y(1.06)), '第一乳磨牙早失 → 带环丝圈式（颊面观）', size=30,
           bold=True, anchor='mm', fill=(31, 54, 77))
    legend(f, (1140, 120, 1740, 720), [
        ('①', '带环（预成不锈钢，厚 0.12–0.18 mm）'),
        ('②', '丝圈（不锈钢丝 0.8–0.9 mm）'),
        ('③', 'U 形曲：便于调整与加力'),
        ('④', '丝圈距牙龈 0.5–1.0 mm'),
        ('⑤', '缺隙：保持近远中径与高度'),
        ('⑥', '丝圈抵于近中邻牙邻面，不进入倒凹'),
    ], size=25, gap=62, title='结构要点')
    return f.save(os.path.join(OUT, 'fig02_band_loop.png'))


# ------------------------------------------------------------------ 图 3 舌弓
def fig03():
    f = Fig(1780, 900)
    f.rrect((40, 40, 1080, 860), r=14, fill=(252, 253, 254), outline=(216, 222, 229),
            width=1.6)
    info, (cx, cy, a, b) = mini_lingual(f, (90, 80, 1030, 800), numbers=True)
    f.text((cx, 690), '固定舌弓（下颌 · 合面观）', size=30, bold=True, anchor='mm',
           fill=(31, 54, 77))
    x, y, ang, w, h = info['36']
    f.text((x - 12, y + h * 0.90), '①', size=27, bold=True, fill=BLUE, halo=3)
    for sgn in (-1, 1):
        p = arch_curve(cx, cy, a, b, 0.77, 1.10 * sgn, 1.10 * sgn, 1)[0]
        f.text((p[0] + 42 * sgn - 12, p[1] + 34), '②', size=27, bold=True, fill=BLUE,
               halo=3)
    f.text((cx - 150, cy - b * 0.90), '③', size=27, bold=True, fill=BLUE, halo=3)
    f.text((cx + 20, cy - b * 0.30), '④', size=27, bold=True, fill=BLUE, halo=3)
    legend(f, (1140, 150, 1740, 750), [
        ('①', '带环：下颌第一恒磨牙（36 / 46）'),
        ('②', 'U 形曲：调整间隙、适应牙弓生长'),
        ('③', '舌弓距舌侧牙龈 0.5–1.0 mm'),
        ('④', '不压迫舌体、不进入倒凹'),
    ], size=26, gap=66, title='结构要点')
    return f.save(os.path.join(OUT, 'fig03_lingual_arch.png'))


# ------------------------------------------------------------------ 图 4 Nance 腭弓
def fig04():
    f = Fig(1800, 900)
    f.rrect((40, 40, 1090, 860), r=14, fill=(252, 253, 254), outline=(216, 222, 229),
            width=1.6)
    info, (cx, cy, a, b) = mini_nance(f, (100, 70, 1040, 780), numbers=True)
    x, y, ang, w, h = info['16']
    f.text((x - 14, y + h * 0.95), '①', size=27, bold=True, fill=BLUE, halo=3)
    f.text((cx + a * 0.62, cy - b * 0.48), '②', size=27, bold=True, fill=BLUE, halo=3)
    f.text((cx - 14, cy - b * 0.46), '④', size=27, bold=True, fill=BLUE, halo=3)
    f.text((cx, 660), 'Nance 腭弓（上颌 · 合面观）', size=30, bold=True,
           anchor='mm', fill=(31, 54, 77))

    # 矢状剖面示意
    f.rrect((1130, 470, 1770, 860), r=14, fill=(252, 253, 254), outline=(216, 222, 229),
            width=1.6)
    f.text((1450, 505), '腭部矢状剖面', size=26, bold=True, anchor='mm',
           fill=(31, 54, 77))
    px0, px1 = 1180, 1720
    py = 700
    f.line([(px0, py), (px1, py)], fill=(226, 170, 170), width=9)
    f.hatch((px0 + 40, py - 62, px0 + 330, py - 4), shape='rrect', spacing=11)
    f.text((px0 + 185, py - 33), '腭托 2–3 mm', size=23, anchor='mm', fill=(120, 80, 140))
    f.wire([(px0 + 30, py - 88), (px0 + 520, py - 74)], width=6)
    f.text((px0 + 250, py - 116), '③ 腭弓距黏膜 0.5–1.0 mm', size=22, anchor='mm',
           fill=(96, 104, 114))
    f.rrect((px1 - 60, py - 150, px1 - 10, py - 30), r=8, fill=METAL,
            outline=METAL_EDGE, width=2)
    f.text((px1 - 35, py - 90), '6', size=20, anchor='mm', fill=(90, 98, 108))
    f.text((px0 - 30, py + 40), '腭黏膜 / 骨面', size=22, anchor='lm',
           fill=(178, 106, 106))

    legend(f, (1140, 130, 1760, 440), [
        ('①', '带环：上颌第一恒磨牙（16 / 26）'),
        ('②', '腭弓：0.9–1.0 mm 不锈钢丝'),
        ('③', '腭弓距腭黏膜 0.5–1.0 mm（见剖面）'),
        ('④', '前腭托：厚 2–3 mm，边缘圆钝、均匀贴合'),
    ], size=24, gap=62, title='结构要点')
    return f.save(os.path.join(OUT, 'fig04_nance.png'))


# ------------------------------------------------------------------ 图 5 改良 Nance 弓
def fig05():
    f = Fig(1800, 1230)
    m, gap = 26, 22
    pw = (1800 - 2 * m - gap) / 2
    ph = (1230 - 2 * m - gap) / 2
    specs = [
        ('① 推磨牙向远中型', '上颌第一恒磨牙异位萌出 / 早期 II 类',
         '腭弓加圈曲或推簧 → 磨牙远中移动'),
        ('② 前方牵引支抗型', '安氏 III 类上颌后缩',
         '带环焊颊面管 / 牵引钩 + 面具'),
        ('③ 扩弓—保持型', '上颌横向不足合并间隙丧失',
         '腭中缝加螺旋扩弓器'),
        ('④ 骨支抗 / 固位改良型', '需绝对支抗或基牙条件差',
         '腭部微种植钉 / 改全冠固位'),
    ]
    for i, (title, cap, note) in enumerate(specs):
        r, c = divmod(i, 2)
        x0 = m + c * (pw + gap)
        y0 = m + r * (ph + gap)
        box = (x0, y0, x0 + pw, y0 + ph)
        f.panel(box, title=title)
        inner = (x0 + 20, y0 + 58, x0 + pw - 20, y0 + ph - 86)
        if i == 0:
            mini_modified(f, inner, 'spring')
        elif i == 1:
            info, (cx, cy, a, b) = mini_nance(f, inner)
            for sgn in (-1, 1):
                p0 = (cx + a * 0.62 * sgn, cy + b * 0.06)
                f.curved_arrow([p0, (cx + a * 0.42 * sgn, cy - b * 0.44),
                                (cx + a * 0.16 * sgn, cy - b * 0.78)], RED, 5, 17)
            f.text((cx, cy + b * 0.42), '前方牵引 300–500 g/侧 · 向前下 15°–30° · 12–14 h/日',
                   size=22, anchor='mm', fill=(150, 60, 60))
        elif i == 2:
            info, (cx, cy, a, b) = mini_nance(f, inner)
            f.rrect((cx - 74, cy - b * 0.42, cx + 74, cy + b * 0.10), r=6,
                    fill=(226, 232, 240), outline=(110, 122, 136), width=2)
            f.line([(cx - 74, cy - b * 0.42), (cx - 74, cy + b * 0.10)],
                   fill=(110, 122, 136), width=2)
            f.text((cx, cy - b * 0.16), '螺旋\n扩弓器', size=21, anchor='mm',
                   fill=(70, 82, 96))
            for sgn in (-1, 1):
                f.arrow((cx + 100 * sgn, cy - b * 0.16), (cx + 250 * sgn, cy - b * 0.16),
                        BLUE, 5, 16)
        else:
            info, (cx, cy, a, b) = mini_nance(f, inner)
            f.ellipse((cx - 26, cy - b * 0.34, cx + 26, cy - b * 0.34 + 52),
                      fill=METAL, outline=METAL_EDGE, width=3)
            f.line([(cx - 15, cy - b * 0.34 + 26), (cx + 15, cy - b * 0.34 + 26)],
                   fill=(80, 90, 100), width=3)
            f.line([(cx, cy - b * 0.34 + 10), (cx, cy - b * 0.34 + 42)],
                   fill=(80, 90, 100), width=3)
            f.text((cx, cy - b * 0.34 + 80), '腭部微种植钉', size=21, anchor='mm',
                   fill=(70, 82, 96))
            for num in ('16', '26'):
                x, y, ang, w, h = info[num]
            f.text((cx, cy + b * 0.55), '基牙改全冠 → 固位增强', size=21, anchor='mm',
                   fill=(70, 82, 96))
        caption(f, ((box[0] + box[2]) / 2, box[3] - 56), cap, size=24, bold=True,
                fill=(31, 54, 77))
        caption(f, ((box[0] + box[2]) / 2, box[3] - 24), note)
    return f.save(os.path.join(OUT, 'fig05_modified_nance.png'))


# ------------------------------------------------------------------ 图 6 决策流程
def fbox(f, cx, cy, w, h, lines, kind='box', fill=(238, 244, 250),
         edge=(120, 150, 180), tcol=(28, 60, 92), size=25, bold=False):
    if kind == 'box':
        f.rrect((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), r=12, fill=fill,
                outline=edge, width=2.2)
    elif kind == 'diamond':
        f.poly([(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)],
               fill=fill, outline=edge, width=2.2)
    if isinstance(lines, str):
        lines = [lines]
    n = len(lines)
    for i, s in enumerate(lines):
        f.text((cx, cy + (i - (n - 1) / 2) * (size * 1.35)), s, size=size,
               anchor='mm', fill=tcol, bold=bold)
    return (cx, cy, w, h)


def fig06():
    f = Fig(1800, 1240)
    spine = 300
    bx = 900          # 分支框中心
    fbox(f, spine, 70, 430, 92, '乳牙早失 + 影像评估', fill=(232, 240, 248),
         bold=True, size=27)
    d1 = fbox(f, spine, 235, 560, 132, ['继承恒牙', '6 个月内萌出？'], kind='diamond',
              fill=(255, 248, 232), edge=(210, 170, 90), size=26)
    fbox(f, bx + 120, 235, 560, 96, '定期观察，不做保持器', fill=(236, 250, 242),
         edge=(120, 190, 150), tcol=(24, 100, 62), size=26)
    d2 = fbox(f, spine, 430, 620, 132, ['第一恒磨牙已萌出、', '可戴带环？'],
              kind='diamond', fill=(255, 248, 232), edge=(210, 170, 90), size=26)
    fbox(f, bx + 120, 430, 560, 96, '远端靴式（引导恒磨牙萌出）', fill=(240, 244, 252),
         edge=(130, 150, 200), tcol=(40, 60, 130), size=26)
    d3 = fbox(f, spine, 640, 560, 132, ['缺隙类型？'], kind='diamond',
              fill=(255, 248, 232), edge=(210, 170, 90), size=26)
    fbox(f, bx + 150, 540, 620, 84, '单侧 → 带环 / 全冠丝圈式', size=26)
    fbox(f, bx + 150, 644, 620, 84, '双侧上颌 → Nance 腭弓', size=26)
    fbox(f, bx + 150, 748, 620, 84, '双侧下颌 → 固定舌弓', size=26)
    d4 = fbox(f, spine, 900, 640, 146, ['有早期矫治目标？', '（异位萌出 / 推磨牙 /', '前牵引 / 扩弓）'],
              kind='diamond', fill=(255, 248, 232), edge=(210, 170, 90), size=24)
    fbox(f, bx + 150, 900, 620, 110, ['是 → 改良 Nance 弓', '+ 推簧 / 颊面管 / 扩弓器'],
         fill=(250, 240, 250), edge=(160, 120, 185), tcol=(96, 40, 120), size=26)
    d5 = fbox(f, spine, 1090, 620, 132, ['口腔卫生 / 依从性差？'], kind='diamond',
              fill=(255, 248, 232), edge=(210, 170, 90), size=26)
    fbox(f, bx + 150, 1090, 620, 110, ['是 → 先控制龋病、强化菌斑控制；',
                                       '必要时改活动式装置'],
         fill=(253, 242, 242), edge=(215, 150, 150), tcol=(150, 50, 50), size=25)
    fbox(f, spine, 1210, 430, 60, '戴入 → 定期复查', fill=(232, 240, 248), bold=True,
         size=25)

    def varrow(y0, y1):
        f.arrow((spine, y0), (spine, y1), (120, 132, 146), 4, 15)

    varrow(116, 169)
    varrow(301, 364)
    varrow(496, 574)
    varrow(706, 827)
    varrow(973, 1024)
    varrow(1156, 1180)
    f.arrow((spine + 300, 235), (bx - 160, 235), GREEN, 4, 15)
    f.text((spine + 330, 210), '是', size=24, fill=GREEN, bold=True)
    f.arrow((spine + 320, 430), (bx - 160, 430), BLUE, 4, 15)
    f.text((spine + 350, 405), '否', size=24, fill=BLUE, bold=True)
    for yy in (540, 644, 748):
        f.arrow((spine + 120, 640 + (yy - 640) * 0.25), (bx - 170, yy), (120, 132, 146), 4, 14)
    f.arrow((spine + 330, 900), (bx - 170, 900), (150, 110, 180), 4, 15)
    f.text((spine + 360, 872), '是', size=24, fill=(150, 110, 180), bold=True)
    f.arrow((spine + 320, 1090), (bx - 170, 1090), (200, 90, 90), 4, 15)
    f.text((spine + 350, 1062), '是', size=24, fill=(200, 90, 90), bold=True)
    f.text((900, 30), '固定式间隙保持器 · 装置选择决策流程', size=34, bold=True,
           anchor='mm', fill=(31, 54, 77))
    return f.save(os.path.join(OUT, 'fig06_decision_flow.png'))


# ------------------------------------------------------------------ 图 7 操作流程
def fig07():
    f = Fig(1800, 620)
    f.text((900, 46), '操作流程（固定式保持器 / 改良 Nance 弓通用）', size=34,
           bold=True, anchor='mm', fill=(31, 54, 77))
    steps = [
        ('1', '术前评估', '影像 · 间隙 · 基牙'),
        ('2', '试带环', '就位 · 密合 · 无干扰'),
        ('3', '取模灌模', '带环须嵌于印模内'),
        ('4', '技工制作', '丝圈 / 腭弓 / 腭托'),
        ('5', '试戴调整', '组织避让 · 咬合'),
        ('6', '粘接', '严格隔湿 · 去净多余'),
        ('7', '医嘱宣教', '清洁 · 饮食 · 复查'),
        ('8', '定期复查', '3–6 个月 / 4–6 周'),
    ]
    w, h, gap = 196, 190, 22
    x = (1800 - (8 * w + 7 * gap)) / 2
    y = 150
    for i, (n, t, s) in enumerate(steps):
        x0 = x + i * (w + gap)
        f.rrect((x0, y, x0 + w, y + h), r=14, fill=(240, 246, 252),
                outline=(150, 175, 205), width=2)
        f.ellipse((x0 + w / 2 - 24, y + 16, x0 + w / 2 + 24, y + 64), fill=(31, 54, 77))
        f.text((x0 + w / 2, y + 40), n, size=28, bold=True, anchor='mm', fill=WHITE,
               halo=0)
        f.text((x0 + w / 2, y + 96), t, size=27, bold=True, anchor='mm',
               fill=(28, 60, 92))
        f.text((x0 + w / 2, y + 140), s, size=21, anchor='mm', fill=(96, 104, 114))
        if i < 7:
            f.arrow((x0 + w + 3, y + h / 2), (x0 + w + gap - 3, y + h / 2),
                    (140, 152, 166), 5, 15)
    f.rrect((150, 400, 1650, 560), r=14, fill=(253, 250, 240),
            outline=(226, 208, 160), width=1.8)
    f.text((900, 440), '关键点', size=27, bold=True, anchor='mm', fill=(150, 110, 20))
    f.text((900, 492),
           '① 隔湿是粘接成功的关键　② 丝圈/腭弓距组织 0.5–1.0 mm　'
           '③ 腭托边缘圆钝、均匀贴合　④ 咬合无干扰',
           size=25, anchor='mm', fill=(90, 80, 50))
    f.text((900, 532), '⑤ 加力型装置 4–6 周复诊，保持型 3–6 个月复查',
           size=25, anchor='mm', fill=(90, 80, 50))
    return f.save(os.path.join(OUT, 'fig07_steps.png'))


# ------------------------------------------------------------------ 图 8 对错对比
def frag_gingiva(f, box, ok=True):
    b = Box(f, box)
    gy = b.Y(0.70)
    f.rect((b.X(0.06), gy, b.X(0.94), b.Y(0.96)), fill=GINGIVA)
    f.line([(b.X(0.06), gy), (b.X(0.94), gy)], fill=GINGIVA_EDGE, width=3)
    y = gy - b.h * (0.30 if ok else 0.02)
    f.wire([(b.X(0.08), y), (b.X(0.92), y)], width=6)
    if ok:
        f.arrow((b.X(0.80), gy - 6), (b.X(0.80), y + 6), BLUE, 3, 12)
        f.arrow((b.X(0.80), y + 6), (b.X(0.80), gy - 6), BLUE, 3, 12)
        f.text((b.X(0.72), (gy + y) / 2), '0.5–1.0 mm', size=22, anchor='rm',
               fill=BLUE)
    else:
        f.ellipse((b.X(0.40), gy - 10, b.X(0.60), gy + 26), fill=(240, 170, 170))
        f.text((b.X(0.86), b.Y(0.56)), '压迫\n牙龈', size=21, anchor='mm', fill=RED)


def frag_button(f, box, ok=True):
    b = Box(f, box)
    my = b.Y(0.78)
    f.rect((b.X(0.04), my, b.X(0.96), b.Y(0.96)), fill=PALATE)
    f.line([(b.X(0.04), my), (b.X(0.96), my)], fill=(226, 170, 170), width=2)
    if ok:
        f.hatch((b.X(0.18), my - b.h * 0.42, b.X(0.82), my), shape='rrect', spacing=10)
        f.text((b.X(0.5), my - b.h * 0.21), '均匀贴合', size=22, anchor='mm',
               fill=(120, 80, 140))
    else:
        f.hatch((b.X(0.18), my - b.h * 0.46, b.X(0.82), my - b.h * 0.16),
                shape='rrect', spacing=10)
        f.ellipse((b.X(0.42), my - b.h * 0.20, b.X(0.58), my), fill=(240, 170, 170))
        f.text((b.X(0.5), my - b.h * 0.56), '局部高点、悬空', size=22, anchor='mm',
               fill=RED)


def frag_embrasure(f, box, ok=True):
    b = Box(f, box)
    W, H = b.w * 0.30, b.h * 0.62
    for cx in (b.X(0.32), b.X(0.68)):
        f.rrect((cx - W / 2, b.Y(0.22), cx + W / 2, b.Y(0.22) + H), r=14,
                fill=ENAMEL, outline=ENAMEL_LINE, width=2.4)
    cy = b.Y(0.52) if ok else b.Y(0.86)
    f.wire([(b.X(0.30), cy), (b.X(0.70), cy)], width=6)
    if ok:
        f.text((b.X(0.5), b.Y(0.30)), '抵于邻面外形高点', size=22, anchor='mm',
               fill=GREEN)
    else:
        f.text((b.X(0.5), b.Y(0.30)), '进入倒凹', size=22, anchor='mm', fill=RED)
        f.arrow((b.X(0.86), b.Y(0.60)), (b.X(0.72), b.Y(0.84)), RED, 3, 12)


def frag_band(f, box, ok=True):
    b = Box(f, box)
    W = b.w * 0.42
    f.rrect((b.X(0.5) - W / 2, b.Y(0.16), b.X(0.5) + W / 2, b.Y(0.86)), r=16,
            fill=ENAMEL, outline=ENAMEL_LINE, width=2.4)
    y0 = b.Y(0.56) if ok else b.Y(0.50)
    f.rrect((b.X(0.5) - W / 2 - (2 if ok else 8), y0, b.X(0.5) + W / 2 + (2 if ok else 8),
             b.Y(0.88)), r=8, fill=METAL, outline=METAL_EDGE, width=2.4)
    if ok:
        f.text((b.X(0.5), b.Y(0.10)), '边缘密合', size=22, anchor='mm', fill=GREEN)
    else:
        f.text((b.X(0.5), b.Y(0.10)), '悬突 + 菌斑堆积', size=22, anchor='mm', fill=RED)
        for dx in (-0.60, -0.42, 0.42, 0.60):
            f.ellipse((b.X(0.5 + dx * 0.36) - 7, b.Y(0.94) - 7,
                       b.X(0.5 + dx * 0.36) + 7, b.Y(0.94) + 7), fill=(120, 170, 90))


def fig08():
    f = Fig(1800, 1320)
    f.text((900, 40), '常见错误对照（左侧正确 · 右侧错误）', size=34, bold=True,
           anchor='mm', fill=(31, 54, 77))
    rows = [
        ('丝圈与牙龈的距离', frag_gingiva, '距牙龈 0.5–1.0 mm', '压迫牙龈'),
        ('腭托与腭黏膜的贴合', frag_button, '组织面均匀贴合', '局部高点、压迫'),
        ('丝圈与邻牙的关系', frag_embrasure, '抵于外形高点', '进入倒凹、压龈'),
        ('带环边缘', frag_band, '密合无悬突', '悬突、滞留菌斑'),
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
        fn(f, (lx[0] + 62, lx[1] + 8, lx[2] - 12, lx[3] - 36), True)
        fn(f, (rx[0] + 62, rx[1] + 8, rx[2] - 12, rx[3] - 36), False)
        f.text((lx[0] + 32, (lx[1] + lx[3]) / 2), '√', size=46, bold=True, fill=GREEN,
               anchor='mm')
        f.text(((lx[0] + lx[2]) / 2 + 20, lx[3] - 24), gt, size=23, anchor='mm',
               fill=(24, 100, 62))
        f.text((rx[0] + 32, (rx[1] + rx[3]) / 2), '×', size=46, bold=True, fill=RED,
               anchor='mm')
        f.text(((rx[0] + rx[2]) / 2 + 20, rx[3] - 24), bt, size=23, anchor='mm',
               fill=(160, 50, 50))
    return f.save(os.path.join(OUT, 'fig08_dos_donts.png'))


# ------------------------------------------------------------------ 图 9 复诊时间轴
def fig09():
    f = Fig(1800, 560)
    f.text((900, 44), '复诊与维护时间轴', size=34, bold=True, anchor='mm',
           fill=(31, 54, 77))
    y = 300
    f.line([(120, y), (1700, y)], fill=(150, 162, 176), width=6)
    nodes = [
        ('戴入当天', '医嘱 + 清洁示范', 190, 1),
        ('1 周', '装置稳定与组织反应', 500, -1),
        ('1 个月', '基牙与软组织', 810, 1),
        ('每 3–6 个月', '保持型复查', 1150, -1),
        ('每 4–6 周', '加力型复查', 1460, 1),
        ('拆除', '恒牙萌出到位', 1720, -1),
    ]
    for label, sub, x, side in nodes:
        f.ellipse((x - 17, y - 17, x + 17, y + 17), fill=(31, 54, 77))
        ty = y - 62 if side > 0 else y + 62
        f.text((x, ty), label, size=27, bold=True, anchor='mm', fill=(28, 60, 92))
        f.text((x, ty + (36 if side > 0 else -36)), sub, size=21, anchor='mm',
               fill=(96, 104, 114))
        f.line([(x, y - 20 if side > 0 else y + 20), (x, ty + (20 if side > 0 else -20))],
               fill=(180, 188, 198), width=1.6)
    return f.save(os.path.join(OUT, 'fig09_timeline.png'))


# ------------------------------------------------------------------ 图 10 加力
def fig10():
    f = Fig(1800, 820)
    f.rrect((30, 30, 880, 790), r=14, fill=(252, 253, 254), outline=(216, 222, 229),
            width=1.6)
    f.text((455, 70), '推磨牙向远中', size=30, bold=True, anchor='mm', fill=(31, 54, 77))
    info, (cx, cy, a, b) = mini_nance(f, (90, 110, 820, 660))
    for sgn in (-1, 1):
        pts = arch_curve(cx, cy, a, b, 0.74, 1.18 * sgn, 1.86 * sgn, 8)
        f.curved_arrow(pts, RED, 5, 17)
        q = arch_curve(cx, cy, a, b, 0.74, 1.05 * sgn, 1.05 * sgn, 1)[0]
        wire_circle(f, q[0], q[1], 13, 13, width=5)
    f.text((455, 700), '轻力、少量多次：约 0.5–1.0 mm / 次', size=25, anchor='mm',
           fill=(90, 98, 108))
    f.text((455, 742), '每 4–6 周复诊 1 次，避免牙根吸收', size=25, anchor='mm',
           fill=(90, 98, 108))

    f.rrect((920, 30, 1770, 790), r=14, fill=(252, 253, 254), outline=(216, 222, 229),
            width=1.6)
    f.text((1345, 70), '前方牵引（改良 Nance 弓 + 面具）', size=30, bold=True,
           anchor='mm', fill=(31, 54, 77))
    info, (cx, cy, a, b) = mini_nance(f, (980, 110, 1710, 660))
    for sgn in (-1, 1):
        p0 = (cx + a * 0.66 * sgn, cy + b * 0.02)
        f.curved_arrow([p0, (cx + a * 0.48 * sgn, cy - b * 0.42),
                        (cx + a * 0.20 * sgn, cy - b * 0.76)], RED, 5, 17)
    f.text((cx, cy + b * 0.46), '300–500 g/侧 · 向前下 15°–30° · 12–14 h/日',
           size=24, anchor='mm', fill=(160, 60, 60))
    f.text((1345, 700), '腭托分散反作用力、减少磨牙近中移动', size=25, anchor='mm',
           fill=(90, 98, 108))
    f.text((1345, 742), '配合面具佩戴时间不足则疗效不可预期', size=25, anchor='mm',
           fill=(90, 98, 108))
    return f.save(os.path.join(OUT, 'fig10_force.png'))


# ------------------------------------------------------------------ 图 11 拆除时机
def fig11():
    f = Fig(1760, 780)

    def draw_panel(x0, ok):
        f.rrect((x0, 30, x0 + 820, 750), r=14, fill=(252, 253, 254),
                outline=(216, 222, 229), width=1.6)
        cx = x0 + 410
        f.text((cx, 74), '可以拆除' if ok else '继续戴用', size=30, bold=True,
               anchor='mm', fill=(GREEN if ok else AMBER))
        # 骨 / 牙龈
        crest = 330 if ok else 250
        f.rect((x0 + 110, crest, x0 + 710, 690), fill=(246, 240, 232))
        f.line([(x0 + 110, crest), (x0 + 710, crest)], fill=(186, 176, 160), width=3)
        f.line([(x0 + 110, crest - 34), (x0 + 710, crest - 34)], fill=GINGIVA_EDGE,
               width=6)
        f.text((x0 + 130, crest + 30), '骨面 / 牙槽嵴', size=21, anchor='lm',
               fill=(150, 138, 120))
        # 继承恒牙
        top = crest - 30 if ok else crest + 34
        f.rrect((cx - 78, top, cx + 78, top + 116), r=14, fill=ENAMEL,
                outline=ENAMEL_LINE, width=2.6)
        f.line([(cx - 40, top + 116), (cx - 46, top + 300)], fill=ENAMEL_LINE, width=6)
        f.line([(cx + 40, top + 116), (cx + 46, top + 300)], fill=ENAMEL_LINE, width=6)
        f.text((cx, top + 52), '继承恒牙', size=22, anchor='mm', fill=(110, 118, 128))
        # 邻牙
        for sgn in (-1, 1):
            f.rrect((cx + sgn * 210 - 74, crest - 150, cx + sgn * 210 + 74,
                     crest + 140), r=14, fill=(248, 246, 240), outline=ENAMEL_LINE,
                    width=2.4)
        # 牙根形成标注
        l1 = 560
        f.text((cx, l1), '牙根形成 2/3 以上' if ok else '牙根形成不足 2/3',
               size=24, anchor='mm', fill=(90, 98, 108))
        f.text((cx, l1 + 42), '骨覆盖消失、临床可触及' if ok else '骨覆盖仍存在',
               size=24, anchor='mm', fill=(90, 98, 108))
        f.text((cx, l1 + 84), '邻接关系已建立' if ok else '邻牙尚未建立邻接',
               size=24, anchor='mm', fill=(90, 98, 108))
        if ok:
            f.text((cx, 712), '拆除后仍需定期随访', size=24, anchor='mm', fill=GREEN)
        else:
            f.text((cx, 712), '过早拆除 → 间隙再度丧失', size=24, anchor='mm',
                   fill=AMBER)

    draw_panel(40, True)
    draw_panel(900, False)
    f.text((880, 762), '拆除时机判断（影像学 + 临床）', size=30, bold=True,
           anchor='mm', fill=(31, 54, 77))
    return f.save(os.path.join(OUT, 'fig11_removal.png'))


# ------------------------------------------------------------------ 图 12 病例
def fig12():
    f = Fig(1800, 1240)
    f.text((900, 40), '典型病例示意', size=34, bold=True, anchor='mm',
           fill=(31, 54, 77))
    m, gap = 26, 22
    pw = (1800 - 2 * m - gap) / 2
    ph = (1240 - 120 - 2 * m - gap) / 2
    y0base = 96

    def panel(i, title, sub, drawfn):
        r, c = divmod(i, 2)
        x0 = m + c * (pw + gap)
        y0 = y0base + r * (ph + gap)
        box = (x0, y0, x0 + pw, y0 + ph)
        f.panel(box, title=title)
        inner = (x0 + 20, y0 + 56, x0 + pw - 20, y0 + ph - 84)
        drawfn(f, inner)
        caption(f, ((box[0] + box[2]) / 2, box[3] - 56), sub, size=23, bold=True,
                fill=(31, 54, 77))
        caption(f, ((box[0] + box[2]) / 2, box[3] - 24),
                {'0': '红圈 = 缺隙　→ 带环丝圈式（基牙 75）',
                 '1': '红圈 = 双侧缺隙　→ Nance 腭弓',
                 '2': '红圈 = 异位萌出的 16　→ 改良 Nance 弓 + 推簧',
                 '3': '红箭头 = 前牵引方向　→ 改良 Nance 弓 + 颊面管 + 面具'}[str(i)], size=22)

    def c1(f, box):
        info, (cx, cy, a, b) = draw_arch(f, box, arch=ARCH_MAND, a_frac=0.40,
                                         b_frac=0.40, cy_frac=0.56, numbers=True,
                                         bands=('75',), missing=('74',), scale=0.90,
                                         mirror_sgn=-1)
        x, y, ang, w, h = info['74']
        f.ellipse((x - w * 0.72, y - h * 0.72, x + w * 0.72, y + h * 0.72),
                  outline=RED, width=4)

    def c2(f, box):
        info, (cx, cy, a, b) = mini_nance(f, box, numbers=True)
        for num in ('55',):
            x, y, ang, w, h = info[num]
            f.ellipse((x - w * 0.72, y - h * 0.72, x + w * 0.72, y + h * 0.72),
                      outline=RED, width=4)
        x, y, ang, w, h = info['65']
        f.ellipse((x - w * 0.72, y - h * 0.72, x + w * 0.72, y + h * 0.72),
                  outline=RED, width=4)

    def c3(f, box):
        info, (cx, cy, a, b) = mini_nance(f, box, numbers=True)
        x, y, ang, w, h = info['16']
        f.ellipse((x - w * 0.78, y - h * 0.78, x + w * 0.78, y + h * 0.78),
                  outline=RED, width=4)
        pts = arch_curve(cx, cy, a, b, 0.74, -1.10, -1.80, 8)
        f.curved_arrow(pts, RED, 5, 16)
        q = arch_curve(cx, cy, a, b, 0.74, -1.00, -1.00, 1)[0]
        wire_circle(f, q[0], q[1], 13, 13, width=5)

    def c4(f, box):
        info, (cx, cy, a, b) = mini_nance(f, box, numbers=True)
        for sgn in (-1, 1):
            p0 = (cx + a * 0.66 * sgn, cy + b * 0.02)
            f.curved_arrow([p0, (cx + a * 0.46 * sgn, cy - b * 0.44),
                            (cx + a * 0.18 * sgn, cy - b * 0.80)], RED, 5, 16)

    panel(0, '病例 1　6 岁 4 个月 · 男', '左下第一乳磨牙因龋拔除，75 完好', c1)
    panel(1, '病例 2　7 岁 1 个月 · 女', '双侧上颌第二乳磨牙早失', c2)
    panel(2, '病例 3　7 岁 8 个月 · 男', '16 异位萌出（可复性）', c3)
    panel(3, '病例 4　8 岁 2 个月 · 女', '上颌后缩，安氏 III 类（拟前牵引）', c4)
    return f.save(os.path.join(OUT, 'fig12_cases.png'))


if __name__ == '__main__':
    for fn in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09,
               fig10, fig11, fig12):
        print(fn())
