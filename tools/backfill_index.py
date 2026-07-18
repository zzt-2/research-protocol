#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────────────
# 一次性回填脚本：扫 search-archive/*/*.json → 重建 search-archive/_index/all-papers.jsonl
#
# 用法：
#   ~/.venvs/torch/bin/python tools/backfill_index.py            # 默认全量
#   ~/.venvs/torch/bin/python tools/backfill_index.py --dry-run  # 不写盘，只统计
#   ~/.venvs/torch/bin/python tools/backfill_index.py --since 2026-07  # 只扫 2026-07 之后
#
# 幂等：多次运行结果一致（去重 + 合并）
# 估计耗时：2084 文件 × 18 条目 ≈ 1-2 分钟
# ──────────────────────────────────────────────────────────────────────────────

import argparse
import json
import os
import sys
import time
from pathlib import Path

# 把 tools/ 加入 path 以便 import litsearch 包
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from litsearch.search_index import (
    _dedup_key,
    _index_path,
    _merge,
    _result_to_record,
    _write_index,
)


def scan_archive(archive_root: Path, since: str = None) -> tuple:
    """
    扫所有 search-archive/{date}/*.json，合并到全局索引。
    返回 (records dict, stats dict)
    """
    records = {}
    files_scanned = 0
    files_failed = 0
    entries_seen = 0
    since_prefix = since  # 如 "2026-07"

    # 按日期升序扫，保证 first_seen/last_seen 正确
    date_dirs = sorted(
        [d for d in archive_root.iterdir() if d.is_dir() and d.name[0].isdigit()]
    )
    for date_dir in date_dirs:
        if since_prefix and date_dir.name < since_prefix:
            continue
        date_str = date_dir.name
        json_files = sorted(date_dir.glob("*.json"))
        for jf in json_files:
            files_scanned += 1
            try:
                with jf.open(encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                files_failed += 1
                continue
            query = data.get("query", "")
            sources = data.get("sources", [])
            results = data.get("results", [])
            for r in results:
                if not isinstance(r, dict):
                    continue
                entries_seen += 1
                rec = _result_to_record(r, query, date_str)
                if sources and r.get("source_api") is None:
                    rec["source_apis"] = list(sources)
                key = rec["key"]
                if key in records:
                    records[key] = _merge(records[key], rec)
                else:
                    records[key] = rec
    stats = {
        "files_scanned": files_scanned,
        "files_failed": files_failed,
        "entries_seen": entries_seen,
        "unique_papers": len(records),
    }
    return records, stats


def main():
    parser = argparse.ArgumentParser(
        description="回填全局论文索引：扫 search-archive/*/*.json → all-papers.jsonl"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="不写盘，只统计"
    )
    parser.add_argument(
        "--since", default=None,
        help="只扫指定前缀之后（如 --since 2026-07）"
    )
    args = parser.parse_args()

    archive_root = SCRIPT_DIR.parent / "search-archive"
    if not archive_root.exists():
        print(f"错误：search-archive 不存在：{archive_root}", file=sys.stderr)
        sys.exit(1)

    print(f"扫描 {archive_root}{'（since=' + args.since + '）' if args.since else ''} ...")
    t0 = time.time()
    records, stats = scan_archive(archive_root, since=args.since)
    elapsed = time.time() - t0

    print()
    print("=" * 60)
    print("  回填统计")
    print("=" * 60)
    print(f"  扫描文件数：    {stats['files_scanned']}")
    print(f"  失败文件数：    {stats['files_failed']}")
    print(f"  条目总数（去重前）：{stats['entries_seen']}")
    print(f"  唯一论文数（去重后）：{stats['unique_papers']}")
    print(f"  去重率：        {stats['entries_seen'] / max(stats['unique_papers'],1):.1f}x")
    print(f"  耗时：          {elapsed:.1f}s")
    print()

    if args.dry_run:
        print("[dry-run] 不写盘")
        return

    path = _index_path()
    _write_index(path, records)
    size_kb = path.stat().st_size / 1024
    print(f"已写入：{path}")
    print(f"文件大小：{size_kb:.1f} KB ({size_kb/1024:.2f} MB)")


if __name__ == "__main__":
    main()
