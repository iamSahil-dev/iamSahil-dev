from PIL import Image, ImageEnhance, ImageFilter
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-prepped.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "sahil-ascii.svg")

# ============================================================
# QUALITY SETTINGS
# ============================================================

COLS = 190
ROWS = 120

CELL_W = 4.7
CELL_H = 7.2

RAMP = (
    " .'`^\",:;Il!i><~+_-?][}{1)(|\\/"
    "tfjrxnuvczXYUJCLQ0OZmwqpdbsahil*#MW&8%B@$"
)

CONTRAST = 1.75
BRIGHTNESS = 1.08
GAMMA = 0.82
SHARPEN = True
WHITE_FLOOR = 0.95

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30

ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H

CANVAS_W = int(ART_W + PAD * 2)
CANVAS_H = int(TITLEBAR_H + ART_H + STATUS_H + PAD)

BG = "#0d1117"
BG2 = "#111722"

FRAME = "#1f6feb"
TITLE_TEXT = "#7d8590"

INK = "#c9d1d9"

CURSOR = "#22d3ee"
SCAN = "#22d3ee"

ROW_DUR = 0.035
STAGGER = 0.018

# ============================================================
# IMAGE PROCESSING
# ============================================================

im = Image.open(SRC).convert("L")

if SHARPEN:
    im = im.filter(
        ImageFilter.UnsharpMask(
            radius=1.2,
            percent=260,
            threshold=1
        )
    )

im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
im = ImageEnhance.Contrast(im).enhance(CONTRAST)

im = im.resize((COLS, ROWS), Image.LANCZOS)

px = im.load()

STATIC = bool(os.environ.get("STATIC"))

rows_txt = []

for y in range(ROWS):
    chars = []

    for x in range(COLS):
        lum = px[x, y] / 255.0

        lum = pow(lum, GAMMA)

        if lum >= WHITE_FLOOR:
            chars.append(" ")
            continue

        idx = int(
            (1.0 - lum) *
            (len(RAMP) - 1) +
            0.5
        )

        idx = max(
            0,
            min(
                len(RAMP) - 1,
                idx
            )
        )

        chars.append(RAMP[idx])

    rows_txt.append(
        "".join(chars)
    )

art_top = TITLEBAR_H + PAD * 0.35

# ============================================================
# SVG
# ============================================================

parts = []

parts.append(
f'''
<svg xmlns="http://www.w3.org/2000/svg"
width="{CANVAS_W}"
height="{CANVAS_H}"
viewBox="0 0 {CANVAS_W} {CANVAS_H}"
font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
'''
)

parts.append(
f'''
<defs>

<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{BG2}"/>
<stop offset="100%" stop-color="{BG}"/>
</linearGradient>

<linearGradient id="scanLine" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{SCAN}" stop-opacity="0"/>
<stop offset="50%" stop-color="{SCAN}" stop-opacity="0.9"/>
<stop offset="100%" stop-color="{SCAN}" stop-opacity="0"/>
</linearGradient>

</defs>
'''
)

parts.append(
f'''
<rect width="{CANVAS_W}"
height="{CANVAS_H}"
rx="12"
fill="url(#bg)"/>
'''
)

parts.append(
f'''
<rect
x="0.5"
y="0.5"
width="{CANVAS_W-1}"
height="{CANVAS_H-1}"
rx="12"
fill="none"
stroke="{FRAME}"
stroke-width="1.3"
stroke-opacity="0.65"/>
'''
)

parts.append(
f'''
<line x1="0"
y1="{TITLEBAR_H}"
x2="{CANVAS_W}"
y2="{TITLEBAR_H}"
stroke="{FRAME}"/>
'''
)

dots = ["#ff5f56","#ffbd2e","#27c93f"]

for i,dot in enumerate(dots):
    parts.append(
    f'''
    <circle
    cx="{PAD+i*16}"
    cy="{TITLEBAR_H/2}"
    r="5"
    fill="{dot}"/>
    '''
    )

parts.append(
f'''
<text
x="{CANVAS_W/2}"
y="{TITLEBAR_H/2+4}"
fill="{TITLE_TEXT}"
font-size="12"
text-anchor="middle">
sahil@github: ~$ ./portrait.sh
</text>
'''
)

