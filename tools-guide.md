# 工具链指南

> 研究协议 v2 Groundwork 阶段工具链。纯 Python、CLI、轻量优先。
> 工具脚本都有 `--help`，详细参数不在这里列举。

## 1. 工具总览

| 工具 | 入口 | 用途 |
|------|------|------|
| 搜索 | `./tools/search "关键词"` | 七源聚合搜索，自动路由，存档 |
| blit | `./tools/blit "关键词" --source cnki` | 浏览器文献检索（IEEE/万方/CNKI），Playwright 驱动，支持 PDF 下载 |
| 下载 | `./tools/download <json\|arxiv\|doi>` | 批量/单篇下载 + PDF 转 markdown |
| 转换 | `./tools/convert source.pdf` | PDF → markdown，支持分章节输出、图片提取、MinerU 高质量转换 |

所有脚本统一使用 `~/.venvs/torch/bin/python`（含 torch + MinerU + pymupdf + 搜索依赖）。

### 调用方式（重要）

`tools/search`、`tools/download`、`tools/convert` 都是 **bash shell wrapper**，不是 Python 文件。必须从项目根目录调用：

```bash
# 正确 ✅ — 从项目根目录调用
cd /mnt/d/code/study/research-protocol && ./tools/search "LEO satellite"
cd /mnt/d/code/study/research-protocol && bash tools/search "LEO satellite"

# 错误 ❌ — 用 python 跑 shell 脚本
python tools/search "..."        # shell wrapper，不是 .py
python tools/literature_search.py "..."  # 缺少依赖路径
```

## 2. 论文检索

```bash
# 基本搜索
./tools/search "LEO satellite channel prediction"

# 按文档类型路由（自动选最优源 + 注入查询修饰词）
./tools/search "3GPP NTN specification" --doc-types standard
./tools/search "reinforcement learning patent" --doc-types patent
./tools/search "知识蒸馏 大语言模型" --doc-types chinese_journal
./tools/search "LLM fine-tuning" --doc-types code
./tools/search "NVIDIA revenue 2025" --doc-types financial

# 指定模式/策略
./tools/search "beamforming" --mode academic --preset scenario-method

# 手动指定源
./tools/search "5G NR" --sources exa firecrawl

# Exa 模式选择
./tools/search "..." --sources exa --exa-mode neural    # 纯语义
./tools/search "..." --sources exa --exa-mode keyword   # 纯关键词
./tools/search "..." --sources exa --exa-mode auto      # 默认，双跑去重

# 相似论文（从 URL 找相关文献）
./tools/search --find-similar https://arxiv.org/abs/1706.03762

# 引用图谱（OpenAlex，无限额）
./tools/search --citations 10.1109/TWC.2024.3406952
./tools/search --citations 10.1109/TWC.2024.3406952 --citations-direction backward
./tools/search --citations 10.1109/TWC.2024.3406952 --citations-depth 2

# 发文趋势
./tools/search "LEO satellite handover" --trend
./tools/search "transformer attention" --trend --trend-years 10

# 展开引用链
./tools/search "channel prediction" --refs 2

# 合并历史结果
./tools/search "beamforming" --merge search-archive/old-results.json

# 输出格式
./tools/search "..." --format json     # 默认，结构化
./tools/search "..." --format markdown # 可读表格
./tools/search "..." --format brief    # 每行一条
```

### 中文查询格式（重要）

中文关键词**用空格分隔**，让工具正确拆词做相关性评分：

```bash
# 正确 ✅ — 空格分隔，每个词独立参与相关性匹配
./tools/search "针灸 偏头痛 随机对照试验"
./tools/search "个人信息保护法 司法适用 判例"
./tools/search "混合式教学 学习成效 meta分析"

# 效果差 ❌ — 连写整句，工具无法正确拆分语义单元
./tools/search "针灸治疗偏头痛随机对照试验"
```

工具内部有 jieba 分词兜底，但空格分隔的粒度由调用方控制，效果更可控。

