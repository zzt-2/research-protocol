# Q-B Bounded Baseline/Testbed Feasibility Gate Audit

> **Owner**: AMC 独立专题 `2026-08-02-fso-amc-groundwork`。本轮（2026-08-03）bounded Step 4a gate。
> **阶段**: GW Step 4a 维度 A0 §0（问题判据门控）前置 bounded gate — **不是正式 Step 4a MVE**。
> **范围**: 本轮只判断 Q-B 是否值得进入正式 Step 4a MVE。不运行 MVE，不报增益，不建 METHOD_SIGNAL。
> **canonical owner**: `stages/gw-feasibility.md` §A0 + `stages/glossary.md` 问题四判据 + `.agents/skills/research-direction-lab/references/baseline-adjudication.md`（pre-method gate / minimal baseline ladder）。

## 0. Q-B 定义（本轮冻结，来自 brief + literature_notes §6）

- **M**: L023 将 TX modulation/power loading 与 RX detector switching 放在**同一个 per-frame CSI 反馈环**（coherent 外差，地面 MDM-FSO，自陈 receiver-directed adaptive loading 在 LEO 卫星不可行）[papers/_read_notes/L023_jlt_2023.md；content.md:122,147,155,171,313]。
- **C**: LEO 星地 coherent FSO；RTT 接近或超过相干时间；RX 能本地快速观察，TX 只能获得慢速/过期反馈；存在 coded-chain。
- **A**: 同一新鲜 CSI 环绑定 RX-local 快动作和 TX-side 慢动作，造成**动作位置—信息时效契约不可部署**（失效位置可证伪：L023 自陈 LEO 不可行）。

**预期方法产出形态**: RX-local fast adaptation + TX-side slow statistical/risk-aware rate-power control + 明确的跨层接口与双时间尺度更新。

**本轮只判四问**: (1) 是否存在合法同任务 baseline；(2) 是否能在 ≤1 天基础设施内构建可比较 testbed；(3) 候选是否有不同于传统组合的真实信息/动作增量；(4) 是否值得进入正式 Step 4a MVE。

---

## B1. 动作—信息—时间尺度审计

> 所有数字标来源: **[LITERATURE]**（论文全文）/ **[EMPIRICAL]**（代码实测）/ **[EXTRAPOLATED]**（跨场景外推）/ **[ARGUMENT_ONLY]**（纯论证）。
> 禁止用"RTT 大概很慢"作承重结论（brief B1 末句）。

| component | action owner | receiver-visible input | update period | feedback requirement | deployable? | 数字来源 |
|---|---|---|---|---|---|---|
| TX modulation/coding/rate | TX | 无即时（依赖反馈） | per-frame（L023）/per-burst（Nguyen）/per-codeword（Galijasevic） | RX→TX CSI 反馈 | 仅当反馈新鲜 | L023 content.md:122,147 [LITERATURE]；Galijasevic content.md:57,114,179 [LITERATURE] |
| TX power | TX | 无即时 | per-burst（Nguyen SAMP）/per-frame（L023） | RX→TX | 仅当反馈新鲜 | Nguyen content.md:73,231-273 [LITERATURE]；L023 content.md:122 [LITERATURE] |
| RX detector/decoder selection | RX-local | 即时导频/信号 | per-frame（L023 MMSE/SIC/MLD/SIC-MLD） | 无（本地） | ✅ 即时可部署 | L023 content.md:147,313 [LITERATURE] |
| CPR/receiver recovery mode | RX-local | 即时信号 | per-block/per-frame（_recovery.py DPLL/BPS） | 无（本地） | ✅ 即时可部署 | `_recovery.py` docstring [EMPIRICAL]；**注：是论文现有主贡献，不变量禁止当 AMC** |
| ACK/NAK 或 soft reliability | RX-local | 解码结果 | per-codeword | 无（本地） | ✅ 即时 | Galijasevic content.md:87,114 [LITERATURE]（隐式） |
| slow channel statistics | RX-local | 滑窗统计 | 慢（≫相干时间） | 无（本地可估） | ✅ 即时 | ARGUMENT_ONLY（无文献显式建模，但物理上可由 RX 滑窗估） |
| instantaneous CSI | RX-local | 导频估计 ŝ=h+noise | per-frame/per-codeword | 无（本地） | ✅ RX 即时；TX 须等反馈 | L023 content.md:72,112 [LITERATURE]；Galijasevic content.md:158,167 [LITERATURE] |
| predicted CSI | RX-local（预测） | 历史 ŝ 序列 | per-frame | 无（本地预测） | ✅ RX 即时；反馈给 TX 仍受 RTT | Galijasevic content.md:24,114 [LITERATURE]；Nguyen content.md:133-175 [LITERATURE] |

