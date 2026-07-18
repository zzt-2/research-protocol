# pandoc 管线说明

将 markdown 转为符合北理工本科毕业论文格式要求的 Word 文档。

## 文件清单

| 文件 | 用途 |
|------|------|
| `reference.docx` | Word 模板，定义基础样式（标题层级、正文、"图片"/"表格" 等自定义样式） |
| `gb7714-2015.csl` | GB/T 7714-2015 参考文献引文样式（数字顺序编码制，中文 locale） |
| `auto-numbering.lua` | 自动编号：H1="第X章"、H2="X.Y"、H3="X.Y.Z"；图标题加 "图 X-Y " 前缀 |
| `replace-et-al.lua` | 将含中文作者名的参考文献中的 "et al." 替换为 "等" |
| `format-cn-academic.py` | python-docx 后处理（详见下方） |

## 构建命令

```bash
cd 毕设/开题报告

# Step 1: pandoc 生成 docx
pandoc kaiti-report.md \
  -o kaiti.docx \
  --citeproc \
  --csl=../pandoc/gb7714-2015.csl \
  --bibliography=../写作材料/references.bib \
  --reference-doc=../pandoc/reference.docx \
  --lua-filter=../pandoc/replace-et-al.lua \
  --lua-filter=../pandoc/auto-numbering.lua

# Step 2: 后处理格式化（原地覆盖，可指定第二参数另存）
python ../pandoc/format-cn-academic.py kaiti.docx
```

> lua filter 顺序无关紧要（各自处理不同 AST 元素）。

## Markdown 写作规范

### 标题——不加编号

```markdown
# 选题依据          → 输出 "第1章 选题依据"（居中，黑体三号加粗）
## 研究意义         → 输出 "1.1 研究意义"（左齐，黑体四号加粗）
### 系统模型        → 输出 "1.1.1 系统模型"（左齐，黑体小四加粗）
```

### 图——不加 "图 X-Y "

```markdown
![星地链路示意图](figures/fig.png)
→ 输出 "图 1-1 星地链路示意图"（lua filter 自动加前缀）
```

### 表标题——写 "表 " 开头，不带数字

```markdown
表 仿真参数体系
| 参数 | 值 |
|------|----|
| ...  | ...|
→ 输出 "表 3-1 仿真参数体系"（后处理自动加编号）
```

### 公式——直接写，不加编号

```markdown
$$\gamma = \bar{\gamma} \cdot h$$
→ 输出公式居中，右侧自动编号 "(3-1)"
```

公式编号使用 `w:ptab`（绝对定位制表符），公式居中不受编号宽度影响。

### 引用

```markdown
[@khalighi2014]     → 上标 [1]
```

参考文献列表由 `--citeproc` + CSL 自动生成，格式为 GB/T 7714-2015 数字编码制。

## format-cn-academic.py 模块说明

按职责分 6 组：

### 1. Run / 段落辅助

| 函数 | 作用 |
|------|------|
| `set_run_font` | 给 python-docx Run 设 CJK+西文字体/字号/加粗 |
| `_set_raw_run_font` | 给裸 OxmlElement run 设字体（公式编号等） |
| `set_space_lines` | 段前/段后间距（行单位，100=1行） |
| `set_space_after_half_line` | 段后 0.5 行 |

### 2. 段落分类

| 函数 | 判断 |
|------|------|
| `get_heading_level` | 返回 Heading 级别 1-4，非标题返回 0 |
| `is_heading` | 是否标题段落 |
| `is_caption` | 是否图/表标题（样式名或文本匹配） |
| `has_display_math` | 是否含 `m:oMathPara`（独立公式） |
| `has_image` | 是否含图片 |
| `is_bibliography` | 是否参考文献条目 |

### 3. 公式编号

| 函数 | 作用 |
|------|------|
| `_convert_omathpara_to_omath` | `m:oMathPara`（块级）→ `m:oMath`（行内），为 ptab 做准备 |
| `_make_ptab_run` | 创建 `w:ptab` 绝对定位制表符 run |
| `_make_text_run` | 创建带字体的文本 run |

公式编号布局：`[center ptab] oMath [right ptab] (X-Y)`。`w:ptab` 相对 margin 动态定位，不需要预计算制表位位置。

### 4. 表格

| 函数 | 作用 |
|------|------|
| `set_three_line_table` | 三线表：顶线/底线 1.5pt，表头下线 0.75pt |
| `clear_cell_inherits` | 清除单元格段落的正文继承格式 |

### 5. 参考文献

| 函数 | 作用 |
|------|------|
| `format_bibliography` | 五号字，悬挂缩进，编号对齐，去超链接 |
| `strip_hyperlinks` | 将 `w:hyperlink` 展平为普通 run |
| `clean_hyperlink_style` | 去蓝色/下划线/hyperlink 样式 |

### 6. 页面设置

| 函数 | 作用 |
|------|------|
| `_setup_header` | 页眉："北京理工大学本科生毕业设计（论文）"，宋体四号居中，字间距+0.5pt，底部横线 |
| `_setup_footer` | 页脚：PAGE 域，宋体五号居中 |

## 格式规范

### 页面设置

A4 纵向，上 3.5cm / 下 2.6cm / 左 3cm / 右 2.6cm，页眉 2.4cm / 页脚 2cm / 装订线 0。

### 字体与字号

| 元素 | 中文字体 | 西文字体 | 字号 | 其他 |
|------|---------|---------|------|------|
| H1 | 黑体 | TNR | 三号 16pt | 加粗居中，段前 0.5 行段后 1 行，1.5 倍行距 |
| H2 | 黑体 | TNR | 四号 14pt | 加粗左齐，段前 0.5 行段后 0 行，1.5 倍行距 |
| H3 | 黑体 | TNR | 小四 12pt | 加粗左齐，段前 0.5 行段后 0 行，1.5 倍行距 |
| 正文 | 宋体 | TNR | 小四 12pt | 22 磅固定行距，段后 0.5 行 |
| 图/表标题 | 宋体 | TNR | 五号 10.5pt | 居中 |
| 公式 | 宋体 | TNR | 小四 12pt | 居中（ptab），右侧 "(X-Y)" 编号 |
| 表格内容 | 宋体 | TNR | 五号 10.5pt | 表头黑体，三线表 |
| 参考文献 | 宋体 | TNR | 五号 10.5pt | 悬挂缩进，按最大编号宽度对齐 |

### 三线表

顶线/底线 1.5pt，表头下线 0.75pt，无竖线和内部横线。表头黑体，内容宋体，均为五号。

### 参考文献

- 去除超链接（元素 + rels + 蓝色/下划线样式）
- 五号字，悬挂缩进（宽度按最大编号位数自适应）
- 短编号补空格对齐

### CSL 定制 (gb7714-2015.csl)

相比官方版本的修改：
- 取消作者姓名大写（移除 `text-case="uppercase"`）
- 有印刷版的文献类型（期刊 J、会议 C、专著 M、学位论文 D 等）不加 `/OL` 载体标识
- 隐藏 URL 和 DOI 输出
- `second-field-align="flush"` 支持编号右对齐
