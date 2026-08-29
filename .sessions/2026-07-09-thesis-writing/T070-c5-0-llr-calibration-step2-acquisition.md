# Task Brief: C5-0 reliability-aware LLR calibration 候选级 Step 2 获取

> 来源: S027–S028 / D049 / T040–T041 / T067 / V024 | 产出位置: `projects/thesis-fso/apsk-llr-calibration-groundwork/step2-coverage-report.md` 与合格全文池
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 11
  action_class: GW_STEP2_ACQUIRE_C5_LLR_CALIBRATION
  mission_checkpoint: CP011
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

为既有 C5-0 方法卡完成候选级 GW Step 2 acquisition：获取并验证足以支持“receiver-visible residual/reliability → 低维 LLR 校准 → calibrated LLR/decoded bits”的直接方法原子、正确未校准 baseline 与 target-scene 邻居全文池。只回答后续 Step 3 是否有合格输入；不构造 Q#、不实现、不仿真、不写论文正文。

## 候选边界

- 当前方法卡只是 seed：Ch4/Ch3 后的 known-pilot residual 或其他 receiver-visible reliability，驱动一个低维、因果的 LLR scaling/temperature/clip calibration；输出 calibrated LLR，再进入冻结 LDPC decoder。
- B0：同一 max-log/APP demapper 的未校准 LLR；后续强 cheap 对手至少包含一个全局 scalar scaling。不得把多个 scale/clip 系数拆成多种方法。
- C5-1 已因真实 held-out BER/GMI 无信号关闭；不得复活 covariance geometry、加入 synthetic anisotropy 或把 C5-1 Groundwork 冒充 C5-0 authority。
- 旧 P08/P08-R 的固定 NOMS/clip 小效应只作负面先验，不直接继承为 C5-0 方法成立。

## 获取问题与最小覆盖

1. 路线 A：mismatched BICM/demapper 的 LLR scaling、L-value correction、temperature calibration 或 GMI-optimal scalar correction，至少 2 篇合格全文，其中至少 1 篇给出可执行公式。
2. 路线 B：用 pilots/known symbols/decision residual 估计噪声或 reliability，并据此生成/校准 soft metrics，至少 2 篇合格全文。
3. 路线 C：APSK、coherent optical 或 FSO 中的 soft-demapping/LLR mismatch 直接邻居，至少 1 篇合格全文；若只能得到通信通用原子，必须诚实标 target-scene limitation，不自动 FAIL。
4. 总池目标 6–10 篇 qualified fulltext；至少一个正确未校准 baseline authority、一个 scalar cheap alternative、一个可执行校准原子。完整 recipe exact collision 留到 Step 3.5，不在 Step 2 先验裁决。

## 执行规则

1. 先读 T041、S027 的 C5-0 卡、T067/V024 负终态、`stages/groundwork.md` 的 Step 2、`tools-guide.md` 与 acquisition 规范；运行 task-control validator。
2. 先查本地 `papers/index.json`、`search-archive/_index` 与现有 P08/P08-R 证据；再用项目 `tools/search` 做至多 8 个聚焦 query，不用主线程 WebSearch。
3. 只用 `tools/download` 获取全文，验证 DOI/arXiv 身份、meta 来源、文本质量与关键公式页；不得自己创建任意 papers 目录或用标题摘要冒充全文。
4. 对每篇记录：方法 IAO、校准参数来源、是否需要 truth、baseline、指标、场景、与 C5-0 的 exact/primitive/related 关系、Step 3 需精读的具体问题。

## Terminal

- `STEP2_READY_FOR_STEP3`：三路线覆盖满足，总 qualified=`6..10`，且直接公式/正确 baseline/scalar cheap 三项均有全文；允许另派 Step 3 精读。
- `STEP2_READY_WITH_TARGET_LIMITATION`：通信通用校准原子与 baseline 闭合，但 APSK/optical/FSO 直接邻居只有 related evidence；仍可进入 Step 3，但 claim ceiling 预先收窄为 target-scene migration。
- `EVIDENCE_BLOCKED`：缺直接可执行 LLR calibration 原子或正确 baseline 全文；列出最小缺口，轮换 C5-5，不实现、不仿真。

## 交付

交付 `step2-coverage-report.md`、必要 acquisition/read-note/index/search-archive 增量与 usage log；不得修改 Skill/controller、仿真代码、Ch3/Ch4、正式论文正文或新建候选。报告 facts-first，含 query/池 arithmetic、qualified ledger、coverage、limitation、terminal、Step 3 read pool 和唯一下一步。运行 validator、身份/meta/全文质量审计、路径白名单与 `git diff --check`；一次 commit、不 push。
