# 阶段 0.4：公平对照框架设计（baseline / 双测度 / pilot overhead 摊薄 / 叙事定位 / 范围维度）

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback | 阶段: 0.4
> 日期: 2026-07-08
> 守: INVARIANT 13（饱和池 dB 难出区）+ INVARIANT 11（张力首验证，阶段 0.1 维度 B/C2 输入）+ FR-15（贡献目标 baseline 对照）+ FR-25（Go/Kill 标准分离）+ V2 三方对照
> 输入: 阶段 0.1 `_tension_validation_design.md` + 阶段 0.2 `_db_sourcing_audit.md` + 阶段 0.3 `_architecture_decision.md` + step4a 公平对照框架（`_step4a_detail_extract.md` §6）

## 0. 设计目标

把阶段 0.1 设计的 fair comparison 4 维度分解 + 阶段 0.3 前馈化架构，**制度化**为 sandbox/MVE 可直接执行的公平对照规则。明确回答 5 个问题：
1. baseline 是谁？
2. fair gain 测度是什么？
3. pilot overhead 怎么公平处理？
4. 叙事怎么定位（跟 NDA-ML 差异化）？
5. 范围维度（饱和池难出区）怎么应对？

## 1. Baseline 选定（FR-15 贡献目标 baseline）

### 1.1 三方对照矩阵（继承阶段 0.1 §3.1 + V2 三方对照）

| 方案 | blind 侧 | pilot 侧 | 角色 | 必须赢谁 |
|---|---|---|---|---|
| **A. 纯 blind freeze [79]** | fft_foe + 功率阈值 freeze | 无 | **祖师爷 baseline**（FR-15 目标）| — |
| **B. 纯 pilot-aided（step4a DA ML）** | 无 | da_ml_recovery 全程 | 已知在 fade 崩溃（step4a 反证）| — |
| **C. B2-Q2 双模切换（本候选）** | fft_foe/nda_ml（非 fade）| da_ml/psa_foe（fade）| 提出方法 | **必须赢 A**（FR-15）|

### 1.2 FR-15 贡献目标 baseline = 方案 A（纯 blind freeze [79]）

**理由**：
1. **[79] Matsuda 是 B2-Q2 的直接祖师爷**（sat.1553 L558/L582 引 [79] 为 fade 对策设计建议）—— V3 祖师爷警报要求 B2-Q2 必须跟 [79] 对照
2. **方案 B（step4a DA ML）已在 fade 崩溃**，不是合理 baseline（step4a 实证 BER 0.38 vs NDA 0.29）
3. **FR-15 要求"贡献声称要超越的对手"** = [79] Matsuda 静态功率阈值 freeze（传统未优化 baseline，符合 FR-25 Go 标准）

**方案 A 实现细节**（sandbox 要实现）：
- 信号流：rx → 功率检测 P → 阈值 γ_th → [P ≥ γ_th] 正常 fft_foe/nda_ml 跟踪 / [P < γ_th] **freeze（hold 上一估计值）**
- [79] freeze 机制：fade 期间不更新 FOE/CPE 估计，hold 进入 fade 前最后一个估计
- 恢复：fade 结束（P ≥ γ_th）后 blind 重收敛

### 1.3 辅助对照（非 FR-15 目标，用于归因）

- **oracle 上界**（真 h）：仅作物理上限参考，不作 Go/Kill 判据（FR-21 降级为参考，FR-25 Go/Kill 分离）
- **方案 B（纯 pilot-aided）**：确认 B2-Q2 比纯 pilot 好（双模切换的增量之一是非 fade 期不退化）

## 2. Fair Gain 双测度（阶段 0.1 §3.2 制度化）

### 2.1 测度 1：稳态 BER（跟 step4a 同测度）

**定义**：非 fade 期 + fade 期稳态（排除恢复瞬态）的 BER，@ HD-FEC 阈值 3.8e-3（跟 NDA-ML 跨候选可比）

**fair gain @ HD-FEC**：
- gain_A = (γ_tot,blind_freeze @ HD-FEC) − (γ_tot,B2Q2 @ HD-FEC)
- 正值 = B2-Q2 赢（达 HD-FEC 所需总能量更低）
- **PASS 标准**：gain_A ≥ 0 dB（B2-Q2 在稳态 BER 不应比纯 blind freeze 差）

