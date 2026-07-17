#!/usr/bin/env python3
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "languages.json")
OUT_PATH = os.path.join(HERE, "..", "langs.svg")

MAX_LANGS = 6

LANG_COLORS = {
    "C++": "#f34b7d",
    "Python": "#3572A5",
    "C": "#555555",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "Java": "#b07219",
    "React": "#61dafb",
    "Shell": "#89e051",
    "Dockerfile": "#384d54",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "PHP": "#4F5D95",
}

FALLBACK_COLOR = "#8b949e"

W = 869
PAD = 22
TITLEBAR_H = 30
ROW_H = 38

NAME_W = 120
PCT_W = 55

BAR_X = PAD + NAME_W
BAR_MAX_W = W - PAD - BAR_X - PCT_W

BG = "#0d1117"
BG2 = "#111722"

FRAME = "#1f6feb"

MUTED = "#7d8590"
INK = "#e6edf3"

TRACK = "#161b22"

GREEN = "#39d353"

BAR_DUR = 0.9
STAGGER = 0.10


def render(data):
    langs = data["languages"][:MAX_LANGS]

    n = len(langs)

    top_y = TITLEBAR_H + 52
    H = top_y + n * ROW_H + 35

    css = f"""
@keyframes grow {{
    from {{
        transform: scaleX(0);
    }}
    to {{
        transform: scaleX(1);
    }}
}}

@keyframes fade {{
    from {{
        opacity:0;
        transform:translateX(-8px);
    }}
    to {{
        opacity:1;
        transform:translateX(0);
    }}
}}

@keyframes breathe {{
    0% {{
        opacity:1;
    }}
    50% {{
        opacity:.75;
    }}
    100% {{
        opacity:1;
    }}
}}

.bar {{
    transform-origin:left;
    animation:
        grow {BAR_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both;
}}

.label {{
    opacity:0;
    animation:fade .5s ease forwards;
}}

.live {{
    animation:breathe 2s ease-in-out infinite;
}}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',

        f'<style>{css}</style>',

        '<defs>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{BG2}"/>'
        f'<stop offset="100%" stop-color="{BG}"/>'
        f'</linearGradient>'
        '</defs>',

        f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>',

        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" '
        f'rx="14" fill="none" stroke="{FRAME}" stroke-opacity=".6"/>',

        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" '
        f'stroke="{FRAME}" stroke-opacity=".45"/>'
    ]

    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(
            f'<circle cx="{PAD+i*16}" '
            f'cy="{TITLEBAR_H/2}" r="5.5" fill="{dot}"/>'
        )

    parts.append(
        f'<text x="{W/2}" y="{TITLEBAR_H/2+4}" '
        f'fill="{MUTED}" font-size="12" '
        f'text-anchor="middle">'
        f'sahil@github: ~/stack --profile'
        f'</text>'
    )

    parts.append(
        f'<text x="{PAD}" '
        f'y="{TITLEBAR_H+20}" '
        f'fill="{MUTED}" '
        f'font-size="11">'
        f'compiled from repositories and active projects'
        f'</text>'
    )

    for i, lang in enumerate(langs):

        y = top_y + i * ROW_H

        color = LANG_COLORS.get(
            lang["name"],
            FALLBACK_COLOR
        )

        frac = max(
            lang["pct"] / langs[0]["pct"],
            0.03
        )

        bar_w = BAR_MAX_W * frac

        delay = i * STAGGER

        name = lang["name"]

        if len(name) > 15:
            name = name[:14] + "…"

        parts.append(
            f'<circle '
            f'class="label" '
            f'cx="{PAD+6}" '
            f'cy="{y-5}" '
            f'r="4" '
            f'fill="{color}" '
            f'style="animation-delay:{delay:.2f}s"/>'
        )

        parts.append(
            f'<text class="label" '
            f'x="{PAD+18}" '
            f'y="{y}" '
            f'fill="{INK}" '
            f'font-size="13" '
            f'font-weight="600" '
            f'style="animation-delay:{delay:.2f}s">'
            f'{name}'
            f'</text>'
        )

        parts.append(
            f'<rect '
            f'x="{BAR_X}" '
            f'y="{y-12}" '
            f'width="{BAR_MAX_W}" '
            f'height="12" '
            f'rx="6" '
            f'fill="{TRACK}"/>'
        )

        pulse = ""

        if i == 0:
            pulse = '''
            <animate
                attributeName="opacity"
                values="1;.75;1"
                dur="2.5s"
                repeatCount="indefinite"/>
            '''

        parts.append(
            f'''
            <rect
                class="bar"
                x="{BAR_X}"
                y="{y-12}"
                width="{bar_w:.1f}"
                height="12"
                rx="6"
                fill="{color}"
                style="animation-delay:{delay:.2f}s">

                {pulse}

                <title>
                    {lang["name"]}: {lang["pct"]:.1f}% of tracked code
                </title>

            </rect>
            '''
        )

        parts.append(
            f'<text class="label" '
            f'x="{W-PAD}" '
            f'y="{y}" '
            f'fill="{MUTED}" '
            f'font-size="12" '
            f'text-anchor="end" '
            f'style="animation-delay:{delay+0.45:.2f}s">'
            f'{lang["pct"]:.1f}%'
            f'</text>'
        )

    parts.append("</svg>")

    return "".join(parts)


if __name__ == "__main__":
    data = json.load(open(IN_PATH))

    svg = render(data)

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(svg)

    print(f"wrote {OUT_PATH}")