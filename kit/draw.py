import math
import cairo

W = 1080
STAGE_H = 1280
COUNTER_Y = 930

INK = (0.17, 0.12, 0.10)
FONT = "Poppins"


def hexc(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out_back(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def fill_stroke(ctx, fill, lw=6, stroke=INK):
    ctx.set_source_rgba(*fill)
    ctx.fill_preserve()
    ctx.set_source_rgba(*stroke, 1) if len(stroke) == 3 else ctx.set_source_rgba(*stroke)
    ctx.set_line_width(lw)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()


def circle(ctx, x, y, r):
    ctx.new_sub_path()
    ctx.arc(x, y, r, 0, 2 * math.pi)


def ellipse(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, max(ry, 0.01))
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, 2 * math.pi)
    ctx.restore()


def set_font(ctx, size):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)


def wrap(ctx, text, size, maxw):
    set_font(ctx, size)
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if ctx.text_extents(test).x_advance <= maxw or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- background

def background(ctx):
    ctx.set_source_rgba(*hexc("#FCE9D2"))
    ctx.rectangle(-50, -2000, W + 100, 5000)
    ctx.fill()
    # backsplash tiles
    ctx.set_source_rgba(*hexc("#F6DCC0"))
    ctx.rectangle(-50, 770, W + 100, COUNTER_Y - 770)
    ctx.fill()
    ctx.set_source_rgba(*hexc("#E9C9A6"))
    ctx.set_line_width(3)
    for y in range(770, COUNTER_Y, 55):
        ctx.move_to(-50, y)
        ctx.line_to(W + 50, y)
    for i, y in enumerate(range(770, COUNTER_Y, 55)):
        off = 0 if i % 2 == 0 else 55
        for x in range(-55 + off, W + 60, 110):
            ctx.move_to(x, y)
            ctx.line_to(x, min(y + 55, COUNTER_Y))
    ctx.stroke()


def counter(ctx):
    # front
    ctx.set_source_rgba(*hexc("#B9814F"))
    ctx.rectangle(-50, COUNTER_Y + 50, W + 100, 3000)
    ctx.fill()
    ctx.set_source_rgba(*hexc("#A06C3F"))
    ctx.set_line_width(4)
    for x in range(90, W, 180):
        ctx.move_to(x, COUNTER_Y + 50)
        ctx.line_to(x, COUNTER_Y + 3000)
    ctx.stroke()
    # top
    ctx.rectangle(-50, COUNTER_Y, W + 100, 50)
    fill_stroke(ctx, hexc("#8E5A33"), lw=6)
    ctx.set_source_rgba(1, 1, 1, 0.18)
    ctx.rectangle(-50, COUNTER_Y + 8, W + 100, 8)
    ctx.fill()


# ---------------------------------------------------------------- people

SKIN = hexc("#F2C29B")
BLUSH = hexc("#F08A8A", 0.45)

EU = dict(shirt=hexc("#3E7CB1"), hair=hexc("#3B2A20"), apron=True, curly=False, beard=False)
AMIGO = dict(shirt=hexc("#6BAF5A"), hair=hexc("#D9773A"), apron=False, curly=True, beard=False)


def person_body(ctx, hx, hy, p):
    # arms
    for side in (-1, 1):
        ctx.save()
        x = hx + side * 175
        rrect(ctx, x - 40, hy + 140, 80, COUNTER_Y - (hy + 140) + 20, 40)
        fill_stroke(ctx, p["shirt"])
        ctx.restore()
    # torso
    rrect(ctx, hx - 180, hy + 105, 360, 700, 110)
    fill_stroke(ctx, p["shirt"])
    if p["apron"]:
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(6)
        ctx.move_to(hx - 85, hy + 230)
        ctx.line_to(hx - 50, hy + 120)
        ctx.move_to(hx + 85, hy + 230)
        ctx.line_to(hx + 50, hy + 120)
        ctx.stroke()
        rrect(ctx, hx - 115, hy + 225, 230, 700, 30)
        fill_stroke(ctx, hexc("#FFFDF7"))
        # pocket with a tiny wheat mark
        rrect(ctx, hx - 55, hy + 300, 110, 80, 14)
        fill_stroke(ctx, hexc("#F3E9D8"), lw=5)
    # neck
    ctx.rectangle(hx - 38, hy + 80, 76, 50)
    ctx.set_source_rgba(*SKIN)
    ctx.fill()


