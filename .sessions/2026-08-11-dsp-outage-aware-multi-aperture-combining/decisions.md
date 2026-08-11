# 决策记录

## D001：新专题仅执行 Groundwork Step 1

- 日期：2026-08-11
- 状态：accepted
- 强度：INVARIANT
- 来源：主控验收 K1 后的显式授权；用户原话见 `voice.md`
- 决策：创建 `2026-08-11-dsp-outage-aware-multi-aperture-combining`，仅执行 GW Step 1。固定 SNR 阈值 discard/SC/GSC 是传统 comparator；potential extension 只保留多源 receiver-visible DSP validity 的 soft weighting/abstention，或有明确时序前提的 hysteretic admission。
- 为什么：Johst 2024 已直接报告低于约 −1 dB 的 DSP-outage 支路会恶化合并，说明 defect 形状值得核查；但这不证明软方法有效或新颖，必须先做 exact-action collision 搜索。
- 为什么不进入 Step 2/实现/仿真：当前只有 hypothesis，没有 Step 1 检索终态，也没有后续授权；提前行动会违反 FR-22。
- 否决条件：六组 query 后如 direct-action collision 已闭合，则 terminal=`STEP1_EXACT_ACTION_COLLISION`；如质量门或 direct competitor 身份无法闭合，则 terminal=`STEP1_EVIDENCE_INSUFFICIENT`。
- 取代：无。
- 被取代：无。

### D001 执行结论

- Step 1 terminal（V001 独立终验 PASS）：`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。
- 关键边界：2019 direct competitor 的 exact collision 为 `UNRESOLVED`，因此 terminal 不是“新颖性已通过”；下一步只能在主控确认后用 Step 2 全文动作签名闭合。
- method / thesis delta：`NONE / NONE`。