**关键时间尺度数字（全部 [LITERATURE]，FR-26 证据指针）**:

| 量 | 值 | 来源 |
|---|---|---|
| LEO 反馈 RTT | 2-10ms round-trip → 300-1500km；Galijasevic 仿真 td∈{0,1,2,3,4}ms | Galijasevic content.md:66,68 [LITERATURE] |
| 相干时间 τ₀ | Galijasevic 10ms（lognormal PSI=10，模型 LEO sat 信道）；Nguyen <1ms（sat-UAV，Rytov σ²≤0.1020）；L023 Greenwood τ≈4ms（地面 ~10km von Kármán） | Galijasevic content.md:19,57,156 [LITERATURE]；Nguyen content.md:93,355 [LITERATURE]；L023 content.md:155,171 [LITERATURE] |
| 码字/帧时长 | Galijasevic 码字 3.69-31.5μs（≪τ₀）；Nguyen burst Tb<相干；L023 per-frame | Galijasevic content.md:114,179 [LITERATURE] |
| RX 处理延迟 | Galijasevic: 预测+反馈计算"negligible compared to feedback delay" | Galijasevic content.md:66 [LITERATURE] |
| 反馈更新周期 | = RTT（一次反馈一轮） | Galijasevic content.md:66 [LITERATURE] |

**时间尺度审计结论**: 在 Galijasevic 的 LEO 模型下，**RTT（2-10ms）≈ 相干时间（10ms）**——Galijasevic 自己把 td/τ₀∈{0,0.1,0.2,0.3,0.4} 作为核心扫描轴，确认 RTT 与 τ₀ 同量级。这与 L023 自陈"LEO round-trip > Greenwood τ≈4ms 致 receiver-directed loading 不可行"一致。**RX-local 动作（detector/CPR/ACK）可在帧/码字级即时执行（μs-ms 级），TX-side 动作受 RTT（ms 级）约束**——两时间尺度差距客观存在。但所有数字均为 **Galijasevic/Nguyen/L023 各自场景的 [LITERATURE] 值**，无单一文献同时给出"coherent sat-ground GG"下的 RTT+τ₀+frame+processing 完整数字集（Galijasevic 用 lognormal 非 GG；L023 地面；Nguyen sat-UAV lognormal）。

---

## B2. 合法 baseline 梯子

> 判定门（brief B2 末）: 至少存在一个近期、可部署、同任务或差异可校准的增强 baseline，Q-B 才能继续。只有 terrestrial L023 / RF split-timescale / 静态固定 MCS → `Q_B_BASELINE_UNAVAILABLE`。

