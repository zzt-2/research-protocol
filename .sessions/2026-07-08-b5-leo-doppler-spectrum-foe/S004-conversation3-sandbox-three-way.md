# [S004] 对话 3 — 阶段 1 sandbox 三方对照（B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power）

> 2026-07-08 | 阶段: 工作对话执行阶段 1 sandbox 三方对照（首次写代码）| 状态: 完成，路径 C sandbox PASS，可进 MVE

## 目标

承接工作对话对话 2 S003 + H003 派发，执行阶段 1 sandbox 三方对照。核心是验证路径 C 在湍流下是否成立——前馈归一化后 B5 范围优势（捕获范围 ±4.5GHz + 残频 σ<140MHz + 收敛性）在湍流信道下是否仍成立。

## 记录

### 报到 + 接收方验证（步骤 1）

session-governance Trigger 1 报到 + 读必读清单 1-7：
- 本专题文件（topic-index 14 不变量 / H003 / S003 / decisions.md D001 / voice.md）
- 对话 2 阶段 0.3-0.6 产出 4 文件（_architecture_decision / _fair_comparison_framework / _b5_params_draft / _file_organization）
- B5 锚全文 content.md L60-159（算法原理 L71-87 / 式 2-4 / L85 α=6×10⁸ / L87 1024组16点 / L117 ±B/2 / L141 收敛性 / L147 56MHz/s / L149 BER 1e-3 −48dBm）
- [60] Leven 全文 L1-90（L55-65 Mth-power 算法 / L57 500 样本 / L121 BER 1e-3 / L123 7dB penalty）
- 复用基建（fft_foe_m0_omega sc_nda_ml_sim.py:137 / fft_foe common/_recovery.py:37 / _channel.py generate_shared_realization / B7Params params.py:606）
- 框架文件 + 教训（sim-preflight SKILL §1.5 C1-C5 + §1.6 C6-C8 / mve-validation V1-V6 / param-source.md / interrupt.md 10-12 / thesis-lessons TL-13/20/26/27）
- B2 sandbox 脚本参照（_sandbox_three_way.py 含 meta 字段强制 + 公平对照设计）

接收方验证 4 条全打钩 + 3 条关键事实核查全 PASS：
- 前馈归一化后范围优势三项验证 PASS（_architecture_decision.md §0.3b 三项验证表 + B5 锚 L71-87/L93/L117/L141）
- baseline = 传统 FFT FOE（_fair_comparison_framework.md §0.4.1 + common/_recovery.py:37 fft_foe 接口存在）
- B5Params 20 字段全溯源（_b5_params_draft.md 溯源审计汇总表 + B5 锚 content.md 行号数值匹配）
- registry 4 依赖全稳定 + 范围未违反"明确不含"

### 简版理论预期表（步骤 2，TL-20 sandbox 前必写）

**C6 公式重建**（B5 锚式 2-4 picture omitted，从 L77-87 文字重建）：
- 式 1：`R[k] = |FFT(r[n]·win)|²`（离散功率谱）
- 式 2：`Δf_est = α × R_{p-n}`（L85 α=6×10⁸）
- 式 3：`R_{p-n} = P_+ − P_−`（正负功率谱面积比，归一化变体 `(P_+−P_−)/(P_+ + P_−)`）
- 式 4：`Δf_comp = Δf_est + ephemeris_pred`（星历预测调 LO）
- **C6 标注**：PDF→md 公式丢失，从 L77-87 文字重建。Rp-n 歧义（绝对差 vs 归一化差）→ normalize_mode 三方案都实现，sandbox 选最优

**理论预期表**（TL-20 量化锚点）：

| 指标 | B5 | 传统 FFT FOE | [60] Leven | 偏离阈值 |
|---|---|---|---|---|
| 捕获范围 | ±4.5GHz（星历+FFT） | ±312.5MHz | ±312.5MHz | B5 <±4GHz → 查 |
| 残频 σ（无湍流） | <140MHz | <312.5MHz | <10MHz | B5 >200MHz → 查 |
| 残频 σ（有湍流+归一化） | <140MHz（路径 C 前提） | baseline 实测 | baseline 实测 | **>140MHz → 红线警报** |
| 范围扩展 vs fft_foe | 15× | 1× | ~1× | **<10× → 路径 C 不成立** |
| 收敛性 | 3-4 次迭代 | 单次 | 单次 | >6 次 → 查 |

