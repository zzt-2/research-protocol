# Ch4 Q-C4-2 GW Step 3.5 exact-recipe closure

> T050｜2026-08-30｜只完成 Q-C4-2 Step 3.5；未进入 Step 4a、实现、实验或论文正文。
> 控制校验：`C:\Users\zzt\.agents\skills\research-direction-lab\scripts\validate_task_control.py` = `PASS`（epoch 5 / CP005 / `TARGETED_SUPPLEMENT_SEARCH`）。

## 1. 固定目标与 collision 门

目标完整 receiver-visible IAO recipe 固定为：

`有限 pilot 的 2×2 LS 初始化 + 已知 (8,8)-16APSK ring identity + payload residual/decision distance`
`→ 对均衡更新逐样本 reliability gate/weight`
`→ semi-blind refined 2×2 demultiplexer`。

只有 receiver-visible input、pilot-init、APSK ring-aware error、逐样本 reliability gate/weight 和 2×2 equalizer output 五项全部相同才记 `EXACT_RECIPE_COLLISION`。不同调制/场景、generic confidence-weighted LMS、soft-decision equalization、RDE 或 pilot initialization 只记邻居，不自动关闭硕士级 target-scene extension。

## 2. 轮次、计数与收敛

| 轮次 | 动作 | raw / unique | 2019+ raw / unique | 新增 MUST | 新增 SHOULD | 终态 |
|---|---|---:|---:|---:|---:|---|
| Round 1 | 预注册 6/6 task query matrix | 29 / 27 | 29 / 27 | 0 | 1 | Di Rosa–Richter 2021 进入 action closure |
| Round 2 | 2021 邻居双向 citation + RDE/Fatadin/Baldi/Roudas 有限 citation/alias closure | 286 / 269 | 118 / 108 | 0 | 3 | 召回 FEC-SoftRDE、MAPSK outer-ring CMA、pilot+EM RSOP 邻居 |
| Round 3 | 三个最强新增邻居的 backward/alias closure | 13 / 13 | 5 / 5 | 0 | 0 | saturation；停止 |

三轮合计 328 archive rows，按 DOI、否则按规范化题名去重为 305 条；其中 2019+ 为 152 rows / 140 unique records。15 个纳入计数的显式 archive 与 SHA-256 见 `search-archive/2026-08-30/t050-ch4-ring-aware-gated-step3-5-receipt.json`。

## 3. exact-action ledger

| 对象与证据层 | receiver-visible input / init | ring-aware error | reliability action | equalizer output | verdict |
|---|---|---|---|---|---|
| Di Rosa & Richter, JLT 2021, DOI `10.1109/JLT.2021.3098220`；摘要 | time-multiplexed pilots + payload；摘要称 pilot-aided adaptive-filter update，但未确认“pilot-only 2×2 LS initialization” | PS-QAM amplitude-level/radius assignment likelihood，不是 `(8,8)-16APSK` ring identity | payload 依正确 blind assignment likelihood 做选择性更新 | 摘要确认用于 fast SOP tracking；2×2 butterfly 细节未获全文核验 | `STRONG_RECIPE_NEIGHBOR`；最强邻居，调制与 init 语义不匹配，非 exact collision |
| 同血缘 ECOC 2020, DOI `10.1109/ECOC48923.2020.9333378`；摘要 | blind payload，无 pilot init | high-order / shaped QAM amplitude levels | assignment-likelihood conditional filter update | blind RDE equalizer | `STRONG_NEIGHBOR / ALIAS_LINEAGE`；JLT 2021 的会议前身，不新增独立 collision |
| FEC-assisted RLS-SoftRDE, ACP 2025, DOI `10.1109/ACP66871.2025.11349870`；摘要 | FEC decoder posterior；未见 pilot-LS init | DP-64QAM probabilistic soft-ring radius | decoder soft information weights error reference | polarization demultiplexing | `STRONG_RECIPE_NEIGHBOR`；soft-ring primitive 已碰撞，但信息源、调制和 init 均不同 |
| MAPSK outer-ring CMA, 2025, DOI `10.1117/12.3067096`；摘要 | blind MAPSK samples；无 pilot | APSK outer-ring constellation points | 选择 outer-ring，不是 residual/confidence reliability gate | 摘要未确认 2×2 polarization demux | `STRONG_PRIMITIVE_COLLISION`；APSK ring selection 已知，不是完整 recipe |
| Time-domain ML/EM RSOP+phase, 2025, DOI `10.1109/TCOMM.2024.3522036`；摘要 | pilot symbols + unknown payload as EM latent variables | 无 APSK ring-aware error | EM/DA iterative refinement，不是逐样本 decision-distance gate | dynamic RSOP/phase tracking and detection | `STRONG_NEIGHBOR`；pilot+payload+polarization 原子接近，更新机制不同 |
| Generalized enhanced decision-adjusted modulus, 2020, DOI `10.1109/MTTW51045.2020.9244924`；摘要 | blind QAM samples；无 pilot | closely positioned circles + optimized detection thresholds | decision threshold 防 misadjustment，非目标 residual gate | blind equalizer | `PRIMITIVE_COLLISION`；circle-aware threshold 已知 |
| Nonlinear concurrent butterfly equalizer, 2021, DOI `10.13164/RE.2021.0261`；摘要 | blind DP-QAM samples；无 pilot | CMA/MCMA + soft direct decision | concurrent CMA-SDD | butterfly polarization equalizer | `STRONG_NEIGHBOR`；2×2 + soft decision 原子已知，但无 APSK ring/pilot init |
| Hybrid FEC/channel equalization, 2025, DOI `10.1364/OE.564077`；Round 3 摘要 | LDPC SISO posterior + received samples；未见 pilot init | 无 APSK ring error | decoder soft information assists LMMSE equalizer | PDM-16QAM channel equalization | `NEIGHBOR_ONLY`；Round 3 新记录但不达 MUST/SHOULD 全文门 |

