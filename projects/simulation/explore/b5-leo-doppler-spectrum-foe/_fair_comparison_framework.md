# 阶段 0.4 公平对照框架 — baseline 选定 + fair gain 定义 + 工作点 + LEO Doppler 差异化

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 来源: S003（工作对话对话 2）| 日期: 2026-07-08
> 纪律: INVARIANT 14（B5 特殊·代码基建新增需求 + LEO Doppler 主题差异化）+ D005 务实路线 + FR-25 Go/Kill 标准分离 + sim-preflight C7 三方对照 + TL-13 共用信道
> 守: 阶段 0 不写代码，本文件只定公平对照框架规约

## 核心问题

1. baseline 选 [60] Leven Mth-power 还是传统 FFT FOE？（任务环节对口度 + 范围可比性）
2. 范围 fair gain 怎么定义？（B5 不是 dB 增量是范围优势，单一 dB 指标不够）
3. 工作点选 BER 1e-3（B5 锚）还是 HD-FEC 3.8e-3（跨候选可比）？
4. B5 / B7 / B4 三个 LEO Doppler 候选的叙事怎么差异化避免撞车？

## 0.4.1 baseline 选定：传统 FFT FOE 为主 + [60] Leven Mth-power 作祖师爷对照

### 任务环节区分（S002 §3 溯源确认）

| 方法 | 任务环节 | 原文依据 |
|---|---|---|
| **B5 短时谱** | **粗 CFO**（残频落精估范围 ±312.5MHz 即完成任务）| B5 锚 L57 "compensate for frequency offsets in the range of [−B/8, +B/8]" + L93 残频检测交后续 DSP |
| **[60] Leven Mth-power** | **精细 FE**（前置于相位估计，残频交后续 PE）| [60] Leven L9 "frequency estimation allows, if performed **prior to block phase estimation**" + L157 OSNR <9dB 近乎与频偏无关 |
| **传统 FFT FOE** | **粗 CFO**（4 次幂 blind QPSK 找谱峰，跟 B5 同任务环节）| `common/_recovery.py:37` fft_foe，4 次幂 + Hanning 窗 + FFT 找谱峰 |

**关键警示**（S002 §3 + H002 已知债务）：[60] Leven 7dB penalty 是 differential decoding **无 FE** 时 500MHz 频偏的 OSNR penalty（[60] Leven L123），**不是 B5 vs [60] Leven 直接对比基线**。B5 vs [60] Leven 的 dB 对比需重新设计实验，不能直接引"7dB penalty"作 B5 增量。

### baseline 选定决策

| baseline 候选 | 任务环节对口度 | 范围可比性 | 复用基建 | 选定 |
|---|---|---|---|---|
| **传统 FFT FOE**（fft_foe）| **高**（频域找谱峰粗 CFO）| ±312.5MHz vs B5 ±4.5GHz = 15× 扩展 | ✅ `common/_recovery.py:37` | **主 baseline** |
| fft_foe_m0_omega | 高（M0 升幂找谱峰）| 同 ±312.5MHz | ✅ `sc_nda_ml_sim.py:137` | 备选（M0 升幂变体）|
| [60] Leven Mth-power | **低**（时域相位增量，精细 FE）| ±1.6GHz（实测），任务环节不同 | ❌ 需新写 | **祖师爷对照**（C7 三方对照用）|

**决策**：
- **主 baseline = 传统 FFT FOE（fft_foe）**——任务环节对口（频域找谱峰粗 CFO），范围 15× 扩展直接对比，复用基建已实现
- **[60] Leven Mth-power = 祖师爷对照**（C7 三方对照）——经典频偏估计方法（2007 Bell Labs），任务环节不同（精细 FE），作理论锚不作主 baseline
- **三方对照**（sim-preflight V2/C7）：B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power

### 公平性保证

1. **三方法都做前馈归一化**（0.3 决策，B5 路径 C 加湍流验证要求，baseline 也归一化保证公平）
2. **三方法共用同一信道实现**（TL-13，从 `common/_channel.py` 导入 `generate_shared_realization`，禁自建）
3. **三方法都用同一 BER 工作点评估**（BER 1e-3 + HD-FEC 3.8e-3 双工作点）
4. **三方法都扫同一 Doppler 范围**（±4.5GHz 全量程，确认捕获范围差异）