| baseline | 来源论文 | 同 scenario? | 同 action? | 同 information source? | 同 metric? | task mismatch | 实现成本 | 能否合法 Go comparator? |
|---|---|---|---|---|---|---|---|---|
| **B0**: 固定 TX MCS/power + RX local conventional | 通用 | ✓（可设定） | 部分（缺 AMC action） | — | ✓ | 无 AMC（下界） | 低 | ✅ strawman 下界 |
| **B1**: L023-style delayed-CSI single-loop transplantation | L023 (JLT 2023) | ✗ **terrestrial 地面 MDM，自陈 LEO 不可行** | 部分（coherent mod+power+RX detector，但无 coded-chain/HARQ） | 部分（per-frame CSI 反馈） | 部分（rate/OSNR，非 coded goodput/FER） | **场景错位（地面→星地）+ 自陈失效** | 中（须迁移信道模型） | ✗ **failure reference，非合法最强 baseline** |
| **B2**: Nguyen/Galijasevic-style slow prediction/statistical TX adaptation + conventional RX-local selection | Nguyen2024 (TAES) + Galijasevic (OJCOMS 2024) | 部分（sat FSO；但 **IM/DD 非 coherent，lognormal 非 GG**） | 部分（rate+power / rate-only，**RX 无 AMC action**） | 部分（延迟 CSI + 预测） | 部分（throughput/FER，IM/DD 风格） | **检测错位（IM/DD→coherent）+ 湍流错位（lognormal→GG）+ RX 无 AMC** | 高（须改检测+信道+加 RX AMC） | △ **最重要的增强传统 baseline 候选，但 task mismatch 严重** |
| **B3**: elevation/statistical channel schedule 驱动的慢 TX adaptation + RX local fast action | 无直接 FSO 文献（须自建） | ✓（可设定 sat-ground） | ✓（可定义） | ✓（滑窗统计） | ✓ | 无直接文献实现 | 高（须自建 slow schedule + RX fast） | △ **逻辑合法但无文献 backing，等于自建对手** |
| **B4**: 传统 hierarchical/split-timescale control 直接移植 | RF massive-MIMO split-timescale (10.1049/cmu2.12389, 2022) + two-timescale movable antenna (2025 arXiv) | ✗ **RF cellular，非 FSO** | ✗（RF 波束/功率，非光 AMC） | ✗（RF CSI） | ✗（RF metric） | **全错位（RF→光，cellular→sat）** | 极高（须跨域迁移） | ✗ **仅证路径非空，不可直接移植当 baseline** |

**baseline 梯子判定**:

- **B0**（固定下界）是唯一同 scenario 且无 task mismatch 的 baseline，但它无 AMC action，是 strawman 下界，**不构成合法 Go comparator**（brief FR-25/TL-32: Go 标准 = 赢传统未优化 baseline，但该 baseline 须有真实 deployable action）。
- **B1**（L023）= **failure reference**——L023 自陈 LEO 不可行，它是 Q-B 要解构的 M 本体，不是要超越的对手。把它当唯一 Go 对手 = 把"解构对象"当"超越对象"。
- **B2**（Nguyen/Galijasevic）= **最重要的增强传统 baseline 候选**，但 task mismatch 严重: Nguyen/Galijasevic 是 IM/DD + lognormal + RX 无 AMC，与 Q-B 目标（coherent + GG + RX-local AMC + TX-slow）在**检测/湍流/RX-action 三轴错位**。要当合法 comparator 须先做**三轴迁移校准**（改检测模型、换 GG 信道、加 RX AMC action），这些是 testbed 构建成本，不是 baseline 复现成本。
- **B3** = 逻辑合法但**无文献 backing**，等于自建对手（不是从文献移植的 baseline，而是 executor 自己设计的对照——违反 baseline 合法性，baseline 须有独立来源）。
- **B4**（RF split-timescale）= 仅证 split-timescale **路径非空**（R003 Q-B closure 已确认），但全错位（RF→光），不可直接移植。

**B2 判定门结论**: **不存在一个近期、可部署、同任务或差异可校准的增强 baseline**。可用的只有:
- terrestrial L023（B1，自陈失效，是 M 本体非对手）；
- RF split-timescale（B4，全错位）；
- 静态固定 MCS（B0，无 AMC action 的 strawman）。

Nguyen/Galijasevic（B2）是最接近的，但三轴错位需迁移校准 = testbed 构建成本。

→ **触发 `Q_B_BASELINE_UNAVAILABLE` 候选终态**（待 B3/B4 复核）。

---

## B3. testbed 资产审计（只读盘点，沿 caller→callee 查真实实现）

