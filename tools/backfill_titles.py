"""回填 metadata.json 的 title 字段（当 title 为空/URL/slug 且 content.md 有真标题）。

只动 unverifiable 论文，绝不动 match/mismatch（mismatch 是真损坏，回填会掩盖）。
回填后重算 classify_mismatch，预期 unverifiable 里的"基准无效"类降为 match。

安全边界（四条都满足才回填）：
1. 当前 title_check ∈ {unverifiable, None}（不碰 mismatch/match）
2. metadata title 是 empty/url/slug（绝不覆盖已有真标题）
3. extract_real_title 返回 confidence == 'high'（低置信不回填）
4. 非垃圾 content.md（_detect_junk 已在 extract_real_title 内挡掉）

用法：
    python tools/backfill_titles.py --dry-run    # 只打印计划，不改文件
    python tools/backfill_titles.py             # 执行回填 + 写回填日志

回填日志写到 .sessions/2026-06-15-read-traceability/backfill-log.md（审计用）。
"""
import argparse
import glob
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from litdownload.title_verify import (
    _is_invalid_metadata_title,
    classify_mismatch,
    extract_real_title,
)

# 正文片段/期刊名特征词——回填标题命中即拒绝（V003c 子 agent 交叉验证归纳）。
# 来源：4 篇 all_failed/残缺 content.md 抓到的"标题"实际是这些内容。
# 注意：只放"几乎只作为期刊名出现"的词，避免误伤真标题（如 "technology" 太通用会误拒）。
# all_failed 类期刊名主要由边界 0（method guard）兜底，本表是补充防线。
_NON_TITLE_MARKERS = (
    "compared with", "compared to", "the baseline", "we propose",
    "in this paper", "in this work", "as shown", "figure ", "table ",
    "scientific rep", "scientific reports",
    "transactions on", "letters on", "journal of", "proceedings of",
    "ieee access", "science china", "aerospace science",
    "physical communication", "results in optics",
)


def _looks_like_non_title(text: str) -> str | None:
    """回填标题合理性二次校验。返回失败原因 str 或 None（通过）。

    子 agent API 交叉验证（V003c）发现 4 类把非标题当标题回填的失败模式：
    1. 期刊名（"Scientific Reports"/"Aerospace Science and Technology"）
    2. 页眉碎片（"orts Scientific Rep"）
    3. 正文段落（含"compared with"/百分比/完整句子）
    4. "Open Access" 前缀泄漏（"OPEN Secure and..."）

    本函数用启发式捕获这些，避免回填看起来正确实则错误的内容。
    """
    t = text.strip()
    if not t:
        return "空"
    low = t.lower()
    # 正文/期刊名特征词
    for marker in _NON_TITLE_MARKERS:
        if marker in low:
            return f"正文/期刊名特征({marker})"
    # 正文段落特征：含句号且句号后还有多个词（标题极少含句号）
    if ". " in t and len(t.split(". ")[1].split()) >= 3:
        return "正文段落（含句号+多词）"
    # 百分比/数字开头（正文里的"60%..."）
    if t[:4].rstrip("%").replace(".", "").replace(",", "").isdigit() and "%" in t[:6]:
        return "正文数字开头"
    # 单词过少（<3 个实词多半是页眉碎片）
    words = [w for w in re.findall(r"[A-Za-z]+", t) if len(w) > 2]
    if len(words) < 3:
        return "词数过少（疑似页眉碎片）"
    return None


