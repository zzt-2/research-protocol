# Feasibility Report — 星地相干 FSO AMC Groundwork Step 4a

> ⚠️ **INVALIDATED_BY_D007 (2026-08-03)** — 本报告的**科学层 KILL recommendation 被 D007 撤回**。
> D006 建立在 8 个承重缺陷上（Phase A T1-T10 全部 RED_OBSERVED：B1 未用 per-rate margin/scoring 对齐 k 而非 k+td/FER 当 hard fail/per-turbulence dB-mean 重定心/outage floor 是 action-contract artifact）。
> 正确重测见 **`feasibility_report_v2.md`**（同目录）。本文件**保留不删不改**作 D006 历史证据 + RED 根因材料。
> D006 的**执行合规性声明继续有效**（canonical 顺序 / 不进 4b/5/Contract/Execute / executor 只提 recommendation）。
> 撤回依据: S007/D007/V008（verifier 12/12 PASS CONFIRM）+ corrected_v2 raw + Galijasevic PDF receipt。

> **Owner**: AMC 独立专题 `2026-08-02-fso-amc-groundwork`（S006/D006/V007）。
> 创建: 2026-08-03 | 阶段: GW Step 4a | 状态: **Q-A 实例化 KILL（MVE 证据驱动），family 不 Kill**。
> canonical owner: `stages/gw-feasibility.md` §A0/A′/A/B/D；本报告不覆盖旧 receiver `feasibility_report.md`。
> 候选: Q-A（预测驱动自适应编码的风险失配）— 唯一 survivor（Q-B 在 A0§0 判据3 致命暂存）。

## 0. GW Step 4a 执行合规声明

- 执行顺序: A0§0 → A0§1–6 → A′ → A/B → D(headroom probe) — 合规（gw-feasibility §A0 末"执行顺序"）。
- A0/A′/A/B 任一致命即停止，不靠 MVE 翻案 — 已遵守。
- Go/No-Go 最终决定属用户；本报告提交 **recommendation = KILL**，待用户确认。
- 本轮不进 Step 4b/5/Contract/Execute（brief 明示）。
- Groundwork 整体完成门 = ≥8 篇；当前 5 CORE（Step 3 单步门满足），**即使本轮 KILL 也不宣称 Groundwork 闭合**（缺 3 篇须进 Step 5 前补齐或用户处理）。

## 1. Phase A — A0§0 + A0 §1–6

### A0§0 前置（候选合法性，glossary 四判据 owner = glossary.md L22-31 / templates.md L301）

**Q-A** — literature_notes_amc.md §6 Q-A（L180-196）。canonical 四判据 Step 3 层全 ✅（判据1 M-C-A 明确可证伪；判据2 risk/posterior-aware rule 可复用设计准则；判据3 Galijasevic 2024 直接竞品；判据4 FER违约率/goodput head-to-head）。→ 进 A0 §1-6。

**Q-B** — literature_notes_amc.md §6 Q-B（L197-212）。**判据3 致命**：R003 闭包确认无合法 coherent 星地 AMC baseline（L023/L124/TCOMM2026/LCOMM2026 全 terrestrial；L165 sat 但 AO）。判据3 要求"近期顶刊 baseline 可对标"——目标场景缺位 = **A0§0 致命**。→ 不进 §1-6，暂存。Q-B 进 §1-6 须先自建合法 coherent 星地 AMC baseline（多日新 coded-chain 基础设施 = brief 预注册 Kill 条件之一）。

**唯一 survivor = Q-A**（主控优先项，与 brief 一致）。

### A0 §1–6（Q-A，file:line 证据 + FR-02 来源标注）