| 模式 | 触发条件 | 搜索源 |
|------|---------|--------|
| academic（默认） | 英文查询 | S2 + OpenAlex + arXiv + SerpAPI + **Exa** |
| chinese | 中文字符 | **Exa** + SerpAPI + **Firecrawl** |
| standard | 含 standard/ITU-R/3GPP | **Firecrawl** + **Exa** + SerpAPI + Tavily |
| broad | 手动指定 | **七源全开** |

### 文档类型路由（`--doc-types`）

指定文档类型后，自动路由到最优源并注入查询修饰词：

| 类型 | 最优源 | 自动修饰 | 典型场景 |
|------|--------|---------|---------|
| journal | Exa + FC | — | 期刊论文 |
| conference | Exa + FC | — | 会议论文 |
| preprint | Exa + FC | `site:arxiv.org` | arXiv 预印本 |
| standard | FC + Exa | `3GPP ETSI specification` | 3GPP/ETSI 标准 |
| patent | FC + Exa | — | Google Patents |
| policy | FC + Exa | — | 政府政策 |
| financial | Exa + FC | — | 财报/SEC/IR |
| industry_report | FC + Exa | `Gartner McKinsey report` | 行业报告 |
| whitepaper | FC + Exa | `technical report` | 白皮书 |
| code | Exa | — | GitHub（category=github） |
| dataset | Exa | — | HuggingFace |
| news | Exa | — | 新闻（category=news） |
| blog | FC + Exa | — | 技术博客 |
| book | Exa + FC | — | 书籍 |
| chinese_journal | Exa + FC | — | 中文学术期刊 |
| thesis | OpenAlex | — | 学位论文 |

多个类型可组合：`--doc-types journal conference preprint`

### 预设策略

| 预设 | 用途 |
|------|------|
| `--preset scenario-method` | 拆分查询为子查询，分别搜索再合并 |
| `--preset problem-driven` | 全源搜索，不限制年份 |
| `--preset comparison` | 追加 survey/review/benchmark 关键词 |
| `--preset implementation` | 找代码/实现 |

### 搜索源

| 源 | 能力 | 权重 |
|----|------|------|
| S2 (Semantic Scholar) | 学术论文元数据、引用数 | 1.0 |
| SerpAPI (Google Scholar) | 学术搜索、中文支持 | 0.9 |
| **Exa** | **语义搜索 (neural)、关键词搜索、find_similar、category 过滤** | **0.85** |
| arXiv | 预印本搜索 | 0.8 |
| OpenAlex | 学术搜索、引用图谱、趋势分析 | 0.6 |
| **Firecrawl** | **网页搜索（标准/专利/政策/博客）、全文抓取** | **0.6** |
| Tavily | 通用网页搜索 | 0.5 |

### 发表状态判断

搜索结果 JSON 中每条结果会包含 `publication_status` 字段（由后处理自动标注）：
- `published`：有正式 DOI（非 arXiv）或有正式期刊 venue
- `preprint`：DOI 为 arXiv（10.48550）或 venue 含 "arxiv"
- `unknown`：无法判断

如需补充正式发表文献，可用 `tools/blit`（浏览器检索工具）：
```bash
bash tools/blit "LEO satellite handover" --source ieee        # IEEE Xplore
bash tools/blit "低轨卫星 切换" --source wanfang               # 万方（中文期刊）
bash tools/blit "关键词" --source cbpt --journal wxdg          # CNKI 单刊
```

注意：blit 使用 Playwright 渲染，限速严格（IEEE 50次/会话，万方 10次/会话），适合低频补充检索。

### 排序权重

S2(1.0) > SerpAPI(0.9) > Exa(0.85) > arXiv(0.8) > OpenAlex(0.6) ≈ Firecrawl(0.6) > Tavily(0.5)

每次搜索自动存档到 `search-archive/{date}/{slug}.json`。

## 3. 论文下载

