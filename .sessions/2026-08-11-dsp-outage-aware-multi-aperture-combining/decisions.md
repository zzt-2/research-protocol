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

> status: superseded
> date: 2026-08-11
> 取代：无
> 被取代：D003
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

## D003: 以 JLT 2023 修复 Step 2 coverage，并在 2019 全文限制下授权 Step 3

> status: active
> date: 2026-08-11
> 取代：D002
> 被取代：无
> 依据：主控 scope decision + 调研 R002/R003 + 共享全文 `D:/code/study/research-protocol/papers/doi/10.1109_jlt.2023.3276637/content.md` + 用户原话 `voice.md` 2026-08-11

### 决策

保留 2019 Optics Communications 全文不可得的事实，但撤销“P0 缺失即绝对阻断”的处置；将可读的 Liu et al. JLT 2023 绑定为 strongest estimator-changing optical CORE，使 Step 2 qualified fulltext 从 4 增至 5，terminal 改为 `STEP2_ACCEPTED_WITH_2019_FULLTEXT_LIMITATION`，并立即授权本专题执行 GW Step 3 全文精读。

### 理由

2019 摘要足以维持“宽泛 adaptive combining 已被占”的边界，却不足以裁剪精确 post-DSP validity action。JLT 2023 是更晚、可读且动作更强的直接邻接竞品：其 2N×2 blind adaptive MIMO equalizer 用 CMA/RDE 联合处理 gain/phase/SOP/skew，可以先裁 raw-signal estimator-changing route 对问题的吸收程度。只有 Step 3 后窄 Q# 仍存活，2019 全文才回到 Step 3.5 critical debt。

### 排除的替代方案

- 不重做下载或新增搜索；2019 availability 事实与 claim limitation 原样保留。
- 不以 abstract-only 2019 条目充作第 5 篇全文。
- 不把 JLT 2023 的 metadata `all_failed` 当成 source/content 不存在；以实际 PDF/Markdown、SHA、标题/DOI 正文闭合为准，并显式记录 metadata 冲突。
- 不在 Step 3 设计具体算法、运行 smoke、进入 Step 3.5/4a 或改 b3 代码。

### 影响范围

更新 Step 2 coverage/receipt、topic-index、master-state、registry；创建 S003 与专题 literature_notes owner，派 T007–T009 完成五篇精读，最终形成 R004/D004/V003/H003。

### 来源

S003；主控 scope decision。触发原话见 `voice.md`。

## D004: Q001 通过 Step 3 问题门，进入 Step 3.5 确认等待

> status: active
> date: 2026-08-11
> 取代：无
> 被取代：无
> 依据：R004 + 五篇全文 read notes + T007–T009 worker logs

### 决策

将 canonical Q001 判为通过 Groundwork Step 3 四判据，terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`。Q001 严格限定到 Wang 2023 有全文证据的 branch-local boundary：per-branch FS/alignment 与 branch phase correction 后、MRC 前，用 receiver-visible branch-local validity 产生 bounded reliability/abstention，并输出 combined sequence 与 no-valid-branch flag。

### 理由

Wang 2023 在 per-branch FS/alignment 与 branch phase correction 后执行 MRC、再做 shared pol-demux/FOE，该真实位置没有 validity action；Johst 2024 给出 invalid branch 会恶化 combining 且应 hard discard 的 defect shape。Liu 2023 是更强的 estimator-changing alternative，但没有 explicit admission/abstention；Tu 2020 占据 known-OSNR phase-window/positive-gain admission；Yang 2022 占据 generic pilot-attenuation soft weight。完整“所有独立 FS/CE/CPE 后”位置因缺近期 task-matched baseline 保持 Step 3.5 debt，不并入 Q001 PASS。

### 排除的替代方案

- 不把 fixed SNR discard、SC/GSC、pilot attenuation weight、OSNR-positive-gain admission 或 2N×2 CMA/RDE 包装成新方法。
- 不因 2019 摘要未出现窄关键词就宣称 non-collision；exact action 仍为 `UNRESOLVED`。
- 不把 Step 3 问题存活写成方法有效、新颖性闭合、Go/Kill 或 METHOD_SIGNAL。
- 不在本轮进入 Step 3.5/4a、设计算法或运行 smoke。

### 影响范围

Step 3.5 的唯一合法任务是补 2019 exact-action debt 并做窄 post-DSP/lock-aware/multi-source validity collision search。若 2019 或新 direct competitor 覆盖相同 input-trigger-action-output，则 Q001 在 Step 3.5 终止。

### 来源

S003 / R004。触发原话：无（全文证据综合裁决）。
