#!/usr/bin/env python3
"""
Fetch real per-language byte counts across a user's public, non-fork repos via
GitHub's REST API and write data/languages.json.

Uses the automatic GITHUB_TOKEN in Actions when available (5,000 req/hr) --
falls back to unauthenticated (60 req/hr) for local runs, which is fine for a
one-off but can get rate-limited on shared networks / repeated local testing.
"""
import json
import os
import sys

import requests

USERNAME = os.environ.get("GH_PROFILE_USER", "YOUR_GITHUB_USERNAME")
TOKEN = os.environ.get("GITHUB_TOKEN")  # auto-provided inside GitHub Actions
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "languages.json")

API = "https://api.github.com"
HEADERS = {"User-Agent": "profile-readme-bot/1.0", "Accept": "application/vnd.github+json"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def get(url, **params):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if resp.status_code == 403 and "rate limit" in resp.text.lower():
        print("rate limited -- try again later, or run this inside GitHub Actions "
              "where GITHUB_TOKEN gives a 5,000/hr limit", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


def list_repos():
    repos, page = [], 1
    while True:
        batch = get(f"{API}/users/{USERNAME}/repos", per_page=100, page=page, type="owner")
        if not batch:
            break
        repos.extend(r for r in batch if not r["fork"])
        page += 1
    return repos


def aggregate_languages(repos):
    totals = {}
    for repo in repos:
        langs = get(f"{API}/repos/{USERNAME}/{repo['name']}/languages")
        for lang, byte_count in langs.items():
            totals[lang] = totals.get(lang, 0) + byte_count
    return totals


if __name__ == "__main__":
    repos = list_repos()
    totals = aggregate_languages(repos)
    grand_total = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    data = {
        "username": USERNAME,
        "repo_count": len(repos),
        "languages": [
            {"name": name, "bytes": b, "pct": round(b / grand_total * 100, 1)}
            for name, b in ranked
        ],
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    top = ", ".join(f"{l['name']} {l['pct']}%" for l in data["languages"][:5])
    print(f"wrote {OUT_PATH}: {len(repos)} repos -- {top}")
