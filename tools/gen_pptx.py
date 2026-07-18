#!/usr/bin/env python3
"""从 JSON 内容定义 + 北理 PPT 模板生成答辩 PPT。

核心思路：克隆模板中的示例幻灯片，替换文字内容。这样保留所有装饰元素。

用法:
    python tools/gen_pptx.py --content slides.json
    python tools/gen_pptx.py --example   # 用示例内容测试
"""

import argparse
import copy
import json
import sys

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Pt


# ── 模板中用作母版的示例幻灯片索引（0-based）── ──────────
TEMPLATE_SLIDES = {
    "cover":     2,    # 封面样式1-首页
    "end":       3,    # 封面样式1-尾页
    "toc":       22,   # 目录样式1
    "section":   14,   # 封面样式6（章节分隔）
    # 内页内容布局（全部基于内页样式1，标题位置统一）
    "一段文字":     66,
    "两段文字":     69,
    "观点对比":     72,
    "三个观点":     78,
    "四个观点":     79,
    "五个观点":     83,
    "六个观点":     85,
    "参考文献":     86,   # TABLE
    "人物介绍":     87,   # IMG
    "两人介绍":     90,   # IMG
    "多人介绍":     91,   # IMG
    "框架图":       93,
    "一段一图":     94,   # IMG
    "一段一图式":   98,   # IMG
    "一段二图":     99,   # IMG
    "一段四图":     103,  # IMG
    "二段二图":     104,  # IMG
    "三段一图":     105,  # IMG
    "三段三图":     106,  # IMG
    "四段四图":     109,  # IMG
    "五段五图":     110,  # IMG
    "四段时间轴":   111,
    "五段时间轴":   112,
    "数据表格":     114,  # TABLE
    "数据对比":     116,
    "折线图":       117,
    "柱状图分析":   118,
    "柱状图对比":   119,
    "饼图":         122,
}

ORIGINAL_SLIDE_COUNT = 362  # 模板原幻灯片数


def clone_slide(prs: Presentation, src_idx: int):
    """克隆指定幻灯片，返回新幻灯片对象。"""
    src = prs.slides[src_idx]
    layout = src.slide_layout
    dst = prs.slides.add_slide(layout)

    # 删除新幻灯片默认生成的占位符
    for sp in list(dst.shapes._spTree):
        if sp.tag == qn("p:sp") or sp.tag == qn("p:pic") or sp.tag == qn("p:grpSp") or sp.tag == qn("p:cxnSp"):
            dst.shapes._spTree.remove(sp)

    # 深拷贝源幻灯片所有 shape（跳过 nvGrpSpPr 和 grpSpPr）
    skip_tags = {qn("p:nvGrpSpPr"), qn("p:grpSpPr")}
    for el in src.shapes._spTree:
        if el.tag not in skip_tags:
            dst.shapes._spTree.append(copy.deepcopy(el))

    return dst


def remove_original_slides(prs: Presentation, keep: int):
    """删除前 keep 张之后的所有幻灯片，保留后 keep 张（新生成的）。"""
    slide_list = prs.slides._sldIdLst
    ids = list(slide_list)
    for sldId in ids[:-keep]:
        slide_list.remove(sldId)


# ── 文本写入工具 ────────────────────────────────────────

def set_run_text(para, text: str, font_size_pt: int | None = None, bold: bool | None = None):
    """清空段落，写入单个 run。"""
    for run in list(para.runs):
        run._r.getparent().remove(run._r)
    para._p.text = ""
    run = para.add_run()
    run.text = text
    if font_size_pt:
        run.font.size = Pt(font_size_pt)
    if bold is not None:
        run.font.bold = bold
    return run


def _enable_shrink(shape):
    """启用文本自动缩小以适应形状。"""
    if not shape.has_text_frame:
        return
    bodyPr = shape.text_frame._txBody.find(qn("a:bodyPr"))
    bodyPr.set("anchor", "t")
    # 移除旧设置
    for tag in ["normAutofit", "spAutoFit"]:
        el = bodyPr.find(qn(f"a:{tag}"))
        if el is not None:
            bodyPr.remove(el)
    # 添加 spAutoFit（PowerPoint 自动缩小）
    etree.SubElement(bodyPr, qn("a:spAutoFit"))


