#!/usr/bin/env python3
"""Draw the figures of the book into src/img/: python3 fig.py

A card is one cell wide and every meld is three cells tall, so a three-card
meld is a square and a winning hand is seven squares.  胡 add up by eye: a
grey fill is the 1 胡 of a meld, a coin is the 1 胡 of a 將帥, and an empty
box is 0 胡.

    1  車馬炮 or 碰                 grey square
    K  將士象                       grey square, coin on its left card
    S  三色兵卒                     red, yellow and green stripes
    Q  四色兵卒                     the same with a white stripe, four wide
    D  暗刻, any 三胡三張組         dark square: 3 胡 is three times the grey
    G  單張將帥                     empty strip with the coin
    P  對子                         empty box, two wide

A colour and a piece are a real card, dyed like the cards of the text: y俥 is
the yellow 俥.  Two marks go before a card or a meld: + points a triangle at
the card that came from the table, ? draws what the hand is still waiting for,
dashed and faint.

The files are inlined with {{#include}}, so they take the page's ink and font.
Keep 顏色 + 棋子 out of the text: book.toml would turn it into a card.
"""
import math
import re
from pathlib import Path

U = 24  # one card
GAP = 16  # between blocks
FS = 14  # labels
CARDS = dict(zip("1KSQDGP", (3, 3, 3, 4, 3, 1, 2)))
STRIPES = "#d9534f", "#f0c541", "#4caf7d", "#fdfdf7"  # the cards of style.css
SHADE = {"1": 0.2, "K": 0.2, "D": 0.6}
COLORS = dict(zip("rygw", STRIPES))
INK = "#1b1b1b"  # on a card, whatever the theme
CARD = re.compile("[紅黃][帥仕相俥傌炮兵]|[綠白][將士象車馬包卒]")  # what book.toml replaces


def width(text, size=FS):
    return sum(size if ord(c) > 0x2E7F else size * 0.6 for c in text)


def parse(pieces):
    """Split a block into its (mark, kind): a kind of two characters is a real card."""
    out, mark, chars = [], "", iter(pieces)
    for c in chars:
        if c in "+?":
            mark = c
        else:
            out.append((mark, c + next(chars) if c in COLORS else c))
            mark = ""
    return out


def cells(kind):
    return CARDS.get(kind, 1)


def card(kind, x, y):
    return [
        f'<rect x="{x + 1.5}" y="{y + 1.5}" width="{U - 3}" height="{3 * U - 3}" rx="2" fill="{COLORS[kind[0]]}"/>',
        f'<text x="{x + U / 2:g}" y="{y + 1.5 * U + 6:g}" fill="{INK}" stroke="none" font-size="16" font-weight="bold" text-anchor="middle">{kind[1]}</text>',
    ]


def piece(kind, x, y, mark=""):
    out = card(kind, x, y) if len(kind) == 2 else meld(kind, x, y)
    if mark == "?":
        out = ['<g opacity="0.5" stroke-dasharray="4 3">', *out, "</g>"]
    if mark == "+":  # over the last card
        out.append(f'<path d="M{x + (cells(kind) - 0.5) * U - 5:g},{y - 8}h10l-5,7z" stroke="none"/>')
    return out


def meld(kind, x, y):
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


def bracket(a, b, y):
    return f'<path d="M{a:g},{y - 3}v-5H{b:g}v5" fill="none" stroke-width="1"/>'


def row(y, blocks, total=None, over=(), slots=False):
    """Blocks are (pieces, 胡, name): returns the shapes, the text and the size."""
    shapes, text, spans = [], [], []
    lid = y + 26 * bool(over)
    top = lid + 10 * any("+" in pieces for pieces, *_ in blocks)
    base = top + 3 * U + 10 * slots
    x = 0
    for pieces, *labels in blocks:
        start = x
        for mark, kind in parse(pieces):
            shapes += piece(kind, x, top, mark)
            x += cells(kind) * U
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
        shapes.append(bracket(spans[i][0] + 3, spans[j][1] - 3, lid))
        text.append(f'<text x="{(spans[i][0] + spans[j][1]) / 2:g}" y="{y + 13}">{label}</text>')
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
    return svg(alt, w, y, shapes, text)