**为什么是 ≥0 不是 ≥0.5dB**：
- 阶段 0.1 分析：B2-Q2 在非 fade 期用 blind（跟方案 A 同），fade 期用 pilot（可能跟 freeze 持平或稍好）
- 稳态 BER 维度 B2-Q2 的增量预期小（不是核心增量维度）
- 稳态 BER 测度的作用是**确认不退化**（非 fade 期切回 blind 不引入 BER 损失），不是主要 Go 判据

### 2.2 测度 2：动态恢复时间（B2-Q2 核心增量维度）

**定义**：fade 结束（P 从 < γ_th 回到 ≥ γ_th）后，BER 收敛回稳态所需的符号数 N_recover

**fair gain @ 动态恢复**：
- gain_recover = N_recover,blind_freeze − N_recover,B2Q2
- 正值 = B2-Q2 恢复更快（核心增量）
- **PASS 标准**：gain_recover ≥ ΔN_min（"显著改善"阈值，待 sandbox 实测方案 A 的 N_recover 后定）

**为什么动态恢复是核心增量**（阶段 0.1 维度 B 结论）：
- [79] freeze 在 fade 期 hold 估计 → 恢复时需 blind 重收敛（N_recover,freeze 较大）
- B2-Q2 在 fade 期用 pilot 持续跟踪 → 恢复时已有当前估计（N_recover,B2Q2 较小）
- 这个差异 step4a 没测（step4a 是稳态 BER 对比，无 freeze/恢复动态）
- **这是 B2-Q2 命题最可能站住的维度**

**N_recover 测量方法**（sandbox 实现）：
- 滑窗 BER：fade 结束后每 K 符号算一次 BER，画 BER vs 距 fade 结束符号数曲线
- N_recover = BER 回到稳态 BER ±10% 所需符号数

### 2.3 测度 3（辅助）：工作区扩展（饱和池难出区对策）

**定义**：strong 湍流下纯 blind freeze HD-FEC 不可达（物理上限，D005 step4a 已证），B2-Q2 是否可达 HD-FEC

**PASS 标准**：B2-Q2 在 strong 湍流某些 OSNR 点可达 HD-FEC（3.8e-3）而方案 A 不可达 → 范围维度增量

**这是 INVARIANT 13 饱和池难出区对策**：dB 难出时靠范围/鲁棒性维度够格（D005 会议门槛放宽允许）。

## 3. Pilot Overhead 摊薄（阶段 0.1 §3.3 制度化）

### 3.1 step4a 框架（继承，DA 全帧 25% overhead）

step4a 公平对照（`_step4a_detail_extract.md` §6）：
- DA ML：全帧 25% pilot overhead = 1.249 dB 总能量代价（PILOT_OVERHEAD_DB = 10·log10(4/3)）
- NDA-ML：0% overhead，纯数据
- fair gain = (DA γ_d + 1.249) − NDA γ_d @ HD-FEC

### 3.2 B2-Q2 摊薄机制（pilot 只在 fade 期发）

**B2-Q2 pilot overhead 不是全帧 25%，而是 fade 占空比 × 25%**：
- B2-Q2 只在 fade 期（P < γ_th）发 pilot，非 fade 期全数据
- 实际 overhead = ρ_fade × 25%，其中 ρ_fade = P(P < γ_th) = fade 占空比

**ρ_fade 的物理决定**：
- ρ_fade 由 GG 块衰落统计 + 阈值 γ_th 决定
- weak（α4/β3）：fade 深度浅但频次高，ρ_fade 适中
- strong（α1.5/β0.8）：fade 深度深，ρ_fade 较高
- 阈值 γ_th 越高 → ρ_fade 越大（更多块被判为 fade）

**B2-Q2 总能量代价**：
- B2Q2_overhead_dB = 10·log10(1 + ρ_fade × 0.25/(1−0.25))（推导：pilot 占 fade 块 25%，非 fade 块 0%）
- 简化：B2Q2_overhead_dB ≈ ρ_fade × 1.249 dB（小 overhead 近似）

**示例**（待 sandbox 实测 ρ_fade）：
- 若 ρ_fade = 10%（weak 典型）→ B2Q2_overhead ≈ 0.125 dB（vs step4a DA 的 1.249 dB）
- 若 ρ_fade = 30%（strong 典型）→ B2Q2_overhead ≈ 0.375 dB

### 3.3 公平对照实现（sandbox 代码层面）

