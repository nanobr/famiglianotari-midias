"""Elenco da famiglianotari no estilo do kit.

Personagens: NANO, CLEIDE, CAMMY, ISIS. Uso:

    fam_body(ctx, hx, hy, NANO)            # antes do balcão
    fam_head(ctx, hx, hy, NANO, "happy")   # expressões: happy, talk, worried, shocked, love, angry, smug
    counter(ctx)
    fam_hands(ctx, hx, hy, NANO)           # depois do balcão

Crianças usam c["scale"] < 1 e a cabeça mais baixa (hy maior).
"""
import math, os
import cairo
from draw import *

HERE = os.path.dirname(os.path.abspath(__file__))

NANO = dict(name="Nano", skin=hexc("#F0C29E"), hair=hexc("#2E2420"), shirt=hexc("#2F5DA8"),
            style="short", beard=True, glasses=None, apron=True, scale=1.0)
CLEIDE = dict(name="Cleideane", skin=hexc("#F5CDB0"), hair=hexc("#1F1A1C"), shirt=hexc("#9C2F6E"),
              style="long_straight", beard=False, glasses=hexc("#B8862F"), turtleneck=True, scale=1.0)
CAMMY = dict(name="Cammy", skin=hexc("#F8D6C0"), hair=hexc("#D97B3A"), shirt=hexc("#3A2A2A"),
             style="long_curly", beard=False, glasses=hexc("#9A9A9A"), cardigan=hexc("#F7F1E8"),
             choker=True, scale=0.97)
ISIS = dict(name="Ísis", skin=hexc("#F6D2BA"), hair=hexc("#2A1F1D"), shirt=hexc("#F4A9C4"),
            style="kid", beard=False, glasses=None, headband=hexc("#3D6FD1"), scale=0.78)

CAST = {"nano": NANO, "cleide": CLEIDE, "cammy": CAMMY, "isis": ISIS}
R = 120


def _xf(ctx, hx, hy, c):
    ctx.save()
    ctx.translate(hx, hy)
    ctx.scale(c.get("scale", 1.0), c.get("scale", 1.0))


def _back_hair(ctx, c):
    st = c["style"]
    if st == "long_straight":
        rrect(ctx, -R - 28, -R - 12, 2 * R + 56, R + 360, 120)
        fill_stroke(ctx, c["hair"])
    elif st == "kid":
        rrect(ctx, -R - 22, -R - 8, 2 * R + 44, R + 300, 110)
        fill_stroke(ctx, c["hair"])
    elif st == "long_curly":
        pts = [(0, -18, R + 34)]
        for y in range(-70, 270, 42):
            for side in (-1, 1):
                pts.append((side * (R + 4 + 10 * math.sin(y / 30)), y, 50))
        ctx.set_line_width(6)
        for x, y, r in pts:
            circle(ctx, x, y, r)
            ctx.set_source_rgba(*INK)
            ctx.stroke()
        for x, y, r in pts:
            circle(ctx, x, y, r)
            ctx.set_source_rgba(*c["hair"])
            ctx.fill()