def person_hands(ctx, hx, p):
    for side in (-1, 1):
        circle(ctx, hx + side * 175, COUNTER_Y + 12, 40)
        fill_stroke(ctx, SKIN)


def person_head(ctx, hx, hy, p, expr="happy", blink=1.0, mouth=0.0, t=0.0):
    R = 120
    # curls behind
    if p["curly"]:
        for a in range(195, 350, 18):
            ang = math.radians(a)
            circle(ctx, hx + (R + 2) * math.cos(ang), hy + (R + 2) * math.sin(ang), 42)
            fill_stroke(ctx, p["hair"])
    # ears
    for side in (-1, 1):
        circle(ctx, hx + side * 116, hy + 12, 27)
        fill_stroke(ctx, SKIN)
    # head
    circle(ctx, hx, hy, R)
    fill_stroke(ctx, SKIN)
    # beard shadow
    if p["beard"]:
        ctx.save()
        circle(ctx, hx, hy, R - 3)
        ctx.clip()
        ellipse(ctx, hx, hy + 95, 112, 70)
        ctx.set_source_rgba(*hexc("#3B2A20", 0.22))
        ctx.fill()
        ctx.restore()
    # hair cap
    ctx.save()
    circle(ctx, hx, hy, R)
    ctx.clip()
    ctx.set_source_rgba(*p["hair"])
    ctx.rectangle(hx - R - 20, hy - R - 30, 2 * R + 40, R - 30)
    ctx.fill()
    for i in range(-3, 4):
        circle(ctx, hx + i * 36, hy - 52 + (abs(i) * 4), 24)
        ctx.fill()
    ctx.restore()
    circle(ctx, hx, hy, R)
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(6)
    ctx.stroke()
    if p["curly"]:
        for a in (240, 270, 300):
            ang = math.radians(a)
            circle(ctx, hx + (R - 6) * math.cos(ang), hy + (R - 6) * math.sin(ang), 28)
            fill_stroke(ctx, p["hair"], lw=5)

    # blush
    for side in (-1, 1):
        circle(ctx, hx + side * 72, hy + 42, 21)
        ctx.set_source_rgba(*BLUSH)
        ctx.fill()

    ex, ey = 44, 4
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(7)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    # eyes
    if expr == "shocked":
        for side in (-1, 1):
            circle(ctx, hx + side * ex, hy + ey - 4, 30)
            fill_stroke(ctx, (1, 1, 1, 1), lw=5)
            circle(ctx, hx + side * ex, hy + ey - 4, 12)
            ctx.set_source_rgba(*INK)
            ctx.fill()
    elif expr == "love":
        for side in (-1, 1):
            ctx.new_sub_path()
            ctx.arc(hx + side * ex, hy + ey + 10, 18, math.pi * 1.1, math.pi * 1.9)
            ctx.set_source_rgba(*INK)
            ctx.stroke()
    else:
        for side in (-1, 1):
            ellipse(ctx, hx + side * ex, hy + ey, 13, 20 * blink)
            ctx.set_source_rgba(*INK)
            ctx.fill()
            if blink > 0.6:
                circle(ctx, hx + side * ex + 4, hy + ey - 7, 4.5)
                ctx.set_source_rgba(1, 1, 1, 1)
                ctx.fill()

    # brows
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(8)
    by = hy - 34
    for side in (-1, 1):
        x0 = hx + side * (ex - 20)
        x1 = hx + side * (ex + 20)
        if expr == "worried":
            ctx.move_to(x0, by - 14)
            ctx.line_to(x1, by + 2)
        elif expr == "shocked":
            ctx.move_to(x0, by - 26)
            ctx.curve_to(x0 + side * 10, by - 36, x1 - side * 10, by - 36, x1, by - 22)
        else:
            ctx.move_to(x0, by - 2)
            ctx.curve_to(x0 + side * 10, by - 10, x1 - side * 10, by - 10, x1, by - 2)
    ctx.stroke()

    # mouth
    mx, my = hx, hy + 60
    if expr == "shocked":
        ellipse(ctx, mx, my + 6, 26, 34)
        fill_stroke(ctx, hexc("#7A2E2E"), lw=6)
    elif mouth > 0.05:
        ellipse(ctx, mx, my, 24, 6 + 18 * mouth)
        fill_stroke(ctx, hexc("#7A2E2E"), lw=6)
    elif expr == "worried":
        ctx.move_to(mx - 26, my + 6)
        ctx.curve_to(mx - 12, my - 6, mx + 12, my + 14, mx + 26, my + 2)
        ctx.stroke()
    elif expr == "love":
        ctx.move_to(mx - 38, my - 6)
        ctx.curve_to(mx - 20, my + 32, mx + 20, my + 32, mx + 38, my - 6)
        ctx.close_path()
        fill_stroke(ctx, hexc("#7A2E2E"), lw=6)
    else:
        ctx.new_sub_path()
        ctx.arc(mx, my - 18, 30, math.pi * 0.2, math.pi * 0.8)
        ctx.stroke()