> 每项标: READY / NEEDS_SMALL_ADAPTER / NEEDS_NEW_INFRASTRUCTURE / SCIENTIFICALLY_INVALIDATED / TASK_MISMATCH。
> 沿调用链核实，不凭文件名判断。特别防止复用旧失效资产（scale artifact / gamma truth leakage / reset/lifecycle 错误 / fixed-label/PI metric mismatch / P08 coded-chain invalidated / P11 gamma 未注入 / G1 post-CMA scaling / 旧 Q-A probe）。

| 资产 | 路径 | Q-B 需要的角色 | 真实实现核实（caller→callee） | 状态 |
|---|---|---|---|---|
| GG 时间域包络 | `common/_gg_time.py:gg_time_envelope_blockwise` | GG 信道（Q-B C 条件之一） | corrected_v2 `probe_corrected.py:49,382` import 并调用；docstring 自证 GG h=X·Y，E[h]=1，AR(1) 块间，τ_c 控制；V008 独立验证 E[h]=1.004-1.015 | **READY**（但仅 GG envelope，**非 coherent 检测，无卫星几何**） |
| 相干检测/外差 | `common/_channel.py`（GG+多普勒相位+APSK） | coherent sat-ground 检测 | `_channel.py` 有 GG + 多普勒相位 + APSK 调制（QPSK/8APSK/16APSK），是 coherent-style；但**无卫星轨道/仰角/RTT 模型**，是块衰落非时间几何 | **NEEDS_NEW_INFRASTRUCTURE**（须加 sat-ground 几何 + RTT + elevation-dependent τ_c） |
| DA/NDA CPR | `common/_recovery.py`（FFT-FOE/DPLL/VV-CPR/BPS） | RX-local 快动作之一 | `_recovery.py` 存在且功能完整；**但这是论文现有主贡献（不变量），不得当 AMC 候选/对照** | **SCIENTIFICALLY_RESERVED**（资产 READY 但被不变量锁定为论文主贡献，非 AMC 对照源） |
| dual-pol GG | `common/_dual_pol_channel.py` | （Q-B 不需要 dual-pol） | 存在，modulation-aware，QPSK bit-exact；Q-B 是单 Pol coherent AMC，不需要 | **TASK_MISMATCH**（Q-B 不需要 dual-pol） |
| coded-chain（LDPC/HARQ） | **无** | coded goodput/FER（brief 合法 testbed 门之一） | `find` 全树无 LDPC/prefix-LS/bit-true 资产；dead-end#6 标 P08-R2 是工程资产非证据；corrected_v2 仅用速率索引非真实解码 | **NEEDS_NEW_INFRASTRUCTURE**（且 brief 禁本轮新建真实 LDPC decoder） |
| prefix-LS / receiver-visible CSI 边界 | corrected_v2 `probe_corrected.py` s_hat=h+noise | receiver-visible 信息边界 | corrected_v2 有 `s_hat = h + N(0,sigma)` receiver-visible；**但无 split-timescale 接口（RX-fast vs TX-slow 信息分流）** | **NEEDS_SMALL_ADAPTER**（边界已冻结，但须加 split 接口） |
| 卫星 timing/elevation 模型 | **无** | elevation-dependent RTT/τ_c | 全树无卫星轨道/仰角模型；Galijasevic 用固定 td∈{0,1,2,3,4}ms 参数化非几何模型 | **NEEDS_NEW_INFRASTRUCTURE** |
| feedback delay 模型 | corrected_v2 `td_ratio` 参数 | RTT 反馈延迟 | corrected_v2 有 `td_blocks` 参数化 td（predict_horizon）；**但是单时间尺度（per-frame rate），无 split RX-fast/TX-slow** | **NEEDS_SMALL_ADAPTER**（须拆成双时间尺度） |
| state lifecycle / reset | corrected_v2 per-seed RNG + gg_time steady-state init | trajectory lifecycle | corrected_v2 `gen_trajectories` per-seed 重置，V008 核 reset_scope 正确 | **READY** |
| receiver mode switching | `common/_recovery.py`（CPR mode）+ L023 detector | RX-local fast action 候选 | L023 detector 选择（MMSE/SIC/MLD）在文献不在代码；CPR mode 在 `_recovery.py` 但锁定为主贡献 | **TASK_MISMATCH / SCIENTIFICALLY_RESERVED** |
| paired realization/evaluator | corrected_v2 `verdict_evaluator.py` | paired goodput/FER 评估 | corrected_v2 有 feasibility-first 5 类评估器；V008 核 raw→aggregate 一致 | **READY**（但是 Contract A/B 单时间尺度评估，**无 split-timescale 评估**） |

