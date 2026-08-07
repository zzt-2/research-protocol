# [R004] Step 1 综合、候选预卡与 outage-vs-burst 语义门

> 2026-08-07 | 关联：2026-08-07-strong-turbulence-coded-burst-groundwork / D002

## 调研问题

综合 R001–R003，判断是否至少有一个候选同时通过旧 4b#1 reopen gate 与 outage-vs-burst 语义门，从而合法进入 GW Step 2。

## Step 1 receipt

### Query/source/count

| 组 | 技术面 | source | count | 证据 |
|---|---|---|---:|---|
| Q1 | low-elevation strong-turbulence/GG | 本地 `search-archive` + `papers` | 19 个文件级命中 | R001 |
| Q2 | temporal correlation/coherence/AFD/burst | 本地 `search-archive` + `papers` | 39 个首次文件级命中 | R001 |
| Q3 | coded FSO correlated interleaving | S2 + OpenAlex | 20 | R002 / `coded-fso-correlated-interleaving.json` |
| Q4 | channel-aware interleaver/codeword mapping | S2 + OpenAlex | 7 | R002 / `coded-fso-channel-aware-mapping.json` |
| Q5 | parity/bit mapping across fading blocks | S2 + OpenAlex | 20 | R002 / `coded-fso-parity-placement.json` |
| Q6 | recent coded-FSO direct baseline | S2 + OpenAlex | 0 | R002 / `coded-fso-recent-baselines.json` |

总 query 组数 **6/6**。没有追加 query。Q1–Q2 复用本地索引/全文，没有新建 JSON；Q3–Q6 结果为 20/7/20/0。检索 API 只有 S2 + OpenAlex，未达到 `gw-search.md` 的三搜索源门；本地全文可用于证据核对，但不能冒充第三个检索 API。

### Search JSON SHA256

| 文件 | SHA256 |
|---|---|
| `coded-fso-correlated-interleaving.json` | `ac06590665000c45e31c73aa580274f3982d05dfd0d50a63033cf97f31f94972` |
| `coded-fso-channel-aware-mapping.json` | `e29f269e4ab22623eea5cd28a283e50737209fa7ab2c2decb23debbe5d36f932` |
| `coded-fso-parity-placement.json` | `37a3988ea807251e63995ed53b4f7ee176de0cc0fdb289b6835b1a6ca6f86232` |
| `coded-fso-recent-baselines.json` | `c40794548a87b0d37a0b2c509ba2f77dbaf5e6e0f4b04f317b725f10da5f7747` |

### Research note SHA256

| 文件 | SHA256 |
|---|---|
| R001 | `b5704492e57b2a5830cb8252f826dc4a08da97905ac0913a95c2c59d619578ac` |
| R002 | `61a810316dc3173f08cb9df946240430ccf141099ee29733c5095e9127947e92` |
| R003 | `480d1debc18528161e27cc6a91051075179589b75f2bc67d779690da05dc7e0b` |

## 物理参数证据边界

1. 两篇 SPIE 一手物理推导（`10.1117/12.363622`、`10.1117/12.453235`）支持“大天顶角 space/ground 链路可能进入强起伏且 GG 适用”，但本地只有 abstract，未闭合站点、仰角、`α/β`、`σ_R²`、fade threshold 或 AFD 数值。
2. TVT 2022（`10.1109/TVT.2021.3127193`）提供 LEO HV/Rytov/zenith 与相关 burst 建模，但其 strong 分档是仿真输入；同文物理推导在覆盖条件下报告 LEO-to-ground `σ_R²<1`，不能把 `Cn²(0)=10^-13` 仿真标签当真实 occurrence。
3. Light: Science & Applications 2023（`10.1038/s41377-023-01201-7`）外场类比链路实测 few-ms coherence、SI 1–4、`r0≈4 cm`，但它是 53.42 km terrestrial surrogate，不是实际低仰角星地 occurrence。
4. 在各来源自己的高速符号率下，ms 相关时间远大于 810 symbols；这支持“810 symbols 可能全部落在同一相关状态内”的 outage 风险，不支持“存在接近 810 且可通过交织恢复的 burst”。