| § | 维度 | 判定 | 证据/来源标注 |
|---|------|------|------|
| §1 性能间隙 | PASS（gap 存在，量级待量化） | [EMPIRICAL] Galijasevic content.md:360 自证"adding a small margin improved FER"= 点预测选码存在 FER 约束违约需加 margin；content.md:116 选码=预测增益单值查表。[EMPIRICAL] Nguyen content.md:81脚注2 显式排除估计/量化误差（仅建模反馈时延）→ Q-A 的 C(估计误差同时存在)是开放缝。[ARGUMENT_ONLY] 尾部误差经非线性 FER 门限放大——放大倍数待 Phase C |
| §2 问题结构适配 | PASS | 时变 GG trajectory + 延迟 + 带噪 receiver-visible observation + 预测后验 = 环境动态复杂（时变、随机、非平稳），≥1 项满足 |
| §3 跨域先例 | PASS（≥2 STRONG） | 子 agent 检索（≤500词摘要）：SALAD（arXiv 2510.05784, posterior SINR→BLER-constrained MCS）；Forbes2026（LEO NTN BLER-centric LA under stale CSI，最接近 Q-A 的 C 镜像）；Gao WCNC2024（DOI 10.1109/WCNC57260.2024.10570645，URLLC reliability-constrained）；Chen&Han2023（Bayesian OLLA）。注：Forbes/Song/Chen DOI 标 UNVERIFIED（abstract级，FR-26）；SALAD+Gao 足够支撑 §3 |
| §4 MDP 非平凡 | PASS | S=(ŝ, σ̂, 延迟态)，A=离散码率{8/9…8/77}，R=goodput 约束 FER≤1e-6，P=GG AR(1)（_gg_time.py）。状态空间连续≫1000；贪心选最高码率=Galijasevic=已知违约（§1）→ 非平凡 |
| §5 负面证据 | PASS（no fatal） | 检索未发现"risk-aware rate adaptation fails/not worth it"反例；Chen&Han2023 反向支持（OLLA effectiveness 随 BLER target 收紧而下降 = 点预测可靠性在 FER 门限处退化） |
| §6 先验覆盖 [FR-01] | **⚠ 待 Phase C 量化** | 主指标(a)FER违约率：全局 margin(B2)覆盖度未知；条件 margin(B4/C1)相对增量未知。无法纯分析判定 → Phase C headroom probe 量化（gw-feasibility §A0§6: "无法判断→必须在 MVE 中加入该简单方法作 baseline"） |

**A0 判定**: §1-5 无致命；§6 唯一可能致命点 → Phase C 闭合。**A0 通过（条件性）**。

## 2. Phase B — A′ / A / B

### A′ 竞争维度分解（gw-feasibility §A′）

| 维度 | 先验覆盖度 | 改善空间 | 方法增量来源 |
|------|-----------|---------|-------------|
| (a) FER 约束违约率（主指标，可靠性） | 中（全局 margin 非条件化，重尾区欠覆盖） | 待量化 | C1 用预测残差估条件分位数，全局→条件 margin |
| (b) goodput（主指标，吞吐） | 高（点预测达零延迟 74-101%，Galijasevic content.md:388） | 低-中 | C1 在满足 FER 约束前提下最大化 goodput vs 全局 margin 过保守 |
| (c) 平均码率（次指标） | 中 | 低 | 跟随 (a)(b) |
| (d) 功率/能效（次指标） | 未建模（Galijasevic 固定功率） | 低 | 本轮不竞争 |

**创新声称落点**: 只能落在 (a) FER违约率维度——条件 margin 在 heteroscedastic 重尾下解 FER/goodput 耦合。要求 Phase C 证明条件 margin 相对最强全局 margin 在 (a) 维度 ≥5% 增量且 (b) goodput 代价可接受。**A′ 通过（条件性）**。

### A 结构优势论证（gw-feasibility §A，FR-03 增强基线 + FR-08 范式对齐）

**baseline ladder**（brief Phase B 强制冻结）:

| ID | 方法 | 类型 |
|----|------|------|
| B0 | 保守固定码率 8/77 | 弱先验（稻草人下界） |
| B1 | Galijasevic 点预测 + 原始阈值查表（content.md:116） | **传统 baseline（Go 对手）= M 本体** |
| B2 | Galijasevic + dev-tuned 全局安全裕量（content.md:360 已用的 small margin） | **增强传统 baseline（最强简单先验）** |
| B3 | dev-tuned 经验分位数/quantile 全局裕量 | 增强传统 baseline |
| B4 | 低复杂度条件分箱裕量（predicted-gain 分 K=5 箱，每箱独立 dev-tuned） | 增强传统 baseline（C1 简单版） |
| C1 | 利用可部署预测残差估条件分位数的 risk-aware rate rule（mean+k·σ per bin，k dev-tuned） | 候选最小形式 |
| O1 | 真实信道状态码率选择 | **oracle（仅 Kill/headroom bound，禁 Go）** |
| O2 | 真实条件分布风险最优规则（若定义合法） | oracle |

