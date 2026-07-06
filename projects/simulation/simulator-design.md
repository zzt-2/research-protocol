# 仿真器设计规格 — 单载波时域 NDA-ML 载波相位估计（SC-NDA-ML 正式仿真器）

> 项目: projects/simulation | 阶段: GW Step 6（仿真器设计，gw-experiment §sim）| 日期: 2026-07-06
> 上游: feasibility_report.md（4a+4b Go, D005/D-4b-01）+ decision_log.md（D-S5-01 DA ML 选定）+ MVE-SPEC + `_mve_results.json`
> 框架: gw-experiment.md §sim + FR-12（MVE→Formal 架构差异门控）+ FR-18（环境保真度竞争格局）
> 设计确认状态: ⬜（待用户确认，gw-experiment §sim [MUST]）

## 0. 设计目标

把 MVE 验证过的"单载波时域 NDA-ML 升 M₀=8 次幂"方法工程化为**正式仿真器**，支撑：
1. **主实验**：NDA-ML（提出方法）vs DA ML（FR-15 目标 baseline，D-S5-01）vs oracle（上界）公平对照 BER 曲线
2. **多湍流等级泛化**：AWGN + weak/moderate/strong Gamma-Gamma 块衰落（形态 A+C 双增量）
3. **统计稳健性**：多种子统计（MVE 单 seed → Formal 多 seed 置信区间）
4. **辅助指标**：AIR/BMD（SPEC §7，strong 不可达 HD-FEC 时用）

**不是**重写 MVE——是独立工程实现（守已知债务"MVE 脚本是 `_time_domain_crlb.py` 薄包装，Formal 需独立实现"）。

---

## 1. [FR-12] MVE vs Formal 架构差异对照表（门控核心）

> MVE 架构摘要来源: `_mve_results.json` fr11_architecture_summary。FR-12 要求 Formal 设计与本表对照，差异影响对比机制则重验证。

| 维度 | MVE（来自 §D 架构摘要）| Formal（本设计）| 影响 model→baseline 对比？ |
|------|------------------------|-----------------|---------------------------|
| **动作空间** | NDA-ML 升 M₀=8 次幂盲去调制（连续相位估计）| **一致**（NDA-ML 升 M₀=8，DA ML pilot-aided，oracle genie-aided）| **否**。核心估计算子不变，Formal 只工程化包装 |
| **决策粒度** | per-block（256 符号 CPE 估计 + 256 符号 resolve 模糊 + 100 符号 h 估计）| **基本一致**（256 CPE + 256 resolve），h 估计块 CH_BLOCK=100 不变。**可选消融**：加跨块 KF/CPE 跟踪（FR-18 预判项，作 ablation 不作主路径）| **否（主路径）**。主路径决策粒度与 MVE 一致。跨块 KF 是消融维度，单独报告不影响 NDA vs DA 主对比 |
| **对比范式** | NDA-ML（无 pilot）vs DA ML（pilot sp=4，25% overhead），公平对照含 pilot 能量代价（γ_tot 坐标）| **一致**。公平对照框架不变（DA 总能量 = 信息 SNR + 1.249dB pilot overhead；NDA 总能量 = 信息 SNR）。γ_tot 坐标 | **否**。公平对照框架是 MVE 已验证的核心机制 |
| **奖励语义** | BER @ HD-FEC threshold=3.8e-3（信息符号有效 SNR）| **一致**（主指标 BER @ HD-FEC）+ **辅助** AIR/BMD（SPEC §7，strong 不可达时用）| **否**。主指标不变。AIR 是辅助指标不替换 BER 判据 |
| **先验强度** | DA ML pilot sp=4（pilot-aided 近最优，DRL/先验 = NDA/DA fair gain 0.704-1.922dB）| **一致**。DA ML pilot sp=4 不变（D-S5-01 锁定）。可选 ablation：加 BPS（田野调查候选补充，主面 QAM 场景不同，二级迁移对比）| **否（主路径）**。主 baseline DA ML 强度不变。BPS 是消融/迁移对比非主判据 |
| **统计稳健性** | 单 seed 固定（N_sym=102400/点）| **升级**：多 seed（设计 5 seed，每点 N_sym=102400，总 5×102400）+ 置信区间 | **否**。多 seed 是统计增强不改架构，结论方向不变但置信度升级 |
| **实现独立性** | `_time_domain_crlb.py` 薄包装（已知债务：独立性不足）| **升级**：独立实现（从 `common/` 模块重新组织，不复用 explore 探针）| **否**。代码组织不同但数学算子一致（守 TL-13 共用 `common/_channel.py` 信道实现）|

