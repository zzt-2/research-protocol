#!/usr/bin/env python3
"""
Crossref-only author enrichment (avoids SS rate limits).
Handles both surname-based and topic-based citekeys.

Usage:
  python tools/bib_enrich_cr.py                 # Dry run
  python tools/bib_enrich_cr.py --apply         # Update bib
"""

import re
import sys
import time
import argparse
from pathlib import Path

try:
    import requests
except ImportError:
    print("pip install requests")
    sys.exit(1)

BIB_PATH = Path("毕设/写作材料/references.bib")
TOPIC_PREFIXES = ('fpga', 'cpr', 'all', 'param', 'perf', 'improved', 'phasync')
RATE_LIMIT = 0.3  # seconds between Crossref requests


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


def normalize_name(s):
    import unicodedata
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.replace('-', '').replace(' ', '').replace('.', '')


def is_surname_citekey(citekey):
    prefix = re.match(r'([a-z]+)', citekey)
    if not prefix:
        return False
    return not any(prefix.group(1).startswith(t) for t in TOPIC_PREFIXES)


def validate_author(citekey, authors_str):
    """For surname-based citekeys, verify first author matches. Always True for topic-based."""
    if not is_surname_citekey(citekey):
        return True
    km = re.match(r'([a-z]+)', citekey)
    key_surname = normalize_name(km.group(1))
    first_author = authors_str.split(" and ")[0].strip()
    if "," in first_author:
        first_surname = normalize_name(first_author.split(",")[0].strip())
    else:
        parts = first_author.split()
        first_surname = normalize_name(parts[-1]) if parts else ""
    return (key_surname and first_surname
            and (key_surname in first_surname or first_surname in key_surname))


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
    authors = item.get("author", [])
    parts = []
    for a in authors:
        given = a.get("given", "")
        family = a.get("family", "")
        parts.append(f"{given} {family}".strip())
    return " and ".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    entries = parse_bib(BIB_PATH)
    targets = []
    for e in entries:
        author = e["fields"].get("author", "")
        if "others" not in author.lower():
            continue
        lang = e["fields"].get("language", "")
        if lang == "chinese" or any(ord(c) > 0x4e00 for c in author[:6]):
            continue
        targets.append(e)

    print(f"Total: {len(entries)}, Need update: {len(targets)}")
    if args.limit > 0:
        targets = targets[:args.limit]
        print(f"Limit: {args.limit}")

    results = []  # (citekey, status, authors_str, overlap, real_title)

    for i, entry in enumerate(targets):
        ck = entry["citekey"]
        title = entry["fields"].get("title", "").replace("{", "").replace("}", "")
        is_topic = not is_surname_citekey(ck)

        print(f"[{i+1}/{len(targets)}] {ck} ({'topic' if is_topic else 'surname'}): ", end="", flush=True)

        if len(title.split()) < 3:
            print(f"SKIP (short title: '{title}')")
            results.append((ck, "short_title", "", 0.0, ""))
            continue

        items = cr_search(title, rows=3)
        time.sleep(RATE_LIMIT)

        if not items:
            print("NOT FOUND")
            results.append((ck, "not_found", "", 0.0, ""))
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
            res_title = best_item.get("title", [""])[0] if best_item else ""
            print(f"LOW-OVERLAP ({best_sim:.0%}: {res_title[:50]})")
            results.append((ck, "low_overlap", "", best_sim, res_title[:60]))
            continue

        authors_str = format_authors(best_item)
        res_title = best_item.get("title", [""])[0] if best_item.get("title") else ""

        # Reject empty/incomplete author lists
        if not authors_str or not authors_str.split(" and ")[0].strip():
            print(f"NO-AUTHORS ({best_sim:.0%})")
            results.append((ck, "no_authors", "", best_sim, res_title[:60]))
            continue

        # Validate author (skip for topic-based citekeys)
        if not validate_author(ck, authors_str):
            print(f"AUTHOR-MISMATCH ({authors_str.split(' and ')[0][:20]})")
            results.append((ck, "author_mismatch", authors_str, best_sim, res_title[:60]))
            continue

        n = len(authors_str.split(" and "))
        print(f"OK ({best_sim:.0%}, {n} authors, {authors_str.split(' and ')[0][:20]})")
        results.append((ck, "ok", authors_str, best_sim, res_title[:80]))

    ok = sum(1 for r in results if r[1] == "ok")
    not_found = sum(1 for r in results if r[1] == "not_found")
    low = sum(1 for r in results if r[1] == "low_overlap")
    mismatch = sum(1 for r in results if r[1] == "author_mismatch")
    short = sum(1 for r in results if r[1] == "short_title")
    print(f"\nOK: {ok}, Not found: {not_found}, Low overlap: {low}, Author mismatch: {mismatch}, Short title: {short}")

    # Apply
    if args.apply and ok > 0:
        bib_text = BIB_PATH.read_text(encoding="utf-8")
        applied = 0
        for ck, status, authors_str, _, _ in results:
            if status != "ok":
                continue
            pattern = rf"(@\w+\{{{ck},.*?author\s*=\s*\{{)([^}}]*)(\}})"
            def replacer(m, a=authors_str):
                return m.group(1) + a + m.group(3)
            new_text = re.sub(pattern, replacer, bib_text, count=1, flags=re.DOTALL)
            if new_text != bib_text:
                bib_text = new_text
                applied += 1
            else:
                print(f"  WARNING: could not replace author for {ck}")
        BIB_PATH.write_text(bib_text, encoding="utf-8")
        print(f"Applied {applied} author updates to {BIB_PATH}")
    elif not args.apply:
        print("\nDry run. Use --apply to update bib.")


if __name__ == "__main__":
    main()