def sweat(ctx, x, y, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(0, -30)
    ctx.curve_to(14, -6, 22, 8, 0, 22)
    ctx.curve_to(-22, 8, -14, -6, 0, -30)
    ctx.close_path()
    fill_stroke(ctx, hexc("#8FD3F4"), lw=5)
    ctx.restore()


def heart(ctx, x, y, s=1.0, alpha=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.move_to(0, 30)
    ctx.curve_to(-60, -10, -30, -55, 0, -22)
    ctx.curve_to(30, -55, 60, -10, 0, 30)
    ctx.close_path()
    fill_stroke(ctx, hexc("#E8505B", alpha), lw=5, stroke=(*INK, alpha))
    ctx.restore()


def shock_marks(ctx, hx, hy, k=1.0):
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(8)
    for ang in (-150, -120, -60, -30):
        a = math.radians(ang)
        r0, r1 = 150, 150 + 45 * k
        ctx.move_to(hx + r0 * math.cos(a), hy + r0 * math.sin(a))
        ctx.line_to(hx + r1 * math.cos(a), hy + r1 * math.sin(a))
    ctx.stroke()


# ---------------------------------------------------------------- jar

def jar(ctx, cx, bottom, t=0.0, blink=1.0, w=280, h=340):
    x0, top = cx - w / 2, bottom - h
    # levain inside (clip to glass)
    rrect(ctx, x0, top + 30, w, h - 30, 50)
    ctx.set_source_rgba(*hexc("#E4F1F6", 0.9))
    ctx.fill()
    ctx.save()
    rrect(ctx, x0 + 6, top + 36, w - 12, h - 42, 44)
    ctx.clip()
    level = top + 120 + 6 * math.sin(t * 2.2)
    ctx.set_source_rgba(*hexc("#EED6A8"))
    ctx.move_to(x0, bottom + 10)
    ctx.line_to(x0, level)
    for i in range(0, 9):
        xa = x0 + i * w / 8
        ctx.curve_to(xa + w / 32, level - 18, xa + w / 16 + w / 32, level - 18, xa + w / 8, level)
    ctx.line_to(x0 + w, bottom + 10)
    ctx.close_path()
    ctx.fill()
    # bubbles rising
    for i in range(14):
        seed = (i * 73) % 100 / 100
        speed = 40 + 30 * ((i * 37) % 10) / 10
        bx = x0 + 25 + (w - 50) * seed
        by = bottom - 20 - ((t * speed + i * 47) % (bottom - level - 20))
        r = 5 + (i % 4) * 3
        circle(ctx, bx, by, r)
        ctx.set_source_rgba(*hexc("#C9A96E", 0.9))
        ctx.set_line_width(3)
        ctx.stroke()
    ctx.restore()
    # glass outline + shine
    rrect(ctx, x0, top + 30, w, h - 30, 50)
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(7)
    ctx.stroke()
    rrect(ctx, x0 + 24, top + 70, 22, h - 140, 11)
    ctx.set_source_rgba(1, 1, 1, 0.55)
    ctx.fill()
    # cloth cover (gingham)
    ctx.save()
    rrect(ctx, x0 - 22, top - 10, w + 44, 58, 22)
    ctx.clip_preserve()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    ctx.set_source_rgba(*hexc("#D9433B", 0.75))
    for gx in range(int(x0 - 22), int(x0 + w + 44), 28):
        ctx.rectangle(gx, top - 10, 14, 58)
    ctx.fill()
    ctx.set_source_rgba(*hexc("#D9433B", 0.45))
    for gy in range(int(top - 10), int(top + 48), 28):
        ctx.rectangle(x0 - 22, gy, w + 44, 14)
    ctx.fill()
    ctx.restore()
    rrect(ctx, x0 - 22, top - 10, w + 44, 58, 22)
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(6)
    ctx.stroke()
    # face (on the dough)
    fy = top + 205
    for side in (-1, 1):
        ellipse(ctx, cx + side * 42, fy, 12, 18 * blink)
        ctx.set_source_rgba(*INK)
        ctx.fill()
        if blink > 0.6:
            circle(ctx, cx + side * 42 + 4, fy - 6, 4)
            ctx.set_source_rgba(1, 1, 1, 1)
            ctx.fill()
        circle(ctx, cx + side * 72, fy + 30, 16)
        ctx.set_source_rgba(*BLUSH)
        ctx.fill()
    ctx.new_sub_path()
    ctx.arc(cx, fy + 18, 18, math.pi * 0.15, math.pi * 0.85)
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(6)
    ctx.stroke()


# ---------------------------------------------------------------- speech bubble

def bubble(ctx, text, x, y, maxw, size, tip, pop=1.0, chars=None, align="left", pad=34, shake=0.0):
    if pop <= 0.001:
        return
    lines = wrap(ctx, text, size, maxw - 2 * pad)
    set_font(ctx, size)
    lh = size * 1.18
    tw = max(ctx.text_extents(l).x_advance for l in lines)
    bw = tw + 2 * pad
    bh = lh * len(lines) + 2 * pad - (lh - size) + 6
    if align == "right":
        x = x - bw
    elif align == "center":
        x = x - bw / 2
    ctx.save()
    tx, ty = tip
    ctx.translate(tx + shake, ty)
    ctx.scale(pop, pop)
    ctx.translate(-tx, -ty)
    # tail base points: inside the bubble, toward the tip
    bx = clamp(tx, x + 60, x + bw - 60)
    base_y = y + bh - 12
    tail = [(bx - 34, base_y), (tx, ty), (bx + 30, base_y)]

    def tail_path():
        ctx.move_to(*tail[0])
        ctx.curve_to(tail[0][0], base_y + 30, tx - 10, ty - 20, tx, ty)
        ctx.curve_to(tx - 4, ty - 30, tail[2][0], base_y + 20, *tail[2])
        ctx.close_path()

    ctx.set_source_rgba(*INK)
    ctx.set_line_width(7)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    rrect(ctx, x, y, bw, bh, 42)
    ctx.stroke()
    tail_path()
    ctx.stroke()
    ctx.set_source_rgba(1, 1, 1, 1)
    rrect(ctx, x, y, bw, bh, 42)
    ctx.fill()
    tail_path()
    ctx.fill()

    # text (typewriter)
    set_font(ctx, size)
    ctx.set_source_rgba(*INK)
    total = sum(len(l) for l in lines)
    remaining = total if chars is None else total * clamp(chars)
    for i, l in enumerate(lines):
        if remaining <= 0:
            break
        part = l[: int(remaining)]
        remaining -= len(l)
        lx = x + (bw - ctx.text_extents(l).x_advance) / 2
        ly = y + pad + size * 0.86 + i * lh
        ctx.move_to(lx, ly)
        ctx.show_text(part)
    ctx.restore()
    return lines


def text_len(text):
    return len(text.replace(" ", ""))  # approx typing length