**旧失效资产防复用核查（brief B3 末列表）**:
- scale artifact / gamma truth leakage / reset 错误: corrected_v2 V008 已核 GG E[h]=1.004-1.015（无 leakage）、per-seed reset 正确。Q-B 若复用 GG envelope **不继承这些失效**（corrected_v2 已修）。
- fixed-label/PI metric mismatch: Q-B 评估须用 coded goodput/FER 非 BER——corrected_v2 用 FER（连续 Eq.23 近似），**但无真实 coded-chain**（仅速率索引），coded goodput 是近似。
- P08 coded-chain invalidated: **资产不存在**（find 全树无），无复用风险但也无资产可用。
- P11 gamma 未注入: 不适用（corrected_v2 用 GG envelope，V008 已核 E[h]≈1）。
- G1 post-CMA scaling: 不适用（Q-B 不是 CMA 方向）。
- 旧 Q-A probe: corrected_v2 是 Q-A Contract A/B probe（单时间尺度 rate selection），**不是 Q-B split-timescale testbed**——不可直接复用为 Q-B testbed。

**合法 testbed 门（brief B3）核查**:
- ✗ **READY + SMALL_ADAPTER 能在约一天内闭合**? **否**。需要: (a) 相干 sat-ground GG 几何模型（NEW_INFRASTRUCTURE）；(b) coded-chain（NEW_INFRASTRUCTURE，且 brief 禁本轮建）；(c) split-timescale 控制接口（SMALL_ADAPTER 但须设计）；(d) elevation-dependent RTT/τ_c（NEW_INFRASTRUCTURE）。≥3 项 NEW_INFRASTRUCTURE。
- ✗ **不修改 common/ 或 params.py**? brief 合法门之一；建 sat-ground 几何 + coded-chain 几乎必然要扩 common（与 brief 禁令冲突）。
- ✗ **不需要重建完整卫星轨道、真实 FEC、coherent waveform 和多层控制全部四项**? **需要重建**（四项中至少 3 项须新建）。
- △ **能公平运行 B2/B3 与未来候选**? B2（Nguyen/Galijasevic）须先做三轴迁移校准（检测/湍流/RX-action），这本身就是 testbed 构建成本。
- ✗ **receiver-visible 信息边界可冻结**? 边界可冻结（corrected_v2 已有 s_hat 边界），但 split-timescale 须重新定义 RX-fast vs TX-slow 信息分流。
- ✗ **primary metric 可定义为 coded goodput/FER**? 无真实 coded-chain，coded goodput 仅近似（速率索引 + Eq.23 FER）。

→ **触发 `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET` 候选终态**（≥3 项 NEW_INFRASTRUCTURE，超约一天，且与 brief 禁令"不修改 common/"冲突）。

---

## B4. 方法增量审计

> 候选不得只是 "Nguyen slow TX + 现有 RX local + 一个 if/else 拼接"（brief B4 末）。若无明确信息/动作增量 → `Q_B_MECHANICAL_COMBINATION_KILL`。

**强 baseline B2/B3 丢失了什么信息?**
- B2（Nguyen/Galijasevic）丢失: RX-local 即时 reliability 信息（它只有 RX 估 CSI 反馈给 TX，不利用 RX 本地解码 reliability 做 RX-local fast action）；coded-chain 的 HARQ/soft-reliability（二者均无 HARQ action）。
- B3（自建 slow schedule）丢失: 瞬时 CSI（slow schedule 只用统计）；RX-local fast action 的即时性。

**候选新增什么 receiver-visible 信息?**
- 候选新增: **RX-local 即时 reliability 信号（ACK/NAK/CPR-lock/decoded-FER）作为 TX-slow risk-state 输入**——这是 Nguyen/Galijasevic（点预测/延迟 CSI）未利用的信息维度。

