#!/usr/bin/env python3
"""缩写全称一致性检查脚本。

检查 markdown 文件中的缩写是否符合写作规范：
  1. 首次出现必须有中文全称+英文全称+缩写：中文（English Full Name, ABBR）
  2. 后续出现直接用缩写，不重复给全称
  3. 不允许出现"中文（ABBR）"缺英文的形式（除非是首次定义但无英文的已知例外）

用法:
  python check-abbreviations.py <file.md>
  python check-abbreviations.py <file.md> --strict   # 将 WARNING 也视为失败
"""

import re
import sys
from collections import defaultdict

# 不需要检查的缩写
SKIP_ABBRS = {
    "NASA", "ESA", "IEEE", "CNKI", "OSA",     # 组织
    "MATLAB", "Vivado", "Xilinx",               # 工具/公司
    "TODO", "PPT",                               # 非正文
    "TB", "GB", "GS", "MS", "NS", "PS",         # 单位
    "ML", "CN", "AR",                            # 公式/数学
    "IP",                                        # FPGA 通用
}

MIN_ABBR_LEN = 2


def extract_sub_abbrs(compound):
    """从复合缩写中提取子缩写 (IM-DD → {IM, DD, IM-DD})。"""
    parts = re.split(r'[-/]', compound)
    result = {compound}
    for p in parts:
        if len(p) >= MIN_ABBR_LEN and p.isupper():
            result.add(p)
    return result


def find_all_definitions(lines):
    """扫描所有定义模式，返回结构化结果。"""
    full_defs = []       # (line_no, abbr_set, english, context)
    cn_only_defs = []    # (line_no, abbr, context)
    bare_abbrs = []      # (line_no, abbr)

    for i, line in enumerate(lines, 1):
        if line.startswith("```") or re.match(r'^\|[-\s|]+\|$', line):
            continue

        line_def_spans = []  # (start, end) of definition parentheses

        # --- 模式A: English（ABBR）如 Gamma-Gamma（GG）、Viterbi-Viterbi（VV）---
        for m in re.finditer(r'([A-Z][A-Za-z\-.]+(?:\s+[A-Za-z]+)*)\s*（([A-Z]{2,}(?:[-/][A-Z]{2,})?)）', line):
            eng_pre, abbr_raw = m.group(1).strip(), m.group(2)
            abbr_set = extract_sub_abbrs(abbr_raw)
            if abbr_raw in SKIP_ABBRS:
                continue
            ctx = line[max(0, m.start()-10):m.end()+10].strip()
            full_defs.append((i, abbr_set, eng_pre, ctx))
            line_def_spans.append((m.start(), m.end()))

        # --- 模式B: （English Full Name, ABBR）---
        for m in re.finditer(r'（([A-Z][A-Za-z\s\-/,.]+),\s*([A-Z][A-Za-z\-]{1,}(?:[-/][A-Z][A-Za-z\-]*)?)）', line):
            english, abbr_raw = m.group(1).strip(), m.group(2)
            abbr_set = extract_sub_abbrs(abbr_raw)
            if abbr_raw in SKIP_ABBRS:
                continue
            # 排除已被模式A覆盖
            if any(d[0] == i and abbr_set & d[1] for d in full_defs):
                continue
            ctx = line[max(0, m.start()-15):m.end()+15].strip()
            full_defs.append((i, abbr_set, english, ctx))
            line_def_spans.append((m.start(), m.end()))

        # --- 模式C: 中文（ABBR）缺英文 ---
        for m in re.finditer(r'[\u4e00-\u9fff]（([A-Z]{2,}(?:[/\-,]\s*[A-Z]{2,})*)）', line):
            abbr_raw = m.group(1)
            sub_abbrs = set()
            for part in re.split(r'[/\-,\s]+', abbr_raw):
                part = part.strip()
                if len(part) >= MIN_ABBR_LEN and part.isupper():
                    sub_abbrs.add(part)
            if not sub_abbrs:
                continue
            if all(a in SKIP_ABBRS for a in sub_abbrs):
                continue
            # 排除已被模式A/B覆盖
            if any(d[0] == i and sub_abbrs & d[1] for d in full_defs):
                continue
            ctx = line[max(0, m.start()-15):m.end()+15].strip()
            for a in sub_abbrs:
                cn_only_defs.append((i, a, ctx))
            line_def_spans.append((m.start(), m.end()))

        # --- 裸缩写使用 ---
        for m in re.finditer(r'\b([A-Z]{2,})\b', line):
            abbr = m.group(1)
            if abbr in SKIP_ABBRS or len(abbr) < MIN_ABBR_LEN:
                continue
            # 跳过定义括号内的
            in_span = any(s <= m.start() < e for s, e in line_def_spans)
            if in_span:
                continue
            bare_abbrs.append((i, abbr))

    return full_defs, cn_only_defs, bare_abbrs


