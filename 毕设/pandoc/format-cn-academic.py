#!/usr/bin/env python3
"""Post-process pandoc docx for Chinese academic formatting.

Handles: fonts, margins, header/footer, heading styles, three-line tables,
figure/table captions, display-math numbering (w:ptab), bibliography formatting.
"""

import re
import shutil
import sys
import zipfile

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

# ---- Constants ----
BODY_CN = '宋体'
BODY_EN = 'Times New Roman'
HEADING_CN = '黑体'
BODY_SIZE = Pt(12)       # 小四
SMALL_SIZE = Pt(10.5)    # 五号
LINE_SPACING = Pt(22)    # 22磅固定行距

# Equation tab stop positions (twips, relative to left margin)
_TEXT_W = 21 - 3 - 2.6  # text area width in cm
EQ_TAB_CENTER = int(Cm(_TEXT_W / 2) / 635)
EQ_TAB_RIGHT = int(Cm(_TEXT_W) / 635)


# =====================================================================
# Run / paragraph helpers
# =====================================================================

def set_run_font(run, cn_font, en_font, size, bold=False):
    """Set CJK + Western font, size, and bold on a run."""
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


def _set_raw_run_font(run_el, cn_font, en_font, size_pt):
    """Set font on a raw w:r OxmlElement (no python-docx Run wrapper)."""
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:eastAsia'), cn_font)
    rFonts.set(qn('w:ascii'), en_font)
    rFonts.set(qn('w:hAnsi'), en_font)
    rPr.append(rFonts)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(int(size_pt * 2)))
    rPr.append(sz)
    run_el.insert(0, rPr)


def set_space_lines(para, before_lines=None, after_lines=None):
    """Set before/after spacing in line units (100 = 1 line)."""
    pPr = para._element.get_or_add_pPr()
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        pPr.append(spacing)
    if before_lines is not None:
        spacing.set(qn('w:beforeLines'), str(before_lines))
        if spacing.get(qn('w:before')) is not None:
            del spacing.attrib[qn('w:before')]
    if after_lines is not None:
        spacing.set(qn('w:afterLines'), str(after_lines))
        if spacing.get(qn('w:after')) is not None:
            del spacing.attrib[qn('w:after')]


def set_space_after_half_line(para):
    """Set space after to 0.5 lines via w:afterLines."""
    pPr = para._element.get_or_add_pPr()
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        spacing = OxmlElement('w:spacing')
        pPr.append(spacing)
    spacing.set(qn('w:afterLines'), '50')
    if spacing.get(qn('w:after')) is not None:
        del spacing.attrib[qn('w:after')]


# =====================================================================
# Paragraph classification
# =====================================================================

def get_heading_level(para):
    s = para.style.name if para.style else ''
    for i in range(1, 5):
        if s == f'Heading {i}' or s == str(i):
            return i
    return 0


def is_heading(para):
    s = para.style.name if para.style else ''
    return 'Heading' in s


def is_caption(para):
    s = para.style.name if para.style else ''
    if 'Caption' in s:
        return True
    t = para.text.strip()
    return (t.startswith('图') or t.startswith('表')) and len(t) < 80


def has_display_math(para):
    return para._element.find('.//' + qn('m:oMathPara')) is not None


def has_image(para):
    return para._element.find('.//' + qn('w:drawing')) is not None


def is_bibliography(para):
    s = para.style.name if para.style else ''
    if 'Bibliography' in s or 'bibliography' in s.lower():
        return True
    t = para.text.strip()
    return t and t[0] == '[' and len(t) > 2 and t[1].isdigit()


# =====================================================================
# Display math: oMathPara → oMath + w:ptab numbering
# =====================================================================

def _convert_omathpara_to_omath(p_elem):
    """Convert m:oMathPara (display) to m:oMath (inline) for ptab compatibility."""
    omathpara = p_elem.find(qn('m:oMathPara'))
    if omathpara is None:
        omathpara = p_elem.find('.//' + qn('m:oMathPara'))
    if omathpara is None:
        return None
    omath_children = omathpara.findall(qn('m:oMath'))
    if not omath_children:
        return None
    idx = list(p_elem).index(omathpara)
    p_elem.remove(omathpara)
    for i, omath in enumerate(omath_children):
        p_elem.insert(idx + i, omath)
    return omath_children[0]