**结构优势声称**: 当预测误差分布随预测增益值条件变化（heteroscedastic）时，全局 margin 用一个值覆盖所有条件 → 高不确定区欠保护（违约）、低不确定区过保护（goodput 损失）；条件 margin 解此耦合。**FR-08**: 不偏离该领域范式（预测器+查表选码），只升级"点预测→查表"为"预测+残差→条件分位数查表"。**A 通过（条件性：差距消失与否由 Phase C 定）**。

### B 新颖性-可行性解耦 + 空白零假设（gw-feasibility §B）

新颖性（事实，R003 闭包）：FSO 域无 posterior/risk-aware code-rate rule under prediction error。空白零假设 ≥3 结构性原因逐一反驳：
1. "简单安全裕量已经足够" — **部分成立**（Galijasevic content.md:360 自证 margin 有效），但全局非条件化，重尾下非最优。**若 Phase C 证明全局 margin 覆盖 ≥95% → 升级致命**。
2. "预测误差在门限处无足够影响" — content.md:388 自述"线性预测偶尔高估峰值"= 点预测系统性高估 = 支持 A。
3. "GG/延迟/误差联合不物理" — τ_c 物理性核算（见 §3 Phase C C0）：td/tau_c 是谱非二元，td>tau_c **不致命**（Nguyen2024 在 td>tau_c 用 ESN 预测工作，是预测动机非终点）。
4. "Safi 已覆盖" — UNVERIFIED 尾巴（全文 BLOCKED，FR-26 禁推）。
5. "posterior 成本超收益" — 待 Phase C 量化。

**B 通过（条件性）**：3 个待 Phase C 闭合的决策点：(i) 全局 margin 覆盖 ≥95%? (ii) 条件 margin goodput 增量 ≥5%? (iii) τ_c 物理性? (iii 已在 C0 闭合=不致命)。

## 3. Phase C — 解析/MC headroom probe + testbed 物理语义

### C0. Testbed 物理语义验证（brief 强制项，逐项）

| # | 语义项 | 验证结论 | 证据 |
|---|--------|---------|------|
| 1 | GG 输出语义 | 输出辐照度包络 h（intensity/envelope, E[h]=1），块内恒定块间 AR(1)。**与 Galijasevic "fading channel gain" 同构**（Galijasevic 也归一化 E{ρ}=1, content.md:261） | `_gg_time.py:130-156` |
| 2 | coherent SNR 映射 | **本轮不自建 coherent 链**——Galijasevic FER 模型直接用 gain→FER 查表（content.md:116），SNR 隐含在 gain 阈值；headroom probe 直接用 gain→阈值表 | Galijasevic content.md:102,116,128 |
| 3 | trajectory 初始化/reset/连续跨度 | 平稳初始化（_gg_time.py:74,93）；AR(1) 递推；reset=新 seed；连续跨度=n_blocks | `_gg_time.py` |
| 4 | 反馈延迟映射到帧/码字 | td∈{0..4}ms，码字 3.69-31.5μs ≪ τ₀；延迟=预测 horizon | Galijasevic content.md:19,114 |
| 5 | CSI 估计误差来自 receiver-visible observation | ŝ = h + 估计噪声（receiver 观测）；true h 不进 deployable decide | probe 设计保证 |
| 6 | true channel 不进 deployable decide | ✅ C1 用预测残差（历史 ŝ 序列）估条件分位数；O1 用 true h 仅作 oracle | 设计+代码审计 |
| 7 | FER approximation 与 Galijasevic 一致 | **PDF→md 把 eq(23) NA FER 公式转丢**（content.md:244-260 空行）→ **V1 禁靠文字重建**。**绕过**：用 Galijasevic 自带 Table 1 阈值查表（正是 Galijasevic content.md:116 选码机制），不需重建 NA 公式 | content.md:116,128; mve-validation.md V1 |
| 8 | 码率集合与论文一致 | 16 码率 8/9…8/77（72 全集），阈值差 ~0.5dB；Table 1 含 per-rate margin | Galijasevic content.md:128 |

**语义结论**: `_gg_time.py` 调用链语义**一致**，可复用 GG trajectory；FER/选码层需新建（用阈值表，绕过 V1）。**不 BLOCKED**。

### C1. τ_c 物理性核算（dead-end#2 门控）

td/tau_c 物理性扫描: {0.1, 0.4, 0.67, 1.0, 1.33}。td>tau_c **不致命**（Nguyen2024 在此区用 ESN 预测工作）。dead-end#2（反馈延迟>相干时间）在 Q-A **不成立**——延迟>相干时间是预测的动机，非 AMC 终点。**τ_c 物理性 OK，不 Kill**。