## 0.4.2 范围 fair gain 定义：二维报告（范围扩展 + 残频/BER 对比）

### 问题

B5 不是 dB 增量是范围优势（S002 §0.1c + `_cut-b4b5-verify.md:64-66` 确认），单一 dB 指标无法体现范围优势。参考 B7Params 已用的"二维 fair gain 报告"模式（B7 S004 D004+D005 fair gain 二维报告）。

### fair gain 二维定义

**参考口径**：sat.1553 L353 "SNR penalty vs perfectly synchronized system"（BER 1e-3 参照）+ B7 二维报告模式。

| 维度 | 指标 | B5 vs 传统 FFT FOE | B5 vs [60] Leven |
|---|---|---|---|
| **维度 1：范围扩展** | 捕获范围扩展倍数 | ±4.5GHz / ±312.5MHz = **15×** | ±4.5GHz / ±1.6GHz = **2.8×**（任务环节不同需标注）|
| **维度 1：Doppler rate 跟踪** | 最大可跟踪 Doppler rate | 56 MHz/s（B5 锚 L147）| [60] Leven 无 Doppler rate 跟踪设计（WDM 静态频偏）|
| **维度 2：残频指标** | 粗补偿后残频 σ | σ<140MHz（B5 锚）/ sandbox 实测 baseline 残频 | 任务环节不同，[60] Leven 残频 <10MHz（精细 FE，前提是 FE 已工作）|
| **维度 2：BER 工作点** | BER 1e-3 / HD-FEC 3.8e-3 接收灵敏度 | −48 dBm @ BER 1e-3（B5 锚 L149）| sandbox 实测三方法 BER 曲线 |

### fair gain 报告形式（sandbox/MVE 产出）

1. **范围扩展表**：B5 / 传统 FFT FOE / [60] Leven 三方法的捕获范围 + Doppler rate 跟踪能力 + 残频指标
2. **残频/BER 对比表**：三方法在同一信道（含湍流）下的残频 σ + BER 曲线 @ BER 1e-3 和 HD-FEC 3.8e-3

### 路径 C 够格条件（S002 §0.1c + H002 验证阈值表）

- 范围扩展 ≥10×（B5 15× 满足）+ 残频 <5MHz @ BER 1e-3 **或** 范围扩展 ≥10×
- **sandbox 需验证**：湍流下 B5 范围优势仍成立（残频 σ 不超 140MHz / 收敛性不退化 / 范围扩展仍 ≥10×）

## 0.4.3 工作点选定：BER 1e-3（B5 锚）为主 + HD-FEC 3.8e-3（跨候选可比）补充

### 工作点一致性核查

| 来源 | 工作点 | 原文依据 |
|---|---|---|
| B5 锚 | BER 1e-3 | L149 "the BER of 1 × 10⁻³ can be obtained at a receiver sensitivity of −48 dBm" |
| sat.1553 | BER 1e-3 | L353 "SNR penalty... relative to a perfectly synchronized system" @ BER 10⁻³ |
| [60] Leven | BER 1e-3 | L121 "Required OSNR for a BER of 1e−3" |
| NDA-ML/B7/B2（跨候选）| HD-FEC 3.8e-3 | sat.1553 L440 + D005 会议门槛 + 跨候选统一叙事 |

### 决策：双工作点报告

- **BER 1e-3**（主工作点）：B5 锚 + sat.1553 + [60] Leven 三者一致，跟锚论文对口
- **HD-FEC 3.8e-3**（跨候选可比补充）：跟 NDA-ML/B7/B2 对齐（B7Params 已用 HD-FEC），sat.1553 L440 也提 HD-FEC

**理由**：B5 锚论文工作点是 BER 1e-3，复现 B5 必须报 BER 1e-3。但跨候选可比需 HD-FEC（D005 务实路线会议门槛 + 跨候选统一叙事）。双工作点不冲突，sandbox 同时报两个。