def _make_tab_char_run():
    """Create a w:r containing a w:tab character."""
    run_el = OxmlElement('w:r')
    run_el.append(OxmlElement('w:tab'))
    return run_el


def _setup_eq_tab_stops(pPr, center_twips, right_twips):
    """Set center + right tab stops on paragraph properties."""
    old_tabs = pPr.find(qn('w:tabs'))
    if old_tabs is not None:
        pPr.remove(old_tabs)
    tabs = OxmlElement('w:tabs')
    ct = OxmlElement('w:tab')
    ct.set(qn('w:val'), 'center')
    ct.set(qn('w:pos'), str(center_twips))
    tabs.append(ct)
    rt = OxmlElement('w:tab')
    rt.set(qn('w:val'), 'right')
    rt.set(qn('w:pos'), str(right_twips))
    tabs.append(rt)
    pPr.append(tabs)


def _make_text_run(text, cn_font, en_font, size_pt):
    """Create a w:r OxmlElement with font styling and text content."""
    run_el = OxmlElement('w:r')
    _set_raw_run_font(run_el, cn_font, en_font, size_pt)
    t_el = OxmlElement('w:t')
    t_el.text = text
    run_el.append(t_el)
    return run_el


# =====================================================================
# Table formatting
# =====================================================================

def _make_border_el(name, val, sz, color='000000'):
    el = OxmlElement(f'w:{name}')
    el.set(qn('w:val'), val)
    el.set(qn('w:sz'), sz)
    el.set(qn('w:space'), '0')
    el.set(qn('w:color'), color)
    return el


def set_three_line_table(table):
    """三线表: top/bottom 1.5pt, header separator 0.75pt, no other borders."""
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)

    # Center table
    jc = tblPr.find(qn('w:jc'))
    if jc is None:
        jc = OxmlElement('w:jc')
        tblPr.append(jc)
    jc.set(qn('w:val'), 'center')

    # Table-level borders: all none
    existing = tblPr.find(qn('w:tblBorders'))
    if existing is not None:
        tblPr.remove(existing)
    borders = OxmlElement('w:tblBorders')
    for name in ['top', 'bottom', 'left', 'right', 'insideV', 'insideH']:
        borders.append(_make_border_el(name, 'none', '0', 'auto'))
    tblPr.append(borders)

    # Auto-fit width
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is None:
        tblW = OxmlElement('w:tblW')
        tblPr.append(tblW)
    tblW.set(qn('w:w'), '0')
    tblW.set(qn('w:type'), 'auto')

    nrows = len(table.rows)
    for ri, row in enumerate(table.rows):
        for cell in row.cells:
            tc = cell._element
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is None:
                tcPr = OxmlElement('w:tcPr')
                tc.insert(0, tcPr)
            tcBorders = tcPr.find(qn('w:tcBorders'))
            if tcBorders is not None:
                tcPr.remove(tcBorders)
            tcBorders = OxmlElement('w:tcBorders')
            tcBorders.append(_make_border_el('left', 'none', '0', 'auto'))
            tcBorders.append(_make_border_el('right', 'none', '0', 'auto'))
            if ri == 0:
                tcBorders.append(_make_border_el('top', 'single', '12'))
            else:
                tcBorders.append(_make_border_el('top', 'none', '0', 'auto'))
            if ri == 0:
                tcBorders.append(_make_border_el('bottom', 'single', '6'))
            elif ri == nrows - 1:
                tcBorders.append(_make_border_el('bottom', 'single', '12'))
            else:
                tcBorders.append(_make_border_el('bottom', 'none', '0', 'auto'))
            tcPr.append(tcBorders)


def clear_cell_inherits(para):
    """Clear inherited body-text formatting from a table cell paragraph."""
    pf = para.paragraph_format
    pf.first_line_indent = Pt(0)
    pf.left_indent = Pt(0)
    pf.space_before = Pt(2)
    pf.space_after = Pt(2)
    pf.line_spacing = Pt(18)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY


# =====================================================================
# Bibliography
# =====================================================================

