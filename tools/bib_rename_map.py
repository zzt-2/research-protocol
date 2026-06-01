#!/usr/bin/env python3
"""
Generate citekey rename mapping for AUTHOR-MISMATCH entries.
Crossref found the correct paper but citekey has wrong first author.

Usage:
  python tools/bib_rename_map.py    # Generate mapping table
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
RATE_LIMIT = 0.4


def parse_bib(path):
    text = path.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(r"(@\w+\{.+?)(?=\n@|\Z)", text, re.DOTALL):
        raw = m.group(1).strip()
        km = re.match(r"@\w+\{([^,]+),", raw)
        if not km:
            continue
        citekey = km.group(1)
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{([^}]*)\}", raw):
            fields[fm.group(1).lower()] = fm.group(2)
        entries.append({"citekey": citekey, "raw": raw, "fields": fields})
    return entries


def word_overlap(t1, t2):
    w1 = set(re.findall(r'\b\w{3,}\b', t1.lower()))
    w2 = set(re.findall(r'\b\w{3,}\b', t2.lower()))
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / min(len(w1), len(w2))


def normalize_surname(s):
    import unicodedata
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', s)


def extract_year_suffix(citekey):
    """Extract year and suffix from citekey like 'chen2025dsp' → (2025, 'dsp')."""
    m = re.match(r'[a-z]+(\d{4})(.*)', citekey)
    if m:
        return int(m.group(1)), m.group(2)
    return None, ''


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
        print(f"ERR:{e}", end=" ", flush=True)
    return []


def format_authors(item):
    parts = []
    for a in item.get("author", []):
        given = a.get("given", "")
        family = a.get("family", "")
        parts.append(f"{given} {family}".strip())
    return " and ".join(parts)


def main():
    entries = parse_bib(BIB_PATH)
    existing_keys = {e["citekey"] for e in entries}

    # Find entries with "and others" that have real titles (>=3 words)
    targets = []
    for e in entries:
        author = e["fields"].get("author", "")
        if "others" not in author.lower():
            continue
        lang = e["fields"].get("language", "")
        if lang == "chinese" or any(ord(c) > 0x4e00 for c in author[:6]):
            continue
        title = e["fields"].get("title", "").replace("{", "").replace("}", "")
        if len(title.split()) < 3:
            continue
        targets.append(e)

    print(f"Entries with real titles and 'and others': {len(targets)}\n")

    renames = []  # (old_ck, new_ck, first_author, n_authors, real_title, overlap)

    for i, entry in enumerate(targets):
        ck = entry["citekey"]
        title = entry["fields"].get("title", "").replace("{", "").replace("}", "")

        print(f"[{i+1}/{len(targets)}] {ck}: ", end="", flush=True)

        items = cr_search(title, rows=3)
        time.sleep(RATE_LIMIT)

        if not items:
            print("NOT FOUND")
            continue

        # Find best match by title overlap
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
        res_title = best_item.get("title", [""])[0] if best_item.get("title") else ""

        if not authors_str:
            print("NO-AUTHORS")
            continue

        first_author = authors_str.split(" and ")[0].strip()
        if not first_author:
            print("NO-FIRST-AUTHOR")
            continue

        # Extract first author surname
        if "," in first_author:
            surname_raw = first_author.split(",")[0].strip()
        else:
            surname_raw = first_author.split()[-1]
        surname_norm = normalize_surname(surname_raw)

        # Generate new citekey
        year, suffix = extract_year_suffix(ck)
        new_ck = f"{surname_norm}{year}{suffix}" if year else f"{surname_norm}{ck}"

        # Check if new citekey collides with existing (and is different from old)
        collision = ""
        if new_ck == ck:
            collision = "(SAME - citekey already correct)"
        elif new_ck in existing_keys:
            collision = f"(COLLISION with existing {new_ck}!)"

        n = len(authors_str.split(" and "))
        print(f"{first_author} → {new_ck} {collision}")
        renames.append((ck, new_ck, first_author, n, res_title[:70], best_sim, collision))

    print(f"\n{'='*80}")
    print(f"Mapping table ({len(renames)} entries):\n")
    print(f"| old_citekey | new_citekey | first_author | n_authors | overlap | note |")
    print(f"|-------------|-------------|--------------|-----------|---------|------|")
    for old, new, first, n, title, sim, note in renames:
        print(f"| {old} | {new} | {first} | {n} | {sim:.0%} | {note or 'OK'} |")

    # Print rename commands for review
    print(f"\n# Renames to apply:")
    for old, new, first, n, title, sim, note in renames:
        if old != new and "COLLISION" not in note:
            print(f"# {old} → {new} ({first}, {n} authors)")


if __name__ == "__main__":
    main()
