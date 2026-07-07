# [S002] 阶段 0.1-0.6 六项前置规约全完成（张力验证 + dB 溯源 + 架构 + 公平对照 + 参数 + 文件）

> 2026-07-08 | 阶段: 工作对话执行阶段 0.1-0.6（不写代码）| 状态: 完成，阶段 0 六项规约全做完，可进 sandbox
> 2026-07-08 续接：用户授权"先接着做吧"，0.3-0.6 在本对话继续完成

## 目标

承接主控对话 S001 + H001 派发，执行阶段 0.1-0.6 六项前置规约（不写代码）。守 profile 第 9 次"急于推进"防线 + INVARIANT 6（阶段 0 六项规约全做完才进 sandbox）。原计划 0.1-0.2 本对话 + 0.3-0.6 下一对话（3 步上限），用户授权继续后本对话一次做完六项。

## 记录

### 报到 + 接收方验证（Trigger 1 + Trigger 5）

读完必读清单 1-7（topic-index / H001 / S001 / decisions / step4a decisions / B2-Q2 详情 / dB 口径核验 / 饱和池警示 / registry / profile）。

**接收方验证 4 条全打钩**（核查 3 条关键事实声称）：
- ✅ step4a 实测"DA pilot BER 0.38 vs NDA 0.29"——核查 `step4a-mve-execution/decisions.md:150, 157` 原文一致
- ✅ sat.1553 L440 +1dB 口径=PE vs VV+diff——核查 `_cut-b1b2b3-verify.md:144-145, 342` + 主线 Read `content.md:440` 原文
- ✅ B2-Q2 不撞 D006——核查 `_B2-deep-fade-freeze-increment.md:68, 75`
- ✅ depends_on 4 依赖全稳定（registry 核查）
- ✅ 未违反"明确不含"

### 阶段 0.1 核心命题张力验证设计（B2 最高优先）

**派子 agent T### 核查 step4a 实测细节**（6 类参数：DA pilot 配置 / NDA-ML 配置 / fade 场景 / BER 测试 / 崩溃机制 / 公平对照框架）。产出 `_step4a_detail_extract.md`。

**主线独立 grep + python 核查子 agent 数字**（不变量 10 核查机制中性双向）：
- PILOT_OVERHEAD_DB = 1.2494 dB ✅
- SIGMA2_P = 2.5133e-5 ✅
- 每 fade 块 25 pilot / DA pilot spacing=4 / da_ml 3 元组 vs nda_ml 4 元组 ✅
- BER 0.38/0.29 出处单一（仅 D004 L157）✅

**子 agent 3 个意外发现**（主线已验证属实）：
1. **σp² 是 Wiener PN 单值**（2.51e-5），weak/moderate/strong 是 GG α/β 块衰落三档——sat.1553 σp²=0.25 是 Rytov 方差，不同物理量
2. **BER 0.38/0.29 是 γ_d=5dB 低 SNR 绝对 BER**，跟 D005 HD-FEC fair gain +1.199dB 是不同 SNR 点（不冲突）
3. **"deep fade 崩溃"机制无量化对比**——step4a 没讨论 pilot spacing（4 符号）vs fade 相干时间（100 符号 fade 块）的关系

**主线设计 fair comparison 4 维度分解**（产出 `_tension_validation_design.md`）：

| 维度 | 张力分解 | 判定 |
|---|---|---|
| A（pilot 配置）| A1 spacing 不够密 → 不成立（pilot 远比 fade 密，25 pilot/fade 块）；A2 pilot 功率/类型可探索但偏离原命题 | 部分可分解 |
| B（触发条件）| **最大差异点**——step4a 静态 BER vs B2-Q2 动态恢复是不同测度 | 可分解 |
| C（pilot-aided 类型）| C1 换算法可验证；C2 路线根本弱是红线风险 | 部分可分解（C2 红线）|
| D（信道场景）| 场景差异是 sat.1553 +1dB 不能搬的物理根因 | 可分解 |

