# [R002] Ch4 reference-source expansion 与 defect-reproduction 入口裁决

> 2026-08-08 | 关联：2026-08-08-ch4-reference-method-extension / D003 / T002

## 1. 恢复验证与防偏三问

### 恢复验证

- **PASS — 权威状态**：`topic-index.md` 当前 terminal 为 `LOCAL_ENTRY_POOL_EXHAUSTED_DEFECT_REPRODUCTION_GATE_REQUIRED`；D002 已被 D003 取代的仅是“战略耗尽 / 两对象失败”强度，R001 的 Paillier/K01 exact collision 与 LBS-RDE FSO defect `UNKNOWN` 事实继续有效。
- **PASS — 专题血缘**：本专题为 `active`，`conflicts_with: []`；依赖的旧 RDL system 为 dormant 历史/dead-end owner，thesis-writing 提供 Ch4 槽位约束。
- **PASS — method-production 规则**：`REFERENCE_CANDIDATE` 与 entry audit 不计 object/package failure；只有后续 evidence-valid、已授权 defect smoke 或 method package 执行后才计数。

### 防偏三问

1. **当前工作是否直接选择一个可进入 defect reproduction 的方法对象？** 是。它只裁决一个进入后续 Groundwork Step 1 的 research object，不裁决 defect、方法或 METHOD_SIGNAL 成立。
2. **本轮是否把检索/治理扩张到最小入口选择以外？** 否。先复用本地索引/全文笔记，再用满 4/4 组机制定向 query；只保留 2 个机制不同对象，没有新增第 3–5 个候选、没有下载全文或扩张到完整 novelty survey。
3. **当前 object/package 失败计数是多少，为什么 T001 不计数？** `object failure=0 / method-bearing package failure=0`。T001/T002 都是 entry screening；Paillier 是历史 exact collision，LBS-RDE 是 transfer `UNKNOWN`，均未执行本专题已授权的 defect smoke 或 method package。

## 2. 检索 receipt

执行顺序为本地 `search-archive/_index/all-papers.jsonl`、`papers/`、既有 literature/read notes、baseline inventory 与 local code/results 优先；明确缺口后才运行 `tools/search`。未使用 WebSearch/WebReader，未下载新全文。`actual` 中的 HTTP 402/0 命中按原样记录。

| # | 定向问题 / 原始 query | requested source | actual source | raw / dedup / kept | 缓存路径 |
|---|---|---|---|---|---|
| Q1 | `FSTS fixed BL BN low received power carrier frequency offset estimation dual polarization coherent FSO` | S2 / OpenAlex / Exa | S2=0，OpenAlex=0，Exa=0 | `0 / 0 / 0` | `search-archive/2026-08-08/ch4-fsts-fixed-lag-defect.json` |
| Q2 | `constant carrier frequency offset estimator Doppler drift rate coherent optical satellite Kalman` | S2 / OpenAlex / Exa | OpenAlex=10，S2=0，Exa=HTTP 402 | `10 / 9 / 7` | `search-archive/2026-08-08/ch4-doppler-rate-defect.json` |
| Q3 | `deep fade pilot aided carrier phase recovery decision directed RLS cycle slip high order QAM coherent optical` | S2 / OpenAlex / Exa | OpenAlex=1，S2=0，Exa=HTTP 402 | `1 / 1 / 1` | `search-archive/2026-08-08/ch4-pilot-rls-fade-defect.json` |
| Q4 | `high order QAM low SNR cycle slip feedforward carrier phase recovery coherent optical fixed window defect` | S2 / OpenAlex / SerpAPI | SerpAPI=12，S2=0，OpenAlex=0 | `12 / 12 / 12` | `search-archive/2026-08-08/ch4-feedforward-cpr-cycle-slip-defect.json` |

说明：`kept` 是项目相关性筛选后的缓存结果数。Q2/Q3 的 Exa 请求失败不是命中；Q1 的关键 FSTS 证据来自检索前已有本地全文精读笔记，不把 0 命中改写成外部支持。逐源 stdout receipt、raw/dedup/kept 与四个 cache SHA256 已持久化到 `search-archive/2026-08-08/ch4-reference-source-expansion-receipt.json`；该 sidecar 明确标注 raw/dedup 来自 fresh-context source scout 的执行回执、未重跑 query，避免把缓存可复算范围写得更强。

