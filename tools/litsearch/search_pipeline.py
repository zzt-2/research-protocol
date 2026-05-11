# 去重、过滤、排序、相关性打分、模式检测、预设策略、自动存档

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from .search_config import (
    DOMAIN_BLACKLIST,
    DOMAIN_GREYLIST,
    DOC_TYPE_LABELS,
    DOC_TYPE_SOURCE_MAP,
    MODE_SOURCES,
    PRESET_STRATEGIES,
    SOURCE_WEIGHTS,
    STANDARD_KEYWORDS,
    VALID_DOC_TYPES,
)


def _detect_mode(query: str) -> str:
    if re.search(r'[\u4e00-\u9fff]', query):
        return "chinese"
    query_lower = query.lower()
    if any(kw.lower() in query_lower for kw in STANDARD_KEYWORDS):
        return "standard"
    return "academic"


def _resolve_sources(mode: str, explicit_sources: Optional[list[str]] = None) -> list[str]:
    if explicit_sources:
        return explicit_sources
    return MODE_SOURCES.get(mode, MODE_SOURCES["academic"])


def _resolve_sources_with_doctypes(
    mode: str,
    doc_types: Optional[list[str]] = None,
    sources: Optional[list[str]] = None,
) -> list[str]:
    if sources:
        return sources
    base = list(MODE_SOURCES.get(mode, MODE_SOURCES["academic"]))
    if not doc_types:
        return base
    extra = []
    for dt in doc_types:
        extra.extend(DOC_TYPE_SOURCE_MAP.get(dt, []))
    # 去重保序合并
    seen = set(base)
    for s in extra:
        if s not in seen:
            base.append(s)
            seen.add(s)
    return base


def _extract_keywords(query: str) -> set[str]:
    keywords = set()
    en_stopwords = {
        "the", "and", "for", "with", "from", "using", "based",
        "that", "this", "are", "was", "were", "been", "has",
        "have", "had", "not", "but", "its", "can", "will",
        "all", "also", "than", "into", "such", "over", "only",
    }
    cn_stopwords = {
        "的", "了", "在", "是", "和", "与", "或", "对", "中",
        "等", "及", "其", "被", "将", "从", "以", "为", "上",
        "下", "不", "有", "个", "这", "那", "之", "到", "也",
    }
    for w in re.findall(r'[a-zA-Z]{3,}', query.lower()):
        if w not in en_stopwords:
            keywords.add(w)

    # 中文：优先按空格/标点拆分（调用方控制粒度）
    cn_segments = re.split(r'[\s,;，；、]+', query)
    cn_parts = []
    for seg in cn_segments:
        cn_chunks = re.findall(r'[\u4e00-\u9fff]{2,}', seg)
        if cn_chunks:
            # 空格分隔的多段查询，直接保留原始段
            if len(cn_chunks) > 1 or re.search(r'[\s,;，；、]', query):
                cn_parts.extend(cn_chunks)
            else:
                # 单段无分隔的纯中文，用 jieba 兜底分词
                try:
                    import jieba
                    words = [w for w in jieba.cut(seg) if len(w) >= 2 and w not in cn_stopwords]
                    cn_parts.extend(words if words else cn_chunks)
                except ImportError:
                    cn_parts.extend(cn_chunks)
    keywords.update(cn_parts)
    return keywords


def _compute_relevance(results: list[dict], query: str) -> list[dict]:
    keywords = _extract_keywords(query)
    if not keywords:
        for r in results:
            r["relevance_score"] = 0.5
        return results
    for r in results:
        text = f"{r.get('title', '')} {r.get('abstract', '')}".lower()
        matched = sum(1 for kw in keywords if kw.lower() in text)
        r["relevance_score"] = round(matched / len(keywords), 3)
    return results


def _filter_by_relevance(results: list[dict], threshold: float = 0.3) -> list[dict]:
    filtered = [r for r in results if r.get("relevance_score", 0) >= threshold]
    removed = len(results) - len(filtered)
    if removed > 0:
        print(f"  [筛选] 过滤掉 {removed} 条低相关性结果（阈值 {threshold:.0%}）")
    return filtered