def fam_body(ctx, hx, hy, c):
    s = c.get("scale", 1.0)
    cy_local = (COUNTER_Y - hy) / s
    _xf(ctx, hx, hy, c)
    _back_hair(ctx, c)
    if c["style"] == "short":  # volume on top of the head
        ctx.move_to(-R + 6, -30)
        ctx.curve_to(-R - 10, -120, -40, -175, 20, -160)
        ctx.curve_to(60, -178, 120, -150, R - 4, -40)
        ctx.close_path()
        fill_stroke(ctx, c["hair"])
    # arms
    for side in (-1, 1):
        rrect(ctx, side * 175 - 40, 140, 80, cy_local - 140 + 20, 40)
        fill_stroke(ctx, c.get("cardigan", c["shirt"]))
    # torso
    rrect(ctx, -180, 105, 360, max(cy_local - 60, 400), 110)
    fill_stroke(ctx, c["shirt"])
    if c.get("cardigan"):
        ctx.save()
        rrect(ctx, -180, 105, 360, max(cy_local - 60, 400), 110)
        ctx.clip()
        ctx.rectangle(-180, 100, 105, 900)
        ctx.rectangle(75, 100, 105, 900)
        ctx.set_source_rgba(*c["cardigan"])
        ctx.fill()
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(5)
        for side in (-1, 1):
            ctx.move_to(side * 75, 120)
            ctx.line_to(side * 75, 1000)
        ctx.stroke()
        ctx.restore()
        rrect(ctx, -180, 105, 360, max(cy_local - 60, 400), 110)
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(6)
        ctx.stroke()
    if c.get("apron"):
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(6)
        ctx.move_to(-85, 230); ctx.line_to(-50, 120)
        ctx.move_to(85, 230); ctx.line_to(50, 120)
        ctx.stroke()
        rrect(ctx, -115, 225, 230, 700, 30)
        fill_stroke(ctx, hexc("#FFFDF7"))
        # little pizza on the apron
        circle(ctx, 0, 320, 34)
        fill_stroke(ctx, hexc("#E9B35F"), lw=4)
        circle(ctx, 0, 320, 24)
        ctx.set_source_rgba(*hexc("#D9433B"))
        ctx.fill()
        for dx, dy in ((-9, -6), (8, 4), (-2, 11)):
            circle(ctx, dx, 320 + dy, 5)
            ctx.set_source_rgba(*hexc("#FFF2C9"))
            ctx.fill()
    # neck
    ctx.rectangle(-38, 80, 76, 50)
    ctx.set_source_rgba(*c["skin"])
    ctx.fill()
    if c.get("turtleneck"):
        rrect(ctx, -60, 92, 120, 46, 20)
        fill_stroke(ctx, c["shirt"], lw=5)
    if c.get("choker"):
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(9)
        ctx.move_to(-38, 104); ctx.line_to(38, 104)
        ctx.stroke()
        ctx.set_line_width(3)
        ctx.move_to(-30, 112); ctx.curve_to(-20, 170, 20, 170, 30, 112)
        ctx.stroke()
        circle(ctx, 0, 165, 13)
        fill_stroke(ctx, hexc("#D8D8D8"), lw=4)
    ctx.restore()


def fam_hands(ctx, hx, hy, c, which=(-1, 1)):
    s = c.get("scale", 1.0)
    for side in which:
        circle(ctx, hx + side * 175 * s, COUNTER_Y + 12, 40 * s)
        fill_stroke(ctx, c["skin"])


