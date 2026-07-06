# 方向可行性报告 — 单载波时域 NDA-ML 改进（形态 A+C）

> 项目: projects/simulation | 阶段: GW Step 4a + 4b（方向根基 + 初步可行性 + 仿真条件/资源风险）| 日期: 2026-07-06
> 框架: gw-feasibility.md §4a（A0/A'/A/B/D 维度）+ §4b（C/E 维度，2026-07-06 补完）
> 决策: **Go**（4a: D005 MVE PASS + 4b: C/E 无致命）| 用户确认: ⬜（待）

## 研究方向

**单载波时域 NDA-ML（Non-data-aided Maximum Likelihood）载波相位估计改进**——在星地激光通信 (8,8)-16APSK + Wiener 相位噪声 + Gamma-Gamma 湍流块衰落信道下，用升 M₀=8 次幂盲去调制 + 单正弦 ML 估 CPE 替代 DA ML（pilot-aided，pilot spacing=4，25% pilot overhead），在公平总功率对照下取得频谱效率（形态 A，去 pilot overhead）+ 湍流鲁棒性（形态 C，NDA 全帧积分 vs DA pilot 受 fade）双增量。

**Q# 对应**：载波同步 v2 精读沉淀 B11-Q1（literature_notes.md 载波同步 v2 总表行 675，"NDA-ML 联合 STO+CPE，够格 +2dB 下沿"）的场景迁移+架构改进版——B11 是 OFDM 频域 ML（D002 重定位为理论参考），本方向落在单载波时域（贴星地主流，D002 论证）。

## A0. 问题-方法适配性预检（§0 前置 + §1-§6）

### §0 前置门控

1. **候选对应 Q#？** ✅ 是。对应载波同步 v2 总表 **B11-Q1**（literature_notes.md 行 675）。本方向是 B11-Q1 的场景迁移（OFDM 频域→单载波时域）+ 架构改进（频域 R(k)^M₀ → 时域 r(n)^M₀ + per-block 盲 h）。
2. **该 Q# 四判据全过？** ✅ 是。B11-Q1 在总表标"够格（+2dB 下沿）"，四判据全过（literature_notes.md 载波同步 v2 总表 + S006 综合分析行 519）。

### §1 性能间隙 [FR-02]

**[实证]** MVE 实测公平对照 fair gain @ HD-FEC（BER=3.8e-3，DA 含 1.249dB pilot overhead 总能量代价，来源 `_mve_results.json` gain_analysis）：
- AWGN **+0.704 dB**（形态 A）
- weak (α4/β3) **+1.199 dB**
- moderate (α2.5/β1.8) **+1.922 dB**
- strong (α1.5/β0.8) HD-FEC 物理不可达，工作区(≥15dB) NDA 全赢 DA（per-point fair gain +1.19~+2.62dB）

差距 ≥0.5dB（D005 Go 门）→ 有空间，继续。

### §2 问题结构适配

✅ 满足多项：
- 状态空间大（连续相位 θ(k) per-symbol Wiener 演化，N=102400 符号/点）
- 环境动态复杂（GG 块衰落 h 时变 + Doppler CFO + Wiener PN 三重随机）
- 需跨场景泛化（不同湍流等级 weak/moderate/strong 共用同一估计器）

### §3 跨域成功先例

✅ ≥2 篇成功先例：
- B11（IEEE PTL 2025）：OFDM 频域 NDA-ML 升 M₀ 次幂，CO-OFDM (8,8)-16APSK +2dB vs DA ML（papers/_read_notes/_B11-nda-ml-sto-cpe-increment.md）
- Wang[13]（B11 引用）：单正弦 ML 闭式频率+相位估计经典理论锚
- 同类升幂 NDA 思路在 fiber CO-OFDM 相位噪声 ML 系列（Kam 团队）多篇验证

### §4 MDP 非平凡性

N/A（本方向是**信号处理估计算法**，不是 RL/MDP）。A0 §4 针对 ML 决策类方法，估计类方法跳过此项（ gw-feasibility §A0 §4 隐含——"写下 S/A/R/P"对估计器无意义）。

### §5 负面证据搜索