def _extract_domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        host = urlparse(url).netloc.lower()
        # 去掉端口，取主域名
        host = host.split(":")[0]
        # 匹配黑名单时优先精确匹配，再匹配父域名
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def _filter_by_domain(results: list[dict]) -> list[dict]:
    if not DOMAIN_BLACKLIST and not DOMAIN_GREYLIST:
        return results
    kept = []
    greylisted = 0
    blacklisted = 0
    for r in results:
        urls = [r.get("url", ""), r.get("link", ""), r.get("pdf_url", "")]
        domain = ""
        for u in urls:
            if u:
                domain = _extract_domain(u)
                if domain:
                    break
        # 精确匹配或后缀匹配黑名单
        is_black = False
        if domain:
            parts = domain.split(".")
            for i in range(len(parts)):
                candidate = ".".join(parts[i:])
                if candidate in DOMAIN_BLACKLIST:
                    is_black = True
                    break
        if is_black:
            blacklisted += 1
            continue
        # 灰名单降权：扣减相关性分数
        is_grey = False
        if domain:
            parts = domain.split(".")
            for i in range(len(parts)):
                candidate = ".".join(parts[i:])
                if candidate in DOMAIN_GREYLIST:
                    is_grey = True
                    break
        if is_grey:
            r["relevance_score"] = max(0, r.get("relevance_score", 0.5) - 0.3)
            greylisted += 1
        kept.append(r)
    if blacklisted > 0 or greylisted > 0:
        tags = []
        if blacklisted:
            tags.append(f"{blacklisted} 条黑名单域名")
        if greylisted:
            tags.append(f"{greylisted} 条灰名单降权")
        print(f"  [域名] {', '.join(tags)}")
    return kept


def _split_scenario_method(query: str) -> list[str]:
    connectors = [" + ", " and ", " with ", " using ", " via ", " by ", " through "]
    for conn in connectors:
        idx = query.lower().find(conn)
        if idx >= 0:
            parts = [query[:idx].strip(), query[idx + len(conn):].strip()]
            if all(len(p) > 2 for p in parts):
                return [query, parts[0], parts[1]]
    words = query.split()
    if len(words) >= 4:
        mid = len(words) // 2
        return [query, " ".join(words[:mid]), " ".join(words[mid:])]
    return [query]


def _apply_preset(query: str, preset: str) -> tuple[str, dict]:
    strategy = PRESET_STRATEGIES.get(preset, {})
    if preset == "scenario-method":
        return query, strategy
    modified_query = query
    append_terms = strategy.get("append_terms", [])
    if append_terms:
        modified_query = f'{query} {" ".join(append_terms)}'
    return modified_query, strategy


def deduplicate(results: list[dict]) -> list[dict]:
    seen_doi: dict[str, int] = {}
    seen_title: dict[str, int] = {}
    unique = []

    for r in results:
        doi = r.get("doi")
        title_key = re.sub(r'\s+', '', (r.get("title") or "").lower())

        if doi and doi in seen_doi:
            idx = seen_doi[doi]
            if r.get("citation_count", 0) > unique[idx].get("citation_count", 0):
                unique[idx] = r
            else:
                unique[idx]["source_api"] = f"{unique[idx].get('source_api', '')}+{r.get('source_api', '')}"
            continue
        if title_key and title_key in seen_title:
            idx = seen_title[title_key]
            if r.get("citation_count", 0) > unique[idx].get("citation_count", 0):
                unique[idx] = r
            else:
                unique[idx]["source_api"] = f"{unique[idx].get('source_api', '')}+{r.get('source_api', '')}"
            continue

        idx = len(unique)
        if doi:
            seen_doi[doi] = idx
        if title_key:
            seen_title[title_key] = idx
        unique.append(r)

    return unique