## 3. 候选来源与保留边界

本地索引先确认两个 2019+ 具体 reference：Wang et al., *IEEE Photonics Journal* 2023，DOI `10.1109/JPHOT.2023.3265847`；Liu et al., *Journal of Lightwave Technology* 2023，DOI `10.1109/JLT.2023.3276637`。只保留两个机制不同对象：

1. **C1 RML-FSTS**：FSTS 细频偏估计的 fixed-lag/`BL` 条件依赖；未来动作占位为 receiver-visible reliability-weighted multi-lag circular fusion。
2. **C2 BUM-CMA**：多孔径 `2N×2` CMA 的分支不确定性掩码；候选 defect 是弱分支污染固定步长更新，但 source-domain 证据不足。

未保留 Q2–Q4 中的 Doppler-rate、pilot-RLS repair、adaptive VV/BPS/window 候选，因为分别命中 B3-Q2、B10、C3/P09 或 Paillier/K01 等 exact historical object/action 边界；这只是 exact collision 拒绝，不外推为整个 FOE/CPR/equalization 家族禁令。没有制造第 3 个候选来填满上限。

## 4. E1–E8 总表

| 候选 | E1 External reference | E2 Published defect | E3 FSO transfer | E4 Smoke contract | E5 One future action | E6 Collision boundary | E7 Chapter path | E8 Budget | 入口裁决 |
|---|---|---|---|---|---|---|---|---|---|
| **C1 RML-FSTS** | PASS | PASS | PASS（可证伪推断） | PASS（含 strongest-cheap-alternative 与 identity 退出门） | PASS | PASS（tight claim ceiling） | PASS_SHAPE | PASS_CONDITIONAL | **READY_FOR_GW_STEP1_DEFECT_REPRODUCTION** |
| **C2 BUM-CMA** | PASS | **FAIL / UNVERIFIED** | PASS_INFERENCE | **FAIL** | PASS_SHAPE / identity unknown | PASS_NO_EXACT，但邻近度高 | **FAIL** | **FAIL / >7d risk** | **REJECT_AT_ENTRY** |

只有 C1 八门全过。C2 的 weak-branch gradient pollution 不是论文已发表 defect，不能用物理直觉替代 E2，也不能因有多孔径代码就降低 E4/E7/E8。

## 5. 逐候选 FACT / INFERENCE / UNKNOWN

### C1 — RML-FSTS（Reliability-weighted Multi-Lag FSTS）

**Reference identity / FACT**

- Wang et al., “Carrier FOE Scheme Based on FSTS in Spatial Diversity PM Coherent FSO Communication,” *IEEE Photonics Journal*, 2023, DOI `10.1109/JPHOT.2023.3265847`。本地精读笔记确认正式发表、双偏振 FSTS、先 frame sync 再 MRC/偏振解复用/两级 FOE，输入只需接收复样值与已知训练结构。证据：`papers/_read_notes/10.1109_jphot.2023.3265847.md:5-17`。
- 论文固定 320-symbol 设计在 4-QAM 使用 `BN=16, BL=20`，16-QAM 使用 `BN=8, BL=40`；低接收功率下 timing peak 可能不可辨，且 proposed FOE 精度可能低于其他算法。证据：同笔记 `:19-21`。
- baseline 依赖共同 CFO/LO、相邻符号尺度慢变以及 FS 已正确定位；FOE 是 1 sample/symbol，不覆盖 fractional timing/SCO。证据：同笔记 `:45-52`。

**Published defect / FACT**

- 可承重 defect 只写成：**单一 fixed lag/`BL` 的合适取值依赖调制、训练长度与接收功率；低功率下固定设计会出现可测的 timing/FOE 退化**。论文已有 `BL/BN` 扫描、normalized CFO-MSE 与低功率边界；不得扩大成“星地时变 outage 已被论文观察”。证据：同笔记 `:16-21,28-43,87-96`。

**FSO transfer / INFERENCE**

