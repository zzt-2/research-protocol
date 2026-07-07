# B7 阶段 0.4：公平对照框架设计

> 阶段 0.4 | 专题 `2026-07-08-b7-gardner-ted-foe` | 日期 2026-07-08
> 依据：D005 务实路线（fair gain 维度对齐）+ INVARIANT 6（阶段 0 不写代码）+ sim-preflight v1.3.0 C7（三方对照）+ TL-26（参数溯源）+ FR-26（读原文数值）
> 用户决策（2026-07-08）：① 工作点 = BER 2e-2 + HD-FEC 3.8e-3 双工作点 ② 场景参数 = B7 锚论文原参数 25GBaud/1.8kHz
> 结论：**B7 fair gain = 二维报告（BER gain @ 双工作点 + Doppler 估计范围比）+ 工作点主判据 HD-FEC / 锚论文一致性校验 BER 2e-2 + PSA FOE baseline 必须重写（谱不对称法，非 pilot-aided）**

## 0. 核查触发

H003 阶段 0.4 要求回答 4 个问题：
1. fair gain 定义（B7 vs PSA FOE 都是前馈 FOE，无 pilot overhead 差异，不能照搬 NDA-ML 的 1.25dB pilot 代价框架）
2. 工作点选择（B7 锚论文 BER 2e-2 vs NDA-ML HD-FEC 3.8e-3）
3. 范围维度量化（B7 1.9× 估计范围怎么进 fair gain）
4. Doppler 扫频公平性（PSA FOE >12GHz 失败的"失败"怎么定义）

## 1. NDA-ML vs B7 公平对照维度对比（为什么不能照搬）

| 维度 | NDA-ML（step4a 专题） | B7（本专题） |
|---|---|---|
| baseline 类型 | DA ML（pilot-aided）| PSA FOE（谱不对称法，前馈盲估）|
| pilot overhead 差异 | **有**（DA ML 25% pilot = 1.25dB 总能量代价，NDA-ML 0%）| **无**（两者都是盲前馈 FOE，无 pilot overhead）|
| fair gain 核心来源 | 频谱效率（pilot overhead 去除）+ fade 鲁棒性 | 估计范围扩展 + 低 SNR 鲁棒性 |
| BER gain 量级 | +1.3~2.5dB @ HD-FEC | +0.6dB @ BER 2e-2 |
| 范围维度 | 无（都在相同 Doppler 范围测） | **有**（1.9× = 0-23GHz vs 0-12GHz，结构性优势）|

**关键结论**：NDA-ML 的 fair gain 框架（fair gain = BER gain @ HD-FEC，相同 Doppler 范围）**不能直接搬给 B7**。B7 增量一半在 BER gain（0.6dB），一半在范围扩展（1.9×），单一 BER gain 指标会丢失范围维度信息。

## 2. B7 fair gain 定义（二维报告，不合成单一指标）

### 2.1 维度 1：BER gain @ 双工作点

**主判据**：HD-FEC BER = 3.8e-3（跟 NDA-ML 跨候选可比，FR-15 目标 baseline 对照）
**一致性校验**：BER 2e-2（跟 B7 锚论文对齐，验证复现真实性）

| 工作点 | 角色 | 用途 | 预期 B7 vs PSA FOE |
|---|---|---|---|
| **HD-FEC 3.8e-3** | 主判据 | 跨候选排序（B7 vs NDA-ML vs B2-Q2）| 待 sandbox 测；TL-20 预期 ≥0.3dB（LPF2 噪声抑制 + 范围优势在 HD-FEC 应仍成立）|
| **BER 2e-2** | 锚论文一致性校验 | 验证 B7 复现真实性 | 实测应 ≈0.6dB（`content.md:21/65/69`）；偏离 >0.2dB 触发 TL-20 偏离即查 |

