# 新对话提示词：GNN-based LEO Routing — GW Step 2-3 恢复

## 任务

恢复 GNN-based LEO mega-constellation routing 方向的 Groundwork Step 2-3。用户已手动下载 IEEE 论文，需要转换、精读、更新 literature_notes.md，然后确认覆盖面后进入 Step 3.5 → Step 4a。

## 背景

上一轮对话完成了：
- 项目目录创建和初始化
- 7 篇 arXiv 论文下载和精读
- `literature_notes.md` 综合分析（7 篇精读 + 5 篇浅读）
- 覆盖面缺口报告：5 篇 IEEE 必读论文在付费墙后

用户选择"先获取论文再继续"。

## 恢复步骤

### Step 0：读文件恢复上下文（必须）

1. `projects/leo-mega-constellation-gnn-routing/sessions/2026-05-13-handoff.md` — 交接上下文
2. `projects/leo-mega-constellation-gnn-routing/literature_notes.md` — 当前精读产出
3. `stages/groundwork.md` §Step 3-3.5 — 精读完成后的流程
4. `stages/gw-read.md` — 精读模板（如果需要补充精读）
5. `stages/gw-acquire.md` — 覆盖面确认规则

### Step 1：检查新论文

检查 `papers/doi/` 下是否有用户新放入的 PDF：

- `papers/doi/10.1109_nfv-sdn61811.2024.10807492/` — **L08（最关键）**
- `papers/doi/10.1109_tvt.2024.3396350/` — L11
- `papers/doi/10.1109_jiot.2025.3638842/` — L09
- `papers/doi/10.1109_tmc.2025.3570670/` — L10
- `papers/doi/10.1109_jiot.2025.3576912/` — L12

也检查 `papers/downloads/2026-05-13/` 是否有新文件。

### Step 2：转换 + 精读

对每篇新论文：
1. `bash tools/convert papers/doi/{path}/source.pdf --quality standard` 转 markdown
2. 按精读模板提取结构化数据
3. **特别关注 L08**：是否已解决 GNN+LEO 路由？是否涉及 size generalization？

### Step 3：更新 literature_notes.md

将新精读结果补充到 literature_notes.md，更新综合分析（尤其是"创新空间确认"部分）。

### Step 4：确认覆盖面 → Step 3.5 → Step 4a

覆盖面确认后：
1. 执行 Step 3.5 定向补充检索
2. 进入 Step 4a 方向根基 Go/No-Go

## 约束

- 工具调用从项目根目录：`cd /mnt/d/code/study/research-protocol && ...`
- 子 agent 最多 3 个并发
- 论文路径合规：`papers/{arxiv|doi|manual}/{id}/`
- L08 的结论决定方向是否继续——如果核心创新已被发表，需与用户讨论调整
