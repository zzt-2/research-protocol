import json
from datetime import datetime, timezone
from pathlib import Path

from .download_config import DownloadResult


def _save_metadata(paper: dict, result: DownloadResult, dest: Path) -> None:
    meta = {
        "storage_version": 2,
        "id": paper.get("id", ""),
        "title": paper.get("title", ""),
        "doi": paper.get("doi"),
        "arxiv_id": paper.get("arxiv_id"),
        "download_status": "success" if result.success else "failed",
        "download_method": result.method,
        "content_type": result.content_type,
        "content_quality": result.content_quality,
        "content_file": result.content_file,
        "downloaded_at": datetime.now(timezone.utc).astimezone().isoformat(),
    }
    (dest / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8",
    )


def _save_batch_manifest(
    source_name: str,
    results: list[dict],
    paper_ids: list[str],
    batch_dir: Path,
) -> None:
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    skipped = sum(1 for r in results if r["status"] in ("skipped", "manual_required"))
    already = sum(1 for r in results if r["status"] == "already_exists")

    manifest = {
        "paper_ids": paper_ids,
        "source_archive": source_name,
        "stats": {
            "total": len(results),
            "success": success,
            "failed": failed,
            "skipped": skipped,
            "already_exists": already,
        },
        "created_at": datetime.now(timezone.utc).astimezone().isoformat(),
    }
    batch_dir.mkdir(parents=True, exist_ok=True)
    (batch_dir / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8",
    )


def _print_summary(results: list[dict]) -> None:
    print(f"\n{'='*70}")
    print(f"  下载结果: {len(results)} 篇")
    print(f"{'='*70}\n")

    for r in results:
        status_map = {
            "success": "OK",
            "failed": "FAIL",
            "skipped": "SKIP",
            "manual_required": "MANUAL",
            "already_exists": "CACHED",
        }
        tag = status_map.get(r["status"], r["status"])
        method = r.get("method", "").ljust(14)
        title = r.get("title", "")[:50]
        print(f"  {r['id']:5s} [{tag:6s}] {method}  {title}")

    success = sum(1 for r in results if r["status"] == "success")
    cached = sum(1 for r in results if r["status"] == "already_exists")
    failed = sum(1 for r in results if r["status"] == "failed")
    skipped = sum(1 for r in results if r["status"] in ("skipped", "manual_required"))
    print(f"\n  成功: {success} | 缓存: {cached} | 失败: {failed} | 跳过: {skipped}")
    print()
