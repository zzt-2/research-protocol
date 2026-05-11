import os
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Optional

import requests

from .download_config import (
    ARXIV_EPRINT_BASE,
    ARXIV_HTML_BASE,
    ARXIV_PDF_BASE,
    BLOCKED_DOMAINS,
    CONNECT_TIMEOUT,
    REQUEST_TIMEOUT,
    UNPAYWALL_API_BASE,
    USER_AGENT,
    DownloadResult,
)


# ---------- Firecrawl Scrape ----------


def try_firecrawl_scrape(
    paper: dict,
    dest: Path,
    *,
    api_key: str,
    timeout: int = 60,
) -> Optional[DownloadResult]:
    url = paper.get("url") or paper.get("pdf_url")
    if not url:
        return None

    try:
        resp = requests.post(
            "https://api.firecrawl.dev/v1/scrape",
            json={"url": url, "formats": ["markdown"], "onlyMainContent": True},
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            timeout=timeout,
        )
        if resp.status_code != 200:
            return None
    except requests.exceptions.RequestException:
        return None

    data = resp.json()
    if not data.get("success"):
        return None

    md = data.get("data", {}).get("markdown", "")
    if not md or len(md.strip()) < 200:
        return None

    (dest / "content.md").write_text(md, encoding="utf-8")
    lines = md.count("\n")
    quality = "good" if lines > 100 else "poor"
    return DownloadResult(
        success=True,
        method="firecrawl_scrape",
        content_file="content.md",
        content_type="html",
        content_quality=quality,
    )


# ---------- HTTP ----------


def _http_get(url: str, **kwargs) -> Optional[requests.Response]:
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    kwargs.setdefault("headers", {})
    kwargs["headers"]["User-Agent"] = USER_AGENT
    try:
        resp = requests.get(url, **kwargs)
        if resp.status_code == 200:
            return resp
        return None
    except requests.exceptions.RequestException:
        return None


def _download_file(url: str, dest: Path, max_size_mb: int = 100) -> bool:
    try:
        resp = requests.get(
            url, stream=True, timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" in content_type and dest.suffix != ".html":
            return False
        size = 0
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                size += len(chunk)
                if size > max_size_mb * 1024 * 1024:
                    return False
        return dest.stat().st_size > 1024
    except Exception:
        if dest.exists():
            dest.unlink()
        return False


# ---------- PDF 转 Markdown ----------


def pdf_to_markdown(pdf_path: Path, quality: str = "fast") -> tuple[str, str]:
    if quality == "fast":
        try:
            import pymupdf4llm
            md_text = pymupdf4llm.to_markdown(str(pdf_path))
            if not md_text or len(md_text.strip()) < 100:
                return "", "empty"
            return md_text, "good"
        except ImportError:
            print("  [WARN] pymupdf4llm 未安装，跳过 PDF 转换", file=sys.stderr)
            return "", "missing_tool"
    return "", "not_implemented"


# ---------- pandoc 转换 ----------


def _pandoc_html_to_md(html_path: Path, md_path: Path) -> bool:
    try:
        result = subprocess.run(
            ["pandoc", "-f", "html", "-t", "markdown", "--wrap=none",
             "-o", str(md_path), str(html_path)],
            capture_output=True, text=True, timeout=60,
        )
        return result.returncode == 0 and md_path.exists() and md_path.stat().st_size > 100
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _pandoc_latex_to_md(tex_path: Path, md_path: Path) -> bool:
    try:
        result = subprocess.run(
            ["pandoc", "-f", "latex", "-t", "markdown", "--wrap=none",
             "-o", str(md_path), str(tex_path)],
            capture_output=True, text=True, timeout=120,
        )
        return result.returncode == 0 and md_path.exists() and md_path.stat().st_size > 100
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


# ---------- arXiv ID 补充查找 ----------


def _enrich_arxiv_id_from_doi(paper: dict) -> bool:
    """通过 Semantic Scholar API 用 DOI 查找 arXiv ID。"""
    doi = paper.get("doi")
    if not doi or paper.get("arxiv_id"):
        return False

    s2_key = os.environ.get("S2_API_KEY", "")
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}"
    headers = {}
    if s2_key:
        headers["x-api-key"] = s2_key

    try:
        resp = requests.get(
            url, params={"fields": "externalIds"},
            headers=headers, timeout=CONNECT_TIMEOUT,
        )
        if resp.status_code == 200:
            ext_ids = resp.json().get("externalIds") or {}
            arxiv_id = ext_ids.get("ArXiv")
            if arxiv_id:
                paper["arxiv_id"] = arxiv_id
                print(f"    [enrich] DOI→arXiv: {doi} → {arxiv_id}", file=sys.stderr)
                return True
    except requests.exceptions.RequestException:
        pass
    return False