载波同步子地带 NDA-ML 升幂方法**无失败报告**。B11 自报 +2dB（条件性：仅 (8,8)-16APSK + CLW 容限付 1dB cost），未被后续论文反驳（cited-by 池仅 1 篇 HSR 地对车背景引用，见 D002）。

### §6 先验覆盖检查 [FR-01]

DA ML（pilot sp=4）是 pilot-aided 载波相位估计的**近最优**实现（pilot 充分时），覆盖"有 pilot 可用"场景 ≥90% 最优。但 **NDA-ML 的竞争维度不是"比 DA ML 更准"而是"无 pilot 下达到近 DA ML 性能"**（频谱效率维度）+ "deep fade 鲁棒性"（形态 C 维度）——这两个维度 DA ML 不覆盖。主指标（BER@HD-FEC 公平对照）未被简单策略覆盖，次指标（频谱效率 + 鲁棒性）DA ML 不竞争。

**A0 结论**：6 项无致命信号，进 A'。

## A'. 竞争维度分解 [FR-05]

| 维度 | 先验覆盖度（DA ML）| ML 改善空间 | NDA-ML 方法增量 |
|---|---|---|---|
| **频谱效率（形态 A）**| 低（DA 需 25% pilot overhead，1.249dB 总能量代价）| ≥5%（MVE 实测 +0.704dB @ AWGN）| 无 pilot 保留全频谱效率 |
| **湍流鲁棒性（形态 C）**| 低（DA pilot 在 deep fade 块崩溃，BER floor）| ≥5%（MVE 实测 +1.19~+2.62dB @ strong 工作区）| NDA 全帧积分对单点 fade 鲁棒 |
| 绝对 BER 精度 | 高（pilot sp=4 近最优）| <5%（NDA-vs-oracle gap 0.38-2.58dB）| NDA 略逊 oracle 但公平对照赢 DA |

**创新声称建立在"频谱效率 + 鲁棒性"两个先验覆盖度低 + ML 改善空间 ≥5% 的维度上**，不是建在 DA ML 最强的"绝对 BER 精度"维度。✅ 满足 A'。

## A. 结构优势论证

**核心方法（单载波时域 NDA-ML）相比最简 baseline（DA ML pilot sp=4）的结构性优势**：

1. **频谱效率维度（形态 A）**：DA ML 需多发 1/spacing=25% pilot 符号，总能量代价 10·log10(4/3)=1.249dB（per-symbol avg power equal 假设）。NDA-ML 用全部 N 个信息符号盲估相位，无 pilot overhead。**信息论支撑**：CRB_NDA(φ)/CRB_DA(φ) ≈ N_p/N = 1/4（来源 `_crlb_results.json` meta.analytic_crlb_conclusion.ratio，M₀² 严格相消——升幂噪声方差放大 = 相位参数增益 (d arg(z)/dφ)²=M₀²）→ CRLB 层 NDA-ML 理论下界优于 DA ML（用全 N 符号 vs 仅 N_p=N/4 pilot）。

2. **鲁棒性维度（形态 C）**：DA pilot 估计 ĥ=mean(|r(p)/s(p)|²) 仅用 block 内 N_p=64 个 pilot 位置（block=256），在 deep fade 块（h<<1）pilot 统计涨落大 → ĥ 严重偏差 → BER 崩溃。NDA 盲 ĥ=mean(|rx|²)−1/(2γ) 用全 N=256 符号，积分长度 4× → 对单点 fade 鲁棒。**MVE 实测**：strong 湍流工作区(≥15dB) NDA 全 5/5 点赢 DA（per-point fair gain +1.19~+2.62dB，来源 `_mve_results.json` gain_analysis.strong.per_point_fair_gain）。

3. **结构性优势的具体条件**（不是"特征不同所以需要复杂模型"）：在 pilot overhead 是真实能量代价的场景（总功率受限，如星地激光下行 EIRP 受限）+ 湍流致 deep fade 频发的场景（GG 块衰落），DA ML 的 pilot 局部估计在 fade 块崩溃，NDA-ML 全帧积分吸收 fade。**简单方法（DA ML）导致信息损失**：pilot 局部估计丢失了信息符号位置的信道状态信息。