def strip_hyperlinks(para):
    """Flatten w:hyperlink elements to plain runs."""
    p = para._element
    for hl in p.findall(qn('w:hyperlink')):
        runs = hl.findall(qn('w:r'))
        idx = list(p).index(hl)
        for i, run in enumerate(runs):
            p.insert(idx + i, run)
        p.remove(hl)


def clean_hyperlink_style(run):
    """Remove blue color, underline, and hyperlink rStyle from a run."""
    rpr = run._element.find(qn('w:rPr'))
    if rpr is None:
        return
    for tag in ['w:rStyle', 'w:u', 'w:color']:
        el = rpr.find(qn(tag))
        if el is not None:
            rpr.remove(el)


def _bib_num(para):
    """Extract [N] citation number from a bibliography paragraph."""
    m = re.match(r'\[(\d+)\]', para.text.strip())
    return int(m.group(1)) if m else None


def format_bibliography(bib_entries):
    """Format bibliography entries: 五号, 悬挂缩进, aligned numbers."""
    if not bib_entries:
        return
    max_num = max(_bib_num(p) or 0 for p in bib_entries)
    max_digits = len(str(max_num))
    prefix_chars = max_digits + 3  # [NN] + space
    indent_pt = prefix_chars * SMALL_SIZE.pt * 0.55
    indent = Pt(indent_pt)

    for para in bib_entries:
        strip_hyperlinks(para)
        for run in para.runs:
            set_run_font(run, BODY_CN, BODY_EN, SMALL_SIZE)
            clean_hyperlink_style(run)

        num = _bib_num(para)
        if num is not None:
            padding = max_digits - len(str(num))
            if padding > 0 and len(para.runs) > 1:
                para.runs[1].text = ' ' * (1 + padding)

        pf = para.paragraph_format
        pf.line_spacing = Pt(22)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        pf.left_indent = indent
        pf.first_line_indent = Pt(-indent_pt)

        pPr = para._element.get_or_add_pPr()
        tabs = pPr.find(qn('w:tabs'))
        if tabs is None:
            tabs = OxmlElement('w:tabs')
            pPr.append(tabs)
        tab = OxmlElement('w:tab')
        tab.set(qn('w:val'), 'left')
        tab.set(qn('w:pos'), str(int(indent_pt * 12700)))
        tabs.append(tab)


# =====================================================================
# Style management
# =====================================================================

def _ensure_style(doc, name, base_name='Normal', cn_font=BODY_CN, en_font=BODY_EN,
                  size=SMALL_SIZE, first_indent=0, left_indent=0, alignment=None,
                  line_spacing=22, hanging_indent=None):
    """Get or create a paragraph style with specified formatting."""
    try:
        return doc.styles[name]
    except KeyError:
        style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.base_style = doc.styles[base_name]
        style.font.name = en_font
        style.font.size = size
        rpr = style.element.find(qn('w:rPr'))
        if rpr is None:
            rpr = OxmlElement('w:rPr')
            style.element.append(rpr)
        rFonts = rpr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = OxmlElement('w:rFonts')
            rpr.insert(0, rFonts)
        rFonts.set(qn('w:eastAsia'), cn_font)
        rFonts.set(qn('w:ascii'), en_font)
        rFonts.set(qn('w:hAnsi'), en_font)
        pPr = style.element.find(qn('w:pPr'))
        if pPr is None:
            pPr = OxmlElement('w:pPr')
            style.element.append(pPr)
        ind = pPr.find(qn('w:ind'))
        if ind is None:
            ind = OxmlElement('w:ind')
            pPr.append(ind)
        if hanging_indent:
            emu = int(hanging_indent * 12700 / 20)
            ind.set(qn('w:left'), str(emu))
            ind.set(qn('w:hanging'), str(emu))
        else:
            ind.set(qn('w:firstLine'), str(int(first_indent * 12700 / 20)))
            if left_indent:
                ind.set(qn('w:left'), str(int(left_indent * 12700 / 20)))
        if alignment is not None:
            jc = pPr.find(qn('w:jc'))
            if jc is None:
                jc = OxmlElement('w:jc')
                pPr.append(jc)
            jc.set(qn('w:val'), alignment)
        spacing = pPr.find(qn('w:spacing'))
        if spacing is None:
            spacing = OxmlElement('w:spacing')
            pPr.append(spacing)
        spacing.set(qn('w:line'), str(int(line_spacing * 20)))
        spacing.set(qn('w:lineRule'), 'exact')
        return style


