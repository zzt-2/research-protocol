# Information-Source Candidate Map v1

> 组合级 Map（D019 / H012）。**不按模型名（EKF/GRU/Transformer）拆方向，按"信息来源 × 作用点 × 输出动作"组织**。
> 候选 = "新增的合法信息是什么"，不是"换个网络结构"。
> 日期: 2026-07-22 | 来源: S011/D017/D018/D019 + 探索子 agent A/B/C 三方盘点 + 主线源码核验

## 排序维度（统一，本表用此 8 维打分 1-5）

1. **合法 headroom** — 在 scoring-only/oracle 条件下，相对公平传统 baseline（fixed-μ CMA μ=0.03 + blind_affine_compare_16qam）能关闭多少可恢复 PI-SER 余量。来源 = Probe（本批未跑前为先验）。
2. **receiver 可观测性** — 新增信息在 inference 时是否真的可见（不偷用 eval truth）。
3. **物理实用性** — pre-FEC BER/GMI/FEC 阈值距离；当前无 FEC chain 时只能报相对收益（domain-comms.md:164-171, communications.md:75-91）。
4. **公平传统 comparator 可建立性** — 是否有广泛采用、任务适配、可公平调参的传统对手。
5. **基础设施成本** — SMALL_ADAPTER（半天内）/ HALF_DAY / MULTI_DAY / INFRASTRUCTURE_BLOCKED。
6. **文献新颖性** — 撞车风险（尤其 pilot→Jones→inverse 已 COLLISION；C16 HOS 已 task-mismatched）。
7. **毕业论文贡献潜力** — 主结果 / 次级材料 / 负面材料。
8. **可逆性与失败后的次级材料价值** — Kill 后仍可作方法论/边界材料。

---

## 候选清单（按信息族）

### 族 1 — channel-model prior（信道物理模型先验）

合法信息 = GG/SOP 状态模型（α/β、sop_rate、τ_c、AR(1) ρ≈0.99997），不是另一条盲 cost。
作用点 = CMA/SOP 均衡（AP10）+ 载波/CPR（AP07-09）。输出动作 = estimate（Jones / 残差相位）→ 喂 MMSE 均衡器。

| ID | 候选（信息来源 × 作用点 × 动作） | 合法信息 | 可见性 | comparator | 物理门限 | 基建 | 撞车 | 论文 | 否决条件（falsifier） |
|----|------|------|------|------|------|------|------|------|------|
| **F1-A** | GG/SOP **真状态**作 scoring-only oracle（per-block h, θ → 精确 Jones → per-block MMSE） | eval-truth h, θ | scoring-only | fixed-μ CMA | 无 FEC→报相对收益 | SMALL_ADAPTER（h/θ 已在 channel return, `_dual_pol_channel.py:139-140`；Jones 可解析重建 `sqrt(h)*[[cos,sin],[-sin,cos]]`） | 与 oracle_affine 同级（已是 Kill 工具范式） | headroom 上界 / 负面材料 | oracle headroom < 0.03（与 D018 同阈值）→ Kill 整族 |
| **F1-B** | **可部署 model-based tracker**（EKF/KF on Jones 用 GG/SOP 模型先验） | receiver-estimated Jones via model dynamics | receiver-visible（causal） | fixed-μ CMA + blind_affine_compare_16qam | 同上 | MULTI_DAY（现有 `_kf.py` 是 single-pol pilot-based，CB3 警告 silent Y-drop `capability-leverage-atlas.v1.yaml:111-114`；需新建 dual-pol model-based） | 文献 EKF 非占位邻居（topic-index.md:262 R007），但 OSL GG+SOP + dual-pol 组合未被本项目占 | 主结果潜力（model-driven 均衡） | F1-A oracle headroom 不存活 → 不建；observability Probe FAIL → 不建 |
| **F1-C** | model-driven 等化（用 model prior 形成非盲代价 / 软约束 on CMA 权重） | GG/SOP 约束信号 | receiver-visible（model 推断） | fixed-μ CMA | 同上 | HALF_DAY（在 CMA 损失上加正则项） | 中（与 MMA/ring-aware cost C15 撞族，但信息来源不同） | 次级 | F1-B 不存活 → 不建 |

**族 1 前置 Probe（最轻量）**：先跑 F1-A oracle headroom（model-based tracker 的上界）。只有 F1-A 显示 ≥0.03 headroom 且 receiver-visible observability 可证，才进 F1-B/C。
**已知未堵死**：D018 只 Kill 了"同类盲 FIR 专家路由"，model-based tracker 维度仍 `IDENTIFIED_NOT_EXECUTED`（portfolio/current.yaml:93-100）。

### 族 2 — sparse/adaptive pilot（稀疏/自适应导频）

