import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 540, 470

PAD = 20
TITLEBAR_H = 30

KEY_X = PAD
VAL_X = PAD + 120

LINE_H = 22

BG = "#0d1117"
BG2 = "#111722"

FRAME = "#1f6feb"

MUTED = "#7d8590"
INK = "#c9d1d9"

KEY = "#ffa657"
SECTION = "#58a6ff"

GREEN = "#3fb950"
ACCENT = "#22d3ee"

HOST = "sahilkumar"

ROWS = [
    ("host",),

    ("kv", "Education", "B.Tech CCE • Manipal University Jaipur"),
    ("kv", "Graduation", "2028 • GPA 9.12/10"),

    ("gap",),

    ("sec", "Tech Stack"),

    ("kv", "Languages", "C • C++ • Python • JavaScript • SQL"),
    ("kv", "Web Dev", " HTML • CSS • React.js • Node.js • Firebase • REST APIs"),
    ("kv", "Tools", "Git • GitHub • Linux • VS Code"),

    ("gap",),

    ("sec", "Computer Science"),

    ("kv", "Cs Core", "DSA • OOP • DBMS • OS • CN"),
    ("kv", "Learning", "Machine Learning • Deep Learning"),

    ("gap",),

    ("sec", "Projects"),

    ("bul", "KrishiSetu", "AI-powered agriculture marketplace"),
    ("bul", "i-Blood", "Real-time donor matching platform"),
    ("bul", "Daksh", "Browser-based AI + AR/VR vocational learning platform"),

    ("gap",),

    ("sec", "Currently"),

    ("bul2", "Learning Machine Learning and Deep Learning"),
    ("bul2", "Exploring Computer Vision and Generative AI"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"

    delay = 0.15 + i * 0.06

    return (
        f'''
        <g opacity="0" transform="translate(0,6)">
            {inner}

            <animate
                attributeName="opacity"
                from="0"
                to="1"
                begin="{delay:.2f}s"
                dur="0.4s"
                fill="freeze"/>

            <animateTransform
                attributeName="transform"
                type="translate"
                from="0 6"
                to="0 0"
                begin="{delay:.2f}s"
                dur="0.4s"
                fill="freeze"
                calcMode="spline"
                keySplines="0.2 0.8 0.2 1"/>
        </g>
        '''
    )


parts = [
    f'''
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{W}"
         height="{H}"
         viewBox="0 0 {W} {H}"
         font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
    ''',

    f'''
    <defs>

        <linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="{BG2}"/>
            <stop offset="100%" stop-color="{BG}"/>
        </linearGradient>

    </defs>
    ''',

    f'''
    <rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>
    ''',

    f'''
    <rect
        x="0.5"
        y="0.5"
        width="{W-1}"
        height="{H-1}"
        rx="12"
        fill="none"
        stroke="{FRAME}"
        stroke-width="1.2"
        stroke-opacity="0.65"/>
    ''',

    f'''
    <line
        x1="0"
        y1="{TITLEBAR_H}"
        x2="{W}"
        y2="{TITLEBAR_H}"
        stroke="{FRAME}"/>
    '''
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(
        f'''
        <circle
            cx="{PAD + i*16}"
            cy="{TITLEBAR_H/2}"
            r="5"
            fill="{dotcol}"/>
        '''
    )

parts.append(
f'''
<text
    x="{W/2}"
    y="{TITLEBAR_H/2 + 4}"
    fill="{MUTED}"
    font-size="12"
    text-anchor="middle">

    {HOST}@github: ~$ neofetch

</text>
'''
)

# LIVE indicator
parts.append(
f'''
<g>

    <circle
        cx="{W-90}"
        cy="{TITLEBAR_H/2}"
        r="4"
        fill="#3fb950">

        <animate
            attributeName="opacity"
            values="1;0.3;1"
            dur="1.8s"
            repeatCount="indefinite"/>

    </circle>

    <text
        x="{W-80}"
        y="{TITLEBAR_H/2+4}"
        fill="#3fb950"
        font-size="10"
        font-weight="700">

        LIVE

        <animate
            attributeName="opacity"
            values="1;0.4;1"
            dur="1.8s"
            repeatCount="indefinite"/>

    </text>

</g>
'''
)

y = TITLEBAR_H + 30

for i, row in enumerate(ROWS):

    kind = row[0]

    if kind == "gap":
        y += LINE_H * 0.5
        continue

    if kind == "host":

        rule_x = KEY_X + 105

        inner = (
            f'''
            <text x="{KEY_X}" y="{y:.1f}" font-size="14" font-weight="700">

                <tspan fill="{GREEN}">{HOST}</tspan>
                <tspan fill="{MUTED}">@</tspan>
                <tspan fill="{ACCENT}">github</tspan>

            </text>

            <line
                x1="{rule_x}"
                y1="{y-4:.1f}"
                x2="{W-PAD}"
                y2="{y-4:.1f}"
                stroke="{FRAME}"
                stroke-opacity="0.8"/>
            '''
        )

    elif kind == "sec":

        title = esc(row[1])

        inner = (
            f'''
            <text
                x="{KEY_X}"
                y="{y:.1f}"
                fill="{SECTION}"
                font-size="12.5"
                font-weight="700">

                — {title}

                <animate
                    attributeName="opacity"
                    values="0.6;1;0.6"
                    dur="4s"
                    repeatCount="indefinite"/>

            </text>

            <line
                x1="{KEY_X + 12 + len(row[1])*8}"
                y1="{y-4:.1f}"
                x2="{W-PAD}"
                y2="{y-4:.1f}"
                stroke="{FRAME}"
                stroke-opacity="0.8"/>
            '''
        )

    elif kind == "kv":

        inner = (
            f'''
            <text
                x="{KEY_X}"
                y="{y:.1f}"
                fill="{KEY}"
                font-size="12.5"
                font-weight="700">

                {esc(row[1])}

            </text>

            <text
                x="{VAL_X}"
                y="{y:.1f}"
                fill="{INK}"
                font-size="12.5">

                {esc(row[2])}

            </text>
            '''
        )

    elif kind == "bul":
        inner = (
        f'''
        <circle
            cx="{KEY_X+3}"
            cy="{y-4:.1f}"
            r="2.5"
            fill="{GREEN}"/>

        <text
            x="{KEY_X+14}"
            y="{y:.1f}"
            fill="{ACCENT}"
            font-size="12.5"
            font-weight="700">

            {esc(row[1])}

        </text>

        <text
            x="{KEY_X+125}"
            y="{y:.1f}"
            fill="{MUTED}"
            font-size="12">

            →

        </text>

        <text
            x="{KEY_X+145}"
            y="{y:.1f}"
            fill="{INK}"
            font-size="12.5">

            {esc(row[2])}

        </text>
        '''
    )
        
    elif kind == "bul2":
        inner = (
        f'''
        <circle
            cx="{KEY_X+3}"
            cy="{y-4:.1f}"
            r="2.5"
            fill="{GREEN}"/>

        <text
            x="{KEY_X+14}"
            y="{y:.1f}"
            fill="{INK}"
            font-size="12.5">

            {esc(row[1])}

        </text>
        '''
    )

    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")

svg = "".join(parts)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(
    "wrote",
    OUT,
    len(svg),
    "bytes;",
    W,
    "x",
    H
)