## 0.4.4 LEO Doppler 主题差异化：B5 / B7 / B4 三种正交解法

### 三候选机制辨析（基于已读全文）

| 候选 | 锚方法 | 机制层 | 估计域 | 范围 | 增量维度 |
|---|---|---|---|---|---|
| **B5** | 分块 FFT + 正负功率谱面积比 Rp-n + 星历预测调 LO | **算法层**（频域谱分析）| **频域功率比**（积分量）| ±4.5GHz（15×）| 范围扩展 + 鲁棒性 |
| **B7** | Gardner TED 复用 FOE | **算法层**（定时域）| **定时域 TED 增益**（周期相关）| 0-23GHz 需扫频（1.9× 精估）| 0.6dB OSNR + 范围 1.9× |
| **B4** | 双反馈环（外环大动态 + 内环小动态）| **架构层**（双环结构）| **环路反馈**（PADE + V-V）| ±920MHz（~3×）| MSE 4× 改善 + ±920MHz @ 0.5dB |

### 差异化叙事（B5 视角）

- **B5 = 频域功率比粗 CFO**（算法层，盲估无 pilot，不依赖 MIMO DSP）—— 范围 15× 最强，无 dB 增量
- **B7 = 定时域 TED 增益精估**（算法层，Gardner TED 复用 FOE）—— 有 0.6dB OSNR 增量，范围 1.9×
- **B4 = 双反馈环架构**（架构层，外环+内环）—— MSE 4× 改善，范围 ~3×

### 机制正交无撞车（`_B5-...-increment.md:161` 确认）

- B5 频域功率比 ≠ B7 定时域 TED（估计域不同，频域积分量 vs 定时域周期相关）
- B5 频域功率比 ≠ B4 双环架构（B5 是单环前馈，B4 是双环反馈）
- **三个候选是 LEO Doppler 大动态的三种正交解法**（频域粗估 / 定时域精估 / 双环架构），可作大论文跨章节统一叙事

**叙事定位**（大论文章节级）：
- B5 章节：LEO Doppler 全量程粗捕获（频域功率比，范围 15×）
- B7 章节：LEO Doppler 精估计（定时域 TED，0.6dB OSNR）
- B4 章节：LEO Doppler 双环架构（外环大动态 + 内环小动态）
- 三章节统一叙事 = "LEO Doppler 大动态载波同步的三层解法（频域粗估 / 定时域精估 / 双环架构）"

## 对 sandbox/MVE 的影响

- **sandbox 三方对照**（sim-preflight V2/C7）：B5 短时谱 / 传统 FFT FOE / [60] Leven Mth-power，三方法都做前馈归一化 + 共用信道 + 双工作点
- **fair gain 二维报告**：范围扩展表 + 残频/BER 对比表
- **[60] Leven 需新写**（common 没有，作祖师爷对照）——sandbox 时实现，MVE 通过才转正进 common
- **路径 B 补 dB**（S002 §0.1c 路径 B）：sandbox 若发现 B5 vs [60] Leven 有 dB 增量则叠加够格，若无则靠路径 C/A（范围扩展 + 绝对指标）

## 来源

- S003（本轮工作对话）+ S002（阶段 0.1-0.2 溯源）
- B5 锚 content.md L57（粗 CFO 定义）/ L149（BER 1e-3 −48dBm）/ L147（56MHz/s + ≥9GHz 锁定）
- [60] Leven content.md L9（prior to block PE）/ L121（BER 1e-3）/ L123（7dB penalty 无 FE）/ L157（OSNR <9dB）
- sat.1553 content.md L353（SNR penalty vs 完美同步）/ L440（HD-FEC）/ L548-559（粗补偿即可）
- `common/_recovery.py:37`（fft_foe 主 baseline）
- `sc_nda_ml_sim.py:137`（fft_foe_m0_omega 备选 baseline）
- `_B5-short-time-spectrum-cfo-increment.md:161`（B5 vs B7 机制辨析）
- B7 S004 D004+D005（B7Params fair gain 二维报告模式参考）
- INVARIANT 14（topic-index，LEO Doppler 主题差异化）+ D005 务实路线 + FR-25 Go/Kill 标准分离
