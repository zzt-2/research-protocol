import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Optional

from .download_channels import (
    _enrich_arxiv_id_from_doi,
    _enrich_arxiv_id_from_title,
    try_arxiv_html,
    try_arxiv_latex,
    try_arxiv_pdf,
    try_firecrawl_scrape,
    try_oa_pdf,
    try_unpaywall,
)
from .download_config import DownloadResult
from .download_output import _print_summary, _save_batch_manifest, _save_metadata


def _paper_key(paper: dict) -> Optional[str]:
    arxiv_id = paper.get("arxiv_id")
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    doi = paper.get("doi")
    if doi:
        return f"doi:{doi.lower()}"
    return None


def _paper_storage_path(paper: dict, base: Path) -> Path:
    arxiv_id = paper.get("arxiv_id")
    if arxiv_id:
        return base / "papers" / "arxiv" / arxiv_id
    doi = paper.get("doi")
    if doi:
        doi_path = doi.lower().replace("/", "_")
        return base / "papers" / "doi" / doi_path
    title = paper.get("title", "unknown")
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:50] or "manual"
    return base / "papers" / "manual" / slug


def _load_index(base: Path) -> dict:
    index_path = base / "papers" / "index.json"
    if index_path.exists():
        try:
            return json.loads(index_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"papers": {}}


def _save_index(index: dict, base: Path) -> None:
    index_path = base / "papers" / "index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8",
    )


def classify_paper(paper: dict) -> str:
    doc_type = paper.get("doc_type")
    if doc_type in ("code", "dataset"):
        return "code"
    if doc_type == "standard":
        return "standard"
    if paper.get("arxiv_id"):
        return "paper"
    source = paper.get("source_api", "")
    venue = (paper.get("venue", "") or "").lower()
    if source in ("tavily", "firecrawl"):
        if "github" in venue or "code" in venue:
            return "code"
        if "standard" in venue:
            return "standard"
    if paper.get("doi"):
        return "paper"
    title = paper.get("title", "")
    has_url = bool(paper.get("url") or paper.get("pdf_url"))
    if re.search(r"[\u4e00-\u9fff]", title) and not paper.get("arxiv_id"):
        if has_url:
            return "chinese_scrape"
        return "chinese"
    if has_url and source in ("firecrawl", "exa") and not paper.get("doi"):
        return "scrape"
    return "paper"


def download_paper(
    paper: dict,
    dest: Path,
    quality: str = "fast",
    force: bool = False,
    unpaywall_email: str = "",
) -> DownloadResult:
    dest.mkdir(parents=True, exist_ok=True)

    # 补充查找 arXiv ID（DOI 反查 → 标题模糊搜索）
    if not paper.get("arxiv_id"):
        if paper.get("doi"):
            _enrich_arxiv_id_from_doi(paper)
        if not paper.get("arxiv_id"):
            _enrich_arxiv_id_from_title(paper)

    fc_key = os.environ.get("FIRECRAWL_API_KEY", "")

    channels = [
        lambda: try_arxiv_html(paper, dest),
        lambda: try_arxiv_latex(paper, dest),
        lambda: try_arxiv_pdf(paper, dest, quality),
        lambda: try_oa_pdf(paper, dest, quality),
        lambda: try_unpaywall(paper, dest, unpaywall_email, quality),
    ]
    if fc_key:
        channels.append(lambda: try_firecrawl_scrape(paper, dest, api_key=fc_key))

    best_result: Optional[DownloadResult] = None
    for channel in channels:
        result = channel()
        if result is None:
            continue
        if result.success:
            if result.content_quality != "poor":
                return result
            # poor 质量保存为候补，继续尝试更好的通道
            if not best_result:
                best_result = result
            continue
        if result.method:
            continue

    if best_result:
        return best_result
    return DownloadResult(success=False, method="all_failed")


def _is_already_downloaded(dest: Path) -> bool:
    meta_path = dest / "metadata.json"
    if not meta_path.exists():
        return False
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return meta.get("download_status") == "success"
    except (json.JSONDecodeError, OSError):
        return False