parts.append(
f'''
<g>

<circle
cx="{CANVAS_W-120}"
cy="{TITLEBAR_H/2}"
r="5"
fill="#ff6b6b">

<animate
attributeName="opacity"
values="1;0.15;1;0.15;1"
dur="2s"
repeatCount="indefinite"/>

</circle>

<text
x="{CANVAS_W-105}"
y="{TITLEBAR_H/2+4}"
fill="#ff7b7b"
font-size="11"
font-weight="600"
letter-spacing="2">

SCANNING

<animate
attributeName="opacity"
values="1;0.4;1"
dur="2s"
repeatCount="indefinite"/>

</text>

</g>
'''
)

font_size = CELL_H * 0.86

for ry,line in enumerate(rows_txt):

    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER

    safe = html.escape(line)

    text = (
        f'''
        <text xml:space="preserve"
        x="{PAD}"
        y="{y:.1f}"
        fill="{INK}"
        font-size="{font_size:.1f}"
        textLength="{ART_W}"
        lengthAdjust="spacing">
        {safe}
        </text>
        '''
    )

    if STATIC:
        parts.append(text)
        continue

    parts.append(
    f'''
    <clipPath id="r{ry}">
    <rect
    x="{PAD}"
    y="{row_y:.1f}"
    height="{CELL_H}"
    width="0">

    <animate
    attributeName="width"
    from="0"
    to="{ART_W}"
    begin="{delay:.3f}s"
    dur="{ROW_DUR:.2f}s"
    fill="freeze"/>

    </rect>
    </clipPath>
    '''
    )

    parts.append(
    f'''
    <g clip-path="url(#r{ry})">
    {text}
    </g>
    '''
    )

    parts.append(
    f'''
    <rect
    y="{row_y+1:.1f}"
    width="{CELL_W}"
    height="{CELL_H-2}"
    fill="{CURSOR}"
    opacity="0">

    <animate
    attributeName="x"
    from="{PAD}"
    to="{PAD+ART_W}"
    begin="{delay:.3f}s"
    dur="{ROW_DUR:.2f}s"
    fill="freeze"/>

    <set
    attributeName="opacity"
    to="0.85"
    begin="{delay:.3f}s"/>

    <set
    attributeName="opacity"
    to="0"
    begin="{delay+ROW_DUR:.3f}s"/>

    </rect>
    '''
    )

# ============================================================
# SCANNING EFFECT
# ============================================================

parts.append(
f'''
<rect
x="0"
y="{TITLEBAR_H}"
width="{CANVAS_W}"
height="5"
fill="url(#scanLine)">

<animate
attributeName="y"
values="{TITLEBAR_H};{CANVAS_H-60};{TITLEBAR_H}"
dur="6s"
repeatCount="indefinite"/>

</rect>
'''
)

parts.append(
f'''
<rect
x="0"
y="{TITLEBAR_H}"
width="{CANVAS_W}"
height="25"
fill="{SCAN}"
opacity="0.03">

<animate
attributeName="y"
values="{TITLEBAR_H};{CANVAS_H-60};{TITLEBAR_H}"
dur="6s"
repeatCount="indefinite"/>

</rect>
'''
)

# ============================================================
# STATUS BAR
# ============================================================

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19

parts.append(
f'''
<line
x1="0"
y1="{status_line_y:.1f}"
x2="{CANVAS_W}"
y2="{status_line_y:.1f}"
stroke="{FRAME}"/>
'''
)

parts.append(
f'''
<text
x="{PAD}"
y="{status_y:.1f}"
fill="{TITLE_TEXT}"
font-size="13">

sahil@github:~$ whoami

<tspan fill="{INK}">
 Sahil Kumar
</tspan>

</text>
'''
)

parts.append(
f'''
<rect
x="{PAD+250}"
y="{status_y-12:.1f}"
width="8"
height="14"
fill="{CURSOR}">

<animate
attributeName="opacity"
values="1;1;0;0"
keyTimes="0;0.5;0.51;1"
dur="1s"
repeatCount="indefinite"/>

</rect>
'''
)

parts.append("</svg>")

svg = "".join(parts)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(
    "wrote",
    OUT,
    len(svg),
    "bytes",
    CANVAS_W,
    "x",
    CANVAS_H
)