[FR-03] 对比对象是 DA ML 的增强版本（pilot sp=4 密集，pilot-aided 近最优），不是裸 DA ML。[FR-08] 本方向是经典参数估计（ML），不是 ML/DL 学习范式，无范式对齐要求。

## B. 新颖性-可行性解耦

- **新颖性论据**：单载波时域 NDA-ML 升 M₀ 次幂在星地湍流 (8,8)-16APSK 场景**零竞争**（D002 调研 `_star_ground_link_survey.md`：星地 FSO 主流是单载波 QPSK/8PSK/M-APSK + DVB-S2/S2X，OFDM 仅研究探索；B11 是 OFDM 频域 ML 与单载波时域架构性不等价，被引仅 1 次 HSR 背景引用）。
- **可行性论据**：MVE 实测公平对照 fair gain @ HD-FEC 全 ≥0.5dB（AWGN +0.704 / weak +1.199 / moderate +1.922），TL-20 预期 5 项全 PASS 0 DEVIATION，NDA-vs-oracle gap 全 <3dB（升幂实现正确）。**做了会更好有实证支撑**。
- **空白原因分析**：技术限制刚解除 + 场景迁移。B11 团队主体是 fiber CO-OFDM 相位噪声 ML 系列，未迁移到星地单载波；星地 FSO 主流 DSP 流水线（DVB-S2/S2X + DLR sat.1553）无 NDA-ML 升幂方案。**前人没做不是因为不好，是因为跨子领域迁移**（fiber OFDM → 星地单载波）。

### 空白零假设检查 [MUST]

列出 ≥3 个空白存在的结构性/技术性原因，逐一反驳：
1. **"单载波时域升 M₀ 次幂噪声放大无 DFT 处理增益抵消，性能不行"** → 反驳：CRLB 层 M₀² 严格相消（`_crlb_results.json` meta M0_cancellation_note），MVE 实测 NDA-vs-oracle gap 仅 0.38-2.58dB（<3dB），升幂噪声可控。
2. **"单载波时域逐样本 Wiener θ(n) 方差放大 M₀² 倍，CPE 跟踪失败"** → 反驳：per-block（256 符号）CPE 估计假设块内相位恒定（block 准则），块内 Wiener 累积方差 σ²_θ·T_block 可控（CLW=500kHz 对应块内相位变化 <0.1rad）。MVE 用 per-block blind h + 两阶段 fft_foe+nda_ml 修复 BER floor（`_ber_floor_diagnostic.json`）。
3. **"deep fade 块盲 ĥ 估计噪声大，NDA 反不如 DA pilot"** → 反驳：MVE 实测 strong 工作区 NDA 全赢 DA（per-point +1.19~+2.62dB）。盲 ĥ=mean(|rx|²)−1/(2γ) 用全 N=256 符号 vs DA pilot 仅 N_p=64，积分长度 4× 抵消盲估计噪声。

无致命信号。

## C. 仿真条件可行性（4b，2026-07-06 补完）

> Step 5（D-S5-01 baseline 选定 + 田野调查）后执行。守 gw-feasibility §4b 维度 C。

1. **仿真环境能否创造条件让核心方法（单载波时域 NDA-ML 升 M₀=8 次幂）优势体现？** ✅ 是。MVE 已实测验证：`_mve_results.json` 公平对照 fair gain @ HD-FEC AWGN +0.704 / weak +1.199 / moderate +1.922 dB 全 ≥0.5dB，strong 工作区(≥15dB)全赢 DA（per-point +1.19~+2.62dB）。仿真环境（`common/_channel.py` GG 块衰落 + Doppler + Wiener PN + `_recovery.py` NDA-ML/DA ML）已支撑核心方法关键特征，NDA-ML 升 M₀ 次幂的去调制优势 + 全帧积分对 deep fade 的鲁棒性都在仿真中显现。

2. **目标方法关键特征在仿真中是否有足够大差异信号？** ✅ 是。BER 曲线跨 SNR 下降明显（AWGN 0.187→0.002，~2 个数量级；strong 0.40→0.024，~1.2 个数量级，来源 `_mve_results.json` results.awgn/strong nda_ber）。NDA vs DA 差异在 HD-FEC 阈值处达 0.7-1.9 dB 公平增益，**远超仿真噪声底**（N=102400 符号/点 × 多 SNR 点，统计涨落 <0.1dB）。差异信号足够大。

