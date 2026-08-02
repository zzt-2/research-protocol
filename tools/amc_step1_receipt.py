#!/usr/bin/env python
"""Build the persistent _step1_receipt.json for GW Step 1 (Phase A4)."""
import json, os, hashlib, datetime

ARCH = "search-archive/2026-08-02"


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(8192), b""):
            h.update(c)
    return h.hexdigest()


def main():
    rc = json.load(open("tools/_amc_step1_recompute_out.json", encoding="utf-8"))
    a1, a2 = rc["phase_a1"], rc["phase_a2"]
    dig = {it["L"]: it for it in json.load(open(os.path.join(ARCH, "_alldigest.json"), encoding="utf-8"))}

    shortlist = ["L018", "L096", "L126", "L073", "L023", "L075", "L020",
                 "L124", "L165", "L146", "L050", "L206"]

    def provenance(L):
        it = dig.get(L, {})
        return {
            "L": L, "title": it.get("title"), "year": it.get("year"),
            "venue": it.get("venue"), "doi": it.get("doi") or None,
            "pub": it.get("pub"), "source_set": it.get("source_set"),
            "url_or_doi": it.get("doi") or "(no DOI; search hit only)",
        }

    alias = [
        {"query": "coherent FSO ACM ModCod satellite",
         "file": "coherent-fso-acm-modcod-satellite.json", "n_results": 9},
        {"query": "optical feeder link variable-rate FEC adaptive coding",
         "file": "optical-feeder-link-variable-rate-fec.json", "n_results": 7},
        {"query": "free-space optical rate-compatible LDPC puncturing adaptive",
         "file": "fso-rate-compatible-ldpc-puncturing.json", "n_results": 1},
        {"query": "satellite optical DVB-S2X ACM",
         "file": "satellite-optical-dvbs2x-acm.json", "n_results": 15},
    ]
    for q in alias:
        p = os.path.join(ARCH, q["file"])
        q["sha256"] = sha256_file(p)
        q["size_bytes"] = os.path.getsize(p)
        q["direct_competitor"] = False

    receipt = {
        "schema": "amc-gw-step1-receipt/v1",
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "topic": ".sessions/2026-08-02-fso-amc-groundwork/",
        "purpose": ("Persistent provenance receipt for GW Step 1 search contract, hashes, "
                    "and shortlist. Force-added to git so a clean clone can reconstruct the "
                    "search contract even though raw JSON is gitignored."),
        "search_facts": {
            "raw_json_files": a1["raw_json_files"],
            "unique_queries": a1["unique_queries"],
            "nonzero_result_queries": a1["nonzero_result_queries"],
            "duplicate_query_groups": a1["duplicate_query_groups"],
            "duplicate_query_note": ("32 raw files = 17 unique queries; each query stored "
                                      "twice by the wrapper (slug-archived + named-output JSON, "
                                      "identical results). 16 of 17 queries returned >=1 result."),
            "requested_source_union": a1["requested_source_union"],
            "result_bearing_source_union_note": ("Result-level source_api tags observed only for: "
                "openalex, serpapi_scholar, cnki (plus 2 results tagged openalex+openalex). "
                "exa contributed candidates (171 digest items carry exa in source_set) but its "
                "results were not distinctly tagged at result level (provenance artifact). "
                "arxiv was requested twice (mcs-fer-goodput query) and returned 0 both times."),
            "unique_candidates": a1["unique_candidates"],
            "publication_status": a1["publication_status"],
            "published_fraction": round(a1["publication_status"].get("published", 0) / a1["unique_candidates"], 4),
            "priority_distribution": a1["priority_distribution"],
            "empty_or_zero_result_files": a1["empty_or_zero_result_files"],
            "zero_byte_files_in_archive": ["_cnki-r2-linkadapt.txt (auxiliary .txt, NOT a CNKI .json)"],
            "published_miscount_history": ("_manifest.json pub_status.published=153 is a duplicate-counted "
                "figure (merges r1-digest re-runs); the unique-_alldigest truth is 115 published / 209 = 55.0%."),
            "sources_miscount_history": ("R001/S001/V001 claimed 5 sources (openalex/exa/arxiv/serpapi/cnki) "
                "but conflated requested vs result-bearing. Correct: 4 requested API sources (arxiv returned 0) "
                "+ cnki = 4 distinct data channels producing results."),
        },
        "duplicate_abstract_groups": {
            "group_count": a2["shared_abstract_group_count"],
            "total_items": a2["total_items_in_shared_abstract_groups"],
            "mechanism": ("Exa/SerpAPI abstract-scrape corruption: a small number of generic survey abstracts "
                "(6G-roadmap, OWC-survey, SATCOM-survey, ISAC-survey, FSO-enabling-tech-survey, IRS-survey) "
                "were repeatedly injected across many items with DIFFERENT titles. The abstract is NOT "
                "trustworthy for these items; title+DOI must be used for identity. Affects shortlist/flagged "
                "items L124, L020, L038, L090."),
            "groups": a2["shared_abstract_groups"],
        },
        "alias_collision_repair": {
            "queries": alias,
            "total_alias_hits": sum(q["n_results"] for q in alias),
            "direct_competitors_found": 0,
            "coverage_caveat": ("Exa returned HTTP 402 NO_MORE_CREDITS on all 4 queries; OpenAlex returned 0 "
                "hits; S2 abstract-completion rate-limited. Only SerpAPI Scholar was live. A re-run after "
                "Exa top-up is advisable before declaring the gap fully closed."),
            "near_miss_to_revisit": ("L003 Softwarization/Virtualization EHF-FSO (2018) is the only hit "
                "co-locating coherent sat-ground + ACM, but it is a survey with no Gamma-Gamma channel model."),
        },
        "l124_identity_resolution": {
            "codename": "L124",
            "local_title": ("Physics-informed adaptive transmission for coherent free-space optical "
                            "communications: multi-dimensional amplitude-phase statistics"),
            "local_abstract_status": "MISMATCHED (generic 6G-roadmap text, shared with L005) - confirmed corrupt",
            "official_identity": {
                "title": ("Physics-informed adaptive transmission for coherent free-space optical "
                          "communications: multi-dimensional amplitude-phase statistics"),
                "authors": ["Shengsong Xiao", "Bei Li", "Xiuyuan Liu", "Ruiheng Zhang",
                            "Bao Zhang", "Kai Xie"],
                "year": 2026, "venue": "Optics Express", "volume": "34", "issue": "14",
                "page": "26128", "doi": "10.1364/oe.595557",
                "publisher": "Optica Publishing Group", "issn": "1094-4087",
                "url": "https://doi.org/10.1364/oe.595557",
            },
            "verification_sources": [
                "Semantic Scholar Graph API (paper/search, exact title match, with S2_API_KEY)",
                "Crossref /works/10.1364/oe.595557 (title/authors/venue/pages/abstract)",
            ],
            "real_abstract_preview": ("Coherent free-space optical (FSO) communications suffer from coupled "
                "amplitude fading and phase distortion. Conventional adaptive modulation and coding (AMC) "
                "relying solely on signal-to-noise ratio (SNR) feedback cannot capture phase dynamics, "
                "leading to error floors under strong turbulence. We propose a physics-informed AMC framework "
                "that extracts scintillation index and phase variance from pilots..."),
            "action_closure": ("(a) coherent FSO AMC with a real transmitter-side control action (modulation "
                "selection driven by multi-dimensional CSI vector [SNR, scintillation index, phase variance]). "
                "NOT AO/DSP/receiver-side-only. Does NOT explicitly name Gamma-Gamma or satellite/feeder link "
                "in abstract; full-text confirmation required in Step 2."),
            "pre_fix_status": "UNVERIFIED_BIBLIOGRAPHIC_HIT (identity resolved at bibliographic level; full-text not yet read)",
            "implication_for_candidate_map": ("L124 is a genuine coherent-FSO AMC paper with a real AMC action, "
                "so the prior claim of a 4-mechanism-distinct family F4 collapses into the MCS/power-control "
                "family - L124 is a real (coherent, phase-aware) instance of AMC, not a separate mechanism family."),
        },
        "shortlist_provenance": [provenance(L) for L in shortlist],
        "raw_file_hashes": a1["raw_sha256"],
        "replay": {
            "recompute_script": "tools/amc_step1_recompute.py (deterministic, no network)",
            "recompute_output": "tools/_amc_step1_recompute_out.json",
            "command": "python tools/amc_step1_recompute.py",
            "note": ("Receipt fields search_facts/duplicate_abstract_groups/raw_file_hashes are produced by "
                     "tools/amc_step1_recompute.py from the raw JSON in search-archive/2026-08-02/. Re-running "
                     "the script regenerates them deterministically."),
        },
    }
    out = os.path.join(ARCH, "_step1_receipt.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
    json.load(open(out, encoding="utf-8"))  # validate
    print("wrote", out, os.path.getsize(out), "bytes; json parse OK")


if __name__ == "__main__":
    main()