**为什么用双工作点**：
- BER 2e-2 单独不够：跟 NDA-ML 不可比（NDA-ML 在 HD-FEC），跨候选排序时需额外换算
- HD-FEC 单独不够：B7 锚论文 0.6dB @ BER 2e-2 是唯一已知的真实增量，HD-FEC 处的增量是外推（sandbox 需测）
- 双工作点：HD-FEC 作主判据保证跨候选可比，BER 2e-2 作锚校验保证 B7 复现不失真

**PSA FOE 在 >12GHz 的失败定义**（H003 Q4）：
- **失败判据 A（BER 爆）**：BER > 1e-1（无法解调，超 FEC 纠错能力）
- **失败判据 B（FOE 输出漂零）**：FOE 估计值偏离真值 > 50%（`content.md:49` "PSA FOE output drifts toward zero due to reduced spectral asymmetry"）
- sandbox 阶段两个判据都记录，主用 A（BER 爆）作 fair gain 计算边界，B 作机制解释

### 2.2 维度 2：Doppler 估计范围比

**定义**：range_ratio = B7 可估准 Doppler 上限 / PSA FOE 可估准 Doppler 上限

**poster 实测**（`content.md:49`）：
- B7 可估准 0-23GHz（扫描范围上限）
- PSA FOE >12GHz 失败（半 baud rate 限制，`content.md:19` "typically confined to a narrow estimation range—usually within half the baud rate"）
- **range_ratio = 23/12 ≈ 1.9×**（poster `content.md:21/49/69` 三处一致）

**为什么单独维度不合成**：
- 0.6dB BER gain 偏小（D005 会议门槛"几 dB"标尺下偏弱）
- 1.9× 范围是结构性优势（非边际 dB），硬合成单一指标（如「等效 dB」）会引入主观加权
- 二维报告让读者自行判断：会议级别贡献 = BER gain 够 HD-FEC + 范围够 1.9× + OSNR 10dB 鲁棒性

### 2.3 鲁棒性维度（辅助，非主判据）

**OSNR 10dB 可解调**（`content.md:21/69`）：B7 在 OSNR 10dB 仍可解调，PSA FOE 失败。
- 作辅助维度报告（记录但不进 fair gain 主判据）
- 理由：OSNR 10dB 是"低 SNR 极限"，不是标准工作点，跨候选对比时 NDA-ML 没在这个点测

## 3. PSA FOE baseline 实现债务（H003 重点，sandbox 必须解决）

### 3.1 债务描述

**common `_recovery.py:435` `psa_foe_recovery` 函数概念错**：
- 函数名 "PSA FOE"（Power-Spectrum-Asymmetry FOE，谱不对称法）
- 实现是 **pilot-aided FOE（pilot 差分相位法）**：`r_p = rx[pilot_idx]/pilot_sym; dtheta = diff(unwrap(angle(r_p))); df_est = LS(dθ/dt)`（L442-453）
- 注释自承 "Pilot-Aided Frequency Offset Estimation"（L437），跟 B7 真 baseline 不是一回事

**B7 真 baseline = PSA FOE（谱不对称法，Vieira 2023 [5/6]）**：
- 机制：Doppler 频偏致信号谱不对称，FFT 估功率谱 → 检测谱不对称方向/幅度 → 反演频偏
- 范围限制：估准范围 ≤ 半 baud rate（`content.md:19`，B7 场景 25GBaud → PSA FOE ≤12.5GHz，实测 >12GHz 失败）
- 不用 pilot（盲前馈），跟 B7 proposed FOE 同维度（都是盲前馈 FOE）

### 3.2 sandbox 阶段处理

**必须重写 `psa_foe_recovery`**（或新写 `psa_foe_asymmetry_recovery` 不污染旧函数）：
- 实现 Vieira 2023 [5] 谱不对称法（FFT → 功率谱 → 不对称度量化 → 频偏反演）
- 估准范围验证 ≤ 半 baud rate（25GBaud 场景 ≤12.5GHz，跟 poster 一致）
- 阶段 0 不写（守 INVARIANT 6），sandbox 阶段子 agent 实现