3. **仿真是否包含 NDA-ML 擅长的信号特征？** ✅ 是。NDA-ML 的两个擅长维度都在仿真中：
   - **频谱效率维度（形态 A）**：pilot overhead 是真实能量代价（DA ML 需 25% pilot，1.249dB 总能量代价），仿真含公平总功率对照（γ_tot 坐标）
   - **deep fade 鲁棒性维度（形态 C）**：GG 块衰落 h 时变 + Wiener PN 逐符号演化 + Doppler CFO 三重随机全在仿真中。NDA 全帧积分（N=256）vs DA pilot 局部估计（N_p=64）的差异在 strong 湍流工作区显现（NDA 全 5/5 点赢 DA）

4. **领域专属检查（domain-comms.md "过于平滑"预警）** ✅ 无预警。"过于平滑"经典案例是缺少随机化模块致自相关过高（如 leo-channel-pred 缺 ITU-R P.1853 雨衰时序→自相关 0.98）。本 MVE 含三重独立随机源（GG 块衰落 h + Wiener 逐符号 θ + Doppler CFO），BER 曲线陡峭（见 §2），非平滑假象。

**C 维度结论**：无致命信号。仿真条件充分支撑核心方法关键特征，差异信号远超噪声底。

## D. 最小可行实验（MVE）

- **假设**：在单载波时域 (8,8)-16APSK + Wiener PN + GG 块衰落信道下，NDA-ML（升 M₀=8）相对 DA ML（pilot sp=4）的公平对照 BER gain @ HD-FEC ≥0.5dB（AWGN/weak/moderate），strong 全工作区 NDA 赢 DA。
- **最小实例**：N_sym=102400 符号/点（400 块 × 256，FR-21 N≥1e5），seed 固定。调制 (8,8)-16APSK + Gray。信道 AWGN [5,8,10,12,14,16,18,20]dB + 星地湍流 weak/moderate/strong [5,10,15,20,22,24,26]dB。
- **[FR-04] 实例保真度**：保留 GG 幅度分布 + Wiener PN + 单载波时域升幂 ML + pilot overhead 公平对照全部核心结构。合理简化：省略 OFDM 帧结构（架构性不等价已论证 D002）+ STO 估计（B7 范围）+ 块内 h 恒定（BLOCK=256 约定）。结论可外推到含 STO 的完整单载波系统。
- **[FR-20] 关键物理参数溯源**（执行前已做）：CLW=500kHz / HD-FEC BER=3.8e-3 / LEO Doppler rate / (8,8)-16APSK / M₀=8 全从 `params.py` B11Params 取，source 标 B11/sat.1553/Fernandes（TL-26 已制度化）。
- **[FR-21] oracle 上界前置门控**：CRLB 层 CRB_NDA/CRB_DA = N_p/N = 1/4（M₀² 严格相消），NDA-ML 理论下界优于 DA ML → 上界 ≥0.5dB 通过，跑 MVE（D004 GO_MVE）。
- **pass/fail 标准**（SPEC §5 预定义）：Go = AWGN/weak/moderate fair gain ≥0.5dB AND strong NDA 全工作区赢 DA。
- **结果**（`_mve_results.json` 实测，主线 grep 核查）：

| 场景 | fair gain @ HD-FEC | SPEC §5 Go 门 | 判定 |
|---|---|---|---|
| AWGN（形态 A）| **+0.704 dB** | ≥0.5 | ✅ PASS |
| weak（形态 A+C）| **+1.199 dB** | ≥0.5 | ✅ PASS |
| moderate（形态 A+C）| **+1.922 dB** | ≥0.5 | ✅ PASS |
| strong（形态 C）| HD-FEC 不可达 + 工作区(≥15dB)全赢（per-point +1.19~+2.62dB）| 形态 C 鲁棒性 | ✅ PASS |

辅助：NDA-vs-oracle gap 全 <3dB（0.38/1.49/1.97/2.58dB，升幂实现正确）；TL-20 预期 5 项全 PASS 0 DEVIATION。

### MVE 架构摘要 [FR-11]

