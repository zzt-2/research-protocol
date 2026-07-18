#!/usr/bin/env python3
"""生成 Ch2/Ch3/Ch4 概述页: P14, P16, P18 (左文字+右仿真图)"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
FONT = "微软雅黑"

C_DARK = RGBColor(0x44, 0x44, 0x44)
C_MED  = RGBColor(0x66, 0x66, 0x66)
C_BLUE = RGBColor(0x2E, 0x75, 0xB6)
C_ORANGE = RGBColor(0xC5, 0x5A, 0x11)
C_IP_BLUE = RGBColor(0x1F, 0x4E, 0x79)
C_IP_ORANGE = RGBColor(0x84, 0x3C, 0x0B)

IMG_DIR = "/mnt/d/code/study/research-protocol/毕设/开题报告/figures/png"
OUT_DIR = "/mnt/d/code/study/research-protocol/毕设/开题PPT"


def add_run(paragraph, text, size=12, bold=False, color=C_MED, font_name=FONT):
    run = paragraph.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font_name
    return run


def add_title(slide, text, size=22):
    txBox = slide.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(12.1), Inches(0.8))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    add_run(p, text, size=size, bold=True, color=C_DARK)


def build_overview_slide(prs, title, sections, img_file, accent_color):
    """
    Build an overview slide with left text + right figure.

    sections: list of (label, content_lines, label_color)
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_title(slide, title)

    # Left text area
    left_x = Inches(0.6)
    left_w = Inches(7.2)
    text_top = Inches(1.3)
    line_h = 0.38  # inches per line roughly

    # Calculate total height needed
    total_lines = sum(len(lines) for _, lines, _ in sections) + len(sections) * 2
    text_block = slide.shapes.add_textbox(
        left_x, text_top, left_w, Inches(min(total_lines * line_h, 5.5))
    )
    tf = text_block.text_frame
    tf.word_wrap = True

    first = True
    for label, lines, label_color in sections:
        if not first:
            p = tf.add_paragraph()
            p.space_before = Pt(8)
        else:
            p = tf.paragraphs[0]
            first = False

        # Label (bold, colored)
        add_run(p, label, size=13, bold=True, color=label_color)

        # Content lines
        for line in lines:
            p2 = tf.add_paragraph()
            add_run(p2, line, size=12, color=C_MED)
            p2.space_after = Pt(2)

    # Right figure
    img_path = os.path.join(IMG_DIR, img_file)
    if os.path.exists(img_path):
        # Place figure on right side, vertically centered
        slide.shapes.add_picture(
            img_path,
            Inches(8.2), Inches(1.5),
            Inches(4.8)  # width only, height auto-scales
        )
    else:
        print(f"  WARNING: {img_path} not found")

    return slide


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    # ═══════════════════════════════════════
    # P14: Ch2 星地激光通信系统与信道模型
    # ═══════════════════════════════════════
    build_overview_slide(prs,
        title="建立 QPSK 相干检测系统模型与 Gamma-Gamma 湍流信道模型",
        sections=[
            ("针对问题", [
                "星地链路系统建模与湍流参数量化需求",
                "后续章节需要统一的参数基础（SNR 范围、湍流参数）",
            ], C_DARK),
            ("研究内容", [
                "① 建立 QPSK 相干检测系统模型（信号模型 + 噪声模型）",
                "② 建立 Gamma-Gamma 大气湍流信道模型",
                "③ 完成星地链路预算分析",
            ], C_DARK),
            ("输出", [
                "SNR 工作范围 + 湍流参数 (α, β) → 为 Ch3/Ch4 提供统一参数基础",
            ], C_BLUE),
        ],
        img_file="gg-pdf-three-turbulence.png",
        accent_color=C_BLUE,
    )

    # ═══════════════════════════════════════
    # P16: Ch3 大气湍流信道估计与接收性能分析
    # ═══════════════════════════════════════
    build_overview_slide(prs,
        title="对比分析估计方法精度，给出方法可用性边界与面向同步的精度设计准则",
        sections=[
            ("针对问题", [
                "信道估计误差对接收性能的量化影响尚不明确",
                "估计精度如何约束下游同步设计缺乏系统性分析",
            ], C_DARK),
            ("研究方法", [
                "① 对比 LS / MMSE / KF 信道估计方法精度",
                "② 建立估计误差级联传播模型，分析对接收性能的影响机制",
                "③ 分析 E[1/h] 发散判据与前馈方法可用性边界",
                "④ 评估调制格式灵敏度差异",
            ], C_BLUE),
            ("创新点 IP1", [
                "拟建立湍流 FSO 系统中信道估计误差对接收性能影响的量化分析框架",
                "给出面向同步的精度设计准则",
            ], C_IP_BLUE),
        ],
        img_file="NMSE灵敏度曲线.png",
        accent_color=C_BLUE,
    )

    # ═══════════════════════════════════════
    # P18: Ch4 湍流下相干接收端信号处理方法研究
    # ═══════════════════════════════════════
    build_overview_slide(prs,
        title="分析载波同步方法性能边界，建立方法选择与参数设计准则",
        sections=[
            ("针对问题", [
                "湍流下载波同步方法缺乏系统性分析与设计指导",
                "Ch3 精度设计准则约束下，同步方法的选择与参数配置尚无准则",
            ], C_DARK),
            ("三层次递进", [
                "① 分析：VV / BPS / DPLL 性能边界与失效机制（确定性交付）",
                "② 设计：分湍流条件的方法选择与参数配置准则（确定性交付）",
                "③ 探索：分析方法完整性 / 参数解析设计 / 跨模块联合处理（拟探索）",
            ], C_ORANGE),
            ("创新点 IP2", [
                "拟建立湍流下载波同步方法的性能分析框架",
                "给出分湍流条件的方法选择与参数设计准则",
            ], C_IP_ORANGE),
        ],
        img_file="ber-vv-vs-dpll.png",
        accent_color=C_ORANGE,
    )

    # ── Save ──
    out = os.path.join(OUT_DIR, "开题答辩_批量生成_Ch2-3-4概述.pptx")
    prs.save(out)
    print(f"Saved {len(prs.slides)} slides → {out}")


if __name__ == "__main__":
    main()
