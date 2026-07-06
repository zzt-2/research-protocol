# OFDM 基建适配性评估 — common 单载波时域 vs B11 OFDM 频域 ML

> 评估报告 | 评估日期: 2026-07-06 | 任务: 评估现有 common 基建（单载波时域）复现 B11（OFDM 频域 ML）+2dB 的差距
> 不修代码（纪律 1）| TL-26 行号溯源（纪律 2）| 不替主线拍板（纪律 3）| 不臆测（纪律 4）

## 0. 结论速览（TL;DR）

**common 现有单载波时域基建不能等价复现 B11 的 +2dB，根因是架构性差异（频域 ML + OFDM 帧结构循环移位性质），非 bug。** 上一轮诊断修了 nda_ml_recovery 两个 bug 后 NDA-ML fixed 仍输 DA 0.59 dB（`_awgn_repro_results.json` 行 85），这个 0.59 dB **不是实现 bug，是架构错配**：

1. **B11 NDA-ML 是频域 ML**（R(k)^M₀，k=子载波，content.md 行 75），common 是时域 ML（r(n)^M₀，`_recovery.py` 行 194）。**数学不等价**（见 §3.2）。
2. **B11 STO 估计依赖 OFDM 帧循环移位性质**（content.md 行 37/49/63），单载波没这个性质，common 已显式置 tau_est=0（`_recovery.py` 行 222）—— **STO 维度整个丢失**。
3. **DA ML baseline 信息量不对等**：common 的 DA ML 用真发送符号等距 pilot（"理想 DA"，`_awgn_repro_diagnostic.py` 行 152-154），B11 DA ML 是 decision-feedback（content.md 行 181 "decision errors and error propagation"）。**common 的 DA 太强（近 oracle 18.10 vs 17.83 dB），人为压扁了 NDA 的相对增益空间**。

**推荐方案 C**（B11 作频域 ML 参考，单载波做时域 NDA-ML 改进，不直接对标 +2dB），理由：补 OFDM 基建成本（3-4 子 agent）换的是"复现已发表顶刊 baseline"，按用户拍板"B11 是 baseline 复现对象"——但 baseline 复现的价值是建立可信对标，而非自证增量；若主线目标仍是星地湍流迁移增量，单载波时域 NDA-ML 改进更贴近实际链路（单载波在 FSO 湍流幅度衰落下的星座判决鲁棒性 ≠ OFDM）。最终方案由主线 + 用户拍板。

---

## 1. B11 仿真链分析（频域 ML + OFDM 帧结构）

### 1.1 仿真链（content.md 行 155）

```
PRBS(2^15−1) → M-APSK 映射 → N=256 并行子载波 → IFFT(DFT 256) → 加 CP(32) → 加 Wiener PN + AWGN
→ 去 CP → FFT → 频域 R(k) → 升 M₀ 次幂去调制 → 单正弦 ML 闭式估 (τ̂, φ̂) → 补偿
```

- **DFT size N=256，CP=32 sample，25 GBaud**（content.md 行 155）
- **调制**：(8,8)-16APSK（K=2 环，M₀=8 点/环，M=16）/ (4,4)-8APSK / (4,4,4,4)-16APSK（行 155）
- **信道**：纯 AWGN + 激光线宽 Wiener PN（σp²=2π·Δν·Ts，行 51）；**湍流/指向/Doppler/CFO 假设已补偿**（行 33，_read_notes 行 9/12）
- **PN 频域分解**：DFT 后 PN 分 CPE（常相位 Φ(0)）+ ICI（行 53-57）；σp²→0 时 ICI≈AWGN，本文聚焦 CPE（行 57）

### 1.2 频域 ML 核心数学（content.md 行 75-127）

1. **升 M₀ 次幂去调制**（行 75-77）：对接收**频谱** R(k) 升 M₀ 次幂。M-APSK 每环 M₀ 点，M₀·ξ(k) 是 2π 整数倍 → 调制相位消零（行 77）
2. **化简为单正弦**（行 77-81）：升幂后 y(k) 的相位 = M₀(φ + 2πτk/N)，**k 是子载波索引，τ 是 STO**。这是"单复正弦的频率（∝τ）+ 相位（∝φ）"问题
3. **Wang[13] 单正弦 ML 闭式解**（行 103-121，Eq.12-14）：凸二次似然函数最小化 → τ̂、φ̂ 闭式表达式
4. **仅用第一个 OFDM 符号估 STO**（行 127），再逐符号估 CPE（行 123，Eq.16）
5. **genie-aided 相位解卷绕**（行 129-131，Table I）：用真实相位调整 ψ(k) 到 M₀(φ+2πτk/N)±π——**非可实现**（_read_notes 行 17/62）

