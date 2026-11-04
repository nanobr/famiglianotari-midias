import math
from draw import *

HOOK = "Quem tem levain vai entender..."
END_CARD = "Comenta o nome do SEU levain!"
END_CARD_AT = 3.8  # segundos dentro da última cena

EU_X, AM_X, HEAD_Y = 790, 290, 560


def blink_at(t, *moments):
    for m in moments:
        if m <= t < m + 0.15:
            return 0.1
    return 1.0


def talk(t, start, end):
    if start <= t <= end:
        return 0.5 + 0.5 * math.sin(t * 28)
    return 0.0


def two_people(ctx, t, am_expr, eu_expr, am_mouth=0.0, eu_mouth=0.0,
               am_blink=1.0, eu_blink=1.0, am_shake=0.0):
    background(ctx)
    person_body(ctx, AM_X, HEAD_Y, AMIGO)
    person_body(ctx, EU_X, HEAD_Y, EU)
    person_head(ctx, AM_X + am_shake, HEAD_Y, AMIGO, am_expr, am_blink, am_mouth, t)
    person_head(ctx, EU_X, HEAD_Y, EU, eu_expr, eu_blink, eu_mouth, t)
    counter(ctx)
    person_hands(ctx, AM_X, AMIGO)
    person_hands(ctx, EU_X, EU)


# --- scene 1: friend invites ------------------------------------------------
S1_DUR = 3.6


def s1(ctx, t):
    two_people(ctx, t, "happy", "happy",
               am_mouth=talk(t, 0.4, 1.4),
               am_blink=blink_at(t, 3.1), eu_blink=blink_at(t, 2.4))
    bubble(ctx, "Bora viajar no feriado?", 40, 60, 720, 80, (300, 420),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 0.9)


# --- scene 2: "who will feed Jorge?" ----------------------------------------
S2_DUR = 3.8


def s2(ctx, t):
    two_people(ctx, t, "happy", "worried",
               eu_mouth=talk(t, 0.5, 2.1), am_blink=blink_at(t, 2.8))
    k = ease_out_back((t - 1.6) / 0.3)
    if k > 0.01:
        sweat(ctx, EU_X + 112, HEAD_Y - 70, k)
    bubble(ctx, "Não dá... Quem vai alimentar o Jorge?", 1040, 60, 880, 78, (770, 420),
           pop=ease_out_back((t - 0.25) / 0.3), chars=(t - 0.45) / 1.6, align="right")


# --- scene 3: "WHO IS JORGE??" -----------------------------------------------
S3_DUR = 3.0


def s3(ctx, t):
    shake = 16 * math.sin(t * 55) * max(0.0, 1 - t / 0.7)
    two_people(ctx, t, "shocked", "worried", am_shake=shake, eu_blink=blink_at(t, 2.2))
    shock_marks(ctx, AM_X + shake, HEAD_Y, ease_out_back((t - 0.1) / 0.25))
    bubble(ctx, "QUEM É JORGE??", 40, 70, 1000, 104, (300, 420),
           pop=ease_out_back((t - 0.1) / 0.22), shake=shake)


# --- scene 4: the reveal ------------------------------------------------------
S4_DUR = 6.0
JAR_X, JAR_BOTTOM = 330, 958


def s4(ctx, t):
    background(ctx)
    person_body(ctx, EU_X, HEAD_Y, EU)
    person_head(ctx, EU_X, HEAD_Y, EU, "love", 1.0, 0.0, t)
    counter(ctx)
    jar(ctx, JAR_X, JAR_BOTTOM, t, blink=blink_at(t, 1.5, 4.2))
    person_hands(ctx, EU_X, EU)
    for k in range(2):
        ph = (t * 0.45 + k * 0.5) % 1.0
        heart(ctx, 600 + 12 * math.sin(t * 3 + k), 640 - 230 * ph, 0.55 + 0.45 * ph, 1 - ph)
    bubble(ctx, "Meu levain. 3 anos e MUITA carência.", 1040, 50, 920, 76, (800, 420),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.6, align="right")
    bubble(ctx, "Tô com fome.", 40, 440, 560, 64, (300, 592),
           pop=ease_out_back((t - 2.8) / 0.3), chars=(t - 2.9) / 0.5)


SCENES = [(s1, S1_DUR), (s2, S2_DUR), (s3, S3_DUR), (s4, S4_DUR)]
FINAL_T = [3.0, 3.0, 2.0, 3.6]

# sound cues per scene (local time, kind, duration)
CUES = [
    [(0.3, "pop", 0), (0.4, "type", 0.9)],
    [(0.25, "pop", 0), (0.45, "type", 1.6), (1.6, "drip", 0)],
    [(0.1, "boing", 0)],
    [(0.3, "pop", 0), (0.45, "type", 1.6), (2.8, "pop", 0), (2.9, "type", 0.5), (3.8, "whoosh", 0)],
]
