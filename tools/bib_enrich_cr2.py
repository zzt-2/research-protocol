#!/usr/bin/env python3
"""
Second-pass Crossref enrichment: search by author surname + year + keywords.
Handles entries that failed pure title search.

Usage:
  python tools/bib_enrich_cr2.py                 # Dry run
  python tools/bib_enrich_cr2.py --apply         # Update bib
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


def extract_surname_year(citekey):
    """Extract author surname and year from citekey like 'chen2025dsp'."""
    m = re.match(r'([a-z]+?)(\d{4})', citekey)
    if m:
        return m.group(1), int(m.group(2))
    return None, None


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


def validate_author(citekey, authors_str):
    surname, _ = extract_surname_year(citekey)
    if not surname:
        return True
    key_norm = normalize_name(surname)
    first_author = authors_str.split(" and ")[0].strip()
    if not first_author:
        return False
    if "," in first_author:
        first_surname = normalize_name(first_author.split(",")[0].strip())
    else:
        parts = first_author.split()
        first_surname = normalize_name(parts[-1]) if parts else ""
    if not first_surname:
        return False
    return key_norm in first_surname or first_surname in key_norm


def cr_search_author_title(surname, year, keywords, rows=5):
    """Search Crossref by author surname + year + keywords."""
    try:
        params = {
            "query.author": surname,
            "query": keywords,
            "rows": rows,
        }
        if year:
            params["filter"] = f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31"

        r = requests.get(
            "https://api.crossref.org/works",
            params=params,
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


def extract_keywords(title):
    """Extract meaningful keywords from (possibly abbreviated) title."""
    # Remove common non-informative words
    stop = {'and', 'for', 'the', 'with', 'from', 'based', 'using', 'over', 'under'}
    words = re.findall(r'\b\w{3,}\b', title.lower())
    return ' '.join(w for w in words if w not in stop)


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

    print(f"Total with 'and others': {len(targets)}")
    if args.limit > 0:
        targets = targets[:args.limit]
        print(f"Limit: {args.limit}")

    results = []

    for i, entry in enumerate(targets):
        ck = entry["citekey"]
        title = entry["fields"].get("title", "").replace("{", "").replace("}", "")
        surname, year = extract_surname_year(ck)

        print(f"[{i+1}/{len(targets)}] {ck} ({surname}/{year}): ", end="", flush=True)

        if not surname:
            print("SKIP (no surname)")
            results.append((ck, "no_surname", "", 0.0, ""))
            continue

        # Build keyword query from title
        keywords = extract_keywords(title)
        if not keywords:
            # Use the raw title as-is
            keywords = title

        items = cr_search_author_title(surname, year, keywords, rows=5)
        time.sleep(RATE_LIMIT)

        if not items:
            # Try without year filter (some years might be off)
            items = cr_search_author_title(surname, None, keywords, rows=5)
            time.sleep(RATE_LIMIT)

        if not items:
            print("NOT FOUND")
            results.append((ck, "not_found", "", 0.0, ""))
            continue

        # Pick best match: prefer items where author surname matches
        best_item, best_score = None, -1
        for item in items:
            res_title = item.get("title", [""])[0] if item.get("title") else ""
            authors_str = format_authors(item)

            # Score: title overlap + author match bonus
            sim = word_overlap(title, res_title) if len(title.split()) >= 3 else 0.0
            author_match = validate_author(ck, authors_str)
            score = sim + (0.5 if author_match else 0.0)

            if score > best_score:
                best_score = score
                best_item = item

        if not best_item:
            print("NO MATCH")
            results.append((ck, "no_match", "", 0.0, ""))
            continue

        authors_str = format_authors(best_item)
        res_title = best_item.get("title", [""])[0] if best_item.get("title") else ""

        if not authors_str or not authors_str.split(" and ")[0].strip():
            print("NO-AUTHORS")
            results.append((ck, "no_authors", "", best_score, res_title[:60]))
            continue

        if not validate_author(ck, authors_str):
            # Even best match has wrong author - report for manual review
            print(f"BEST-MISMATCH ({authors_str.split(' and ')[0][:20]} | {res_title[:40]})")
            results.append((ck, "best_mismatch", authors_str, best_score, res_title[:60]))
            continue

        n = len(authors_str.split(" and "))
        sim = word_overlap(title, res_title) if len(title.split()) >= 3 else -1
        print(f"OK ({n} auth, sim={sim:.0%}, {authors_str.split(' and ')[0][:20]})")
        results.append((ck, "ok", authors_str, best_score, res_title[:80]))

    ok = sum(1 for r in results if r[1] == "ok")
    mismatch = sum(1 for r in results if r[1] == "best_mismatch")
    not_found = sum(1 for r in results if r[1] in ("not_found", "no_match"))
    other = sum(1 for r in results if r[1] not in ("ok", "best_mismatch", "not_found", "no_match"))
    print(f"\nOK: {ok}, Best-mismatch: {mismatch}, Not found: {not_found}, Other: {other}")

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
        BIB_PATH.write_text(bib_text, encoding="utf-8")
        print(f"Applied {applied} updates")
    elif not args.apply:
        print("Dry run. Use --apply to update bib.")


if __name__ == "__main__":
    main()