def set_shape_text(shape, text: str, font_size_pt: int | None = None, bold: bool | None = None):
    """替换 shape 的全部文本为单段单行。"""
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    set_run_text(tf.paragraphs[0], text, font_size_pt, bold)
    _enable_shrink(shape)


def set_shape_lines(shape, lines: list[str], font_size_pt: int | None = None, bold: bool | None = None, shrink: bool = True):
    """替换 shape 的全部文本为多行。"""
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    # 清空所有段落
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    for i, line in enumerate(lines):
        if i == 0:
            para = tf.paragraphs[0]
        else:
            para = tf.add_paragraph()
        set_run_text(para, line, font_size_pt, bold)
    if shrink:
        _enable_shrink(shape)


def set_shape_bullets(shape, points: list[str], font_size_pt: int = 12):
    """写入带项目符号的要点列表。"""
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    tf.word_wrap = True
    # 清空
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    for i, point in enumerate(points):
        if i == 0:
            para = tf.paragraphs[0]
        else:
            para = tf.add_paragraph()
        # 确保有项目符号
        pPr = para._p.get_or_add_pPr()
        buNone = pPr.find(qn("a:buNone"))
        if buNone is not None:
            pPr.remove(buNone)
        buChar = pPr.find(qn("a:buChar"))
        if buChar is None:
            buChar = etree.SubElement(pPr, qn("a:buChar"))
        buChar.set("char", "•")
        set_run_text(para, point, font_size_pt)
    _enable_shrink(shape)


def find_shapes_with_text(slide, min_chars: int = 0):
    """返回所有有文本的 shape 列表，按 top 位置排序。"""
    result = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            txt = (shape.text_frame.text or "").strip()
            if len(txt) >= min_chars:
                result.append(shape)
    result.sort(key=lambda s: s.top)
    return result


def find_shapes_in_group(slide):
    """递归找到组合内的文本 shape。"""
    results = []
    for shape in slide.shapes:
        if shape.shape_type == 6:  # GROUP
            for child in shape.shapes:
                if child.has_text_frame:
                    results.append(child)
    return results


# ── 图片替换 ─────────────────────────────────────────────

def replace_pics_with_images(slide, image_paths: list[str]):
    """替换幻灯片中的 PIC shape 为新图片。按 left 位置排序匹配。"""
    pics = sorted(
        [s for s in slide.shapes if s.shape_type == 13],
        key=lambda s: s.left,
    )
    for i, pic in enumerate(pics):
        if i >= len(image_paths) or not image_paths[i]:
            continue
        left, top = pic.left, pic.top
        width, height = pic.width, pic.height
        slide.shapes._spTree.remove(pic._element)
        slide.shapes.add_picture(image_paths[i], left, top, width, height)


# ── 布局专用填充器 ──────────────────────────────────────

def _fill_title(slide, title: str):
    """填充标题 shape（通用逻辑）。"""
    all_shapes = sorted(
        [s for s in slide.shapes if s.has_text_frame],
        key=lambda s: (s.top, s.left),
    )
    # 优先 PLACEHOLDER
    for shape in all_shapes:
        if shape.shape_type == 14 and shape.top < 1500000:
            set_shape_text(shape, title)
            return
    # 备选：top 最小的有文本 shape
    for shape in all_shapes:
        txt = (shape.text_frame.text or "").strip()
        if not txt or (len(txt) <= 2 and txt.isdigit()):
            continue
        if shape.top < 1500000:
            set_shape_text(shape, title)
            return
    # 再备选
    for shape in all_shapes:
        txt = (shape.text_frame.text or "").strip()
        if txt and not (len(txt) <= 2 and txt.isdigit()):
            set_shape_text(shape, title)
            return


