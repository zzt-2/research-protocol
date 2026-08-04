# Task Brief: Ch4 概念方法构造批次 001

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-20-research-direction-lab-system/topic-index.md
  control_epoch: 14
  action_class: CONCEPT_METHOD_CONSTRUCTION
  mission_checkpoint: CP003
```
<!-- RDL-TASK-CONTROL:END -->

> 来源: S015 / D023 / CP002 | 产出位置: `projects/thesis-fso/direction-lab/harvest/ch4-concept-method-batch-001.md`
> 日期: 2026-08-04
> 唯一任务: 为学位论文 Ch4 构造并筛选一批完整方法原型

## 0. TL;DR

在 worktree `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
执行一个 **design-only** 方法构造批次。当前基线提交为
`ffa26b5ef797ae710696462a2e011f68dadf2b97`，分支
`codex/rdl-method-production-v2`。

围绕 Ch4“CCISP 之后的校准、鲁棒或接收机适配方法”，先从本地既有资产和同行
recipe 构造 **3–5 个机制不同的完整方法原型**，再做已有动作、历史 dead end 和
strongest cheap alternative 碰撞检查，最多保留 1–2 个 survivor。

最高纪律：

1. 不跑仿真、代码、held-out、统计或 oracle；不调用 web/search，不下载论文。
2. 不把“换场景、补验证、画统一表、调一个常数”包装成方法；必须有真实的新动作链。
3. 不预设 2A 一定存活；T004 已被 regional retune 吸收，T005 已与 CCISP 动作碰撞。
4. 不只检查 CCISP；使用当前 inventory 中所有方法、组件、invalidated 和 dead-end。
5. 只新增一个产出文件，不修改 Skill、`.sessions/`、state/portfolio、论文正文或科学代码。
6. 最终一次 commit，不 push；四个既有 `p05_run*.log` 不修改、不暂存。

## 1. 必读与事实边界

按顺序读取：

1. `.agents/skills/research-direction-lab/SKILL.md`；
2. `.agents/skills/research-direction-lab/references/method-production.md` 的
   `Concept construction batch`；
3. `.sessions/2026-07-20-research-direction-lab-system/R006-lightweight-method-construction-lane-design.md`；
4. `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`；
5. `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md`；
6. `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`；
7. `projects/thesis-fso/direction-lab/harvest/conference-to-thesis-map.md`；
8. `projects/thesis-fso/direction-lab/harvest/asset-claim-matrix.yaml`。

已知事实只作边界，不作答案：CCISP 是当前唯一 ready 主方法；Ch4 尚无 ready 方法；
2A/T004 被廉价 region retune 吸收；2B/T005 的 single-branch action 与 CCISP
select-before-execute 重复。任何进一步事实声称必须给本地 `path:line`。

## 2. 构造要求

先从 recipe library 与内部组件做组合推演，再写 3–5 张卡。候选至少跨 3 种动作
机制；不得全部是 threshold/region retune。允许的候选来源包括 estimator、校准器、
状态记忆、置信度控制、分支协调、计算图或部署约束，但必须形成真实
`receiver-visible input → action → output`。

每张原型卡必须完整包含：

1. 章节槽位与方法名；
2. `M-C-A`；
3. receiver-visible 输入、动作、输出；
4. 5–8 步算法流程；
5. 相对 CCISP 和当前 inventory 的新增点；
6. 传统 comparator 与 strongest cheap alternative；
7. 主图、核心消融、最小实现切片；
8. 可诚实写出的 claim ceiling 与失败 fallback；
9. 事实、推断、假设分别标为 `[FACT] / [INFERENCE] / [HYPOTHESIS]`；
10. 五行 collision receipt：
   - existing action collision；
   - historical dead end；
   - strongest cheap alternative；
   - reopen condition；
   - classification：`NEW_ACTION / EXTENSION / ENGINEERING_COMPONENT / REJECT`。

## 3. 筛选与终态

先比较核心动作，再考虑证据闭合成本。排序维度只有五个：

- 动作是否真实且可部署；
- 是否与既有 contribution 重复；
- 是否会被廉价传统方案吸收；
- 是否能形成算法、主图、消融和 baseline 的完整一章；
- 最小实现是否可在现有资产上完成。

只允许以下终态：

- `CONCEPT_SURVIVOR_AVAILABLE`：保留 1–2 个，并分别给出下一步应从哪个 GW Step 1
  问题定义开始；不写实验任务。
- `NO_CONSTRUCT_SURVIVES`：全部碰撞或被廉价方案吸收；明确下一批应更换哪种候选来源，
  不继续修同一标签。
- `EXISTING_ASSET_READY`：发现 inventory 判断过期，已有完整 Ch4 方法；给证据并停止构造。

原型 survivor 不是 METHOD_SIGNAL、不是 Go，也不能进论文正文。

## 4. 唯一产出文件

新增：

`projects/thesis-fso/direction-lab/harvest/ch4-concept-method-batch-001.md`

固定结构：

1. `Terminal verdict`
2. `Existing contribution/dead-end map`（紧凑表）
3. `Prototype cards`（3–5 张完整卡）
4. `Cross-card comparison`
5. `Survivor(s) and why`
6. `Next formal entry`（只写 GW 入口，不写实验）

不要生成 worker-log、receipt、verifier、raw artifact、D/V/S/H 或新 registry。

## 5. 验收与提交

提交前检查：

- 原型数为 3–5，且至少 3 种动作机制；
- 每张卡 10 项字段齐全，所有碰撞事实有本地证据；
- survivor 不超过 2；
- 无 web/search、仿真、代码和科学 claim；
- `git diff --check` 通过；diff 只有唯一产出文件；
- 单次 commit，消息概括 Ch4 concept batch，不 push。

最终只回五项：terminal verdict；原型列表；survivor 与 collision 结论；产出路径；commit SHA。