### FR-12 门控判定

**全部"否"** → 主路径架构与 MVE 一致，**通过 FR-12 门控**，可进 Step 7 实现。

**两个可选消融**（不影响主路径 Go，作 Step 7 ablation 报告）：
1. **跨块 KF/CPE 跟踪消融**（FR-18 预判）：加跨块 KF 跟踪后 cross-over 位置移动，DA ML 高 SNR 可能反超。这是 FR-18 要求的"真实化后竞争格局"验证，作消融非主路径
2. **BPS 迁移对比消融**（田野调查候选补充）：BPS 主面 QAM 场景不同，作二级迁移 baseline 非主判据

### FR-18 环境简化偏差（MVE 已记录）

来源 `_mve_results.json` fr18_competition_analysis：
- **简化项**：单载波时域（无 OFDM DFT 处理增益）+ GG 块衰落（块内 h 恒定）+ per-block 独立 CPE（无跨块跟踪）
- **对主方法（NDA-ML）影响**：升幂噪声放大无 DFT 增益抵消，deep fade 处不利（amp_limit 缓解）
- **对 baseline（DA ML）影响**：pilot sp=4 在 deep fade 块 pilot 受 fade，pilot h 估计噪声大
- **预判真实化后**：加跨块 KF → DA ML 高 SNR 反超强化（cross-over 移动）；加 OFDM 频域 ML → 完全不同架构（B11 路径，已 D002 排除）

**Formal 处理**：主路径保留 MVE 简化（与 baseline 公平），跨块 KF 作消融验证 FR-18 预判。

---

## 2. 模块清单

每模块标功能和引用来源（gw-experiment §sim 要求）。

| 模块 | 功能 | 来源（common/ 复用 / 新实现）| 验证状态 |
|------|------|------------------------------|---------|
| **信道生成** | GG 块衰落 h + Doppler CFO + Wiener PN 三重随机 | 复用 `common/_channel.py:generate_shared_realization_apsk`（守 TL-13）| MVE 已验证 |
| **调制** | (8,8)-16APSK + Gray 映射 + 符号生成 | 复用 `common/_modulation.py:m16apsk_*` | MVE 已验证 |
| **NDA-ML 估计**（提出方法）| 升 M₀=8 次幂盲去调制 + 单正弦 ML 估 CPE + per-block 盲 h + resolve M₀-fold 模糊 | 复用 `common/_recovery.py:nda_ml_recovery`（D003 修复后）+ `resolve_m16apsk_blockwise` | MVE 已验证 |
| **DA ML 估计**（FR-15 baseline）| pilot-aided ML，pilot sp=4 等距，pilot 符号从已知 bits 生成 | 复用 `common/_recovery.py:da_ml_recovery` | MVE 已验证 |
| **两阶段 FOE**（湍流场景）| fft_foe(M₀=8) 粗估 CFO 补偿 + nda_ml_recovery(assume_df_zero=True) 估残余 CPE | 复用 `common/_recovery.py:fft_foe`（D003 约定）| MVE 已验证 |
| **oracle 上界** | genie-aided 真相位 + 真 h 补偿（非 baseline，上界对照）| 新实现（Formal 独立，逻辑同 MVE）| MVE 已验证逻辑 |
| **公平对照框架** | γ_tot 坐标（DA 总能量含 1.249dB pilot overhead）| 新实现（Formal 独立，公式同 MVE-SPEC §4）| MVE 已验证 |
| **BER 评估** | @ HD-FEC threshold=3.8e-3 + per-SNR-point BER 曲线 | 复用 `common/_experiment.py:ber_eval` 模式 | MVE 已验证 |
| **AIR/BMD 计算**（辅助）| (8,8)-16APSK 4 bit Gray label BICM AIR | 新实现（参考 SC-NDA-ML-MVE-SPEC §7）| ⬜ Formal 新增 |
| **多种子统计** | 5 seed × N_sym=102400/点 + 置信区间 | 新实现（Formal 新增）| ⬜ Formal 新增 |
| **跨块 KF/CPE 跟踪**（消融）| 可选 ablation，验证 FR-18 预判 | 复用 `common/_kf.py`（已有 KF 模块）| ⬜ Step 7 消融 |

**复用率**：6/11 模块复用 common/（信道/调制/估计器/FOE/BER 评估），5/11 新实现（oracle 包装/公平对照/AIR/多种子/KF 消融）。**核心算法（NDA-ML/DA ML 估计器）全复用 common/，无新算法实现**——Formal 是工程组织非算法重做。

