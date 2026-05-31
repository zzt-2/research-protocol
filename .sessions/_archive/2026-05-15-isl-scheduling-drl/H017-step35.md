# 新对话提示词：ISL Scheduling + DRL — Step 3.5 补充检索 + 竞品精读

## 任务

为"LEO 星座 ISL 调度 + DRL"方向执行 GW Step 3 剩余（竞品精读）+ Step 3.5（定向补充检索）。

## 状态恢复

按以下优先级读取：
1. 项目记忆：`~/.claude/projects/-mnt-d-code-study-research-protocol/memory/project_leo-isl-scheduling-drl.md`
2. 最新 handoff：`projects/leo-isl-scheduling-drl/sessions/2026-05-15-handoff-2.md`
3. 精读产出：`projects/leo-isl-scheduling-drl/literature_notes.md`
4. 框架文件：`stages/gw-supplement.md`（Step 3.5 流程）、`stages/gw-read.md`（精读模板）

## 待做事项

### 1. 竞品精读（Step 3 补充）

已下载并转换就位的 4 篇竞品（全部可直接精读）：
- **Wang TCOM 2024**（MADRL 激光 ISL 调度）：`papers/manual/wang-tcom-2024-madrl-laser-isl/content.md`（713 行）
- **Guo TWC 2024**（分布式拓扑优化）：`papers/manual/guo-twc-2024-distributed-topo/content.md`（772 行）
- **Wang TWC 2024**（联邦 RL 激光 ISL）：`papers/manual/wang-twc-2024-federated-rl-isl/content.md`（715 行）
- **Pi ICC 2022**（MADDPG ISL 规划）：`papers/manual/pi-icc-2022-maddpg-isl/content.md`（325 行）

精读按 `gw-read.md` 模板提取，追加到 `literature_notes.md` 的"待补充论文"部分。

### 2. 定向补充检索（Step 3.5，必做）

基于精读产生的综合分析，做一轮定向检索弥补盲区。重点方向：
- **DRL/RL 在 ISL 调度中的最新应用**（当前仅 SatFlow 1 篇用 MARL，可能有遗漏）
- **激光 ISL 建立/切换时延建模**（仅 L04 考虑 setup delay，需补充）
- **GNN + DRL 联合优化**（DeepLaDu 用 GNN 但非 DRL，需找 GNN+DRL 结合的文献）

读 `stages/gw-supplement.md` 执行完整流程。检索用 `tools/search`，结果存 `search-archive/2026-05-15/`。

### 3. 更新 literature_notes.md

补充检索后如有新论文下载成功，追加精读并更新综合分析。

### 4. 更新 handoff

完成后写 handoff 到 `projects/leo-isl-scheduling-drl/sessions/2026-05-15-handoff-3.md`。

## 约束

- 工具从项目根目录调用：`cd /mnt/d/code/study/research-protocol && ...`
- 子 agent 最多 3 个并发
- 论文全文精读在子 agent 中执行
- 单对话不超过 3 步
- PDF 转换必须用 `tools/convert`
