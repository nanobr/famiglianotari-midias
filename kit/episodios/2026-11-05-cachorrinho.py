"""Família: a Ísis quer um cachorrinho... e o Jorge se candidata."""
import math
from draw import *
from avatars import *

HOOK = "Quando a criança pede um bichinho..."
END_CARD = "Seu levain tem nome? Conta aí!"
END_CARD_AT = 3.6
LOGO = True

CL, IS = 300, 770          # Cleide à esquerda, Ísis à direita
CA = 215                   # Cammy espelhada à esquerda


def talk_bob(t, a, b):
    return 10 * abs(math.sin(t * 14)) if a <= t <= b else 0.0


def jblink(t, *ts):
    return 0.1 if any(a <= t < a + 0.15 for a in ts) else 1.0


# 1 — o pedido
S1 = 3.6


def s1(ctx, t):
    background(ctx)
    av(ctx, "cleide", CL)
    av(ctx, "isis", IS, lift=talk_bob(t, 0.45, 1.6))
    pillar(ctx, "left")
    counter(ctx)
    k = 0.5 + 0.5 * math.sin(t * 4)
    heart(ctx, 560, 560 - 20 * k, 0.55 * ease_out_back((t - 1.6) / 0.3), 1.0)
    bubble(ctx, "Mãe, posso ter um cachorrinho?", 1040, 60, 780, 80, head_top("isis", IS),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.45) / 1.2, align="right")


# 2 — a resposta da mãe
S2 = 3.6
J2 = 810


def s2(ctx, t):
    background(ctx)
    av(ctx, "cleide", CL, lift=talk_bob(t, 0.4, 1.5))
    pillar(ctx, "left")
    counter(ctx)
    jar(ctx, J2, 958, t, blink=jblink(t, 2.2))
    bubble(ctx, "A gente já tem o Jorge!", 40, 60, 760, 82, head_top("cleide", CL),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.0)


# 3 — a realidade, pela irmã
S3 = 3.6


def s3(ctx, t):
    background(ctx)
    av(ctx, "cammy", CA, flip=True, lift=talk_bob(t, 0.4, 1.5))
    av(ctx, "isis", IS)
    pillar(ctx, "left")
    counter(ctx)
    if t > 1.7:
        gloom_fx(ctx, head_c("isis", IS)[0], head_top("isis", IS)[1] - 75, t)
    bubble(ctx, "O Jorge é massa num pote!", 40, 60, 760, 80, head_top("cammy", CA, flip=True),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 1.1)


# 4 — o Jorge se candidata
S4 = 5.8
J4 = 330


def s4(ctx, t):
    hop = 22 * abs(math.sin(t * 9)) if 0.4 <= t <= 1.4 else 0.0
    background(ctx)
    av(ctx, "isis", IS, lift=10 * abs(math.sin(t * 10)) if 2.0 <= t <= 2.9 else 0.0)
    counter(ctx)
    jar(ctx, J4, 958 - hop, t, blink=jblink(t, 1.8, 4.6))
    if t > 2.0:
        for k in range(3):
            ph = (t * 0.6 + k / 3) % 1.0
            heart(ctx, 560 + 40 * math.sin(t * 3 + k * 2), 700 - 250 * ph, 0.45 + 0.4 * ph, 1 - ph)
    bubble(ctx, "Au... au?", 40, 330, 520, 84, (J4, 600 - hop),
           pop=ease_out_back((t - 0.3) / 0.3), chars=(t - 0.4) / 0.6)
    bubble(ctx, "EU AMEI ELE!", 1040, 60, 700, 92, head_top("isis", IS),
           pop=ease_out_back((t - 2.0) / 0.3), chars=(t - 2.1) / 0.6, align="right")


SCENES = [(s1, S1), (s2, S2), (s3, S3), (s4, S4)]
FINAL_T = [3.0, 3.0, 3.0, 3.4]
CUES = [
    [(0.3, "pop", 0), (0.45, "type", 1.2)],
    [(0.3, "pop", 0), (0.4, "type", 1.0)],
    [(0.3, "pop", 0), (0.4, "type", 1.1), (1.7, "drip", 0)],
    [(0.3, "boing", 0), (0.4, "type", 0.6), (2.0, "pop", 0), (2.1, "type", 0.6)],
]