---

## 3. 关键参数表（gw-experiment §sim + TL-26 溯源）

每参数标来源。[ASSUMPTION] 超 30% 才 STOP（gw-experiment §sim）。本设计 [ASSUMPTION] = 0%。

### 3.1 信号/调制参数

| 参数 | 值 | 来源 | 验证状态 |
|------|-----|------|---------|
| 调制 | (8,8)-16APSK + Gray | B11 行 75-77（params B11Params）| 已验证（MVE 用）|
| M₀（升幂次数）| 8 | (8,8)-16APSK 星座环数，B11 行 75-77 | 已验证 |
| 符号率 BAUD | 25 GBaud | B11 行 143/155（params B11Params.BAUD）| 已验证 |
| 符号周期 T_S | 40 ps（=1/25GBaud）| derived = 1/BAUD | 已验证 |
| N_DFT（DFT 块大小）| 256 | B11 行 155 DFT size | 已验证（`_time_domain_crlb.py:118`）|
| RESOLVE_BLOCK | 256 | D003 修复约定（`_time_domain_crlb.py:125`）| 已验证 |
| CH_BLOCK（h 估计块）| 100 | params ExperimentParams.BLOCK=100（h 块内恒定）| 已验证 |

### 3.2 信道参数

| 参数 | 值 | 来源 | 验证状态 |
|------|-----|------|---------|
| CLW（combined linewidth）| 500 kHz | B11 行 143/155 | 已验证 |
| σ²_p（Wiener PN 每符号方差）| 2π·Δν_CLW·T_S | derived（Viterbi 1963 标准激光相位噪声模型，`_time_domain_crlb.py:131`）| 已验证 |
| Doppler CFO | LEO 500km ~150 MHz/s 推导 | params DopplerParams.f_dot | 已验证（SPEC §1.3）|
| 残余频偏 f_res | ~1 MHz（FOE 补偿后）| derived Δf ≈ 1/(4·N_fft·T_S)，`_time_domain_crlb.py` | 已验证 |

### 3.3 湍流参数（Gamma-Gamma）

| 等级 | α | β | 来源 |
|------|---|---|------|
| weak | 4.0 | 3.0 | SPEC §1.4（夜间/高仰角典型值）|
| moderate | 2.5 | 1.8 | SPEC §1.4（白天/中仰角）|
| strong | 1.5 | 0.8 | SPEC §1.4（低仰角/恶劣天气）|

### 3.4 评估参数

| 参数 | 值 | 来源 | 验证状态 |
|------|-----|------|---------|
| HD-FEC threshold | BER=3.8e-3（7%）| B11 行 181/191 | 已验证 |
| pilot spacing（DA ML）| 4（25% overhead）| D-S5-01 + B11（pilot-aided 近最优）| 已验证 |
| pilot overhead 能量代价 | 1.249 dB（=10·log10(4/3)）| derived（per-symbol avg power equal）| 已验证 |
| N_sym/点 | 102400（400 块 × 256）| FR-21 N≥1e5（`_time_domain_crlb.py`）| 已验证 |
| SNR 扫描 γ_tot（dB）| AWGN [5,8,10,12,14,16,18,20]；湍流 [5,10,15,20,22,24,26] | SC-NDA-ML-MVE-SPEC §6（扩至 26dB 让 weak/moderate HD-FEC 可达）| 已验证 |
| seed 数（Formal 新增）| 5 | [ASSUMPTION] 会议级别统计稳健性约定（MVE 单 seed → Formal 多 seed 置信区间）| ⬜ 待用户确认 |

**[ASSUMPTION] 占比**：1/30 ≈ 3.3% < 30% → 通过。

---

## 4. 验证标准（gw-experiment §sim + Part A 验证清单）

### 4.1 解析验证（已知参数→解析公式）

- [ ] **AWGN BER 解析对照**：NDA-ML / DA ML / oracle 在 AWGN（无湍流）下 BER 曲线与 (8,8)-16APSK 理论 BER 对照（无相位噪声时应贴近理论 Q 函数曲线）
- [ ] **CRLB 对照**：NDA-ML 估计方差 vs CRB_NDA（`_crlb_results.json` meta.analytic_crlb_conclusion.ratio ≈ 1/4）— Formal 估计方差应 ≥ CRB_NDA 且与 MVE 一致
- [ ] **公平对照坐标验证**：DA ML 在 γ_tot 坐标下 BER 曲线 = DA ML 在 γ_d 坐标下曲线左移 1.249dB（pilot overhead 公式验证）

