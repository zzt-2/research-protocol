#!/usr/bin/env python3
"""
Batch CNKI author lookup for Chinese bib entries with 'and others'.
Uses blit --source cnki to search by title.

Usage:
  python tools/bib_cnki_authors.py                 # Dry run
  python tools/bib_cnki_authors.py --apply          # Apply changes
"""

import re
import json
import subprocess
from pathlib import Path

BIB_PATH = Path("毕设/写作材料/references.bib")

# 16 Chinese entries needing author lookup: citekey -> title
ENTRIES = {
    "caominghua2020": "Gamma-Gamma大气湍流下超奈奎斯特光通信系统性能",
    "sunjing2018": "Gamma-Gamma大气湍流下相干光通信分集接收技术",
    "lixiaoyan2017": "Gamma-Gamma大气湍流下零判决门限差分探测FSO系统误码率",
    "hanliqiang2011": "Gamma-Gamma大气湍流下自由空间光通信的性能",
    "madongtang2004": "大气激光通信中多光束传输性能分析和信道建模",
    "wuying2026": "基于DNN信道估计的自适应概率整形FSO系统",
    "xuwenjing2021": "相干光通信载波相位恢复算法研究",
    "guanhaijun2019": "基于数字相位恢复算法的QPSK自由空间相干光通信系统",
    "xiangjinsong2011": "空间相干光通信中基于DSP的多普勒频移补偿技术",
    "zhaoyun2025": "星地激光通信研究现状与前沿技术",
    "yuanrenzhi2024": "面向星地融合的激光通信：研究现状、关键技术与未来展望",
    "qiaoyuanzhe2025": "面向星地融合的光通信：激光通信终端研究进展和发展建议",
    "fuyulong2025": "非柯湍流对星地激光通信分集接收系统性能影响",
    "maning2025a": "气象数据融合的星地激光链路多物理场损耗分析",
    "caominghua2026b": "数据驱动DBLNet无线光OOFDM信号接收算法",
    "liu2025spaceLaserNetworking": "空间激光组网技术进展",
}


def cnki_search(title):
    """Search CNKI via blit and return parsed results."""
    try:
        result = subprocess.run(
            ["bash", "tools/blit", "--source", "cnki", title, "--max", "3", "--format", "json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        # Find JSON in output (skip non-JSON lines)
        lines = result.stdout.strip().split("\n")
        json_start = None
        for i, line in enumerate(lines):
            if line.startswith("{"):
                json_start = i
                break
        if json_start is not None:
            json_text = "\n".join(lines[json_start:])
            return json.loads(json_text)
    except Exception as e:
        print(f"ERR:{e}")
    return None


def to_pinyin(chinese):
    """Simple Chinese→pinyin for first-author validation via citekey prefix."""
    # Use the citekey pinyin prefix, not actual pinyin conversion.
    # Just return the raw string for comparison.
    return chinese


def citekey_first_author_pinyin(citekey):
    """Extract expected pinyin prefix from citekey like 'caominghua2020' → 'caominghua'."""
    m = re.match(r'([a-z]+)', citekey)
    return m.group(1) if m else ""


def validate_first_author(citekey, first_author_chinese, bib_text):
    """Check if CNKI's first author matches what's already in bib."""
    first_in_bib = get_bib_first_author(citekey, bib_text)
    if not first_in_bib:
        return True
    return first_author_chinese == first_in_bib


def get_bib_first_author(citekey, bib_text):
    """Get first author from bib entry."""
    pattern = rf'(@\w+\{{{citekey},.*?author\s*=\s*\{{)([^}}]*)(\}})'
    match = re.search(pattern, bib_text, re.DOTALL)
    if not match:
        return ""
    return match.group(2).split(" and ")[0].strip()


def format_chinese_authors(authors_list):
    """Format CNKI author list as BibTeX author field (Chinese names with ' and ')."""
    # Handle comma-separated string authors (some CNKI results)
    result = []
    for a in authors_list:
        if "," in a and len(authors_list) == 1:
            result = [x.strip() for x in a.split(",")]
            break
        result.append(a)
    return " and ".join(result)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    bib_text_cache = BIB_PATH.read_text(encoding="utf-8")
    bib_text = bib_text_cache

    results = {}  # citekey -> authors_str

    for i, (ck, title) in enumerate(ENTRIES.items()):
        print(f"[{i+1}/{len(ENTRIES)}] {ck}: ", end="", flush=True)

        data = cnki_search(title)
        if not data or not data.get("results"):
            print("NOT FOUND")
            continue

        # Find best match: prefer exact title match, then validate first author
        best = None
        for r in data["results"]:
            rtitle = r.get("title", "").replace("{", "").replace("}", "")
            if rtitle == title or title in rtitle or rtitle in title:
                best = r
                break
        if not best:
            best = data["results"][0]

        authors = best.get("authors", [])
        if not authors:
            print("NO AUTHORS")
            continue

        # Get first author (handle comma-separated)
        first_cn = authors[0]
        if "," in first_cn and len(authors) == 1:
            first_cn = first_cn.split(",")[0].strip()

        # Validate first author matches what's in bib
        if not validate_first_author(ck, first_cn, bib_text_cache):
            # Try remaining results
            alt_found = False
            for r in data["results"]:
                alt_authors = r.get("authors", [])
                if not alt_authors:
                    continue
                alt_first = alt_authors[0]
                if "," in alt_first and len(alt_authors) == 1:
                    alt_first = alt_first.split(",")[0].strip()
                if validate_first_author(ck, alt_first, bib_text_cache):
                    best = r
                    authors = alt_authors
                    first_cn = alt_first
                    alt_found = True
                    break
            if not alt_found:
                print(f"MISMATCH (bib has '{get_bib_first_author(ck, bib_text_cache)}', CNKI has '{first_cn}')")
                continue

        authors_str = format_chinese_authors(authors)
        n = len(authors_str.split(" and "))
        venue = best.get("venue", "")
        year = best.get("year", "")
        print(f"{first_cn} and {'...'} ({n} auth, {venue} {year})")
        results[ck] = authors_str

    print(f"\nFound: {len(results)}/{len(ENTRIES)}")

    if args.apply and results:
        applied = 0
        for ck, authors_str in results.items():
            pattern = rf"(@\w+\{{{ck},.*?author\s*=\s*\{{)([^}}]*)(\}})"
            match = re.search(pattern, bib_text, re.DOTALL)
            if match:
                bib_text = bib_text[:match.start()] + match.group(1) + authors_str + match.group(3) + bib_text[match.end():]
                applied += 1
            else:
                print(f"  WARN: {ck} not found in bib")
        BIB_PATH.write_text(bib_text, encoding="utf-8")
        print(f"Applied {applied} updates")
    elif results:
        print("\nDry run. Use --apply to update bib.")


if __name__ == "__main__":
    main()
