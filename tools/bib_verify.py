#!/usr/bin/env python3
"""
Batch verify bib entries against Semantic Scholar API.
For each entry with missing/wrong metadata, search by title and report correct data.

Usage:
  python tools/bib_verify.py                    # Dry run, show report
  python tools/bib_verify.py --apply            # Update bib file with correct metadata
  python tools/bib_verify.py --citekeys a,b     # Only process specific citekeys
"""

import re
import json
import time
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("requests not found. Install: pip install requests")
    sys.exit(1)

# Load .env
def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ[k.strip()] = v.strip()

load_env()

BIB_PATH = Path("毕设/写作材料/references.bib")
S2_API_KEY = os.getenv("S2_API_KEY", "")
SS_FIELDS = "title,authors,year,venue,externalIds,journal,publicationVenue"
SS_RATE_LIMIT = 0.2  # seconds between requests

session = requests.Session()
if S2_API_KEY:
    session.headers.update({"x-api-key": S2_API_KEY})
session.headers.update({"User-Agent": "bib-verify/1.0 (research-protocol)"})


def parse_bib(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    entries = []
    for m in re.finditer(r"(@\w+\{.+?)(?=\n@|\Z)", text, re.DOTALL):
        raw = m.group(1).strip()
        km = re.match(r"@\w+\{([^,]+),", raw)
        if not km:
            continue
        citekey = km.group(1)
        # Skip commented entries
        if raw.startswith("%"):
            continue
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{([^}]*)\}", raw):
            fields[fm.group(1).lower()] = fm.group(2)
        entries.append({"citekey": citekey, "raw": raw, "fields": fields})
    return entries


def get_cited_keys(report_path: Path) -> set[str]:
    text = report_path.read_text(encoding="utf-8")
    keys = set(re.findall(r'@([a-zA-Z0-9_]+)', text))
    return keys


def title_similarity(t1: str, t2: str) -> float:
    w1 = set(re.findall(r'\b\w{3,}\b', t1.lower()))
    w2 = set(re.findall(r'\b\w{3,}\b', t2.lower()))
    if not w1 or not w2:
        return 0.0
    return len(w1 & w2) / min(len(w1), len(w2))


def search_ss_by_title(title: str) -> dict | None:
    try:
        r = session.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            params={"query": title, "limit": 5, "fields": SS_FIELDS},
            timeout=15,
        )
        if r.status_code == 200:
            results = r.json().get("data", [])
            if not results:
                return None
            # Pick best match
            best, best_sim = None, 0.0
            for res in results:
                res_title = res.get("title") or ""
                sim = title_similarity(title, res_title)
                if sim > best_sim:
                    best_sim = sim
                    best = res
            if best_sim >= 0.35:
                return best
    except Exception as e:
        print(f"  API error: {e}", file=sys.stderr)
    return None


def search_ss_by_doi(doi: str) -> dict | None:
    try:
        r = session.get(
            f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}",
            params={"fields": SS_FIELDS},
            timeout=15,
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def extract_metadata(ss_result: dict) -> dict:
    """Extract structured metadata from SS result."""
    meta = {}
    ids = ss_result.get("externalIds") or {}
    meta["doi"] = ids.get("DOI", "")
    meta["title"] = ss_result.get("title") or ""
    meta["year"] = ss_result.get("year")

    # Authors
    authors = ss_result.get("authors") or []
    meta["authors"] = [a.get("name", "") for a in authors if a.get("name")]

    # Journal info
    j = ss_result.get("journal") or {}
    meta["journal_name"] = j.get("name", "")
    meta["volume"] = j.get("volume", "")
    meta["pages"] = j.get("pages", "")

    # Publication venue fallback
    pv = ss_result.get("publicationVenue") or {}
    if not meta["journal_name"] and pv:
        meta["journal_name"] = pv.get("name", "")

    meta["venue"] = ss_result.get("venue") or ""

    return meta