def check(filepath):
    """执行检查，返回 (errors, warnings)。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    full_defs, cn_only_defs, bare_abbrs = find_all_definitions(lines)
    errors = []
    warnings = []

    # 索引: 缩写 → 首次完整定义
    first_def = {}
    for line_no, abbr_set, english, ctx in full_defs:
        for abbr in abbr_set:
            if abbr not in first_def:
                first_def[abbr] = (line_no, english)

    # 索引: 缩写 → 首次裸使用
    first_bare = {}
    for line_no, abbr in bare_abbrs:
        if abbr not in first_bare:
            first_bare[abbr] = line_no

    # === 检查1: 裸缩写在定义之前出现 ===
    for abbr in sorted(first_bare.keys()):
        bare_line = first_bare[abbr]
        if abbr in first_def:
            def_line, english = first_def[abbr]
            if bare_line < def_line:
                errors.append(
                    f"L{bare_line} ERROR: {abbr} 首次使用在第 {bare_line} 行，"
                    f"但定义在第 {def_line} 行（{english}）"
                )

    # === 检查2: 裸缩写无任何定义 ===
    cn_defined = {d[1] for d in cn_only_defs}
    for abbr in sorted(first_bare.keys()):
        if abbr not in first_def and abbr not in cn_defined:
            errors.append(f"L{first_bare[abbr]} ERROR: {abbr} 全文无定义")

    # === 检查3: 冗余完整定义 ===
    by_primary = defaultdict(list)
    for line_no, abbr_set, english, ctx in full_defs:
        primary = max(abbr_set, key=len)  # 最长的为主缩写
        by_primary[primary].append((line_no, english))

    for abbr in sorted(by_primary.keys()):
        entries = by_primary[abbr]
        if len(entries) > 1:
            locs = ", ".join(f"L{e[0]}" for e in entries)
            warnings.append(
                f"WARNING: {abbr} 重复定义 {len(entries)} 次 ({locs})"
            )

    # === 检查4: 中文（ABBR）缺英文 ===
    for line_no, abbr, ctx in cn_only_defs:
        if abbr in first_def:
            def_line = first_def[abbr][0]
            if line_no > def_line:
                warnings.append(
                    f"L{line_no} WARNING: {abbr} 已在 L{def_line} 定义，"
                    f"此处应直接用缩写"
                )
            else:
                errors.append(f"L{line_no} ERROR: {abbr} 定义缺英文全称: ...{ctx[:60]}...")
        else:
            errors.append(f"L{line_no} ERROR: {abbr} 定义缺英文全称: ...{ctx[:60]}...")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    filepath = sys.argv[1]
    strict = "--strict" in sys.argv

    errors, warnings = check(filepath)

    if errors:
        print(f"=== ERROR ({len(errors)}) ===")
        for e in errors:
            print(f"  {e}")

    if warnings:
        print(f"\n=== WARNING ({len(warnings)}) ===")
        for w in warnings:
            print(f"  {w}")

    if not errors and not warnings:
        print(f"全部通过: {filepath} — 0 ERROR, 0 WARNING")
    else:
        print(f"\n汇总: {len(errors)} ERROR, {len(warnings)} WARNING")

    if errors or (strict and warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
