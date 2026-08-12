# Task Brief: 历史方法资产硕士级重裁

> 来源: S019 | 产出位置: `projects/thesis-fso/direction-lab/harvest/`
> 日期: 2026-08-12
> 唯一文档: 执行方可读取本任务列出的仓库文件及其证据指针，不得扩展为新检索或科学实验

## 0. TL;DR

你在 `D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`。

**任务**：把 thesis-fso 过去积累的全部方法候选、组件和失败路线按“硕士级 reference-method extension”标准重新裁决，找出可直接包装或只差一次小补证的候选。

**产出**：

1. `projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.md`
2. `projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.yaml`
3. 更新本专题 S019、D/V、topic-index 与 registry；由 fresh-context verifier 独立终验。

**最高纪律**：只读历史证据；不检索、不下载论文、不实现、不仿真、不改 Skill/controller/common/params/正式论文。不得因存在更强方法或相邻动作就自动 Kill，也不得复活科学无效证据。

## 1. 背景

过去流程把“硕士方法是否可写”过多等同于“是否具有期刊级独立机制、是否避开所有强近邻、是否接近全局最优”，造成大量可信但增量有限的资产被提前降级。用户已确认新的务实标准：

- 方法可以是已有 reference 在本场景中的迁移、适配或工程化；
- 只需相对选定经典 baseline 在冻结条件下形成可信增量，不要求击败所有近期强方法；
- 其他场景、full-general 或性能更强的方法通常限制 claim ceiling，不自动否决；
- 正文不必展示所有内部廉价替代，但内部必须确认明显的一步调参不能完全解释增益；
- 不得声称 SOTA、全面领先或全新算法，除非证据确实支持。

权威记录：

1. `.sessions/2026-07-20-research-direction-lab-system/R007-thesis-grade-reference-extension-recalibration.md`
2. `.sessions/2026-07-09-thesis-writing/S019-historical-assets-thesis-grade-remap.md`
3. `.sessions/2026-07-09-thesis-writing/decisions.md#D027`

## 2. 必读与读取顺序

先读 summary owner，不要一开始遍历全部 worker-log：

1. `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
2. `projects/thesis-fso/direction-lab/harvest/method-production-campaign-thesis-map.md`
3. `projects/thesis-fso/direction-lab/harvest/campaign-level-thesis-contribution-synthesis.md`
4. `projects/thesis-fso/direction-lab/harvest/thesis-method-spines.md`
5. `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md` §2–§4
6. `projects/thesis-fso/direction-lab/harvest/peer-thesis-method-packaging-audit.md`
7. RDL system `decisions.md` D036–D041 与本专题 D026–D027

随后仅沿 owner 内的路径核验承重事实。每个候选最多深追 3 个原始证据文件；只有分类无法确定时才增加读取，并在报告中解释。

必须覆盖：CCISP、P01–P11/P07-R/P08-R2、G1、P09、AMC Q-A/Q-A′/Q-B、P1 shared-M0、C3 segmented CPE、过采样同步 Q1、RML-FSTS、coded decoder-feedback C1、DSP-outage combining Q001、multi-hypothesis phase unwrapping K2、CCISP select-before-execute、fixed-point/prefix-LS/coded-chain 工程资产，以及 inventory 中其他有名字的候选。

## 3. 裁决标准

每项必须落入且只能落入一档：

### A. READY_FOR_THESIS_PACKAGING

- 有可命名方法、完整 receiver-visible input→action→output、参考/经典 baseline；
- 已有可信性能或工程增量；
- 不需要新科学实验即可写方法流程、主结果和边界；
- 存在更强方法只导致“非 SOTA/局部条件”表述，不自动降级。

### B. NEEDS_ONE_BOUNDED_CONFIRMATION

- 方法动作与 reference-extension 形态完整；
- 历史科学证据有效，或已有局部正向信号；
- 只缺一个可以在单对话内裁决的结果、消融或公平比较；
- 必须写明唯一实验问题、现成 testbed、baseline、PASS/FAIL 和失败后的诚实降级用途。

### C. SUPPORTING_ONLY

- 只有正确性、工具、定点、局部边界或独立组件价值；
- 没有独立成章的 action/result chain，但可以并入 Ch3/Ch4/Ch5。

### D. PERMANENTLY_INVALID

只允许以下原因：truth leakage、privileged oracle 被当方法、scale/metric/cost artifact、不可复现或 chronology 失效且无合法证据、物理自由度不存在、目标问题已被当前强 baseline 证明不存在、明确 headroom/科学 gate FAIL。必须保留原始 D/V/worker-log 指针，不得用“已有更强方法”作为该档理由。

## 4. 对更强方法与 comparator 的处理

- 其他方法性能更好，不等于候选失效；记录为 `claim_ceiling`。
- 不要求每个候选打败 full-general、superset 或 SOTA；Go 对手是选定 reference 或广泛使用的经典 baseline。
- exact collision 只有在同任务、同条件、同信息、同动作输出且无场景特定 delta 时才关闭方法身份。
- 显而易见廉价方案必须内部处置；若完全吸收承重增益，不能升 A/B。若没有吸收或与 claim 无关，不要求进入论文主表。
- 不评价“作者是否敢写”，只判断本项目能否诚实限定 claim 后形成硕士方法章。

## 5. 输出格式

### 5.1 Markdown 主报告

按以下顺序：

1. 一页人话结论：现有资产能否凑出 Ch3/Ch4/Ch5 方法链；
2. 全量资产表：名称、原 terminal、关键证据、旧关闭原因、新四档、claim ceiling；
3. A/B 档详细卡：方法名、reference、目标场景、适配 delta、baseline、现有数字、主图、消融、最小缺口；
4. 永久无效清单及原因；
5. 最多 3 个优先候选排序；
6. **唯一推荐下一包**，或诚实报告无候选；
7. 对 Skill 最小修订建议，只列需要改变的 1–3 条行为，不实施。

### 5.2 YAML

每项字段至少包括：

```yaml
- id: stable_id
  name: method_name
  original_terminal: string
  new_tier: READY_FOR_THESIS_PACKAGING | NEEDS_ONE_BOUNDED_CONFIRMATION | SUPPORTING_ONLY | PERMANENTLY_INVALID
  chapter_fit: Ch3 | Ch4 | Ch5 | none
  evidence:
    - path
  reference_method: string
  adaptation_delta: string
  baseline: string
  stronger_neighbor_effect: CLAIM_CEILING_ONLY | DIRECT_COLLISION | NOT_APPLICABLE
  missing_gate: string | none
  recommended_action: string