合法信息 = 已知 pilot 符号（CSI_PILOT）→ 估 Jones → 喂均衡器。**必须与旧 pilot→Jones→inverse 去重**（p03 COLLISION）。

| ID | 候选 | 合法信息 | 可见性 | comparator | 物理门限 | 基建 | 撞车 | 论文 | 否决条件 |
|----|------|------|------|------|------|------|------|------|------|
| **F2-A** | pilot-aided Jones **oracle headroom**（真 Jones + 量化 pilot 数→ overhead vs headroom 曲线） | 真 Jones（scoring）→ 模拟不同 pilot 密度下 LS/EMA 估计精度 | scoring + 模拟 | blind CMA + fixed-μ CMA | pilot overhead ≤10%（CB3 预注册 `capability-leverage-atlas.v1.yaml:124`） | SMALL_ADAPTER（无 pilot 注入代码；模拟即可，Jones 可从 θ/h 解析重建） | **高**（JLT 2023 / LCOMM 2026 / OE2021 / TCOM2025 / JLT2022-23 全是 pilot-Jones 直接竞品，p03:150-163 D055） | 次级 / 负面 | headroom < 0.03 或撞车确认 → Kill；机械与 p03 等价 → 直接 COLLISION |
| **F2-B** | **半盲状态估计**（pilot + blind CMA trace 联合，非纯 Jones-LS） | pilot + z-stream 联合 | receiver-visible | blind_affine_compare_16qam + pilot-LS baseline | overhead ≤10% | HALF_DAY–MULTI_DAY | 中（半盲是新机制，但落到 OSL 仍可能撞 JLT2023） | 主结果潜力 | F2-A 不存活 → 不建 |
| **F2-C** | **自适应 pilot 调度**（按 GG 衰落 / SOP 漂移动态分配 pilot） | 调度决策 + pilot | receiver-visible | 固定调度 pilot baseline | overhead ≤10% + latency | MULTI_DAY | 低（调度是 OSL 新角度） | 主结果潜力 | F2-A/B 不存活 → 不建 |

**族 2 前置 Probe**：F2-A 模拟 pilot overhead 曲线 + 撞车核查（JLT 2023 / OE 2021 三-pilot RSOP 等）。若 F2-A 与 p03 机械等价 → 直接 COLLISION，不复活。

### 族 3 — causal temporal history（因果多 block 历史）

合法信息 = 过去 block 的 z-stream / 权重轨迹（causal），预测未来状态或动作。
**必须证明历史确实增加信息，不能假设 RNN 自动创造信息**（C11 已证 DD-LMS 在合法化后无收益 D011/D012）。

| ID | 候选 | 合法信息 | 可见性 | comparator | 物理门限 | 基建 | 撞车 | 论文 | 否决条件 |
|----|------|------|------|------|------|------|------|------|------|
| **F3-A** | **历史信息增量 Probe**（用过去 K block 的 z/权重预测当前 block 最优动作/状态 vs 仅 block-0） | 条件互信息 / 预测 R² | scoring（用 oracle 标签量化增量） | block-0-only baseline | — | SMALL_ADAPTER（CMA trace 已在 cb1_cell_runner standard_cma_godard_with_z 输出 w_norm_traj/z_amp_traj） | 低 | 次级 / 方法论 | 条件互信息 ≈ 0 → 历史无增量 → Kill 整族 |
| **F3-B** | 多 block 因果状态估计（KF on per-block Jones 用 GG AR(1) ρ≈0.99997） | 历史 Jones 估计 | receiver-visible | per-block blind + F1-B | 同 F1-B | HALF_DAY–MULTI_DAY | 中（与 F1-B 重叠，但用历史而非模型先验） | 次级 | F3-A FAIL → 不建 |
| **F3-C** | learned 跨帧 re-init / 控制（用历史决定何时/如何 reinit） | 历史 trace + 动作 | receiver-visible | C03/C07 threshold reinit | action hook 缺（INFRASTRUCTURE_BLOCKED） | MULTI_DAY（需 action hook） | 中（C03/C07 已 IDENTIFIED） | 次级 | F3-A FAIL 或 action hook 不建 → 不建 |

**族 3 前置 Probe**：F3-A 历史信息增量（条件互信息 / 预测 R²）。若过去 block 对当前最优动作/状态无超出 block-0 的条件信息 → 整族 Kill。
**已知未堵死**：C11 只测了"per-symbol DD-LMS on 固定 block"，未测"多 block 跨帧状态连续性"。

### 族 4 — decoder/CRC/soft feedback（译码/CRC/软反馈）

合法信息 = decoder/CRC/soft 输出反馈到前端。**C12 旧 GMI 上界无效（oracle 仅换全局 σ²，histogram-MI scale-invariant，`soft_demap.py:344` + V006:220），进族前必须先修 metric/oracle 语义**。

