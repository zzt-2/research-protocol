# 提示词：P0-3 + P0-4 中文检索策略 + 源路由修复

## 任务

修复中文检索的两个结构性问题：
1. 框架文档中完全缺失中文检索策略
2. `search_config.py` 的 chinese 模式源路由错误

## 背景

详见 `.session/framework-evolution/LOG-001-framework-issues-2026-05-15.md` 的 P0-3 和 P0-4。

核心问题：
- `MODE_SOURCES["chinese"]` 只有 `serpapi`，对中文学术搜索无效
- `DOC_TYPE_SOURCE_MAP["chinese_journal"]` 映射到 `exa`/`firecrawl`，对中文无效
- blit 的 CNKI/万方搜索能力无法通过 literature_search 调用
- 两者结果格式不一致
- CNKI 初始化流程（cnki_login.py）、CAJ 格式处理、期刊官网抓取等全部未文档化

## 要读的文件

1. `tools/litsearch/search_config.py` — MODE_SOURCES 和 DOC_TYPE_SOURCE_MAP 定义
2. `tools/litsearch/search_sources.py` — 各源搜索函数，理解集成点
3. `tools/blit.py` — CNKI/万方/IEEE 搜索和下载功能（重点读 CNKI 相关函数）
4. `tools/cnki_login.py` — CNKI cookie 获取流程
5. `tools-guide.md` — 当前工具文档
6. `stages/gw-search.md` — 当前检索流程定义

## 具体改动

### Part 1: 代码修复

**`tools/litsearch/search_config.py`**:
- 修正 `DOC_TYPE_SOURCE_MAP["chinese_journal"]`，映射到有效源
- 考虑 `MODE_SOURCES["chinese"]` 是否应包含更多源，或在文档中明确 chinese 模式应配合 blit 使用

**`tools/blit.py`**:
- CNKI 搜索增加 `--type journal` 参数支持（默认过滤学位论文）

**`tools/pdf_convert.py`**:
- 增加 CAJ 文件检测，给出明确提示："CAJ 格式不支持自动转换，请用 CAJ Viewer 手动转为 PDF"

### Part 2: 文档更新

**`tools-guide.md`** — 增加独立章节"中文检索策略"：
1. CNKI 初始化流程（运行 `cnki_login.py` → 过验证 → cookie 自动保存）
2. 期刊论文 vs 学位论文过滤（`--type journal`）
3. CAJ 格式处理说明
4. 期刊官网 HTML 全文抓取（webReader 备选路径）
5. CSSCI 核心期刊验证方法
6. blit 和 literature_search 的分工和结果合并方法

**`stages/gw-search.md`** — 在检索流程中增加中文检索的入口指引

## 约束

- 优先做文档更新（快速生效），代码修复作为第二优先级
- 不做 blit ↔ literature_search 的深度代码集成（工作量大），用文档化分工解决
- 保持 tools-guide.md 的中文用中文写