def _front_hair(ctx, c, t):
    st = c["style"]
    ctx.save()
    circle(ctx, 0, 0, R)
    ctx.clip()
    ctx.set_source_rgba(*c["hair"])
    if st == "short":
        ctx.rectangle(-R - 10, -R - 10, 2 * R + 20, R - 40)
        ctx.fill()
        for i in range(-3, 4):
            circle(ctx, i * 36 + 10, -50 + abs(i) * 5, 24)
            ctx.fill()
        # sideburns
        for side in (-1, 1):
            ctx.rectangle(side * (R - 12) - 10, -60, 20, 130)
            ctx.fill()
    elif st in ("long_straight", "kid"):
        ctx.rectangle(-R - 10, -R - 10, 2 * R + 20, R - 50)
        ctx.fill()
        ctx.move_to(-R - 10, -64)
        ctx.curve_to(-60, -30, -20, -70, 0, -78)  # side part
        ctx.curve_to(30, -60, 80, -40, R + 10, -64)
        ctx.line_to(R + 10, -R - 10)
        ctx.line_to(-R - 10, -R - 10)
        ctx.close_path()
        ctx.fill()
        for side in (-1, 1):  # side curtains
            rrect(ctx, side * (R - 4) - 18, -80, 36, 150, 16)
            ctx.fill()
    elif st == "long_curly":
        ctx.rectangle(-R - 10, -R - 10, 2 * R + 20, R - 55)
        ctx.fill()
        for i in range(-3, 4):
            circle(ctx, i * 34, -70 + abs(i) * 7, 24)
            ctx.fill()
        for side in (-1, 1):
            for y in (-50, -8, 34):
                circle(ctx, side * (R - 4), y, 24)
                ctx.fill()
    ctx.restore()
    circle(ctx, 0, 0, R)
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(6)
    ctx.stroke()
    if st == "kid" and c.get("headband"):
        ctx.new_sub_path()
        ctx.arc(0, 0, R - 18, math.radians(205), math.radians(335))
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(22)
        ctx.stroke()
        ctx.new_sub_path()
        ctx.arc(0, 0, R - 18, math.radians(205), math.radians(335))
        ctx.set_source_rgba(*c["headband"])
        ctx.set_line_width(14)
        ctx.stroke()
        # bow
        bx, by = -62, -98
        for side in (-1, 1):
            ctx.move_to(bx, by)
            ctx.line_to(bx + side * 46, by - 26)
            ctx.line_to(bx + side * 46, by + 26)
            ctx.close_path()
            fill_stroke(ctx, c["headband"], lw=5)
        circle(ctx, bx, by, 12)
        fill_stroke(ctx, c["headband"], lw=5)
        for dx, dy in ((-30, -6), (28, 8), (-20, 12), (34, -10)):
            circle(ctx, bx + dx, by + dy, 3.5)
            ctx.set_source_rgba(1, 1, 1, 0.9)
            ctx.fill()


def _beard(ctx, c):
    ctx.save()
    circle(ctx, 0, 0, R - 3)
    ctx.clip()
    ctx.set_source_rgba(*c["hair"])
    ellipse(ctx, 0, 92, 128, 92)
    ctx.fill()
    ctx.set_source_rgba(*c["skin"])
    ellipse(ctx, 0, 30, 92, 40)  # cheeks/upper lip zone
    ctx.fill()
    ellipse(ctx, 0, 68, 34, 15)  # around the mouth
    ctx.fill()
    ctx.restore()
    # moustache
    ctx.move_to(-46, 52)
    ctx.curve_to(-30, 34, -8, 38, 0, 46)
    ctx.curve_to(8, 38, 30, 34, 46, 52)
    ctx.curve_to(26, 50, 10, 54, 0, 56)
    ctx.curve_to(-10, 54, -26, 50, -46, 52)
    ctx.close_path()
    ctx.set_source_rgba(*c["hair"])
    ctx.fill()