- 星地强湍流与分支耦合变化可能让不同 lag 的相关量呈异方差；相关幅值是 receiver-visible 信息，因此“已按 modulation/TS length/received-power 条件化的最强廉价 single-lag policy 是否仍在同一可见条件内失配”可以低成本证伪。
- 否决条件：held-out 条件中不存在同一 modulation/TS/power bin 内的 lag-ranking crossover，或 dev-frozen conditioned single-lag policy 在 MDE 内覆盖全部条件，则 transfer mechanism FAIL，退出对象；不把这种 FAIL 改写成整个 FSTS/FOE 家族失败。

**UNKNOWN**

- 目标星地 testbed 的真实残余 CFO 分布、各分支相关性、同一 receiver-visible condition 内 lag-ranking 是否交叉，以及 conditioned single-lag policy 是否已吸收全部差距均未知。
- 现有 B3 scaffold 不是论文忠实实现：细估采用简化单支路 FFT，frame-sync 模板也明确标成单偏振简化。证据：`projects/simulation/explore/b3-joint-estimation/joint_estimation_pipeline.py:48-70`、`frame_sync_fsts.py:15-78`。这只形成未来 identity 退出门，不在本轮实现修复。

**未来唯一 action 占位**

- 仅允许：由各 lag 当前/历史相关幅值形成归一化可靠度，对多个 lag 的 CFO 圆周估计作一次融合。输入为 receiver-visible correlation；输出为一个 CFO estimate。
- 不允许变成 frame relocalization、Doppler-rate regression、branch routing、逐格 lookup、纯 scalar retune 或 truth/genie 选择。

### C2 — BUM-CMA（Branch-Uncertainty-Masked 2N×2 CMA）

**Reference identity / FACT**

- Liu et al., “Multi-Aperture Coherent Digital Combining Based on Complex-Valued MIMO 2N×2 Adaptive Equalizer for FSO Communication,” *JLT*, 2023, DOI `10.1109/JLT.2023.3276637`；其 baseline 是多孔径 X/Y 复样值进入 `2N×2` butterfly，以 CMA/RDE 更新 tap 并输出合并后的双偏振符号。证据：`.sessions/2026-07-10-dual-pol-osl-groundwork/S038-residual-cascade-read.md:75-86`。
- 论文支持 branch skew 会延长收敛或失败、大线宽会伤害后级载波恢复；它没有支持“弱分支污染固定步长 CMA gradient”这一承重 defect。

**FSO transfer / INFERENCE**

- 独立 Gamma–Gamma 分支衰落可能造成 branch-gradient 可靠度差异；但这只是目标机制假设，不能填补 source-domain published defect 缺口。

**UNKNOWN / FAIL**

- weak-branch gradient pollution 的 source-domain failure、MDE 与 faithful `2N×2` runner 均未闭合；0.5–1 天内不能同时完成 baseline 重建与 defect smoke，E2/E4/E7/E8 失败。
- future action shape 可描述为 receiver-visible branch-confidence update mask，但连续 soft mask 可能只是 branch-specific step-size calibration。P05 已有 confidence-gated CMA-loss update，C15 也有 fade/confidence gating 邻域；虽非 exact branch-wise `2N×2` collision，claim 区分度过低。

## 6. 唯一入口与未来 0.5–1 天 smoke contract

**terminal：`ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1`**

唯一入口为 **C1 RML-FSTS research object**。此名称只是对象占位，不是方法名、Q#、Go、METHOD_SIGNAL 或论文贡献。

### 未来 defect-reproduction smoke（只预注册，本轮不运行）

