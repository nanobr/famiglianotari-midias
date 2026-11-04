"""Amor: o teste da última fatia (Nano e Cleideane) — com os avatares reais."""
import math
from draw import *
from family import plate_with_slice, slice_in_hand, broken_heart
from avatars import *

HOOK = "O verdadeiro teste do amor..."
END_CARD = "Você daria a última fatia?"
END_CARD_AT = 3.4
LOGO = True

CL, NA = 300, 905          # centros de Cleide e Nano (Nano espelhado, encostado à direita)
PL_X, PL_Y = 630, 978


def talk_bob(t, a, b):
    return 10 * abs(math.sin(t * 14)) if a <= t <= b else 0.0


def blink_none(*_):
    return 1.0


def stage(ctx, t, cl_lift=0.0, na_lift=0.0, na_shake=0.0, na_squash=1.0, cl_rot=0.0, plate=1):
    background(ctx)
    av(ctx, "cleide", CL, lift=cl_lift, rot=cl_rot)
    av(ctx, "nano", NA, flip=True, lift=na_lift, shake=na_shake, squash=na_squash)
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    if plate == 0:
        ellipse(ctx, PL_X, PL_Y, 150, 58)
        fill_stroke(ctx, (1, 1, 1, 1))
        ellipse(ctx, PL_X, PL_Y, 108, 38)
        ctx.set_source_rgba(*hexc("#EFE8DE"))
        ctx.fill()
    else:
        plate_with_slice(ctx, PL_X, PL_Y, 1.0, sparkle=t if plate == 2 else None)


# 1 — a pergunta
S1 = 3.6


def s1(ctx, t):
    stage(ctx, t, cl_lift=talk_bob(t, 0.4, 1.6))
    bubble(ctx, "Amor, você me ama mais que pizza?", 40, 50, 760, 76, head_top("cleide", CL),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.2)


# 2 — a resposta fácil
S2 = 3.2


def s2(ctx, t):
    stage(ctx, t, na_lift=talk_bob(t, 0.35, 1.1))
    for k in range(3):
        ph = (t * 0.5 + k / 3) % 1.0
        heart(ctx, 600 + 30 * math.sin(t * 3 + k * 2), 640 - 240 * ph, 0.5 + 0.45 * ph, 1 - ph)
    bubble(ctx, "Claro! Muito mais!", 1040, 60, 700, 84, head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.25) / 0.3), chars=(t - 0.35) / 0.8, align="right")


# 3 — a armadilha
S3 = 3.6


def s3(ctx, t):
    hit = (t - 2.2) / 0.25
    shake = 14 * math.sin(t * 55) * max(0.0, 1 - (t - 2.2) / 0.7) if t > 2.2 else 0.0
    squash = 1 + 0.06 * math.sin(clamp(hit) * math.pi) if t > 2.2 else 1.0
    stage(ctx, t, cl_lift=talk_bob(t, 0.4, 1.6), na_shake=shake, na_squash=squash, plate=2)
    if t > 2.2:
        hx, hy = head_c("nano", NA, flip=True)
        shock_fx(ctx, hx + shake, hy, ease_out_back(hit), r0=230)
        exclaim_fx(ctx, hx - 300, hy - 90, ease_out_back(hit))
    bubble(ctx, "Então me dá a última fatia.", 40, 50, 760, 76, head_top("cleide", CL),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.2)


# 4 — a verdade
S4 = 5.6


def s4(ctx, t):
    gap = 4 + 26 * ease_out((t - 2.6) / 0.4)
    stage(ctx, t, na_lift=talk_bob(t, 0.5, 2.3), cl_rot=-0.03, plate=0)
    # Nano agarrado à fatia
    circle(ctx, 800, 728, 40)
    fill_stroke(ctx, hexc("#F3C6A5"))
    slice_in_hand(ctx, 760, 760, 1.05, -0.45)
    tears_fx(ctx, eye_pts("nano", NA, flip=True), t)
    hx, hy = head_c("cleide", CL)
    anger_fx(ctx, hx + 115, hy - 150, 1.8 * ease_out_back((t - 2.6) / 0.3))
    if t > 2.6:
        broken_heart(ctx, 590, 600, 1.1, gap)
    bubble(ctx, "Te amo... mas essa massa fermentou 72 horas!", 1040, 30, 980, 72,
           head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.9, align="right")


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [3.0, 2.0, 3.0, 3.2]
CUES = [
    [(0.3, "pop", 0), (0.4, "type", 1.2)],
    [(0.25, "pop", 0), (0.35, "type", 0.8)],
    [(0.3, "pop", 0), (0.4, "type", 1.2), (2.2, "boing", 0)],
    [(0.3, "pop", 0), (0.45, "type", 1.9), (1.2, "drip", 0), (2.6, "whoosh", 0), (3.4, "pop", 0)],
]
