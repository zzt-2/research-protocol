#!/usr/bin/env python3
"""
Batch enrich bib entries with complete author lists and abstracts.

Uses Semantic Scholar API (primary) + Crossref API (fallback).
Skips entries that already have complete author lists.

Usage:
  python tools/bib_enrich.py                    # Dry run, show what needs updating
  python tools/bib_enrich.py --apply            # Actually update the bib file
  python tools/bib_enrich.py --apply --force    # Update ALL entries (even complete ones)
"""

import re
import json
import time
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("requests not found. Install: pip install requests")
    sys.exit(1)

BIB_PATH = Path("毕设/写作材料/references.bib")
REPORT_PATH = Path(".sessions/2026-05-31-thesis-writing-prep/S003-author-abstract-audit.md")

SS_FIELDS = "authors,title,abstract,year,venue,externalIds,publicationVenue"
SS_RATE_LIMIT = 0.15  # seconds between requests (Semantic Scholar allows ~100/5min)
CR_RATE_LIMIT = 0.1   # Crossref is more generous

session = requests.Session()
session.headers.update({"User-Agent": "bib-enrich/1.0 (research-protocol)"})


def parse_bib(path: Path) -> list[dict]:
    """Parse bib file into list of entry dicts preserving order and raw text."""
    text = path.read_text(encoding="utf-8")
    entries = []
    # Match each bib entry
    for m in re.finditer(r"(@\w+\{.+?)(?=\n@|\Z)", text, re.DOTALL):
        raw = m.group(1).strip()
        # Extract citekey
        km = re.match(r"@\w+\{([^,]+),", raw)
        if not km:
            continue
        citekey = km.group(1)
        # Extract entry type
        tm = re.match(r"(@\w+)\{", raw)
        entry_type = tm.group(1) if tm else "@misc"
        # Extract fields
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{([^}]*)\}", raw):
            fields[fm.group(1).lower()] = fm.group(2)
        entries.append({
            "citekey": citekey,
            "type": entry_type,
            "raw": raw,
            "fields": fields,
        })
    return entries


def has_incomplete_authors(entry: dict) -> bool:
    """Check if author field has 'others' or is empty."""
    authors = entry["fields"].get("author", "")
    return "others" in authors.lower() or not authors.strip()