# =====================================================================
# Page setup: header / footer
# =====================================================================

def _setup_header(section):
    """Set header: '北京理工大学本科生毕业设计（论文）', 宋体四号居中."""
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    hp.clear()
    hr = hp.add_run('北京理工大学本科生毕业设计（论文）')
    set_run_font(hr, BODY_CN, BODY_EN, Pt(14))
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    hp_fmt = hp.paragraph_format
    hp_fmt.space_before = Pt(0)
    hp_fmt.space_after = Pt(0)
    # 字间距加宽 0.5 磅 (twentieths of a point)
    rPr = hr._element.get_or_add_rPr()
    cs = rPr.find(qn('w:spacing'))
    if cs is None:
        cs = OxmlElement('w:spacing')
        rPr.append(cs)
    cs.set(qn('w:val'), '10')
    # Bottom border
    pPr = hp._element.get_or_add_pPr()
    pBdr = pPr.find(qn('w:pBdr'))
    if pBdr is not None:
        pPr.remove(pBdr)
    pBdr = OxmlElement('w:pBdr')
    bdr = OxmlElement('w:bottom')
    bdr.set(qn('w:val'), 'single')
    bdr.set(qn('w:sz'), '6')
    bdr.set(qn('w:space'), '1')
    bdr.set(qn('w:color'), '000000')
    pBdr.append(bdr)
    pPr.append(pBdr)


def _setup_footer(section):
    """Set footer: centered PAGE field, 宋体五号."""
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    fp.clear()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp_fmt = fp.paragraph_format
    fp_fmt.first_line_indent = Pt(0)
    fp_fmt.left_indent = Pt(0)
    fp_fmt.space_before = Pt(0)
    fp_fmt.space_after = Pt(0)
    for fld_type in ['begin', 'instrText', 'separate', 'text', 'end']:
        r = fp.add_run('1' if fld_type == 'text' else None)
        set_run_font(r, BODY_CN, BODY_EN, SMALL_SIZE)
        if fld_type in ('begin', 'separate', 'end'):
            fc = OxmlElement('w:fldChar')
            fc.set(qn('w:fldCharType'), fld_type)
            r._element.append(fc)
        elif fld_type == 'instrText':
            it = OxmlElement('w:instrText')
            it.set(qn('xml:space'), 'preserve')
            it.text = ' PAGE '
            r._element.append(it)


# =====================================================================
# Main processing
# =====================================================================