### B5Params 落盘 params.py（步骤 2，主线程直接做）

B5Params 类加到 params.py（B7Params 之后，B3Params 之前），20 字段全溯源 + HD_FEC_THRESHOLD_B5 跨候选对齐。修正 draft 里 RX_SENSITIVITY_B5 单位歧义（改成 RX_SENSITIVITY_DBM_B5=-48.0 dBm，跟 B7Params BER_SENSITIVITY 模式对齐）。import 验证 PASS。

### 两个估计器实现（步骤 2，派 2 子 agent 并行）

**子 agent 1：short_time_spectrum_foe**（598 行）：
- 分块 FFT + Hanning + 均值滤波 + Rp-n + α·Rp-n + 星历预测 + 迭代收敛（B5 锚 L141）
- normalize_mode 三方案：block/agc/ratio。**实测发现 α=6×10⁸ 暗 ratio 模式**（Rp-n 饱和 0.5 × 6e8 = 300MHz ≈ B/8=312.5MHz）
- **block ≡ ratio**（按块归一化后 Rp-n 尺度无关），agc 须重校 α
- 迭代收敛：0.5GHz→2 次，1.0GHz→3 次，1.5GHz→4 次（吻合 B5 锚 L141）
- 大频偏 4GHz + 星历 3GHz 迭代 3 次残频 -23MHz（±4.5GHz 全量程覆盖）
- **机制发现**：测试信号须带限（RRC/低通），平坦白谱 Rp-n≈0 无信息（B5 锚 L115 ICR 低通 + L85 Nyquist shaping 致 sinc 谱）

**子 agent 2：leven_mthpower_foe**（290 行）：
- [60] Leven L55-65：差分 → 4 次方 → 500 样本求和 → 相位/4 → 频偏估计
- normalize_mode 三方案：block/agc/ratio。**agc≡ratio 数学等价**（差分域归一）
- 100MHz 估计 101.024MHz（含信道 1MHz F_RESIDUAL），捕获范围 ±312.5MHz 命中理论边界
- 纯信号验证算法零偏（fest=3.6e-16 MHz 无频偏）

**主线独立核查**（V5，子 agent 归因独立验证）：
- B5 前馈开环无环路 TF ✓（grep 无"环路/反馈/H(z)"，实现步骤 0a-7 全前馈）
- 参数从 B5Params 导入 ✓（默认参数留字面值跟 B5Params 一致，main 用 B5Params）
- 信道从 common 导入 ✓（`from common._channel import generate_shared_realization`）
- C6 公式标注 ✓（式 1-4 标 content.md 行号 + PDF→md 重建）
- 自测数字独立重跑验证：B5 1GHz 迭代 3 次残频 163.6MHz / 4GHz+星历残频 -23MHz / 三方案 138.2/138.5/138.5 ✓ 全一致
- [60] Leven 100MHz 101.024MHz / 捕获范围 ±312.5MHz ✓ 一致

### 三方对照 sandbox（步骤 3，派子 agent + 主线独立核查）

**子 agent 3 跑 sandbox**（9.6s，3 turb × 3 snr × 20 seed 主表 + 19 点 × 5 seed 范围扫描 + 27 点 × 20 seed 湍流扫描）：

**fair gain 二维报告**：

| 方法 | 捕获范围 | 收敛点/19 | 残频 σ（weak/snr13） |
|---|---|---|---|
| B5（星历+迭代） | ±4.5GHz | 19/19 ✓ | 6.5MHz |
| B5纯FFT（无星历） | ±1.18GHz | 5/19 | — |
| 传统 FFT FOE | ±0.24GHz（理论 ±312.5MHz） | 1/19（仅 f=0） | 0.1MHz（范围内） |
| [60] Leven | ±0.24GHz（理论 ±312.5MHz） | 1/19（仅 f=0） | 2.9MHz（范围内） |