### 1.3 B11 帧结构（STO 估计的关键前提）

- **前两个连续 OFDM 符号相同，不插 CP**（content.md 行 37/49，Fig.1）
- **循环移位性质**（行 63）：若 STO τ∈[0,N−1]，则前 N 个样本是原始发射前 N 样本的**循环移位**（circularly shifted）
- **频域对应**：时域循环移位 τ ↔ 频域线性相位 e^{j2πτk/N}（DFT 循环移位定理）→ ML 可把 STO 估成单正弦的"频率"
- **STO 估计精度**：prob 1 @ −10 dB SNR 高 CLW（行 183）—— **直接依赖循环移位性质**

---

## 2. common 现有基建差距（单载波时域 vs OFDM 频域）

### 2.1 信道基建（`_channel.py`）

- `generate_shared_realization_apsk`（行 60-124）：**单载波时域**，`signal = tx * sqrt(h) * carrier`（行 113），无 IFFT/FFT、无 CP、无子载波映射
- 调制 `m16apsk_mod`（`_modulation.py` 行 175）：直接产 (8,8)-16APSK 星座点序列，**逐符号时域采样**，非频域子载波
- **缺**：OFDM 调制（IFFT + CP 插入）、OFDM 解调（FFT + CP 移除）、频域子载波映射、B11 帧结构（前两符号相同不插 CP）

### 2.2 恢复基建（`_recovery.py`）

- `nda_ml_recovery`（行 171-224）：**时域升 M₀ 次幂**（`raised = rx ** M0`，行 194），FFT 找的是 **M₀·Δf（频率偏置）**（行 198-211），**不是 STO**
- **STO 显式置 0**（行 222 注释）："STO 在 B11 OFDM 频域线性相位模型; 单载波时序此处不分离, 标 0"——**已自承架构错配**
- `da_ml_recovery`（行 136-168）：用真发送符号 pilot，线性回归 (φ, Δf)，**无 decision feedback**（"理想 DA"形式）

### 2.3 上一轮诊断结果（`_awgn_repro_results.json`）

| 方案 | SNR @ HD-FEC (dB) | vs DA | vs oracle |
|------|-------------------|------|-----------|
| DA ML | 18.10 | — | +0.27 |
| NDA-ML fixed（修 FFT-df bug） | 18.70 | **−0.59（输 DA）** | +0.87 |
| NDA-ML blockwise（现 nda_ml_recovery） | 20.00 | −1.90 | +2.17 |
| oracle | 17.83 | — | — |

（行 82-101）DA ML 近 oracle 仅 0.27 dB → **DA 在单载波时域下被人为加强到近最优**，压扁了 NDA 的增益空间。

---

## 3. 四个问题的回答（附 B11 行号 + 技术依据）

### 3.1 Q1：B11 NDA-ML 是频域 ML 还是时域 ML？

**频域 ML。** 直接依据：

- content.md **行 75**："we firstly remove the modulated phase by raising **R(k)** to the M₀-th power"——R(k) 是接收**频谱**（DFT 后，行 53 "After performing the N-point DFT, ... The received data R(k) on the k-th subcarrier"）
- content.md **行 77**：升幂后相位 = M₀(φ + 2πτk/N)，**k 是子载波索引**（行 53 "k = 0,1,...,N−1"）
- content.md **行 29**（摘要）："By utilizing the phase information from **received spectrum data**"
- _read_notes **行 10**："把接收频谱 R(k) 升 M₀ 次幂去调制相位"
- content.md **行 159**："uses the entire OFDM symbol for CPE estimation"——整个 OFDM 符号 = 频域 N=256 子载波

**时域 vs 频域的根本区别**：B11 在 DFT **之后**（频域 R(k)）升 M₀ 次幂；common 在 DFT **之前**（时域 r(n)）升 M₀ 次幂。

### 3.2 Q2：单载波时域升 M₀ 次幂能否等价复现频域升 M₀ 次幂？（数学推导）

**不能等价。** 数学依据：

**频域（B11）**：DFT 后慢 PN 坍缩为 CPE（行 57，σp²→0 时 ICI≈0）：
$$R(k) \approx X(k) \cdot e^{j\phi_{CPE}} \cdot e^{j 2\pi\tau k/N} + W(k)$$
升 M₀：$R(k)^{M_0} = |X(k)|^{M_0} e^{j M_0(\phi_{CPE} + 2\pi\tau k/N)} + \text{升幂噪声}$ → **k 的线性相位单正弦**（频率 ∝τ，相位 ∝φ），Wang[13] ML 闭式解 τ̂/φ̂（行 103-121）。

