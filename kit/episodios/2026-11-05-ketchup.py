"""Família + pizza: 48 horas de fermentação e... ketchup — com os avatares reais."""
import math
from draw import *
from family import pizza, ketchup, splat
from avatars import *

HOOK = "Ser pizzaiolo em casa é sofrer..."
END_CARD = "Ketchup na pizza: pode ou não pode?"
END_CARD_AT = 3.4
LOGO = True

CL, NA = 300, 905          # Cleide à esquerda, Nano espelhado à direita
CA, IS = 215, 770          # Cammy espelhada à esquerda, Ísis à direita


def talk_bob(t, a, b):
    return 10 * abs(math.sin(t * 14)) if a <= t <= b else 0.0


# 1 — o pizzaiolo orgulhoso
S1 = 3.8


def s1(ctx, t):
    background(ctx)
    av(ctx, "cleide", CL)
    av(ctx, "nano", NA, flip=True, lift=talk_bob(t, 0.45, 1.8))
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    pizza(ctx, 620, 978, 340, 8, steam_t=t)
    bubble(ctx, "Pizza de levain: 48 horas de fermentação!", 1040, 40, 960, 74,
           head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.4, align="right")


# 2 — a pequena crítica
S2 = 3.4


def s2(ctx, t):
    background(ctx)
    av(ctx, "cammy", CA, flip=True)
    av(ctx, "isis", IS, lift=talk_bob(t, 0.45, 1.4))
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    pizza(ctx, 470, 985, 330, 8, steam_t=t)
    bubble(ctx, "Papai... cadê o ketchup?", 1040, 110, 760, 80, head_top("isis", IS),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 0.9, align="right")


# 3 — o horror
S3 = 3.2


def s3(ctx, t):
    shake = 16 * math.sin(t * 55) * max(0.0, 1 - t / 0.7)
    lift = ease_out_back((t - 0.6) / 0.4)
    background(ctx)
    av(ctx, "cammy", CA, flip=True)
    av(ctx, "nano", NA, flip=True, shake=shake, squash=1 + 0.05 * math.sin(clamp(t / 0.3) * math.pi))
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    pizza(ctx, 600, 985, 330, 8)
    # Cammy levanta o ketchup
    by = COUNTER_Y - 20 - 170 * lift
    ketchup(ctx, 380, by, 0.85, 0.22 * lift)
    hx, hy = head_c("nano", NA, flip=True)
    shock_fx(ctx, hx + shake, hy, ease_out_back((t - 0.1) / 0.25), r0=230)
    exclaim_fx(ctx, hx - 310, hy - 60, ease_out_back((t - 0.15) / 0.25))
    bubble(ctx, "KETCHUP?!", 1040, 70, 900, 120, head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.1) / 0.22), shake=shake, align="right")


# 4 — o Jorge entende
S4 = 5.6
JAR_X = 300


def s4(ctx, t):
    background(ctx)
    av(ctx, "nano", NA, flip=True, lift=talk_bob(t, 0.45, 1.3))
    pillar(ctx, "right")
    pillar(ctx, "left")
    counter(ctx)
    jar(ctx, JAR_X, 958, t, blink=0.1 if 1.6 <= t < 1.75 or 4.4 <= t < 4.55 else 1.0)
    tears_fx(ctx, eye_pts("nano", NA, flip=True), t)
    pizza(ctx, 640, 1010, 270, 8)
    for dx, dy in ((-55, -8), (45, 2), (-5, 16)):
        splat(ctx, 640 + dx, 1010 + dy, 0.75)
    bubble(ctx, "48 horas...", 1040, 70, 600, 84, head_top("nano", NA, flip=True),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 0.9, align="right")
    bubble(ctx, "Eu sinto a sua dor.", 50, 410, 760, 62, (290, 590),
           pop=ease_out_back((t - 2.0) / 0.3), chars=(t - 2.1) / 0.8)


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [3.0, 2.6, 2.4, 3.2]
CUES = [
    [(0.3, "pop", 0), (0.45, "type", 1.4)],
    [(0.3, "pop", 0), (0.45, "type", 0.9)],
    [(0.1, "boing", 0), (0.6, "whoosh", 0)],
    [(0.3, "pop", 0), (0.45, "type", 0.9), (1.0, "drip", 0), (2.0, "pop", 0), (2.1, "type", 0.8)],
]
