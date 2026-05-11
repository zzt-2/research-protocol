# 五源搜索函数（S2 / OpenAlex / arXiv / SerpAPI / Tavily）、S2 引用链、HTTP retry

import re
import shlex
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Optional

import requests

from .search_config import (
    ARXIV_NS,
    ARXIV_SEARCH_URL,
    DOC_TYPE_QUERY_MODIFIERS,
    EXA_API_BASE,
    FIRECRAWL_API_BASE,
    OPENALEX_WORKS_URL,
    REQUEST_TIMEOUT,
    S2_FIELDS,
    S2_SEARCH_URL,
    USER_AGENT,
    _resolve_keys,
)


def _retry_request(
    method: str,
    url: str,
    max_retries: int = 5,
    fast_fail: bool = False,
    **kwargs,
) -> Optional[requests.Response]:
    """带指数退避的 HTTP 请求"""
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    kwargs.setdefault("headers", {})
    kwargs["headers"]["User-Agent"] = USER_AGENT

    for attempt in range(max_retries):
        try:
            resp = requests.request(method, url, **kwargs)
            if resp.status_code == 429:
                if fast_fail and attempt == 0:
                    print(f"  [RATE-LIMIT] 被限速，跳过此源", file=sys.stderr)
                    return None
                wait = 3 * (2 ** attempt)
                print(f"  [RATE-LIMIT] 等待 {wait}s 后重试 ({attempt+1}/{max_retries})...", file=sys.stderr)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"  [ERROR] 请求失败: {e}", file=sys.stderr)
                return None
            time.sleep(2 ** attempt)
    return None


# ---------- Semantic Scholar ----------