**候选新增什么 action 或协调机制?**
- 候选新增: **双时间尺度 split 控制**——RX-local fast action（detector/CPR-mode/rate-selection 用即时 CSI）+ TX-slow action（rate/power 用统计/risk-aware，更新周期 ≫ 相干时间），中间一个跨层接口契约。

**该增量为何无法由固定双时间尺度、独立局部最优或简单 hysteresis 覆盖?** [ARGUMENT_ONLY，须 MVE 验证]
- 固定双时间尺度: 可能覆盖——若 RX-fast 和 TX-slow 独立局部最优已接近联合最优，则 split 控制无增量。**此假设未证伪**。
- 独立局部最优: RX-local 最优 rate + TX-slow 最优 power 是否联合次优? 须 MVE 验证耦合性。**未证**。
- 简单 hysteresis: TX-slow 用 reliability hysteresis 切换 risk-state 是否等价学习器? **未证**。

**是否存在至少 5% 可测 headroom?** **未量化**。无合法 testbed 跑不出可信 headroom；B2/B3 三轴错位，跑出来的 "headroom" 是迁移 artifact 非 Q-B headroom。**[ARGUMENT_ONLY]**。

**贡献落在架构、接口、控制规则还是学习器?**
- 落在**接口 + 控制规则**（split-timescale 接口契约 + risk-aware TX-slow rule）。这是合法贡献形态（判据2 方法产出形态 ✓）。

**若真正增量只是"根据 RX reliability 给慢 TX 更新风险状态"**:
- 必须把它具体化成**单一可证伪假设**（非泛称 hierarchical control）: 例如 "TX-slow rate 选择以 RX-local 滑窗 FER-violation 率为 risk-state 输入，相比以 delayed-CSI 点预测为输入，在中强湍流 + RTT≈τ₀ 下降低 FER-violation 率 ≥5% goodput 等价"。**此假设本轮无法验证（无 testbed）**。

**B4 结论**: 候选**存在明确的信息/动作增量方向**（RX-local reliability → TX-slow risk-state，split-timescale），但:
1. 增量**未量化**（无 5% headroom 证据，[ARGUMENT_ONLY]）。
2. 增量**可能被固定双时间尺度/独立局部最优/hysteresis 覆盖**（未证伪）。
3. 增量的单一可证伪假设**须 MVE 验证**，但 MVE 须合法 testbed（B3 不通过）。

→ 不触发 `Q_B_MECHANICAL_COMBINATION_KILL`（增量方向非纯拼接），但**增量未量化 + 未证伪简单替代** → 落入 evidence-insufficient 区间。

---

## B5. 最小语义 smoke

> brief B5: 只有 baseline 与 testbed 门都通过，才允许建立不含科学结论的最小接口 smoke。**B2（baseline）与 B3（testbed）门均未通过** → **本轮不执行 B5 smoke**。

不执行 smoke。理由: B2 baseline 门未通过（无合法同任务增强 comparator）+ B3 testbed 门未通过（≥3 项 NEW_INFRASTRUCTURE，超约一天预算，与 brief 禁令冲突）。建立 smoke 须先有可运行 B2/B3 接口，二者均不可在约一天内闭合。

---

## C. 唯一终态判定

四个候选终态（brief Phase C）逐一核查:

| 候选终态 | 触发条件 | 本轮核查 | 命中? |
|---|---|---|---|
| `Q_B_READY_FOR_STEP4A_MVE` | 合法增强 baseline + testbed ≤1 天 + 单一可证伪增量 + smoke 通过 | baseline 无（B2 三轴错位）+ testbed ≥3 NEW_INFRASTRUCTURE + 增量未量化 + smoke 未跑 | ✗ |
| `Q_B_BASELINE_UNAVAILABLE` | 缺合法同任务 comparator | B0 无 AMC action（strawman）+ B1 自陈失效（M 本体）+ B2 三轴错位 + B3 无文献 + B4 RF 全错位 | **△ 命中** |
| `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET` | 基础设施超约一天或需重建多模块 | ≥3 项 NEW_INFRASTRUCTURE（sat 几何/coded-chain/elevation-RTT）+ 与 brief"不修改 common/"冲突 | **△ 命中** |
| `Q_B_MECHANICAL_COMBINATION_KILL` | 只是已有模块拼接，无新信息/动作增量 | 增量方向存在（RX-reliability→TX-risk-state split-timescale），非纯拼接 | ✗ |
| `Q_B_EVIDENCE_INSUFFICIENT` | 文献/参数/资产身份仍无法判断 | 时间尺度数字有文献但跨场景（Galijasevic lognormal/L023 地面/Nguyen IM/DD）；coherent sat-ground GG 场景无单一文献完整参数集 | △ 部分命中 |