def fam_head(ctx, hx, hy, c, expr="happy", blink=1.0, mouth=0.0, t=0.0):
    _xf(ctx, hx, hy, c)
    if c["style"] == "short":
        for side in (-1, 1):
            circle(ctx, side * 116, 12, 27)
            fill_stroke(ctx, c["skin"])
    circle(ctx, 0, 0, R)
    fill_stroke(ctx, c["skin"])
    if c.get("beard"):
        _beard(ctx, c)
    _front_hair(ctx, c, t)

    # blush
    for side in (-1, 1):
        circle(ctx, side * 74, 40, 20)
        ctx.set_source_rgba(*BLUSH)
        ctx.fill()

    ex, ey = 44, 8
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if expr == "shocked":
        for side in (-1, 1):
            circle(ctx, side * ex, ey - 4, 28)
            fill_stroke(ctx, (1, 1, 1, 1), lw=5)
            circle(ctx, side * ex, ey - 4, 12)
            ctx.set_source_rgba(*INK)
            ctx.fill()
    elif expr == "love":
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(7)
        for side in (-1, 1):
            ctx.new_sub_path()
            ctx.arc(side * ex, ey + 12, 18, math.pi * 1.1, math.pi * 1.9)
            ctx.stroke()
    elif expr == "smug":
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(7)
        for side in (-1, 1):
            ctx.move_to(side * ex - 16, ey)
            ctx.line_to(side * ex + 16, ey)
            ctx.stroke()
            ellipse(ctx, side * ex, ey + 6, 12, 9)
            ctx.fill()
    else:
        for side in (-1, 1):
            ellipse(ctx, side * ex, ey, 16, 22 * blink)
            ctx.set_source_rgba(*INK)
            ctx.fill()
            if blink > 0.6:
                circle(ctx, side * ex + 5, ey - 8, 5.5)
                ctx.set_source_rgba(1, 1, 1, 1)
                ctx.fill()
                circle(ctx, side * ex - 5, ey + 8, 2.8)
                ctx.fill()
            if c["style"] != "short" and blink > 0.6:  # lashes
                ctx.set_source_rgba(*INK)
                ctx.set_line_width(4)
                ctx.move_to(side * (ex + 14), ey - 16)
                ctx.line_to(side * (ex + 24), ey - 24)
                ctx.stroke()

    # glasses
    if c.get("glasses"):
        ctx.set_line_width(6)
        for side in (-1, 1):
            circle(ctx, side * ex, ey, 36)
            ctx.set_source_rgba(1, 1, 1, 0.12)
            ctx.fill_preserve()
            ctx.set_source_rgba(*c["glasses"])
            ctx.stroke()
        ctx.move_to(-ex + 36, ey - 4)
        ctx.curve_to(-8, ey - 14, 8, ey - 14, ex - 36, ey - 4)
        ctx.stroke()

    # brows
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(10 if c.get("beard") else 7)
    by = -34
    for side in (-1, 1):
        x0, x1 = side * (ex - 20), side * (ex + 20)
        if expr == "worried":
            ctx.move_to(x0, by - 14); ctx.line_to(x1, by + 2)
        elif expr == "angry":
            ctx.move_to(x0, by + 6); ctx.line_to(x1, by - 12)
        elif expr == "shocked":
            ctx.move_to(x0, by - 26); ctx.curve_to(x0 + side * 10, by - 36, x1 - side * 10, by - 36, x1, by - 22)
        elif expr == "smug":
            ctx.move_to(x0, by - (2 if side < 0 else 16)); ctx.line_to(x1, by - (6 if side < 0 else 10))
        else:
            ctx.move_to(x0, by - 2); ctx.curve_to(x0 + side * 10, by - 10, x1 - side * 10, by - 10, x1, by - 2)
    ctx.stroke()

    # mouth
    mx, my = 0, 64
    ctx.set_line_width(7)
    if expr == "shocked":
        ellipse(ctx, mx, my + 4, 24, 30)
        fill_stroke(ctx, hexc("#7A2E2E"), lw=6)
    elif mouth > 0.05:
        ellipse(ctx, mx, my, 22, 5 + 16 * mouth)
        fill_stroke(ctx, hexc("#7A2E2E"), lw=6)
    elif expr == "worried":
        ctx.move_to(mx - 24, my + 4)
        ctx.curve_to(mx - 10, my - 8, mx + 10, my + 12, mx + 24, my)
        ctx.stroke()
    elif expr == "angry":
        ctx.new_sub_path()
        ctx.arc(mx, my + 22, 22, math.pi * 1.2, math.pi * 1.8)
        ctx.stroke()
    elif expr == "love":
        ctx.move_to(mx - 34, my - 8)
        ctx.curve_to(mx - 18, my + 26, mx + 18, my + 26, mx + 34, my - 8)
        ctx.close_path()
        fill_stroke(ctx, hexc("#7A2E2E"), lw=6)
    elif expr == "smug":
        ctx.move_to(mx - 22, my)
        ctx.curve_to(mx - 6, my + 8, mx + 14, my + 4, mx + 26, my - 10)
        ctx.stroke()
    else:
        ctx.new_sub_path()
        ctx.arc(mx, my - 16, 26, math.pi * 0.2, math.pi * 0.8)
        ctx.stroke()
    ctx.restore()