### C2. headroom probe（dev/test 隔离，paired，27 cells × 7 methods）

执行: 子 agent 跑脚本（≤15min）；规格: dev seeds 0-49 / test seeds 50-99，n_blocks=1500/cell；grid = td_ratio{0.1,0.4,0.67} × sigma_est{0,0.1,0.3} × turb{(5,2),(2.5,1.2),(4,0.5)}；threshold 用 Table 1（content.md:128）；calib_offset per-turb 冻结于 dev。
- 脚本: `projects/simulation/explore/amc-q-a-risk-aware-rate/probe_headroom.py`
- raw: `projects/simulation/results/amc_q_a_risk_aware_rate/probe_headroom_raw.json`
- metamorphic gate (a) PASS（sig=0,td=0 → B1==O1，goodput diff=0.0）

### C3. V5 独立重算（主线从 raw rows 重算，mve-validation.md V5）

**C3.1 GG outage floor 独立验证**（主线 scipy MC, N=2e6）:
| (α,β) | E[10log10 h] dB | Pr(gain<-6.8dB rel mean) |
|-------|-----------------|--------------------------|
| (5.0,2.0) | -1.62 | **5.74%** |
| (2.5,1.2) | -2.97 | **11.85%** |
| (4.0,0.5) | -6.09 | **19.79%** |
| lognormal PSI=10（Galijasevic 实际用） | — | **15.60%** |

**关键发现 1**: GG outage floor = 5.7-19.8%，**即使 oracle O1 也无法满足 FER 1e-6**（floor 是 2-3 个量级高于 1e-4 目标）。**Galijasevic 自身的 lognormal PSI=10 也有 15.6% floor**——这是 Galijasevic 帧结构的固有特性，非 GG 特有。根因：块衰落下深衰使最低码率(-6.80dB)失败，且 action ladder 无"outage/no-transmit"动作。

**C3.2 C1 vs B1 Pareto 支配独立重算**（27 cells）:
- **C1 在 0/27 cells Pareto-dominate B1（Galijasevic 点预测 M 本体）**。每个 cell 都是 TRADE（C1 更低违约但更低 goodput）= C1 是 B1 的**保守重缩放**，不是 Pareto 前沿外推。
- vs 最强增强 baseline（B2/B3/B4）：C1 在 0/27 cells Pareto-dominate。

**关键发现 2**: C1 无结构性优势——risk-aware 候选只是把 B1 操作点沿 Pareto 前沿向保守方向移动，未扩展前沿。**风险感知候选无法 Pareto-dominate 它要超越的传统 M。**

### C4. 预注册 Kill 条件裁决（brief Phase C）

| Kill 条件 | 触发? | 证据 |
|---|---|---|
| oracle 相对最强增强 baseline 剩余可用空间 <5% | 否（goodput headroom 大） | 但这是 goodput-only 在 floor-violation，非可达可靠性 floor 处 |
| **简单裕量覆盖 ≥95% 主指标且无重要次指标增量** | **是** | C3.2: C1 0/27 Pareto-dominate B1 = C1 是保守重缩放，无前沿外推 |
| **问题退化为静态 margin calibration** | **是** | C1 = 点预测 + k·σ margin = 静态重缩放 |
| 关键 FER 模型无法从原论文闭合 | 否（阈值表绕过 V1） | — |
| testbed 需多日新 coded-chain 基础设施 | 否（NA 近似 + 阈值表，无真实 decoder） | — |
| **更深层诊断**: 主要失效模式 = 不可恢复信道 outage，非预测不确定性驱动 rate over-selection | **是** | C3.1: outage floor 5.7-19.8% >> 1e-4 目标 |

→ **命中 2 个预注册 Kill 条件 + 1 个更深层诊断**。Q-A 的 A（预测不确定性驱动 rate over-selection）在该 channel+threshold 结构下**不是主要失效模式**。

## 4. Phase D — 跳过

Phase C headroom probe（含 paired realizations / dev-test seed 隔离 / 冻结 metric / metamorphic gate / V5 独立重算）**即 §D 的 MVE-等价**，且它 **FAILED**（C3.1+C3.2）。按 gw-feasibility §A0 "A0/A′/A/B 任一致命立即停止，不得靠 MVE 翻案"+ §D "致命信号：MVE 显示核心方法在最简条件下无结构性优势"——Phase C 已闭合为 KILL，无需 held-out MVE。**禁止修修补补后沿用旧 test raw**（mve-validation）。

