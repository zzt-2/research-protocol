---
project: thesis-fso
direction: 星地湍流激光通信（FSO）——载波同步/信道估计/资源调度方向待精读后从问题清单浮出
method_type: 待定（精读后根据问题方法产出形态确定，见 glossary 判据 2）
domain: comms
created: 2026-06-21
updated: 2026-06-21
current_step: GW-Step-2
current_stage: GW
---

# Master Agent: thesis-fso

> 本文件 2026-06-21 由框架改造 3（缺陷 C 状态层修复，LOG-001）补建。
> 补建前 thesis-fso 无 master-state.md，跨 Step 无硬门控——agent 在 Step 2/3/3.5/4a 全 ⬜ 的真空里跑了 5 个方向（N1/③/A3/4b#1/(c)）全 Kill。本文件 + GW Progress 表把跨 Step 硬门控（FR-22）落到磁盘。

## §1 角色定义

你是研究项目 `thesis-fso` 的 Master 编排 agent。职责见 `templates/master-state-template.md` §1。禁止项同模板（不直接读论文 content.md / 不直接 WebSearch / 不跑长脚本 / 未经用户确认不做 Go-NoGo / 同时只开一个子 agent）。

## §2 项目状态

### 当前位置

- 阶段：GW
- 步骤：Step 2（论文获取）—— **下一步实际是回到 Step 3 精读**（见 H002 路径 A，但 Step 2 尚未完成，需先补获取）
- Contract 状态：not started
- 方法类型：待定

### 项目级参数（glossary 四判据 3/4 的当前值）

- 判据 3 baseline 年份范围：**2019 年至今顶刊**（导师"近 5-8 年"，2026-06-20 voice.md）
- 判据 4 对标数量：**每章 1-2 个对标对象**（导师原话，2026-06-20 voice.md）

> 这两个值是 glossary.md 判据 3/4 的项目级参数，记录在本项目档案里（不写进跨项目的 glossary）。

> **重定方向背景**（见 `.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/H002`）：导师反馈后，研究起点从"找空白/试方法"转为"按问题找"。方法形态必须从 GW Step 3 精读浮出，不从开题报告反推。下一轮第一步 = 路径 A（回 Step 3 精读，问题清单从精读浮出，过四判据筛）。

### GW Progress（跨 Step 硬门控，单一事实源）[MUST]

| Step | 状态 | 完成日期 | commit | 关键产出 | 下游门控 |
| ---- | ---- | -------- | ------ | -------- | -------- |
| 1 search | ✅ | 2026-05-29 | — | search-archive + literature_notes 检索统计 | — |
| 2 acquire | ⬜ | | | papers/*/content.md | 进 Step 3 前 Step 1 必 ✅（已满足）|
| 3 read | ⬜ | | | literature_notes.md（含**研究问题清单 Q#**） | **进 Step 3.5/4a 前必 ✅，且 Q# 清单非空** |
| 3.5 supplement | ⬜ | | | 更新 literature_notes.md | 进 Step 4a 前必 ✅ |
| 4a feasibility | ⬜ | | | feasibility_report.md | **进 Step 5/Contract/MVE 前必 ✅（Go 决策已记录）** |
| 5 validate | ⬜ | | | Baseline 候选表 | 进 Step 4b 前必 ✅ |
| 4b sim-feasibility | ⬜ | | | feasibility_report.md (C/E) | 进 Step 6 前必 ✅ |
| 6 sim-design | ⬜ | | | 仿真器设计规格 | 进 Step 7 前必 ✅ |
| 7 implement | ⬜ | | | baseline_report.md | — |

**硬门控规则（FR-22）**：进入任何下游步骤前先查本表——上游任一项 ⬜ = 禁止进入下游。Step 3 + Step 4a 是 Go/No-Go 硬门不可跳过。本表/literature_notes 进度表任一上游项 ⬜ 时，**禁止进 MVE/Contract/任意"试方法"动作**。跨对话恢复优先读本表。

> **历史教训锚点**（5 次殊途同归全 Kill）：N1(PCS) / ③(MCS排程) / A3(pilot CPE) / 4b#1(自适应交织) / (c)(GG-LLR译码) 全部发生在 Step 1 ✅ 之后、Step 3-4a 全 ⬜ 的真空地带。根因：C1(信道设定)+C2(目标=BER)+C3(单链路DSP) 三轴锁死。详见 `.sessions/2026-06-19-4b1-adaptive-interleaving-groundwork/S004`。

### 关键决策

- decision_log.md 尚未创建（待补）。关键历史决策散落在 `.sessions/`：
  - 4b#1 Kill（自适应交织）：`.sessions/2026-06-19-4b1-.../decisions.md` D001
  - (c) Kill（GG-LLR）：同上 D002
  - 重定方向 v2（问题驱动）：H002
  - 框架护栏 FR-22/23/24、TL-30/31：AGENTS.md + thesis-lessons.md

### 活跃文件

- literature_notes.md: projects/thesis-fso/literature_notes.md（Step 1 进度表已填，Step 2/3/3.5 ⬜；研究问题清单 Q# 待精读后产出）
- thesis-framework.md / cnki-thesis-survey.md: projects/thesis-fso/
- decision_log.md: 待创建
- feasibility_report.md / baseline_report.md: 未创建

## §3 步骤调度表 / §4 FR 防坑清单

见 `templates/master-state-template.md` §3 / §4。本文件不再重复。

## §8 下一步（路径 A，H002）

1. 读 `stages/gw-read.md`（FR-22，进 Step 3 必先读）+ `stages/glossary.md`（问题四判据）
2. **批评汇总先于精读**（见 `.sessions/2026-06-20-problem-driven-redirection/` H001/S001）：派子 agent 用 `tools/search` 汇总星地 FSO 物理层链路 + 目标函数两轴的批评信息（批评维度 / 被批方法 / 时效检查三层）
3. **精读对象由批评汇总结果决定，不由开题线索反推**——Paillier 2020 等开题 4 线索（VV窗口/DPLL/SEP/编码辅助）已降级为事后验证对照（见 S001 第四步 + 不变量 3）
4. Step 3 精读：子 agent 读 content.md，按 gw-read.md 结构化提取 7 子表（含问题提取 M/C/A+四判据）
5. 精读 2-3 篇后：问题清单 Q# 从精读浮出 → 过四判据 → 选 1 个进 Step 4a
6. 同步更新本文件 GW Progress 表 + literature_notes 进度表

## §9 失败恢复

见 `templates/master-state-template.md` §9。恢复优先级：本文件 → `.sessions/` 最新 H### → stage file → decision_log。