def needs_update(entry: dict) -> bool:
    """Check if entry has missing fields."""
    f = entry["fields"]
    has_vol = "volume" in f
    has_pages = "pages" in f
    has_doi = "doi" in f
    author = f.get("author", "")
    # Skip books (andrews2005, gardner1979) from vol/pages check
    entry_type = entry["raw"].split("{")[0] if "{" in entry["raw"] else ""
    is_book = entry_type == "@book" or entry_type == "@misc"

    issues = []
    if not is_book:
        if not has_vol:
            issues.append("no-vol")
        if not has_pages:
            issues.append("no-pages")
    if not has_doi and not is_book:
        issues.append("no-doi")
    if "others" in author.lower():
        issues.append("author-incomplete")
    return len(issues) > 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--citekeys", type=str, default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--output", type=str, default="")
    args = parser.parse_args()

    if not BIB_PATH.exists():
        print(f"Error: {BIB_PATH} not found")
        sys.exit(1)

    # Parse bib
    entries = parse_bib(BIB_PATH)
    entry_map = {e["citekey"]: e for e in entries}

    # Get cited keys from report
    cited_keys = get_cited_keys(Path("毕设/开题报告/kaiti-report.md"))
    print(f"Bib entries: {len(entries)}, Cited in report: {len(cited_keys)}")

    # Filter to cited entries that need update
    targets = []
    for ck in sorted(cited_keys):
        if ck not in entry_map:
            print(f"  WARNING: {ck} cited but not in bib!")
            continue
        e = entry_map[ck]
        if needs_update(e):
            targets.append(e)

    print(f"Entries needing metadata fix: {len(targets)}")

    if args.citekeys:
        filter_keys = set(args.citekeys.split(","))
        targets = [e for e in targets if e["citekey"] in filter_keys]
        print(f"Filtered to: {len(targets)}")

    if args.limit > 0:
        targets = targets[:args.limit]
        print(f"Limit: {args.limit}")

    # Process
    results = []
    for i, entry in enumerate(targets):
        ck = entry["citekey"]
        title = entry["fields"].get("title", "").replace("{", "").replace("}", "")
        old_doi = entry["fields"].get("doi", "")
        print(f"[{i+1}/{len(targets)}] {ck}: ", end="", flush=True)

        # Try DOI first (if exists and not obviously fake)
        ss_result = None
        source = ""
        if old_doi:
            ss_result = search_ss_by_doi(old_doi)
            if ss_result:
                source = "ss_doi"
                # Verify title match
                res_title = ss_result.get("title") or ""
                sim = title_similarity(title, res_title)
                if sim < 0.2:
                    print(f"DOI-mismatch({sim:.0%})→", end="", flush=True)
                    ss_result = None
            time.sleep(SS_RATE_LIMIT)

        # Fallback to title search
        if not ss_result and len(title.split()) >= 3:
            ss_result = search_ss_by_title(title)
            if ss_result:
                source = "ss_title"
            time.sleep(SS_RATE_LIMIT)

        if ss_result:
            meta = extract_metadata(ss_result)
            meta["source"] = source
            sim = title_similarity(title, meta["title"])
            n_authors = len(meta["authors"])
            print(f"OK ({source}, sim={sim:.0%}, {n_authors} authors, DOI={meta['doi'][:30] if meta['doi'] else 'none'})")
            results.append({"citekey": ck, "status": "found", "meta": meta, "old_doi": old_doi})
        else:
            print("NOT FOUND")
            results.append({"citekey": ck, "status": "not_found", "meta": {}, "old_doi": old_doi})

    # Generate report
    report = []
    report.append(f"# Bib 元数据验证报告")
    report.append(f""
)
    report.append(f"> {datetime.now().strftime('%Y-%m-%d %H:%M')} | Semantic Scholar API 批量验证")
    report.append(f"> 目标: {len(targets)} 条 | 找到: {sum(1 for r in results if r['status']=='found')} | 未找到: {sum(1 for r in results if r['status']=='not_found')}")
    report.append(f""
)

    for r in results:
        ck = r["citekey"]
        if r["status"] == "not_found":
            report.append(f"## {ck} — NOT FOUND")
            report.append(f"")
            report.append(f"- Old DOI: `{r['old_doi'] or 'none'}`")
            report.append(f"- Action: manual lookup needed")
            report.append(f"")
            continue

        meta = r["meta"]
        report.append(f"## {ck}")
        report.append(f"")
        report.append(f"| Field | Old (bib) | New (SS) |")
        report.append(f"|-------|-----------|----------|")
        report.append(f"| Title | {entry_map[ck]['fields'].get('title','')[:50]} | {meta['title'][:50]} |")
        report.append(f"| DOI | `{r['old_doi'] or 'none'}` | `{meta['doi'] or 'none'}` |")
        report.append(f"| Authors | {entry_map[ck]['fields'].get('author','')[:40]} | {' and '.join(meta['authors'][:3])[:40]} |")
        report.append(f"| Journal | {entry_map[ck]['fields'].get('journal','')[:40]} | {meta.get('journal_name','')[:40]} |")
        report.append(f"| Volume | {entry_map[ck]['fields'].get('volume','—')} | {meta.get('volume','—')} |")
        report.append(f"| Pages | {entry_map[ck]['fields'].get('pages','—')} | {meta.get('pages','—')} |")
        report.append(f"| Year | {entry_map[ck]['fields'].get('year','—')} | {meta.get('year','—')} |")
        report.append(f"| Source | | {meta['source']} |")
        report.append(f"")

    output_path = args.output or f".sessions/2026-06-04-advisor-review-revision/bib-verify-report.md"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(report), encoding="utf-8")
    print(f"\nReport: {output_path}")


if __name__ == "__main__":
    main()