def _fill_一段文字(slide, points: list[str], body: str):
    """填充一段文字布局的正文区域。"""
    all_shapes = sorted(
        [s for s in slide.shapes if s.has_text_frame],
        key=lambda s: (s.top, s.left),
    )
    content_shapes = [
        s for s in all_shapes
        if s.top >= 1500000
        and (s.text_frame.text or "").strip()
        and not ((s.text_frame.text or "").strip().isdigit() and len((s.text_frame.text or "").strip()) <= 2)
    ]
    if content_shapes:
        if points:
            set_shape_bullets(content_shapes[0], points, font_size_pt=14)
        elif body:
            set_shape_text(content_shapes[0], body, font_size_pt=14)


def _fill_grouped_cards(slide, cards: list[dict]):
    """填充三个观点等分组卡片布局。

    模板结构：3 个 GROUP shape，每个含 title + body 文本 shape。
    """
    groups = sorted(
        [s for s in slide.shapes if s.shape_type == 6 and s.top > 1000000],
        key=lambda s: s.left,
    )
    for i, grp in enumerate(groups):
        if i >= len(cards):
            break
        card = cards[i]
        # 组内文本 shape 按 top 排序
        texts = sorted(
            [s for s in grp.shapes if s.has_text_frame and (s.text_frame.text or "").strip()],
            key=lambda s: s.top,
        )
        for ts in texts:
            txt = (ts.text_frame.text or "").strip()
            if len(txt) <= 2:
                continue
            if ts.height < 800000:  # 短 = 标题
                set_shape_text(ts, card.get("title", ""))
            else:  # 长 = 正文
                set_shape_text(ts, card.get("desc", ""))


def _fill_flat_cards(slide, cards: list[dict]):
    """填充四个观点等扁平卡片布局。

    模板结构：标题 shape（短）+ 描述 shape（长），按 2x2 排列。
    """
    all_shapes = [
        s for s in slide.shapes
        if s.has_text_frame and s.top > 1000000 and (s.text_frame.text or "").strip()
    ]
    # 分离标题（短）和描述（长）
    titles = sorted(
        [s for s in all_shapes if s.height < 1000000],
        key=lambda s: (s.top, s.left),
    )
    descs = sorted(
        [s for s in all_shapes if s.height >= 1000000],
        key=lambda s: (s.top, s.left),
    )
    for i, shape in enumerate(titles):
        if i < len(cards):
            set_shape_text(shape, cards[i].get("title", ""))
    for i, shape in enumerate(descs):
        if i < len(cards):
            set_shape_text(shape, cards[i].get("desc", ""))


def _fill_five_cards(slide, cards: list[dict]):
    """填充五个观点布局。

    模板结构较特殊：5 个描述 shape 分散排列，按 left 位置排序。
    """
    all_shapes = [
        s for s in slide.shapes
        if s.has_text_frame and s.top > 1000000 and (s.text_frame.text or "").strip()
    ]
    # 描述 shape（较长文本）
    descs = sorted(
        [s for s in all_shapes if s.height > 500000],
        key=lambda s: s.left,
    )
    for i, shape in enumerate(descs):
        if i < len(cards):
            set_shape_text(shape, cards[i].get("desc", ""))


def _fill_contrast(slide, cards: list[dict]):
    """填充观点对比布局。

    模板结构：左右两组，各有标题（短）+ 正文（长）。
    """
    all_shapes = [
        s for s in slide.shapes
        if s.has_text_frame and s.top > 1000000 and (s.text_frame.text or "").strip()
    ]
    all_shapes.sort(key=lambda s: s.left)
    if not all_shapes:
        return
    mid_x = sum(s.left for s in all_shapes) / len(all_shapes)
    left_shapes = sorted([s for s in all_shapes if s.left < mid_x], key=lambda s: s.top)
    right_shapes = sorted([s for s in all_shapes if s.left >= mid_x], key=lambda s: s.top)

    for side_shapes, card in [(left_shapes, cards[0] if cards else {}), (right_shapes, cards[1] if len(cards) > 1 else {})]:
        for s in side_shapes:
            if s.height < 1000000:  # 标题
                set_shape_text(s, card.get("title", ""))
            else:  # 正文
                set_shape_text(s, card.get("desc", ""))