### 4.2 统计验证（分布/自相关）

- [ ] **GG 幅度分布**：生成的 h 样本符合 Gamma-Gamma(α,β) 分布（Kolmogorov-Smirnov 检验，每湍流等级）
- [ ] **Wiener PN 增量正态**：θ(n)-θ(n-1) ~ N(0, σ²_p)，验证增量分布
- [ ] **Doppler CFO 线性漂移**：CFO 随时间线性（f_dot 积分）

### 4.3 退化测试（去随机→确定性）

- [ ] **关湍流**：h≡1 → BER 曲线退化为 AWGN 解析曲线
- [ ] **关 Wiener PN**：σ²_p=0 → 相位恒定，NDA-ML/DA ML/oracle BER 应收敛（无相位噪声时三法接近）
- [ ] **关 Doppler**：f_dot=0 → 无 CFO 漂移，两阶段 FOE 第一阶段 fft_foe 输出 ≈ 0

### 4.4 自相关预警（domain-comms "过于平滑"）

> 实测（Step 7 Part A，2026-07-06）：h 序列 lag-1 自相关 = 0.9902，**超过 0.95 阈值**。诊断后判定**非 bug，是 GG 块衰落物理特性**——块内 CH_BLOCK=100 符号 h 恒定，故相邻样本大概率同块。验证 lag-100（块间）自相关 = 0.0164 ≈ 0，证明块间独立，序列非"过于平滑"假象。

- [x] **lag-1 自相关检查**：h=0.9902（块内恒定物理特性，非平滑假象），θ=0.9994（Wiener cumsum 随机游走，预期接近 1）
- [x] **块间自相关（lag=CH_BLOCK=100）**：h=0.0164 ≈ 0 ✅（块间独立，非"过于平滑"）
- [x] **结论**：非 domain-comms "过于平滑" 反模式（该反模式是缺少随机化模块致自相关过高，本设计有三重独立随机源：GG 块衰落 + Wiener PN + Doppler CFO，块间独立性已验证）

> **阈值修正建议**：对块衰落模型，自相关阈值应分块内/块间——块内 lag-1 高是模型设定（块内恒定），块间 lag≥CH_BLOCK 应 < 0.95。domain-comms "过于平滑" 检查的实质是"随机化是否充分"，用块间自相关判断更准确。

### 4.5 MVE 一致性验证（Formal 独立实现的关键）

- [ ] **Formal vs MVE BER 对照**：同 seed 同参数下，Formal 实现的 NDA/DA/oracle BER 应与 `_mve_results.json` 完全一致（小数值容差，验证独立实现未引入 bug）。**这是 Formal 独立实现的正确性锚点**（守 TL-13 共用 common/ 信道，数学算子一致）

---

## 5. 实验矩阵（Step 7 实现指引）

### 5.1 主实验（必跑）

| 场景 | γ_tot 扫描（dB）| 方法 | seed | 产出 |
|------|----------------|------|------|------|
| AWGN（形态 A）| [5,8,10,12,14,16,18,20] | NDA-ML / DA ML / oracle | 5 | BER 曲线 + fair gain @ HD-FEC |
| weak（α4/β3）| [5,10,15,20,22,24,26] | 同上 | 5 | 同上 |
| moderate（α2.5/β1.8）| [5,10,15,20,22,24,26] | 同上 | 5 | 同上 |
| strong（α1.5/β0.8）| [5,10,15,20,22,24,26] | 同上 | 5 | BER 曲线 + per-point fair gain（HD-FEC 不可达用工作区）|

### 5.2 辅助实验（视情况）

| 实验 | 触发条件 | 产出 |
|------|----------|------|
| AIR/BMD | strong HD-FEC 不可达 | AIR vs γ_tot 曲线（不需 FEC 阈值）|
| 跨块 KF 消融 | FR-18 预判验证 | 加 KF 跟踪后 cross-over 位置变化 |
| BPS 迁移对比 | 论文写作需二级 baseline | BPS（主面 QAM 迁移）vs NDA-ML，标场景不同 |

### 5.3 不做（明确排除）

- ❌ **不加 OFDM 频域 ML**（B11 路径，D002 已排除，架构性不等价）
- ❌ **不加 STO 估计**（Gardner TED 是 B7 候选范围，本方向聚焦 CPE）
- ❌ **不实现 decision-feedback DA ML**（B11 论文 DA ML 形式，债务提示①，Step 7 视情况）