> **下载工具分工**：
> - `tools/litdownload/`（通过 `tools/download` 调用）：处理 arXiv、OA PDF、Unpaywall。自动写入全局索引、生成 metadata.json 和 content.md。
> - `tools/blit --download`：处理 IEEE（校园网 IP）和 CNKI（Cookie 认证）。不写全局索引，不自动生成 content.md，需手动运行 `tools/convert` 转换。
> - 如果 blit 下载了 IEEE/CNKI 论文，应手动将信息追加到 `papers/index.json`。

```bash
# 批量（从搜索结果 JSON）
./tools/download search-archive/{date}/xxx.json

# 单篇
./tools/download --arxiv 2405.17150
./tools/download --doi 10.1109/TWC.2024.3406952

# 预览 / 只下指定 / 强制重下
./tools/download xxx.json --dry-run
./tools/download xxx.json --only L001,L003
./tools/download xxx.json --force
```

### 下载通道（按优先级）

1. arXiv HTML（官方 LaTeXML，公式表格完美）
2. arXiv LaTeX（Pandoc 转，公式保留 LaTeX 语法）
3. arXiv PDF → pymupdf4llm 转 md（公式丢失）
4. OA PDF 直链 → pymupdf4llm
5. Unpaywall API
6. **Firecrawl Scrape**（CNKI 期刊/IEEE OA 全文，43-82KB markdown）

### PDF 转 Markdown 质量

| 级别 | 工具 | 说明 |
|------|------|------|
| fast（默认） | pymupdf4llm | 极快，公式全丢，纯文本够用 |
| standard | MinerU pipeline | 公式+表格保留，需 torch venv + GPU |

## 3.5 PDF 转换

```bash
# 单篇转换（fast 模式，默认）
./tools/convert source.pdf

# 高质量转换（保留公式、表格）
./tools/convert source.pdf --quality standard

# 分章节输出
./tools/convert source.pdf --chunk

# 提取图片
./tools/convert source.pdf --figures

# 组合使用
./tools/convert source.pdf --quality standard --chunk --figures -o output/

# 批量转换（每篇输出到各自子目录，互不覆盖）
./tools/convert paper-archive/xxx/ --batch --quality standard

# 多篇并行转换（默认输出 {pdf_stem}.md，互不覆盖）
./tools/convert a.pdf -o output/ &
./tools/convert b.pdf -o output/ &
wait
```

### 输出结构

单篇模式：`{pdf_stem}.md`（以 PDF 文件名命名，同目录多 PDF 互不覆盖）
分章节模式：`content_meta.md` / `content_intro.md` / `content_method.md` 等
图片目录：`figures/`

> **注意**：`tools/download` 管线内部仍使用 `content.md`（每篇论文独占目录，不存在冲突）。

### MinerU 环境

`--quality standard` 需要独立 torch venv（GPU 加速）：

```bash
# 创建 torch venv（仅需一次）
uv venv ~/.venvs/torch
~/.venvs/torch/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
~/.venvs/torch/bin/pip install "mineru[pipeline]"
```

超时可通过环境变量调整：`MINERU_TIMEOUT=600`（默认 300 秒）。

### 存储

```
paper-archive/{batch}/
  _manifest.json
  L001/
    metadata.json    # 下载状态和方法
    source.html      # 或 .tar.gz / .pdf
    content.md       # 转换后的 markdown
```

已下载的自动跳过，`--force` 强制重下。

### 下载现实

通信领域 IEEE/Elsevier 付费墙是常态（50-70%）。arXiv 预印本是最可靠的免费通道。大部分论文需用户手动获取（机构 VPN、作者主页）。

### 跳过规则

- 中文论文 → `manual_required`（有 URL 时尝试 Firecrawl Scrape）
- GitHub/标准文档/网页 → `skipped`
- IEEE PDF 直链 → 跳过（反爬拦截）
- DOI 重定向 URL → 跳过 OA，转 Unpaywall