**三方总能量对比**（@ 相同信息率）：
| 方案 | 总能量 SNR γ_tot |
|---|---|
| A. 纯 blind freeze | γ_d（0% overhead）|
| B. 纯 pilot-aided | γ_d + 1.249 dB（全帧 25%）|
| C. B2-Q2 双模切换 | γ_d + ρ_fade × 1.249 dB（摊薄）|

**fair gain 计算**（@ 测度 1 稳态 BER @ HD-FEC）：
- gain_A = (γ_d,A @ HD-FEC) − (γ_d,C + ρ_fade × 1.249 @ HD-FEC)

**注意事项**：
- ρ_fade 不是定值，sandbox 要实测（每 OSNR 点 × 每湍流档的 ρ_fade 不同）
- γ_th 敏感性扫：γ_th ∈ [γ̄−3σ, γ̄−1σ]，看 ρ_fade 和 fair gain 对 γ_th 的敏感性

## 4. 叙事定位（B2-Q2 vs NDA-ML 差异化）

### 4.1 撞车风险（INVARIANT 13 + S001 B2 特殊风险表）

B2-Q2 和 NDA-ML 都是"fade 鲁棒性问题的解法"：
- NDA-ML：去 pilot，盲估，全帧积分 dilute fade（形态 C 鲁棒性）
- B2-Q2：加 pilot fallback，双模切换，动态恢复（fade 恢复时间）

**如果不差异化，论文叙事会撞**：两者都是"解决 fade 鲁棒性"，审稿人会问"为什么不直接用 NDA-ML"。

### 4.2 差异化论据（基于阶段 0.1/0.2 发现）

**维度 1：测度差异**
- NDA-ML 增量维度 = 稳态 BER fair gain @ HD-FEC（+1.2~1.9 dB，D005 step4a 实证）
- B2-Q2 增量维度 = 动态恢复时间（N_recover 缩短）+ 范围扩展（strong 可达 HD-FEC）
- **两者增量在不同维度，不冲突**

**维度 2：机制差异**
- NDA-ML = 全帧盲估（无 pilot，无切换）
- B2-Q2 = 双模切换（有 pilot fallback，前馈门控）
- **NDA-ML 是"纯盲路线"，B2-Q2 是"盲+pilot 组合路线"，机制正交**

**维度 3：适用场景差异（关键差异化）**
- NDA-ML 在 strong 湍流 HD-FEC 不可达（物理上限，D005 step4a）→ NDA-ML 在 strong 不够格
- B2-Q2 在 strong 湍流可能可达 HD-FEC（pilot fallback 在 deep fade 提供跟踪）→ B2-Q2 填补 NDA-ML 在 strong 的空白
- **叙事定位：B2-Q2 是 NDA-ML 在 strong 湍流的补充，不是替代**

### 4.3 动机叙事锚（sat.1553 [58] open direction）

**阶段 0.2 发现**（`_db_sourcing_audit.md` §4）：
> sat.1553 L440："pilot-based phase estimation could be combined with a second blind phase estimator to further improve performance [58]"

**B2-Q2 动机叙事**（用 sat.1553 自报 open direction 锚）：
1. sat.1553 综述作者提出 "pilot + 盲组合" 是 open direction（证据链最强档，切法地图 §A.4 ~5%）
2. NDA-ML（纯盲）已证在 weak/moderate 有效（D005 step4a），但 strong 物理不可达
3. B2-Q2 双模切换正是 sat.1553 [58] open direction 的具体化（pilot + 盲组合 + fade 门控）
4. B2-Q2 填补 NDA-ML 在 strong 湍流的空白

**这个叙事避免撞车**：B2-Q2 不是"又一个 fade 鲁棒性方法"，是"sat.1553 自报的 pilot+盲组合 open direction 在 strong 湍流场景的具体化"。

## 5. 范围维度对策（INVARIANT 13 饱和池 dB 难出区）

### 5.1 饱和池警示（`_cut-map-final-b1-b12.md` §C + INVARIANT 13）

切法地图 §C 警示：饱和池（B1-B5）是 dB 最难出区（Paillier 安全区 5 篇落盘 0 篇出 dB）。B2 饱和池 §A 小池（sat.1553 + Matsuda + Paillier 3 篇锚）。

**B2-Q2 的 dB 形态**（`_cut-map-final-b1-b12.md:51`）："无 dB 仅结构性"——sat.1553 自己未对 [79] 冻结机制做独立仿真复现，仅引为设计建议。

### 5.2 B2-Q2 够格策略（多维增量）