## 4. fulltext / abstract 边界

- **新全文 0 篇 / 新 read note 0 篇**。唯一可能显著改变 action-level claim ceiling 的 Di Rosa–Richter 2021 在项目 `read-log.md` 中有历史登记，但当前 worktree 没有登记所指的 `content.md` 或 read note，不能冒充已读。
- 对 DOI `10.1109/JLT.2021.3098220` 的一次合规下载返回 `all_failed`；工具对 `papers/index.json` 的副作用已精确回退，失败目录已删除，未进入提交。
- 其余新增对象的摘要已足以确认至少一项硬不匹配（无 pilot-init、非 APSK、无 ring-aware error、非逐样本 gate 或非 2×2 equalizer output），故不扩大全文 acquisition。
- 摘要级证据只支持“本 bounded slice 未确认 exact collision”，不支持“首次”“SOTA”或领域穷尽性声称。S2 曾限速；OpenAlex citation 输出曾因 `title=null` 触发 CLI 打印异常，最终纳入 receipt 的 archives 均已成功落盘并哈希。

## 5. 裁决

**`Q-C4-2 SURVIVES`**。

在本次 6-query、四经典锚 citation/alias closure 与三轮 saturation 切片内，没有确认同时满足以下五项的已发表 recipe：

1. 有限 pilot 的 2×2 LS 初始化；
2. `(8,8)-16APSK` 已知 ring identity；
3. payload receiver residual / decision distance；
4. 对均衡更新逐样本 reliability gate/weight；
5. 输出 refined 2×2 demultiplexer。

但 claim ceiling 已明显收窄：Di Rosa–Richter 2021 已占用“pilot + payload assignment likelihood + selection-RDE + SOP tracking”主干，FEC-SoftRDE 2025 又占用“soft ring + reliability-weighted polarization demux”主干。因此后续若进入 Step 4a，只能声称 **把 receiver-distance reliability-gated RDE 明确适配到有限-pilot `(8,8)-16APSK` 2×2 LS-initialized receiver 的 target-scene extension**；不得声称首创 pilot-aided RDE、likelihood-gated equalizer、soft-ring update 或 semi-blind polarization tracking。

本 verdict 只闭合 Step 3.5，不是 Go、方法信号或可行性证明，也不授权实现、smoke 或实验。

## 6. 唯一 blocker

`FULLTEXT_UNAVAILABLE_DI_ROSA_2021`：最强邻居全文在当前 worktree 不可用且合规下载失败，故其 pilot initialization、逐样本权重公式与明确 2×2 butterfly 实现仍只能标为摘要级/未核。该 blocker 限制 action-level 独立性主张，但由于其调制明确为 PS-QAM、不是目标 `(8,8)-16APSK`，不改变本次 bounded `SURVIVES` verdict。