## 4. 浏览器文献检索（blit）

Playwright 驱动的浏览器爬取工具，用于 API 无法覆盖的学术平台。限速策略内置，低频使用。

```bash
# IEEE 英文论文检索 + 下载（校园网 IP 自动机构认证）
./tools/blit "LEO satellite handover" --source ieee
./tools/blit "beam hopping LEO DRL" --source ieee --download papers/downloads/2026-05-15/

# 万方中文论文（低频，单次 ≤10 请求，间隔 6s）
./tools/blit "针灸 偏头痛 随机对照试验" --source wanfang
./tools/blit "深度强化学习 资源调度" --source wanfang --doc-type phd     # 万方搜博士论文
./tools/blit "企业管理" --source wanfang --doc-type master                # 万方搜硕士论文

# CNKI 主站搜索（校园网 IP + cookie 认证）
./tools/blit "混合式教学 实证研究" --source cnki
./tools/blit "低轨卫星 深度强化学习" --source cnki --doc-type phd    # 搜博士论文
./tools/blit "低轨卫星 资源管理" --source cnki --doc-type master       # 搜硕士论文

# CNKI 搜索 + 自动下载 PDF
./tools/blit "混合式教学 实证研究" --source cnki --download papers/downloads/2026-05-15/

# CNKI cookie 获取（首次使用或过期时）
~/.venvs/torch/bin/python tools/cnki_login.py
```

### 源特性

| 源 | 结果量 | 元数据 | 下载 | 反爬 | 限速 |
|----|--------|--------|------|------|------|
| IEEE | 50次无拦截 | 标题/作者/会议/年份/被引数 | ✅ `--download` 校园网机构认证 | 无 | 50次/会话, 1s间隔 |
| wanfang | 1410条/关键词 | 标题/作者/摘要/关键词/期刊/年份/被引数/质量标签/学位类型 | ❌ | IP封禁(>16次无间隔) | 10次/会话, 6s间隔 |
| cnki | 全库搜索 | 标题/作者/来源/年份/被引数 | ✅ `--download` 校园网+cookie | cookie 过期需验证 | 30次/会话, 3s间隔 |

CNKI 来源字段因文档类型不同：期刊 → 期刊名（如"中国针灸"），博士/硕士论文 → 学位授予单位（如"北京科技大学"）。`--doc-type phd/master` 通过 grid API 的 `Classid` 参数区分学位级别（博士=RMJLXHZ3，硕士=JQIRZIYA），URL 参数 `crossDbcodes`/`KuaKuCode` 无实际过滤效果。

万方 `--doc-type phd/master` 支持：自动切换 `/thesis` 搜索路径，并按 `essay-type` 字段后过滤博士/硕士。本科论文无公开检索平台（CNKI/万方均不收录，维普可能有少量覆盖）。

### IEEE 下载

IEEE 下载利用校园网 IP 自动获得机构认证（无需登录）。下载原理：

1. 访问 IEEE Xplore 建立会话（激活 IP 机构认证）
2. 通过 `stampPDF/getPDF.jsp?arnumber=XXX` 直接获取 PDF 字节流

限制：仅限机构订阅范围内的论文。部分早期/会议论文可能不在订阅范围内。

### CNKI cookie 管理

CNKI 源依赖校园网 IP 认证。首次使用需获取 cookie：

1. 运行 `~/.venvs/torch/bin/python tools/cnki_login.py`，弹出浏览器
2. 完成 CNKI 安全验证（拖动滑块）
3. Cookie 自动保存到 `cnki_cookies.json`

Cookie 有效期通常 1-2 天。过期时 blit 会自动弹窗让用户重新验证。

**注意**：`cnki_cookies.json` 包含会话信息，不应提交到 git。

### CAJ 转 PDF

CNKI 博士论文下载后通常是 CAJ 格式，需转换后才能用 `tools/convert` 转 markdown。

