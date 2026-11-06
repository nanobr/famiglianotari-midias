"""Fim de semana: sextou, bora pedir pizza? (na casa do pizzaiolo) — com os avatares reais."""
import math
from draw import *
from family import pizza
from avatars import *

HOOK = "Sexta-feira na casa de um pizzaiolo..."
END_CARD = "Sexta é pizza feita ou pedida?"
END_CARD_AT = 3.6
LOGO = True

CL, NA = 300, 905          # Cleide à esquerda, Nano espelhado à direita
CA, IS = 215, 770          # Cammy espelhada à esquerda, Ísis à direita
JAR_X = 650


def talk_bob(t, a, b):
    return 10 * abs(math.sin(t * 14)) if a <= t <= b else 0.0


def phone(ctx, x, y, ang=0.25):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    rrect(ctx, -34, -66, 68, 132, 14)
    fill_stroke(ctx, hexc("#2B2B33"))
    rrect(ctx, -24, -52, 48, 98, 6)
    ctx.set_source_rgba(*hexc("#7FC8F8"))
    ctx.fill()
    ctx.restore()


def ring(ctx, x, y, t):
    ctx.set_source_rgba(*INK)
    ctx.set_line_width(6)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(3):
        r = 30 + 22 * k + 6 * math.sin(t * 8 + k)
        ctx.arc(x, y, r, math.radians(-50), math.radians(30))
        ctx.stroke()


# 1 — a proposta
S1 = 3.4


def s1(ctx, t):
    background(ctx)
    av(ctx, "cleide", CL, lift=talk_bob(t, 0.45, 1.6))
    av(ctx, "nano", NA, flip=True)
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    bubble(ctx, "Sextou! Bora pedir uma pizza?", 40, 60, 760, 80, head_top("cleide", CL),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.1)


# 2 — o pizzaiolo ofendido
S2 = 3.4


def s2(ctx, t):
    shake = 16 * math.sin(t * 55) * max(0.0, 1 - t / 0.7)
    background(ctx)
    av(ctx, "cleide", CL)
    av(ctx, "nano", NA, flip=True, shake=shake,
       squash=1 + 0.05 * math.sin(clamp(t / 0.3) * math.pi), lift=talk_bob(t, 0.8, 1.8))
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    hx, hy = head_c("nano", NA, flip=True)
    shock_fx(ctx, hx + shake, hy, ease_out_back((t - 0.1) / 0.25), r0=230)
    exclaim_fx(ctx, hx - 320, hy - 40, ease_out_back((t - 0.15) / 0.25))
    bubble(ctx, "PEDIR?! Eu mesmo faço!", 1040, 60, 760, 96, head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.1) / 0.22), chars=(t - 0.2) / 0.9, shake=shake, align="right")


# 3 — a pergunta inocente
S3 = 4.0


def s3(ctx, t):
    hit = (t - 2.3) / 0.25
    shake = 12 * math.sin(t * 55) * max(0.0, 1 - (t - 2.3) / 0.7) if t > 2.3 else 0.0
    background(ctx)
    av(ctx, "cammy", CA, flip=True, shake=shake)
    av(ctx, "isis", IS, lift=talk_bob(t, 0.45, 1.5))
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    bubble(ctx, "Fica pronta que horas, papai?", 40, 40, 660, 76, head_top("isis", IS),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.0)
    # resposta do Nano, de fora do quadro
    bubble(ctx, "Domingo!", 1040, 320, 480, 96, (1075, 560),
           pop=ease_out_back((t - 1.9) / 0.3), chars=(t - 2.0) / 0.4, align="right")
    if t > 2.3:
        hx, hy = head_c("cammy", CA, flip=True)
        sweat(ctx, hx + 150, hy - 120, 1.0 * ease_out_back(hit))
        ex, ey = eye_pts("isis", IS)[0]
        exclaim_fx(ctx, ex - 270, ey - 10, 0.8 * ease_out_back(hit), text="?!")


# 4 — o plano B
S4 = 5.8


def s4(ctx, t):
    background(ctx)
    av(ctx, "cleide", CL, lift=talk_bob(t, 0.45, 1.8))
    av(ctx, "nano", NA, flip=True)
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    jar(ctx, JAR_X, 958, t, w=200, h=250, blink=0.1 if 1.4 <= t < 1.55 or 4.6 <= t < 4.75 else 1.0)
    phone(ctx, 520, 680, 0.2)
    ring(ctx, 560, 600, t)
    nx, ny = head_top("nano", NA, flip=True)
    gloom_fx(ctx, nx, ny + 30, t)
    tears_fx(ctx, eye_pts("nano", NA, flip=True), t)
    bubble(ctx, "Alô? Uma pizza grande, por favor!", 40, 30, 560, 64, head_top("cleide", CL),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.3)
    bubble(ctx, "Fermentei à toa?", 1040, 40, 400, 64, (JAR_X + 30, 700),
           pop=ease_out_back((t - 2.4) / 0.3), chars=(t - 2.5) / 0.7, align="right")


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [2.6, 2.4, 3.2, 3.6]
CUES = [
    [(0.3, "pop", 0), (0.45, "type", 1.1)],
    [(0.1, "boing", 0), (0.2, "type", 0.9)],
    [(0.3, "pop", 0), (0.45, "type", 1.0), (1.9, "pop", 0), (2.3, "boing", 0)],
    [(0.3, "pop", 0), (0.45, "type", 1.3), (1.0, "drip", 0), (2.4, "pop", 0), (2.5, "type", 0.7)],
]
