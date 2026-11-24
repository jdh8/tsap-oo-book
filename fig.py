#!/usr/bin/env python3
"""Draw the meld diagrams of 第二部 into src/img/: python3 fig.py

A card is one cell wide and every meld is three cells tall, so a three-card
meld is a square and a winning hand is seven squares.  胡 add up by eye: a
grey fill is the 1 胡 of a meld, a coin is the 1 胡 of a 將帥, and an empty
box is 0 胡.

    1  車馬炮 or 碰                 grey square
    K  將士象                       grey square, coin on its left card
    S  三色兵卒, any 三胡三張組     red, yellow and green stripes
    Q  四色兵卒                     the same with a white stripe, four wide
    D  暗刻                         dark square
    G  單張將帥                     empty strip with the coin
    P  對子                         empty box, two wide

The files are inlined with {{#include}}, so they take the page's ink and font.
Keep 顏色 + 棋子 out of the text: book.toml would turn it into a card.
"""
from pathlib import Path

U = 24  # one card
GAP = 16  # between blocks
FS = 14  # labels
CARDS = dict(zip("1KSQDGP", (3, 3, 3, 4, 3, 1, 2)))
STRIPES = "#d9534f", "#f0c541", "#4caf7d", "#fdfdf7"  # the cards of style.css
SHADE = {"1": 0.2, "K": 0.2, "D": 0.6}


def width(text, size=FS):
    return sum(size if ord(c) > 0x2E7F else size * 0.6 for c in text)


def piece(kind, x, y):
    n = CARDS[kind]
    w, h = n * U - 3, 3 * U - 3
    out = [
        f'<rect x="{x + 1.5 + i * w / n:g}" y="{y + 1.5}" width="{w / n:g}" height="{h}" fill="{color}" stroke-width="0.5"/>'
        for i, color in enumerate(STRIPES[:n] if kind in "SQ" else ())
    ]
    out.append(f'<rect x="{x + 1.5}" y="{y + 1.5}" width="{w}" height="{h}" rx="2" fill-opacity="{SHADE.get(kind, 0)}"/>')
    if kind in "KG":  # the coin and its square hole, standing on a corner
        cx, cy = x + U / 2, y + 1.5 * U
        out.append(f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="none"/>')
        out.append(f'<path d="M{cx},{cy - 3}l3,3 -3,3 -3,-3z" stroke="none"/>')
    return out


def row(y, blocks, total=None, over=(), slots=False):
    """Blocks are (pieces, 胡, name): returns the shapes, the text and the size."""
    shapes, text, spans = [], [], []
    top = y + 26 * bool(over)
    base = top + 3 * U + 10 * slots
    x = 0
    for pieces, *labels in blocks:
        start = x
        for kind in pieces:
            shapes += piece(kind, x, top)
            x += CARDS[kind] * U
        spans.append((start, x))
        if slots:  # one bracket for each group of three cards
            for a in range(start, x, 3 * U):
                shapes.append(f'<path d="M{a + 3},{top + 3 * U + 2}v5h{3 * U - 6}v-5" fill="none" stroke-width="1"/>')
        for i, label in enumerate(labels):
            assert width(label) <= x - start + GAP - 2, f"{label} is wider than {pieces}"
            bold = ' font-weight="bold"' * (i == 0)
            text.append(f'<text x="{(start + x) / 2:g}" y="{base + 18 * (i + 1)}"{bold}>{label}</text>')
        x += GAP
    for i, j, label in over:
        a, b = spans[i][0] + 3, spans[j][1] - 3
        shapes.append(f'<path d="M{a},{top - 3}v-5H{b}v5" fill="none" stroke-width="1"/>')
        text.append(f'<text x="{(a + b) / 2:g}" y="{y + 13}">{label}</text>')
    lines = max(len(block) - 1 for block in blocks)
    return shapes, text, (total, top + 1.5 * U + 6), x - GAP, base + 18 * lines + 8


def figure(alt, *rows):
    shapes, text, totals, w, y = [], [], [], 0, 0
    for spec in rows:
        s, t, total, right, y = row(y + 14 * bool(shapes), **spec)
        shapes += s
        text += t
        totals.append(total)
        w = max(w, right)
    for label, at in totals:
        if label:
            text.append(f'<text x="{w + 12}" y="{at}" font-size="16" font-weight="bold" text-anchor="start">{label}</text>')
    w += max(12 + width(label, 16) if label else 0 for label, _ in totals)
    return "\n".join([
        # Markdown needs the whole opening tag on one line and no blank lines inside
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-GAP / 2:g} 0 {w + GAP:g} {y}" width="{w + GAP:g}" height="{y}" role="img" aria-label="{alt}">',
        "<!-- Drawn by fig.py: edit the figure there -->",
        '<g fill="currentColor" stroke="currentColor" stroke-width="1.5">',
        *shapes,
        "</g>",
        f'<g fill="currentColor" font-size="{FS}" text-anchor="middle">',
        *text,
        "</g>",
        "</svg>",
        "",
    ])


