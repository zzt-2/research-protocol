#!/usr/bin/env python3
"""
Apply 14 high-confidence citekey renames + author updates.
Updates both references.bib and material-chapter-literature.md.

Usage:
  python tools/bib_rename_apply.py                 # Dry run
  python tools/bib_rename_apply.py --apply          # Apply changes
"""

import re
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("pip install requests")
    sys.exit(1)

BIB_PATH = Path("毕设/写作材料/references.bib")
LIT_PATH = Path("毕设/写作材料/material-chapter-literature.md")
RATE_LIMIT = 0.4

# 14 high-confidence renames: old_ck → (new_ck, title_for_search)
RENAMES = {
    "chen2025dsp": "valjus2025dsp",
    "rustum2026elsevier": "habib2026elsevier",
    "boroson2022lcrd": "edwards2022lcrd",
    "fields2014edrs": "heine2014edrs",
    "cornwell2019nasa": "lesh2019nasa",
    "seimetz2023flex": "zhang2023flex",
    "malik2025": "han2025",
    "li2024jlt": "lu2024jlt",
    "zhang2021trends": "fernandes2021trends",
    "liu2023carrier": "tsujioka2023carrier",
    "fernandes2024fiber": "davies2024fiber",
    "lee2009diversity": "zhu2009diversity",
    "younus2024overview": "begley2024overview",
}


def word_overlap(t1, t2):
    w1 = set(re.findall(r'\b\w{3,}\b', t1.lower()))
    w2 = set(re.findall(r'\b\w{3,}\b', t2.lower()))
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / min(len(w1), len(w2))


def cr_search(title, rows=3):
    try:
        r = requests.get(
            "https://api.crossref.org/works",
            params={"query.title": title, "rows": rows},
            headers={"User-Agent": "bib-enrich/1.0 (mailto:research@example.com)"},
            timeout=20,
        )
        if r.status_code == 200:
            return r.json().get("message", {}).get("items", [])
    except Exception as e:
        print(f"ERR:{e}")
    return []


def format_authors(item):
    parts = []
    for a in item.get("author", []):
        given = a.get("given", "")
        family = a.get("family", "")
        parts.append(f"{given} {family}".strip())
    return " and ".join(parts)


def parse_bib(path):
    return path.read_text(encoding="utf-8")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    bib_text = parse_bib(BIB_PATH)
    lit_text = LIT_PATH.read_text(encoding="utf-8") if LIT_PATH.exists() else ""

    applied_bib = 0
    applied_lit = 0
    results = []

    for i, (old_ck, new_ck) in enumerate(RENAMES.items()):
        print(f"[{i+1}/{len(RENAMES)}] {old_ck} → {new_ck}: ", end="", flush=True)

        # Extract title from bib
        title_m = re.search(
            rf"(@\w+\{{{old_ck},.*?title\s*=\s*\{{)([^}}]*)(\}})",
            bib_text, re.DOTALL
        )
        if not title_m:
            print("NOT IN BIB")
            continue

        title = title_m.group(2).replace("{", "").replace("}", "")

        # Search Crossref
        items = cr_search(title, rows=3)
        time.sleep(RATE_LIMIT)

        if not items:
            print("NOT FOUND")
            continue

        # Pick best match by title overlap
        best_item, best_sim = None, 0.0
        for item in items:
            res_title = item.get("title", [""])[0] if item.get("title") else ""
            sim = word_overlap(title, res_title)
            if sim > best_sim:
                best_sim = sim
                best_item = item

        if not best_item or best_sim < 0.3:
            print(f"LOW-OVERLAP ({best_sim:.0%})")
            continue

        authors_str = format_authors(best_item)
        if not authors_str or not authors_str.split(" and ")[0].strip():
            print("NO-AUTHORS")
            continue

        n = len(authors_str.split(" and "))
        print(f"{authors_str.split(' and ')[0][:25]} ({n} auth, {best_sim:.0%})")

        results.append((old_ck, new_ck, authors_str, best_sim))

        if args.apply:
            # 1. Rename citekey in bib
            bib_text = bib_text.replace(f"{{{old_ck},", f"{{{new_ck},")

            # 2. Replace author field in bib
            pattern = rf"(@\w+\{{{new_ck},.*?author\s*=\s*\{{)([^}}]*)(\}})"
            def replacer(m, a=authors_str):
                return m.group(1) + a + m.group(3)
            new_bib = re.sub(pattern, replacer, bib_text, count=1, flags=re.DOTALL)
            if new_bib != bib_text:
                bib_text = new_bib
                applied_bib += 1
            else:
                print(f"  WARNING: author replacement failed for {new_ck}")

            # 3. Rename citekey in literature list (word-boundary safe)
            lit_text = re.sub(
                rf'\b{old_ck}\b', new_ck, lit_text
            )
            applied_lit += 1

    print(f"\nLooked up: {len(results)}, Ready to apply: {len(results)}")

    if args.apply and results:
        BIB_PATH.write_text(bib_text, encoding="utf-8")
        print(f"Bib updated: {applied_bib} author fields + {len(results)} citekey renames")
        if lit_text:
            LIT_PATH.write_text(lit_text, encoding="utf-8")
            print(f"Lit list updated: {applied_lit} citekey renames")
    elif results:
        print("\nDry run. Use --apply to update files.")


if __name__ == "__main__":
    main()