def _fill_一段一图(slide, data: dict):
    """填充一段一图布局：替换图片 + 填充标题和正文。"""
    image = data.get("image", "")
    points = data.get("points", [])
    body = data.get("body", "")

    if image:
        replace_pics_with_images(slide, [image])

    # 找内容区文本 shape
    content_shapes = sorted(
        [s for s in slide.shapes if s.has_text_frame and s.top > 1000000],
        key=lambda s: (s.top, s.left),
    )
    # 分离标题和正文（标题较短，正文较长）
    short = [s for s in content_shapes if s.height < 1000000 and (s.text_frame.text or "").strip()]
    long = [s for s in content_shapes if s.height >= 1000000 and (s.text_frame.text or "").strip()]

    if short and data.get("card_title"):
        set_shape_text(short[0], data["card_title"])
    if long:
        if points:
            set_shape_bullets(long[0], points, font_size_pt=12)
        elif body:
            set_shape_text(long[0], body, font_size_pt=12)


def _fill_框架图(slide, data: dict):
    """填充框架图布局：替换为框架图图片。"""
    image = data.get("image", "")
    if image:
        # 框架图布局有一个大的空白区域，把图片插入到中央
        # 模板框架图 slide 93 的内容区大约在 top=1000000, height=5000000
        replace_pics_with_images(slide, [image] if image else [])
    # 填充副标题
    all_text = [
        s for s in slide.shapes
        if s.has_text_frame and 1000000 < s.top < 3000000 and (s.text_frame.text or "").strip()
    ]
    subtitle = data.get("subtitle", "")
    if subtitle and all_text:
        set_shape_text(all_text[0], subtitle)


def _fill_timeline_4(slide, items: list[dict]):
    """填充四段时间轴布局。"""
    # 底部日期标签（shapes 8-11）
    # 描述文字（shapes 12-15）
    all_shapes = [
        s for s in slide.shapes
        if s.has_text_frame and s.top > 1000000 and (s.text_frame.text or "").strip()
    ]
    # 日期标签：高度较短的 shape
    date_shapes = sorted(
        [s for s in all_shapes if s.height < 1000000 and s.top > 4000000],
        key=lambda s: s.left,
    )
    # 描述：高度较长的 shape
    desc_shapes = sorted(
        [s for s in all_shapes if s.height < 1200000 and s.top < 3000000],
        key=lambda s: s.left,
    )
    for i, shape in enumerate(date_shapes):
        if i < len(items):
            set_shape_text(shape, items[i].get("date", ""))
    for i, shape in enumerate(desc_shapes):
        if i < len(items):
            set_shape_text(shape, items[i].get("desc", ""))


def _fill_timeline_5(slide, items: list[dict]):
    """填充五段时间轴布局。"""
    all_shapes = [
        s for s in slide.shapes
        if s.has_text_frame and s.top > 1000000 and (s.text_frame.text or "").strip()
    ]
    # 标题 shape（短，top 较小）
    titles = sorted(
        [s for s in all_shapes if s.height < 800000 and 1500000 < s.top < 2500000],
        key=lambda s: s.left,
    )
    # 描述 shape（高，top 较大）
    descs = sorted(
        [s for s in all_shapes if s.height > 1000000 and s.top > 3500000],
        key=lambda s: s.left,
    )
    # 编号 shape
    numbers = sorted(
        [s for s in all_shapes if (s.text_frame.text or "").strip().isdigit()],
        key=lambda s: s.left,
    )
    for i, shape in enumerate(titles):
        if i < len(items):
            set_shape_text(shape, items[i].get("title", ""))
    for i, shape in enumerate(descs):
        if i < len(items):
            set_shape_text(shape, items[i].get("desc", ""))