| 字段 | 冻结合同 |
|---|---|
| 目标 | 复现“fixed lag/`BL` 在低功率、多调制/湍流条件下出现条件依赖与可测退化”；**不测试 RML-FSTS 方法** |
| 时间预算 | 总计 0.5–1 天；首先做 reference identity preflight，若 1 天内不能忠实复现 fixed-`BL` baseline，立即 `FAIL/BLOCKED_TESTBED` 退出 |
| 冻结 cell/input | PM-4QAM 与 PM-16QAM；320-symbol FSTS；论文 `BN/BL`；弱/强湍流；同一 branch count、CFO distribution、received-power grid、paired seeds；held-out 前用独立 dev seeds 冻结参数 |
| 传统 baseline | 论文 fixed-`BL` two-stage FSTS FOE |
| 最强廉价替代 | dev seeds 上冻结的 **conditioned single-lag lookup**：至少按已知 modulation、TS length 与 receiver-visible received-power bin 选择一个 lag；映射、bin 与 lag 集在 held-out 前冻结，不得用 turbulence truth 或 held-out cell 逐格调参 |
| 诊断上界 | held-out per-cell best lag 只作 defect/headroom 诊断与 Kill 工具，不作为未来动作或 Go comparator |
| primary metric | normalized CFO-MSE + 预注册 FOE-outage（阈值在 GW Step 1–3 后冻结）；BER 仅作辅证 |
| PASS | 在同一 modulation/TS/power bin 内至少两个 held-out turbulence/branch conditions 出现稳定 lag-ranking crossover，且**最强 conditioned single-lag lookup**相对诊断 best-lag bound 仍有 `≥20%` MSE regret 或 `≥10 pp` outage regret，并超过预注册 MDE；论文 fixed `BL` 单独失败不能过门 |
| FAIL / 退出 | 无上述同-bin crossover；或 conditioned single-lag lookup 在 MDE 内覆盖全部条件；或 baseline identity 不能在 1 天内闭合。FAIL 只关闭该 transfer hypothesis，不计 T002 entry screening 为对象失败；后续 smoke 若 evidence-valid 执行，才按 D003 开始计数 |

## 7. Exact collision / prior-art claim ceiling

- **Exact collision 排除**：RML-FSTS 不改变 frame location，不估计 Doppler rate、不做 CPE joint estimation、不复活 K01/P1/C3/K02/K03/CCISP scalar calibration。B3-Q2 被 Kill 的是 FSTS+CPE/Doppler 联合估计；其物理失败与“多 lag reliability fusion”不是同一 action。证据：`.sessions/2026-07-08-b3-joint-estimation/decisions.md:177-227`。
- **邻域 prior art**：reference 本身已有 lag=1+`BL` 两级估计；Yu et al., “Joint Physical Layer Frame Optimization and Carrier Synchronization for Satellite Communications,” *IEEE TVT*, 2023, DOI `10.1109/TVT.2022.3218937`，明确讨论 AC/CC estimator 的范围—精度权衡并提出 stepwise correlation-based CFO estimator。共享论文库证据：`D:/code/study/research-protocol/papers/doi/10.1109_tvt.2022.3218937/source.md:3-9,41-53`。因此未来 claim ceiling 只能是“FSTS 特定、湍流/低功率条件下，以 receiver-visible reliability 做多 lag 圆周融合”，不能声称首创 multi-lag/stepwise CFO、FSTS、联合同步或 Doppler estimation。
- **廉价替代处置**：dev-frozen modulation/TS/power-conditioned single-lag lookup 必须进入 smoke，且它仍失败才可 PASS；equal-weight fusion、single-lag、论文 `BL` 必须进入未来方法包消融。邻域 prior art 限缩 claim，不泛化 Kill 整族。

## 8. Object/package 计数

- T002 结束后：`research-object failure=0 / executed defect-smoke failure=0 / method-bearing package failure=0`。
- C2 是 entry `REJECT_AT_ENTRY`，不计对象失败；C1 是 entry ready，尚未执行。
- 只有下一轮从 Groundwork Step 1 合法启动、Step 1–3 通过并在 Step 4a evidence-valid 执行 smoke 后，才产生首个可计数结果。

## 9. 下一合法动作与禁止动作

### 下一合法动作

新对话完整重读 `stages/groundwork.md`，以 C1 的 fixed-lag/`BL` condition-dependence 为 research object，从 **GW Step 1** 开始。只有 Step 1–3 完成并合法进入 Step 4a 后，才能冻结并运行上述 defect-only smoke。

### 禁止动作

- 不从本报告直接运行 smoke、实现 RML-FSTS、修改仿真参数或创建科学 runner/artifact。
- 不把 `ONE_DEFECT_REPRODUCTION_ENTRY_READY_FOR_GW_STEP1` 写成 defect 已成立、Q#、Go、METHOD_SIGNAL、方法或章节已形成。
- 不并行启动 C2，不补第 3/4/5 个候选，不复活合同列出的 exact historical object。
- 不修改 Skill、旧 dormant topic、正式论文、protected history 或四个 `p05_run*.log`；不 push。

## 对决策的影响

产生 D004：唯一选择 C1 进入后续 Groundwork Step 1 defect-reproduction；本轮 mission method delta 仍为 `NONE`。
