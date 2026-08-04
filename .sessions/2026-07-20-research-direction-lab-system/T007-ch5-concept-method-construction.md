# Task Brief: Ch5 概念方法构造批次 001

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 15
  action_class: CONCEPT_METHOD_CONSTRUCTION
  mission_checkpoint: CP004
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S015 / D023 / CP004 | 产出位置: `projects/thesis-fso/direction-lab/harvest/ch5-concept-method-batch-001.md`
> 日期: 2026-08-04
> 唯一任务: 为学位论文 Ch5 构造并筛选一批部署/计算流程型完整方法原型

## 0. TL;DR

在 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
执行一个 **design-only** 方法构造批次。运行前确认当前分支为
`codex/rdl-method-production-v2`，并以包含本任务书的 HEAD 为事实基点。

T006 的 Ch4 C3 因漏检历史 D-011/D-009 被主控撤回；本轮不修 C3，也不继续 selector
校准族，而是把候选来源切换到 Ch5 的 **部署、计算流程、跨模块复用、近似计算和资源约束**。
构造 3–5 个机制不同的完整方法原型，最多保留 1–2 个 survivor。

最高纪律：

1. 不跑仿真、benchmark、综合、代码、held-out、统计或 oracle；不调用 web/search，不下载论文。
2. 不把“只执行一支”、Q(8,6)、单一字长、resource proxy、测试平台或 bugfix 再包装成方法。
3. 不假定 inventory 穷尽历史。每张卡必须从 action signature 派生 3–6 个中英文检索词，
   用 `rg` 定向扫描 `.sessions/**/decisions.md`、`projects/thesis-fso/worker-logs/`、
   `thesis-lessons.md` 和 harvest；命中后回读原始证据。
4. 只新增一个产出文件，不修改 Skill、inventory、`.sessions/`、论文正文、科学代码或状态文件。
5. 最终一次 commit，不 push；四个既有 `p05_run*.log` 不修改、不暂存。

## 1. 必读与事实边界

按顺序读取：

1. `.agents/skills/research-direction-lab/SKILL.md`；
2. `.agents/skills/research-direction-lab/references/method-production.md` 的
   `Concept construction batch`；
3. `.sessions/2026-07-20-research-direction-lab-system/R006-lightweight-method-construction-lane-design.md`；
4. `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`；
5. `projects/thesis-fso/direction-lab/harvest/ch4-concept-method-batch-001.md` 顶部主控修订；
6. `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md` 中 R3/R4、低复杂度、
   计算图、定点/硬件相关卡；
7. `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`；
8. `projects/thesis-fso/direction-lab/harvest/asset-claim-matrix.yaml`；
9. T005 产出及其终态证据；
10. `.sessions/2026-07-06-step4a-mve-execution/decisions.md` 的 D-009/D-011。

已知禁区：CCISP 已含 select-before-execute；T005 已判 single-branch scheduling 与 CCISP
动作重复；P03 只支持 Q(8,6) 数值可行性且 mixed precision 增益薄；P09 的 early-stop
成本记账无效；A1 adaptive-K 已否决。上述对象不得换名重开。

## 2. 构造要求

先画当前接收链的本地计算/数据流，再构造 3–5 张卡。候选至少跨 3 种动作机制，例如：

- 跨模块中间量复用或联合计算图；
- 分级/粗细两阶段计算，但必须真实少算而非事后少记；
- 硬件友好近似或稀疏更新，但不能只是固定字长；
- 并行/流水/缓存调度带来的新执行合同；
- 性能约束下的动态计算预算分配，但不能复刻 selector 分支或 P09 恒定 early-stop。

这些只是生成源，不预设任何一类必须成卡。每张原型卡必须完整包含：

1. 章节槽位与方法名；
2. `M-C-A`；
3. receiver-visible 输入、动作、输出；
4. 5–8 步算法流程；
5. 相对 CCISP 和当前 inventory 的新增点；
6. 传统 comparator 与 strongest cheap alternative；
7. 主图、核心消融、最小实现切片；
8. 可诚实写出的 claim ceiling 与失败 fallback；
9. `[FACT] / [INFERENCE] / [HYPOTHESIS]` 分层；
10. action-signature 历史检索词、命中路径与结论；
11. 五行 collision receipt：existing action collision / historical dead end /
    strongest cheap alternative / reopen condition / classification
    (`NEW_ACTION / EXTENSION / ENGINEERING_COMPONENT / REJECT`)。

## 3. 筛选与终态

先比较核心动作，再考虑闭合成本：

- 部署动作是否真实发生并改变执行路径；
- 是否相对已有贡献产生独立 action delta；
- 复杂度下降是否可由真实调用数/操作数/延迟定义，而非 proxy 或记账；
- 是否会被常规缓存、固定参数、编译器优化或现有 CCISP action 吸收；
- 是否能形成算法、主图、消融、baseline 和失败边界的一章；
- 最小验证是否能在现有资产上完成。

只允许以下终态：

- `CONCEPT_SURVIVOR_AVAILABLE`：保留 1–2 个；只写其应从哪个 GW Step 1 问题定义开始。
- `NO_CONSTRUCT_SURVIVES`：全部碰撞/被廉价方案吸收；指出下一批必须更换的候选来源或研究对象。
- `EXISTING_ASSET_READY`：发现 inventory 过期且已有完整 Ch5 方法；给证据并停止构造。

若 survivor 的成立依赖尚不存在的 RTL/FPGA 工具链，可以保留为候选，但必须把 testbed
成本和 claim ceiling 写清；不能把“未来可综合”当已有证据。

## 4. 唯一产出文件

新增：

`projects/thesis-fso/direction-lab/harvest/ch5-concept-method-batch-001.md`

固定结构：Terminal verdict / Current computation-action map / Prototype cards /
Cross-card comparison / Survivor(s) and why / Next formal entry。

不要生成 worker-log、receipt、verifier、raw artifact、D/V/S/H 或新 registry。

## 5. 验收与提交

提交前检查：

- 原型数 3–5，至少 3 种动作机制；
- 每张卡 11 项字段齐全；action-signature 检索可复核；
- survivor ≤2，且没有复活 T005/P03/P09/A1；
- 无 web/search、仿真、benchmark、代码和科学 claim；
- `git diff --check` 通过；diff 只有唯一产出文件；
- 单次 commit，不 push。

最终只回五项：terminal verdict；原型列表；survivor 与 collision 结论；产出路径；commit SHA。