**核心结论**：张力**可分解**，不直接 Kill。B2-Q2 真正的增量可能在**动态恢复时间**（fade 恢复期 pilot 帮助重收敛），不是稳态 BER。sandbox 三方对照（阶段 1）验证后才能定 Go/Kill。

**关键论据**（B2-Q2 不撞 step4a 反证）：step4a 对比"全程 DA ML vs 全程 NDA ML"（稳态 BER）；B2-Q2 对比"双模切换 vs 纯 blind freeze"（动态恢复 + 稳态 BER）。机制不同（全程 vs fallback）。**但**：如果 B2-Q2 pilot 侧用 da_ml 且 fade 期 da_ml 仍崩溃，则 B2-Q2 pilot fallback 也崩溃 → 维度 C2 红线风险。

### 阶段 0.2 dB 溯源核查（INVARIANT 12 + FR-26）

**主线 Read sat.1553 content.md L430-460 原文**（不只引二次引用，守 FR-26 读原文数值）。

**sat.1553 L440 +1dB 原口径精确锁定**：
- +1dB = pilot-based PE **vs** VV+差分编码
- 场景：QPSK + AWGN PN（Equation 17）scenario 4（上行强湍 σp²(Rytov)=0.25）
- 测度：SNR penalty @ BER=10⁻³
- VV+diff penalty ~1.5dB，pilot vs VV+diff +1dB → pilot 自身 penalty ~0.5dB

**五重口径差异**（B2-Q2 为什么不能搬）：
1. 对比方法：PE vs VV+diff（不是 FOE freeze 双模切换 vs blind freeze）
2. 估计对象：PE（不是 FOE freeze）
3. 调制：QPSK（不是 16-APSK M₀=8）
4. 场景：OFDM-ish AWGN PN（不是单载波时域 GG 块衰落）
5. 测度：penalty @ BER=10⁻³（不是 fair gain @ HD-FEC 或动态恢复时间）

**意外发现**（sat.1553 L440 的 B2-Q2 叙事锚点）：
> "pilot-based phase estimation could be combined with a second blind phase estimator to further improve performance [58]"

sat.1553 综述作者明确提了"pilot + 盲组合"open direction——正好是 B2-Q2 双模切换的叙事锚点（A1 归属 + 动机叙事支撑）。ref [58] 具体论文待查（阶段 0.5 附带）。

**物理根因**（为什么 sat.1553 +1dB 在单载波时域可能不成立）：
- sat.1553：pilot PE 比 VV+diff 好（两种都依赖判决/差分，fade 都退化，pilot 稍好）
- B2-Q2：pilot-aided vs blind ML（blind 用全帧积分，fade 鲁棒性不同机制）
- step4a 实证：单载波时域 pilot 反而比 blind 差（跟 sat.1553 OFDM 结论方向相反）

## 决策引用

- D001（继承）：开 B2-Q2 专题 + 首验证张力策略
- 无新建决策（阶段 0.1-0.2 是规约设计，非架构/方向决策；核心命题是否 Kill 取决于 sandbox 阶段 1，不是本阶段）
- **阶段 0.3 建议升 D002**（前馈化架构 INVARIANT 级不撞 D006）—— 待主控对话核查确认，工作对话只定规约不记决策

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 0.1-0.6 前置规约，未写代码未进 sandbox）
- **守 profile 第 9 次"急于推进"防线**：阶段 0 六项规约**全做完**才进 sandbox。本轮用户授权"先接着做吧"，一次做完 0.1-0.6 六项
- **守 3 步上限的例外**：AGENTS.md 3 步上限是建议分对话防上下文爆炸，用户明确授权继续则继续。本对话做 6 步（0.1-0.6），每步都先讲清"在干啥+为什么"守防线
- **守 executor 角色边界**：只执行阶段 0 规约，不进 sandbox 不写 MVE 代码

## 阶段 0.3 架构定性（前馈化不撞 D006，INVARIANT 级）