def svg(alt, w, y, shapes, text):
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


def strip(alt, unit, parts, over, pad=0):
    """A bar to scale: parts are (length, shade, label), over are (from, to, label)."""
    shapes, text, x = [], [], 0
    for n, shade, label in parts:
        shapes.append(f'<rect x="{x + 1.5}" y="27.5" width="{n * unit - 3}" height="{U - 3}" rx="2" fill-opacity="{shade}"/>')
        text.append(f'<text x="{x + n * unit / 2:g}" y="{44 + U}">{label}</text>')
        x += n * unit
    for a, b, label in over:
        shapes.append(bracket(a * unit + 3, b * unit - 3, 26))
        text.append(f'<text x="{(a + b) * unit / 2:g}" y="13">{label}</text>')
    return svg(alt, x + pad, 52 + U, shapes, text)


def seats(alt):
    """Four seats around a table, the turn running anticlockwise from 你 at the bottom."""
    c, r, gap = 96, 72, math.radians(24)
    shapes = [f'<rect x="{c - 34}" y="{c - 34}" width="68" height="68" rx="4" fill="none"/>']
    text = [f'<text x="{c}" y="{c + 5}">逆時針</text>']
    for i, name in enumerate(("你", "下家", "對家", "上家")):
        a = math.pi / 2 * (1 - i)  # y points down, so the angle falls as the turn passes
        text.append(f'<text x="{c + r * math.cos(a):g}" y="{c + r * math.sin(a) + 5:g}" font-weight="bold">{name}</text>')
        (x0, y0), (x1, y1) = ((c + r * math.cos(t), c + r * math.sin(t)) for t in (a - gap, a - math.pi / 2 + gap))
        shapes.append(f'<path d="M{x0:.1f},{y0:.1f}A{r},{r} 0 0 0 {x1:.1f},{y1:.1f}" fill="none"/>')
        turn = math.degrees(math.atan2(y1 - c, x1 - c)) - 90  # the tangent where the arc ends
        shapes.append(f'<path d="M0,-5l9,5 -9,5z" stroke="none" transform="translate({x1:.1f},{y1:.1f}) rotate({turn:.1f})"/>')
    return svg(alt, 2 * c, 2 * c, shapes, text)