- **动作空间**：NDA-ML 升 M₀=8 次幂盲去调制（连续相位估计，非离散动作）
- **决策粒度**：per-block（256 符号 CPE 估计 + 256 符号 resolve M₀-fold 模糊 + 100 符号 h 估计）
- **对比范式**：NDA-ML（无 pilot）vs DA ML（pilot sp=4，25% overhead），公平对照含 pilot 能量代价（γ_tot 坐标）
- **奖励语义**：BER @ HD-FEC threshold=3.8e-3（信息符号有效 SNR）
- **先验对照**：DA ML（pilot-aided 近最优，pilot_sym=已知 tx 符号）

### [FR-14] 先验对照 / [FR-15] 目标 baseline 对照

- **FR-14 最强简单先验**：DA ML（pilot sp=4，pilot-aided 近最优）。MVE 实测 NDA-ML 公平对照赢之（fair gain +0.704~+1.922dB @ HD-FEC）。
- **FR-15 贡献目标 baseline**：DA ML（pilot sp=4）。本方向贡献声称 = 单载波时域 NDA-ML 在公平总功率下赢 DA ML，MVE 已验证。

### [FR-18] 环境保真度竞争格局分析

- **简化环境偏差**：单载波时域（无 OFDM DFT 处理增益）+ GG 块衰落（无时变 h，块内恒定）+ per-block 独立 CPE（无跨块跟踪）
- **对主方法（NDA-ML）影响**：升幂噪声放大无 DFT 增益抵消，deep fade 处不利（MVE 已实测，strong 低 SNR cross-over）
- **对 baseline（DA ML）影响**：pilot sp=4 在 deep fade 块崩溃（MVE 实测 strong DA BER 0.030 vs NDA 0.024 @ 26dB）
- **预判真实化后**：加跨块 KF/CPE 跟踪 → DA ML 高 SNR 反超可能强化（cross-over 位置移动）；加 OFDM 频域 ML → 完全不同架构（B11 路径，已 D002 排除）

## E. 资源/风险比例（4b，2026-07-06 补完）

> Step 5（D-S5-01 baseline 选定）后执行。守 gw-feasibility §4b 维度 E。

1. **Baseline 代码可获取性统计**：全部自实现，代码状态良好。
   - **DA ML（FR-15 目标 baseline）**：已实现（`common/_recovery.py:da_ml_recovery`，pilot sp=4，pilot 符号从已知 bits 生成）。MVE 已跑通验证。
   - **NDA-ML（提出方法）**：已实现（`common/_recovery.py:nda_ml_recovery`，升 M₀=8 + per-block 盲 h + resolve blockwise + 两阶段 FOE）。MVE 已跑通。
   - **oracle（FR-21 上界对照）**：已实现（genie-aided 完美 CSI），MVE 已用于 gap 验证（0.38-2.58dB 全 <3dB）。
   - **VV CFR（候选 7，通用 CPR）**：已实现（`common/_recovery.py`），可作为二级迁移对比 baseline。
   - 无"大部分需自实现"风险——Step 6 正式仿真器在 MVE 脚本基础上工程化（独立实现，守已知债务"不复用 explore 探针"），非从零开始。

2. **时间投入估计 vs 预期贡献**：MVE 已 PASS，工程量中等。
   - Step 6（仿真器设计）：写 `simulator-design.md`（守 FR-12 架构差异门控）+ SPEC 补 NDA-ML 段，~1 对话
   - Step 7（实现）：正式仿真器（MVE 脚本 → experiments/ 工程化）+ 训练/评估流水线 + 多种子统计，~2-3 对话
   - 贡献：形态 A（频谱效率，AWGN +0.704dB）+ 形态 C（鲁棒性，strong 全赢 DA）双增量，MVE 已实证。**会议级别够格**（守 D005 务实路线 + 同门范式 2-4dB 区间）。