**旧 `psa_foe_recovery`（pilot-aided）处理**：
- 保留不删（explore/ 历史探针可能 import，B11/B3 候选用过）
- 改名或加 deprecation 注释（标注"非 B7 真 baseline，pilot-aided 非谱不对称法"）
- sandbox 阶段 B7 baseline 用新写的谱不对称版，不用这个

### 3.3 债务登记（带进 sandbox）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|---|---|---|---|
| `psa_foe_recovery` 概念错 | 公式忠实原文（B7 baseline 必须是谱不对称法）| pilot-aided 实现在 L435，非谱不对称法 | sandbox 阶段重写谱不对称版 baseline |

## 4. 三方对照架构（C7 + V2，sandbox 阶段执行）

守 sim-preflight v1.3.0 C7（三方对照）+ V2（改进版/1986 原版/baseline 三方归因可信）：

| 方 | 角色 | 实现 | 来源 |
|---|---|---|---|
| **B7 proposed FOE** | 候选方法 | 前馈扫频 + S-curve 峰反演 + 双候选 + TED2 std 判决（0.2a `_b7_map_reconstruction.py` 扩展）| B7 OFC 2026 `content.md:37` |
| **Gardner 1986 TR** | 祖师爷方（V3 红线警报）| 用户代码 `Tx2Rx.m:176-214` 定时环（Gardner TED + NCO + PI 环路滤波器）| `PSKTimingErrDetector.m` L8-9 + `Tx2Rx.m` L201 |
| **PSA FOE** | baseline（FR-15 目标对手）| **重写**谱不对称法（Vieira 2023 [5]）| Vieira 2023 IEEE Access |

**三方对照的公平性**：
- 三方都在相同 Doppler 扫频 0-23GHz 测（`content.md:49`）
- 三方都用相同 DP-QPSK 25GBaud 信号 + 相同信道实现（TL-13 共用 `common/_channel.py`）
- 三方输出都进相同 BER 评估链（FOE → Gardner TR → MIMO EQ → MP FOC → CPR → BER）

**V3 祖师爷警报触发条件**（sim-preflight v1.3.0 C8）：
- 若 sandbox 跑出 "B7 proposed FOE vs Gardner 1986 TR 持平"（BER gap <0.1dB）→ **红线警报**
- 0.2 已确认任务正交（B7 做 FOE 估 f_D，1986 做 STR 检 τ），持平可能性低
- 若真持平，需查实现 bug（B7 前馈扫频是否被错误实现成反馈跟踪）

## 5. TL-20 理论预期表（MVE 跑之前必须写明，偏离即查）

仿 N1-MVE-SPEC.md §2 格式，B7 fair gain 预期：

| 指标 | 预期 B7 vs PSA FOE | 物理依据 | 锚论文一致性校验 |
|---|---|---|---|
| BER gain @ BER 2e-2 | **+0.4 to +0.8 dB** | LPF2 噪声抑制 + TED 增益周期相关鲁棒性 | poster 实测 ≈0.6dB（`content.md:21/65/69`），偏离 >0.2dB 触发 TL-20 |
| BER gain @ HD-FEC 3.8e-3 | **+0.3 to +0.7 dB** | HD-FEC 比 BER 2e-2 更严格，B7 LPF2 优势在低 SNR 更显著，但绝对 BER gain 可能略减 | 待 sandbox 测（poster 未给）|
| Doppler 估计范围比 | **≈1.9×**（23/12）| B7 利用周期相关扩展到全 baud，PSA FOE 受半 baud 限制 | poster 实测 1.9×（`content.md:21/49/69`），偏离 >20% 触发 TL-20 |
| OSNR 10dB 可解调 | B7 可解调 / PSA FOE 失败 | B7 TED 增益在低 SNR 仍可定位峰 | poster 实测（`content.md:21/69`），二值判定 |