def _fill_两段文字(slide, texts: list[str]):
    """填充两段文字布局。"""
    content_shapes = sorted(
        [s for s in slide.shapes if s.has_text_frame and s.top > 1000000],
        key=lambda s: (s.top, s.left),
    )
    # 只填有文本的大 shape
    big = [s for s in content_shapes if (s.text_frame.text or "").strip()]
    for i, shape in enumerate(big):
        if i < len(texts):
            set_shape_text(shape, texts[i], font_size_pt=13)


# ── 各类幻灯片生成 ──────────────────────────────────────

def make_cover(prs: Presentation, meta: dict):
    """克隆封面页，替换标题和信息。"""
    slide = clone_slide(prs, TEMPLATE_SLIDES["cover"])

    shapes = find_shapes_with_text(slide, min_chars=1)

    title_text = meta.get("title", "论文标题")
    subtitle_text = meta.get("subtitle", "")

    for shape in shapes:
        txt = (shape.text_frame.text or "").strip()
        if "答辩人" in txt or "导师" in txt:
            info_lines = [
                f"答辩人：{meta.get('author', '')}",
                f"导　师：{meta.get('advisor', '')}",
                f"时　间：{meta.get('date', '')}",
            ]
            set_shape_lines(shape, info_lines)
        elif len(txt) > 3 and "答辩人" not in txt:
            lines = [title_text]
            if subtitle_text:
                lines.append(subtitle_text)
            set_shape_lines(shape, lines, font_size_pt=40, bold=True)


def make_toc(prs: Presentation, sections: list[str]):
    """克隆目录页，替换目录项。"""
    slide = clone_slide(prs, TEMPLATE_SLIDES["toc"])

    top_group = None
    for shape in slide.shapes:
        if shape.shape_type == 6:
            top_group = shape
            break
    if not top_group:
        return

    toc_slots = []
    for child_group in top_group.shapes:
        text_shape = None
        num_shape = None
        for sub in child_group.shapes:
            if sub.has_text_frame:
                txt = (sub.text_frame.text or "").strip()
                if txt.isdigit() and len(txt) <= 2:
                    num_shape = sub
                elif len(txt) > 1:
                    text_shape = sub
        if text_shape:
            toc_slots.append((text_shape, num_shape))

    toc_slots.sort(key=lambda x: x[0].top)

    for i, (text_shape, num_shape) in enumerate(toc_slots):
        if i < len(sections):
            set_shape_text(text_shape, sections[i])
            if num_shape:
                set_shape_text(num_shape, str(i + 1))
        else:
            set_shape_text(text_shape, "")
            if num_shape:
                set_shape_text(num_shape, "")


def make_section_divider(prs: Presentation, title: str, num: int):
    """克隆章节分隔页，清除模板残留文字。"""
    slide = clone_slide(prs, TEMPLATE_SLIDES["section"])

    shapes = find_shapes_with_text(slide, min_chars=1)
    for shape in shapes:
        txt = (shape.text_frame.text or "").strip()
        if not txt:
            continue
        if "北京" in txt or "毕业" in txt or "BIT" in txt.upper():
            set_shape_text(shape, f"第{num}部分  {title}", font_size_pt=36, bold=True)
        elif "Template" in txt or "答辩人" in txt or "导师" in txt:
            set_shape_text(shape, "")


def make_content_slide(prs: Presentation, data: dict):
    """克隆内容页，根据布局类型自动填充。"""
    layout_name = data.get("layout", "一段文字")
    src_idx = TEMPLATE_SLIDES.get(layout_name, TEMPLATE_SLIDES["一段文字"])
    slide = clone_slide(prs, src_idx)

    # 1. 填标题
    _fill_title(slide, data.get("title", ""))

    # 2. 按布局类型分发
    cards = data.get("cards", [])
    points = data.get("points", [])
    body = data.get("body", "")
    image = data.get("image", "")
    items = data.get("items", [])

    if layout_name == "一段文字":
        _fill_一段文字(slide, points, body)

    elif layout_name == "三个观点":
        if cards:
            _fill_grouped_cards(slide, cards)

    elif layout_name == "四个观点":
        if cards:
            _fill_flat_cards(slide, cards)

    elif layout_name == "五个观点":
        if cards:
            _fill_five_cards(slide, cards)

    elif layout_name == "观点对比":
        if cards:
            _fill_contrast(slide, cards)

    elif layout_name == "一段一图":
        _fill_一段一图(slide, data)

    elif layout_name == "一段二图":
        images = data.get("images", [image, image] if image else [])
        if images:
            replace_pics_with_images(slide, images)

    elif layout_name == "框架图":
        _fill_框架图(slide, data)

    elif layout_name == "四段时间轴":
        if items:
            _fill_timeline_4(slide, items)

    elif layout_name == "五段时间轴":
        if items:
            _fill_timeline_5(slide, items)

    elif layout_name == "两段文字":
        texts = data.get("texts", [])
        if texts:
            _fill_两段文字(slide, texts)


