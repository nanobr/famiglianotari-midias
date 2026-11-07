"""Cozinha e pizza: a Ísis quer ajudar com a farinha... e o Jorge ganha um banquete — com os avatares reais."""
import math
import random
from draw import *
from avatars import *

HOOK = "Quando a filha quer ajudar na pizza..."
END_CARD = "Quem aí tem ajudante assim em casa?"
END_CARD_AT = 3.6
LOGO = True

IS, NA = 400, 905          # Ísis no centro-esquerda, Nano espelhado à direita
JAR_X = 230
BAG_X = 640


def talk_bob(t, a, b):
    return 10 * abs(math.sin(t * 14)) if a <= t <= b else 0.0


def flour_bag(ctx, cx, bottom, s=1.0, ang=0.0, empty=False):
    ctx.save()
    ctx.translate(cx, bottom)
    ctx.rotate(ang)
    ctx.scale(s, s)
    w, h = 170, 230
    ctx.move_to(-w / 2, 0)
    ctx.line_to(-w / 2 + 8, -h)
    for i in range(6):  # borda de papel dobrada em zigue-zague
        ctx.line_to(-w / 2 + 8 + (i + 0.5) * (w - 16) / 6, -h - 14)
        ctx.line_to(-w / 2 + 8 + (i + 1) * (w - 16) / 6, -h)
    ctx.line_to(w / 2, 0)
    ctx.close_path()
    fill_stroke(ctx, hexc("#F4EAD6"))
    rrect(ctx, -w / 2 + 20, -h + 70, w - 40, 90, 14)
    fill_stroke(ctx, hexc("#D9433B"), lw=5)
    set_font(ctx, 28)
    ctx.set_source_rgba(1, 1, 1, 1)
    txt = "FARINHA"
    ctx.move_to(-ctx.text_extents(txt).x_advance / 2, -h + 128)
    ctx.show_text(txt)
    if empty:
        ctx.move_to(-w / 2 + 30, -40)
        ctx.line_to(w / 2 - 30, -60)
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(4)
        ctx.stroke()
    ctx.restore()


def flour_cloud(ctx, cx, cy, k, t, alpha=1.0):
    """Nuvem de farinha explodindo."""
    if k <= 0.01:
        return
    rnd = random.Random(7)
    for i in range(26):
        a = rnd.uniform(0, 2 * math.pi)
        d = rnd.uniform(0, 1) ** 0.6
        rx = 360 * d * math.cos(a) * k
        ry = 230 * d * math.sin(a) * k
        r = (70 + 90 * rnd.random()) * k * (1 - 0.3 * d)
        circle(ctx, cx + rx + 6 * math.sin(t * 3 + i), cy + ry, r)
        ctx.set_source_rgba(1, 1, 1, alpha * (0.55 + 0.3 * rnd.random()))
        ctx.fill()


def dust(ctx, t, n=60, alpha=0.8):
    """Farinha caindo lentamente pelo quadro."""
    rnd = random.Random(3)
    for i in range(n):
        x = rnd.uniform(0, W)
        sp = rnd.uniform(40, 90)
        y = (rnd.uniform(0, STAGE_H) + t * sp) % STAGE_H
        circle(ctx, x, y, rnd.uniform(3, 8))
        ctx.set_source_rgba(1, 1, 1, alpha)
        ctx.fill()


def floured(ctx, draw_fn, amount=0.55):
    """Desenha algo e 'enfarinha' por cima (tinta branca só onde há desenho)."""
    ctx.push_group()
    draw_fn()
    ctx.set_operator(cairo.OPERATOR_ATOP)
    ctx.set_source_rgba(1, 1, 1, amount)
    ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint()


def stage(ctx, t, is_lift=0.0, na_lift=0.0, na_shake=0.0, na_squash=1.0, bag=True):
    background(ctx)
    av(ctx, "isis", IS, lift=is_lift)
    av(ctx, "nano", NA, flip=True, lift=na_lift, shake=na_shake, squash=na_squash)
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    if bag:
        flour_bag(ctx, BAG_X, COUNTER_Y + 30)


# 1 — o pedido
S1 = 3.6


