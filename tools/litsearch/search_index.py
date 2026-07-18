# 全局论文索引维护：每次检索后增量更新 search-archive/_index/all-papers.jsonl
#
# 设计：
# - 去重键 = DOI（小写）优先；无 DOI 用 title 前 80 字符小写
# - 每条记录字段：doi, title, year, venue, citation_count, arxiv_id,
#   abstract（完整摘要，支持关键词扫描复现原始检索精度），source_apis[],
#   queries[]（命中查询，去重）, first_seen_date, last_seen_date, hit_count
# - 合并策略：已存在 → queries/dates/sources 并集，citation_count 取较大，
#   其他字段取最新非空；新论文 → 追加
# - 失败不阻塞主流程（try/except + 打印警告）
#
# 用法（被 search_pipeline._auto_save 调用）：
#     from .search_index import update_global_index
#     update_global_index(archive_file, output_data)

import json
import os
import re
import sys
from pathlib import Path


# 索引文件路径（相对 research-protocol 根）
def _index_path() -> Path:
    # search_pipeline.py 位于 tools/litsearch/，往上 3 级是 research-protocol 根
    return Path(__file__).resolve().parent.parent.parent / "search-archive" / "_index" / "all-papers.jsonl"


def _dedup_key(result: dict) -> str:
    """去重键：DOI 优先（小写化），否则 title 前 80 字符小写"""
    doi = (result.get("doi") or "").strip().lower()
    if doi:
        return f"doi:{doi}"
    title = (result.get("title") or "").strip().lower()
    # 去标点 + 折叠空白，取前 80 字符
    title = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", "", title))[:80]
    return f"title:{title}"


def _result_to_record(result: dict, query: str, date_str: str) -> dict:
    """从单条 result 抽出索引记录"""
    return {
        "key": _dedup_key(result),
        "doi": (result.get("doi") or "").strip().lower() or None,
        "title": (result.get("title") or "").strip(),
        "year": result.get("year"),
        "venue": result.get("venue") or "",
        "citation_count": result.get("citation_count") or 0,
        "arxiv_id": result.get("arxiv_id") or None,
        "abstract": result.get("abstract") or "",
        "source_apis": [result.get("source_api")] if result.get("source_api") else [],
        "queries": [query[:120]] if query else [],
        "first_seen_date": date_str,
        "last_seen_date": date_str,
        "hit_count": 1,
    }


def _merge(existing: dict, new: dict) -> dict:
    """合并两条记录（已存在 + 新出现）"""
    # queries/dates/sources 并集（保序去重）
    def union(a, b):
        seen = set()
        out = []
        for x in a + b:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    existing["queries"] = union(existing.get("queries", []), new.get("queries", []))
    existing["source_apis"] = union(existing.get("source_apis", []), new.get("source_apis", []))
    existing["hit_count"] = existing.get("hit_count", 0) + 1
    # citation_count 取较大
    if new.get("citation_count", 0) > existing.get("citation_count", 0):
        existing["citation_count"] = new["citation_count"]
    # 其他字段：existing 为空则用 new
    for k in ("doi", "title", "year", "venue", "arxiv_id", "abstract_short"):
        if not existing.get(k) and new.get(k):
            existing[k] = new[k]
    # last_seen_date 取较新
    if new.get("last_seen_date", "") > existing.get("last_seen_date", ""):
        existing["last_seen_date"] = new["last_seen_date"]
    # first_seen_date 取较旧
    if new.get("first_seen_date", "") < existing.get("first_seen_date", "") or not existing.get("first_seen_date"):
        existing["first_seen_date"] = new["first_seen_date"]
    return existing


def _load_index(path: Path) -> dict:
    """读现有 JSONL 到 dict（按 key）"""
    records = {}
    if not path.exists():
        return records
    try:
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    records[r.get("key", "")] = r
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"[索引] 警告：读取现有索引失败，将重建：{e}", file=sys.stderr)
    return records


def _write_index(path: Path, records: dict) -> None:
    """写回 JSONL（全量重写）"""
    path.parent.mkdir(parents=True, exist_ok=True)
    # 先写临时文件再原子替换，防中途崩溃
    tmp = path.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for r in records.values():
            # 输出时去掉内部 key 字段（去重键不暴露给消费者，避免冗余）
            out = {k: v for k, v in r.items() if k != "key"}
            out["key"] = r.get("key", "")  # 保留 key 供去重/查询，放末尾
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
    tmp.replace(path)


def update_global_index_from_results(
    results: list, query: str, date_str: str, source_apis: list = None
) -> tuple:
    """
    把一次检索的 results 合并到全局索引。返回 (新增数, 更新数, 总数)。
    不抛异常——失败时打印警告返回 (0,0,0)。
    """
    try:
        path = _index_path()
        records = _load_index(path)
        new_count, update_count = 0, 0
        for r in results:
            rec = _result_to_record(r, query, date_str)
            if source_apis and r.get("source_api") is None:
                rec["source_apis"] = list(source_apis)
            key = rec["key"]
            if key in records:
                records[key] = _merge(records[key], rec)
                update_count += 1
            else:
                records[key] = rec
                new_count += 1
        _write_index(path, records)
        return (new_count, update_count, len(records))
    except Exception as e:
        print(f"[索引] 警告：更新索引失败（不影响检索）：{e}", file=sys.stderr)
        return (0, 0, 0)


def update_global_index(archive_file: Path, output_data: dict) -> None:
    """
    被 search_pipeline._auto_save 调用：从已落盘的 archive JSON 抽数据更新索引。
    archive_file: 已落盘的 search-archive/{date}/{slug}.json 路径
    output_data: 该 JSON 的内容（含 query/results/sources）
    """
    query = output_data.get("query", "")
    # 从 archive_file 路径抽 date（/{date}/{slug}.json）
    try:
        date_str = archive_file.parent.name
    except Exception:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
    results = output_data.get("results", [])
    sources = output_data.get("sources", [])
    new_n, upd_n, total = update_global_index_from_results(results, query, date_str, sources)
    if new_n or upd_n:
        print(f"[索引] +{new_n} 新 / {upd_n} 更新 → all-papers.jsonl（总 {total}）")
