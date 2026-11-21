#!/usr/bin/env python3
"""The Catalogue Photo of an Impossible Gadget.

Draws, from scratch with Pillow only, a studio catalogue photograph of an
impossible gadget: the LeafCheck BP-1, a pocket blood-pressure monitor for
houseplants.  The device's cuff grips the plant's stem mid-measurement,
its gauge needle sits in the green zone and its screen reads 120/80 --
the plant's blood pressure, taken seriously.  The potted plant is the
single accessory (the patient).  No network, no external images.

Output: /output/entry.png  (PNG, 1024x1024, <= 1 MiB)
Run:  python3 main.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.environ.get("OUTPUT_PATH", "/output/entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()

F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)
F_MONO = lambda s: font("DejaVuSansMono-Bold.ttf", s)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def leaf_points(cx, cy, length, width, angle_deg):
    """Pointed leaf outline, base at (cx, cy), tip along angle."""
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)          # tip direction
    px, py = -dy, dx                            # perpendicular
    pts = []
    for i in range(13):
        t = i / 12.0
        along = length * t
        w = width * math.sin(math.pi * t) ** 0.7
        pts.append((cx + dx * along + px * w, cy + dy * along + py * w))
    for i in range(12, -1, -1):
        t = i / 12.0
        along = length * t
        w = width * math.sin(math.pi * t) ** 0.7
        pts.append((cx + dx * along - px * w, cy + dy * along - py * w))
    return pts


def draw_leaf(d, cx, cy, length, width, angle, color, rib):
    d.polygon(leaf_points(cx, cy, length, width, angle), fill=color)
    a = math.radians(angle)
    d.line([(cx, cy), (cx + math.cos(a) * length * 0.96,
                       cy + math.sin(a) * length * 0.96)],
           fill=rib, width=4)


def rounded_rect(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def main():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- studio backdrop: soft vertical gradient + spotlight ----
    top, bot = (247, 247, 244), (214, 214, 210)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bot, y / H))
    # radial spotlight behind the product
    cx, cy = 520, 470
    for r in range(560, 0, -6):
        t = 1 - r / 560.0
        alpha = int(26 * t * t)
        d.ellipse([cx - r, cy - r * 0.82, cx + r, cy + r * 0.82],
                  fill=(255, 255, 255, alpha))
    # floor line + soft contact shadows
    d.line([(0, 838), (W, 838)], fill=(190, 190, 186), width=2)
    d.ellipse([250, 818, 660, 862], fill=(0, 0, 0, 38))
    d.ellipse([600, 822, 900, 858], fill=(0, 0, 0, 30))

    # ---- the patient: potted plant (the ONE accessory) ----
    # terracotta pot
    d.polygon([(322, 700), (568, 700), (540, 838), (350, 838)],
              fill=(201, 111, 74))
    d.polygon([(322, 700), (568, 700), (560, 724), (330, 724)],
              fill=(176, 92, 60))
    d.rounded_rectangle([312, 682, 578, 712], radius=10, fill=(214, 128, 88))
    d.rectangle([336, 700, 356, 830], fill=(255, 255, 255, 38))  # rim light
    d.ellipse([330, 676, 560, 700], fill=(94, 64, 40))           # soil
    # stem (slight S-curve)
    stem = [(445, 690), (438, 620), (448, 540), (442, 470), (448, 400),
            (444, 330)]
    d.line(stem, fill=(74, 120, 58), width=14, joint="curve")
    # leaves
    draw_leaf(d, 446, 640, 150, 42, -155, (58, 140, 74), (38, 100, 52))
    draw_leaf(d, 444, 560, 165, 46, -25, (46, 128, 66), (30, 92, 46))
    draw_leaf(d, 446, 480, 140, 40, -165, (70, 152, 84), (44, 108, 58))
    draw_leaf(d, 445, 400, 130, 38, -15, (52, 134, 70), (34, 96, 48))
    draw_leaf(d, 445, 330, 120, 36, -90, (62, 146, 78), (40, 104, 54))
    draw_leaf(d, 445, 330, 105, 32, -140, (46, 128, 66), (30, 92, 46))
    draw_leaf(d, 445, 330, 105, 32, -40, (76, 158, 88), (48, 112, 60))

    # ---- the gadget: LeafCheck BP-1 on a chrome stand ----
    # stand pole + base
    d.rectangle([700, 700, 716, 838], fill=(150, 156, 162))
    d.rectangle([700, 700, 706, 838], fill=(210, 214, 218))
    d.ellipse([636, 822, 780, 852], fill=(120, 126, 132))
    d.ellipse([648, 826, 768, 848], fill=(168, 174, 180))
    # device body (white rounded slab)
    body = [576, 420, 852, 716]
    d.rounded_rectangle([body[0] + 8, body[1] + 10, body[2] + 8, body[3] + 8],
                        radius=34, fill=(0, 0, 0, 40))
    rounded_rect(d, body, 34, fill=(250, 250, 248),
                 outline=(200, 200, 196), width=2)
    d.rounded_rectangle([body[0] + 6, body[1] + 6, body[0] + 26, body[3] - 6],
                        radius=10, fill=(255, 255, 255, 90))  # edge light
    # brand
    d.text((714, 448), "LeafCheck", font=F_BOLD(40), fill=(38, 52, 40),
           anchor="ma")
    d.text((714, 492), "BP-1  ·  PLANT MONITOR",
           font=F_REG(16), fill=(110, 116, 110), anchor="ma")
    # ---- analogue gauge ----
    gx, gy, gr = 714, 592, 62
    d.ellipse([gx - gr - 6, gy - gr - 6, gx + gr + 6, gy + gr + 6],
              fill=(228, 228, 224), outline=(180, 180, 176), width=2)
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(255, 255, 255),
              outline=(120, 124, 120), width=3)
    # green healthy zone arc (upper right) + red zone (upper left)
    d.arc([gx - gr + 8, gy - gr + 8, gx + gr - 8, gy + gr - 8],
          start=300, end=30, fill=(46, 160, 80), width=10)
    d.arc([gx - gr + 8, gy - gr + 8, gx + gr - 8, gy + gr - 8],
          start=150, end=210, fill=(200, 70, 60), width=10)
    for ang in range(150, 391, 30):
        a = math.radians(ang)
        x1 = gx + math.cos(a) * (gr - 14)
        y1 = gy + math.sin(a) * (gr - 14)
        x2 = gx + math.cos(a) * (gr - 24)
        y2 = gy + math.sin(a) * (gr - 24)
        d.line([(x1, y1), (x2, y2)], fill=(90, 94, 90), width=3)
    # needle pointing into the green zone
    na = math.radians(330)
    d.line([(gx, gy), (gx + math.cos(na) * (gr - 18),
                       gy + math.sin(na) * (gr - 18))],
           fill=(198, 52, 44), width=5)
    d.ellipse([gx - 8, gy - 8, gx + 8, gy + 8], fill=(60, 64, 60))
    # tiny leaf-heart under the gauge
    d.text((714, 640), "♥", font=F_BOLD(22), fill=(46, 160, 80), anchor="ma")

    # ---- digital readout ----
    rounded_rect(d, [624, 664, 804, 700], 10, fill=(16, 34, 22))
    d.text((714, 682), "120/80", font=F_MONO(26), fill=(110, 230, 140),
           anchor="mm")
    d.text((798, 668), "mmHg", font=F_REG(10), fill=(140, 150, 140),
           anchor="ra")

    # ---- cuff arm: from device to the stem ----
    # chrome arm
    d.line([(576, 560), (470, 500)], fill=(150, 156, 162), width=16)
    d.line([(576, 560), (470, 500)], fill=(210, 214, 218), width=6)
    # cuff band wrapped round the stem
    d.rounded_rectangle([424, 478, 472, 512], radius=12,
                        fill=(52, 58, 64))
    d.rounded_rectangle([424, 478, 472, 492], radius=10,
                        fill=(96, 104, 112))
    d.ellipse([430, 496, 466, 508], fill=(46, 160, 80))  # cuff sensor dot
    # air tube from cuff to device
    tube = [(468, 500), (500, 540), (540, 560), (576, 566)]
    d.line(tube, fill=(90, 96, 102), width=8, joint="curve")
    d.line(tube, fill=(170, 176, 182), width=3, joint="curve")

    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {W}x{H} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