**量化锚点（偏离即停查代码，TL-20）**：
- BER gain @ BER 2e-2 < 0.2dB → **可疑**（LPF2 应有 0.6dB 增益）→ 查 LPF2 实现 + PSA FOE baseline 是否正确
- BER gain @ HD-FEC < 0 → **可疑**（B7 应至少持平 + 范围优势）→ 查 fair 对照坐标（相同 DP-QPSK + 相同信道）
- range_ratio < 1.5 或 > 2.5 → **可疑**（poster 1.9×）→ 查 PSA FOE 估准上限判定 + Doppler 扫频设置
- B7 vs Gardner 1986 TR BER gap <0.1dB → **V3 祖师爷红线警报**（任务正交不应持平）→ 查 B7 前馈扫频是否被错实现成反馈

**TL-20 偏离处理**：BER gain 偏离预期时，先查 LPF2 实现（poster 明确说 0.6dB 来自 LPF2，`content.md:65` "LPF2 improves receiver sensitivity by approximately 0.6dB"），再查 PSA FOE baseline 是否真是谱不对称法（防概念错债务污染）。

## 6. 阶段 0.4 判定

| 维度 | 判定 | 依据 |
|---|---|---|
| fair gain 定义 | **二维报告**（BER gain @ 双工作点 + 范围比）| B7 增量半在 BER gain 半在范围，单一指标丢信息 |
| 工作点 | **HD-FEC 主判据 + BER 2e-2 锚校验** | 用户决策（2026-07-08）：跨候选可比 + 锚论文真实性 |
| PSA FOE baseline | **sandbox 必须重写**（谱不对称法）| `psa_foe_recovery` 概念错（pilot-aided 非谱不对称法）|
| 三方对照架构 | B7 proposed / Gardner 1986 TR / PSA FOE | sim-preflight v1.3.0 C7+V2+V3 |
| TL-20 预期表 | 落盘（本节 §5）| 仿 N1-MVE-SPEC.md §2 |

**门控结论**：0.4 通过，进 0.5 参数真相源。

## 7. 对后续的影响

- **0.5 参数真相源**：B7 用锚论文原参数 25GBaud/1.8kHz（用户决策），跟 NDA-ML（2.5GBaud/10kHz）不统一。fair gain 维度对齐（都报 HD-FEC）而非场景参数统一
- **sandbox 三方对照**：三方都用 B7 场景参数（25GBaud/1.8kHz），公平。PSA FOE baseline 重写谱不对称法
- **跨候选排序**：B7 fair gain = BER gain @ HD-FEC（主）+ 范围比（辅）。NDA-ML fair gain = BER gain @ HD-FEC（主）+ 频谱效率（辅）。两个候选主判据对齐，辅维度各自报告
- **论文叙事**：B7 贡献定位「Doppler FOE 估计范围扩展 1.9× + 低 SNR 鲁棒性 + 0.6dB BER gain」，非「频谱效率」（那是 NDA-ML 的叙事）

## 8. 证据指针

- B7 锚论文量化：`papers/doi/10.1364_ofc.2026.w2a.62/content.md` L19（PSA FOE 半 baud 限制）/ L21（0.6dB+1.9×+10dB 三数）/ L37（算法结构）/ L49（1.9× 实测 + PSA FOE >12GHz 失败）/ L65（0.6dB 来自 LPF2）/ L69（结论三数）
- NDA-ML fair gain 框架：`projects/simulation/explore/single-carrier-nda-ml/SC-NDA-ML-MVE-SPEC.md` §4（pilot overhead 公平对照）
- N1-MVE-SPEC §2 模板：`projects/simulation/explore/n1-pcs-gain/N1-MVE-SPEC.md` §2（TL-20 理论预期表格式）
- PSA FOE 概念错：`projects/simulation/common/_recovery.py` L435-453（`psa_foe_recovery` 实现是 pilot-aided 非谱不对称法，L437 注释自承）
- B7 0.2a 数值重建（fair gain 复现基础）：`_b7_map_reconstruction.py` + `_b7_map_results.json`
- 用户决策原话：voice.md 2026-07-08 对话 4（双工作点 + B7 锚论文原参数）