| ID | 候选 | 合法信息 | 可见性 | comparator | 物理门限 | 基建 | 撞车 | 论文 | 否决条件 |
|----|------|------|------|------|------|------|------|------|------|
| **F4-A** | **修正后的 soft/GMI oracle headroom**（用 per-symbol/per-block σ² 而非全局 σ²，做真上界） | per-symbol LLR（scoring，用 TX truth 算真后验） | scoring | max-log soft demap | GMI 阈值（无 FEC→报相对 GMI 增益） | SMALL_ADAPTER（`soft_demap.py` + `gmi.py` 已建，仅需 oracle 改 per-symbol σ² + 用 analytic GMI 交叉验证） | 低（C12 资产 H067 保留） | headroom 上界 | 修正后 oracle GMI headroom ≈ 0 → Kill 整族 |
| **F4-B** | coded receiver 前端闭环（decoder/CRC feedback → CMA/SOP 修正） | decoder/CRC 输出 | receiver-visible（需 coded chain） | uncoded CMA | coded BER/FER 阈值 | **INFRASTRUCTURE_BLOCKED**（无 FEC chain，p04 EXTERNAL；CB2 HIGH_multi_day） | 中 | 主结果潜力（coded 闭环） | 无 FEC chain → blocked，不写成科学失败 |
| **F4-C** | CRC-flip 标签监督（H1 标签纠错，topic-index.md:330 S033/D039） | CRC → 翻转标签 | receiver-visible | PI-BER baseline | — | SMALL_ADAPTER | **已证 = PI-BER**（5591× fixed-label BER 是 trivially PI-BER） | 负面材料（已结案） | 已 Kill（trivially = PI-BER），不复活 |

**族 4 前置 Probe**：F4-A 修正后 soft/GMI oracle headroom（per-symbol σ² + analytic GMI 交叉验证）。若修正后仍无 headroom → 整族 Kill；若存活 → F4-B 需要 coded chain 基建（INFRASTRUCTURE_BLOCKED，需用户授权投资）。

---

## 去重与已堵死轴（不复活清单）

- **HYBRID_ROUTING**（D018 VERDICT_C_CLOSED）：CMA↔MMA/DD-LMS 同类盲 FIR 专家路由。本批不复活。
- **C13 pilot→Jones→inverse→pre-CMA**（p03 COLLISION）：与 U05/U36/U52/RC3 机械等价。F2 必须与 p03 比对，等价即 COLLISION。
- **C12 GMI 全局-σ² oracle**（D017/V006 scale-artifact）：F4 必须用 per-symbol σ² 修正，否则复刻 artifact。
- **C16 非-FIR HOS 专家**（D017 task-mismatched）：非合法 fallback expert，不进专家池。
- **C04/C09 self-referential 目标**（D016/D017 UNRESOLVED）：未在 corrected target 上重跑；p01 已证 3 个 corrected objective 有 input-dependent optimum（未堵死，但不在本轮 4 族范围）。
- **seeds 71-80**：永久失去 held-out（≥6 批复用，D017）。本批用全新 disjoint seeds。

## 本批不宣称数学完备

四个族是当前可见的主要信息来源，但不穷尽所有可能。审计中若发现机制不同的新信息来源（如 hardware/AGC AP06、joint Rx/Tx AP28），允许追加，但 portfolio 保持 OPEN（`OPEN_PORTFOLIO_NO_COMPLETENESS_CLAIM`）。

## 统一排序（先验，Probe 后用真实数据重排）

| 候选 | headroom(先验) | observability | 物理 | comparator | 基建 | 撞车风险 | 论文 | 可逆 | 合计 |
|------|----|----|----|----|----|----|----|----|----|
| F1-A oracle state headroom | ? | scoring-only | rel | fixed-μ CMA | 5(SMALL) | 5(低) | 4 | 5 | 待 Probe |
| F1-B deployable tracker | ? | 4 | rel | fixed-μ+blind_affine | 2(MULTI) | 3 | 5(主) | 4 | 待 F1-A |
| F2-A pilot overhead curve | ? | scoring+模拟 | overhead≤10% | blind CMA | 4(SMALL) | **1(高)** | 3 | 3 | 待 Probe + 撞车核查 |
| F3-A history MI Probe | ? | scoring | — | block-0-only | 5(SMALL) | 5(低) | 3 | 4 | 待 Probe |
| F4-A corrected soft/GMI oracle | ? | scoring | rel GMI | max-log | 5(SMALL) | 4(低) | 3 | 4 | 待 Probe |

**先验结论**：F1-A / F3-A / F4-A 三个 headroom Probe 都是 SMALL_ADAPTER、撞车低、可逆性高，应**并行**优先跑。F2-A 需先做撞车核查。F1-B/F2-B/F4-B 是后续投资决策。
