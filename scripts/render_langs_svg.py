#!/usr/bin/env python3
"""
Render data/languages.json (from fetch_languages.py) as a self-hosted, animated
top-languages bar card -- same terminal aesthetic as the rest of the profile.
Bars grow in once on load (CSS keyframes), then freeze. No external service,
so it can never 404 or get replaced by a "rate limited" placeholder image.
"""
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "languages.json")
OUT_PATH = os.path.join(HERE, "..", "langs.svg")

MAX_LANGS = 6

# Approximate GitHub linguist colors for common languages -- extend as needed.
LANG_COLORS = {
    "C++": "#f34b7d", "Python": "#3572A5", "C": "#555555",
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Kotlin": "#A97BFF",
    "HTML": "#e34c26", "CSS": "#563d7c", "Java": "#b07219",
    "Jupyter Notebook": "#DA5B0B", "Shell": "#89e051", "Dockerfile": "#384d54",
    "Go": "#00ADD8", "Rust": "#dea584", "PHP": "#4F5D95",
}
FALLBACK_COLOR = "#8b949e"

W = 869
PAD = 20
TITLEBAR_H = 30
ROW_H = 30
NAME_W = 108
PCT_W = 46
BAR_X = PAD + NAME_W
BAR_MAX_W = W - PAD - BAR_X - PCT_W

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
TRACK = "#161b22"

BAR_DUR = 0.7
STAGGER = 0.09


def render(data):
    langs = data["languages"][:MAX_LANGS]
    n = len(langs)
    top_y = TITLEBAR_H + 26
    H = top_y + n * ROW_H + 22

    css = f"""
@keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
@keyframes fade {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
.bar {{ transform-origin: left; animation: grow {BAR_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both; }}
.pct {{ opacity: 0; animation: fade 0.3s ease both; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>'
        f'<linearGradient id="lbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#lbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
                 f'text-anchor="middle">{data["username"]}@github: ~$ lang --stats</text>')
    parts.append(f'<text x="{PAD}" y="{TITLEBAR_H + 16}" fill="{MUTED}" font-size="10.5">'
                 f'top languages across {data["repo_count"]} public repos</text>')

    for i, lang in enumerate(langs):
        y = top_y + i * ROW_H
        color = LANG_COLORS.get(lang["name"], FALLBACK_COLOR)
        frac = max(lang["pct"] / langs[0]["pct"], 0.03)
        bar_w = BAR_MAX_W * frac
        delay = i * STAGGER
        name = lang["name"]
        if len(name) > 13:
            name = name[:12] + "\u2026"
        parts.append(f'<circle cx="{PAD+4}" cy="{y-4:.1f}" r="4" fill="{color}"/>')
        parts.append(f'<text x="{PAD+14}" y="{y:.1f}" fill="{INK}" font-size="12">{name}</text>')
        parts.append(f'<rect x="{BAR_X}" y="{y-11:.1f}" width="{BAR_MAX_W:.1f}" height="10" rx="5" fill="{TRACK}"/>')
        parts.append(
            f'<rect class="bar" x="{BAR_X}" y="{y-11:.1f}" width="{bar_w:.1f}" height="10" rx="5" '
            f'fill="{color}" style="animation-delay:{delay:.3f}s"/>'
        )
        parts.append(
            f'<text class="pct" x="{W-PAD}" y="{y:.1f}" fill="{MUTED}" font-size="11.5" text-anchor="end" '
            f'style="animation-delay:{delay+BAR_DUR-0.15:.3f}s">{lang["pct"]:.1f}%</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    data = json.load(open(IN_PATH))
    svg = render(data)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg)} bytes)")