3. **失败兜底（沉没成本可转化）**：✅ 可以。
   - **形态 A 独立成立**：AWGN fair gain +0.704dB 已 MVE PASS，即使 Step 6/7 退化（如 cross-over 位置移动、strong 不可达），形态 A 单独够发（频谱效率维度，去 pilot overhead 是真实能量代价）
   - **形态 C 有 weak/moderate 数据支撑**：即使 Step 6 加跨块 KF/CPE 跟踪后 strong cross-over 移动，weak(+1.199)/moderate(+1.922) 仍有 ≥0.5dB buffer
   - **次优成果可回收**：①条件边界分析（哪些湍流等级 NDA 赢/输 DA）②对比基准（DA ML pilot sp=4 近最优实现 + 公平对照框架）③方法可行性验证（单载波时域 NDA-ML 升幂 MVE 通过）
   - **无"全部沉没"风险**：MVE 已 PASS，最坏情况是 Step 7 正式实验后增益缩窄但仍 ≥0.5dB（MVE buffer 足够）

**E 维度结论**：无致命信号。Baseline 代码良好 + 时间投入与贡献成比例 + 失败兜底充分（形态 A 独立成立 + 形态 C 有 buffer + 次优成果可回收）。

## 4b 决策（2026-07-06）

> 阶段: GW Step 4b（C/E 维度，gw-feasibility §4b）| 依据: C/E 维度评估 + D-S5-01 baseline 选定 + 田野调查
> 用户确认: ⬜（待）

**决策**：**Go**（继续 Step 6 仿真器设计）。

**理由**：
- C 维度无致命：仿真条件充分支撑核心方法关键特征，差异信号远超噪声底，无"过于平滑"预警
- E 维度无致命：Baseline 代码良好 + 时间投入与贡献成比例 + 失败兜底充分（形态 A 独立 + 形态 C buffer + 次优可回收）
- 前置依赖满足：D005 MVE Go（4a）+ D-S5-01 baseline 选定（Step 5）+ 田野调查部分确认

**风险记录**（已知，不卡 Go）：
- 田野调查"部分确认"（DA ML 非最高频显式基准，BPS 在光纤 QAM 子领域更高频）→ 不影响本项目（单载波 M-APSK + 星地，BPS 主面 QAM 场景不同），但论文写作时需说明 baseline 选择的场景依据
- Step 6 正式仿真器需独立实现（不复用 explore 探针，守 MVE 独立性债务）

## Go/No-Go 决策

- **决策**：**Go**（4a: D005 MVE PASS + 4b: C/E 无致命）
- **4a 理由**：A0 无致命 + A'/A/B 无致命 + MVE 通过（公平对照 fair gain @ HD-FEC AWGN/weak/moderate 全 ≥0.5dB，strong 形态 C 成立）+ FR-20 参数已溯源 + FR-21 oracle 上界前置门控通过（CRLB 层）。
- **4b 理由**：C 维度（仿真条件充分支撑核心方法关键特征，差异信号远超噪声底，无"过于平滑"预警）+ E 维度（Baseline 代码良好 + 时间投入与贡献成比例 + 失败兜底充分）。
- **用户确认**：⬜（待）

## 下一步（Step 5 Baseline 选定，待用户确认 Go 后）

按 gw-validate.md Step 5：
1. 统计 literature_notes 载波同步 v2 章节中"使用的 Baseline 方法"频率
2. 领域 Baseline 田野调查（≥10 篇）
3. 生成 Baseline 候选评估表
4. 选定 1-2 个 baseline

**初步锁定**（D005，待 Step 5 正式确认）：DA ML（pilot sp=4，pilot-aided 近最优）= FR-15 目标 baseline；NDA-ML（升 M₀=8 + per-block 盲 h + resolve blockwise + 两阶段 FOE）= 提出方法。

## 已知债务

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| 单载波 DA ML 近最优（pilot sp=4）vs B11 论文 DA ML（decision-feedback）不对等 | FR-14 baseline 公平对照 | D004 公平对照框架（含 pilot overhead）部分缓解 | Step 5/6 视情况补 decision-feedback DA ML 对照 |
| 子 agent MVE 脚本是 `_time_domain_crlb.py` 薄包装 | MVE 独立性 | 主线 grep 核查底层代码合格（6 项纪律全落实）→ 结论有效 | Step 6 正式仿真器需独立实现（不复用 explore 探针）|
| strong 湍流 HD-FEC 不可达（物理上限）| FR-21 工作点 | oracle 也不可达 = 物理上限非方法缺陷 | 若需 strong 工作点，换 AIR 指标（SPEC §7）或更低 FEC 阈值 |