def _enrich_arxiv_id_from_title(paper: dict) -> bool:
    """通过 arXiv API 用标题模糊匹配查找 arXiv ID。"""
    if paper.get("arxiv_id"):
        return False

    title = paper.get("title", "")
    if not title or len(title) < 10:
        return False

    import xml.etree.ElementTree as ET

    # 在词边界截断，避免 mid-word 断开导致精确匹配失败
    _STOP = {"a", "an", "the", "of", "for", "in", "on", "to", "and", "or",
             "with", "via", "by", "from", "based", "using", "its", "their"}
    words = [w for w in title.split() if w.lower() not in _STOP]
    # 取前 8 个关键词做搜索
    keywords = " ".join(words[:8])

    try:
        resp = requests.get(
            "http://export.arxiv.org/api/query",
            params={"search_query": f"all:{keywords}", "max_results": 5},
            headers={"User-Agent": USER_AGENT}, timeout=30,
        )
        if resp.status_code != 200:
            return False

        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(resp.text)
        for entry in root.findall("atom:entry", ns):
            entry_title = (entry.findtext("atom:title", "", ns) or "").strip().replace("\n", " ").lower()
            query_words = set(w.lower() for w in words)
            entry_words = set(entry_title.split())
            if not query_words:
                continue
            overlap = len(query_words & entry_words) / len(query_words)
            if overlap >= 0.6:
                entry_id = entry.findtext("atom:id", "", ns) or ""
                arxiv_id = entry_id.split("/abs/")[-1] if "/abs/" in entry_id else ""
                if arxiv_id:
                    paper["arxiv_id"] = arxiv_id
                    print(f"    [enrich] title→arXiv: '{title[:40]}...' → {arxiv_id}", file=sys.stderr)
                    return True
    except requests.exceptions.Timeout:
        print(f"    [enrich] arXiv API 超时，跳过标题搜索", file=sys.stderr)
    except Exception:
        pass
    return False


# ---------- LaTeX 辅助 ----------


def _find_main_tex(extract_dir: Path, arxiv_id: str) -> Optional[Path]:
    tex_files = list(extract_dir.rglob("*.tex"))
    if not tex_files:
        return None

    candidates = {f.name.lower(): f for f in tex_files}
    for preferred in ["main.tex", "ms.tex", "paper.tex", "article.tex",
                       f"{arxiv_id}.tex", f"{arxiv_id.replace('v1', '').replace('v2', '')}.tex"]:
        if preferred.lower() in candidates:
            return candidates[preferred.lower()]

    for tf in tex_files:
        try:
            if "\\documentclass" in tf.read_text(encoding="utf-8", errors="ignore"):
                return tf
        except Exception:
            continue
    return tex_files[0]


def _flatten_latex(tex_path: Path, base_dir: Path, depth: int = 0) -> str:
    """递归展开 \\input{} / \\include{} 指令，返回完整 LaTeX 文本。"""
    if depth > 10:
        return ""

    try:
        content = tex_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

    def _replace_input(match: re.Match) -> str:
        ref = match.group(1).strip()
        # 去掉可选参数中的扩展名后再补 .tex
        if not ref.endswith(".tex"):
            ref += ".tex"
        ref_path = base_dir / ref
        if not ref_path.exists():
            # 尝试相对于当前文件目录
            ref_path = tex_path.parent / ref
        if ref_path.exists():
            return _flatten_latex(ref_path, base_dir, depth + 1)
        return ""

    # 匹配 \input{file} 和 \include{file}（含注释行跳过）
    result = re.sub(r"(?<!%)\\input\{([^}]+)\}", _replace_input, content)
    result = re.sub(r"(?<!%)\\include\{([^}]+)\}", _replace_input, result)
    return result


# ---------- 下载通道 ----------


