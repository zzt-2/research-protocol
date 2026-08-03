# Task Brief: 2A Calibration-Aware Robust Adaptive CPR 包装诊断

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v1
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 10
  action_class: THESIS_PACKAGING_TASK_DISPATCH
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S015 | 产出位置: 当前 Codex 任务最终回复（只读，不落科学结论）
> 日期: 2026-08-03
> 唯一文档: 执行方先读本 T，再按必读清单读取仓库证据

## 0. TL;DR（执行方先读）

你在 `D:/code/study/research-protocol` 的隔离 worktree 中。你的任务不是跑实验，而是判断现有 P01/P02/CCISP 能否诚实组织成学位论文 Ch4 的一个方法，并把唯一 bounded package 设计到可以下一对话直接执行。

**产出**：一份 2A 方法包装诊断，最终明确 `THESIS_METHOD_READY / NEEDS_ONE_BOUNDED_PACKAGE / SUPPORTING_ONLY / REJECT`。

**最高纪律**：

1. 不运行仿真、不改代码/文件、不 commit、不写正式论文正文。
2. 不把 `cand_rank` 或 `ref 9→11 dB` 单独包装成新方法；它们最多是被否决候选或校准规则组件。
3. 必须区分 offline region retune 与 receiver-visible online estimator→calibration→branch action；若二者没有独立信息/动作增量，诚实否决 2A。
4. `METHOD_SIGNAL=0` 不自动否决论文方法章；但 artifact、truth leakage、无真实 action 仍直接拒绝。
5. 只设计一个 bounded package，不继续扩成新方向或多轮研究计划。

## 1. 背景

现有主方法 CCISP 用 receiver-visible 统计量在 DA/NDA CPR 间选择。P01 发现名义 SNR ±3 dB 失配可造成约 0.32–0.70 dB 损害，pilot-SNR adapter 恢复 4/5 个 harm cells。P02 发现复杂 `cand_rank` 的局部收益可被常规 weak-region retune 吸收，因此 `cand_rank` 不是方法信号。候选 2A 的统一链是：

`pilot-SNR estimator → operating-region calibration → CCISP branch action`

目标是判断这条链是否比“离线把一个阈值重调好”多出一个诚实、可部署、可写步骤和主图的方法增量。

## 2. 必读证据

1. `.agents/skills/research-direction-lab/SKILL.md`
2. `.agents/skills/research-direction-lab/references/method-production.md`
3. `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
4. `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`
5. `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md`
6. `projects/thesis-fso/worker-logs/step-028-p01-cpr-snr-mismatch.md`
7. `projects/thesis-fso/worker-logs/step-029-p02-cand-rank-operating-regime.md`
8. `projects/simulation/paper/ccisp2026/sections/method.tex`
9. `projects/simulation/paper/ccisp2026/sections/results.tex`

## 3. 必须回答的问题

### 3.1 方法身份

- 最合适的方法名与一句话 contribution；
- 精确 M-C-A；
- 输入、状态估计、校准动作、branch action、输出；
- 与 Ch3 CCISP 的独立性在哪里，哪些只是参数而非方法。

### 3.2 对照与反解释

- baseline ladder：original CCISP、global retune、region retune、完整 2A；oracle 仅作上界；
- 最强 cheap alternative 是什么；
- 什么证据能证明 online estimated-SNR calibration 不是 offline retune 换名；
- weak@9 残余会否否决整章。

### 3.3 唯一 bounded package

给出可以直接冻结为实验合同的最小设计：cell/grid、dev/test 隔离、paired unit、primary metric、MDE/通过门、信息边界、方法集合、消融、主结果图、PASS/FAIL 后各自 disposition。不要实际执行。

### 3.4 章节可写性

给出：算法步骤、建议框图、核心公式对象、1 张主图 + 1 张消融表、claim ceiling、不能说什么。不要写章节正文。

## 4. 已知陷阱

- P02 的结论只关闭 `cand_rank`，不能无分析地抹除 P01 adapter；反过来也不能用 4/5 恢复直接证明完整 2A。
- true SNR、TX truth、真实 GG 标签不得进入 deployable action。
- 不能把固定 11 dB、weak 标签或 estimator 名称单独当创新。
- 不能用“每章需要方法”倒推 PASS；包装失败就输出 `SUPPORTING_ONLY`。

## 5. 强制输出格式

1. `Verdict`
2. `最强可包装版本`（方法名、M-C-A、I-A-O）
3. `为什么不是参数换名`
4. `baseline ladder 与 cheap alternative`
5. `唯一 bounded package 合同`
6. `算法/框图/主图/消融`
7. `claim ceiling 与失败降级`
8. `给主控的一句话下一动作`

## 6. 验收

- [ ] 没有运行或修改任何科学资产
- [ ] 明确区分 P01 adapter 与 P02 retune
- [ ] bounded package 只有一个且可判定
- [ ] PASS 与 FAIL 都有诚实去向
- [ ] 输出能让主控下一轮直接决定是否派实验
