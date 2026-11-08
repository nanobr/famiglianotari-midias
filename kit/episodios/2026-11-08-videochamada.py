"""Domingo livre: a videochamada com a vovó... que encontra um "netinho" novo — com os avatares reais."""
import math
from draw import *
from family import fam
from avatars import *

HOOK = "Videochamada de domingo com a vovó..."
END_CARD = "Quem aí faz chamada de domingo com a vó?"
END_CARD_AT = 3.6
LOGO = True

IS, NA = 790, 905   # Ísis à direita, Nano espelhado à direita
JAR_X = 250

VOVO = dict(name="Vovó", skin=hexc("#F3CDB2"), hair=hexc("#D9D6D2"), shirt=hexc("#8E7CC3"),
            style="long_straight", beard=False, glasses=hexc("#6B4E9B"), scale=1.0)


def talk_bob(t, a, b):
    return 10 * abs(math.sin(t * 14)) if a <= t <= b else 0.0


def tablet(ctx, cx, bottom, w, h, mode, t, expr="happy", mouth=0.0, jorge_pip=False):
    """Tablet em pé no balcão, com a vovó na tela.
    mode: "testa" (só o topo da cabeça), "rosto" (enquadrada certinho)."""
    x0, y0 = cx - w / 2, bottom - h
    # suporte
    ctx.move_to(cx - 40, bottom + 4)
    ctx.line_to(cx + 40, bottom + 4)
    ctx.line_to(cx + 20, bottom - 40)
    ctx.line_to(cx - 20, bottom - 40)
    ctx.close_path()
    fill_stroke(ctx, hexc("#5A5A66"), lw=5)
    # moldura
    rrect(ctx, x0, y0, w, h, 26)
    fill_stroke(ctx, hexc("#2B2B33"), lw=7)
    sx, sy, sw, sh = x0 + 18, y0 + 18, w - 36, h - 36
    ctx.save()
    rrect(ctx, sx, sy, sw, sh, 12)
    ctx.clip()
    ctx.set_source_rgba(*hexc("#F3E4C8"))
    ctx.paint()
    # quadro na parede da vovó
    ctx.rectangle(sx + sw * 0.72, sy + 20, sw * 0.18, sh * 0.22)
    fill_stroke(ctx, hexc("#9FD0A8"), lw=4)
    k = sh / 520
    ctx.save()
    if mode == "testa":
        ctx.translate(cx, sy + sh + 5 * k)       # cabeça quase toda abaixo da tela
        ctx.scale(k * 2.3, k * 2.3)
        circle(ctx, 0, -150, 55)
        fill_stroke(ctx, VOVO["hair"])
        fam(ctx, 0, 0, VOVO, "happy", t=t)
    else:
        ctx.translate(cx, sy + sh * 0.47)
        ctx.scale(k * 1.3, k * 1.3)
        circle(ctx, 0, -150, 55)
        fill_stroke(ctx, VOVO["hair"])
        fam(ctx, 0, 0, VOVO, expr, mouth=mouth, t=t)
    ctx.restore()
    if jorge_pip:   # janelinha da própria câmera mostrando o Jorge
        px, py, pw, ph = sx + sw - 120, sy + sh - 140, 108, 128
        rrect(ctx, px, py, pw, ph, 10)
        fill_stroke(ctx, hexc("#FCE9D2"), lw=4)
        ctx.save()
        rrect(ctx, px, py, pw, ph, 10)
        ctx.clip()
        ctx.translate(px + pw / 2, py + ph + 6)
        ctx.scale(0.32, 0.32)
        jar(ctx, 0, 0, t)
        ctx.restore()
    ctx.restore()
    # câmera
    circle(ctx, cx, y0 + 9, 4)
    ctx.set_source_rgba(*hexc("#777788"))
    ctx.fill()
    # "ao vivo"
    rrect(ctx, x0 + 26, y0 + 26, 64, 28, 8)
    ctx.set_source_rgba(*hexc("#D9433B"))
    ctx.fill()
    set_font(ctx, 18)
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.move_to(x0 + 36, y0 + 47)
    ctx.show_text("VÍDEO")


# 1 — só aparece a testa
S1 = 3.8
TB1 = (390, 925, 500, 400)


def s1(ctx, t):
    background(ctx)
    av(ctx, "isis", IS, lift=talk_bob(t, 0.45, 1.5))
    pillar(ctx, "left")
    pillar(ctx, "right")
    counter(ctx)
    cx, b, w, h = TB1
    tablet(ctx, cx, b, w, h, "testa", t)
    bubble(ctx, "Vovó, só aparece sua testa!", 1040, 60, 760, 80, head_top("isis", IS),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.1, align="right")


