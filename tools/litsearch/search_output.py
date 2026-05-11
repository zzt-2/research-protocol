# 输出格式化：JSON、Markdown 表格、简要列表、Markdown 文献索引、终端摘要

from datetime import datetime, timezone

from .search_config import DOC_TYPE_LABELS
from .search_pipeline import PUBLICATION_STATUS_LABELS


def to_json(results: list[dict], query: str, sources: list[str]) -> dict:
    return {
        "query": query,
        "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
        "sources": sources,
        "total": len(results),
        "results": results,
    }


def to_markdown(results: list[dict]) -> str:
    lines = [
        "---",
        "type: literature_notes",
        f"created: {datetime.now().strftime('%Y-%m-%d')}",
        f"last_updated: {datetime.now().strftime('%Y-%m-%d')}",
        "---",
        "",
        "# 文献笔记",
        "",
        "## 文献列表",
        "",
    ]

    for r in results:
        rid = r.get("id", "L???")
        title = r.get("title", "未知标题")
        authors = ", ".join(r.get("authors", [])[:5])
        if len(r.get("authors", [])) > 5:
            authors += " et al."

        venue = r.get("venue", "")
        year = r.get("year", "")
        pub_info = f"{venue}, {year}" if venue else str(year)

        doi = r.get("doi")
        doi_line = f"https://doi.org/{doi}" if doi else "[DOI-PENDING]"

        abstract = r.get("abstract", "") or "（摘要不可用）"
        if len(abstract) > 500:
            abstract = abstract[:497] + "..."

        citation_count = r.get("citation_count", 0)
        oa_status = "OA" if r.get("is_open_access") else "非 OA"
        arxiv_note = f" | arXiv: {r['arxiv_id']}" if r.get("arxiv_id") else ""
        dt = r.get("doc_type")
        dt_label = DOC_TYPE_LABELS.get(dt, dt) if dt else ""
        dt_note = f" | 类型: {dt_label}" if dt_label else ""
        pub_status = PUBLICATION_STATUS_LABELS.get(r.get("publication_status", "unknown"), "未知")

        lines.extend([
            f"### {rid} {title}",
            "",
            f"- **作者**: {authors}",
            f"- **出版信息**: {pub_info}",
            f"- **状态**: {pub_status}",
            f"- **DOI**: {doi_line}",
            f"- **摘要**: {abstract}",
            f"- **补充信息**: 引用数 {citation_count} | {oa_status} | 来源 {r.get('source_api', '')}{arxiv_note}{dt_note}",
            "",
        ])

    return "\n".join(lines)


def to_markdown_table(results: list[dict], query: str, sources: list[str]) -> str:
    lines = [
        f"# 搜索结果: {query}",
        "",
        f"共 {len(results)} 条 | 来源: {', '.join(sources)} | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| # | 标题 | 作者 | 年份 | 引用 | 相关性 | 状态 | 类型 | 来源 |",
        "|---|------|------|------|------|--------|------|------|------|",
    ]
    for r in results:
        rid = r.get("id", "")
        title = r.get("title", "")[:80]
        authors_list = r.get("authors", [])
        authors = f"{authors_list[0]} et al." if len(authors_list) > 2 else ", ".join(authors_list[:2])
        year = r.get("year", "-")
        cites = r.get("citation_count", 0)
        rel = f"{r.get('relevance_score', 0):.0%}"
        status = PUBLICATION_STATUS_LABELS.get(r.get("publication_status", "unknown"), "未知")
        dt = r.get("doc_type")
        dt_label = DOC_TYPE_LABELS.get(dt, dt or "")
        src = r.get("source_api", "")
        doi = r.get("doi")
        link = f" ([DOI](https://doi.org/{doi}))" if doi else ""
        lines.append(f"| {rid} | {title} | {authors} | {year} | {cites} | {rel} | {status} | {dt_label} | {src}{link} |")
    lines.append("")
    return "\n".join(lines)


def to_brief(results: list[dict]) -> str:
    lines = []
    for r in results:
        rid = r.get("id", "")
        title = r.get("title", "")[:70]
        year = r.get("year", "?")
        cites = r.get("citation_count", 0)
        rel = f"{r.get('relevance_score', 0):.0%}"
        dt = r.get("doc_type")
        dt_tag = f"[{DOC_TYPE_LABELS.get(dt, dt)}]" if dt else ""
        pub_tag = {"published": "P", "preprint": "R", "unknown": "?"}.get(r.get("publication_status", "unknown"), "?")
        lines.append(f"  {rid} [{year}] c={cites:>4} rel={rel} {pub_tag} {dt_tag:>6s}  {title}")
    return "\n".join(lines)


def print_summary(results: list[dict]) -> None:
    print(f"\n{'='*70}")
    print(f"  搜索结果: {len(results)} 篇 (去重后)")
    print(f"{'='*70}\n")

    for r in results:
        rid = r.get("id", "???")
        title = r.get("title", "")[:55]
        year = r.get("year", "?")
        cites = r.get("citation_count", 0)
        rel = f"{r.get('relevance_score', 0):.0%}"
        oa = "OA" if r.get("is_open_access") else "  "
        dl = "↓" if r.get("download") else " "
        arxiv = "arXiv" if r.get("arxiv_id") else "     "
        src = r.get("source_api", "")[:6].ljust(6)
        dt = r.get("doc_type")
        dt_tag = f"[{DOC_TYPE_LABELS.get(dt, dt)}]" if dt else "      "
        pub_tag = {"published": "P", "preprint": "R", "unknown": "?"}.get(r.get("publication_status", "unknown"), "?")
        print(f"  {rid} [{year}] {oa} {dl} c={cites:>4} r={rel} {pub_tag} {arxiv} {src} {dt_tag}  {title}")

    oa_count = sum(1 for r in results if r.get("is_open_access"))
    dl_count = sum(1 for r in results if r.get("download"))
    print(f"\n  OA: {oa_count}/{len(results)} | 建议下载: {dl_count}/{len(results)}")
    print()