**时域（common）**：$r(n) = x(n) e^{j\theta(n)} + w(n)$，θ(n) 是逐样本 Wiener（行 51）。升 M₀：$r(n)^{M_0} = |x(n)|^{M_0} e^{j M_0 \theta(n)} + \text{升幂噪声}$。

**三处不等价**：
1. **PN 模型**：频域升幂对慢变 CPE（每 OFDM 符号一个常相位）做；时域升幂对逐样本 Wiener θ(n) 做——升 M₀ 把 Wiener 方差放 M₀² 倍（行 85 Σ_{M₀ε}=M₀²Σ_ε），**时域升幂噪声放大更严重**。
2. **STO 表达**：频域 STO = 子载波 k 上的线性相位斜率 2πτk/N（行 63/77，DFT 循环移位定理）；时域 STO = 整数采样偏移 → **索引移位**（x(n)→x(n−τ)），**不是乘性相位斜率**，升 M₀ 后无法形成"频率∝τ"的单正弦。common `nda_ml_recovery` 行 198 的 FFT 找的是 M₀·Δf（频偏），**不是 STO**。
3. **处理增益**：频域 R(k) 有 DFT 的 N=256 点处理增益（ICI/AWGN 在子载波上平均）；时域 r(n) 逐样本升幂无处理增益。

**一句话**：频域升 M₀ 把整数 STO τ 转成子载波线性相位（可 ML 估），时域升 M₀ 做不到（整数 STO 是索引移位非相位）；且时域升 M₀ 对逐样本 Wiener PN 放大 M₀² 倍，频域升 M₀ 对坍缩后的 CPE 放大——**架构性不等价，非参数调优可弥合**。

### 3.3 Q3：B11 STO 估计需要 OFDM 帧结构，单载波缺失影响 +2dB 复现吗？

**显著影响，STO 维度整个丢失。** 依据：

- B11 STO 估计依赖"前两 OFDM 符号相同不插 CP"（content.md 行 37/49）→ 循环移位性质（行 63）→ 频域线性相位 2πτk/N（行 77）→ ML 闭式 τ̂（行 103-121）
- common `nda_ml_recovery` 行 222 **显式置 tau_est=0**，注释自承"STO 在 B11 OFDM 频域线性相位模型; 单载波时序此处不分离"
- B11 +2dB 的核心卖点之一是**联合 STO+CPE 估计**（行 29 "jointly estimate the STO and CPE"），STO 精度 prob 1 @ −10 dB SNR（行 183）。单载波下 STO=0 → NDA-ML **退化为纯 CPE 估计**，丢掉了联合估计的相对优势
- **+2dB 的构成**：B11 vs DA ML 的增益来自 (a) STO 估计（DA ML 无 STO 能力，PA[8] 也无，行 185）+ (b) 全 OFDM 符号 CPE 估计 vs DA decision-feedback 错误传播（行 181）。单载波下 (a) 整个丢失，(b) 也失真（见 Q4）

### 3.4 Q4：DA ML 在 OFDM vs 单载波下信息量差异（为什么单载波 DA 近最优）

**信息量 + 结构双重不对等，common 的 DA 被人为加强到近 oracle。** 依据：

| 维度 | B11 DA ML [10] | common da_ml_recovery |
|------|----------------|----------------------|
| 数据来源 | **decision-feedback**（行 27/181，Cao 2012 "decision-aided, pilot-aided, decision-feedback"） | **真发送符号 pilot**（`_awgn_repro_diagnostic.py` 行 152-154 "无决策错误传播 — 理想 DA 形式"） |
| 错误传播 | **有**（行 181 "decision errors and error propagation"，(8,8)-16APSK 高密度下敏感） | **无**（用 tx 真 pilot） |
| pilot 密度 | 单 pilot 符号启动 + decision feedback 覆盖全 OFDM 符号 | 等距 spacing=4（`_awgn_repro_diagnostic.py` 行 73/164），每 256-sample 块 64 个真 pilot |
| 相位模型 | 每 OFDM 符号一个 CPE（频域坍缩） | 块内线性 (φ, Δf) 回归（`_recovery.py` 行 154-161） |