def try_arxiv_html(paper: dict, dest: Path) -> Optional[DownloadResult]:
    arxiv_id = paper.get("arxiv_id")
    if not arxiv_id:
        return None

    url = f"{ARXIV_HTML_BASE}/{arxiv_id}"
    try:
        head = requests.head(url, timeout=CONNECT_TIMEOUT, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
        if head.status_code != 200:
            return None
    except requests.exceptions.RequestException:
        return None

    resp = _http_get(url)
    if not resp or "text/html" not in resp.headers.get("Content-Type", ""):
        return None

    html_path = dest / "source.html"
    html_path.write_text(resp.text, encoding="utf-8")

    md_path = dest / "content.md"
    if not _pandoc_html_to_md(html_path, md_path):
        return DownloadResult(success=False, method="arxiv_html")

    quality = "poor" if md_path.read_text(encoding="utf-8").count("\n") < 50 else "good"
    return DownloadResult(
        success=True, method="arxiv_html",
        content_file="content.md", content_type="html", content_quality=quality,
    )


def try_arxiv_latex(paper: dict, dest: Path) -> Optional[DownloadResult]:
    arxiv_id = paper.get("arxiv_id")
    if not arxiv_id:
        return None

    url = f"{ARXIV_EPRINT_BASE}/{arxiv_id}"
    archive_path = dest / "source.tar.gz"
    if not _download_file(url, archive_path, max_size_mb=50):
        if archive_path.exists():
            archive_path.unlink()
        return None

    if not tarfile.is_tarfile(archive_path):
        archive_path.unlink()
        return None

    with tempfile.TemporaryDirectory() as tmp:
        try:
            with tarfile.open(archive_path) as tf:
                tf.extractall(tmp)
        except tarfile.TarError:
            archive_path.unlink()
            return None

        tmp_path = Path(tmp)
        main_tex = _find_main_tex(tmp_path, arxiv_id.split("v")[0])
        if not main_tex:
            archive_path.unlink()
            return None

        # 展开所有 \input/\include，生成完整单文件
        flat_content = _flatten_latex(main_tex, tmp_path)
        flat_path = tmp_path / "_flat_main.tex"
        if flat_content:
            flat_path.write_text(flat_content, encoding="utf-8")
        else:
            flat_path = main_tex

        md_path = dest / "content.md"
        if not _pandoc_latex_to_md(flat_path, md_path):
            # 展开失败时回退到原始文件重试
            if flat_path != main_tex and not _pandoc_latex_to_md(main_tex, md_path):
                archive_path.unlink()
                return None

    quality = "poor" if md_path.read_text(encoding="utf-8").count("\n") < 50 else "good"
    return DownloadResult(
        success=True, method="arxiv_latex",
        content_file="content.md", content_type="latex", content_quality=quality,
    )


def try_arxiv_pdf(paper: dict, dest: Path, quality: str = "fast") -> Optional[DownloadResult]:
    arxiv_id = paper.get("arxiv_id")
    if not arxiv_id:
        return None

    url = f"{ARXIV_PDF_BASE}/{arxiv_id}"
    pdf_path = dest / "source.pdf"
    if not _download_file(url, pdf_path, max_size_mb=100):
        return None

    md_text, conv_quality = pdf_to_markdown(pdf_path, quality)
    if not md_text:
        return DownloadResult(success=False, method="arxiv_pdf")

    (dest / "content.md").write_text(md_text, encoding="utf-8")
    return DownloadResult(
        success=True, method="arxiv_pdf",
        content_file="content.md", content_type="pdf", content_quality=conv_quality,
    )


def try_oa_pdf(paper: dict, dest: Path, quality: str = "fast") -> Optional[DownloadResult]:
    pdf_url = paper.get("pdf_url")
    if not pdf_url or not isinstance(pdf_url, str):
        return None

    if pdf_url.startswith(("https://doi.org/", "http://doi.org/")):
        return None

    if any(domain in pdf_url for domain in BLOCKED_DOMAINS):
        return None

    pdf_path = dest / "source.pdf"
    if not _download_file(pdf_url, pdf_path, max_size_mb=100):
        return None

    md_text, conv_quality = pdf_to_markdown(pdf_path, quality)
    if not md_text:
        return DownloadResult(success=False, method="oa_pdf")

    (dest / "content.md").write_text(md_text, encoding="utf-8")
    return DownloadResult(
        success=True, method="oa_pdf",
        content_file="content.md", content_type="pdf", content_quality=conv_quality,
    )


def try_unpaywall(paper: dict, dest: Path, email: str, quality: str = "fast") -> Optional[DownloadResult]:
    doi = paper.get("doi")
    if not doi or not email:
        return None

    url = f"{UNPAYWALL_API_BASE}/{doi}?email={email}"
    resp = _http_get(url)
    if not resp:
        return None

    data = resp.json()
    oa_url = None
    best = data.get("best_oa_location") or {}
    if best.get("url"):
        oa_url = best["url"]

    if not oa_url:
        for loc in data.get("oa_locations", []):
            if loc.get("url") and "pdf" in (loc.get("url") or "").lower():
                oa_url = loc["url"]
                break

    if not oa_url:
        return None

    if any(domain in oa_url for domain in BLOCKED_DOMAINS):
        return None

    pdf_path = dest / "source.pdf"
    if not _download_file(oa_url, pdf_path, max_size_mb=100):
        return None

    md_text, conv_quality = pdf_to_markdown(pdf_path, quality)
    if not md_text:
        return DownloadResult(success=False, method="unpaywall")

    (dest / "content.md").write_text(md_text, encoding="utf-8")
    return DownloadResult(
        success=True, method="unpaywall",
        content_file="content.md", content_type="pdf", content_quality=conv_quality,
    )