RICH = [("K", "2"), ("S", "3")]
PAIRS = dict(
    blocks=RICH + [("PPP", "0")] + [("1", "1")] * 3,
    total="＝ 8 胡",
    over=[(0, 1, "6 張 5 胡"), (2, 2, "三個對子，佔兩組"), (3, 5, "剩下三組")],
)

FIGURES = {
    "seven-fit": figure(
        "四種湊成三張的配法：一張將帥配一個對子是一組，四色兵卒配一個對子是兩組，三張將帥是一組，三個對子是兩組",
        dict(
            blocks=[
                ("GP", "3 張 1 胡", "將帥配對子"),
                ("QP", "6 張 5 胡", "四色兵卒配對子"),
                ("GGG", "3 張 3 胡", "三張將帥"),
                ("PPP", "6 張 0 胡", "三個對子"),
            ],
            slots=True,
        ),
    ),
    "seven-ones": figure(
        "七組都是 1 胡：三組車馬炮、兩組碰、兩組將帥配對子，合計 7 胡",
        dict(
            blocks=[("1", "1", "車馬炮")] * 3 + [("1", "1", "碰")] * 2 + [("GP", "1", "將帥配對子")] * 2,
            total="＝ 7 胡",
        ),
    ),
    "seven-rich": figure(
        "比 1 胡多的四種組：將士象 2 胡，三色兵卒、暗刻、三張單張將帥各 3 胡",
        dict(
            blocks=[
                ("K", "2 胡", "將士象"),
                ("S", "3 胡", "三色兵卒"),
                ("D", "3 胡", "暗刻"),
                ("GGG", "3 胡", "三張單張將帥"),
            ],
        ),
    ),
    "seven-ten": figure(
        "上排：將士象 2 胡、三胡三張組 3 胡，加上五組 1 胡，合計 10 胡。下排：同樣的 6 張 5 胡，三個對子佔掉兩組，剩下三組各 1 胡，合計 8 胡",
        dict(
            blocks=[("K", "2", "將士象"), ("S", "3", "三胡三張組")] + [("1", "1")] * 5,
            total="＝ 10 胡",
            over=[(0, 1, "6 張 5 胡"), (2, 6, "另外五組，各 1 胡")],
        ),
        PAIRS,
    ),
    "seven-eight": figure(
        "上排：一組將士象加六組 1 胡，合計 8 胡。下排：6 張 5 胡、三個對子、三組 1 胡，合計 8 胡",
        dict(
            blocks=[("K", "2")] + [("1", "1")] * 6,
            total="＝ 8 胡",
            over=[(0, 0, "將士象"), (1, 6, "另外六組，各 1 胡")],
        ),
        PAIRS,
    ),
    "material-pair": figure(
        "將帥和士吃成對子是 3 張 1 胡，等到象湊成將士象是 3 張 2 胡",
        dict(blocks=[("GP", "3 張 1 胡", "吃成對子"), ("K", "3 張 2 胡", "等到順子")]),
    ),
}

if __name__ == "__main__":
    out = Path(__file__).parent / "src" / "img"
    out.mkdir(exist_ok=True)
    for name, svg in FIGURES.items():
        (out / f"{name}.svg").write_text(svg)