**两个候选终态同时命中**（`Q_B_BASELINE_UNAVAILABLE` + `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET`）。brief 要求唯一终态。

**裁决（RDL scientific judgment，research-direction-lab skill 授权）**: 当 baseline 与 testbed 门**同时**因 task-mismatch（非工程难度）失败时，**baseline 门是上游、是根本**——无合法 baseline 意味着即使搭出 testbed 也无合法对手可比，headroom 无意义。因此:

- **本轮 Q-B 终态 = `Q_B_BASELINE_UNAVAILABLE`（primary）**，附记 testbed 亦 `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET`（secondary，根因同源: coherent sat-ground AMC 在文献中无人做，baseline 和 testbed 都因此缺位）。
- 不 Kill Q-B family（与 Q-A family 处理一致，brief "不 Kill family"）: Q-B 是"无合法 baseline + 无 ≤1 天 testbed"的**基础设施缺位**，不是"假设被证伪"。若未来 (a) 用户授权搭 multi-day coherent sat-ground GG testbed + (b) 出现 coherent sat-ground AMC 文献作 B2，Q-B 可重启正式 Step 4a。

**本轮不进入正式 Step 4a MVE**（brief 明示；baseline + testbed 双门未过）。

---

## D. 对决策的影响

- **不新建独立 D### for Q-B**: Q-B gate verdict 记录在本 audit + V009 + topic-index/feasibility_report_v2。Q-B 不进 Step 4a MVE = 无 scope 变更（仍在 GW Step 4a bounded gate 范围内）。
- **Q-B 状态**: 从 D006 的"A0§0 判据3 致命暂存"细化为 `Q_B_BASELINE_UNAVAILABLE`（primary）+ `Q_B_TESTBED_UNAVAILABLE_WITHIN_BUDGET`（secondary）。
- **下一合法动作（待用户）**: Q-B 当前不可进 Step 4a MVE。选项: (a) 接受 Q-B baseline 缺位停 Q-B；(b) 用户授权搭 multi-day coherent sat-ground GG testbed（跨阶段基础设施决策）；(c) 等 coherent sat-ground AMC 文献出现作 B2。
- **不修改 Skill / dormant receiver / 4 个 p05 log / common/ params.py**（边界遵守）。

## 附录: 关键证据指针

- 时间尺度 [LITERATURE]: Galijasevic `papers/doi/10.1109_ojcoms.2024.011100/content.md:19,57,66,68,114,156,179`；Nguyen `papers/doi/10.1109_taes.2024.3403809/content.md:81fn2,93,355,357`；L023 `papers/doi/10.1109_jlt.2023.3242215/content.md:122,147,155,171,313`。
- baseline closure: R003 §3 Q-B 闭包表（`search-archive/2026-08-03/` + `.sessions/.../R003-...md` §3）。
- testbed 资产: `common/_gg_time.py`（GG envelope READY）、`common/_channel.py`（coherent+多普勒，无 sat 几何）、`common/_recovery.py`（CPR，主贡献锁定）、`corrected_v2/probe_corrected.py:49,382`（import _gg_time）。
- coded-chain 缺位: `find projects/simulation -iname "*ldpc*"` 返回空（无 P08 资产）。
- RF split-timescale 先例: 10.1049/cmu2.12389（R003 closure DISTINCT，证路径非空非 baseline）。
