"""Família + pizza: 48 horas de fermentação e... ketchup."""
import math
from draw import *
from family import *

HOOK = "Ser pizzaiolo em casa é sofrer..."
END_CARD = "Ketchup na pizza: pode ou não pode?"
END_CARD_AT = 3.4
LOGO = True

L_X, R_X, HY = 280, 800, 560
KID_HY = 650
PZ_X, PZ_Y = 545, 975


def blink_at(t, *ms):
    return 0.1 if any(m <= t < m + 0.15 for m in ms) else 1.0


def talk(t, a, b):
    return 0.5 + 0.5 * math.sin(t * 28) if a <= t <= b else 0.0


def tears(ctx, hx, hy, t):
    for side in (-1, 1):
        for k in range(2):
            ph = (t * 1.2 + k * 0.5) % 1.0
            sweat(ctx, hx + side * 44, hy + 40 + 120 * ph, 0.55 * (1 - 0.4 * ph))


# 1 — the proud pizzaiolo
S1 = 3.8


def s1(ctx, t):
    background(ctx)
    fam_body(ctx, L_X, HY, CLEIDE)
    fam_body(ctx, R_X, HY, NANO)
    fam_head(ctx, L_X, HY, CLEIDE, "love")
    fam_head(ctx, R_X, HY, NANO, "love" if t > 1.8 else "happy", 1.0, talk(t, 0.45, 1.8), t)
    counter(ctx)
    fam_hands(ctx, L_X, HY, CLEIDE)
    fam_hands(ctx, R_X, HY, NANO)
    pizza(ctx, PZ_X, PZ_Y, 330, 8, steam_t=t)
    bubble(ctx, "Pizza de levain: 48 horas de fermentação!", 1040, 50, 960, 74, (800, 420),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.4, align="right")


# 2 — the little critic
S2 = 3.4


def s2(ctx, t):
    background(ctx)
    fam_body(ctx, L_X, KID_HY, ISIS)
    fam_body(ctx, R_X, HY, CAMMY)
    fam_head(ctx, L_X, KID_HY, ISIS, "happy", blink_at(t, 2.4), talk(t, 0.45, 1.4), t)
    fam_head(ctx, R_X, HY, CAMMY, "smug" if t > 1.5 else "happy", blink_at(t, 0.9))
    counter(ctx)
    fam_hands(ctx, L_X, KID_HY, ISIS)
    fam_hands(ctx, R_X, HY, CAMMY)
    pizza(ctx, PZ_X, PZ_Y, 330, 8, steam_t=t)
    bubble(ctx, "Papai... cadê o ketchup?", 40, 90, 700, 80, (300, 470),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 0.9)


# 3 — the horror
S3 = 3.2


def s3(ctx, t):
    shake = 16 * math.sin(t * 55) * max(0.0, 1 - t / 0.7)
    lift = ease_out_back((t - 0.6) / 0.4)
    background(ctx)
    fam_body(ctx, L_X, HY, CAMMY)
    fam_body(ctx, R_X + shake, HY, NANO)
    fam_head(ctx, L_X, HY, CAMMY, "smug")
    fam_head(ctx, R_X + shake, HY, NANO, "shocked")
    shock_marks(ctx, R_X + shake, HY, ease_out_back((t - 0.1) / 0.25))
    counter(ctx)
    fam_hands(ctx, L_X, HY, CAMMY, (-1,))
    fam_hands(ctx, R_X + shake, HY, NANO)
    pizza(ctx, PZ_X, PZ_Y, 330, 8)
    # Cammy raises the ketchup
    ketchup(ctx, L_X + 175, COUNTER_Y - 10 - 160 * lift, 0.85, 0.25 * lift)
    circle(ctx, L_X + 175, COUNTER_Y - 30 - 160 * lift, 40)
    fill_stroke(ctx, CAMMY["skin"])
    bubble(ctx, "KETCHUP?!", 1040, 80, 900, 120, (800, 420),
           pop=ease_out_back((t - 0.1) / 0.22), shake=shake, align="right")


# 4 — Jorge understands
S4 = 5.6
JAR_X = 330


def s4(ctx, t):
    background(ctx)
    fam_body(ctx, R_X, HY, NANO)
    fam_head(ctx, R_X, HY, NANO, "worried", 1.0, talk(t, 0.45, 1.5), t)
    tears(ctx, R_X, HY, t)
    counter(ctx)
    jar(ctx, JAR_X, 958, t, blink=blink_at(t, 1.6, 4.4))
    fam_hands(ctx, R_X, HY, NANO)
    # pizza covered in ketchup, in front
    pizza(ctx, 590, 1010, 270, 8)
    for k, (dx, dy) in enumerate(((-55, -8), (45, 2), (-5, 16))):
        splat(ctx, 590 + dx, 1010 + dy, 0.75)
    bubble(ctx, "48 horas...", 1040, 70, 600, 84, (800, 420),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 0.9, align="right")
    bubble(ctx, "Eu sinto a sua dor.", 40, 410, 760, 64, (300, 590),
           pop=ease_out_back((t - 2.0) / 0.3), chars=(t - 2.1) / 0.8)


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [3.0, 2.6, 2.4, 3.2]
CUES = [
    [(0.3, "pop", 0), (0.45, "type", 1.4)],
    [(0.3, "pop", 0), (0.45, "type", 0.9)],
    [(0.1, "boing", 0), (0.6, "whoosh", 0)],
    [(0.3, "pop", 0), (0.45, "type", 0.9), (1.0, "drip", 0), (2.0, "pop", 0), (2.1, "type", 0.8)],
]