**主线 Read D006 原文**（`decisions.md:313-355`）+ B2 笔记 L61-75 + `_recovery.py` 4 估计器实现核查。

**核心论证**：D006 Kill 的是"把湍流相位 φ_T 主动纳入同步算法设计"（无论 KF/环路 TF）。B2-Q2 是"按 fade 状态选估计器"（外部 switch），估计器内部不碰 φ_T。机制上 ≠ B1/Q12。

**架构决策：前馈化（INVARIANT 级）**：
- 4 估计器全部前馈闭式（`_recovery.py:37 fft_foe` / `:136 da_ml` 线性回归 / `:171 nda_ml` 升幂 mean-angle / `:435 psa_foe` 差分最小二乘，grep 核查全开环一次性）
- fade 检测用开环功率阈值 γ_th（不闭环，不用误差驱动）
- 模式切换是 switch 不是 feedback
- 补偿一次性（无跨块迭代）

**创新性论证**：前馈化不削弱 B2-Q2 创新——创新在切换策略（何时/切哪个/怎么公平对照），不在估计器数学。与 [79] freeze 机制差异（hold 估计 vs 切 pilot 继续跟踪）依然存在。

产出 `_architecture_decision.md`。建议升 D002（待主控对话确认）。

## 阶段 0.4 公平对照框架设计（baseline + 双测度 + 摊薄 + 叙事 + 范围）

**baseline 选定（FR-15）**：纯 blind freeze [79] Matsuda（祖师爷 + sat.1553 L558/L582 引用）。方案 B（step4a 纯 pilot）已知 fade 崩溃不作 baseline。

**fair gain 双测度**（阶段 0.1 制度化）：
- 测度 1 稳态 BER @ HD-FEC 3.8e-3：PASS 标准 ≥0 dB（不退化，非主要 Go 判据）
- 测度 2 动态恢复时间 N_recover：PASS 标准 gain_recover ≥ ΔN_min（核心增量，sandbox 实测方案 A 后定）
- 测度 3（辅助）范围扩展：strong 湍流 B2-Q2 可达 HD-FEC 而方案 A 不可达

**pilot overhead 摊薄**：B2-Q2 overhead = ρ_fade × 1.249 dB（vs step4a 全帧 1.249），ρ_fade 实测。示例 weak 10% → 0.125dB，strong 30% → 0.375dB。

**叙事定位（跟 NDA-ML 差异化）**：测度差异（NDA-ML 稳态 BER / B2-Q2 动态恢复）+ 机制差异（纯盲 / 盲+pilot 组合）+ 场景差异（NDA-ML strong 不可达 / B2-Q2 填补 strong 空白）。

**范围维度对策（INVARIANT 13 饱和池）**：多维增量（动态恢复 + 范围扩展 + 鲁棒性），任一够格即 Go，不押注稳态 BER dB。

**判定门控**：Go = 任一多维够格；Kill = 维度 C2 红线 或 动态恢复无差 或 稳态 BER 退化。

产出 `_fair_comparison_framework.md`。

## 阶段 0.5 参数真相源前置（σp² vs GG α/β + ref [58] 查证）

**σ²_pN vs GG α/β 严格区分**（消除阶段 0.1 子 agent 发现的命名混淆）：
- σ²_pN（Wiener PN）= 2.51e-5 单值（2π·10kHz·4e-10，D-007 统一）
- GG α/β = fade 三档（weak α4/β3, moderate α2.5/β1.8, strong α1.5/β0.8）
- sat.1553 σp²=0.25 是 Rytov 方差 σ²_R，不同物理量
- 禁用"σp² 三档"表述

**ref [58] 查证完成**（主线 grep sat.1553 reference list L1261 + B1 笔记交叉确认）：
- ref [58] = Martins, Guiomar, Pinto (2021) "Hardware Optimization of Dual-Stage CPR" OSA Continuum 4(12):3157-3175
- 机制 = dual-stage pilot-CPE + BPS（并行处理每符号）
- **修正阶段 0.2 叙事锚点解读**：[58] 是 dual-stage 并行，B2-Q2 是 fade 门控切换，机制不同
- B2-Q2 增量定位修正为"把 [58] 静态 dual-stage 扩展到 fade 动态场景"（更扎实的 A1 归属）