RICH = [("K", "2"), ("D", "3")]
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
            blocks=[("K", "2", "將士象"), ("D", "3", "三胡三張組")] + [("1", "1")] * 5,
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
    "play-seats": seats("四家圍著牌桌，逆時針輪流：你、右手邊的下家、對面的對家、左手邊的上家，再回到你"),
    "play-deck": strip(
        "112 張牌：莊家 21 張，另外三家各 20 張，共發出 81 張。牌堆 31 張，最多摸 25 張，最底下 6 張是廢牌",
        6,
        [(21, 0, "莊家 21 張"), (20, 0, "20 張"), (20, 0, "20 張"), (20, 0, "20 張"), (25, 0.2, "最多摸 25 張"), (6, 0.6, "廢牌 6 張")],
        [(0, 81, "發出 81 張"), (81, 112, "牌堆 31 張")],
        pad=8,
    ),
    "melds-hand": figure(
        "21 張牌排成八個牌組：將帥 1 胡、四色兵卒 5 胡、將士象 2 胡、車馬炮 1 胡、暗刻 3 胡、兩個對子 0 胡、胡的那一張湊成的車馬炮 1 胡，合計 13 胡",
        dict(
            blocks=[
                ("y帥", "1", "將帥"),
                ("r兵y兵g卒w卒", "5", "四色兵卒"),
                ("g將g士g象", "2", "將士象"),
                ("r俥r傌r炮", "1", "車馬炮"),
                ("w車w車w車", "3", "暗刻"),
                ("y仕y仕", "0", "對子"),
                ("r相r相", "0", "對子"),
                ("g車g馬+g包", "1", "車馬炮"),
            ],
            total="＝ 13 胡",
        ),
    ),
    "melds-belly": figure(
        "上排把三張俥拆成一個對子和一組車馬炮，不行。下排三張俥是暗刻，傌和炮等第四張俥",
        dict(blocks=[("y俥y俥", "對子"), ("y俥y傌y炮", "車馬炮")], total="不行"),
        dict(blocks=[("y俥y俥y俥", "暗刻"), ("?y俥y傌y炮", "等第四張")], total="可以"),
    ),
    "shrink-outside": figure(
        "每個牌組只有一張外來的牌：對子原有 1 張，三張的順子和碰原有 2 張，四色兵卒和槓原有 3 張，摸到的將帥原有 0 張",
        dict(
            blocks=[
                ("w馬+w馬", "1 張", "對子"),
                ("r俥r傌+r炮", "2 張", "順子"),
                ("g車g車+g車", "2 張", "碰"),
                ("r兵y兵g卒+w卒", "3 張", "四色兵卒"),
                ("y仕y仕y仕+y仕", "3 張", "槓"),
                ("+y帥", "0 張", "將帥"),
            ],
        ),
    ),
    "material-third": figure(
        "兩張將帥各配一個對子，剛好配完。又摸到一張將帥，還缺一個對子來配",
        dict(
            blocks=[("GP", "1"), ("GP", "1"), ("+G?P", "1", "還缺一個對子")],
            over=[(0, 1, "2 張將帥配兩個對子"), (2, 2, "又摸到一張")],
        ),
    ),
    "pairs-count": figure(
        "三手 10 胡的牌。上排：將士象和三胡三張組是 6 張 5 胡，兩張將帥各配一個對子，上限 2 個。中排：四色兵卒配一個對子是 6 張 5 胡，兩張將帥各配一個，上限 3 個。下排：兩個三胡三張組和一組將士象多出 2 胡，換三個對子，上限 3 個",
        dict(
            blocks=RICH + [("GP", "1")] * 2 + [("1", "1")] * 3,
            total="上限 2 個",
            over=[(0, 1, "6 張 5 胡"), (2, 3, "將帥各配一個"), (4, 6, "剩下三組")],
        ),
        dict(
            blocks=[("QP", "5")] + [("GP", "1")] * 2 + [("1", "1")] * 3,
            total="上限 3 個",
            over=[(0, 0, "6 張 5 胡，對子算一個"), (1, 2, "將帥各配一個"), (3, 5, "剩下三組")],
        ),
        dict(
            blocks=[("D", "3"), ("D", "3"), ("K", "2"), ("PPP", "0")] + [("1", "1")] * 2,
            total="上限 3 個",
            over=[(0, 1, "6 張 6 胡，多 1 胡"), (2, 2, "多 1 胡"), (3, 3, "2 胡換三個對子"), (4, 5, "剩下兩組")],
        ),
    ),
    "pairs-over": figure(
        "兩手牌都是 20 張 9 胡。上排照上限打，最後一組是車馬的搭子，等炮。下排多吃一個對子，最後一組是對子，等將帥來配",
        dict(
            blocks=RICH + [("GP", "1")] * 2 + [("1", "1")] * 2 + [("y俥y傌?y炮", "等順子")],
            total="9 胡，聽牌",
            over=[(2, 3, "上限 2 個")],
        ),
        dict(
            blocks=RICH + [("GP", "1")] * 2 + [("1", "1")] * 2 + [("?GP", "等將帥")],
            total="9 胡，聽牌",
            over=[(2, 3, "上限 2 個"), (6, 6, "多吃的")],
        ),
    ),
    "pairs-two": figure(
        "上排多吃兩個對子，各缺一張將帥，手上還有一張散牌，8 胡，沒有聽牌。下排自己摸到一張將帥，配掉一個對子，打掉散牌，9 胡，聽另一張將帥",
        dict(
            blocks=RICH + [("GP", "1")] * 2 + [("1", "1"), ("?GP", "0"), ("?GP", "0"), ("w士", "散牌")],
            total="8 胡，沒聽牌",
            over=[(2, 3, "上限 2 個"), (5, 6, "多吃兩個，佔 4 張")],
        ),
        dict(
            blocks=RICH + [("GP", "1")] * 2 + [("1", "1"), ("+GP", "1"), ("?GP", "等將帥")],
            total="9 胡，聽牌",
            over=[(2, 3, "上限 2 個"), (5, 5, "自己摸到")],
        ),
    ),
    "partial-waits": figure(
        "兩色兵卒等另外兩色的 8 張，吃成 3 胡。將士等 4 張象吃成將士象 2 胡，也等 3 張士吃成對子，配將帥 1 胡，合計 7 張。車馬等 4 張炮，吃成 1 胡",
        dict(blocks=[("r兵y兵",), ("?g卒" * 4 + "?w卒" * 4, "3 胡")], total="8 張"),
        dict(blocks=[("y帥y仕",), ("?y相" * 4, "2 胡"), ("?y仕" * 3, "1 胡")], total="7 張"),
        dict(blocks=[("y俥y傌",), ("?y炮" * 4, "1 胡")], total="4 張"),
    ),
    "eat-swap": figure(
        "吃之前，手上有一組車馬炮和一張散牌。吃進上家打的俥之後，桌上是一組車馬炮，手上原本的俥落單，另一張散牌打掉。胡數和散牌的張數都沒有變",
        dict(
            blocks=[("y俥y傌y炮", "1 胡"), ("w士", "散牌"), ("y俥", "打出")],
            over=[(0, 1, "手上"), (2, 2, "上家")],
            total="1 胡，1 張散牌",
        ),
        dict(
            blocks=[("+y俥y傌y炮", "1 胡"), ("y俥", "散牌"), ("w士", "打掉")],
            over=[(0, 0, "桌上"), (1, 1, "手上"), (2, 2, "棄牌")],
            total="1 胡，1 張散牌",
        ),
    ),
    "waiting-keep": figure(
        "上排打掉仕，剩下兩張帥和俥、炮，等傌，聽牌。下排打掉俥，剩下兩張帥和仕、炮兩張散牌，沒有聽牌",
        dict(
            blocks=[("r帥",), ("r帥",), ("r俥?r傌r炮",)],
            over=[(0, 1, "將帥"), (2, 2, "等傌")],
            total="打仕：聽牌",
        ),
        dict(
            blocks=[("r帥",), ("r帥",), ("r仕",), ("r炮",)],
            over=[(0, 1, "將帥"), (2, 3, "兩張散牌")],
            total="打俥：沒有聽牌",
        ),
    ),
    # The 12.2 胡 of payoff.md: lose 12, win 3 × 12.2 ≈ 37
    "payoff-swing": strip(
        "輸一局付 12，贏一局收 37，相差 49。多一胡只多收 3",
        10,
        [(12, 0, "輸一局 −12"), (37, 0.2, "贏一局 +37"), (3, 0.6, "多一胡 +3")],
        [(0, 49, "相差 49")],
        pad=14,
    ),
}

