#!/usr/bin/env python
"""Deterministic recompute of GW Step 1 search facts from raw JSON.

Phase A1 (search facts) + Phase A2 (title-abstract identity audit) share the
same raw-data pass, so this single script computes both and prints a compact
machine-readable summary plus the raw numbers. No network access.

Run: python tools/amc_step1_recompute.py
"""
import json
import os
import hashlib
from collections import defaultdict, Counter

ARCH = "search-archive/2026-08-02"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(s):
    if not s:
        return ""
    return " ".join(s.lower().split())


def main():
    # Alias collision queries (Phase A3 bounded repair) are tracked separately in
    # the receipt's alias_collision_repair block; exclude them from the primary
    # "original Step 1 search contract" recompute so search_facts stays at the
    # 17 original queries. The 4 alias slugs (each stored twice: slug + named):
    ALIAS_FILES = {
        "coherent-fso-acm-modcod-satellite.json",
        "2026-08-02-coherent-fso-acm-modcod-satellite-1.json",
        "optical-feeder-link-variable-rate-fec.json",
        "optical-feeder-link-variable-rate-fec-adaptive-coding.json",
        "fso-rate-compatible-ldpc-puncturing.json",
        "free-space-optical-rate-compatible-ldpc-puncturing-adaptive.json",
        "satellite-optical-dvbs2x-acm.json",
        "satellite-optical-dvb-s2x-acm.json",
    }
    all_files = sorted(
        f for f in os.listdir(ARCH)
        if f.endswith(".json") and not f.startswith("_") and f not in ALIAS_FILES
    )

    # ---- Phase A1: per-file facts ----
    per_file = []
    for fn in all_files:
        path = os.path.join(ARCH, fn)
        size = os.path.getsize(path)
        sha = sha256_file(path)
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            per_file.append({"file": fn, "size": size, "sha256": sha,
                             "error": f"PARSE_FAIL: {e}"})
            continue
        is_cnki = fn.startswith("cnki-")
        query = d.get("query", "")
        ts = d.get("timestamp", "")
        requested_sources = d.get("sources", [])
        results = d.get("results", [])
        n_results = len(results)
        zero_byte = (size == 0)
        # result-bearing sources (per result actual source_api / source)
        bearing = set()
        for r in results:
            src = r.get("source_api") or r.get("source")
            if src:
                bearing.add(src)
        per_file.append({
            "file": fn, "size": size, "sha256": sha, "zero_byte": zero_byte,
            "is_cnki": is_cnki, "query": query, "timestamp": ts,
            "requested_sources": requested_sources, "n_results": n_results,
            "result_bearing_sources": sorted(bearing),
        })

    # ---- unique queries (dedupe by query string) ----
    by_query = defaultdict(list)
    for p in per_file:
        if "error" not in p:
            by_query[p["query"]].append(p["file"])
    unique_queries = list(by_query.keys())
    nonzero_queries = [q for q, fs in by_query.items()
                       if sum(p["n_results"]
                              for p in per_file if p["file"] in fs) > 0]

    # ---- requested source union vs result-bearing source union ----
    requested_union = set()
    for p in per_file:
        requested_union.update(p.get("requested_sources", []))
    bearing_union = set()
    for p in per_file:
        bearing_union.update(p.get("result_bearing_sources", []))

    # ---- candidates: use _alldigest as canonical unique list ----
    digest = json.load(open(os.path.join(ARCH, "_alldigest.json"), encoding="utf-8"))
    n_unique = len(digest)

    # ---- publication status (from digest 'pub' field) ----
    pub_counter = Counter(item.get("pub", "unknown") or "unknown" for item in digest)

    # ---- priority distribution (parse R001 triage by reading the file) ----
    # We recompute priority by scanning R001 for "L### | pri" rows.
    pri_dist = Counter()
    r1path = ".sessions/2026-08-02-fso-amc-groundwork/R001-amc-step1-landscape.md"
    r1text = open(r1path, encoding="utf-8").read()
    import re
    # rows like "| L018 | 必读 |" or "| L018 | 建议读 |" etc.
    for m in re.finditer(r"\|\s*(L\d{3})\s*\|\s*(必读|建议读|待确认|备选|排除)\s*\|", r1text):
        pri_dist[m.group(2)] += 1

    # ---- 0-byte / empty result files ----
    empty_files = [p["file"] for p in per_file
                   if p.get("zero_byte") or p.get("n_results") == 0]

    # ---- raw file sha256 map ----
    raw_sha = {p["file"]: p["sha256"] for p in per_file if "error" not in p}

    # =====================================================================
    # Phase A2: title-abstract identity audit
    # =====================================================================
    # Group digest items by normalized abstract.
    by_abs = defaultdict(list)
    for item in digest:
        na = norm(item.get("abstract", ""))
        by_abs[na].append(item)

    dup_groups = []
    for na, items in by_abs.items():
        if len(items) > 1:
            titles = [it.get("title", "") for it in items]
            # only count as "shared abstract" if there is a non-trivial abstract
            if len(na) >= 40:
                dup_groups.append({
                    "normalized_abstract_len": len(na),
                    "normalized_abstract_preview": na[:160],
                    "items": [
                        {"L": it.get("L"), "title": it.get("title"),
                         "year": it.get("year"), "venue": it.get("venue"),
                         "doi": it.get("doi"), "pub": it.get("pub")}
                        for it in items
                    ],
                    "same_title": len(set(titles)) == 1,
                })
    dup_groups.sort(key=lambda g: -len(g["items"]))

    # Items with empty abstract (separate from shared-abstract dup)
    empty_abstract_items = [it.get("L") for it in digest
                            if not norm(it.get("abstract", ""))]

    # ============ print summary ============
    print("=" * 70)
    print("PHASE A1 — SEARCH FACTS (deterministic recompute)")
    print("=" * 70)
    print(f"raw JSON files (non-_prefix): {len(all_files)}")
    print(f"unique queries (by query string): {len(unique_queries)}")
    print(f"non-zero-result queries: {len(nonzero_queries)}")
    print(f"zero-result / 0-byte files: {empty_files}")
    print(f"requested source union: {sorted(requested_union)}")
    print(f"result-bearing source union: {sorted(bearing_union)}")
    print(f"unique candidates (_alldigest): {n_unique}")
    print(f"publication status: {dict(pub_counter)}")
    print(f"priority distribution (from R001 triage rows): {dict(pri_dist)}")
    print()
    print("--- duplicate-query file pairs (same query, 2 filenames) ---")
    dup_pair_count = 0
    for q, fs in by_query.items():
        if len(fs) > 1:
            dup_pair_count += 1
    print(f"duplicate-query groups (query ran twice, 2 files each): {dup_pair_count}")
    print(f"=> {len(all_files)} files = {len(unique_queries)} unique queries "
          f"(each query stored twice: slug-archived + named-output)")
    print()
    print("=" * 70)
    print("PHASE A2 — TITLE-ABSTRACT IDENTITY AUDIT")
    print("=" * 70)
    print(f"shared-abstract groups (norm abstract len>=40, >1 item): {len(dup_groups)}")
    total_in_dup = sum(len(g["items"]) for g in dup_groups)
    print(f"total items in shared-abstract groups: {total_in_dup}")
    print(f"items with empty abstract: {len(empty_abstract_items)}")
    print()
    for i, g in enumerate(dup_groups):
        print(f"--- dup group {i+1} ({len(g['items'])} items, "
              f"abs_len={g['normalized_abstract_len']}, same_title={g['same_title']})")
        print(f"    abstract preview: {g['normalized_abstract_preview'][:120]}...")
        for it in g["items"]:
            print(f"    {it['L']}: {it['title'][:70]}  | {it.get('year')} | "
                  f"{it.get('venue','')[:30]} | doi={it.get('doi')}")
        print()

    # ============ write machine-readable json for receipt ============
    out = {
        "phase_a1": {
            "raw_json_files": len(all_files),
            "unique_queries": len(unique_queries),
            "nonzero_result_queries": len(nonzero_queries),
            "duplicate_query_groups": dup_pair_count,
            "requested_source_union": sorted(requested_union),
            "result_bearing_source_union": sorted(bearing_union),
            "unique_candidates": n_unique,
            "publication_status": dict(pub_counter),
            "priority_distribution": dict(pri_dist),
            "empty_or_zero_result_files": empty_files,
            "per_file": per_file,
            "raw_sha256": raw_sha,
        },
        "phase_a2": {
            "shared_abstract_group_count": len(dup_groups),
            "total_items_in_shared_abstract_groups": total_in_dup,
            "empty_abstract_item_count": len(empty_abstract_items),
            "shared_abstract_groups": dup_groups,
        },
    }
    with open("tools/_amc_step1_recompute_out.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("wrote tools/_amc_step1_recompute_out.json")


if __name__ == "__main__":
    main()
