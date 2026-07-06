# [S003] 单载波时域 NDA-ML CRLB GO_MVE + MVE-SPEC 写完（执行 H002）

> 2026-07-06 | Step 4a 维度 D MVE 执行 | 状态：完成（CRLB GO_MVE + 信道校准修复 + MVE-SPEC 契约）

## 目标

执行 H002 三步：报到+框架重读 + 单载波时域 NDA-ML 改进增量定位（讨论锁形态）+ 派子 agent 推导时域 CRLB + 数值验证。

## 记录

### 步骤 1：报到 + 框架重读 ✅

- 用户："要不你接着做？上下文还够"——续做对话 2，不新开
- H002 + decisions（D001/D002/D003）刚写，上下文都有
- 关键文件：_star_ground_link_survey / _OFDM_infra_assessment / _awgn_repro_results（上轮产出，本轮继承）

### 步骤 2：增量形态拍板 = A+C ✅

基于 _awgn_repro_results.json 分析：
- DA ML（pilot sp=4）@ HD-FEC = 18.10dB 含 1.25dB pilot 代价 → 总能量 19.35dB
- NDA-ML @ HD-FEC = 18.70dB（纯数据）
- 公平对照（相同总功率）下 AWGN 增量 = 19.35 - 18.70 = +0.65dB

讨论 3 个形态（A 频谱效率 / B 稀疏 pilot + NDA 辅助 / C 湍流鲁棒性）。**用户拍板形态 A+C**：AWGN 频谱效率 + 星地湍流鲁棒性，双增量叙事。MVE 扫描含湍流维度。

### 步骤 3：时域 CRLB 推导 + 公平对照 BER ✅（GO_MVE）

派子 agent（≤15min）：

**解析 CRB 推导**：
- CRB_NDA(φ) = σ²/Σ_n |s(n)|²h(n)（全 N 符号贡献）
- CRB_DA(φ) = σ²/Σ_{n∈P} |s_p|²h(n)（仅 N_p=N/4 pilot 贡献）
- **M₀² 严格相消**：升幂噪声方差放大 M₀²（分母）与相位参数增益 (d arg(z)/dφ)²=M₀²（分子）相消
- **比值 CRB_NDA/CRB_DA ≈ N_p/N = 1/4**（不是上一轮误推的 64×）
- **CRLB 层 NDA-ML 理论下界优于 DA ML**

**公平对照 BER**（首轮，BER floor 太高）：
- AWGN +0.70dB（HD-FEC）✅
- 湍流 HD-FEC 不可达（BER floor 0.08-0.14）

**TL-22 物理前提核查**：BER floor 太高需诊断。strong +4.04dB 超 B11 +2dB 但 NDA-vs-oracle gap 仅 1.82dB（排除升幂 bug）。

### 步骤 3'：信道校准修复 ✅（关键）

派子 agent 诊断 BER floor 根因：
- **主因 D2**：h_med 标量均衡残差（连 oracle 真相位+真 h 都被锁 BER floor，证明是幅度均衡问题）
- **次因 D1**：CFO 残余（assume_df_zero=True 跳 FOE 在星地有 Doppler 下错误）
- D3（CLW）无关（湍流用 LASER_LW=10kHz 单端）

**修复**：
- per-block h 均衡（NDA 盲 ĥ=mean(|rx|²)−1/(2γ)，DA pilot ĥ=mean(|r(p)/s(p)|²)，oracle 真 h）
- 两阶段相位（fft_foe(M0=8) 粗估 CFO + nda_ml_recovery(assume_df_zero=True) 估残余 CPE）
- SNR 扫扩至 26dB（TL-22 物理可达性）

**修复后**：
- weak: BER floor 7.83e-2 → 5.37e-4（HD-FEC 可达 @~22dB）
- moderate: 9.73e-2 → 2.71e-3（可达 @~26dB）
- strong: 1.35e-1 → 2.43e-2（不可达，但 oracle@26dB=1.96e-2 也不可达——物理上限）

**公平 gain @ HD-FEC**：AWGN +0.70 / weak +1.20 / moderate +1.92 / strong 物理不可达但 NDA 全工作区赢。全 PASS TL-20。

### 步骤 4：SC-NDA-ML-MVE-SPEC.md 写完 ✅

仿 N1-MVE-SPEC.md 9 节模板：
1. 核心假设（形态 A+C，CRLB 理论支撑）
2. TL-20 理论预期表（4 场景预期 gain + 量化锚点）
3. 最小实例（FR-04 保真度）
4. baseline 设计（FR-14/15，DA ML 含 1.25dB pilot overhead 公平对照）
5. pass/fail 标准（AWGN ≥0.5dB Go / 0.3-0.5 Conditional / <0.3 Kill）
6. 扫描设计（AWGN [5-20] + 湍流 [5-26]，N=102400/点）
7. AIR 计算（可选辅助）
8. 执行约束（≤900s + 守 D003 调用方式）
9. 子 agent 返回格式

## 决策引用

- D004：单载波时域 NDA-ML GO_MVE + 公平对照框架（新建，CRLB + 修复后公平对照综合支撑）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。形态 A+C 是 D002 方案 C（单载波时域 NDA-ML 改进）的具体化，在范围（"复用 common 基建 + 增量扩充 common" + "explore/ 模式每候选一子目录"）。

## 后续

1. **对话 3**（H003）：跑 SC-NDA-ML MVE（守 FR-11 架构摘要 + FR-14/15 + FR-18）
2. **B7 后置**：单载波 NDA-ML MVE 完后视情况
3. **B3 架构决策**：待最后（多孔径阵列 vs 单链路）
4. **本轮产出**：_time_domain_crlb.py + _crlb_results.json + _ber_floor_diagnostic.py + _ber_floor_diagnostic.json + SC-NDA-ML-MVE-SPEC.md
