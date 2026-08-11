# [R001] GW Step 1 检索综合

> 2026-08-11 | 关联：2026-08-11-dsp-outage-aware-multi-aperture-combining / D001

## 调研问题

在不下载、不全文精读、不实现、不仿真的边界内，判断 post-DSP multi-aperture MRC 的 DSP-outage-aware branch admission / soft weighting 是否有足够候选进入 Step 2，并识别 exact-action collision 风险与传统 comparator。

## 发现

### 1. 质量门

| 门 | 结果 | 判定 |
|---|---:|---|
| query / round | 6/6；2/2 | 达上限，未超 |
| 原始结果 / DOI-title 去重 | 169 / 157 | PASS（≥20） |
| 实际贡献源 | Semantic Scholar、OpenAlex、Tavily = 3 | PASS |
| 语义候选 | 27 | PASS |
| 正式发表 | 24/27 = 88.89% | PASS（unknown 不计正式） |
| 必读 | 8 | PASS（≥5） |
| 技术路线 | A hard；B soft | PASS（≥2） |

完整回执见 `step1-search-receipt.md`；逐条语义裁决见 `step1-candidate-collision-matrix.md`。

### 2. 问题证据与新颖性证据必须分开

- **问题证据**：Johst WiSEE 2024 明确指出低 SNR/DSP-outage 支路可能使 post-DSP combining 变差，并应 discard。这支持“无效支路会伤害组合”的 defect 形状。
- **不能推出**：上述证据不证明 soft validity weight 有效，也不证明它新颖。Johst/OFC 的 X-MRC 或固定 SNR discard 属 hard comparator。
- **reference M**：Wang 2023 提供 FS/CE/CPE→MRC 的 post-DSP 链形状；Geisler 2016 提供多孔径相位对齐/MRC 基础动作。两者都不是本专题方法。

### 3. 两条保留路线

**A. hard admission（传统 comparator）**

`estimated SNR / branch quality → SC、top-L GSC、threshold GSC、H-S/MRC 或 discard → selected-branch MRC`。最强便宜形态是 normalized-threshold GSC 或保底 N 支 + threshold；Johst 的约 −1 dB discard 必须作为光学 task-matched comparator。该路线已碰撞，不是 extension。

**B. soft robust weighting（潜在 extension，须进一步缩窄）**

`多源 receiver-visible per-branch DSP validity → 对 estimated-channel MRC 权重做有界 shrinkage；极低 validity abstain → combined symbols + no-valid-branch flag`。ICCC 2022 已有 pilot-energy attenuation→interpolated MRC weights，因此“泛化 reliability-weighted MRC”本身已被占；潜在 extension 必须落在 **post-DSP outage-model violation + FS/CE/CPE 多源 validity**，而不是把 pilot SNR 换名。

**C. temporal/hysteretic admission：当前不保留。** 本轮没有找到 hysteresis 所需的时序物理前提；快速时变、feedback delay 或 block-length response 不足以授权该动作。

### 4. 最近 direct competitor 与 collision 状态

最近 direct competitor 是 2019 Optics Communications：*Adaptive digital combining for coherent free space optical communications with spatial diversity reception*，DOI `10.1016/j.optcom.2019.03.069`。当前 Q2 的 Tavily/ADS 条目提供 direct hit；本轮前已存在的全局 S2/OpenAlex 索引条目补齐 year/venue/DOI，并明确“四孔径 adaptive digital combining”及“避免耗时、复杂的随机时变衰落估计”动机。摘要仍没有披露 input/trigger/weight 的完整实现语义。

动作签名对比：

| 字段 | 本专题 hypothesis | 2019 competitor 摘要可见 |
|---|---|---|
| input | post-FS/CE/CPE 多源 validity | 多孔径接收信号 |
| trigger | lock/outage confidence | 未披露 |
| action | shrink estimated-MRC weight；可 abstain | adaptive digital combining weights |
| output | combined symbols + no-valid flag | combined output / BER gain |
| collision | — | `UNRESOLVED`，不能据缺词判 non-exact |

2024 Optics Letters real-valued MIMO equalizer是联合 equalization/combining 的 estimator-changing strong neighbor；2020 两篇 phase-alignment work 解决复杂度/相位误差；均非摘要级 exact action。

### 5. Receiver-visible feature 证据

| feature | Step 1 证据状态 | 解释 |
|---|---|---|
| pilot-LS residual | CANDIDATE_ONLY | ICCC 2022 实用的是 pilot energy attenuation，不是 LS residual。 |
| frame-sync peak margin | CANDIDATE_ONLY | Optics Express 2022 使用 timing-sync 结果，但未明确 peak margin→admission。 |
| CPE coherence / cycle-slip metric | CANDIDATE_ONLY | phase-error/combining-loss 与 cycle slip 被讨论，但未作为 branch-weight 输入。 |
| decoder/FEC flag | ABSENT | 只见 FEC threshold/result 或其他任务 reliability test；不复活 coded C1。 |

### 6. Identity / provenance 核

- Johst 2024：`papers/doi/10.1109_wisee61249.2024.10850117/content.md`，标题/作者/会议与 DOI 同一；用户给定 defect 行为锚保持一手来源。
- Wang 2023：DOI `10.1109/JPHOT.2023.3265847`。本 worktree metadata 仍为 `all_failed` 且未物化 content；共享根 `D:/code/study/research-protocol/papers/doi/10.1109_jphot.2023.3265847/metadata.json` 为 success，real_title=`Carrier FOE Scheme Based on FSTS...` 并有 `content.md`。本轮只核身份，不修资产。
- Geisler 2016：DOI `10.1364/OE.24.012661`；当前 Q2/Q6 Tavily 命中与本轮前既有 OpenAlex/S2 全局索引在 title/DOI/action 上一致。
- closest 2019：DOI `10.1016/j.optcom.2019.03.069`；当前 Q2 Tavily/ADS 命中与本轮前既有 Semantic Scholar/OpenAlex 全局索引在 title/DOI/abstract 上一致。两条可复算原始索引摘录已固定到 `step1-provenance-receipt.md`，不以未提交的全局索引修改状态作隐含证据。
- Johst OFC 2024：DOI `10.1364/OFC.2024.W2A.31`；全局索引的 abstract 字段存在错配，故本轮只采用其 identity 与已有一手锚，不把该错误摘要作为动作证据。

## 结论

`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`

理由：所有 Step 1 质量门通过；hard comparator 与宽泛 soft-weight 先例已被诚实识别；仍存在一个明确、可由全文动作签名快速证伪的 2019 direct-collision 风险，而不是已确认 exact collision 或证据池不足。此 terminal 只说明 Step 1 检索合格，不是 Q#、Go、METHOD_SIGNAL 或方法贡献。

## 对决策的影响

D001 范围保持。下一合法动作仅是主控确认后进入 GW Step 2，获取/绑定 must-read shortlist，并优先闭合 2019 competitor、Johst OFC/WiSEE 与 ICCC 2022 的完整 input-trigger-action-output；在确认前 Step 2 仍 `NOT_AUTHORIZED`。