## 候选预卡

以下三张卡只记录机制与证据缺口。readiness 均为 `HYPOTHESIS_ONLY/ADJACENT`，不是方法卡、Go 或 METHOD_SIGNAL。

### Pre-A：coherence-matched fixed-interleaver design rule

| 字段 | 内容 |
|---|---|
| M-C-A | **M**：2025 CCSDS O3K fixed block interleaver/depth；**C**：一手证据支持的低仰角强湍流、threshold-conditioned fade span 与固定 span 同量级；**A**：固定设计只按静态 depth 配置，若 burst-duration 分布跨过容量，可能形成码字内错误聚集。当前 C/同量级未证实。 |
| 可用信息 | 离线可审计的 AFD/coherence 分布与码率；不使用在线 hidden truth。 |
| 真实 action | 根据物理分布输出固定 depth/buffer/delay 的设计准则，不做运行时 B switching。 |
| 输出 | 固定 interleaver depth 与 delay/reliability design curve。 |
| 最强传统 comparator | Sun & Noh 2025 CCSDS O3K fixed block interleaver；旧唐承茂 B=27 固定 baseline。 |
| collision receipt | 与旧 4b#1 高碰撞：只要落成运行时 depth/B switching 即 exact collision；2012 adaptive interleaving 已按 burst information 切 depth。与 P08/AMC 不同。 |
| 物理参数来源 | SPIE 1999/2002 only abstract + TVT 2022 modeling + 2023 terrestrial surrogate；目标 occurrence/AFD 未闭合。 |
| 指标 | FER/BLER、effective information rate、buffer/de-interleaver delay、outage-conditioned loss。 |
| 方法产出形态 | 解析/半解析固定设计准则；不是孤立 BER 曲线。 |
| Kill 条件 | 固定 deep interleaver 已覆盖 ≥95% 可用收益；所有 810-symbol span 都位于同一不可恢复 fade；或 action 实际退化为旧 depth switching。 |
| 最小 testbed 工程量 | 外层 adapter 3.75–5.0 人日；若需重建完整 lifecycle/runner 为 8.5–12.0 人日。 |
| Step 1 状态 | **FAIL_TO_PASS**：目标 physical/temporal span UNKNOWN，且 collision 风险高。 |

### Pre-B：cross-coherence codeword/parity placement

| 字段 | 内容 |
|---|---|
| M-C-A | **M**：连续码字映射 + 固定 3GPP inner interleaver；**C**：一个码字/缓冲窗可跨多个独立或弱相关 fade block；**A**：映射忽略 code-bit role 与 fade boundary，使关键可靠度集中在同一坏块。当前 C 未证实。 |
| 可用信息 | 仅 transmitter/receiver 可合法获得的 causal/predicted channel-state 或离线相关分布；未来 fade truth 禁止。 |
| 真实 action | 通过外层可逆 `PlacementPlan` 把 systematic/parity/bit roles 分配到不同 channel slots；不改 LLR、码率或 MCS。 |
| 输出 | placement permutation + buffer contract + inverse map。 |
| 最强传统 comparator | continuous mapping、固定 deep/random outer interleaver；generic comparator 为 Chen 2020 SPMM（RF Rayleigh，仅 adjacent）。 |
| collision receipt | 不等同旧 B=27 depth switching；不等同 P08 LLR calibration；不等同 AMC。generic RF/block-fading reliability-aware mapping 已存在，不能声称空白。 |
| 物理参数来源 | 同 R001；尚无目标链路 weakly-independent block count/AFD CDF。 |
| 指标 | FER/BLER、bit-role-conditioned LLR/error clustering、effective rate、buffer delay。 |
| 方法产出形态 | 可复用外层 placement algorithm/准则。 |
| Kill 条件 | codeword 不跨弱相关块；finest oracle 仍整码字失败；future CSI 才能实现；generic prior art 使贡献只剩换场景；无 2019+ FSO task comparator。 |
| 最小 testbed 工程量 | P08-R2 需新增 `BitRoleMap`/placement inverse/per-cw schema，3.75–5.0 人日起；lineage 不可见时增加 1–2 人日。 |
| Step 1 状态 | **FAIL_TO_PASS**：channel lifecycle 未验、FSO exact baseline 不足、testbed controllability=NO。 |

