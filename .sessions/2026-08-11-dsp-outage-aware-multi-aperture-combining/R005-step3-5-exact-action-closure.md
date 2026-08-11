# [R005] Step 3.5 exact-action collision closure

> 2026-08-11 | 关联：2026-08-11-dsp-outage-aware-multi-aperture-combining / D005

## 调研问题

在冻结的 Wang branch-local FS/alignment+phase-correction→MRC 边界，现有一手方法是否已经实现 `receiver-visible branch-local validity → bounded reliability/admission/abstention → combined sequence + no-valid flag`；若未确认碰撞，现有证据是否足以允许 Q001 进入 Step 4a。

## 发现

### 检索与引用链收敛

- Round 1 query matrix：8/8 queries，S2+OpenAlex raw=`115`、跨 query unique=`45`；S2/OpenAlex 分别实际贡献 17/28 个 unique retained。语义初筛 MUST/SHOULD=`0/0`。
- 前向/后向引用链：Wang、Liu、Johst、Sun 共 7 份 receipt，raw=`134`、unique=`121`、有摘要=`106`；新增 MUST/SHOULD=`5/5`。
- Round 2 定向补查：6/6 queries，raw=`6`、unique=`4`；其中 Qiu 2025 是已知 MUST，其他 3 篇 REJECT。最后一轮 new MUST/SHOULD=`0/0`，故检索身份层达到 `ROUND2_SEARCH_CONVERGED`。
- Step 3.5 整体实际贡献源为 S2+OpenAlex；Round 2 单轮 OpenAlex 因限流为 0 贡献，不虚报为贡献源。
- 可复现性限制：Round 1/2 的 provider-raw=`115/6` 来自执行时 stdout 并汇入 worker receipt 表，未单独保存 provider 原始返回；持久 JSON 可独立复算的是 retained=`46/4`、cross-query unique=`45/4`、citation raw/unique=`134/121` 与最后一轮 new MUST/SHOULD=`0/0`。

### 统一 exact-action signature

| 方法/身份 | input 与位置 | trigger / action | output / no-valid / state | 对 Q001 裁决 |
|---|---|---|---|---|
| Wang JPHOT 2023 | branch FSTS samples；FS/alignment+phase correction 后、MRC 前 | FSTS 阈值完成同步/校相；estimated-channel MRC，无 validity admission | combined symbols；无 no-valid；FS/MRC 本身非 validity policy | `REFERENCE_BASELINE`；Q001 的实际 M |
| Johst WiSEE 2024 | known-sequence DSP + branch SNR/BER/outage | 低于约 −1 dB 的 DSP-outage 支路应 hard discard | valid stream/outage marker；无 soft policy | `CHEAP_ABSORPTION`：fixed discard comparator |
| SC/GSC/fixed SNR discard | branch SNR/rank/threshold | select/drop qualified branches | selected/combined stream；全无可用支路的输出未统一 | `CHEAP_ABSORPTION` comparator |
| Tu JPHOT 2020 | aligned fields + known OSNR/loss | choose M、phase rotate、positive-net-gain recursive admission | coherent sum；无 DSP-validity/no-valid | `CHEAP_ABSORPTION` / known-OSNR neighbor |
| Yang ICCC 2022 | RF pilots/attenuation + channel estimate | attenuation-derived continuous MRC weight | weighted decisions；无 FS/phase validity、abstention/no-valid | `NEIGHBOR`；generic reliability-weighted MRC 已占 |
| Liu JLT 2023 | post-IQ/clock 2N streams | stateful CMA/RDE 2N×2 FIR joint equalize/combine | two PM streams；无 branch validity/no-valid | `NEIGHBOR`；estimator-changing strongest alternative |
| Zhang JPHOT 2023 | 4 branches after frequency recovery/timing sync | MSE-triggered FSE-MCMA/DD taps + MEKF/AKF innovation updates | one recovered stream；stateful；无 admission/abstention/no-valid | `NEIGHBOR`；全文确认非 exact collision |
| Sun OptCom 2019 | primary fulltext unavailable；后续一手只支持 input modulus-normalized adaptive cost | adaptive calculation；branch ordering/trigger/zero/drop/bounds 均 unknown | complete output/state/no-valid unknown | `UNRESOLVED`；宽泛 adaptive combining 已占，但不能裁窄 exact action |
| Xie OptCom 2023 | title-only direct multi-aperture digital combining；无摘要/全文 | unknown | unknown | `UNRESOLVED_BEARING`；最直接的新增承重债务 |
| Chen O&LT 2025 | title-only frequency-domain 4N×2 adaptive equalizer | exact trigger/taps/branch action unknown | unknown | `UNRESOLVED_NEAR_DIRECT`；标题指向 estimator-changing，不能替代全文裁决 |
| Qiu OptCom 2025 | title-only dynamic channel tracking in distributed-aperture MIMO combining | exact tracking/admission action unknown | unknown | `UNRESOLVED_BEARING`；Round 2 再命中但仍无摘要 |
| Li OptCom 2026 | title-only noncircular-CMA 4N×2 adaptive combining | exact trigger/taps/branch action unknown | unknown | `UNRESOLVED_NEAR_DIRECT` |

### 获取与全文边界

- Sun 2019 primary fulltext 在 worktree/共享根均不存在；本轮合法 backend 实下 `all_failed`。Zhang 2023 后续一手只闭合 `{input signals → modulus normalization inside adaptive cost → adaptive calculation}`，不得外推 branch-local validity action。
- Xie/Chen/Qiu/Li 四篇 MUST 均完成资产核查、dry-run 与第一轮合法 DOI/OA/Unpaywall 获取，结果 `0/4 qualified`；Xie 精确题名 arXiv 补查超时且无 receipt。五篇 SHOULD 仅完成资产核与 dry-run，按 15 分钟 MUST-first 止损。
- 新可读的 Zhang 2023 通过 title gate（Jaccard=`0.667`）并完成定向全文精读；其联合 FSE/MEKF/AKF 是 estimator-changing neighbor，不是 exact collision。

### Q001 终态

检索身份层已经收敛，且所有可读一手竞品均未确认完整 Q001 input-trigger-action-output；因此不能判 `EXACT_ACTION_COLLISION`。但是 Xie 2023 与 Qiu 2025 是 task-matched direct identities，其承重动作字段仍为 primary-fulltext unavailable；Sun 2019 的宽泛 adaptive action也只能由后续一手缩窄到 modulus-normalized cost fragment。标题/摘要不足以证明 non-collision。

终态：`EVIDENCE_BLOCKED`。

该终态表示 exact-action 证据不足，不表示方法不存在、方法成立或方向科学失败。Q001 当前没有合法 Step 4a 入口；完整 post-all-FS/CE/CPE 版本继续 excluded/unresolved。

## 结论

两轮检索已按“最后一轮 new MUST/SHOULD=0”收敛，但新增直接竞品无法取得承重全文，故无法同时满足 `SURVIVES_STEP3_5` 的“窄动作无 confirmed collision + recent task-matched baseline/evidence 充分”。Step 3.5 以 `EVIDENCE_BLOCKED` 截断，不进入 Step 4a。

## 对决策的影响

建立 D006。恢复条件仅为取得 Sun/Xie/Qiu 等承重一手全文，或出现可等价闭合其完整 input-trigger-action-output 的后续一手来源；不得以新一轮宽泛检索或标题推断重开。