**D005 会议门槛放宽**：纯仿真 + 鲁棒性 dB / 范围 / 绝对指标 / 同族 dB 都算够格。

**B2-Q2 多维增量设计**（任一维度够格即 Go）：

| 维度 | 增量形态 | PASS 标准 | 难度 |
|---|---|---|---|
| **动态恢复时间** | gain_recover ≥ ΔN_min | sandbox 实测方案 A N_recover 后定 | 中（核心维度）|
| **范围扩展（strong）**| B2-Q2 在 strong 可达 HD-FEC 而方案 A 不可达 | strong 某些 OSNR 点 B2-Q2 < 3.8e-3 | 中（物理上限对策）|
| **稳态 BER fair gain** | gain_A @ HD-FEC | ≥0 dB（不退化）+ 最好 ≥0.5 dB | 高（饱和池难出）|
| **鲁棒性维度** | B2-Q2 对 γ_th / 调制阶数 / 符号率的鲁棒性 | 定性论证 + sandbox 扫参稳定性 | 低（辅助）|

**预期够格路径**：动态恢复时间 + 范围扩展（strong）双维度够格，稳态 BER 不退化即可。**不押注稳态 BER fair gain ≥0.5dB**（饱和池警示）。

### 5.3 FR-21 oracle 上界（降级为参考，不作 Kill 门）

- strong 湍流 oracle 也不可达 HD-FEC（D005 step4a 已证）→ B2-Q2 在 strong 不可达不算 fail
- FR-21 oracle 上界只作物理上限参考，不作 Kill 判据（FR-25 Go/Kill 分离，INVARIANT 2 D005 务实路线）

## 6. 判定门控（sandbox 阶段 1 → Go/Kill）

### 6.1 Go 标准（FR-25，赢传统 baseline）

sandbox 三方对照后，**任一满足即 Go**（D005 多维够格）：
1. B2-Q2 动态恢复时间显著优于纯 blind freeze（gain_recover ≥ ΔN_min）
2. B2-Q2 在 strong 湍流某些 OSNR 点可达 HD-FEC 而方案 A 不可达（范围扩展）
3. B2-Q2 稳态 BER fair gain @ HD-FEC ≥ 0.5 dB（饱和池难出，bonus）

### 6.2 Kill 标准（阶段 0.1 维度 C2 红线 + FR-25）

sandbox 三方对照后，**任一满足即 Kill**：
1. **维度 C2 红线**：所有 pilot-aided 变体（da_ml/psa_foe/power-boosted pilot）在 fade 期间都输 NDA-ML（pilot-aided 路线根本弱）→ 核心命题崩塌
2. B2-Q2 动态恢复时间 ≈ 纯 blind freeze（pilot fallback 没帮助恢复）→ 核心增量不成立
3. B2-Q2 稳态 BER 反而比纯 blind freeze 差（非 fade 期切回 blind 引入损失）→ 架构设计错

### 6.3 Kill 是合法选项（INVARIANT 11）

如果 sandbox 验证后核心命题崩塌（维度 C2 成立或动态恢复无差），B2-Q2 转 Kill 是合法选项，不是失败。阶段 0.1-0.6 的规约投入（张力验证设计 + dB 溯源 + 架构定性 + 公平对照）即使 Kill 也有价值（为 NDA-ML/B7 提供交叉验证 + 沉淀 pilot-aided vs blind 的对比方法论）。

## 7. 阶段 0.4 结论

**公平对照框架制度化完成**：
- **baseline** = 纯 blind freeze [79]（FR-15 贡献目标 + V3 祖师爷）
- **双测度** = 稳态 BER @ HD-FEC（不退化）+ 动态恢复时间（核心增量）+ 范围扩展（strong，辅助）
- **pilot overhead 摊薄** = ρ_fade × 1.249 dB（vs step4a 全帧 1.249 dB），sandbox 实测 ρ_fade
- **叙事定位** = sat.1553 [58] pilot+盲组合 open direction 具体化，填补 NDA-ML 在 strong 湍流空白（不撞车）
- **范围维度对策** = 多维增量（动态恢复 + 范围扩展 + 鲁棒性），不押注稳态 BER dB（饱和池警示）

**判定门控明确**：Go = 任一多维够格；Kill = 维度 C2 红线 或 动态恢复无差 或 稳态 BER 退化。

**进阶段 0.5**：参数真相源前置（fade σp² / GG α/β / OSNR / pilot 配置全标 source + 读原文数值 + ref [58] 查证）。