### Pre-C：burst-boundary-aware coded-frame segmentation

| 字段 | 内容 |
|---|---|
| M-C-A | **M**：连续 long-interleaved frames / 固定 codeword boundary；**C**：可观测 burst boundary 与 codeword duration 同量级且存在恢复窗口；**A**：固定边界可能让单个坏区吞没整个码字。当前 boundary/恢复窗口未证实。 |
| 可用信息 | causal receiver-visible fade/burst detector及合法反馈；不得使用 true outage label。 |
| 真实 action | 改 codeword/frame start、segment boundary 或外层 buffer placement；不改 MCS/rate，不以 ARQ 重传作为主 action。 |
| 输出 | segmentation/boundary schedule 与 overhead contract。 |
| 最强传统 comparator | 2024 LEO 工程 long-interleaved frames + fixed segmentation；2025 physical-vs-link-layer interleaving capacity work仅 adjacent。 |
| collision receipt | 与 AMC/HARQ 高邻近，若 action 变成选码率/IR/retransmission 即 collision；与 P08 LLR 不同，与旧 depth switching 不同。 |
| 物理参数来源 | R001 only：few/tens-ms correlation 存在，但 threshold-conditioned AFD 与目标 occurrence 未闭合。 |
| 指标 | FER/BLER、burst-boundary capture、effective throughput、segmentation overhead、latency。 |
| 方法产出形态 | 可复用 segmentation/boundary scheduling rule。 |
| Kill 条件 | burst detector 无 causal signal；segment 仍落在同一 outage；overhead/delay 抵消 FER 收益；最强 fixed deep 已覆盖 ≥95%；无 task-matched comparator。 |
| 最小 testbed 工程量 | 最小 adapter 3.75–5.0 人日；现有 runner 无 segmentation config 或 delay metric，完整为 8.5–12.0 人日。 |
| Step 1 状态 | **FAIL_TO_PASS**：boundary semantics、metric 与 2019+ comparator 均未闭合。 |

## Collision receipt 汇总

- **旧 4b#1/depth**：2003 length、2009 hardware length、2010 optimum depth、2012 burst-information adaptive depth、2025 CCSDS O3K fixed depth 构成连续 prior art；任何 depth/B switching 直接排除。
- **P08**：estimated-CSI equalization、decoder/LLR calibration 是接收侧信息处理，不是 placement。
- **AMC/HARQ**：2025 predictive LDPC-rate control、2024 RC-LDPC IR-HARQ 的 action 是 rate/redundancy/feedback，直接排除。
- **generic prior art**：2020 SPMM bit mapper、2012 block-fading precoding/mapping 证明 reliability-aware placement 不是空白，只能作 adjacent。

## Outage-vs-burst 语义门