def filter_results(
    results: list[dict],
    min_citations: int = 0,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> list[dict]:
    filtered = []
    for r in results:
        if r.get("citation_count", 0) < min_citations:
            continue
        year = r.get("year")
        if year_from and year and year < year_from:
            continue
        if year_to and year and year > year_to:
            continue
        filtered.append(r)
    return filtered


def sort_results(results: list[dict], sort_by: str = "composite", query: str = "") -> list[dict]:
    if sort_by == "citations":
        return sorted(results, key=lambda r: r.get("citation_count", 0), reverse=True)
    elif sort_by == "year":
        return sorted(results, key=lambda r: r.get("year") or 0, reverse=True)
    elif sort_by == "relevance":
        return sorted(results, key=lambda r: r.get("relevance_score", 0), reverse=True)
    elif sort_by == "composite":
        max_cites = max((r.get("citation_count", 0) for r in results), default=1) or 1
        current_year = datetime.now().year
        for r in results:
            relevance = r.get("relevance_score", 0.5)
            citation_rank = r.get("citation_count", 0) / max_cites
            source_w = SOURCE_WEIGHTS.get(r.get("source_api", ""), 0.5)
            year_val = r.get("year") or (current_year - 10)
            recency = max(0, min(1, (year_val - (current_year - 10)) / 10))
            r["_score"] = relevance * 0.5 + source_w * citation_rank * 0.3 + recency * 0.2
        return sorted(results, key=lambda r: r.get("_score", 0), reverse=True)
    return results


PREPRINT_DOI_PREFIXES = ("10.48550",)
PREPRINT_VENUE_KEYWORDS = ["arxiv", "ssrn", "biorxiv", "medrxiv", "preprint"]

PUBLICATION_STATUS_LABELS = {
    "published": "正式发表",
    "preprint": "预印本",
    "unknown": "未知",
}


def infer_publication_status(result: dict) -> str:
    doi = (result.get("doi") or "").strip()
    if doi:
        if doi.startswith("10.48550") or "/arXiv." in doi:
            return "preprint"
        if doi.startswith("10."):
            return "published"
    venue = (result.get("venue") or "").lower()
    if venue:
        if any(pv in venue for pv in PREPRINT_VENUE_KEYWORDS):
            return "preprint"
        if len(venue) > 3:
            return "published"
    return "unknown"


def assign_publication_status(results: list[dict]) -> list[dict]:
    for r in results:
        r["publication_status"] = infer_publication_status(r)
    return results


def assign_ids(results: list[dict], start_id: int = 1) -> list[dict]:
    for i, r in enumerate(results):
        r["id"] = f"L{start_id + i:03d}"
        r["download"] = bool(
            r.get("is_open_access")
            or r.get("arxiv_id")
            or r.get("citation_count", 0) >= 5
        )
    return results


def _auto_save(results: list[dict], query: str, sources: list[str]) -> None:
    from .search_output import to_json

    archive_dir = Path(__file__).resolve().parent.parent.parent / "search-archive"
    archive_dir.mkdir(exist_ok=True)
    if query.startswith(('http://', 'https://')):
        from urllib.parse import urlparse
        parsed = urlparse(query)
        slug = "url-" + re.sub(r'[^a-z0-9]+', '-', parsed.netloc + parsed.path).strip('-')[:50]
    elif re.match(r'10\.\d{4,9}/', query):
        slug = "doi-" + re.sub(r'[^a-z0-9]+', '-', query.lower()).strip('-')[:50]
    else:
        slug = re.sub(r'[^a-z0-9]+', '-', query.lower()).strip('-')[:60] or "search"
    date_str = datetime.now().strftime('%Y-%m-%d')
    archive_file = archive_dir / f"{date_str}-{slug}.json"
    counter = 1
    while archive_file.exists():
        archive_file = archive_dir / f"{date_str}-{slug}-{counter}.json"
        counter += 1
    output_data = to_json(results, query, sources)
    archive_file.write_text(
        json.dumps(output_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    rel_path = archive_file.relative_to(Path(__file__).resolve().parent.parent.parent)
    print(f"[存档] {rel_path}")
