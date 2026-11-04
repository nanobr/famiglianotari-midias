# Kit de tirinhas — famiglianotari

Gera, a partir de um único arquivo de episódio, a **tirinha** (PNG 1080x1350, 4 quadros) e o **reel animado** (MP4 1080x1920, com efeitos sonoros e música gerados, sem direitos autorais de terceiros).

Este repositório é público: aqui ficam só as mídias publicadas e este kit de desenho. Nunca coloque chaves, senhas ou arquivos pessoais.

## Uso

```bash
pip install --break-system-packages pycairo numpy
cd kit
python3 episodio.py exemplo_jorge.py ../posts/AAAA-MM-DD-slug            # tirinha.png + reel.mp4
python3 episodio.py meu_episodio.py /tmp/previa --stills                  # só a tirinha e 4 quadros de prévia
```

## Como escrever um episódio

Copie `exemplo_jorge.py` e altere:

- `HOOK` — frase do topo (título da tirinha e faixa do reel).
- `END_CARD` e `END_CARD_AT` — chamada para comentar, que sobe no fim da última cena do reel.
- `SCENES` — exatamente 4 funções `(fn, duração_em_s)`. Cada `fn(ctx, t)` desenha o quadro no tempo `t` num palco de 1080x1280.
- `FINAL_T` — o instante de cada cena usado na tirinha estática (com balões completos e olhos abertos).
- `CUES` — sons por cena: `pop`, `type` (digitação, com duração), `drip`, `boing` e `whoosh`.

Peças prontas em `draw.py`: `background`, `counter`, `person_body` / `person_head` / `person_hands` (expressões `happy`, `worried`, `shocked`, `love`; `mouth` para falar e `blink` para piscar), `jar` (o Jorge, com bolhas animadas), `bubble` (balão com efeito pop e digitação), `heart`, `sweat` e `shock_marks`, além das curvas `ease_out_back` e `ease_out`.

## Elenco fixo (família Notari)

**Use sempre os avatares reais** (`avatars.py`, imagens em `assets/avatares/`), recortados dos stickers da família:

- `nano` (pai, pizzaiolo da casa): corte do lado esquerdo, então use `flip=True` e encoste à direita (cx ≈ 905), com `pillar(ctx, "right")`.
- `cleide` (Cleideane, esposa): acenando, vai bem à esquerda (cx ≈ 300).
- `cammy` (filha ruiva): corte do lado direito, então use `flip=True` e encoste à esquerda (cx ≈ 215), com `pillar(ctx, "left")`.
- `isis` (Ísis, filha caçula): mãos no queixo; é menor, então funciona no centro ou à direita (cx ≈ 770).
- **Jorge** (`jar` em `draw.py`): o levain no pote, carente e sempre com fome.

Ordem de desenho: `background` → `av(...)` → `pillar(...)` → `counter` → adereços → efeitos → balões. A base de cada avatar fica escondida atrás do balcão.
Os avatares têm expressão fixa, sorrindo. As emoções vêm dos efeitos (`shock_fx`, `exclaim_fx`, `tears_fx`, `anger_fx`, `gloom_fx`, além de `sweat`, `heart` e `broken_heart`) e da animação (`lift` para pular ou falar, `shake` para tremer, `squash` para impacto e `rot` para inclinar). Para apontar balões e efeitos, use `head_top`, `head_c` e `eye_pts`.
Os adereços em `family.py` são `pizza`, `plate_with_slice`, `slice_in_hand`, `ketchup`, `splat`, `broken_heart` e `logo`. Use `LOGO = True` no episódio.
Personagens extras (amigos, vizinhos, avós) podem ser desenhados com `fam(...)` de `family.py`, que tem o mesmo traço vetorial, mudando cores e estilo de cabelo.

Os episódios de referência são `episodios/2026-11-05-ultima-fatia.py` e `episodios/2026-11-05-ketchup.py`.