def fam(ctx, hx, hy, c, expr="happy", blink=1.0, mouth=0.0, t=0.0):
    """Body + head (call counter and fam_hands afterwards)."""
    fam_body(ctx, hx, hy, c)
    fam_head(ctx, hx, hy, c, expr, blink, mouth, t)


# ---------------------------------------------------------------- props

def pizza(ctx, cx, cy, w=300, slices_left=8, steam_t=None):
    """Pizza seen from a 3/4 angle, sitting on the counter (cy = centre)."""
    h = w * 0.42
    ctx.save()
    ctx.translate(cx, cy)
    # board
    ellipse(ctx, 0, 10, w / 2 + 24, h / 2 + 14)
    fill_stroke(ctx, hexc("#C9935A"))
    ctx.save()
    ctx.scale(1, h / w)
    if slices_left >= 8:
        circle(ctx, 0, 0, w / 2)
    else:
        a0 = -math.pi / 2
        a1 = a0 + 2 * math.pi * slices_left / 8
        ctx.move_to(0, 0)
        ctx.arc(0, 0, w / 2, a0, a1)
        ctx.close_path()
    ctx.restore()
    path = ctx.copy_path()
    fill_stroke(ctx, hexc("#E7B566"))
    ctx.save()
    ctx.scale(1, h / w)
    if slices_left >= 8:
        circle(ctx, 0, 0, w / 2 - 22)
    else:
        ctx.move_to(0, 0)
        ctx.arc(0, 0, w / 2 - 22, -math.pi / 2, -math.pi / 2 + 2 * math.pi * slices_left / 8)
        ctx.close_path()
    ctx.restore()
    ctx.set_source_rgba(*hexc("#D9433B"))
    ctx.fill_preserve()
    ctx.save()
    ctx.clip()
    for i in range(14):
        a = i * 2.4
        rr = (w / 2 - 40) * ((i * 37) % 10) / 10
        circle(ctx, rr * math.cos(a), rr * math.sin(a) * h / w, 16)
        ctx.set_source_rgba(*hexc("#FFF2C9"))
        ctx.fill()
    for i in range(6):
        a = i * 1.7 + 0.5
        rr = (w / 2 - 50) * ((i * 53) % 10) / 10
        ellipse(ctx, rr * math.cos(a), rr * math.sin(a) * h / w, 12, 7)
        ctx.set_source_rgba(*hexc("#3E8E41"))
        ctx.fill()
    ctx.restore()
    if slices_left < 8 and slices_left > 0:
        # slice lines
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(4)
        for k in range(1, slices_left):
            a = -math.pi / 2 + 2 * math.pi * k / 8
            ctx.move_to(0, 0)
            ctx.line_to((w / 2) * math.cos(a), (w / 2) * math.sin(a) * h / w)
        ctx.stroke()
    if steam_t is not None:
        ctx.set_line_width(6)
        for k in range(3):
            ph = (steam_t * 0.8 + k / 3) % 1
            x = -60 + k * 60
            ctx.move_to(x, -30 - 120 * ph)
            ctx.curve_to(x + 18, -50 - 120 * ph, x - 18, -70 - 120 * ph, x, -90 - 120 * ph)
            ctx.set_source_rgba(0.55, 0.45, 0.4, 0.6 * (1 - ph))
            ctx.stroke()
    ctx.restore()