def main():
    ap = argparse.ArgumentParser(description="回填 metadata.json 的无效 title")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划不写文件")
    ap.add_argument("--base", default=".", help="research-protocol 根目录")
    args = ap.parse_args()

    base = Path(args.base).resolve()
    backfilled = []
    skipped = []

    for mp_str in glob.glob(str(base / "papers" / "*" / "*" / "metadata.json")):
        mp = Path(mp_str)
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue

        old_title = meta.get("title", "")
        old_check = meta.get("title_check")
        method = meta.get("download_method", "")

        # 边界 1：只动 unverifiable / 无校验记录的（不碰 mismatch/match）
        if old_check not in (None, "unverifiable"):
            continue

        # 边界 0（关键）：method=all_failed 的 content.md 本就残缺（firecrawl/unpaywall 全败），
        # 从中提取的"标题"多半是期刊名/页眉/正文片段。禁止回填。
        # 来源：子 agent API 交叉验证发现 all_failed 类 4/4 抓错页面（V003c）。
        if method == "all_failed":
            skipped.append((mp.parent.name, method, invalid_reason if (invalid_reason := _is_invalid_metadata_title(old_title)) else "?", "all_failed 不回填"))
            continue

        # 边界 2：metadata title 必须是无效（empty/url/slug），绝不覆盖真标题
        invalid_reason = _is_invalid_metadata_title(old_title)
        if not invalid_reason:
            continue

        # 边界 3+4：提取真标题，必须 high 置信（含垃圾检测）
        cm = mp.parent / "content.md"
        if not cm.exists():
            continue
        ri = extract_real_title(cm, method)
        if ri.get("confidence") != "high" or not ri.get("real_title"):
            skipped.append((mp.parent.name, method, invalid_reason, "提取非 high 置信"))
            continue

        real_title = ri["real_title"]

        # 边界 5（关键）：回填标题合理性二次校验。防止把正文片段/期刊名当标题回填。
        # 来源：子 agent 交叉验证发现的 4 类失败模式（V003c）。
        bad = _looks_like_non_title(real_title)
        if bad:
            skipped.append((mp.parent.name, method, invalid_reason, f"标题像{bad}"))
            continue

        # 回填后重算（此时 metadata title == real_title，应判 match）
        new_check = classify_mismatch(real_title, ri)

        backfilled.append({
            "dir": mp.parent.name,
            "method": method,
            "old_title": old_title,
            "real_title": real_title,
            "old_check": old_check,
            "new_check": new_check["status"],
            "new_overlap": new_check["overlap"],
            "invalid_reason": invalid_reason,
        })

        if not args.dry_run:
            meta["title"] = real_title
            meta["real_title"] = real_title
            meta["title_check"] = new_check["status"]
            meta["title_overlap"] = new_check["overlap"]
            meta["title_backfilled_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            mp.write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                          encoding="utf-8")

    # 报告
    print(f"\n{'='*70}")
    print(f"  回填{'计划（dry-run）' if args.dry_run else '完成'}：{len(backfilled)} 篇")
    print(f"  跳过（提取非 high）：{len(skipped)} 篇")
    print(f"{'='*70}\n")

    by_new = {}
    for b in backfilled:
        by_new.setdefault(b["new_check"], []).append(b)
    for status, items in sorted(by_new.items()):
        print(f"  回填后 {status}: {len(items)} 篇")

    print("\n明细（前 20）：")
    for b in backfilled[:20]:
        print(f"  [{b['method']:14s}] {b['dir']}")
        print(f"      {b['invalid_reason']:6s} → {b['new_check']:12s} (overlap={b['new_overlap']})")
        print(f"      old: {b['old_title'][:50]!r}")
        print(f"      new: {b['real_title'][:50]!r}")

    # 写回填日志（非 dry-run 时）
    if not args.dry_run and backfilled:
        log_dir = base / ".sessions" / "2026-06-15-read-traceability"
        log_path = log_dir / "backfill-log.md"
        with log_path.open("w", encoding="utf-8") as f:
            f.write(f"# Title 回填日志\n\n> {datetime.now().strftime('%Y-%m-%d %H:%M')} | backfill_titles.py | {len(backfilled)} 篇\n\n")
            f.write("回填规则：metadata title 为空/URL/slug 且 content.md 有 high 置信真标题 → 回填 title + 重算 title_check。绝不碰 match/mismatch。\n\n")
            f.write("| 目录 | method | invalid | 新状态 | overlap | 旧 title | 新 title |\n|---|---|---|---|---|---|---|\n")
            for b in backfilled:
                f.write(f"| {b['dir']} | {b['method']} | {b['invalid_reason']} | {b['new_check']} | {b['new_overlap']} | `{b['old_title'][:30]}` | `{b['real_title'][:50]}` |\n")
        print(f"\n回填日志：{log_path}")


if __name__ == "__main__":
    main()