## 5. Step 4a 决策

**recommendation = KILL（Q-A 当前实例化），family 不 Kill。**

依据（MVE 证据驱动，非 oracle-Kill，符合 TL-32/FR-25 + profile "务实可毕业"）:
1. **C1（risk-aware 候选）在 0/27 cells Pareto-dominate B1（传统 M 本体）** → 候选无结构性优势，是保守重缩放。
2. **outage floor 5.7-19.8% 使 FER 1e-4 目标结构上不可达**（即使 oracle）→ Q-A 的 A 不是主要失效模式；主要失效是不可恢复 outage。
3. 命中预注册 Kill 条件（简单裕量覆盖 / 退化为静态校准）。

**不 Kill family** 的理由: 当前 KILL 针对"Q-A 在 Galijasevic Table-1 阈值查表 + 无 outage action + 块衰落"这一具体实例化。失效模式诊断指出 2 条 reframe 路径（均需新 GW 周期，非本 Q-A 救援）:
- **Reframe (a)**: 加 "outage/no-transmit" action → 改变 M（Galijasevic 无此 action）= **新问题 Q-A'**（须回 GW Step 1-3 重新 M-C-A + 四判据）。
- **Reframe (b)**: 提高 link operating point 使深衰不触底 → 需 gamma_bar offset **14.8-65.8 dB**（不可行，且提高后 AMC 问题可能 moot）。

**可回收产出**（避免沉没成本归零，gw-feasibility §E）:
- 头空间探针脚本（dev/test 隔离 + Table-1 阈值查表 + 7-method ladder）可复用于任何后续 AMC rate-selection 问题。
- **outage-floor 诊断**（GG 中强湍流 + 无 outage action 使 FER 目标不可达）是可引用的研究发现——任何后续 FSO AMC 工作都须先处理 outage floor。
- baseline ladder 设计（B0-O2）+ Pareto-frontier 评估方法是可复用方法论。

## 6. Q-B 状态 & Remaining Groundwork gate

- **Q-B**: A0§0 判据3 致命（baseline 缺位）暂存。Q-B 进 §1-6 须自建合法 coherent 星地 AMC baseline（多日工程）。本轮不并行搭建。
- **Groundwork 整体完成门**: ≥8 篇；当前 5 CORE（L023/L096/L146/Galijasevic/Nguyen2024）。**即使本轮 KILL 也不宣称 Groundwork 闭合**——缺 3 篇须进 Step 5 前补齐或用户处理。
- **Safi/L124 全文 BLOCKED**: Q-A KILL 后 Safi UNVERIFIED 尾巴不再是阻塞（Q-A 已 KILL，Safi 是否覆盖已不影响判定）；L124 coherent-C 族身份闭合仍 open。

## 7. 下一步合法动作（待用户确认）

- **若用户接受 KILL**: (i) Q-B 进 A0§1-6 需先评估自建 baseline 工程量（用户决策）；(ii) 或调整 C 条件 / 换 AMC 子族 / 停止（跨阶段决策，禁 agent 自行放宽 C）；(iii) 补齐 3 篇 CORE 后再议 Groundwork 闭合。
- **若用户不接受 KILL（要求 reframe）**: Reframe (a)/(b) 均需新 GW 周期（新 Q-A'，非本 Q-A 救援），且 (b) 不可行。
- **executor 不能自行最终 Go/No-Go**；本报告是 recommendation，等用户确认。

## 附录: 关键数字证据指针

- probe script: `projects/simulation/explore/amc-q-a-risk-aware-rate/probe_headroom.py`
- probe raw: `projects/simulation/results/amc_q_a_risk_aware_rate/probe_headroom_raw.json`（27 cells × 7 methods，dev/test 分离，metamorphic gate (a) PASS）
- V5 重算: outage floor（scipy N=2e6）+ Pareto 支配（0/27）— 主线独立从 raw 重算，未信子 agent 归因
- Galijasevic Table 1: `papers/doi/10.1109_ojcoms.2024.011100/content.md:128`（16 码率阈值 + per-rate margin）
- Galijasevic 选码规则: content.md:116（预测增益单值查表）
- Galijasevic margin 自证: content.md:360
- Galijasevic 排除估计误差: Nguyen content.md:81脚注2
