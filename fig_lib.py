# -*- coding: utf-8 -*-
"""示意图绘制库：牙齿、弓丝、带环、腭托等图元 + 各类装置示意。"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 3  # supersample

FONT_REG = r'C:\Windows\Fonts\msyh.ttc'
FONT_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'

_fc = {}


def font(size, bold=False):
    key = (int(size), bold)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FONT_BOLD if bold else FONT_REG,
                                      max(6, int(size * S)), index=0)
    return _fc[key]


INK = (52, 60, 70)
GREY = (128, 136, 146)
LIGHT = (233, 237, 241)
WHITE = (255, 255, 255)
ENAMEL = (250, 248, 242)
ENAMEL_LINE = (126, 133, 142)
GROOVE = (176, 183, 192)
WIRE = (188, 194, 202)
WIRE_EDGE = (104, 112, 122)
METAL = (203, 209, 217)
METAL_EDGE = (104, 112, 122)
ACRYLIC = (233, 216, 240)
ACRYLIC_EDGE = (146, 106, 168)
GINGIVA = (249, 216, 216)
GINGIVA_EDGE = (231, 173, 173)
PALATE = (250, 222, 222)
ALVEOLAR = (247, 206, 206)
RED = (198, 58, 58)
BLUE = (36, 106, 176)
GREEN = (32, 140, 96)
AMBER = (206, 138, 30)
DASH = (168, 176, 186)


class Fig:
    def __init__(self, w, h, bg=WHITE):
        self.W, self.H, self.S = w, h, S
        self.img = Image.new('RGB', (w * S, h * S), bg)
        self.d = ImageDraw.Draw(self.img)

    # ---------------- primitives (final-pixel coordinates) ----------------
    def line(self, pts, fill=INK, width=3, joint='curve'):
        self.d.line([(p[0] * S, p[1] * S) for p in pts], fill=fill,
                    width=max(1, int(width * S)), joint=joint)

    def wire(self, pts, width=7, edge=WIRE_EDGE, core=WIRE):
        self.line(pts, fill=edge, width=width + 3)
        self.line(pts, fill=core, width=width)

    def rrect(self, box, r=10, fill=None, outline=None, width=2):
        self.d.rounded_rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                                 radius=r * S, fill=fill, outline=outline,
                                 width=max(1, int(width * S)))

    def rect(self, box, fill=None, outline=None, width=2):
        self.d.rectangle([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                         fill=fill, outline=outline, width=max(1, int(width * S)))

    def ellipse(self, box, fill=None, outline=None, width=2):
        self.d.ellipse([box[0] * S, box[1] * S, box[2] * S, box[3] * S],
                       fill=fill, outline=outline, width=max(1, int(width * S)))

    def arc(self, box, start, end, fill=INK, width=3):
        self.d.arc([box[0] * S, box[1] * S, box[2] * S, box[3] * S], start, end,
                   fill=fill, width=max(1, int(width * S)))

    def poly(self, pts, fill=None, outline=None, width=2):
        self.d.polygon([(p[0] * S, p[1] * S) for p in pts], fill=fill,
                       outline=outline, width=max(1, int(width * S)))

    def text(self, xy, s, size=26, fill=INK, anchor='la', bold=False,
             halo=2, align='center'):
        self.d.text((xy[0] * S, xy[1] * S), s, font=font(size, bold), fill=fill,
                    anchor=anchor, align=align,
                    stroke_width=int(halo * S) if halo else 0,
                    stroke_fill=WHITE)

    def arrow(self, p1, p2, color=RED, width=5, head=17):
        ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        L = head
        base = (p2[0] - L * math.cos(ang), p2[1] - L * math.sin(ang))
        self.line([p1, base], fill=color, width=width)
        w2 = head * 0.46
        self.poly([p2,
                   (base[0] + w2 * math.sin(ang), base[1] - w2 * math.cos(ang)),
                   (base[0] - w2 * math.sin(ang), base[1] + w2 * math.cos(ang))],
                  fill=color)

    def curved_arrow(self, pts, color=RED, width=5, head=17):
        self.line(pts, fill=color, width=width)
        p1, p2 = pts[-2], pts[-1]
        ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
        L = head
        base = (p2[0] - L * math.cos(ang), p2[1] - L * math.sin(ang))
        w2 = head * 0.46
        self.poly([p2,
                   (base[0] + w2 * math.sin(ang), base[1] - w2 * math.cos(ang)),
                   (base[0] - w2 * math.sin(ang), base[1] + w2 * math.cos(ang))],
                  fill=color)

    def leader(self, txt_xy, pt_xy, s, size=23, color=INK, anchor='la',
               bold=False, dot=True, lw=1.6):
        self.line([txt_xy, pt_xy], fill=(150, 158, 168), width=lw)
        if dot:
            self.ellipse([pt_xy[0] - 3, pt_xy[1] - 3, pt_xy[0] + 3, pt_xy[1] + 3],
                         fill=color)
        self.text(txt_xy, s, size=size, fill=color, anchor=anchor, bold=bold)

    def panel(self, box, title=None, fill=(252, 253, 254), edge=(214, 220, 227),
              radius=14, tsize=28):
        self.rrect(box, r=radius, fill=fill, outline=edge, width=1.6)
        if title:
            self.rrect((box[0], box[1], box[2], box[1] + 42), r=radius,
                       fill=(238, 242, 246), outline=None)
            self.rect((box[0], box[1] + 30, box[2], box[1] + 42), fill=(238, 242, 246))
            self.text(((box[0] + box[2]) / 2, box[1] + 21), title, size=tsize,
                      anchor='mm', bold=True, fill=(31, 54, 77))

    def hatch(self, box, shape='ellipse', fill=ACRYLIC, line_col=ACRYLIC_EDGE,
              spacing=11, width=1.6, angle=45):
        """在指定形状内绘制斜线阴影（用于丙烯酸腭托）。"""
        x0, y0, x1, y1 = [v * S for v in box]
        w, h = int(x1 - x0) + 2, int(y1 - y0) + 2
        if w <= 0 or h <= 0:
            return
        mask = Image.new('L', (w, h), 0)
        md = ImageDraw.Draw(mask)
        if shape == 'ellipse':
            md.ellipse([0, 0, w - 1, h - 1], fill=255)
        else:
            md.rounded_rectangle([0, 0, w - 1, h - 1], radius=int(min(w, h) * 0.35),
                                 fill=255)
        pat = Image.new('RGB', (w, h), fill)
        pd = ImageDraw.Draw(pat)
        step = int(spacing * S)
        n = int((w + h) / max(1, step)) + 4
        for i in range(-2, n):
            off = i * step
            pd.line([(off, 0), (off - h, h)], fill=line_col, width=max(1, int(width * S)))
        self.img.paste(pat, (int(x0), int(y0)), mask)
        # 轮廓
        self.ellipse(box, outline=line_col, width=1.8) if shape == 'ellipse' else \
            self.rrect(box, r=min(box[2] - box[0], box[3] - box[1]) * 0.35,
                       outline=line_col, width=1.8)

    def save(self, path):
        out = self.img.resize((self.W, self.H), Image.LANCZOS)
        out.save(path)
        return path


class Box:
    """把归一化坐标映射到画布上的一个面板区域。"""

    def __init__(self, fig, box, pad=0.0):
        self.f = fig
        x0, y0, x1, y1 = box
        dx, dy = (x1 - x0) * pad, (y1 - y0) * pad
        self.x0, self.y0 = x0 + dx, y0 + dy
        self.x1, self.y1 = x1 - dx, y1 - dy
        self.w, self.h = self.x1 - self.x0, self.y1 - self.y0

    def X(self, u):
        return self.x0 + u * self.w

    def Y(self, v):
        return self.y0 + v * self.h

    def P(self, u, v):
        return (self.X(u), self.Y(v))

    def U(self, s):
        """按宽度比例换算长度（用于字号、线宽、牙齿尺寸）。"""
        return s * min(self.w, self.h * 1.1)


# ------------------------------------------------------------------ 颊面观牙齿
def tooth_buccal(f, cx, top, w, h, kind='molar', crown=False, dashed=False,
                 num=None, num_size=20):
    """颊面观牙冠：两个牙尖 + 中央沟；crown=True 时整体为金属全冠。"""
    fill = METAL if crown else ENAMEL
    edge = METAL_EDGE if crown else ENAMEL_LINE
    pts = [(cx - w / 2, top + h * 0.30),
           (cx - w * 0.30, top + h * 0.02),
           (cx - w * 0.07, top + h * 0.20),
           (cx + w * 0.07, top + h * 0.20),
           (cx + w * 0.30, top + h * 0.02),
           (cx + w / 2, top + h * 0.30),
           (cx + w / 2, top + h),
           (cx - w / 2, top + h)]
    if dashed:
        f.poly(pts, fill=(248, 249, 251), outline=DASH, width=1.6)
    else:
        f.poly(pts, fill=fill, outline=edge, width=2.2)
    if not crown:
        f.line([(cx, top + h * 0.22), (cx, top + h * 0.62)], fill=GROOVE, width=2)
    if num:
        f.text((cx, top + h * 0.72), num, size=num_size, anchor='mm',
               fill=(120, 128, 138), halo=0)
    return pts


def band(f, cx, top, w, h, h_frac=0.40, num=None):
    """带环：覆盖牙冠颈 1/3 的金属环。"""
    y0 = top + h * (1 - h_frac)
    f.rrect((cx - w / 2 - 2, y0, cx + w / 2 + 2, top + h), r=6,
            fill=METAL, outline=METAL_EDGE, width=2.2)
    if num:
        f.text((cx, y0 + h * h_frac * 0.55), num, size=17, anchor='mm',
               fill=(96, 104, 114), halo=0)


def gingiva(f, box, top_v=0.80, label=None, label_size=22):
    """牙龈 / 牙槽黏膜带（颊面观）。"""
    x0, x1 = box.X(0.0), box.X(1.0)
    y0, y1 = box.Y(top_v), box.Y(1.0)
    f.rect((x0, y0, x1, y1), fill=GINGIVA)
    f.line([(x0, y0), (x1, y0)], fill=GINGIVA_EDGE, width=2)
    if label:
        f.text(((x0 + x1) / 2, (y0 + y1) / 2 + 4), label, size=label_size,
               anchor='mm', fill=(178, 106, 106), halo=1)


def missing_tooth(f, cx, top, w, h, label='缺隙', num=None):
    """缺牙位置：虚线轮廓 + 标注。"""
    tooth_buccal(f, cx, top, w, h, dashed=True, num=num)
    f.text((cx, top + h * 0.42), label, size=21, anchor='mm', fill=(150, 158, 168))


# ------------------------------------------------------------------ 合面观牙弓
def arch_layout(cx, cy, a, b, ts):
    out = []
    for t in ts:
        x = cx + a * math.sin(t)
        y = cy - b * math.cos(t)
        ang = math.degrees(math.atan2(b * math.sin(t), a * math.cos(t)))
        out.append((x, y, -ang))
    return out


def tooth_occl(f, cx, cy, w, h, angle=0, kind='molar', number=None,
               tone=None, edge=None, band=False, crown=False, dashed=False):
    """合面观牙齿（可旋转）：圆角外形 + 牙尖/中央沟；band=带环，crown=全冠。"""
    W, H = w * S, h * S
    pad = 0.9
    tmp = Image.new('RGBA', (int(W * (1 + pad)) + 6, int(H * (1 + pad)) + 6),
                    (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    X, Y = tmp.width / 2, tmp.height / 2
    fill = METAL if crown else (tone or ENAMEL)
    line = METAL_EDGE if crown else (edge or ENAMEL_LINE)
    if band:
        td.rounded_rectangle([X - W * 0.62, Y - H * 0.62, X + W * 0.62, Y + H * 0.62],
                             radius=min(W, H) * 0.30, fill=METAL,
                             outline=METAL_EDGE, width=int(2.2 * S))
    td.rounded_rectangle([X - W / 2, Y - H / 2, X + W / 2, Y + H / 2],
                         radius=min(W, H) * 0.28, fill=fill, outline=line,
                         width=int(2.3 * S))
    if dashed:
        td.rounded_rectangle([X - W / 2, Y - H / 2, X + W / 2, Y + H / 2],
                             radius=min(W, H) * 0.28, outline=(196, 202, 210),
                             width=int(2.4 * S))
    elif kind == 'molar':
        r = min(W, H) * 0.135
        for dx, dy in ((-0.235, -0.235), (0.235, -0.235), (-0.235, 0.235), (0.235, 0.235)):
            td.ellipse([X + dx * W - r, Y + dy * H - r, X + dx * W + r, Y + dy * H + r],
                       outline=GROOVE, width=int(1.7 * S))
        td.line([X - W * 0.36, Y, X + W * 0.36, Y], fill=GROOVE, width=int(2 * S))
    else:
        td.line([X - W * 0.20, Y - H * 0.24, X + W * 0.20, Y + H * 0.22],
                fill=GROOVE, width=int(1.7 * S))
    if angle:
        tmp = tmp.rotate(angle, resample=Image.BICUBIC, expand=True)
    f.img.paste(tmp, (int(cx * S - tmp.width / 2), int(cy * S - tmp.height / 2)), tmp)
    if number:
        f.text((cx, cy), number, size=19, anchor='mm', fill=(118, 126, 136), halo=0)


ARCH_MAX = [
    # (t, kind, w, h, number)
    (0.15, 'incisor', 62, 76, '11'),
    (0.45, 'incisor', 54, 68, '12'),
    (0.74, 'canine', 58, 72, '13'),
    (1.05, 'molar', 84, 88, '54'),
    (1.36, 'molar', 92, 96, '55'),
    (1.68, 'molar', 100, 104, '16'),
]

ARCH_MAND = [
    (0.15, 'incisor', 54, 66, '31'),
    (0.45, 'incisor', 50, 62, '32'),
    (0.74, 'canine', 56, 68, '33'),
    (1.05, 'molar', 84, 88, '74'),
    (1.36, 'molar', 92, 96, '75'),
    (1.68, 'molar', 100, 104, '36'),
]


MIRROR = {1: 2, 2: 1, 3: 4, 4: 3, 5: 6, 6: 5, 7: 8, 8: 7}


def mirror_num(n):
    return str(MIRROR[int(n[0])]) + n[1:]


def draw_arch(f, box, arch=ARCH_MAX, a_frac=0.40, b_frac=0.40, cy_frac=0.42,
              palate=True, numbers=True, scale=1.0, bands=(), crowns=(),
              missing=(), mirror_sgn=1):
    """绘制牙弓（合面观）。返回 {number: (x, y, angle, w, h)} 便于后续标注。"""
    if not isinstance(box, Box):
        box = Box(f, box)
    cx, cy = box.X(0.5), box.Y(cy_frac)
    b = min(box.w * b_frac, box.h * 0.46)
    a = min(box.w * a_frac, b * 1.20)
    unit = box.w / 1500.0
    if palate:
        f.ellipse((cx - a * 1.02, cy - b * 1.02, cx + a * 1.02, cy + b * 1.02),
                  fill=PALATE)
        f.ellipse((cx - a * 1.16, cy - b * 1.16, cx + a * 1.16, cy + b * 1.16),
                  outline=ALVEOLAR, width=max(2, 16 * unit))
    info = {}
    for sgn in (-1, 1):
        for (t, kind, w, h, num) in arch:
            shown = mirror_num(num) if sgn == mirror_sgn else num
            x, y, ang = arch_layout(cx, cy, a, b, [sgn * t])[0]
            tooth_occl(f, x, y, w * unit * scale, h * unit * scale, ang, kind,
                       number=(shown if numbers else None),
                       band=(shown in bands), crown=(shown in crowns),
                       dashed=(shown in missing))
            info[shown] = (x, y, ang, w * unit * scale, h * unit * scale)
    return info, (cx, cy, a, b)


def lingual_offset(cx, cy, a, b, ts, k=0.80, side=None):
    """舌/腭侧弓丝路径（牙弓内侧偏移曲线）。"""
    pts = []
    for t in ts:
        pts.append((cx + a * k * math.sin(t), cy - b * k * math.cos(t)))
    return pts
