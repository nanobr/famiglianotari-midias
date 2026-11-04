"""Avatares reais da família (recortes dos stickers em assets/avatares/).

    av(ctx, "nano", cx, height, flip=True)   # antes do counter(ctx); a parte de baixo fica escondida no balcão
    eye_pts("nano", cx, height, flip=True)   # posição dos olhos na tela (para lágrimas, brilho etc.)
    head_top("nano", cx, height, flip=True)  # ponta para os balões de fala

Os avatares têm expressão fixa (sorrindo); emoções vêm dos efeitos (suor, choque, lágrimas,
coração partido, veia de raiva) e da animação (pulo, tremida, zoom).

Lados cortados (onde dois personagens estavam juntos no sticker original):
- nano: corte à ESQUERDA -> use flip=True e encoste na borda direita do quadro (cx >= 880).
- cammy: corte à DIREITA -> use flip=True e encoste na borda esquerda do quadro (cx <= 190).
"""
import math, os
import cairo
from draw import *

HERE = os.path.dirname(os.path.abspath(__file__))
BOTTOM = COUNTER_Y + 70  # base do avatar, escondida atrás do balcão

# anchors in normalised image coords (u, v), before flipping
META = {
    "nano":   dict(h=640, eyes=((0.22, 0.42), (0.53, 0.42)), head=(0.42, 0.36), top=0.02),
    "cleide": dict(h=640, eyes=((0.20, 0.43), (0.465, 0.43)), head=(0.34, 0.40), top=0.0),
    "cammy":  dict(h=620, eyes=((0.42, 0.40), (0.75, 0.40)), head=(0.58, 0.40), top=0.02),
    "isis":   dict(h=500, eyes=((0.33, 0.52), (0.66, 0.52)), head=(0.50, 0.48), top=0.05),
}
_cache = {}


def _surf(name):
    if name not in _cache:
        _cache[name] = cairo.ImageSurface.create_from_png(os.path.join(HERE, "assets", "avatares", name + ".png"))
    return _cache[name]


def _geom(name, cx, height=None, flip=False, lift=0.0):
    s = _surf(name)
    h = height or META[name]["h"]
    k = h / s.get_height()
    w = s.get_width() * k
    top = BOTTOM - h - lift
    return s, k, w, h, cx - w / 2, top


def _pt(name, uv, cx, height=None, flip=False, lift=0.0):
    s, k, w, h, x0, top = _geom(name, cx, height, flip, lift)
    u, v = uv
    if flip:
        u = 1 - u
    return x0 + u * w, top + v * h


def av(ctx, name, cx, height=None, flip=False, lift=0.0, shake=0.0, squash=1.0, rot=0.0):
    """Desenha o avatar centrado em cx, apoiado na base do balcão.
    lift: sobe o personagem (pulo); squash: <1 achata, >1 estica (impacto); rot: inclinação em rad."""
    s, k, w, h, x0, top = _geom(name, cx + shake, height, flip, lift)
    ctx.save()
    # pivot at the bottom centre
    ctx.translate(cx + shake, top + h)
    ctx.rotate(rot)
    ctx.scale(1.0 / math.sqrt(squash), squash)
    ctx.translate(-(cx + shake), -(top + h))
    ctx.translate(x0, top)
    if flip:
        ctx.translate(w, 0)
        ctx.scale(-1, 1)
    ctx.scale(k, k)
    ctx.set_source_surface(s, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint()
    ctx.restore()


def eye_pts(name, cx, height=None, flip=False, lift=0.0):
    return [_pt(name, e, cx, height, flip, lift) for e in META[name]["eyes"]]


def head_c(name, cx, height=None, flip=False, lift=0.0):
    return _pt(name, META[name]["head"], cx, height, flip, lift)


def head_top(name, cx, height=None, flip=False, lift=0.0):
    hx, _ = head_c(name, cx, height, flip, lift)
    _, y = _pt(name, (0.5, META[name]["top"]), cx, height, flip, lift)
    return hx, y - 10


# ---------------------------------------------------------------- emotion effects

def tears_fx(ctx, eyes, t, k=1.0):
    for (x, y) in eyes:
        for j in range(2):
            ph = (t * 1.3 + j * 0.5) % 1.0
            sweat(ctx, x, y + 35 + 110 * ph, 0.5 * k * (1 - 0.35 * ph))


def anger_fx(ctx, x, y, s=1.0):
    """Veia de raiva estilo mangá."""
    if s <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.set_source_rgba(*hexc("#D9433B"))
    ctx.set_line_width(9)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (0, 90, 180, 270):
        r = math.radians(a + 45)
        ctx.save()
        ctx.rotate(r)
        ctx.move_to(8, -14)
        ctx.curve_to(16, -4, 16, 4, 8, 14)
        ctx.stroke()
        ctx.restore()
    ctx.restore()


def exclaim_fx(ctx, x, y, s=1.0, text="!!"):
    if s <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    set_font(ctx, 110)
    ctx.text_path(text)
    ctx.set_source_rgba(*hexc("#D9433B"))
    ctx.fill_preserve()
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(5)
    ctx.stroke()
    ctx.restore()


def shock_fx(ctx, cx, cy, k=1.0, r0=210):
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(9)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for ang in (-160, -130, -100, -80, -50, -20):
        a = math.radians(ang)
        ctx.move_to(cx + r0 * math.cos(a), cy + r0 * math.sin(a))
        ctx.line_to(cx + (r0 + 50 * k) * math.cos(a), cy + (r0 + 50 * k) * math.sin(a))
    ctx.stroke()


def gloom_fx(ctx, cx, top, t):
    """Nuvenzinha de tristeza com chuva sobre a cabeça."""
    y = top - 40
    for dx, r in ((-50, 38), (0, 50), (50, 38)):
        circle(ctx, cx + dx, y, r)
    ctx.set_source_rgba(*hexc("#8A93A6"))
    ctx.fill()
    ctx.set_source_rgba(*hexc("#5DA9E9"))
    ctx.set_line_width(5)
    for i in range(5):
        ph = (t * 1.6 + i * 0.37) % 1.0
        x = cx - 60 + i * 30
        ctx.move_to(x, y + 40 + 60 * ph)
        ctx.line_to(x - 5, y + 58 + 60 * ph)
    ctx.stroke()


def pillar(ctx, side="right"):
    """Batente de madeira na borda do quadro: esconde o lado cortado dos avatares do Nano e da Cammy."""
    x = 1032 if side == "right" else -12
    rrect(ctx, x, -200, 60, COUNTER_Y + 200, 8)
    fill_stroke(ctx, hexc("#A8703F"))
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.rectangle(x + 10, -200, 8, COUNTER_Y + 200)
    ctx.fill()