def make_end(prs: Presentation, meta: dict):
    """克隆尾页（感谢页）。"""
    slide = clone_slide(prs, TEMPLATE_SLIDES["end"])

    shapes = find_shapes_with_text(slide, min_chars=1)
    for shape in shapes:
        txt = (shape.text_frame.text or "").strip()
        if "感谢" in txt or "批评" in txt or "谢谢" in txt:
            set_shape_lines(shape, ["感谢各位专家老师", "请您批评指正"],
                            font_size_pt=40, bold=True)
        elif "答辩人" in txt or "导师" in txt:
            info_lines = [
                f"答辩人：{meta.get('author', '')}",
                f"导　师：{meta.get('advisor', '')}",
                f"时　间：{meta.get('date', '')}",
            ]
            set_shape_lines(shape, info_lines)


# ── 主流程 ──────────────────────────────────────────────

def generate_pptx(template_path: str, content: dict, output_path: str):
    prs = Presentation(template_path)

    meta = content.get("meta", {})
    slides_def = content.get("slides", [])
    toc_items = content.get("toc", [])

    # 1. 封面
    make_cover(prs, meta)

    # 2. 目录
    if toc_items:
        make_toc(prs, toc_items)

    # 3. 内容
    section_num = 0
    for s in slides_def:
        if s.get("type") == "section":
            section_num += 1
            make_section_divider(prs, s["title"], section_num)
        else:
            make_content_slide(prs, s)

    # 4. 尾页
    make_end(prs, meta)

    # 5. 删除模板原有的 362 张幻灯片，只保留新生成的
    new_count = len(prs.slides) - ORIGINAL_SLIDE_COUNT
    remove_original_slides(prs, new_count)

    prs.save(output_path)
    n_content = sum(1 for s in slides_def if s.get("type") != "section")
    print(f"✓ 已生成: {output_path}")
    print(f"  封面1 + 目录{'1' if toc_items else '0'} + 章节{section_num} + 内容{n_content} + 尾页1 = {new_count}页")


# ── 示例内容 ─────────────────────────────────────────────

