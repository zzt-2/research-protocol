#!/usr/bin/env python3
"""Post-process pandoc docx for Chinese academic formatting.

Based on BIThesis template specs:
  Body:      宋体/TNR, 小四(12pt), 22磅行距, 段后0.5行(afterLines)
  Caption:   宋体/TNR, 五号(10.5pt), 居中
  Figure:    居中, 单倍行距
  Display:   math 单倍行距; inline math keeps body spacing
  Table:     三线表, 宋体/TNR, 五号(10.5pt), 单元格无缩进
  Reference: 五号(10.5pt), 悬挂缩进2字符(21pt)
  Heading:   黑体/TNR
"""

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import sys

# ---- Constants ----
BODY_CN = '宋体'
BODY_EN = 'Times New Roman'
HEADING_CN = '黑体'
BODY_SIZE = Pt(12)       # 小四
SMALL_SIZE = Pt(10.5)    # 五号
LINE_SPACING = Pt(22)    # 22磅固定行距
HANG_INDENT = Pt(21)     # 悬挂缩进2字符 (2 × 10.5pt)


def set_run_font(run, cn_font, en_font, size, bold=False):
    run.font.name = en_font
    run.font.size = size
    run.font.bold = bold
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:eastAsia'), cn_font)
        rFonts.set(qn('w:ascii'), en_font)
        rFonts.set(qn('w:hAnsi'), en_font)
        rPr.insert(0, rFonts)
    else:
        rFonts.set(qn('w:eastAsia'), cn_font)
        rFonts.set(qn('w:ascii'), en_font)
        rFonts.set(qn('w:hAnsi'), en_font)


def set_space_after_half_line(para):
    """Set space after to 0.5 lines using w:afterLines (not pt)."""
    pPr = para._element.get_or_add_pPr()
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        pPr.append(spacing)
    spacing.set(qn('w:afterLines'), '50')  # 50 = 0.5 × 100
    # Remove conflicting pt-based after
    if spacing.get(qn('w:after')) is not None:
        del spacing.attrib[qn('w:after')]


def has_display_math(para):
    return para._element.find('.//' + qn('m:oMathPara')) is not None


def is_heading(para):
    s = para.style.name if para.style else ''
    return 'Heading' in s


def is_caption(para):
    s = para.style.name if para.style else ''
    if 'Caption' in s:
        return True
    t = para.text.strip()
    if (t.startswith('图') or t.startswith('表')) and len(t) < 80:
        return True
    return False


def has_image(para):
    return para._element.find('.//' + qn('w:drawing')) is not None


def is_bibliography(para):
    s = para.style.name if para.style else ''
    if 'Bibliography' in s or 'bibliography' in s.lower():
        return True
    t = para.text.strip()
    if t and t[0] == '[' and len(t) > 2 and t[1].isdigit():
        return True
    return False


def clear_cell_inherits(para):
    """Clear body-text inherited formatting from table cell paragraph."""
    pf = para.paragraph_format
    pf.first_line_indent = Pt(0)
    pf.left_indent = Pt(0)
    pf.space_before = Pt(2)
    pf.space_after = Pt(2)
    pf.line_spacing = Pt(18)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY


def set_three_line_table(table):
    """三线表: top/bottom thick (1.5pt), first-row-bottom thin (0.75pt), no vertical."""
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)

    # Table centered on page
    jc = tblPr.find(qn('w:jc'))
    if jc is None:
        jc = OxmlElement('w:jc')
        tblPr.append(jc)
    jc.set(qn('w:val'), 'center')

    # Borders
    existing = tblPr.find(qn('w:tblBorders'))
    if existing is not None:
        tblPr.remove(existing)

    borders = OxmlElement('w:tblBorders')
    for name, sz in [('top', '12'), ('bottom', '12')]:
        el = OxmlElement(f'w:{name}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), sz)
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), '000000')
        borders.append(el)
    for name in ['left', 'right', 'insideV', 'insideH']:
        el = OxmlElement(f'w:{name}')
        el.set(qn('w:val'), 'none')
        el.set(qn('w:sz'), '0')
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), 'auto')
        borders.append(el)
    tblPr.append(borders)

    # Auto-fit width
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None:
        tblW = OxmlElement('w:tblW')
        tblPr.append(tblW)
    tblW.set(qn('w:w'), '0')
    tblW.set(qn('w:type'), 'auto')

    # First row: thin bottom border only (don't force bold — source decides)
    if len(table.rows) > 0:
        for cell in table.rows[0].cells:
            tc = cell._element
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is None:
                tcPr = OxmlElement('w:tcPr')
                tc.insert(0, tcPr)
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is None:
                tcBorders = OxmlElement('w:tcBorders')
                tcPr.append(tcBorders)
            old = tcBorders.find(qn('w:bottom'))
            if old is not None:
                tcBorders.remove(old)
            b = OxmlElement('w:bottom')
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), '6')
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), '000000')
            tcBorders.append(b)


def main(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    doc = Document(input_path)
    prev_display_math = False
    in_bibliography = False

    for para in doc.paragraphs:
        # Heading
        if is_heading(para):
            t = para.text.strip()
            if '参考文献' in t or 'Reference' in t:
                in_bibliography = True
            for run in para.runs:
                set_run_font(run, HEADING_CN, BODY_EN, run.font.size or Pt(14))
            prev_display_math = False
            continue

        # Bibliography entries: 悬挂缩进2字符
        if in_bibliography or is_bibliography(para):
            in_bibliography = True
            for run in para.runs:
                set_run_font(run, BODY_CN, BODY_EN, SMALL_SIZE)
            pf = para.paragraph_format
            pf.line_spacing = Pt(22)
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.space_after = Pt(0)
            pf.space_before = Pt(0)
            pf.left_indent = HANG_INDENT
            pf.first_line_indent = Pt(-HANG_INDENT.pt)  # negative = hanging
            prev_display_math = False
            continue

        # Caption
        if is_caption(para):
            for run in para.runs:
                set_run_font(run, BODY_CN, BODY_EN, SMALL_SIZE)
            pf = para.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.line_spacing = LINE_SPACING
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            set_space_after_half_line(para)
            pf.space_before = Pt(0)
            prev_display_math = False
            continue

        # Figure
        if has_image(para):
            for run in para.runs:
                run.font.bold = False
            pf = para.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            pf.space_after = Pt(6)
            pf.space_before = Pt(6)
            prev_display_math = False
            continue

        # Body text
        for run in para.runs:
            set_run_font(run, BODY_CN, BODY_EN, BODY_SIZE)

        pf = para.paragraph_format
        if has_display_math(para):
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            pf.space_after = Pt(6)
            pf.space_before = Pt(0)
            prev_display_math = True
        else:
            pf.line_spacing = LINE_SPACING
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            set_space_after_half_line(para)
            pf.space_before = Pt(0)
            if prev_display_math:
                pf.first_line_indent = Pt(0)
            prev_display_math = False

    # Tables: three-line borders + independent cell formatting
    for table in doc.tables:
        set_three_line_table(table)
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        set_run_font(run, BODY_CN, BODY_EN, SMALL_SIZE)
                    clear_cell_inherits(para)

    doc.save(output_path)
    print(f"Formatted: {output_path}")


if __name__ == '__main__':
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp
    main(inp, out)