def search_semantic_scholar(
    query: str,
    max_results: int = 20,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    print(f"[S2] 搜索: {query}")

    params: dict[str, Any] = {
        "query": query,
        "limit": min(max_results, 100),
        "fields": S2_FIELDS,
    }
    if year_from or year_to:
        params["year"] = f"{year_from or ''}-{year_to or ''}"

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    resp = _retry_request(
        "GET", S2_SEARCH_URL,
        fast_fail=not api_key,
        params=params, headers=headers,
    )
    if not resp:
        return []

    data = resp.json()
    papers = data.get("data", [])
    print(f"  [S2] 找到 {data.get('total', '?')} 篇，返回 {len(papers)} 篇")

    results = []
    for p in papers:
        ext_ids = p.get("externalIds") or {}
        oa_pdf = p.get("openAccessPdf") or {}
        authors = [a.get("name", "") for a in (p.get("authors") or [])]
        results.append({
            "title": p.get("title", ""),
            "authors": authors,
            "venue": p.get("venue", ""),
            "year": p.get("year"),
            "doi": ext_ids.get("DOI"),
            "arxiv_id": ext_ids.get("ArXiv"),
            "abstract": p.get("abstract", ""),
            "citation_count": p.get("citationCount", 0),
            "is_open_access": p.get("isOpenAccess", False),
            "pdf_url": oa_pdf.get("url"),
            "source_api": "semantic_scholar",
        })

    time.sleep(1)
    return results


def get_s2_references(
    paper_id: str,
    max_results: int = 20,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references"
    params = {"fields": S2_FIELDS, "limit": min(max_results, 100)}
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    resp = _retry_request("GET", url, fast_fail=not api_key, params=params, headers=headers)
    if not resp:
        return []

    data = resp.json()
    refs = data.get("data") or []
    print(f"  [S2-refs] {paper_id}: 返回 {len(refs)} 条参考文献")

    results = []
    for ref in refs:
        paper = ref.get("citedPaper") or {}
        if not paper.get("title"):
            continue
        ext_ids = paper.get("externalIds") or {}
        oa_pdf = paper.get("openAccessPdf") or {}
        authors = [a.get("name", "") for a in (paper.get("authors") or [])]
        results.append({
            "title": paper.get("title", ""),
            "authors": authors,
            "venue": paper.get("venue", ""),
            "year": paper.get("year"),
            "doi": ext_ids.get("DOI"),
            "arxiv_id": ext_ids.get("ArXiv"),
            "abstract": paper.get("abstract", ""),
            "citation_count": paper.get("citationCount", 0),
            "is_open_access": paper.get("isOpenAccess", False),
            "pdf_url": oa_pdf.get("url"),
            "source_api": "s2_references",
            "expanded_from": paper_id,
        })
    time.sleep(1)
    return results


def get_s2_citations(
    paper_id: str,
    max_results: int = 20,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations"
    params = {"fields": S2_FIELDS, "limit": min(max_results, 100)}
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    resp = _retry_request("GET", url, fast_fail=not api_key, params=params, headers=headers)
    if not resp:
        return []

    data = resp.json()
    cites = data.get("data") or []
    print(f"  [S2-cites] {paper_id}: 返回 {len(cites)} 条引用")

    results = []
    for cite in cites:
        paper = cite.get("citingPaper") or {}
        if not paper.get("title"):
            continue
        ext_ids = paper.get("externalIds") or {}
        oa_pdf = paper.get("openAccessPdf") or {}
        authors = [a.get("name", "") for a in (paper.get("authors") or [])]
        results.append({
            "title": paper.get("title", ""),
            "authors": authors,
            "venue": paper.get("venue", ""),
            "year": paper.get("year"),
            "doi": ext_ids.get("DOI"),
            "arxiv_id": ext_ids.get("ArXiv"),
            "abstract": paper.get("abstract", ""),
            "citation_count": paper.get("citationCount", 0),
            "is_open_access": paper.get("isOpenAccess", False),
            "pdf_url": oa_pdf.get("url"),
            "source_api": "s2_citations",
            "expanded_from": paper_id,
        })
    time.sleep(1)
    return results


# ---------- OpenAlex ----------

def _openalex_restore_abstract(inverted_index: Optional[dict]) -> str:
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions)


def search_openalex(
    query: str,
    max_results: int = 20,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    email: Optional[str] = None,
) -> list[dict[str, Any]]:
    print(f"[OpenAlex] 搜索: {query}")

    params: dict[str, Any] = {
        "search": query,
        "per_page": min(max_results, 50),
        "select": "id,doi,title,authorships,publication_year,primary_location,cited_by_count,open_access,abstract_inverted_index,locations",
    }

    filters = []
    if year_from:
        filters.append(f"publication_year:>{year_from - 1}")
    if year_to:
        filters.append(f"publication_year:<{year_to + 1}")
    if filters:
        params["filter"] = ",".join(filters)

    if email:
        params["mailto"] = email

    resp = _retry_request("GET", OPENALEX_WORKS_URL, params=params)
    if not resp:
        return []

    data = resp.json()
    works = data.get("results", [])
    print(f"  [OpenAlex] 找到 {data.get('meta', {}).get('count', '?')} 篇，返回 {len(works)} 篇")

    results = []
    for w in works:
        abstract = _openalex_restore_abstract(w.get("abstract_inverted_index"))
        doi_raw = w.get("doi") or ""
        doi = doi_raw.replace("https://doi.org/", "") if doi_raw else None

        authors = []
        for authorship in (w.get("authorships") or []):
            name = (authorship.get("author") or {}).get("display_name", "")
            if name:
                authors.append(name)

        primary = w.get("primary_location") or {}
        source = primary.get("source") or {}
        venue = source.get("display_name", "")

        oa_info = w.get("open_access") or {}

        arxiv_id = None
        for loc in (w.get("locations") or []):
            src = loc.get("source") or {}
            src_name = (src.get("display_name") or "").lower()
            src_url = (src.get("homepage_url") or "").lower()
            if src_name == "arxiv" or "arxiv.org" in src_url:
                lp_url = loc.get("landing_page_url") or ""
                if "/abs/" in lp_url:
                    arxiv_id = lp_url.split("/abs/")[-1]
                    break

        results.append({
            "title": w.get("title", ""),
            "authors": authors,
            "venue": venue,
            "year": w.get("publication_year"),
            "doi": doi,
            "arxiv_id": arxiv_id,
            "abstract": abstract,
            "citation_count": w.get("cited_by_count", 0),
            "is_open_access": oa_info.get("is_oa", False),
            "pdf_url": oa_info.get("oa_url"),
            "source_api": "openalex",
        })

    return results


# ---------- arXiv ----------

def _build_arxiv_query(query: str) -> str:
    try:
        tokens = shlex.split(query)
    except ValueError:
        tokens = query.split()

    if not tokens:
        return f"all:{query}"

    parts = []
    for token in tokens:
        escaped = token.replace('"', '')
        parts.append(f'(ti:"{escaped}" OR abs:"{escaped}")')

    return " AND ".join(parts)


def search_arxiv(
    query: str,
    max_results: int = 20,
) -> list[dict[str, Any]]:
    arxiv_query = _build_arxiv_query(query)
    print(f"[arXiv] 搜索: {query}")

    params = {
        "search_query": arxiv_query,
        "start": 0,
        "max_results": min(max_results, 100),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    resp = _retry_request("GET", ARXIV_SEARCH_URL, params=params)
    if not resp:
        return []

    root = ET.fromstring(resp.text)
    entries = root.findall("atom:entry", ARXIV_NS)
    total = root.find("atom:totalResults", {"atom": "http://a9.com/-/spec/opensearch/1.1/"})
    total_text = total.text if total is not None else "?"
    print(f"  [arXiv] 找到 {total_text} 篇，返回 {len(entries)} 篇")

    results = []
    for entry in entries:
        title = (entry.findtext("atom:title", "", ARXIV_NS) or "").strip().replace("\n", " ")
        abstract = (entry.findtext("atom:summary", "", ARXIV_NS) or "").strip().replace("\n", " ")
        authors = [a.findtext("atom:name", "", ARXIV_NS) for a in entry.findall("atom:author", ARXIV_NS)]

        entry_id = entry.findtext("atom:id", "", ARXIV_NS) or ""
        arxiv_id = entry_id.split("/abs/")[-1] if "/abs/" in entry_id else ""

        published = entry.findtext("atom:published", "", ARXIV_NS) or ""
        year = int(published[:4]) if len(published) >= 4 else None

        doi_elem = entry.find("arxiv:doi", ARXIV_NS)
        doi = doi_elem.text if doi_elem is not None else None

        pdf_url = None
        for link in entry.findall("atom:link", ARXIV_NS):
            if link.get("title") == "pdf":
                pdf_url = link.get("href")
                break

        categories = [c.get("term", "") for c in entry.findall("atom:category", ARXIV_NS)]
        venue = f"arXiv ({', '.join(categories[:3])})" if categories else "arXiv"

        results.append({
            "title": title,
            "authors": authors,
            "venue": venue,
            "year": year,
            "doi": doi,
            "arxiv_id": arxiv_id,
            "abstract": abstract,
            "citation_count": 0,
            "is_open_access": True,
            "pdf_url": pdf_url,
            "source_api": "arxiv",
        })

    time.sleep(3)
    return results


# ---------- SerpAPI（Google Scholar）----------

def search_serpapi_scholar(
    query: str,
    max_results: int = 20,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    keys = _resolve_keys(api_key, "SERPAPI_KEY")
    if not keys:
        print("[SerpAPI] 无 API key，跳过", file=sys.stderr)
        return []

    print(f"[SerpAPI] 搜索: {query}")

    try:
        from serpapi import GoogleSearch
    except ImportError:
        print("[SerpAPI] google-search-results 未安装，跳过", file=sys.stderr)
        return []

    params: dict[str, Any] = {
        "engine": "google_scholar",
        "q": query,
        "num": min(max_results, 50),
    }
    if year_from:
        params["as_ylo"] = year_from
    if year_to:
        params["as_yhi"] = year_to

    data = None
    for i, key in enumerate(keys):
        try:
            search = GoogleSearch({**params, "api_key": key})
            data = search.get_dict()
            break
        except Exception as e:
            print(f"  [SerpAPI] key {i+1}/{len(keys)} 失败: {e}", file=sys.stderr)
            if i < len(keys) - 1:
                print(f"  [SerpAPI] 切换到下一个 key...", file=sys.stderr)

    if data is None:
        return []

    organic = data.get("organic_results") or []
    print(f"  [SerpAPI] 返回 {len(organic)} 条结果")

    results = []
    for item in organic:
        pub_info = item.get("publication_info") or {}
        summary = item.get("snippet", "")

        authors_str = pub_info.get("authors") or []
        if isinstance(authors_str, list):
            authors = [a.get("name", "") if isinstance(a, dict) else str(a) for a in authors_str]
        else:
            authors = []

        year = None
        summary_text = pub_info.get("summary", "")
        year_match = re.search(r'\b(19|20)\d{2}\b', summary_text)
        if year_match:
            year = int(year_match.group())

        cited_by = item.get("inline_links", {}).get("cited_by", {})
        citation_count = cited_by.get("total", 0) if isinstance(cited_by, dict) else 0

        doi = None
        link = item.get("link", "")
        doi_match = re.search(r'10\.\d{4,}/[^\s&"]+', link)
        if doi_match:
            doi = doi_match.group()

        arxiv_id = None
        if "arxiv.org/abs/" in link:
            arxiv_id = link.split("/abs/")[-1]
        elif "arxiv.org/pdf/" in link:
            arxiv_id = link.split("/pdf/")[-1].replace(".pdf", "")

        results.append({
            "title": item.get("title", ""),
            "authors": authors,
            "venue": "",
            "year": year,
            "doi": doi,
            "arxiv_id": arxiv_id,
            "abstract": summary,
            "citation_count": citation_count,
            "is_open_access": False,
            "pdf_url": None,
            "source_api": "serpapi_scholar",
            "url": link,
        })

    results.sort(key=lambda r: r.get("citation_count", 0), reverse=True)
    return results


# ---------- Tavily ----------

def search_tavily(
    query: str,
    max_results: int = 10,
    api_key: Optional[str] = None,
) -> list[dict[str, Any]]:
    keys = _resolve_keys(api_key, "TAVILY_KEY")
    if not keys:
        print("[Tavily] 无 API key，跳过", file=sys.stderr)
        return []

    print(f"[Tavily] 搜索: {query}")

    try:
        from tavily import TavilyClient
    except ImportError:
        print("[Tavily] tavily-python 未安装，跳过", file=sys.stderr)
        return []

    response = None
    for i, key in enumerate(keys):
        try:
            client = TavilyClient(api_key=key)
            response = client.search(
                query=query,
                max_results=min(max_results, 20),
                search_depth="advanced",
                include_raw_content=False,
            )
            break
        except Exception as e:
            print(f"  [Tavily] key {i+1}/{len(keys)} 失败: {e}", file=sys.stderr)
            if i < len(keys) - 1:
                print(f"  [Tavily] 切换到下一个 key...", file=sys.stderr)

    if response is None:
        return []

    tavily_results = response.get("results", [])
    print(f"  [Tavily] 返回 {len(tavily_results)} 条结果")

    results = []
    for item in tavily_results:
        url = item.get("url", "")
        content_type = "web"
        if "github.com" in url:
            content_type = "github"
        elif any(d in url for d in ["3gpp", "itu.int", "ietf.org", "w3.org"]):
            content_type = "standard"
        elif any(d in url for d in ["medium.com", "towardsdatascience", "arxiv", "blog"]):
            content_type = "blog"

        results.append({
            "title": item.get("title", ""),
            "authors": [],
            "venue": f"[{content_type}]",
            "year": None,
            "doi": None,
            "arxiv_id": None,
            "abstract": item.get("content", ""),
            "citation_count": 0,
            "is_open_access": True,
            "pdf_url": url,
            "source_api": "tavily",
        })

    return results


# ---------- SerpAPI（Regular Google Web Search）----------


def search_serpapi_web(
    query: str,
    *,
    api_key: Optional[str] = None,
    num_results: int = 20,
    **kwargs,
) -> list[dict[str, Any]]:
    """SerpAPI regular Google search (not Scholar).
    Used for CNKI (site:cnki.net) and other web searches."""
    keys = _resolve_keys(api_key, "SERPAPI_KEY")
    if not keys:
        print("[SerpAPI-Web] 无 API key，跳过", file=sys.stderr)
        return []

    print(f"[SerpAPI-Web] 搜索: {query}")

    try:
        from serpapi import GoogleSearch
    except ImportError:
        print("[SerpAPI-Web] google-search-results 未安装，跳过", file=sys.stderr)
        return []

    params: dict[str, Any] = {
        "engine": "google",
        "q": query,
        "num": min(num_results, 100),
    }

    data = None
    for i, key in enumerate(keys):
        try:
            search = GoogleSearch({**params, "api_key": key})
            data = search.get_dict()
            break
        except Exception as e:
            print(f"  [SerpAPI-Web] key {i+1}/{len(keys)} 失败: {e}", file=sys.stderr)
            if i < len(keys) - 1:
                print(f"  [SerpAPI-Web] 切换到下一个 key...", file=sys.stderr)

    if data is None:
        return []

    organic = data.get("organic_results") or []
    print(f"  [SerpAPI-Web] 返回 {len(organic)} 条结果")

    results = []
    for item in organic:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")

        # 年份从 snippet 或 title 中尽力提取
        year = None
        year_match = re.search(r'\b(19|20)\d{2}\b', f"{snippet} {title}")
        if year_match:
            year = int(year_match.group())

        doi = None
        doi_match = re.search(r'10\.\d{4,}/[^\s&"]+', link)
        if doi_match:
            doi = doi_match.group()

        results.append({
            "title": title,
            "authors": [],
            "venue": "[cnki]" if "cnki.net" in link else "[web]",
            "year": year,
            "doi": doi,
            "arxiv_id": None,
            "abstract": snippet,
            "citation_count": 0,
            "is_open_access": False,
            "pdf_url": None,
            "source_api": "serpapi_web",
            "url": link,
        })

    return results


# ---------- 查询修饰 & URL 推断 ----------


def _apply_query_modifier(query: str, doc_type: Optional[str] = None) -> str:
    modifier = DOC_TYPE_QUERY_MODIFIERS.get(doc_type or "", "")
    if modifier:
        return f"{query} {modifier}"
    return query


def _infer_doc_type_from_url(url: str) -> Optional[str]:
    url_l = url.lower()
    if any(d in url_l for d in ["arxiv.org"]):
        return "preprint"
    if any(d in url_l for d in ["3gpp.org", "etsi.org", "itu.int", "ietf.org", "iso.org"]):
        return "standard"
    if "patents.google" in url_l:
        return "patent"
    if any(d in url_l for d in ["gov.cn", "whitehouse.gov", "europa.eu", "fcc.gov"]):
        return "policy"
    if any(d in url_l for d in ["reuters.com", "bloomberg.com", "sec.gov"]):
        return "financial"
    if "github.com" in url_l:
        return "code"
    if any(d in url_l for d in ["huggingface.co", "paperswithcode.com"]):
        return "dataset"
    if any(d in url_l for d in ["medium.com", "towardsdatascience", "blog"]):
        return "blog"
    if any(d in url_l for d in ["cnki.net", "wanfangdata.com.cn", "ac.cn"]):
        return "chinese_journal"
    if any(d in url_l for d in ["ieee.org", "acm.org", "springer", "wiley", "sciencedirect", "mdpi"]):
        return "journal"
    return None


# ---------- Firecrawl ----------


def search_firecrawl(
    query: str,
    *,
    api_key: Optional[str] = None,
    limit: int = 20,
    lang: str = "en",
) -> list[dict[str, Any]]:
    keys = _resolve_keys(api_key, "FIRECRAWL_API_KEY")
    if not keys:
        print("[Firecrawl] 无 API key，跳过", file=sys.stderr)
        return []

    print(f"[Firecrawl] 搜索: {query}")

    try:
        resp = requests.post(
            f"{FIRECRAWL_API_BASE}/search",
            json={
                "query": query,
                "limit": min(limit, 50),
                "lang": lang,
                "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True},
            },
            headers={"Authorization": f"Bearer {keys[0]}", "Content-Type": "application/json"},
            timeout=60,
        )
        if resp.status_code != 200:
            print(f"  [Firecrawl] 请求失败: {resp.status_code}", file=sys.stderr)
            return []
    except requests.exceptions.RequestException as e:
        print(f"  [Firecrawl] 请求异常: {e}", file=sys.stderr)
        return []

    data = resp.json()
    items = data.get("data", [])
    print(f"  [Firecrawl] 返回 {len(items)} 条结果")

    results = []
    for item in items:
        url = item.get("url", "")
        metadata = item.get("metadata", {})
        title = metadata.get("title", "") or url
        abstract = item.get("markdown", "") or item.get("content", "")
        if len(abstract) > 2000:
            abstract = abstract[:1997] + "..."

        year = None
        published = metadata.get("publishedTime", "")
        if published:
            year_match = re.search(r'\b(19|20)\d{2}\b', published)
            if year_match:
                year = int(year_match.group())

        doi = None
        doi_match = re.search(r'10\.\d{4,}/[^\s&"]+', url)
        if doi_match:
            doi = doi_match.group()

        doc_type = _infer_doc_type_from_url(url)

        results.append({
            "title": title,
            "authors": [],
            "venue": f"[{doc_type}]" if doc_type else "[web]",
            "year": year,
            "doi": doi,
            "arxiv_id": None,
            "abstract": abstract,
            "citation_count": 0,
            "is_open_access": True,
            "pdf_url": url,
            "source_api": "firecrawl",
            "doc_type": doc_type,
            "url": url,
        })

    return results


# ---------- Exa ----------


def search_exa(
    query: str,
    *,
    api_key: Optional[str] = None,
    mode: str = "auto",
    num_results: int = 20,
    category: Optional[str] = None,
) -> list[dict[str, Any]]:
    keys = _resolve_keys(api_key, "EXA_API_KEY")
    if not keys:
        print("[Exa] 无 API key，跳过", file=sys.stderr)
        return []

    headers = {"x-api-key": keys[0], "Content-Type": "application/json"}

    if mode == "auto":
        kw_results = _exa_search_single(query, headers, "keyword", num_results, category)
        ne_results = _exa_search_single(query, headers, "neural", num_results, category)
        seen_urls = set()
        merged = []
        for r in ne_results + kw_results:
            if r.get("url") not in seen_urls:
                merged.append(r)
                seen_urls.add(r.get("url", ""))
        print(f"[Exa] auto: keyword={len(kw_results)} neural={len(ne_results)} 合并={len(merged)}")
        return merged

    return _exa_search_single(query, headers, mode, num_results, category)


def _exa_search_single(
    query: str,
    headers: dict,
    mode: str,
    num_results: int,
    category: Optional[str] = None,
) -> list[dict[str, Any]]:
    print(f"[Exa] 搜索 ({mode}): {query}")

    payload: dict[str, Any] = {
        "query": query,
        "type": mode,
        "numResults": min(num_results, 50),
        "contents": {"text": True},
    }
    if category:
        payload["category"] = category

    try:
        resp = requests.post(
            f"{EXA_API_BASE}/search", json=payload, headers=headers, timeout=30,
        )
        if resp.status_code != 200:
            print(f"  [Exa] {mode} 失败: {resp.status_code} {resp.text[:200]}", file=sys.stderr)
            return []
    except requests.exceptions.RequestException as e:
        print(f"  [Exa] {mode} 异常: {e}", file=sys.stderr)
        return []

    data = resp.json()
    items = data.get("results", [])
    print(f"  [Exa] {mode}: {len(items)} 条")

    results = []
    for item in items:
        url = item.get("url", "")
        title = item.get("title", "") or url
        abstract = item.get("text", "") or ""
        if len(abstract) > 2000:
            abstract = abstract[:1997] + "..."

        year = None
        published = item.get("publishedDate", "")
        if published:
            year_match = re.search(r'\b(19|20)\d{2}\b', published)
            if year_match:
                year = int(year_match.group())

        doi = None
        doi_match = re.search(r'10\.\d{4,}/[^\s&"]+', url)
        if doi_match:
            doi = doi_match.group()

        arxiv_id = None
        if "arxiv.org/abs/" in url:
            arxiv_id = url.split("/abs/")[-1]
        elif "arxiv.org/pdf/" in url:
            arxiv_id = url.split("/pdf/")[-1].replace(".pdf", "")

        doc_type = _infer_doc_type_from_url(url)

        results.append({
            "title": title,
            "authors": item.get("author", "").split(", ") if item.get("author") else [],
            "venue": f"[{doc_type}]" if doc_type else "",
            "year": year,
            "doi": doi,
            "arxiv_id": arxiv_id,
            "abstract": abstract,
            "citation_count": 0,
            "is_open_access": True,
            "pdf_url": url,
            "source_api": "exa",
            "doc_type": doc_type,
            "url": url,
        })

    return results


def exa_find_similar(
    url: str,
    *,
    api_key: Optional[str] = None,
    num_results: int = 10,
) -> list[dict[str, Any]]:
    keys = _resolve_keys(api_key, "EXA_API_KEY")
    if not keys:
        print("[Exa] 无 API key，跳过 find_similar", file=sys.stderr)
        return []

    print(f"[Exa] find_similar: {url}")

    try:
        resp = requests.post(
            f"{EXA_API_BASE}/findSimilar",
            json={"url": url, "numResults": num_results, "contents": {"text": True}},
            headers={"x-api-key": keys[0], "Content-Type": "application/json"},
            timeout=30,
        )
        if resp.status_code != 200:
            print(f"  [Exa] find_similar 失败: {resp.status_code} {resp.text[:200]}", file=sys.stderr)
            return []
    except requests.exceptions.RequestException as e:
        print(f"  [Exa] find_similar 异常: {e}", file=sys.stderr)
        return []

    data = resp.json()
    items = data.get("results", [])
    print(f"  [Exa] find_similar: {len(items)} 条")

    results = []
    for item in items:
        item_url = item.get("url", "")
        title = item.get("title", "") or item_url
        abstract = item.get("text", "") or ""
        if len(abstract) > 2000:
            abstract = abstract[:1997] + "..."

        year = None
        published = item.get("publishedDate", "")
        if published:
            year_match = re.search(r'\b(19|20)\d{2}\b', published)
            if year_match:
                year = int(year_match.group())

        doi = None
        doi_match = re.search(r'10\.\d{4,}/[^\s&"]+', item_url)
        if doi_match:
            doi = doi_match.group()

        arxiv_id = None
        if "arxiv.org/abs/" in item_url:
            arxiv_id = item_url.split("/abs/")[-1]

        doc_type = _infer_doc_type_from_url(item_url)

        results.append({
            "title": title,
            "authors": item.get("author", "").split(", ") if item.get("author") else [],
            "venue": f"[{doc_type}]" if doc_type else "",
            "year": year,
            "doi": doi,
            "arxiv_id": arxiv_id,
            "abstract": abstract,
            "citation_count": 0,
            "is_open_access": True,
            "pdf_url": item_url,
            "source_api": "exa_similar",
            "doc_type": doc_type,
            "url": item_url,
            "similar_to": url,
        })

    return results


# ---------- 源分发 ----------

def _search_source(source: str, query: str, args) -> list[dict]:
    import os

    if source == "s2":
        s2_key = args.s2_api_key or os.environ.get("S2_API_KEY")
        return search_semantic_scholar(
            query, max_results=args.max_per_source,
            year_from=args.year_from, year_to=args.year_to,
            api_key=s2_key,
        )
    elif source == "openalex":
        return search_openalex(
            query, max_results=args.max_per_source,
            year_from=args.year_from, year_to=args.year_to,
            email=args.openalex_email,
        )
    elif source == "arxiv":
        return search_arxiv(query, max_results=args.max_per_source)
    elif source == "serpapi":
        return search_serpapi_scholar(
            query, max_results=args.max_per_source,
            year_from=args.year_from, year_to=args.year_to,
            api_key=args.serpapi_key,
        )
    elif source == "tavily":
        return search_tavily(query, max_results=args.max_per_source, api_key=args.tavily_key)
    elif source == "firecrawl":
        fc_key = getattr(args, "firecrawl_key", None)
        lang = "zh" if re.search(r'[\u4e00-\u9fff]', query) else "en"
        return search_firecrawl(
            query, api_key=fc_key, limit=args.max_per_source, lang=lang,
        )
    elif source == "exa":
        exa_key = getattr(args, "exa_key", None)
        exa_mode = getattr(args, "exa_mode", "auto")
        category = getattr(args, "_exa_category", None)
        return search_exa(
            query, api_key=exa_key, mode=exa_mode,
            num_results=args.max_per_source, category=category,
        )
    elif source == "serpapi_web":
        return search_serpapi_web(
            query, api_key=getattr(args, "serpapi_key", None),
            num_results=args.max_per_source,
        )
    return []


def _resolve_s2_paper_id(result: dict) -> Optional[str]:
    if result.get("doi"):
        return f"DOI:{result['doi']}"
    if result.get("arxiv_id"):
        return f"ArXiv:{result['arxiv_id']}"
    return None


# ---------- OpenAlex 引用图谱 & 趋势 ----------


def openalex_citations(
    doi: str,
    *,
    direction: str = "forward",
    depth: int = 1,
    email: Optional[str] = None,
) -> list[dict[str, Any]]:
    print(f"[OpenAlex] citations ({direction}): {doi}")

    if direction == "backward":
        # 这篇引用了谁 — 先查这篇的引用列表
        ref_url = f"{OPENALEX_WORKS_URL}/doi:{doi}"
        params: dict[str, Any] = {"select": "referenced_works"}
        if email:
            params["mailto"] = email
        resp = _retry_request("GET", ref_url, params=params)
        if not resp:
            return []
        data = resp.json()
        ref_ids = data.get("referenced_works", [])
        if not ref_ids:
            return []
        ids_filter = "|".join(r.split("/")[-1] for r in ref_ids[:50])
        params = {"filter": f"openalex_id:{ids_filter}", "per_page": 50}
        if email:
            params["mailto"] = email
        resp = _retry_request("GET", OPENALEX_WORKS_URL, params=params)
        if not resp:
            return []
        works = resp.json().get("results", [])
    else:
        # 谁引用了这篇
        params = {"filter": f"cites:DOI:{doi}", "per_page": 50}
        if email:
            params["mailto"] = email
        resp = _retry_request("GET", OPENALEX_WORKS_URL, params=params)
        if not resp:
            return []
        works = resp.json().get("results", [])

    print(f"  [OpenAlex] citations: {len(works)} 条")

    results = []
    for w in works:
        abstract = _openalex_restore_abstract(w.get("abstract_inverted_index"))
        doi_raw = w.get("doi") or ""
        w_doi = doi_raw.replace("https://doi.org/", "") if doi_raw else None
        authors = []
        for a in (w.get("authorships") or []):
            name = (a.get("author") or {}).get("display_name", "")
            if name:
                authors.append(name)
        results.append({
            "title": w.get("title", ""),
            "authors": authors,
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
            "year": w.get("publication_year"),
            "doi": w_doi,
            "arxiv_id": None,
            "abstract": abstract,
            "citation_count": w.get("cited_by_count", 0),
            "is_open_access": (w.get("open_access") or {}).get("is_oa", False),
            "pdf_url": (w.get("open_access") or {}).get("oa_url"),
            "source_api": "openalex_citations",
        })

    if depth >= 2 and results:
        expanded = []
        for r in results[:5]:
            if r.get("doi"):
                sub = openalex_citations(r["doi"], direction=direction, depth=1, email=email)
                expanded.extend(sub)
                time.sleep(0.5)
        if expanded:
            results.extend(expanded)

    return results


def openalex_trend(
    query: str,
    *,
    years: int = 5,
    email: Optional[str] = None,
) -> list[dict[str, Any]]:
    print(f"[OpenAlex] trend: {query} ({years} 年)")
    current_year = datetime.now().year
    params: dict[str, Any] = {
        "search": query,
        "group_by": "publication_year",
        "per_page": 50,
    }
    filters = [f"publication_year:>{current_year - years}"]
    params["filter"] = ",".join(filters)
    if email:
        params["mailto"] = email

    resp = _retry_request("GET", OPENALEX_WORKS_URL, params=params)
    if not resp:
        return []

    data = resp.json()
    groups = data.get("group_by", [])
    print(f"  [OpenAlex] trend: {len(groups)} 个年份组")

    results = []
    for g in groups:
        key = g.get("key", "")
        count = g.get("count", 0)
        if key.isdigit():
            results.append({
                "year": int(key),
                "count": count,
                "source_api": "openalex_trend",
            })

    results.sort(key=lambda x: x["year"])
    return results