def main(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    doc = Document(input_path)

    # Ensure custom styles exist
    cap_style = _ensure_style(doc, 'Caption')
    fig_style = doc.styles['图片'] if '图片' in [s.name for s in doc.styles] else None
    bib_style = _ensure_style(doc, '参考文献', size=SMALL_SIZE, line_spacing=22,
                               hanging_indent=28.9)

    prev_display_math = False
    in_bibliography = False
    bib_entries = []
    current_chapter = 0
    table_counter = 0
    eq_counter = 0

    for para in doc.paragraphs:
        # --- Heading ---
        if is_heading(para):
            t = para.text.strip()
            if '参考文献' in t or 'Reference' in t:
                in_bibliography = True
            level = get_heading_level(para)
            if level == 1:
                h_size, h_align = Pt(16), WD_ALIGN_PARAGRAPH.CENTER
                h_before, h_after = 50, 100
                current_chapter += 1
                table_counter = 0
                eq_counter = 0
            elif level == 2:
                h_size, h_align = Pt(14), WD_ALIGN_PARAGRAPH.LEFT
                h_before, h_after = 50, 0
            else:
                h_size, h_align = Pt(12), WD_ALIGN_PARAGRAPH.LEFT
                h_before, h_after = 50, 0
            for run in para.runs:
                set_run_font(run, HEADING_CN, BODY_EN, h_size, bold=True)
            pf = para.paragraph_format
            pf.alignment = h_align
            pf.first_line_indent = Pt(0)
            pf.left_indent = Pt(0)
            set_space_lines(para, before_lines=h_before, after_lines=h_after)
            pf.line_spacing = 1.5
            prev_display_math = False
            continue

        # --- Bibliography ---
        if in_bibliography or is_bibliography(para):
            in_bibliography = True
            if bib_style:
                para.style = bib_style
            bib_entries.append(para)
            prev_display_math = False
            continue

        # --- Table/Figure caption ---
        if is_caption(para):
            t = para.text.strip()
            if t.startswith('表 '):
                table_counter += 1
                caption_text = re.sub(r'^表\s*', '', t)
                new_text = f'表 {current_chapter}-{table_counter} {caption_text}'
                for i, run in enumerate(para.runs):
                    run.text = new_text if i == 0 else ''
            para.style = cap_style
            for run in para.runs:
                set_run_font(run, BODY_CN, BODY_EN, SMALL_SIZE)
            pf = para.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.first_line_indent = Pt(0)
            pf.left_indent = Pt(0)
            pf.line_spacing = LINE_SPACING
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            set_space_after_half_line(para)
            pf.space_before = Pt(0)
            prev_display_math = False
            continue

        # --- Figure (image paragraph) ---
        if has_image(para):
            if fig_style:
                para.style = fig_style
            for run in para.runs:
                run.font.bold = False
            pf = para.paragraph_format
            pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.first_line_indent = Pt(0)
            pf.left_indent = Pt(0)
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            pf.space_after = Pt(6)
            pf.space_before = Pt(6)
            prev_display_math = False
            continue

        # --- Body text (with possible display math) ---
        for run in para.runs:
            set_run_font(run, BODY_CN, BODY_EN, BODY_SIZE)

        pf = para.paragraph_format
        if has_display_math(para):
            eq_counter += 1
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.first_line_indent = Pt(0)
            pf.left_indent = Pt(0)
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            pf.space_after = Pt(6)
            pf.space_before = Pt(0)
            omath = _convert_omathpara_to_omath(para._element)
            if omath is not None:
                pPr = para._element.get_or_add_pPr()
                _setup_eq_tab_stops(pPr, EQ_TAB_CENTER, EQ_TAB_RIGHT)
                omath.addprevious(_make_tab_char_run())
                right_tab = _make_tab_char_run()
                omath.addnext(right_tab)
                right_tab.addnext(
                    _make_text_run(f'({current_chapter}-{eq_counter})',
                                   BODY_CN, BODY_EN, BODY_SIZE.pt)
                )
            prev_display_math = True
        else:
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf.line_spacing = LINE_SPACING
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            set_space_after_half_line(para)
            pf.space_before = Pt(0)
            if prev_display_math:
                pf.first_line_indent = Pt(0)
            prev_display_math = False

    # Bibliography batch formatting
    format_bibliography(bib_entries)

    # Tables: three-line borders + cell formatting
    tbl_style = doc.styles['表格'] if '表格' in [s.name for s in doc.styles] else None
    for table in doc.tables:
        set_three_line_table(table)
        for ri, row in enumerate(table.rows):
            for cell in row.cells:
                for para in cell.paragraphs:
                    if tbl_style:
                        para.style = tbl_style
                    cn_font = HEADING_CN if ri == 0 else BODY_CN
                    for run in para.runs:
                        set_run_font(run, cn_font, BODY_EN, SMALL_SIZE)
                    clear_cell_inherits(para)

    # Page setup + header/footer
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(3.5)
        section.bottom_margin = Cm(2.6)
        section.left_margin = Cm(3)
        section.right_margin = Cm(2.6)
        section.header_distance = Cm(2.4)
        section.footer_distance = Cm(2.0)
        section.gutter = Cm(0)
        _setup_header(section)
        _setup_footer(section)

    doc.save(output_path)
    _clean_rels(output_path)
    print(f"Formatted: {output_path}")


def _clean_rels(path):
    """Remove orphan hyperlink relationships from word/_rels/document.xml.rels."""
    tmp = path + '.tmp'
    with zipfile.ZipFile(path, 'r') as zin:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'word/_rels/document.xml.rels':
                    text = data.decode('utf-8')
                    cleaned = re.sub(
                        r'<Relationship[^>]*Type="[^"]*hyperlink"[^>]*/>\s*',
                        '', text
                    )
                    data = cleaned.encode('utf-8')
                zout.writestr(item, data)
    shutil.move(tmp, path)


if __name__ == '__main__':
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else inp
    main(inp, out)
