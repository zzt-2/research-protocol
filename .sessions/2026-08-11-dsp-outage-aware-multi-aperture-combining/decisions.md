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

## D002: 当前范围由 GW Step 1 变更为 GW Step 2 acquisition

> status: active
> date: 2026-08-11
> 取代：无
> 被取代：无
> 依据：验证 V001 + 主控显式授权（source thread `019fccc3-f9f2-7b52-938f-b2b1dda09b10`）

### 决策

保持原始目标与 Step 1 结论不变，仅开放 Groundwork Step 2 的相关性筛选、既有资产复用、合法下载/转换、identity/content quality gate 与 coverage gap 报告；Step 3 及以后保持 `NOT_AUTHORIZED`。

### 理由

V001 已接受 `STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`，且主控明确确认 coverage 并授权 acquisition。2019 direct competitor 的完整动作签名必须留给 Step 3 fresh-context 精读，Step 2 只闭合全文可得性与身份/内容质量。

### 排除的替代方案

- 不在 Step 2 读取或总结完整 input-trigger-action-output，避免把 acquisition 变成未授权精读。
- 不以 abstract-only、二手引文或 read-note 冒充 fulltext。
- 不以 generic RF hard comparator 替代缺失的 optical CORE，尤其不能掩盖 2019 P0 coverage gap。
- 不实现、不仿真、不修 b3 caller、不运行 smoke。

### 影响范围

更新 topic-index、S002、registry、master-state；新增 R002、Step2 receipt、V002、H002。允许按 `gw-acquire.md` 对优先池执行最多三轮合法获取。

### 来源

主控 Step 2 acquisition 授权；触发原话：无（主控授权，非用户/导师原话）。