def lookup_ss_by_doi(doi: str) -> dict | None:
    """Lookup paper by DOI on Semantic Scholar."""
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
        r = session.get(url, params={"fields": SS_FIELDS}, timeout=15)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def lookup_ss_by_title(title: str) -> dict | None:
    """Search paper by title on Semantic Scholar."""
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        r = session.get(url, params={"query": title, "limit": 5, "fields": SS_FIELDS}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            results = data.get("data", [])
            if results:
                # Pick the result with highest title word overlap (>= 40%)
                best_res, best_sim = None, 0.0
                for res in results:
                    res_title = (res.get("title") or "")
                    sim = title_word_overlap(title, res_title)
                    if sim > best_sim:
                        best_sim = sim
                        best_res = res
                if best_sim >= 0.4:
                    return best_res
                # No good match — return None instead of wrong paper
    except Exception:
        pass
    return None


def lookup_cr_by_doi(doi: str) -> dict | None:
    """Lookup paper by DOI on Crossref."""
    try:
        url = f"https://api.crossref.org/works/{doi}"
        r = session.get(url, timeout=15)
        if r.status_code == 200:
            msg = r.json().get("message", {})
            authors = msg.get("author", [])
            abstract = msg.get("abstract", "").replace("<jats:p>", "").replace("</jats:p>", "").replace("<jats:title>...</jats:title>", "").strip()
            return {
                "authors": [{"name": f"{a.get('given', '')} {a.get('family', '')}".strip()} for a in authors],
                "title": msg.get("title", [""])[0] if msg.get("title") else "",
                "abstract": abstract[:500] if abstract else "",
                "year": msg.get("published-print", msg.get("published-online", {})).get("date-parts", [[None]])[0][0],
                "venue": msg.get("container-title", [""])[0] if msg.get("container-title") else "",
                "externalIds": {"DOI": doi},
            }
    except Exception:
        pass
    return None


def lookup_cr_by_title(title: str) -> dict | None:
    """Search paper by title on Crossref."""
    try:
        url = "https://api.crossref.org/works"
        r = session.get(url, params={"query.title": title, "rows": 3}, timeout=15)
        if r.status_code == 200:
            items = r.json().get("message", {}).get("items", [])
            if items:
                item = items[0]
                authors = item.get("author", [])
                return {
                    "authors": [{"name": f"{a.get('given', '')} {a.get('family', '')}".strip()} for a in authors],
                    "title": item.get("title", [""])[0] if item.get("title") else "",
                    "abstract": "",
                    "year": item.get("published-print", item.get("published-online", {})).get("date-parts", [[None]])[0][0],
                    "venue": item.get("container-title", [""])[0] if item.get("container-title") else "",
                    "externalIds": {"DOI": item.get("DOI", "")},
                }
    except Exception:
        pass
    return None


def format_authors_ss(authors: list[dict]) -> str:
    """Format Semantic Scholar author list for bib."""
    parts = []
    for a in authors:
        name = a.get("name", "")
        if name:
            parts.append(name)
    return " and ".join(parts)


def format_authors_cr(authors: list[dict]) -> str:
    """Format Crossref author list for bib."""
    return " and ".join(a["name"] for a in authors if a.get("name"))


def build_updated_raw(entry: dict, authors_str: str, abstract: str, doi: str = "") -> str:
    """Build updated bib entry raw text."""
    raw = entry["raw"]
    # Update author field
    old_author = entry["fields"].get("author", "")
    if old_author:
        raw = re.sub(r"(author\s*=\s*\{)[^}]*(\})", rf"\g<1>{authors_str}\2", raw)
    else:
        # Insert author field after citekey line
        raw = re.sub(r"(@\w+\{[^,]+,)", rf"\1\n  author = {{{authors_str}}},", raw)

    # Add/update abstract as comment (don't put in bib, just note it)
    # We'll store abstracts in a separate report file

    # Add/update DOI
    if doi and "doi" not in entry["fields"]:
        raw = raw.rstrip().rstrip("}").rstrip().rstrip(",")
        raw += f",\n  doi = {{{doi}}},\n}}"

    return raw


def title_word_overlap(t1: str, t2: str) -> float:
    """Compute word overlap ratio between two titles (words >= 3 chars)."""
    w1 = set(re.findall(r'\b\w{3,}\b', t1.lower()))
    w2 = set(re.findall(r'\b\w{3,}\b', t2.lower()))
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / min(len(w1), len(w2))


def normalize_name(s: str) -> str:
    """Normalize name for fuzzy matching: lowercase, remove diacritics, hyphens."""
    import unicodedata
    s = s.lower()
    # Remove diacritics: Brandão → brandao
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    # Remove hyphens, spaces, dots
    s = s.replace('-', '').replace(' ', '').replace('.', '')
    return s


def validate_author_match(citekey: str, authors_str: str) -> bool:
    """Verify first author surname matches citekey prefix."""
    km = re.match(r'([a-z]+)', citekey)
    if not km:
        return True  # can't validate, accept
    key_surname = normalize_name(km.group(1))
    first_author = authors_str.split(" and ")[0].strip()
    if "," in first_author:
        first_surname = normalize_name(first_author.split(",")[0].strip())
    else:
        parts = first_author.split()
        first_surname = normalize_name(parts[-1]) if parts else ""
    return key_surname in first_surname or first_surname in key_surname


def is_placeholder_doi(doi: str) -> bool:
    """Check if DOI looks fabricated (sequential digits, too short, etc)."""
    if not doi:
        return True
    # DOIs like 10.1117/12.3012345 with sequential digits are suspicious
    digits = re.sub(r'[^0-9]', '', doi)
    if len(digits) < 6:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Enrich bib entries with complete authors and abstracts")
    parser.add_argument("--apply", action="store_true", help="Actually update the bib file (default: dry run)")
    parser.add_argument("--force", action="store_true", help="Process all entries, even those with complete authors")
    parser.add_argument("--limit", type=int, default=0, help="Max entries to process (0=all)")
    args = parser.parse_args()

    if not BIB_PATH.exists():
        print(f"Error: {BIB_PATH} not found")
        sys.exit(1)

    entries = parse_bib(BIB_PATH)
    print(f"Total bib entries: {len(entries)}")

    # Filter entries that need updating
    if args.force:
        targets = entries
    else:
        targets = [e for e in entries if has_incomplete_authors(e)]
    print(f"Entries needing author update: {len(targets)}")

    if args.limit > 0:
        targets = targets[:args.limit]
        print(f"Processing limit: {args.limit}")

    # Lookup and collect results
    results = []  # list of (citekey, status, authors_str, abstract, doi, source)
    updated_count = 0
    failed_count = 0

    def validate_result(res, src, citekey, title):
        """Validate a lookup result: extract authors, verify match. Returns (authors_str, abstract, doi) or None."""
        if src.startswith("ss"):
            authors_str = format_authors_ss(res.get("authors", []))
        else:
            authors_str = format_authors_cr(res.get("authors", []))
        if not validate_author_match(citekey, authors_str):
            return None
        if not authors_str or "others" in authors_str:
            return "partial", authors_str or "", res.get("abstract", "") or "", (res.get("externalIds") or {}).get("DOI", "") or ""
        return "ok", authors_str, res.get("abstract", "") or "", (res.get("externalIds") or {}).get("DOI", "") or ""

    for i, entry in enumerate(targets):
        citekey = entry["citekey"]
        title = entry["fields"].get("title", "").replace("{", "").replace("}", "")
        doi = entry["fields"].get("doi", "")
        is_chinese = entry["fields"].get("language", "") == "chinese"

        print(f"[{i+1}/{len(targets)}] {citekey}: ", end="", flush=True)

        # Skip Chinese papers (unlikely in SS/CR)
        if is_chinese:
            print("SKIP (Chinese)")
            results.append((citekey, "skip_chinese", "", "", doi, ""))
            continue

        found = False  # set True when a valid match is confirmed

        # === Phase 1: Try DOI lookup ===
        if doi:
            print(f"DOI:{doi[:30]}... ", end="", flush=True)
            result = None
            source = ""
            result = lookup_ss_by_doi(doi)
            if result:
                source = "ss_doi"
            if not result:
                result = lookup_cr_by_doi(doi)
                if result:
                    source = "cr_doi"
            if result:
                # Verify title similarity for non-abbreviated titles
                if len(title.split()) >= 4:
                    res_title = result.get("title", "") or ""
                    sim = title_word_overlap(title, res_title)
                    if sim < 0.25:
                        print(f"title-mismatch({sim:.0%})→", end="", flush=True)
                        result = None
                if result:
                    v = validate_result(result, source, citekey, title)
                    if v and v[0] == "ok":
                        _, authors_str, abstract, new_doi = v
                        print(f"OK ({source}, {len(authors_str.split(' and '))} authors)")
                        results.append((citekey, "updated", authors_str, abstract, new_doi or doi, source))
                        updated_count += 1
                        found = True
                    elif v and v[0] == "partial":
                        _, authors_str, abstract, new_doi = v
                        print(f"PARTIAL-DOI ({source})→", end="", flush=True)
            time.sleep(SS_RATE_LIMIT)

        # === Phase 2: Try title search ===
        if not found and title and len(title.split()) >= 3:
            print(f"title... ", end="", flush=True)
            result = None
            source = ""
            result = lookup_ss_by_title(title)
            if result:
                source = "ss_title"
            if not result:
                time.sleep(SS_RATE_LIMIT)
                result = lookup_cr_by_title(title)
                if result:
                    source = "cr_title"
            if result:
                v = validate_result(result, source, citekey, title)
                if v and v[0] == "ok":
                    _, authors_str, abstract, new_doi = v
                    print(f"OK ({source}, {len(authors_str.split(' and '))} authors)")
                    results.append((citekey, "updated", authors_str, abstract, new_doi or doi, source))
                    updated_count += 1
                    found = True
                elif v and v[0] == "partial":
                    print(f"PARTIAL ({source})")
                    _, authors_str, abstract, new_doi = v
                    results.append((citekey, "partial", authors_str, abstract, new_doi or doi, source))
                    failed_count += 1
                    found = True
            if not result:
                time.sleep(CR_RATE_LIMIT)

        if not found:
            print("NOT FOUND")
            results.append((citekey, "not_found", "", "", doi, ""))
            failed_count += 1

    print(f"\n{'='*60}")
    print(f"Updated: {updated_count}, Partial: {sum(1 for r in results if r[1]=='partial')}, "
          f"Skip: {sum(1 for r in results if r[1]=='skip_chinese')}, Not found: {sum(1 for r in results if r[1]=='not_found')}")

    # Generate report
    report_lines = [
        f"# S003 作者+摘要补全审计",
        f"",
        f"> {datetime.now().strftime('%Y-%m-%d')} | 自动化审计",
        f"> 总条目: {len(entries)}, 需更新: {len(targets)}, 成功: {updated_count}",
        f"",
        f"## 结果汇总",
        f"",
        f"| citekey | 状态 | 作者数 | 来源 | 摘要 |",
        f"|---------|------|--------|------|------|",
    ]

    for citekey, status, authors_str, abstract, doi, source in results:
        n_authors = len(authors_str.split(" and ")) if authors_str else "?"
        has_abstract = "✓" if abstract else "✗"
        if status == "updated":
            report_lines.append(f"| {citekey} | ✅ 更新 | {n_authors} | {source} | {has_abstract} |")
        elif status == "partial":
            report_lines.append(f"| {citekey} | ⚠️ 部分 | {n_authors} | {source} | {has_abstract} |")
        elif status == "skip_chinese":
            report_lines.append(f"| {citekey} | ⏭️ 中文跳过 | — | — | — |")
        else:
            report_lines.append(f"| {citekey} | ❌ 未找到 | — | — | — |")

    # Add abstracts section
    updated_results = [r for r in results if r[1] in ("updated", "partial") and r[3]]
    if updated_results:
        report_lines.extend(["", "## 摘要（按 citekey）", ""])
        for citekey, _, _, abstract, _, _ in updated_results:
            report_lines.append(f"### {citekey}")
            report_lines.append(f"")
            report_lines.append(abstract[:400])
            report_lines.append(f"")

    # Write report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nReport: {REPORT_PATH}")

    # Apply updates to bib file
    if args.apply and updated_count > 0:
        # Re-read and apply
        bib_text = BIB_PATH.read_text(encoding="utf-8")
        updates = [r for r in results if r[1] == "updated"]

        for citekey, status, authors_str, abstract, doi, source in updates:
            # Find and replace author field in bib
            pattern = rf"(@\w+\{{{citekey},.*?author\s*=\s*\{{)([^}}]*)(\}})"
            def replacer(m):
                return m.group(1) + authors_str + m.group(3)
            bib_text = re.sub(pattern, replacer, bib_text, count=1, flags=re.DOTALL)

        BIB_PATH.write_text(bib_text, encoding="utf-8")
        print(f"Updated {len(updates)} author fields in {BIB_PATH}")
    elif not args.apply:
        print(f"\nDry run complete. Use --apply to update the bib file.")


if __name__ == "__main__":
    main()
