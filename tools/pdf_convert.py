#!/usr/bin/env python3
"""
PDF → Markdown 转换工具。

支持分章节输出、图片提取、批量转换。
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MINERU_CLI = Path.home() / ".venvs/torch/bin/mineru"
MINERU_TIMEOUT = int(os.environ.get("MINERU_TIMEOUT", "300"))


# ---------- PDF → Markdown ----------

def pdf_to_markdown(pdf_path: Path, quality: str = "fast", output_dir: Path | None = None) -> str:
    if quality == "fast":
        import pymupdf4llm
        md_text = pymupdf4llm.to_markdown(str(pdf_path))
        if not md_text or len(md_text.strip()) < 100:
            return ""
        return md_text
    elif quality == "standard":
        return _convert_mineru(pdf_path, output_dir)
    elif quality not in ("fast", "standard"):
        raise ValueError(f"不支持的质量等级: {quality}，可选: fast, standard")
    return ""


def _convert_mineru(pdf_path: Path, output_dir: Path | None) -> str:
    """通过 MinerU CLI 子进程调用 pipeline 后端。"""
    if not MINERU_CLI.exists():
        raise FileNotFoundError(
            "未找到 mineru CLI (~/.venvs/torch/bin/mineru)，standard 质量需要 MinerU。"
            "安装: ~/.venvs/torch/bin/pip install 'mineru[pipeline]'"
        )

    dest = output_dir or pdf_path.parent
    dest.mkdir(parents=True, exist_ok=True)

    # MinerU 输出到临时目录，完成后复制结果
    with tempfile.TemporaryDirectory(prefix="mineru_") as tmpdir:
        mineru_out = Path(tmpdir) / "output"
        mineru_out.mkdir()

        print(f"  MinerU 转换中 (pipeline)...")
        result = subprocess.run(
            [
                str(MINERU_CLI), "-p", str(pdf_path.resolve()),
                "-o", str(mineru_out), "--backend", "pipeline",
            ],
            capture_output=True, text=True, timeout=MINERU_TIMEOUT,
            env={**os.environ, "MINERU_MODEL_SOURCE": os.environ.get("MINERU_MODEL_SOURCE", "modelscope")},
        )

        if result.returncode != 0:
            err = result.stderr.strip().split("\n")[-1] if result.stderr else "未知错误"
            print(f"  [WARN] MinerU 失败: {err[:200]}", file=sys.stderr)
            for line in result.stderr.strip().split("\n")[-5:]:
                print(f"    {line}", file=sys.stderr)
            return ""

        # MinerU 输出结构: <output>/<stem>/auto/<stem>.md + images/
        stem = pdf_path.stem
        auto_dir = mineru_out / stem / "auto"
        md_file = auto_dir / f"{stem}.md"
        images_src = auto_dir / "images"

        if not md_file.exists():
            # 尝试 rglob 兜底
            md_candidates = list(mineru_out.rglob("*.md"))
            if not md_candidates:
                print(f"  [WARN] MinerU 未生成 markdown", file=sys.stderr)
                return ""
            md_file = md_candidates[0]
            images_src = md_file.parent / "images"

        md_text = md_file.read_text(encoding="utf-8")

        # 复制图片到输出目录
        if images_src.exists():
            fig_dir = dest / "figures"
            fig_dir.mkdir(parents=True, exist_ok=True)
            for img in images_src.iterdir():
                if img.is_file():
                    shutil.copy2(img, fig_dir / img.name)

        return md_text


# ---------- 图片提取 ----------

def extract_figures(pdf_path: Path, output_dir: Path) -> list[Path]:
    import pymupdf

    doc = pymupdf.open(str(pdf_path))
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    extracted = []
    seen_hashes = set()

    for page_num in range(len(doc)):
        page = doc[page_num]
        for img_idx, img_info in enumerate(page.get_images(full=True)):
            xref = img_info[0]
            try:
                pix = pymupdf.Pixmap(doc, xref)
            except Exception:
                continue
            if pix.width < 100 or pix.height < 100:
                continue
            # CMYK → RGB
            if pix.n >= 5:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            # 去重（同一图片可能在多页重复引用）
            img_hash = hash(pix.samples)
            if img_hash in seen_hashes:
                continue
            seen_hashes.add(img_hash)
            fname = figures_dir / f"fig_p{page_num + 1}_{img_idx + 1}.png"
            pix.save(str(fname))
            extracted.append(fname)

    doc.close()
    return extracted


# ---------- 分章节 ----------

# 可选编号前缀：罗马数字 (I. / II.) 或阿拉伯数字 (1. / 2.)
_NUM = r"(?:(?:[IVX]+|\d+)[\.\s]+)"

SECTION_MAP = [
    ("meta", [r"(?i)^#+\s*(?:abstract|摘要)"]),
    ("intro", [rf"(?i)^#+\s*{_NUM}?(?:introduction|背景|background)"]),
    ("related", [rf"(?i)^#+\s*{_NUM}?(?:related\s+work|literature|文献综述|相关工作)"]),
    ("method", [
        rf"(?i)^#+\s*{_NUM}?(?:method|methodology|approach|proposed|framework|"
        r"system\s+model|模型|方法|算法|algorithm|problem\s+formulation|protocol\s+design)",
    ]),
    ("experiment", [
        rf"(?i)^#+\s*{_NUM}?(?:experiment|evaluation|simulation|result|numerical|"
        r"实验|仿真|结果|performance)",
    ]),
    ("discussion", [rf"(?i)^#+\s*{_NUM}?(?:discussion|讨论)"]),
    ("conclusion", [rf"(?i)^#+\s*{_NUM}?(?:conclusion|summary|future|总结|结论|展望)"]),
]

_SECTION_RE = [(key, re.compile("|".join(pats))) for key, pats in SECTION_MAP]

# 顶级章节：## I. TITLE / ## 1. TITLE / ## APPENDIX A
_TOP_SECTION_RE = re.compile(r"^##\s+(?:(?:[IVX]+|\d+)[\.\s]+|APPENDIX\s+[A-Z])")


def _classify_header(line: str) -> str | None:
    for key, pat in _SECTION_RE:
        if pat.match(line.strip()):
            return key
    return None


def _sanitize_title(line: str) -> str:
    """从标题行生成安全的文件名后缀。"""
    # 去掉 ## 前缀和编号
    title = re.sub(r"^#+\s*(?:(?:[IVX]+|\d+)[\.\s]+)?", "", line.strip())
    # 取前 3 个有意义的单词
    words = re.findall(r"[A-Za-z\u4e00-\u9fff]+", title)
    return "_".join(words[:3]).lower() if words else "section"


def chunk_markdown(md_text: str) -> dict[str, str]:
    """按论文结构拆分 markdown。"""
    lines = md_text.split("\n")

    # 找所有顶级章节边界
    boundaries: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if _TOP_SECTION_RE.match(line.strip()):
            key = _classify_header(line)
            if key is None:
                key = _sanitize_title(line)
            boundaries.append((i, key))

    if not boundaries:
        return {"content": md_text}

    result: dict[str, str] = {}

    # 首个顶级章节前的内容归入 meta（标题、摘要、关键词）
    if boundaries[0][0] > 0:
        pre = "\n".join(lines[: boundaries[0][0]]).strip()
        if pre:
            result["content_meta"] = pre

    for idx, (start, key) in enumerate(boundaries):
        end = boundaries[idx + 1][0] if idx + 1 < len(boundaries) else len(lines)
        section_text = "\n".join(lines[start:end]).strip()
        if not section_text:
            continue
        fname = f"content_{key}"
        if fname in result:
            result[fname] += "\n\n" + section_text
        else:
            result[fname] = section_text

    return result


# ---------- 统计 ----------

def _print_stats(md_text: str, file_count: int):
    lines = md_text.count("\n") + 1
    chars = len(md_text)
    print(f"  统计: {lines} 行, {chars} 字符, {file_count} 个输出文件")


# ---------- 单篇转换 ----------

def convert_single(
    pdf_path: Path,
    output_dir: Path | None = None,
    quality: str = "fast",
    chunk: bool = False,
    figures: bool = False,
) -> bool:
    if not pdf_path.exists():
        print(f"[ERROR] 文件不存在: {pdf_path}", file=sys.stderr)
        return False

    if output_dir is None:
        output_dir = pdf_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"转换: {pdf_path.name} (quality={quality})")

    try:
        md_text = pdf_to_markdown(pdf_path, quality, output_dir)
    except (ValueError, FileNotFoundError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return False
    if not md_text:
        print("  [FAIL] 转换结果为空", file=sys.stderr)
        return False

    # 图片提取（仅 fast 模式需要，MinerU 自带图片提取）
    fig_count = 0
    if figures and quality == "fast":
        figs = extract_figures(pdf_path, output_dir)
        fig_count = len(figs)
    elif quality == "standard":
        fig_count = len(list((output_dir / "figures").glob("*"))) if (output_dir / "figures").exists() else 0

    # 输出
    if chunk:
        chunks = chunk_markdown(md_text)
        if len(chunks) == 1 and "content" in chunks:
            (output_dir / "content.md").write_text(md_text, encoding="utf-8")
            print("  未检测到章节结构，输出完整 content.md")
        else:
            for fname in sorted(chunks):
                (output_dir / f"{fname}.md").write_text(chunks[fname], encoding="utf-8")
                lc = chunks[fname].count("\n") + 1
                cc = len(chunks[fname])
                print(f"  {fname}.md  ({lc} 行, {cc} 字符)")
        _print_stats(md_text, len(chunks))
    else:
        (output_dir / "content.md").write_text(md_text, encoding="utf-8")
        _print_stats(md_text, 1)

    if fig_count > 0:
        print(f"  图片: {fig_count} 张 → {output_dir / 'figures/'}")

    return True


# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(
        description="PDF → Markdown 转换工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
示例:
  %(prog)s source.pdf                       单篇转换
  %(prog)s source.pdf --chunk               分章节输出
  %(prog)s source.pdf --figures             提取图片
  %(prog)s source.pdf -o output/            指定输出目录
  %(prog)s paper-archive/xxx/ --batch       批量转换
  %(prog)s source.pdf --quality fast        质量等级（fast/standard/high）
""",
    )
    parser.add_argument("input", help="PDF 文件或目录路径")
    parser.add_argument("-o", "--output", help="输出目录（默认与源文件同目录）")
    parser.add_argument("--batch", action="store_true", help="批量转换目录下所有 PDF")
    parser.add_argument(
        "--quality",
        choices=["fast", "standard"],
        default="fast",
        help="转换质量 (默认: fast)",
    )
    parser.add_argument("--chunk", action="store_true", help="按论文结构分章节输出")
    parser.add_argument("--figures", action="store_true", help="提取图片 (>100px)")

    args = parser.parse_args()
    input_path = Path(args.input)

    if input_path.is_file():
        out = Path(args.output) if args.output else None
        ok = convert_single(input_path, out, args.quality, args.chunk, args.figures)
        sys.exit(0 if ok else 1)

    if input_path.is_dir():
        if not args.batch:
            print("[ERROR] 目录需要 --batch 参数", file=sys.stderr)
            sys.exit(1)
        pdfs = sorted(input_path.rglob("*.pdf"))
        if not pdfs:
            print(f"[ERROR] 未找到 PDF: {input_path}", file=sys.stderr)
            sys.exit(1)

        ok, fail = 0, 0
        for pdf in pdfs:
            out = Path(args.output) / pdf.stem if args.output else None
            if convert_single(pdf, out, args.quality, args.chunk, args.figures):
                ok += 1
            else:
                fail += 1
        print(f"\n批量完成: {ok} 成功, {fail} 失败")
        sys.exit(0 if fail == 0 else 1)

    print(f"[ERROR] 路径不存在: {input_path}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