```

## 6. Terminal

唯一 terminal 三选一：

- `THESIS_GRADE_CANDIDATE_AVAILABLE`：A 或 B 非空，且给出唯一优先项；
- `NO_REUSABLE_CANDIDATE`：A/B 均为空，但全量覆盖和永久无效证据闭合；
- `EVIDENCE_MAP_INCOMPLETE`：owner/原始证据矛盾，无法完成关键候选裁决。

本任务不产生 METHOD_SIGNAL、不恢复 active carrier、不授权实验、不直接改论文正文。

## 7. 已知陷阱

1. 不把“存在更强论文”当永久无效；这是本任务最重要的 RED。
2. 不把 G1/P09 等 artifact 因标准放宽而复活。
3. 不把 fixed-point identity、prefix-LS correctness 或 verifier 工具单独改名成算法方法。
4. 不只看最近 K1/K2；必须覆盖历史 inventory 全量。
5. 不重新做全文检索或 novelty closure；缺失文献只降低 claim ceiling。
6. 不让治理文件数量超过科学/包装产出；主产出只有一份 MD、一份 YAML。

## 8. 验收

- [ ] inventory 与 campaign/thesis map 中所有命名资产均有唯一记录；
- [ ] `PERMANENTLY_INVALID` 每项都有允许的科学无效原因与证据路径；
- [ ] 没有候选仅因“别人更强/动作不够原创”被永久关闭；
- [ ] A/B 每项均有 reference、adaptation delta、baseline、结果或唯一补证缺口；
- [ ] 唯一推荐项能落入 Ch4，或解释为什么只适合 Ch5；
- [ ] fresh-context verifier 逐项抽查至少 12 个资产，其中 A/B 全查、D 至少查 5 个；
- [ ] 不存在检索、下载、实现、仿真、Skill/common/params/论文正文改动；
- [ ] 只提交本任务 allowlist 文件，一次统一 commit，不 push；无关 dirty 不暂存。

## 9. 最终回执

只回五项：

1. 四档计数与 terminal；
2. A/B 候选及关键理由；
3. 唯一推荐 Ch4/下一包；
4. 永久无效项边界；
5. 文件路径、verifier、commit SHA。
