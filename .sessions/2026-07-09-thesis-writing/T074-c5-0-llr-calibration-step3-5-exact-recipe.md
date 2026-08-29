# Task Brief: C5-0 LLR calibration bounded Step 3.5 exact-recipe closure

> 来源: S028 / D053 / T070 / T072 / V026 / V028 | 产出位置: `projects/thesis-fso/apsk-llr-calibration-groundwork/step3-5-exact-recipe-closure.md`
> 日期: 2026-08-30

<!-- RDL-TASK-CONTROL:START -->
```yaml
rdl_task_control:
  schema_version: rdl.task-control.v2
  control_ref: .sessions/2026-07-09-thesis-writing/topic-index.md
  control_epoch: 15
  action_class: GW_STEP3_5_EXACT_RECIPE_C5_LLR_CALIBRATION
  mission_checkpoint: CP015
```
<!-- RDL-TASK-CONTROL:END -->

## 唯一任务

对 T072 的唯一 `Q-C5-0` 做一次 45 分钟封顶的 candidate-specific GW Step 3.5：查清完整 target-scene recipe 是否已存在，并裁清 B2 per-frame global scaling 与 B3 direct auxiliary-variance plug-in 在 max-log/APP 下的等价关系。这里只决定方法身份、claim ceiling 与能否进入纸面 Step 4a；不实现、不仿真、不证明 BER 改善。

`Q-C5-0` 冻结链：

`post-Ch4 demux → per-tributary Ch3 CPR → current-frame known pilots → demeaned residual variance/reliability → one positive per-frame global scalar → channel/extrinsic LLR only → frozen LDPC decoder`。

## 必读与工作方式

1. 必读 T072 brief、`projects/thesis-fso/literature_notes_apsk_llr_calibration.md`、六份 read notes、T070 Step 2 report、D053/V028、`stages/gw-supplement.md`、`stages/glossary.md`、`domain-comms.md`、`thesis-lessons.md` TL-31–33。
2. 先查本地 `search-archive/_index/all-papers.jsonl`、现有论文库与六篇双向引用线索；只在 exact-action 仍有缺口时用项目 `tools/search`。主任务不得直接 WebSearch；需要网页或全文消化时派最多 3 个只读 subagent，单个不超过 15 分钟。
3. 最多两轮、三类 query family：
   - pilot/known-symbol residual 或 noise-variance estimation + online LLR scaling/calibration + BICM/LDPC；
   - APSK/coherent optical/FSO + pilot-aided demapper reliability/noise mismatch + max-log/APP；
   - direct variance plug-in、post-FEC/decoder-facing LLR normalization 与 per-frame SNR scaling。
4. Round 2 只补 Round 1 的 MUST/SHOULD 缺口；Round 2 新 MUST/SHOULD=`0/0` 或墙钟 45 分钟即停。不得把一般 LLR/GMI 综述扩成新 Step 2。

## 必答科学问题

1. 用九字段逐篇比对：observation position、receiver-visible input、statistic、window/cadence、action target、freedom、decoder interaction、output、target scene。只有九字段均相同且目标平台相同，才叫 target-scene exact collision。
2. 明确验证而非口头推断：若 B0 max-log metric 用假设方差 `tilde_sigma2`，把同一 pilot residual estimate `hat_sigma2` 直接 plug-in 是否严格等价于 `s=tilde_sigma2/hat_sigma2` 的全局正缩放；exact APP 的 log-sum-exp 是否仍严格等价，在哪些近似/先验条件下不等价。
3. 说明正全局缩放对 uncoded hard sign、maximum-metric codeword ordering、finite-iteration LDPC/BP、GMI/ASI 的不同影响。不得把“hard sign 不变”误写成“coded BER 必不变”，也不得预先保证 BER 会改善。
4. B1 offline fixed scalar、B2 per-frame scalar、B3 direct plug-in、O1 matched reference 与 Layton per-point neighbor 的信息预算和自由度是否公平。
5. operational minimum pilots/window 当前是否仍 UNKNOWN；若无 authority，保留为 Step 4a falsifier，不拍数字。

## 交付

在指定报告中形成：

- 搜索轮次与去重记录数、query/citation-chain receipt；
- exact-recipe 九字段矩阵与逐条 source pointers；
- max-log/APP B2↔B3 代数裁决；
- comparator/信息预算表；
- claim ceiling、必须披露、不得主张；
- 唯一 terminal 与后续入口。

必要的新全文/元数据按仓库既有工具和 canonical 路径保存；只下载承重 MUST/SHOULD，不为数量扩池。不得修改正式论文、仿真、Skill/controller 或 Ch4 包。

## 冻结 terminal

1. `STEP3_5_SURVIVES_AS_TARGET_SCENE_CLASSICAL_MIGRATION`：没有相同目标平台九字段完整碰撞；允许主控另开 Step 4a。
2. `STEP3_5_EXACT_NEIGHBOR_LIMITS_CLAIM`：邻近场景已有相同动作或 B2/B3 等价，但目标平台/observation contract 不同；仍允许硕士级场景迁移进入 Step 4a，永久关闭首次/新理论主张。
3. `STEP3_5_EVIDENCE_LIMITED_MIGRATION`：两轮后承重 primary evidence 仍有限；在“不声称首次、只作目标场景迁移”前提下允许进入 Step 4a，不把检索不完备写成 novelty 证明。
4. `STEP3_5_TARGET_SCENE_EXACT_COLLISION`：同一 DP-(8,8)-16APSK coherent-FSO observation/action/output recipe 已完整存在；关闭 C5-0，回主控按既定顺序轮换 C5-5。

前三个 terminal 都不是方法成立，只是 Step 4a 入口。任何 terminal 都禁止在本任务实现或仿真。

## 验收与时限

- 独立 reviewer 只核 source→九字段→等价关系→terminal，P0/P1 必须为 0；P2 可局部修。
- task-control、query receipt、source identity、唯一 terminal、`git diff --check` 必须 PASS。
- 墙钟 45 分钟；30 分钟时停止扩搜并开始综合。一次 commit、不 push；回报 commit、轮次/记录数、最强 exact neighbor、B2/B3 等价结论、terminal、claim ceiling 与 blocker。
