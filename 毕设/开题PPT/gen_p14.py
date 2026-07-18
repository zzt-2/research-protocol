#!/usr/bin/env python3
"""重新生成 P14 (Ch2): 上drawio + 下左参数表 + 下右GG PDF"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
import os

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
FONT = "微软雅黑"

C_DARK = RGBColor(0x44, 0x44, 0x44)
C_MED  = RGBColor(0x66, 0x66, 0x66)
C_BLUE = RGBColor(0x2E, 0x75, 0xB6)
C_HDR  = RGBColor(0x2E, 0x75, 0xB6)
C_HDR_TEXT = RGBColor(0xFF, 0xFF, 0xFF)
C_ROW_ALT = RGBColor(0xDE, 0xEB, 0xF7)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_BORDER = RGBColor(0x9D, 0xC3, 0xE6)

IMG_DIR = "/mnt/d/code/study/research-protocol/毕设/开题报告/figures/png"
OUT_DIR = "/mnt/d/code/study/research-protocol/毕设/开题PPT"


def set_cell_text(cell, text, size=11, bold=False, color=C_DARK, alignment=1):
    """Set cell text with formatting. alignment: 0=left, 1=center, 2=right"""
    cell.text = ""
    p = cell.text_frame.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = FONT
    # Set vertical center
    cell.vertical_anchor = 1  # MSO_ANCHOR.MIDDLE


def set_cell_fill(cell, color):
    """Set cell background color"""
    tcPr = cell._tc.get_or_add_tcPr()
    solidFill = tcPr.makeelement(qn('a:solidFill'), {})
    srgbClr = solidFill.makeelement(qn('a:srgbClr'), {'val': '%02X%02X%02X' % (color[0], color[1], color[2])})
    solidFill.append(srgbClr)
    # Remove existing fill
    for existing in tcPr.findall(qn('a:solidFill')):
        tcPr.remove(existing)
    tcPr.append(solidFill)


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ── Title ──
    txBox = slide.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(12.1), Inches(0.6))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "系统链路与信道模型"
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = C_DARK
    run.font.name = FONT

    # ── Two key points (极简) ──
    txBox2 = slide.shapes.add_textbox(Inches(0.6), Inches(1.0), Inches(12.1), Inches(0.35))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    run2 = p2.add_run()
    run2.text = "• 链路预算确定 SNR 工作范围（0–20 dB）\n• Gamma-Gamma 模型描述湍流信道衰落特性"
    run2.font.size = Pt(12)
    run2.font.color.rgb = C_MED
    run2.font.name = FONT

    # ── Top: drawio 系统链路图（宽幅） ──
    drawio_path = os.path.join(IMG_DIR, "P15-Ch2-链路预算.png")
    if os.path.exists(drawio_path):
        slide.shapes.add_picture(drawio_path,
            Inches(0.5), Inches(1.5), Inches(12.3))

    # ── Bottom left: 参数表 ──
    rows, cols = 5, 4  # header + SNR row + 3 turbulence rows
    tbl_shape = slide.shapes.add_table(
        rows, cols,
        Inches(0.6), Inches(4.55),
        Inches(5.5), Inches(2.6)
    )
    tbl = tbl_shape.table

    # Set column widths
    tbl.columns[0].width = Inches(1.4)
    tbl.columns[1].width = Inches(1.2)
    tbl.columns[2].width = Inches(1.2)
    tbl.columns[3].width = Inches(1.7)

    # Header row
    headers = ["湍流等级", "α", "β", "E[1/h]"]
    for i, h in enumerate(headers):
        set_cell_text(tbl.cell(0, i), h, size=12, bold=True, color=C_HDR_TEXT)
        set_cell_fill(tbl.cell(0, i), (0x2E, 0x75, 0xB6))

    # Data rows
    data = [
        ("弱",   "4.0", "3.0", "2.00"),
        ("中",   "2.5", "1.8", "3.75"),
        ("强",   "1.5", "0.8", "+∞"),
    ]
    for r, (level, alpha, beta, e_inv) in enumerate(data, start=1):
        bg = (0xDE, 0xEB, 0xF7) if r % 2 == 1 else (0xFF, 0xFF, 0xFF)
        set_cell_text(tbl.cell(r, 0), level, size=11, bold=True, color=C_DARK)
        set_cell_fill(tbl.cell(r, 0), bg)
        for c, val in enumerate([alpha, beta, e_inv], start=1):
            set_cell_text(tbl.cell(r, c), val, size=11, color=C_DARK)
            set_cell_fill(tbl.cell(r, c), bg)

    # SNR row (merged info)
    set_cell_text(tbl.cell(4, 0), "SNR 范围", size=11, bold=True, color=C_BLUE)
    set_cell_fill(tbl.cell(4, 0), (0xDE, 0xEB, 0xF7))
    set_cell_text(tbl.cell(4, 1), "0–20", size=11, color=C_DARK)
    set_cell_fill(tbl.cell(4, 1), (0xDE, 0xEB, 0xF7))
    set_cell_text(tbl.cell(4, 2), "dB", size=11, color=C_MED)
    set_cell_fill(tbl.cell(4, 2), (0xDE, 0xEB, 0xF7))
    set_cell_text(tbl.cell(4, 3), "", size=11)
    set_cell_fill(tbl.cell(4, 3), (0xDE, 0xEB, 0xF7))

    # ── Bottom right: GG PDF 曲线 ──
    gg_path = os.path.join(IMG_DIR, "gg-pdf-three-turbulence.png")
    if os.path.exists(gg_path):
        slide.shapes.add_picture(gg_path,
            Inches(6.8), Inches(4.3), Inches(6.0))

    # ── Save ──
    out = os.path.join(OUT_DIR, "P14-Ch2-系统链路与信道模型.pptx")
    prs.save(out)
    print(f"Saved → {out}")


if __name__ == "__main__":
    main()