---

## 6. 奖励函数（N/A，估计类方法）

本项目是**信号处理估计算法**（NDA-ML/DA ML 载波相位估计），不是 RL/MDP。gw-experiment §sim"设计奖励函数"+ Part A-checkpoint"MDP 试运行" **不适用**（gw-feasibility §A0 §4 同样判定 N/A）。

**评估指标替代奖励**：
- 主指标：BER @ HD-FEC threshold=3.8e-3（公平对照 fair gain dB）
- 辅助：AIR/BMD（strong 不可达时）、NDA-vs-oracle gap（升幂实现正确性）

---

## 7. 目录结构（gw-experiment 质量门槛：路径合规）

```
projects/simulation/
├── common/                          # 共享基建（已有，复用）
│   ├── _channel.py                  # generate_shared_realization_apsk
│   ├── _modulation.py               # m16apsk_* + resolve_m16apsk_blockwise
│   ├── _recovery.py                 # nda_ml_recovery + da_ml_recovery + fft_foe
│   ├── _experiment.py               # ber_eval 模式
│   └── _kf.py                       # 跨块 KF 消融用
├── simulator/                       # ➕ Step 7 新建（Formal 正式仿真器）
│   ├── sc_nda_ml_sim.py             # 主仿真脚本（独立实现，非 explore 薄包装）
│   ├── fair_comparison.py           # 公平对照框架（γ_tot 坐标）
│   └── air_bmd.py                   # AIR/BMD 计算（辅助）
├── baselines/                       # ➕ Step 7 新建（baseline 实现）
│   └── da_ml.py                     # DA ML pilot sp=4（从 common 包装）
├── results/                         # ➕ Step 7 新建（实验结果）
│   ├── sc_nda_ml_main/              # 主实验
│   └── sc_nda_ml_ablation/          # 消融（KF 跟踪 / BPS 迁移）
├── explore/single-carrier-nda-ml/   # MVE 产出（保留，债务：薄包装，Formal 不复用）
├── feasibility_report.md            # Step 4a+4b 出参（已完成）
├── decision_log.md                  # 决策记录（已完成 D005/D-S5-01/D-4a-01/02/D-4b-01）
└── SPEC.md                          # ⬠ 待补 NDA-ML 段（当前是 QPSK 旧设定，需加 (8,8)-16APSK + B11 参数段）
```

**SPEC.md 补段**：Step 7 前补 SPEC §8（NDA-ML 正式段），含 (8,8)-16APSK + M₀=8 + CLW=500kHz + BLOCK=256 + pilot sp=4 + HD-FEC=3.8e-3，标 B11 行号来源。**不替换** SPEC §1-7（QPSK 旧设定保留作 VV/DPLL/KF 其他实验的参照系）。

---

## 8. 设计风险与债务

| 风险/债务 | 影响 | 缓解 |
|-----------|------|------|
| Formal 独立实现可能引入 bug | BER 数字与 MVE 不一致 | §4.5 MVE 一致性验证（同 seed 同参数 Formal vs MVE 必须一致）|
| 多 seed 增加运行时间 | 5 seed × 4 场景 × 7-8 SNR 点 = ~140-160 运行 | 子 agent 分批，每批一场景，预计每场景 < 5 min（MVE 单 seed 15.9s）|
| 跨块 KF 消融可能改变主结论 | FR-18 预判 cross-over 移动 | 作消融非主路径，单独报告；若主结论翻转回 feasibility_report 风险段重评 |
| BPS 迁移对比场景不对等 | BPS 主面 QAM，本项目 M-APSK | 标"场景不同"，不作主判据，仅作迁移参照 |
| SPEC.md QPSK 旧设定 vs NDA-ML 新参数 | 两套参数共存 | SPEC 补 §8 NDA-ML 段明确隔离，不删 §1-7 |

---

## 9. 用户确认（gw-experiment §sim [MUST]）

进入 Step 7 实现前，用户需确认：
1. [ ] 仿真器设计规格（模块清单完整性、参数合理性、验证标准充分性）
2. [ ] 5 seed 统计约定（[ASSUMPTION] 唯一项，会议级别是否够）
3. [ ] 消融范围（跨块 KF + BPS 迁移是否都做，还是只做主实验）
4. [ ] SPEC.md 补 §8 NDA-ML 段不替换 §1-7 QPSK 段（保留双套参数）

**FR-12 门控结论**：主路径全部"否"（架构与 MVE 一致）→ 通过，可进 Step 7。两消融不影响主路径 Go。