# The coin of 將帥, twice.  The title of the preface is inlined like the figures and
# takes the ink of the page.  A tab hands no ink to theme/favicon.svg, so that file
# flips itself to white on a dark browser, as the icon of mdbook does.
COIN = """<circle r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
<path d="M0,-3l3,3 -3,3 -3,-3z" fill="currentColor"/>
</svg>
"""
# The box is the outer edge of the ring: 6.5 and half the stroke
BOX = 'xmlns="http://www.w3.org/2000/svg" viewBox="-7.25 -7.25 14.5 14.5"'
TITLE = f"""<svg {BOX} width="80" height="80" role="img" aria-label="十胡">
<!-- Drawn by fig.py: edit the figure there -->
{COIN}"""
FAVICON = f"""<svg {BOX}>
<!-- Drawn by fig.py: edit the figure there -->
<style>@media (prefers-color-scheme: dark) {{ svg {{ color: white; }} }}</style>
{COIN}"""

if __name__ == "__main__":
    theme = Path(__file__).parent / "theme"
    theme.mkdir(exist_ok=True)
    (theme / "favicon.svg").write_text(FAVICON)
    out = Path(__file__).parent / "src" / "img"
    out.mkdir(exist_ok=True)
    (out / "coin.svg").write_text(TITLE)
    for name, text in FIGURES.items():
        assert not CARD.search(text), f"book.toml would turn {CARD.search(text)[0]} of {name} into a card"
        (out / f"{name}.svg").write_text(text)