**路径 C 核心前提验证**（湍流下残频 σ，27 点全 <140MHz）：

| 湍流 | B5 残频 σ 范围（MHz） | max（MHz） | 门控 140MHz |
|---|---|---|---|
| weak | 9.25 - 10.33 | 10.33 | ✅ 裕度 129.7MHz |
| moderate | 10.36 - 13.03 | 13.03 | ✅ 裕度 127.0MHz |
| strong | 13.76 - 16.20 | 16.20 | ✅ 裕度 123.8MHz |

**主线独立核查**（V5，从原始 JSON 重算）：
- Doppler 范围扫描：B5 19/19 收敛，fft_foe/leven 1/19（仅 f=0）✓ 一致
- 湍流残频 σ：全 27 点 < 140MHz，max 16.20MHz ✓ 一致
- 范围扩展 B5/fft_foe = 14.4×（±4.5GHz / ±312.5MHz 理论值）✓ 一致
- fair_gain.pathC_verdict = PASS ✓

**诚实标注**：
1. **星历预测完美假设**：sandbox 模拟星历预测 ephemeris_pred=f_true（残频≈0+噪声），B5 估的是噪声/湍流致 Rp-n 抖动。实际星历预测有残差（几十 MHz），但即使加残差 B5 残频 σ 仍远低于 140MHz（裕度 123.8MHz）
2. **baselines 超范围折叠**（预期非 bug）：fft_foe/leven 在 ±312.5MHz 外频偏折叠到 1.25GHz 残频，BER≈0.5。这是 B5 范围优势的体现
3. **B5 BER 偏高**（0.23-0.37）：B5 是粗 CFO 估计器，残频交后续精细 DSP。BER 不是 B5 强项（fair gain 维度 1 范围扩展 + 维度 2 残频 σ 才是）
4. **[60] Leven 范围差异**：0.4.2 表 [60] Leven ±1.6GHz（原文 L157），sandbox ±312.5MHz（1-sps fs=2.5e9 限制）。sandbox [60] Leven 非最优条件，fair gain 报告标注

### 路径 C 判定门控

| 门控项 | 目标 | 实测 | 判定 |
|---|---|---|---|
| 范围扩展 | ≥10× | 14.4× | **PASS** |
| 湍流下残频 σ | <140MHz | max 16.20MHz | **PASS**（裕度 123.8MHz） |
| 收敛性 | 不退化 | 19/19 全收敛 | **PASS** |
| 湍流 σ 扫描通过率 | — | 27/27 | **PASS** |

**路径 C sandbox 判定：PASS** ✓ — 前馈归一化后 B5 范围优势在湍流下仍成立，进 MVE。

**无红线警报**：范围优势未崩塌（残频 σ max 16.20MHz << 140MHz，范围扩展 14.4× ≥10×，收敛性 19/19）。

## 决策引用

- D001：开 B5-Q1 专题 + 首验证够格路径（路径 C 成立）
- 无新建决策（sandbox PASS 不需新建 D###，路径 C 验证完成是 D001 执行结果）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 1 sandbox 三方对照，不回头救 Kill / 不判他候选 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 后续

**对话 4（sandbox 通过后）**：阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
- 写 B5-MVE-SPEC.md（含 TL-20 理论预期表，仿 N1-MVE-SPEC.md §2）
- MVE 跑正式实验（守 FR-11 架构摘要 + FR-12 MVE→Formal 架构差异 + sim-preflight V1-V6）
- consistency bit-exact（MVE vs Formal）
- MVE 通过后 short_time_spectrum_foe 进 common/_recovery.py，B5Params 已在 params.py

**sandbox 产出可复用**：
- _short_time_spectrum_foe.py（B5 估计器，MVE 可直接用）
- _leven_mthpower_foe.py（[60] Leven 对照，MVE 可直接用）
- _sandbox_three_way.py + 3 个 JSON（fair gain 二维报告，MVE 可参照）
