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

## Elenco fixo

- **Eu**: cabelo escuro, camisa azul e avental branco.
- **Amigo**: cabelo ruivo cacheado e camisa verde.
- **Jorge**: o levain no pote com pano xadrez vermelho, carente e sempre com fome.

Novos personagens podem usar `person_*` com outras cores (dicionário igual a `EU` e `AMIGO`).