def slice_in_hand(ctx, x, y, s=1.0, ang=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    ctx.move_to(-60, -10)
    ctx.line_to(60, -10)
    ctx.line_to(0, 120)
    ctx.close_path()
    fill_stroke(ctx, hexc("#E7B566"))
    rrect(ctx, -66, -26, 132, 26, 13)
    fill_stroke(ctx, hexc("#D49A4C"))
    ctx.move_to(-46, 4); ctx.line_to(46, 4); ctx.line_to(0, 100); ctx.close_path()
    ctx.set_source_rgba(*hexc("#D9433B"))
    ctx.fill()
    for dx, dy in ((-18, 20), (14, 30), (0, 60)):
        circle(ctx, dx, dy, 10)
        ctx.set_source_rgba(*hexc("#FFF2C9"))
        ctx.fill()
    ctx.restore()


def ketchup(ctx, cx, bottom, s=1.0, ang=0.0):
    ctx.save()
    ctx.translate(cx, bottom)
    ctx.rotate(ang)
    ctx.scale(s, s)
    rrect(ctx, -45, -200, 90, 200, 30)
    fill_stroke(ctx, hexc("#D7262E"))
    rrect(ctx, -26, -236, 52, 44, 10)
    fill_stroke(ctx, (1, 1, 1, 1))
    rrect(ctx, -32, -140, 64, 70, 10)
    fill_stroke(ctx, hexc("#FFF7E0"), lw=4)
    # tomato mark
    circle(ctx, 0, -105, 16)
    ctx.set_source_rgba(*hexc("#D7262E"))
    ctx.fill()
    ctx.restore()


def splat(ctx, x, y, k=1.0, color="#D7262E"):
    if k <= 0:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k * 0.45)
    ctx.set_source_rgba(*hexc(color))
    circle(ctx, 0, 0, 40)
    ctx.fill()
    for i in range(7):
        a = i * 0.9
        circle(ctx, 52 * math.cos(a), 52 * math.sin(a), 12)
        ctx.fill()
    ctx.restore()


def plate_with_slice(ctx, cx, cy, s=1.0, sparkle=None):
    """Prato com a última fatia (vista 3/4)."""
    ellipse(ctx, cx, cy, 150 * s, 58 * s)
    fill_stroke(ctx, (1, 1, 1, 1))
    ellipse(ctx, cx, cy, 108 * s, 38 * s)
    ctx.set_source_rgba(*hexc("#EFE8DE"))
    ctx.fill()
    slice_in_hand(ctx, cx - 62 * s, cy - 12 * s, 1.15 * s, -1.68)
    if sparkle is not None:
        k = 1.1 + 0.4 * math.sin(sparkle * 6)
        ctx.set_source_rgba(*hexc("#F6C445"))
        for dx, dy in ((-130, -80), (30, -120), (140, -50)):
            ctx.save()
            ctx.translate(cx + dx * s, cy + dy * s)
            ctx.scale(k, k)
            ctx.move_to(0, -22); ctx.line_to(6, -6); ctx.line_to(22, 0); ctx.line_to(6, 6)
            ctx.line_to(0, 22); ctx.line_to(-6, 6); ctx.line_to(-22, 0); ctx.line_to(-6, -6)
            ctx.close_path()
            ctx.fill()
            ctx.restore()


def broken_heart(ctx, x, y, s=1.0, gap=0.0):
    for side in (-1, 1):
        ctx.save()
        ctx.translate(x + side * gap, y)
        ctx.scale(s, s)
        ctx.move_to(0, 30)
        if side < 0:
            ctx.curve_to(-60, -10, -30, -55, 0, -22)
            ctx.line_to(-8, -6); ctx.line_to(6, 6); ctx.line_to(0, 30)
        else:
            ctx.curve_to(60, -10, 30, -55, 0, -22)
            ctx.line_to(-8, -6); ctx.line_to(6, 6); ctx.line_to(0, 30)
        ctx.close_path()
        fill_stroke(ctx, hexc("#E8505B"), lw=5)
        ctx.restore()


_logo = None


def logo(ctx, cx, cy, d):
    """Logo redondo da Famiglia Notari (assets/logo.png)."""
    global _logo
    if _logo is None:
        _logo = cairo.ImageSurface.create_from_png(os.path.join(HERE, "assets", "logo.png"))
    w = _logo.get_width()
    ctx.save()
    ctx.translate(cx - d / 2, cy - d / 2)
    ctx.scale(d / w, d / w)
    ctx.set_source_surface(_logo, 0, 0)
    ctx.paint()
    ctx.restore()