def s1(ctx, t):
    stage(ctx, t, is_lift=talk_bob(t, 0.45, 1.6))
    for k in range(3):
        ph = (t * 0.5 + k / 3) % 1.0
        heart(ctx, 160 + 30 * math.sin(t * 3 + k * 2), 700 - 240 * ph, 0.45 + 0.4 * ph, 1 - ph)
    bubble(ctx, "Papai, posso ajudar na pizza?", 40, 60, 760, 80, head_top("isis", IS),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.1)


# 2 — a instrução
S2 = 3.6


def s2(ctx, t):
    stage(ctx, t, na_lift=talk_bob(t, 0.4, 1.8))
    bubble(ctx, "Pode! Joga só um pouquinho de farinha.", 1040, 50, 820, 74,
           head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.4, align="right")


# 3 — POF!
S3 = 3.4


def s3(ctx, t):
    hit = (t - 0.5) / 0.35
    shake = 14 * math.sin(t * 55) * max(0.0, 1 - (t - 0.5) / 0.7) if t > 0.5 else 0.0
    toss = ease_out_back(clamp(t / 0.45))
    stage(ctx, t, is_lift=30 * math.sin(clamp(t / 0.5) * math.pi), na_shake=shake, bag=False)
    flour_bag(ctx, BAG_X + 40 * toss, COUNTER_Y + 30 - 520 * toss, 0.9, -2.6 * toss)
    if t > 0.5:
        flour_cloud(ctx, 660, 400, ease_out(hit), t)
        dust(ctx, t, 40, 0.9 * clamp(hit))
        hx, hy = head_c("nano", NA, flip=True)
        shock_fx(ctx, hx + shake, hy, ease_out_back(hit), r0=230)
        exclaim_fx(ctx, 60, 200, 1.3 * ease_out_back((t - 0.55) / 0.3), text="POF!")


# 4 — o banquete do Jorge
S4 = 5.8


def s4(ctx, t):
    background(ctx)
    floured(ctx, lambda: av(ctx, "nano", NA, flip=True, lift=talk_bob(t, 0.45, 1.6)), 0.6)
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    # montinhos de farinha no balcão
    for x, r in ((480, 60), (560, 40), (760, 50), (90, 34)):
        ellipse(ctx, x, COUNTER_Y + 2, r, r * 0.45)
        ctx.set_source_rgba(1, 1, 1, 0.95)
        ctx.fill()
    floured(ctx, lambda: jar(ctx, JAR_X, 958, t, blink=0.1 if 3.6 <= t < 3.75 else 1.0), 0.25)
    # chapéu de farinha no pano do Jorge
    ellipse(ctx, JAR_X, 958 - 345, 140, 34)
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill()
    flour_bag(ctx, 620, COUNTER_Y + 30, 0.8, 1.45, empty=True)
    dust(ctx, t, 50, 0.85)
    eyes = eye_pts("nano", NA, flip=True)
    tears_fx(ctx, eyes, t)
    gx, gy = head_top("nano", NA, flip=True)
    if t > 2.0:
        for k in range(3):
            ph = (t * 0.6 + k / 3) % 1.0
            heart(ctx, 440 + 40 * math.sin(t * 2 + k * 2), 820 - 220 * ph, 0.45 + 0.4 * ph, 1 - ph)
    bubble(ctx, "Era a farinha do mês...", 1040, 50, 640, 76, (gx, gy + 20),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.1, align="right")
    bubble(ctx, "MELHOR DIA DA MINHA VIDA!", 40, 250, 520, 60, (JAR_X + 40, 560),
           pop=ease_out_back((t - 2.0) / 0.3), chars=(t - 2.1) / 1.0)


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [3.0, 3.0, 2.4, 3.4]
CUES = [
    [(0.3, "pop", 0), (0.45, "type", 1.1)],
    [(0.3, "pop", 0), (0.45, "type", 1.4)],
    [(0.1, "whoosh", 0), (0.5, "boing", 0)],
    [(0.3, "pop", 0), (0.45, "type", 1.1), (1.2, "drip", 0), (2.0, "pop", 0), (2.1, "type", 1.0)],
]