| 问题 | 事实与裁决 |
|---|---|
| finest oracle LLR/decoder 仍整码字失败时，交织是否只移动失败位置？ | **是，若所有参与重排的符号都处于同一深衰落且 oracle 仍失败。** P08-R2 在旧条件下 3/40 B0 all-cw-fail，O2 仍有 2/40 不可恢复；这是风险锚点，不是新强条件结论。目标条件未跑也不得跑。 |
| 固定长交织能否改变边际 BER/FER？ | 纯 permutation 不改变 uncoded symbol-wise marginal BER；只有当编码比特被重新分散到不同可靠度状态且译码利用该分布时，coded FER/BLER 才可能改变。若 span 全在同一 fade，只改相关结构而不增加可恢复信息。 |
| codeword 是否跨多个独立/弱相关 fade block？ | **UNKNOWN / 未证实。** R001 的 ms 量级相对高速 codeword 反而提示多个码字可能共享同一相关状态；没有 target AFD CDF 或 weakly-independent block count。 |
| 当前信道 lifecycle 是否真实保持跨码字相关性？ | **PARTIAL。** P08-R2 caller 一次生成 16-cw trajectory且 cw 边界不重置，但 generator 内部相关过程和 state receipt 未核实。 |
| delay/overhead 是否进入主指标？ | **NO。** 现有 metric 只有 FER/BER；32-symbol prefix、placement buffer、interleaver/segmentation delay均未进入 effective-rate/latency。 |
| strong fixed deep interleaver 是否已覆盖 ≥95% 可用收益？ | 旧中弱条件 B=27 覆盖 100% 已知 burst（0/15 超容）；新强条件 **UNKNOWN**，没有合法 target burst distribution 或 paired comparator。 |

### 语义门结论

`NOT_PASSED / UNKNOWN`。现有证据不能证明“placement/interleaving 可改变可恢复信息分布”，也不足以断言新目标必然由不可恢复 outage 主导。因此不使用 `OUTAGE_NOT_INTERLEAVING_PROBLEM`，而以证据不足停止；不得通过仿真补做 Step 1 证据。

## Reopen gate

| # | 条件 | 结果 | 依据 |
|---|---|---|---|
| 1 | 一手文献支持合法低仰角/强湍流参数 | **UNKNOWN** | 大天顶角强起伏有物理支持；target occurrence/数值未闭合 |
| 2 | burst/correlation span 接近或超过固定 span | **PARTIAL** | correlation 可远超 810，但 threshold-conditioned recoverable burst span未知 |
| 3 | 失败不是整个 coherence-block outage | **UNKNOWN** | P08-R2/外场类比均提示不可恢复风险，无 target oracle 分类 |
| 4 | action 可改变译码输入错误分布 | **UNKNOWN** | 需跨弱相关块；当前 lifecycle 未证实 |
| 5 | 2019+ task-matched baseline | **PARTIAL / coverage insufficient** | 严格口径仅 Sun & Noh 2025 1 篇；Step 2 要求至少 2 篇 |
| 6 | action 不等同旧 B=27 depth switching | **A FAIL / B-C TENTATIVE PASS** | Pre-A 高碰撞；Pre-B/C action 语义不同但未获物理/竞品支撑 |

没有一张预卡六项全过。

## Testbed BOM

- lifecycle=`PARTIAL`；interleaver controllability=`NO`；schema=`PARTIAL`；delay/overhead metric=`NO`。
- 最小 adapter **3.75–5.0 人日**，存在超过 5 天尾部；完整 testbed **8.5–12.0 人日**，高风险且几乎确定超过 5 天。
- 本轮只读，无脚本执行或修改。由于 Step 1 已失败，不以 `TESTBED_SCOPE_EXCESSIVE` 取代更上游的证据 terminal。

## 结论

合法 terminal：`STEP1_EVIDENCE_INSUFFICIENT`。

理由不是“强湍流 coded-burst 物理上不存在”，而是三个承重链接均未闭合：目标 occurrence/AFD、recoverable cross-block span、第二篇 2019+ task-matched baseline；同时现有 testbed 不能直接回答它们。根据用户规定，任一承重条件不成立即不进入 Step 2。

## 对决策的影响

新建 D002：Step 1 停止，Step 2 不执行。三张预卡保留为 HYPOTHESIS_ONLY lineage；未来只有出现新一手 target evidence 与第二篇 task-matched baseline，才可显式重开 Step 1 缺口补证，不能直接进入 Step 2 或 coded-chain。