# 2 — a vovó se ajeita
S2 = 3.6


def s2(ctx, t):
    background(ctx)
    av(ctx, "isis", IS, lift=6 * abs(math.sin(t * 6 + 1)) if t > 1.6 else 0.0)
    pillar(ctx, "left")
    pillar(ctx, "right")
    counter(ctx)
    cx, b, w, h = TB1
    tablet(ctx, cx, b, w, h, "rosto", t, mouth=abs(math.sin(t * 12)) if 0.4 < t < 1.6 else 0.0)
    for kk in range(3):
        ph = (t * 0.5 + kk / 3) % 1.0
        heart(ctx, 700 + 90 * kk + 20 * math.sin(t * 3 + kk), 420 - 160 * ph, 0.45 + 0.35 * ph, 1 - ph)
    bubble(ctx, "Cadê meu netinho lindo?", 60, 60, 700, 80, (cx + 40, b - h - 10),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.1)


# 3 — a câmera virou para o Jorge
S3 = 3.8
TB3 = (585, 925, 380, 320)


def s3(ctx, t):
    hit = (t - 2.0) / 0.25
    shake = 14 * math.sin(t * 55) * max(0.0, 1 - (t - 2.0) / 0.7) if t > 2.0 else 0.0
    background(ctx)
    av(ctx, "nano", NA, flip=True, shake=shake,
       squash=1 + 0.05 * math.sin(clamp(hit) * math.pi) if t > 2.0 else 1.0)
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    jar(ctx, JAR_X, 958, t, blink=0.1 if 1.2 <= t < 1.35 else 1.0)
    for kk in range(2):
        ph = (t * 0.6 + kk / 2) % 1.0
        heart(ctx, JAR_X - 60 + 120 * kk, 600 - 160 * ph, 0.4 + 0.3 * ph, 1 - ph)
    cx, b, w, h = TB3
    tablet(ctx, cx, b, w, h, "rosto", t, expr="love",
           mouth=abs(math.sin(t * 12)) if 0.4 < t < 1.7 else 0.0, jorge_pip=True)
    if t > 2.0:
        hx, hy = head_c("nano", NA, flip=True)
        shock_fx(ctx, hx + shake, hy, ease_out_back(hit), r0=230)
        exclaim_fx(ctx, 860, 330, ease_out_back(hit))
    bubble(ctx, "Nossa, como esse netinho cresceu!", 40, 50, 760, 76, (cx - 40, b - h - 10),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.3)


# 4 — o Jorge ganha uma avó
S4 = 5.6


def s4(ctx, t):
    background(ctx)
    av(ctx, "nano", NA, flip=True, lift=talk_bob(t, 0.45, 1.5))
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    jl = 14 * abs(math.sin(t * 7)) if t > 2.1 else 0.0
    jar(ctx, JAR_X, 958 - jl, t, blink=0.1 if 3.6 <= t < 3.75 else 1.0)
    cx, b, w, h = TB3
    tablet(ctx, cx, b, w, h, "rosto", t, expr="love", jorge_pip=True)
    hx, hy = head_c("nano", NA, flip=True)
    sweat(ctx, hx - 150, hy - 120, 1.1)
    if t > 2.1:
        for kk in range(3):
            ph = (t * 0.6 + kk / 3) % 1.0
            heart(ctx, JAR_X - 80 + 80 * kk, 580 - 180 * ph, 0.45 + 0.35 * ph, 1 - ph)
        tears_fx(ctx, [(JAR_X - 42, 830 - jl), (JAR_X + 42, 830 - jl)], t, 0.8)
    bubble(ctx, "Mãe... isso é o levain.", 1040, 50, 640, 78, head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.0, align="right")
    bubble(ctx, "Agora eu tenho vó!", 40, 380, 520, 66, (JAR_X + 20, 600 - jl),
           pop=ease_out_back((t - 2.0) / 0.3), chars=(t - 2.1) / 0.8)


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [3.0, 2.4, 3.0, 3.2]
CUES = [
    [(0.3, "pop", 0), (0.45, "type", 1.1)],
    [(0.3, "pop", 0), (0.4, "type", 1.1)],
    [(0.3, "pop", 0), (0.4, "type", 1.3), (2.0, "boing", 0)],
    [(0.3, "pop", 0), (0.45, "type", 1.0), (1.0, "drip", 0), (2.0, "pop", 0), (2.1, "type", 0.8)],
]