**结果**：common DA ML = 18.10 dB，oracle = 17.83 dB，**DA 距 oracle 仅 0.27 dB**（`_awgn_repro_results.json` 行 82-84）→ DA 已近信息论最优。而 B11 DA ML 在 (8,8)-16APSK @ 200 kHz CLW 下因 decision-feedback 错误传播显著退化（行 181），才给 NDA-ML 留出 +2dB 空间。

**这是 +2dB 复现不来的直接原因之一**：common 的 DA baseline 用真 pilot（无错误传播）+ 密集 spacing（信息量足），人为把 DA 抬到近最优；B11 的 DA 是 decision-feedback（有错误传播），在密集星座下弱。**baseline 不对等，gain 自然不对等。**

### 3.5 Q5：补 OFDM 基建工作量估算（子 agent 数）

需补的组件：

| 组件 | 内容 | 复用 | 子 agent |
|------|------|------|---------|
| OFDM 调制/解调 | IFFT(DFT 256) + CP(32) 插入/移除 + M-APSK 频域子载波映射 | `m16apsk_mod` 星座点可复用 | 1 个（~15 min） |
| B11 帧结构 | 前两 OFDM 符号相同不插 CP（content.md 行 37/49）+ Gamma-Gamma/Wiener 信道复用 | `generate_shared_realization_apsk` 信道可复用 | 同上 |
| 频域 ML 估计器 | R(k)^M₀ + 相位解卷绕 + Wang[13] 单正弦 ML 闭式 τ̂/φ̂（Eq.12-16） | `nda_ml_recovery` 的 FFT-df/线性回归逻辑可借鉴 | 1 个（~15 min） |
| DA ML[10] baseline | decision-feedback 相位估计（单 pilot 启动 + 全符号判决反馈） | 现无，需新写 | 1 个（~15 min） |
| PA[8] baseline | 频域 pilot subcarrier CPE 估计 | 现无，需新写 | 同上 |
| AWGN 复现测试 | 目标：NDA-ML vs DA-ML = +2dB @ (8,8)-16APSK @ HD-FEC | `_awgn_repro_diagnostic.py` 框架可复用 | 1 个（~15 min） |

**估算：3-4 个子 agent，串行 ~45-60 min**（OFDM 基建 1 + 频域 ML 1 + DA/PA baseline + 复现测试 1，可选调优 1）。

**风险点**：
- genie-aided 解卷绕（行 129-131）非可实现，复现需用实际解卷绕（可能拿不到 +2dB，因为 B11 Fig.2 低 SNR 段 MSE<CRLB 部分由 genie-aided 致，行 157 自承）
- +2dB 仅 (8,8)-16APSK 成立（行 181），(4,4)-8APSK/(4,4,4,4)-16APSK 下 DA=B11——复现需精确选 (8,8)-16APSK + 合适 CLW（行 181 "200 kHz CLW"）

---

## 4. 三方案代价/收益/风险矩阵

| 方案 | 代价 | 收益 | 风险 |
|------|------|------|------|
| **A. 补 OFDM 基建，复现 B11 +2dB，再做湍流迁移增量** | 3-4 子 agent（~60 min）补 OFDM 调制解调 + 频域 ML + DA/PA baseline；后续湍流迁移再加 1-2 子 agent | 严格对标顶刊 baseline，复现 +2dB 建立可信对标；湍流迁移增量（Q2/Q3）有 B11 频域 ML 母体支撑 | genie-aided 解卷绕非可实现，实际解卷绕可能拿不到 +2dB；OFDM 在 FSO 湍流幅度衰落下的 PAPR/ICI 问题可能与星地实际链路（常单载波）脱节；复现成本高但增量价值取决于主线是否真做 OFDM 星地 |
| **B. 放弃 B11，换单载波时域 baseline（如 B7 Gardner TED）** | 0（B7 已有 `gardner_ted_recovery`，`_recovery.py` 行 227） | 单载波时域与星地 FSO 实际链路一致；B7 Gardner TED 是经典定时恢复 baseline，基建已就绪；无架构错配 | 放弃 B11 频域 ML 赛道（与 B4/B6/B7/B10 重新定位）；若主线目标含 OFDM/频域 ML 维度则丢失；B7 增量空间需重新论证（Gardner TED 已成熟） |
| **C. B11 作"频域 ML 参考"，单载波做时域 NDA-ML 改进（不直接对标 +2dB）** | 0-1 子 agent（文献定位 + 时域 NDA-ML 改进方向论证） | 诚实承认架构差异，不强行对标；时域 NDA-ML 在单载波 FSO 下有实际意义（与星地链路一致）；保留 B11 频域 ML 作理论参考（升 M₀ 次幂 + 单正弦 ML 框架可借鉴到时域） | 增量 dB 需重新锚定（不能引用 B11 +2dB）；需找新的单载波时域 baseline 对标；若审稿人期待 OFDM 频域 ML 对标则被动 |