def _download_batch(args) -> None:
    source_path = args.source.resolve()
    if not source_path.exists():
        print(f"[错误] 文件不存在: {source_path}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(source_path.read_text(encoding="utf-8"))
    papers = data.get("results", [])
    if not papers:
        print("[错误] 搜索结果为空", file=sys.stderr)
        sys.exit(1)

    batch_name = source_path.stem
    output_base = Path(args.output_dir).resolve()

    only_ids = set()
    if args.only:
        only_ids = {s.strip() for s in args.only.split(",")}

    print(f"[批量] {source_path.name} → batches/{batch_name}/")
    print(f"[论文] {len(papers)} 条结果")

    if only_ids:
        papers = [p for p in papers if p.get("id") in only_ids]
        print(f"[筛选] 保留 {len(papers)} 条: {', '.join(sorted(only_ids))}")

    index = _load_index(output_base)
    paper_ids: list[str] = []
    results: list[dict] = []

    for i, paper in enumerate(papers):
        pid = paper.get("id", f"unknown-{i}")
        title = paper.get("title", "")[:50]
        ptype = classify_paper(paper)

        if ptype in ("code", "standard", "web"):
            print(f"  [{pid}] SKIP (非论文: {ptype})  {title}")
            results.append({"id": pid, "status": "skipped", "method": ptype, "title": title})
            continue

        if ptype == "chinese":
            print(f"  [{pid}] MANUAL (中文论文)  {title}")
            results.append({"id": pid, "status": "manual_required", "method": "chinese", "title": title})
            continue

        if ptype in ("chinese_scrape", "scrape"):
            print(f"  [{pid}] SCRAPE ({ptype})  {title}")

        paper_dest = _paper_storage_path(paper, output_base)
        paper_key = _paper_key(paper)

        # 全局索引去重
        if paper_key and not args.force:
            existing = index["papers"].get(paper_key)
            if existing and existing.get("status") == "success":
                print(f"  [{pid}] INDEXED  {title}")
                results.append({"id": pid, "status": "already_exists", "method": "indexed", "title": title})
                paper_ids.append(paper_key)
                continue

        if not args.force and _is_already_downloaded(paper_dest):
            print(f"  [{pid}] CACHED  {title}")
            results.append({"id": pid, "status": "already_exists", "method": "cached", "title": title})
            if paper_key:
                paper_ids.append(paper_key)
            continue

        if args.dry_run:
            has_arxiv = "arXiv" if paper.get("arxiv_id") else ""
            has_oa = "OA" if paper.get("is_open_access") else ""
            has_doi = "DOI" if paper.get("doi") else ""
            flags = " ".join(filter(None, [has_arxiv, has_oa, has_doi]))
            rel = paper_dest.relative_to(output_base)
            print(f"  [{pid}] WILL-DOWNLOAD ({flags})  → {rel}  {title}")
            results.append({"id": pid, "status": "dry_run", "method": "", "title": title})
            if paper_key:
                paper_ids.append(paper_key)
            continue

        print(f"  [{pid}] 下载中...  {title}")
        email = args.unpaywall_email or os.environ.get("UNPAYWALL_EMAIL", "")
        result = download_paper(paper, paper_dest, quality=args.quality, force=args.force, unpaywall_email=email)
        _save_metadata(paper, result, paper_dest)

        if result.success:
            rel = paper_dest.relative_to(output_base)
            print(f"  [{pid}] OK ({result.method})  → {rel} ({result.content_quality})")
            results.append({
                "id": pid, "status": "success", "method": result.method,
                "title": title, "content_quality": result.content_quality,
            })
        else:
            print(f"  [{pid}] FAIL ({result.method})  {title}")
            results.append({"id": pid, "status": "failed", "method": result.method, "title": title})

        if paper_key:
            old_entry = index["papers"].get(paper_key, {})
            batches = list(old_entry.get("batches", []))
            if batch_name not in batches:
                batches.append(batch_name)
            index["papers"][paper_key] = {
                "path": str(paper_dest.relative_to(output_base)),
                "doi": paper.get("doi"),
                "title": paper.get("title", ""),
                "status": "success" if result.success else "failed",
                "batches": batches,
            }
            paper_ids.append(paper_key)

        if result.success:
            time.sleep(0.5)

    if not args.dry_run:
        try:
            manifest_source = str(source_path.relative_to(output_base))
        except ValueError:
            manifest_source = source_path.name
        _save_batch_manifest(
            manifest_source, results, paper_ids,
            output_base / "batches" / batch_name,
        )
        _save_index(index, output_base)

    _print_summary(results)


def _download_single(args) -> None:
    output_base = Path(args.output_dir).resolve()

    arxiv_id = args.arxiv
    doi = args.doi

    if not arxiv_id and not doi:
        print("[错误] 单篇模式需要 --arxiv 或 --doi", file=sys.stderr)
        sys.exit(1)

    paper: dict[str, Any] = {
        "id": arxiv_id or doi,
        "arxiv_id": arxiv_id,
        "doi": doi,
        "title": "",
    }

    paper_dest = _paper_storage_path(paper, output_base)
    paper_key = _paper_key(paper)
    index = _load_index(output_base)

    if not args.force:
        if paper_key:
            existing = index["papers"].get(paper_key)
            if existing and existing.get("status") == "success":
                print(f"[索引] 已存在: {existing['path']}")
                return
        if _is_already_downloaded(paper_dest):
            print(f"[缓存] 已下载: {paper_dest}")
            return

    print(f"[单篇] {'arXiv:' + arxiv_id if arxiv_id else 'DOI:' + doi}")
    print(f"  → {paper_dest.relative_to(output_base)}")

    if args.dry_run:
        return

    email = args.unpaywall_email or os.environ.get("UNPAYWALL_EMAIL", "")
    result = download_paper(paper, paper_dest, quality=args.quality, force=args.force, unpaywall_email=email)
    _save_metadata(paper, result, paper_dest)

    if result.success:
        print(f"[OK] {result.method} → {paper_dest / 'content.md'} ({result.content_quality})")
    else:
        print(f"[FAIL] {result.method}")

    if paper_key:
        index["papers"][paper_key] = {
            "path": str(paper_dest.relative_to(output_base)),
            "doi": paper.get("doi"),
            "title": paper.get("title", ""),
            "status": "success" if result.success else "failed",
            "batches": [],
        }
        _save_index(index, output_base)


def main():
    parser = argparse.ArgumentParser(
        description="论文全文下载工具 - arXiv HTML/LaTeX/PDF + OA PDF + Unpaywall",
    )

    parser.add_argument("source", nargs="?", type=Path, default=None,
                        help="搜索结果 JSON 文件（批量模式）")

    parser.add_argument("--arxiv", default=None, help="arXiv ID（单篇模式）")
    parser.add_argument("--doi", default=None, help="DOI（单篇模式）")

    parser.add_argument("--output-dir", type=str, default=None,
                        help="输出目录（默认 research-protocol/）")
    parser.add_argument("--quality", default="fast",
                        choices=["fast", "standard", "high"],
                        help="PDF→md 质量（默认 fast）")
    parser.add_argument("--force", action="store_true", help="强制重新下载")
    parser.add_argument("--dry-run", action="store_true", help="只打印计划不下载")
    parser.add_argument("--only", default=None, help="只下载指定 ID（逗号分隔）")
    parser.add_argument("--unpaywall-email", default=None, help="Unpaywall 邮箱")

    args = parser.parse_args()

    if args.output_dir is None:
        # download_pipeline.py 位于 tools/litdownload/，向上三层到 v2/
        args.output_dir = str(Path(__file__).resolve().parent.parent.parent)

    if args.source:
        _download_batch(args)
    elif args.arxiv or args.doi:
        _download_single(args)
    else:
        parser.print_help()
        sys.exit(1)
