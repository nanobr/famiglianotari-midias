"""Amor: o teste da última fatia (Nano e Cleideane)."""
import math
from draw import *
from family import *

HOOK = "O verdadeiro teste do amor..."
END_CARD = "Você daria a última fatia?"
END_CARD_AT = 3.4
LOGO = True

CL_X, NA_X, HY = 280, 800, 560
PZ_X, PZ_Y = 545, 968


def blink_at(t, *ms):
    return 0.1 if any(m <= t < m + 0.15 for m in ms) else 1.0


def talk(t, a, b):
    return 0.5 + 0.5 * math.sin(t * 28) if a <= t <= b else 0.0


def stage(ctx, t, cl_expr, na_expr, cl_mouth=0.0, na_mouth=0.0, cl_blink=1.0, na_blink=1.0,
          slices=1, na_hands=(-1, 1), na_shake=0.0):
    background(ctx)
    fam_body(ctx, CL_X, HY, CLEIDE)
    fam_body(ctx, NA_X + na_shake, HY, NANO)
    fam_head(ctx, CL_X, HY, CLEIDE, cl_expr, cl_blink, cl_mouth, t)
    fam_head(ctx, NA_X + na_shake, HY, NANO, na_expr, na_blink, na_mouth, t)
    counter(ctx)
    fam_hands(ctx, CL_X, HY, CLEIDE)
    fam_hands(ctx, NA_X + na_shake, HY, NANO, na_hands)
    if slices:
        plate_with_slice(ctx, PZ_X, PZ_Y, 1.0, sparkle=t if slices == 2 else None)
    else:
        ellipse(ctx, PZ_X, PZ_Y, 150, 58)
        fill_stroke(ctx, (1, 1, 1, 1))
        ellipse(ctx, PZ_X, PZ_Y, 108, 38)
        ctx.set_source_rgba(*hexc("#EFE8DE"))
        ctx.fill()


# 1 — the question
S1 = 3.6


def s1(ctx, t):
    stage(ctx, t, "happy", "happy", cl_mouth=talk(t, 0.4, 1.6), na_blink=blink_at(t, 2.6))
    bubble(ctx, "Amor, você me ama mais que pizza?", 40, 60, 760, 76, (300, 420),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.2)


# 2 — the easy answer
S2 = 3.2


def s2(ctx, t):
    stage(ctx, t, "love", "love", na_mouth=talk(t, 0.35, 1.1))
    for k in range(2):
        ph = (t * 0.5 + k * 0.5) % 1.0
        heart(ctx, 545 + 14 * math.sin(t * 3 + k), 600 - 220 * ph, 0.5 + 0.4 * ph, 1 - ph)
    bubble(ctx, "Claro! Muito mais!", 1040, 70, 700, 84, (790, 420),
           pop=ease_out_back((t - 0.25) / 0.3), chars=(t - 0.35) / 0.8, align="right")


# 3 — the trap
S3 = 3.6


def s3(ctx, t):
    na = "shocked" if t > 2.2 else "happy"
    stage(ctx, t, "smug", na, cl_mouth=talk(t, 0.4, 1.6), slices=2)
    if t > 2.2:
        shock_marks(ctx, NA_X, HY, ease_out_back((t - 2.2) / 0.25))
    bubble(ctx, "Então me dá a última fatia.", 40, 60, 760, 76, (300, 420),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.2)


# 4 — the truth
S4 = 5.6


def s4(ctx, t):
    gap = 4 + 26 * ease_out((t - 2.6) / 0.4)
    stage(ctx, t, "angry", "worried", na_mouth=talk(t, 0.5, 2.3), slices=0, na_hands=(1,))
    # Nano hugs the slice
    slice_in_hand(ctx, NA_X - 170, 700, 1.0, -0.5)
    circle(ctx, NA_X - 175, COUNTER_Y - 150, 40)
    fill_stroke(ctx, NANO["skin"])
    k = ease_out_back((t - 1.2) / 0.3)
    if k > 0.01:
        sweat(ctx, NA_X + 112, HY - 70, k)
    if t > 2.6:
        broken_heart(ctx, 545, 560, 1.1, gap)
    bubble(ctx, "Te amo... mas essa massa fermentou 72 horas!", 1040, 40, 980, 72, (800, 420),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.9, align="right")


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [3.0, 2.0, 3.0, 3.2]
CUES = [
    [(0.3, "pop", 0), (0.4, "type", 1.2)],
    [(0.25, "pop", 0), (0.35, "type", 0.8)],
    [(0.3, "pop", 0), (0.4, "type", 1.2), (2.2, "boing", 0)],
    [(0.3, "pop", 0), (0.45, "type", 1.9), (1.2, "drip", 0), (2.6, "whoosh", 0), (3.4, "pop", 0)],
]