```bash
# 单篇转换
~/.venvs/torch/bin/python ~/.local/share/caj2pdf/caj2pdf convert input.caj -o output.pdf

# 批量转换（shell 目录下所有 .caj）
for f in *.caj; do ~/.venvs/torch/bin/python ~/.local/share/caj2pdf/caj2pdf convert "$f" -o "${f%.caj}.pdf"; done
```

安装位置：`~/.local/share/caj2pdf/`（从 GitHub 克隆），依赖 PyPDF2 + imagesize 已包含在 torch venv 中。已 patch 支持 pymupdf fallback：无 `mutool` 时自动用 `fitz` (pymupdf) 修复 xref，无需 sudo 安装 mupdf-tools。

### 使用策略

- **英文论文**：IEEE 主力
- **中文论文**：CNKI 主力（搜索+下载），万方低频补充
- **cbpt 已废弃**：CNKI 接口变更，cbpt 期刊子站不再可用
- **IP 被封**：停止使用万方，等自然解封（~15min+）

## 5. 中文检索策略

中文文献用 **blit**（CNKI/万方）而非 API 管线。`tools/search --mode chinese` 仅作快速概览。

```bash
# CNKI 搜索（默认搜期刊论文）
./tools/blit "低轨卫星 切换" --source cnki
./tools/blit "关键词" --source cnki --doc-type phd                # 博士学位论文
./tools/blit "关键词" --source cnki --doc-type master             # 硕士学位论文
./tools/blit "关键词" --source cnki --doc-type journal,phd        # 期刊+博士组合
./tools/blit "关键词" --source cnki --download papers/downloads/  # 搜索+下载
./tools/blit "关键词" --source wanfang                            # 万方补充
```

CNKI 初始化见 §4 "CNKI cookie 管理"。CAJ→PDF 转换见 §4 "CAJ 转 PDF"。

万方 `--doc-type phd/master` 支持学位论文检索（自动切换 `/thesis` 路径 + 按学位类型后过滤）。本科论文无公开检索平台。

## 6. 内容处理原则

- LaTeX 源文件（arXiv e-print）：公式表格完美，强制首选
- **不要整篇喂 agent**：精读阶段按章节拆分，title+abstract 用于初筛

## 7. 安装

```bash
# 单一 venv（搜索 + 下载 + 转换 + MinerU）
uv venv ~/.venvs/torch
~/.venvs/torch/bin/pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
~/.venvs/torch/bin/pip install "mineru[pipeline]"
~/.venvs/torch/bin/pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple \
  requests google-search-results tavily-python pymupdf pymupdf4llm
```

环境检查：

```bash
~/.venvs/torch/bin/python -c "import requests, pymupdf, pymupdf4llm, serpapi, tavily" && echo "OK"
~/.venvs/torch/bin/mineru --version
```

### API Key

`.env` 文件（已 gitignore）：

```
S2_API_KEY=xxx
SERPAPI_KEY=key1,key2,key3        # 多 key 逗号分隔
TAVILY_KEY=key1,key2              # 多 key 逗号分隔
FIRECRAWL_API_KEY=xxx
EXA_API_KEY=xxx
```

## 8. 工具引入检查 [FR-06]

> 防止新工具/数据源的完整操作链路仅存在于 commit 消息或 handoff 中，agent 靠试错发现流程。

每次引入新工具或数据源时，必须在本文档中记录以下信息后才能算"已集成"：

| 检查项 | 说明 |
|--------|------|
| 前置条件 | 认证方式（API key / 校园网 IP / Cookie）、系统依赖（Playwright / Chrome） |
| 完整操作链路 | 从搜索到最终可用的完整步骤（搜索→下载→转换→索引） |
| 已知限制 | 限速、付费墙、格式限制、IP 限制 |
| 常见失败模式 | 什么情况下会失败、失败的表现、恢复方法 |

不允许仅在 git commit 消息或 handoff 中隐含操作知识。工具首次成功使用后，同步更新本文档。