EXAMPLE_CONTENT = {
    "meta": {
        "title": "星地激光通信信号处理关键技术研究",
        "subtitle": "硕士学位论文开题报告",
        "author": "张哲铜",
        "advisor": "XXX 教授",
        "date": "2026年6月",
    },
    "toc": [
        "研究背景与意义",
        "国内外研究现状",
        "研究内容与方案",
        "预期成果与创新点",
        "研究计划与进度安排",
    ],
    "slides": [
        # ── 第一部分：研究背景与意义 ──
        {"type": "section", "title": "研究背景与意义"},
        {
            "type": "content",
            "layout": "一段文字",
            "title": "研究背景",
            "points": [
                "星地激光通信具有带宽高、抗干扰、保密性好等优势，是未来空间通信的重要发展方向",
                "大气湍流导致光束漂移、光强闪烁和相位畸变，严重制约通信链路可靠性",
                "信道建模、均衡与同步是提升星地激光通信性能的三个核心问题",
                "深度学习为解决复杂非线性信道下的信号处理问题提供了新思路",
                "本课题围绕星地激光通信信号处理链路，系统研究信道建模、均衡和同步算法",
            ],
        },
        {
            "type": "content",
            "layout": "三个观点",
            "title": "研究意义",
            "cards": [
                {"title": "理论意义", "desc": "建立大气湍流信道的高精度统计模型，揭示信道参数与通信性能之间的内在联系，丰富激光通信信道建模理论体系"},
                {"title": "实际意义", "desc": "提升星地激光通信链路的可靠性和传输速率，为工程实现提供算法支撑，推动激光通信实用化进程"},
                {"title": "方法意义", "desc": "探索人工智能在物理层信号处理中的应用范式，为传统通信信号处理问题提供数据驱动的新解决思路"},
            ],
        },

        # ── 第二部分：国内外研究现状 ──
        {"type": "section", "title": "国内外研究现状"},
        {
            "type": "content",
            "layout": "四个观点",
            "title": "四个关键技术方向",
            "cards": [
                {"title": "信道建模", "desc": "Gamma-Gamma模型已成为大气湍流信道的事实标准，涵盖弱到强湍流全范围，可精确描述光强衰落统计特性"},
                {"title": "信道估计", "desc": "LS/MMSE传统方法成熟，DNN方法在低SNR和强湍流下展现1-3dB增益，是当前研究热点"},
                {"title": "信道均衡", "desc": "DFE+MMSE在弱湍流下近最优，DL方法在中强湍流下BER改善10-55%，FSO用实值信号需特殊设计"},
                {"title": "载波同步", "desc": "VV/BPS为相干系统主流方法，AI辅助同步在联合频偏相位补偿中展现潜力，但创新点风险较高"},
            ],
        },
        {
            "type": "content",
            "layout": "观点对比",
            "title": "传统方法 vs 深度学习方法",
            "cards": [
                {"title": "传统方法优势", "desc": "基于统计模型和先验知识，计算复杂度低，理论体系成熟完善。在弱湍流和高SNR条件下性能接近最优。但需要精确的信道统计先验信息，且在强湍流等非线性严重场景下性能退化明显"},
                {"title": "深度学习方法优势", "desc": "数据驱动方式，自适应能力强，无需精确信道模型。在中强湍流、低SNR等挑战场景下表现优异，能捕捉非线性特征。但需要大量训练数据，泛化性有待验证，计算复杂度较高"},
            ],
        },
        {
            "type": "content",
            "layout": "一段一图",
            "title": "信道估计研究现状",
            "image": "毕设/test_images/ber_curve.png",
            "card_title": "LS / MMSE / DNN 三种估计方法对比",
            "points": [
                "LS估计：复杂度最低，但噪声放大严重",
                "MMSE估计：最优线性估计，需信道统计先验",
                "DNN估计：数据驱动，强湍流下优势明显",
                "DNN在SNR<10dB时相较LS有2-3dB增益",
            ],
        },

        # ── 第三部分：研究内容与方案 ──
        {"type": "section", "title": "研究内容与方案"},
        {
            "type": "content",
            "layout": "框架图",
            "title": "总体研究框架",
            "subtitle": "信道建模 → 信道估计 → 信道均衡 → 载波同步 → 性能评估",
            "image": "毕设/test_images/framework.png",
        },
        {
            "type": "content",
            "layout": "一段一图",
            "title": "第二章：大气湍流信道建模与特征估计",
            "image": "毕设/test_images/bar_compare.png",
            "card_title": "信道建模与估计方案",
            "points": [
                "基于Gamma-Gamma模型建立星地激光通信信道模型",
                "研究LS、MMSE和DNN三种信道估计方法",
                "在不同湍流强度（弱/中/强）和SNR条件下进行性能对比",
                "分析DNN方法在强湍流场景下的性能增益（预期1-3dB）",
            ],
        },
        {
            "type": "content",
            "layout": "一段文字",
            "title": "第三章：信道均衡算法研究",
            "points": [
                "研究DFE、MMSE等经典均衡算法在FSO信道中的性能表现",
                "设计CNN/LSTM神经网络均衡器，利用非线性拟合能力补偿湍流畸变",
                "在OOK调制、不同湍流强度下对比传统与DL均衡器性能",
                "FSO采用IM/DD方式产生实值信号，需设计适配实值信号的均衡架构",
                "预期DL均衡器在中强湍流下BER改善10-55%，弱湍流下接近传统方法",
            ],
        },
        {
            "type": "content",
            "layout": "一段文字",
            "title": "第四章：载波同步与相位恢复算法研究",
            "points": [
                "研究VV算法（QPSK最优）和BPS算法（高阶调制主流）等经典相位恢复方法",
                "分析LEO多普勒频移（±4.6GHz）对同步的影响及预补偿策略",
                "设计RNN/GRU辅助的联合频偏估计与相位恢复方案",
                "在相干检测+QPSK体制下评估同步性能，叠加Gamma-Gamma湍流信道",
                "创新点为FSO特色（湍流鲁棒性/联合频偏+相位补偿/低复杂度改进）",
            ],
        },

        # ── 第四部分：预期成果与创新点 ──
        {"type": "section", "title": "预期成果与创新点"},
        {
            "type": "content",
            "layout": "四个观点",
            "title": "预期研究成果",
            "cards": [
                {"title": "高精度信道模型", "desc": "建立完整的星地激光通信Gamma-Gamma信道模型，实现三种估计方法的系统对比分析，量化各方法在不同湍流条件下的性能边界"},
                {"title": "高效均衡算法", "desc": "提出适用于FSO信道IM/DD实值信号的DL均衡方案，在中强湍流下实现BER改善10-55%，为实际工程应用提供算法支撑"},
                {"title": "鲁棒同步算法", "desc": "设计AI辅助的联合频偏估计与相位恢复方案，解决LEO场景下的多普勒频移挑战，提升复杂信道下的同步鲁棒性"},
                {"title": "系统性能评估", "desc": "完成端到端信号处理链路仿真验证，量化各模块对系统性能的贡献，形成完整的星地激光通信信号处理方案"},
            ],
        },
        {
            "type": "content",
            "layout": "一段文字",
            "title": "主要创新点",
            "points": [
                "将DL方法系统应用于FSO信道估计、均衡和同步三个关键环节，形成完整的信号处理方案",
                "针对FSO信道IM/DD实值信号特点，设计适配的DL均衡架构（区别于RF复值均衡）",
                "提出联合频偏估计与相位恢复的AI辅助方案，解决LEO场景下的多普勒频移挑战",
            ],
        },

        # ── 第五部分：研究计划 ──
        {"type": "section", "title": "研究计划与进度安排"},
        {
            "type": "content",
            "layout": "一段一图",
            "title": "进度安排",
            "image": "毕设/test_images/timeline.png",
            "card_title": "研究阶段划分",
            "points": [
                "2026.06-08：文献调研 + Ch2 信道建模与估计",
                "2026.09-11：Ch3 信道均衡算法研究与仿真验证",
                "2026.12-2027.02：Ch4 载波同步算法研究",
                "2027.03-04：系统集成验证与性能评估",
                "2027.05-06：论文撰写与修改",
            ],
        },
    ],
}


def main():
    parser = argparse.ArgumentParser(description="从 JSON + 北理模板生成答辩 PPT")
    parser.add_argument("--content", "-c", help="幻灯片内容 JSON 文件路径")
    parser.add_argument("--template", "-t",
                        default="毕设/北京理工大学学术答辩PPT模板正式版.pptx",
                        help="PPT 模板路径")
    parser.add_argument("--output", "-o", default="毕设/开题答辩.pptx",
                        help="输出 PPTX 路径")
    parser.add_argument("--example", action="store_true",
                        help="用示例内容生成（测试用）")
    args = parser.parse_args()

    if args.example:
        content = EXAMPLE_CONTENT
    elif args.content:
        with open(args.content, "r", encoding="utf-8") as f:
            content = json.load(f)
    else:
        print("请指定 --content <file> 或 --example")
        sys.exit(1)

    generate_pptx(args.template, content, args.output)


if __name__ == "__main__":
    main()