---

## 5. 推荐方案（给主线决策依据，不替主线拍板）

**推荐方案 C**（B11 作频域 ML 参考，单载波做时域 NDA-ML 改进），理由：

1. **架构诚实**：B11 是 OFDM 频域 ML，common 是单载波时域，强行补 OFDM 基建复现 +2dB 是"为复现而复现"——按用户拍板"B11 是 baseline 复现对象"，baseline 复现的价值是建立可信对标，但**对标的前提是架构一致**；单载波链路对标 OFDM 频域 ML 的 +2dB，即使复现了也不构成单载波场景的增量依据。
2. **星地实际链路**：FSO 星地链路常采用单载波（如 DQPSK/OQPSK）或单载波频域均衡（SC-FDE），纯 OFDM 因 PAPR/ICI 在湍流下未必占优。单载波时域 NDA-ML 改进更贴近实际。
3. **成本效益**：方案 C 成本最低（0-1 子 agent），且不丢失 B11 的理论贡献（升 M₀ 次幂 + 单正弦 ML 框架可迁移到时域）；方案 A 成本高（3-4 子 agent）且复现价值受 genie-aided 解卷绕限制。
4. **方案 B 是 C 的退路**：若时域 NDA-ML 改进方向论证不出增量空间，可退到方案 B（B7 Gardner TED）。

**若主线目标是 OFDM 星地系统**（如未来 feeder link 用 OFDM），则方案 A 合理——但需主线明确这个方向，本评估不替主线拍板。

**关键不确定性（留给主线 + 用户）**：
- 主线目标链路是单载波还是 OFDM？（决定 A vs B/C）
- B11 +2dB 的复现是否是硬性 milestone？（决定是否值得 3-4 子 agent 成本）
- 是否接受"B11 作理论参考，不直接对标 +2dB"的学术定位？（决定 C 的论文叙事）

---

## 附：行号溯源核对表（纪律 2/4）

| 声明 | B11 行号 | 核实状态 |
|------|---------|---------|
| 频域 ML（R(k)^M₀） | content.md 行 29/53/75/77/159 | ✓ grep 核实 |
| DFT 256 + CP 32 + 25 GBaud | content.md 行 155 | ✓ |
| Wiener PN σp²=2π·Δν·Ts | content.md 行 51 | ✓ |
| 前两 OFDM 符号相同不插 CP | content.md 行 37/49 | ✓ |
| 循环移位性质（STO 估计前提） | content.md 行 63 | ✓ |
| 升 M₀ 次幂去调制（M₀ξ(k)=2π 整数倍） | content.md 行 75-77 | ✓ |
| Wang[13] 单正弦 ML 闭式 τ̂/φ̂ | content.md 行 103-121 | ✓ |
| 仅第一 OFDM 符号估 STO，逐符号估 CPE | content.md 行 123/127 | ✓ |
| genie-aided 相位解卷绕（非可实现） | content.md 行 129-131 | ✓ |
| +2dB SNR gain @ (8,8)-16APSK @ HD-FEC | content.md 行 181/191 | ✓（双处一致） |
| DA ML decision-feedback 错误传播 | content.md 行 181 | ✓ |
| (4,4)-8APSK/(4,4,4,4)-16APSK 下 DA=B11 | content.md 行 181 | ✓ |
| STO prob 1 @ −10 dB SNR | content.md 行 183 | ✓ |
| DA ML [10] = Cao 2012 decision-aided pilot-aided | content.md 行 27/213 | ✓ |
| common nda_ml_recovery 时域升 M₀ | `_recovery.py` 行 194 | ✓ |
| common nda_ml_recovery STO 置 0 | `_recovery.py` 行 222 | ✓ |
| common da_ml_recovery 真 pilot（理想 DA） | `_awgn_repro_diagnostic.py` 行 152-154 | ✓ |
| 上一轮诊断 gain NDA-fixed vs DA = −0.59 dB | `_awgn_repro_results.json` 行 85 | ✓ |
| common DA vs oracle = 0.27 dB | `_awgn_repro_results.json` 行 82-84 | ✓ |

---

*评估完成。不修代码（纪律 1）。行号均 grep 核实（纪律 2/4）。三方案 + 推荐供主线 + 用户决策（纪律 3）。*