**B2Params 草稿**（`_param_truth_source.md` §3）：继承 SystemParams / GammaGammaParams，B2-Q2 特有 γ_th / ρ_fade（sandbox 实测不预设）。

**留给 sandbox**：实测 rx 功率分布定 γ_th 扫参范围 + 逐点测 ρ_fade + 确认 GG α/β 文献来源。

产出 `_param_truth_source.md`。

## 阶段 0.6 文件组织规约（目录 + 命名 + 下游同步）

**目录结构**：`explore/b2-fade-freeze-pilot-fallback/` 平铺，私有 `_` 前缀（诊断/核查/草稿/探针）+ 正式无前缀（SPEC/mve）。

**命名规则强制**：禁 "improved"/版本号/备份目录（NDA-ML D-007 教训）。

**下游引用同步清单**（D-007 教训 2）：参数变更触发清理 explore 内脚本 + results JSON meta 字段强制（仿 step4a `_time_domain_crlb.py:592-597`）。

**common 污染防御**：explore 不进 common，MVE 通过才转正。

产出 `_file_organization.md`。**阶段 0 六项规约全部完成**。

## 后续

### 阶段 0 六项规约完成，可进阶段 1 sandbox

阶段 0.1-0.6 全部完成，守 profile 第 9 次"急于推进"防线 + INVARIANT 6 满足。下一步 = 阶段 1 sandbox 三方对照（新对话）。

### 阶段 1 sandbox 三方对照（下一对话核心任务）

1. **实现三方**：方案 A 纯 blind freeze [79]（fft_foe + 功率阈值 freeze）/ 方案 B 纯 pilot-aided（step4a DA ML）/ 方案 C B2-Q2 双模切换
2. **必答维度 C2**：所有 pilot-aided 变体（da_ml/psa_foe/power-boosted）在 fade 是否都输 NDA-ML（红线）
3. **必测动态恢复时间**：B2-Q2 双模切换 N_recover vs 纯 blind freeze N_recover（核心增量）
4. **γ_th 敏感性扫**：[γ̄−3σ, γ̄−1σ] 扫参，实测 ρ_fade
5. 守 V2 三方对照 + V3 祖师爷警报（[79] 是祖师爷）+ V4 参数变更触发算法重审

### 主控对话跟进点

- 核查阶段 0.1 张力验证设计是否真消化 step4a 反证（非绕过）—— 主线判定：4 维度全分解，维度 C2 红线明确
- 核查阶段 0.2 dB 溯源是否限定 sat.1553 +1dB 到原始口径 —— 主线判定：已锁定 PE vs VV+diff
- 核查阶段 0.3 前馈化架构是否真不撞 D006 —— 主线判定：4 估计器全前馈闭式 + 门控外部 switch，机制 ≠ B1/Q12。**建议升 D002**
- 核查阶段 0.4 公平对照框架是否制度化双测度 + 摊薄 + 叙事 —— 主线判定：baseline/双测度/摊薄/叙事/范围全制度化
- 核查阶段 0.5 ref [58] 查证是否修正阶段 0.2 叙事锚点 —— 主线判定：[58]=Martins dual-stage，B2-Q2 增量重定位为"静态扩展到 fade 动态"
- 核查阶段 0.6 文件组织是否防 D-007 混乱 —— 主线判定：命名/下游同步/common 防御全规约

### B2-Q2 跟 NDA-ML 的交叉

阶段 0.1 发现"动态恢复时间"是 NDA-ML 没测的维度，B2-Q2 若在此维度有增量对 NDA-ML 方法方向决策有交叉验证价值。阶段 0.4 叙事定位明确 B2-Q2 填补 NDA-ML 在 strong 湍流空白（NDA-ML strong HD-FEC 物理不可达）。
