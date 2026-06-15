"""论文标题一致性校验。

下载流水线把 metadata.json 的 title 写成搜索结果里的标题；但 content.md 是
从网页/PDF 转换来的，有时抓错了页面（MDPI 站点 nav 噪声、firecrawl 误抓等），
导致 metadata 标题与 content.md 实际内容完全无关（如 photonics10080914：
metadata 说是 OPLL 卫星论文，content.md 实际是石墨烯纳米二聚体）。

本模块从 content.md 提取"真标题"，与 metadata 标题做 token 重叠比对，产出
match / mismatch / unverifiable 三态。**只标记，不阻断下载**——错配论文照常
存盘，下游可 `grep title_check:mismatch` 一键定位。

设计依据（292 篇 content.md 抽样，见 .sessions/2026-06-15-read-traceability）：
- arxiv_html: 第一个带 `.ltx_title_document` class 的 H1
- arxiv_pdf/oa_pdf/unpaywall/firecrawl: nav/banner 噪声后第一个非导航 H1/H2
- arxiv_latex: content.md 里根本没有标题（pandoc 丢 \\title{}），跳过
- ~9.6% 是垃圾（1 字节空文件 / 404 页 / reCAPTCHA 墙），先检测后跳过
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

# ── 常量 ──────────────────────────────────────────────────────────────

# 决策阈值：token Jaccard <0.4 视为 mismatch。photonics 案例实测 ≈0.0；
# 0.4 是"完全不沾边"的硬下限，宽松以避免误伤正常标题变体（大小写/副标题）。
MISMATCH_THRESHOLD = 0.4

# 标题长度合理区间（字符数）。过短多半是 nav 残片，过长多半抓到了正文段。
MIN_TITLE_LEN = 15
MAX_TITLE_LEN = 300

# 垃圾 content.md 信号（先检测后跳过，避免对 1 字节空文件跑提取）
JUNK_MARKERS = (
    "404: Page Not Found",
    "Checking your browser",
    "reCAPTCHA",
    "Enable JavaScript and cookies to continue",
)
JUNK_MAX_BYTES = 3 * 1024  # <3KB 视为垃圾

# MDPI/firecrawl 等站点 nav 噪声里反复出现的 H1/H2 关键词——提取真标题时跳过。
# 来源：photonics10080914 实测 nav 块（Journals/Information/Initiatives/About/
# Notice/Article Menu/Need Help?/JSmol Viewer 等）。
NAV_KEYWORDS = {
    "journals", "information", "initiatives", "about", "notice",
    "article menu", "need help?", "jsmol viewer", "abstract",
    "introduction", "related work", "references", "conclusions",
    "share and cite", "article metrics", "cite", "share link", "share",
    "author contributions", "funding", "menu", "navigation", "search",
    "skip to main content", "table of contents",
}

# 英文停用词，token 化时剔除（与 download_channels._enrich_arxiv_id_from_title
# 的停用词表保持一致，保证与 arXiv 反查逻辑同源）。
_STOP_WORDS = {
    "a", "an", "the", "of", "for", "in", "on", "to", "and", "or",
    "with", "via", "by", "from", "based", "using", "its", "their",
    "is", "are", "was", "were", "be", "been", "as", "at", "this",
    "that", "these", "those", "it", "we", "our", "they", "them",
}


# ── token 化 + 重叠 ──────────────────────────────────────────────────

def _tokenize(text: str) -> set[str]:
    """小写化 → 取字母数字 token → 去停用词。用于标题重叠比对。"""
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return {t for t in tokens if t not in _STOP_WORDS and len(t) > 1}


def title_overlap(t1: str, t2: str) -> float:
    """两个标题的 token Jaccard 重叠率，0.0-1.0。

    任一标题 token 化后为空（如纯中文标题、纯数字）返回 0.0——
    调用方应据此判 unverifiable 而非 mismatch。
    """
    s1, s2 = _tokenize(t1), _tokenize(t2)
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


# ── 垃圾检测 ──────────────────────────────────────────────────────────

def _detect_junk(content_md_path: Path) -> Optional[str]:
    """返回垃圾原因（str）或 None。文件不存在也算垃圾。"""
    if not content_md_path.exists():
        return "file_missing"
    size = content_md_path.stat().st_size
    if size == 0:
        return "empty"
    if size < JUNK_MAX_BYTES:
        # 小文件也可能是合法短文，进一步看内容信号
        try:
            head = content_md_path.read_text(encoding="utf-8", errors="ignore")[:512]
        except OSError:
            return "unreadable"
        for marker in JUNK_MARKERS:
            if marker.lower() in head.lower():
                return f"junk_marker:{marker.split(':')[0]}"
        # 极小且无 markdown 结构，大概率是 nav 残片
        if size < JUNK_MAX_BYTES // 2 and "#" not in head:
            return "too_short_no_md"
    return None


# ── 标题提取（按下载方法分派）──────────────────────────────────────────

# arxiv_html: pandoc 把 HTML 的 <h1 class="ltx_title_document"> 转成形如
# `# Title {#id .ltx_title .ltx_title_document}` 的 H1。锚这个 class 最稳。
_ARXIV_HTML_TITLE_RE = re.compile(
    r"^#{1,2}\s+(.+?)\s*\{[^}]*\.ltx_title_document[^}]*\}\s*$",
    re.MULTILINE,
)

# 通用 H1/H2 行：`# Title` 或 `## Title`，首词大写字母开头（过滤正文小标题如
# `## 2.1 xxx`，但允许 `## A Novel ...` 这类）。
_HEADING_RE = re.compile(r"^(#{1,2})\s+(.+?)\s*$", re.MULTILINE)


def _strip_markdown_inline(text: str) -> str:
    """剥掉行内 markdown（**bold**、[link](url)、{#anchor .class}）。"""
    text = re.sub(r"\{[^}]*\}", "", text)               # pandoc 属性
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # 链接留文本
    text = re.sub(r"\*+", "", text)                     # bold/italic
    text = re.sub(r"`([^`]*)`", r"\1", text)            # code
    text = re.sub(r"\\", "", text)                      # 转义反斜杠
    return text.strip()


def _is_nav_heading(text: str) -> bool:
    """该 H1/H2 是否是 nav 噪声或正文小节标题（不是论文标题）。

    拒绝两类：
    1. nav 关键词（Journals/Information/Introduction/Abstract 等）
    2. 编号小节标题（"2. Topological Analysis"/"2.1 xxx"/"III. Method"/"Section 4"）
       —— 论文标题绝不会以这种编号开头；遇到编号开头直接当小节跳过。
    """
    low = text.lower().strip()

    # 编号小节标题：N. / N.M / N) / Section N / 罗马数字 I./II./III.
    # 注意要在去编号前判，因为 "2. related studies" 去编号后变 "related studies"
    # 会命中 nav 词表——但 "2. topological analysis" 去编号后不在词表里，漏判。
    # 所以编号开头直接判 nav，不依赖后面的词。
    if re.match(r"^(\d+(\.\d*)*\.?\s+|\d+\)\s+|section\s+\d+|[ivx]+\.\s+)", low):
        return True
    # MDPI/IEEE 转 pdf 时常见 "II\. INTRODUCTION" 全大写罗马数字
    if re.match(r"^[ivx]+\\\.\s+", low):
        return True

    # 去编号前缀后，再判整串是否 nav 词
    low = re.sub(r"^[\divvx]+\.?\s*", "", low)
    low = re.sub(r"^section\s+", "", low)
    if low in NAV_KEYWORDS:
        return True
    first_words = low.split()[:2]
    if " ".join(first_words) in NAV_KEYWORDS:
        return True
    return False


def _is_plausible_title(text: str) -> bool:
    """提取到的候选像不像真标题：长度合理 + 非纯 nav + 非纯数字。"""
    text = text.strip()
    if not (MIN_TITLE_LEN <= len(text) <= MAX_TITLE_LEN):
        return False
    if _is_nav_heading(text):
        return False
    # 纯数字/纯符号不算
    if not re.search(r"[A-Za-z]", text):
        return False
    return True


def _extract_arxiv_html(content: str) -> Optional[str]:
    """arxiv_html: 锚 .ltx_title_document class 的 H1。"""
    m = _ARXIV_HTML_TITLE_RE.search(content)
    if not m:
        return None
    title = _strip_markdown_inline(m.group(1))
    return title if _is_plausible_title(title) else None


def _extract_heading_based(content: str) -> Optional[str]:
    """通用提取：扫所有 H1/H2，跳过 nav 噪声，取第一个像标题的。

    适用 arxiv_pdf / oa_pdf / unpaywall / firecrawl。MDPI 的真标题深埋到
    ~line 193，但 nav 块全是 H2 关键词，逐个跳过后第一个 H1 就是真标题。
    """
    for m in _HEADING_RE.finditer(content):
        level, raw = m.group(1), m.group(2)
        text = _strip_markdown_inline(raw)
        if not text:
            continue
        if _is_nav_heading(text):
            continue
        if not _is_plausible_title(text):
            continue
        return text
    return None


# ── 主入口：extract + classify ────────────────────────────────────────

def extract_real_title(content_md_path: Path, method: str = "") -> dict:
    """从 content.md 提取真标题。

    返回 dict: {real_title, confidence, reason}
      - real_title: 提取到的标题 str，或 None
      - confidence: 'high' / 'low' / None
      - reason: 为什么是这个结果（人类可读，用于审计）
    """
    # arxiv_latex: content.md 里根本没有标题（pandoc 丢 \\title{}），跳过
    if method == "arxiv_latex":
        return {
            "real_title": None,
            "confidence": None,
            "reason": "arxiv_latex 不含标题（pandoc 丢 \\title{}），跳过校验",
        }

    junk = _detect_junk(content_md_path)
    if junk:
        return {
            "real_title": None,
            "confidence": None,
            "reason": f"垃圾 content.md：{junk}",
        }

    try:
        content = content_md_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {
            "real_title": None,
            "confidence": None,
            "reason": f"读取失败：{e}",
        }

    # 按方法分派
    if method == "arxiv_html":
        title = _extract_arxiv_html(content)
        if title:
            return {"real_title": title, "confidence": "high",
                    "reason": "arxiv_html: .ltx_title_document H1"}
        # 锚失败则回退通用提取
        title = _extract_heading_based(content)
        if title:
            return {"real_title": title, "confidence": "low",
                    "reason": "arxiv_html: 锚失败，回退通用 heading 提取"}
    else:
        # arxiv_pdf / oa_pdf / unpaywall / firecrawl / 未知方法
        title = _extract_heading_based(content)
        if title:
            return {"real_title": title, "confidence": "high",
                    "reason": f"{method or 'unknown'}: 通用 heading 提取"}

    return {
        "real_title": None,
        "confidence": None,
        "reason": "未找到符合标题模式的 H1/H2",
    }


def _is_invalid_metadata_title(title: str) -> Optional[str]:
    """metadata 标题本身是不是无效（URL / slug / 空串）。

    返回原因 str 或 None。这类标题不是真标题（arXiv 单篇下载 title 字段常为
    URL，manual 论文 title 常是 slug），用它做比对基准会误报 mismatch——
    content.md 本身没问题，只是基准无效。调用方应判 unverifiable。
    """
    if not title or not title.strip():
        return "empty"
    t = title.strip()
    if t.startswith(("http://", "https://", "ftp://")):
        return "url"
    # slug 特征：无空格 + 含连字符/下划线 + 含数字。
    # 真标题几乎必有空格（"A Novel Method for X"），无空格+连字符+数字 = slug
    # 典型：eydian-bipartite-2025 / network-00015 / sun-morl-2024 / GPG-VNFE。
    # 放过无空格但有冒号的（如 "GraphVNE:..." 虽无空格但有真标题结构）——
    # 实际上 "GraphVNE: Graph-Level..." 有空格，不会进这里。
    if " " not in t and ("-" in t or "_" in t) and any(c.isdigit() for c in t):
        return "slug"
    return None


def classify_mismatch(metadata_title: str, real_title_info: dict) -> dict:
    """把提取结果归类成三态。

    返回 dict: {status, overlap, real_title, reason}
      status ∈ 'match' | 'mismatch' | 'unverifiable'
    """
    real_title = real_title_info.get("real_title")
    confidence = real_title_info.get("confidence")
    reason = real_title_info.get("reason", "")

    # 提取失败 / 低置信 → unverifiable（不报 mismatch，避免误伤）
    if not real_title or confidence != "high":
        return {
            "status": "unverifiable",
            "overlap": None,
            "real_title": real_title,
            "reason": reason,
        }

    # metadata 标题本身无效（URL/slug/空）→ 基准不可信，判 unverifiable
    invalid = _is_invalid_metadata_title(metadata_title or "")
    if invalid:
        return {
            "status": "unverifiable",
            "overlap": None,
            "real_title": real_title,
            "reason": f"{reason}；metadata 标题是 {invalid}（非真标题），基准不可信",
        }

    overlap = title_overlap(metadata_title or "", real_title)

    # 任一标题 token 化为空（纯中文/纯数字）→ 无法判，标 unverifiable
    if not _tokenize(metadata_title or "") or not _tokenize(real_title):
        return {
            "status": "unverifiable",
            "overlap": overlap,
            "real_title": real_title,
            "reason": f"{reason}；标题 token 化为空（纯中文/数字），无法判重叠",
        }

    if overlap >= MISMATCH_THRESHOLD:
        return {
            "status": "match",
            "overlap": overlap,
            "real_title": real_title,
            "reason": reason,
        }

    # 缩写/首词挽救：overlap 低但两边共享一个 ≥4 字符的独特首词（缩写或核心名词）
    # 时，多半是同一篇论文的标题变体（如 "GraphVNE: Graph-Level Matching for VNE"
    # vs "GraphVNE: Graph-Level Matching for Efficient..." overlap 0.36）。
    # 挽救词必须足够独特（≥4 字符、非停用词），避免 "A"/"The"/"Method" 误挽救。
    meta_first = _first_significant_word(metadata_title or "")
    real_tokens = _tokenize(real_title)
    if meta_first and len(meta_first) >= 4 and meta_first in real_tokens:
        return {
            "status": "match",
            "overlap": overlap,
            "real_title": real_title,
            "reason": f"{reason}；overlap {overlap:.2f}<阈值 但首词『{meta_first}』挽救",
        }

    return {
        "status": "mismatch",
        "overlap": overlap,
        "real_title": real_title,
        "reason": f"{reason}；token 重叠 {overlap:.2f} < {MISMATCH_THRESHOLD}",
    }


def _first_significant_word(title: str) -> Optional[str]:
    """标题第一个有意义的词（≥4 字符、非停用词、含字母）。
    用于缩写挽救：GraphVNE / Dueling / IKENGA 这类核心名词。"""
    for tok in re.findall(r"[A-Za-z0-9]+", title):
        low = tok.lower()
        if len(low) >= 4 and low not in _STOP_WORDS and re.search(r"[A-Za-z]", tok):
            return low
    return None


# ── PDF 首页标题提取（供 blit 复用）──────────────────────────────────

def extract_pdf_firstpage_title(pdf_path: Path) -> Optional[str]:
    """用 pymupdf4llm 转 PDF 首页 → 通用 heading 提取真标题。

    供 blit._verify_pdf_title 复用——blit 只下裸 PDF，没有 content.md，
    校验时临时转首页一行 markdown。失败返回 None（调用方判 unverifiable）。
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        try:
            import pymupdf4llm
            # pymupdf4llm 不支持单页，转全文档取前若干行
            md = pymupdf4llm.to_markdown(str(pdf_path), page_ids=[0])
        except Exception:
            return None
    else:
        try:
            doc = fitz.open(str(pdf_path))
            if doc.page_count == 0:
                doc.close()
                return None
            # 取前 2 页文本（首页可能只是封面 banner）
            text = ""
            for i in range(min(2, doc.page_count)):
                page = doc[i]
                text += page.get_text("text") + "\n\n"
            doc.close()
            # 用 get_text 拿到的是纯文本无 #，套个伪 H1
            md = "# " + text.lstrip() if text.strip() else ""
        except Exception:
            return None

    if not md or not md.strip():
        return None

    # 优先按 markdown heading 提取（pymupdf4llm 路径）
    title = _extract_heading_based(md)
    if title and _is_plausible_title(title):
        return title

    # 回退：fitz 纯文本路径，取第一个非空且长度合理的行
    for line in md.splitlines():
        line = line.strip()
        if not line:
            continue
        # 跳过页码、期刊 banner残留
        if re.fullmatch(r"[\d\s]+", line):
            continue
        if _is_plausible_title(line):
            return line
    return None


def verify_pdf_title(pdf_path: Path, expected_title: str) -> dict:
    """对 PDF 做标题校验（blit 路径专用，复用 classify_mismatch 逻辑）。

    返回与 classify_mismatch 同构的 dict。
    """
    real = extract_pdf_firstpage_title(pdf_path)
    if not real:
        return {
            "status": "unverifiable",
            "overlap": None,
            "real_title": None,
            "reason": "PDF 首页标题提取失败",
        }
    info = {"real_title": real, "confidence": "high",
            "reason": "PDF 首页提取"}
    return classify_mismatch(expected_title or "", info)


# ── CLI ────────────────────────────────────────────────────────────────

def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m litdownload.title_verify",
        description="从 content.md 提取真标题并校验与 metadata 标题是否一致。",
    )
    parser.add_argument("path", type=Path,
                        help="content.md 路径，或论文目录（含 content.md + metadata.json）")
    parser.add_argument("--method", default="",
                        help="下载方法（arxiv_html/arxiv_latex/arxiv_pdf/oa_pdf/unpaywall/firecrawl_scrape）")
    parser.add_argument("--metadata-title", default=None,
                        help="metadata 标题；不传则尝试从同目录 metadata.json 读")
    args = parser.parse_args()

    target = args.path.resolve()
    if target.is_dir():
        content_md = target / "content.md"
        meta_path = target / "metadata.json"
    else:
        content_md = target
        meta_path = target.parent / "metadata.json"

    # 方法：CLI 未传则尝试从 metadata.json 读
    method = args.method
    metadata_title = args.metadata_title
    if meta_path.exists():
        try:
            import json
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            if not method:
                method = meta.get("download_method", "")
            if not metadata_title:
                metadata_title = meta.get("title", "")
        except (json.JSONDecodeError, OSError):
            pass

    real_info = extract_real_title(content_md, method)
    result = classify_mismatch(metadata_title or "", real_info)

    print(f"路径        : {content_md}")
    print(f"方法        : {method or '(未知)'}")
    print(f"metadata标题: {metadata_title or '(空)'}")
    print(f"真标题      : {result['real_title'] or '(未提取到)'}")
    print(f"状态        : {result['status']}")
    if result["overlap"] is not None:
        print(f"token重叠   : {result['overlap']:.3f}")
    print(f"原因        : {result['reason']}")


if __name__ == "__main__":
    _cli()
