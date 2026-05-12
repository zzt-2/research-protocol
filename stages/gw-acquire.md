# 下载 + 转换 + 质量门（gw-acquire）

## 入参
- `search-archive/{date}/{slug}.json` 中的"必读"+"建议读"论文列表
- 已有论文：`papers/{arxiv|doi}/{id}/content.md`（跳过已下载的）

## 出参
- `papers/{arxiv|doi}/{id}/content.md`（各论文的 markdown 全文）
- 覆盖面缺口报告（阻塞门）

## 操作

1. **相关性过滤**（下载前）：从搜索结果中筛选"必读"+"建议读"的论文（约 8-12 篇），**排除与研究方向不直接相关的论文**
2. 用 `tools/download` 批量下载，先 `--dry-run` 预览
3. 成功的论文自动转为 markdown 存入 `papers/{arxiv|doi}/{id}/`
4. **内容质量检查**（下载后，逐篇执行）：
   ```bash
   wc -l papers/{arxiv|doi}/{id}/content.md
   # 行数 < 50 或文件只有标题/节名 → 标记为 failure，不进入精读
   ```
5. 下载失败的论文列出来交给用户，由用户决定是否手动下载

### 环境检查（运行脚本前）

确认 Python 环境和依赖可用：

```bash
~/.venvs/torch/bin/python -c "import requests, pymupdf, pymupdf4llm, serpapi, tavily" && echo "OK"
```

- 通过 → 正常运行脚本
- 缺依赖 → 安装：`~/.venvs/torch/bin/pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple {包名}`
- venv 不存在 → 创建：`uv venv ~/.venvs/torch && ~/.venvs/torch/bin/pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple requests google-search-results tavily-python pymupdf pymupdf4llm`
- Python 本身不可用 → 停止，报告用户

### 止损规则（硬性）

下载失败是常态，不是异常。严格遵守以下流程：

1. **第一轮**：用 `tools/download` 批量下载
2. **第二轮（仅一轮）**：为第一轮失败的论文搜索 arXiv 版本，再次尝试下载
3. **停止**：两轮后仍然失败的论文 → 进入覆盖面缺口报告

**绝对禁止**：
- 用 web reader、网页抓取等工具获取论文全文——会往上下文灌入大量 HTML，撑爆上下文
- 尝试从 ResearchGate、Semantic Scholar 等页面提取论文内容
- 超过两轮的任何下载尝试

> 试跑教训：12 篇论文只有 2 篇下载成功，agent 没有止损，而是用 web reader 逐篇抓取 ResearchGate/Semantic Scholar 页面，每次抓取灌入大量 HTML，最终撑爆上下文。大部分 IEEE 论文无法自动获取是常态，不是 agent 的问题。

### 覆盖面缺口报告（阻塞门）

下载完成后，**必须**生成覆盖面缺口报告并**等待用户确认**：

```markdown
## 文献覆盖面状态
- 成功获取：{N} 篇（{列出标题}）
- 内容质量不达标：{N} 篇（{列出 ID 和原因}）
- 下载失败（用户待获取）：{N} 篇（{列出标题 + DOI/来源}）

### 覆盖面分析
- 当前精读论文全部来自 {arXiv/...}，可能遗漏 {IEEE/...} 的高相关论文
- 下载失败中与研究方向最相关的：{列出，标注为什么重要}

### 引用质量分析
- 正式发表：{N} 篇（{列出}）
- 预印本：{N} 篇（{列出}）
- 预印本占比：{N/M = X%}
- 预印本中可能已发表的（arXiv 超 1 年）：{列出}

### 用户行动项（引用质量）
- [ ] 检查上述预印本是否有正式发表版本
- [ ] 如果预印本占比 >50%，用 `tools/blit --source ieee` 补充正式发表文献检索

### 用户行动项
- [ ] 手动获取上述失败论文，放入 `papers/manual/{slug}/` 并创建 metadata.json，或确认当前覆盖面可接受
```

**核心原则**：失败下载清单是阻塞项，不是建议。当前精读范围受下载通道限制（主要是 arXiv），agent 必须明确告知用户这个偏差。

> 试跑教训（F4）：6 篇精读全部来自 arXiv，IEEE 付费墙里的高相关论文没读过。文献认知系统性偏向有预印本的论文——协议没把"下载失败 = 覆盖面缺口"建立为阻塞门。

## 质量门槛

- ≥5 篇核心论文已成功转为 markdown
- **内容质量**：每篇 content.md ≥50 行有效内容（非纯标题/节名）
- 转换质量目视可接受（公式/表格没有大面积乱码）

## 不达标时

- 成功转换 <5 篇 → 用户手动补充下载，或换下载通道
- 内容质量不达标 → 对关键论文换 `--quality standard` 或 `--quality high` 重试

## 人介入

[MUST] 覆盖面缺口报告必须经用户确认后方可继续。

> 首次试跑教训：子 agent 一步到位做"筛选 + 写 literature_notes"，结果只产出搜索元数据级别的浅分析。根本原因是没有实际读论文内容，只有 title + abstract。分步执行、先下载再精读，是防止这个问题的硬性流程。
