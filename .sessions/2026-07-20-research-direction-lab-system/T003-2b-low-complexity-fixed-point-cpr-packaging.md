# Task Brief: 2B Low-Complexity Branch-Routed and Fixed-Point CPR 包装诊断

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

你在 `D:/code/study/research-protocol` 的隔离 worktree 中。你的任务不是跑实验，而是判断 branch preselection、single-branch execution 与 Q(8,6) 能否诚实组织成学位论文 Ch5 的一个低复杂度部署方法，并把唯一 bounded package 设计到可直接执行。

**产出**：一份 2B 方法包装诊断，最终明确 `THESIS_METHOD_READY / NEEDS_ONE_BOUNDED_PACKAGE / SUPPORTING_ONLY / REJECT`。

**最高纪律**：

1. 不运行仿真/benchmark/综合，不改代码/文件，不 commit，不写正式论文正文。
2. Q(8,6)、990/990 identity、0/132000 mismatch 都只是组件/验证事实，不能单独冒充方法。
3. 必须计算完整链的真实成本口径，包含 preselect/controller；禁止复活 74.6% 总接收机复杂度声称。
4. 没有 FPGA 综合时只能设计 CPU timing、operation/storage 与 matched-performance 的窄合同；不得声称 LUT/DSP/功耗。
5. 只设计一个 bounded package，不扩建硬件平台或开新方向。

## 1. 背景

CCISP 已能在执行前决定 DA/NDA 分支。历史 route-B 代码表明 preselect 后只执行所选分支，与 route-A 双分支后选择在 990/990 cells 的选中输出一致。P03 表明统一 Q(8,6) 在 132000 次 selector 决策中与 float 一致，mixed precision 没有独立增量；但正式 full-grid timing、float-vs-Q 端到端性能和真实硬件资源尚未闭合。候选 2B 的统一链是：

`quantized receiver statistic → fixed-point controller → preselect → execute one branch`

## 2. 必读证据

1. `.agents/skills/research-direction-lab/SKILL.md`
2. `.agents/skills/research-direction-lab/references/method-production.md`
3. `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
4. `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`
5. `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md`
6. `projects/thesis-fso/direction-lab/harvest/asset-claim-matrix.yaml`
7. `projects/thesis-fso/worker-logs/step-030-p03-fixed-point-codesign.md`
8. `projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_branchrouted_30seed.py`
9. `projects/simulation/paper/ccisp2026/sections/method.tex`

## 3. 必须回答的问题

### 3.1 方法身份

- 最合适的方法名与一句话 contribution；
- 精确 M-C-A；
- quantized statistic、controller、preselect、single branch、output 的完整链；
- 与 Ch3 CCISP 的独立性，以及 route scheduling 与 numeric representation 如何组成一个方法而非两个零碎点。

### 3.2 对照与成本合同

- baseline ladder：route-A dual-branch float、route-B single-branch float、route-B Q ladder；
- 完整 operation count、wall-clock latency/throughput、memory/storage 应怎样定义；
- warm-up、重复次数、平台冻结、输入输出等价和性能非劣如何同时保证；
- 无 FPGA 工具时的最高合法 contribution ceiling。

### 3.3 唯一 bounded package

给出一个统一包：覆盖 formal grid 的 route timing/operation 分解 + float-vs-Q 端到端性能；若仓库已有合法综合工具才把综合列为可选扩展，否则明确不要求。冻结 primary metric、MDE/非劣门、方法集合、消融、主图、PASS/FAIL disposition。不要实际执行。

### 3.4 章节可写性

给出：算法步骤、建议框图、complexity table、1 张主图 + 1 张位宽消融表、claim ceiling、不能说什么。不要写章节正文。

## 4. 已知陷阱

- 不能先计算双分支再少报一个分支的成本；真实 caller path 必须先选后算。
- bit-exact/decision identity 只证明正确性，不证明成本收益。
- proxy 只能支持 proxy 结论；没有综合就不写 FPGA 面积/功耗。
- 若 full-chain timing 无下降，2B 必须降为 `SUPPORTING_ONLY`，不能靠换成本口径保章。

## 5. 强制输出格式

1. `Verdict`
2. `最强可包装版本`（方法名、M-C-A、I-A-O）
3. `为什么是完整部署方法而非两个组件`
4. `baseline ladder 与真实成本口径`
5. `唯一 bounded package 合同`
6. `算法/框图/主图/消融`
7. `claim ceiling 与失败降级`
8. `给主控的一句话下一动作`

## 6. 验收

- [ ] 没有运行或修改任何科学资产
- [ ] 成本口径包含 controller/preselect
- [ ] Q(8,6) 只作统一链的实现点
- [ ] bounded package 只有一个且可判定
- [ ] 没有 74.6% 或 FPGA 无证据外推
