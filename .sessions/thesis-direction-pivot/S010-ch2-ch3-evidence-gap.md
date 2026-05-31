# [S010] Ch2/Ch3 证据缺口补充检索

> 2026-05-30 | 逐章深入论证 | 完成（含修正）
> 产出: PROMPT-023 定向检索 → 后续物理传导链分析 + 假空白检查 + 负面证据搜索

## 目标

S008 A0 检查发现 Ch2/Ch3 存在**场景外推**问题：核心实证数据不是在目标场景（LEO 星地 SP-QPSK）下获得的。本检索旨在判断是否遗漏了更匹配目标场景的文献。

## Ch2 补充检索

### 检索概况

3 个方向、11 组关键词，共 11 个 search JSON。

### 方向1：QPSK FSO 信道估计

| 关键词组 | 高相关论文 |
|---------|-----------|
| "QPSK channel estimation FSO" | 2026 CNN+BiLSTM FSO CE（超越 LS/LMMSE/EKF） |
| "SP-QPSK coherent FSO receiver" | 2024 OL QPSK MDM湍流(c=7); 2024 BPSK/QPSK自适应FSO(c=7) |
| "QPSK pilot-free CE optical" | 2025 VAE pilot-free UAV-FSO |

**关键发现**：
- **未找到任何"SP-QPSK + FSO + CE"的论文**。SP-QPSK 在 FSO 领域几乎没有独立工作，更多用于光纤相干通信
- 2024 OL 实验验证 QPSK+pilot+FSO 自相干接收，证明 QPSK FSO 是活跃研究线
- 2024 Photonics 实验验证 BPSK/QPSK 自适应切换相干 FSO，QPSK 比 BPSK 有 3-4dB 功率代价

### 方向2：DL 信道估计架构进展（2023-2026）

| 论文 | 年份 | 引用 | 架构 | 场景 |
|------|------|------|------|------|
| Symbol Detection & CE for SOC (IEEE TMLCN) | 2024 | 16 | NN+AE | Gamma-Gamma, LEO 下行 |
| Joint estimation FSO CNN (Applied Optics) | 2024 | 3 | CNN | FSO 湍流+检测噪声联合 |
| FSO CE DNN/CNN/RNN 对比 | 2023 | 2 | DNN/CNN/RNN | FSO 通用（DNN 最优） |
| FSO turbulent CE CNN+BiLSTM | 2026 | 0 | CNN+BiLSTM | FSO 湍流 |
| Pilot-free UAV-FSO VAE | 2025 | 1 | VAE | UAV-FSO, IM/DD |
| Clustering-assisted CE FSO satellite | 2026 | 2 | Clustering+LS+GMM | FSO LEO, 4/16/64-QAM |

**关键发现**：
- **2024 TMLCN (c=16) 最强匹配**：直接在 Gamma-Gamma 衰落 + LEO-地面链路做 NN 信道估计，对比 MMSE。可作为 Ch2 核心引用
- 架构演进：MLP → CNN → CNN+BiLSTM/VAE。确实有比 MLP 更新的架构用于 FSO CE，但尚无 Transformer
- 所有论文均未指定 SP-QPSK 调制格式

### 方向3：无导频/盲信道估计 FSO

| 论文 | 年份 | 引用 | 方法 | 信号 |
|------|------|------|------|------|
| Blind Estimation Timing/Attenuation/Noise (TCOMM) | 2024 | 1 | EM/ECM | OOK 格式，非 QPSK；盲估计接近 CRB |
| Moment-Based GG Fading Parameter Estimation (JSAC) | 2025 | 10 | 矩估计 | 估计 GG 参数(α,β)，非信道系数 |
| Pilot-free UAV-FSO VAE | 2025 | 1 | VAE | IM/DD, M=16, 非 QPSK |

**关键发现**：
- 盲 CE 在 FSO 存在但主要针对 OOK，无 QPSK 证据
- Pilot-free 在 IM/DD 下已有 DL 方案（VAE），但不可直接迁移到相干 QPSK
- **无负面证据**（无"pilot-free 在 QPSK 下不 work"的论文），也无正面证据

### Ch2 A0-1 状态更新

- **检索前**：[外推]（Amirabadi 16-QAM → SP-QPSK，1 篇支撑）
- **检索后**：**仍为 [外推]，但支撑从 1 篇增强到 4-5 篇**
  - 2024 TMLCN (c=16)：GG 湍流 + NN CE + LEO，证明 NN CE 接近 MMSE
  - 2026 CNN+BiLSTM：超越 LS/LMMSE/EKF
  - 2024 OL/Photonics：QPSK FSO 实验验证可行性
  - 但 SP-QPSK + FSO + DL CE 精确交叉点仍是空白

### Ch2 新风险

1. **SP-QPSK 在 FSO 的合理性**：该术语几乎不用于 FSO 领域。建议论文中考虑弱化"SP-QPSK"特殊性，改为"QPSK"或明确说明选择理由
2. **MLP 架构过时风险**：2025-2026 已有 VAE、CNN+BiLSTM 用于 FSO CE，Ch2 如用 MLP 需论证（如计算复杂度、实时性）
3. **Pilot-free 在相干检测下的空白**：所有 pilot-free CE 工作都在 IM/DD 下，相干检测下 pilot-free 未验证

## Ch3 补充检索

### 检索概况

3 个方向、12 组关键词，共 12 个 search JSON。

### 方向1：LEO/卫星 FSO 功率控制

| 论文 | 年份 | 引用 | 匹配度 | 核心发现 |
|------|------|------|--------|---------|
| **Seifi & LoPresti, Beam Power Optimization FSO Using RL+SLM** | 2026 | — | 高 | TD3+SLM 优化 FSO 光束功率，面向 LEO 光学链路 |
| **Carrillo-Flores & Giggenbach, Received Power Statistics for Optical LEO Uplinks** | 2025 | — | 高 | LEO 光学上行链路接收功率时间序列统计，不同仰角衰落特性 |
| **Cheng et al., Simulated 1000km LEO using 1.8km OWC** | 2025 | 10 | **极高** | 1.8km 地面链路模拟 1000km LEO，EDFA+MEMS，**缩比方法论先例** |

### 方向2：FSO 功率预补偿/预加重

| 论文 | 年份 | 引用 | 匹配度 | 核心发现 |
|------|------|------|--------|---------|
| **Correia et al., Reciprocity-Driven Power Adaptation (JLT)** | 2026 | — | **极高** | EDFA APC 自适应光功率预补偿实验验证，上游 Rytov 方差降低 2 个数量级，可靠性约 90% |
| **Nguyen et al., Adaptive Rate/Power Control with ML Channel Prediction (IEEE TAES)** | 2024 | 5 | **极高** | FSO 卫星系统自适应速率/功率控制，ESN 预测信道解决长距离高延迟 CSI 过时问题 |
| **Brandao et al., 100G FSO field trial with LoRa feedback (JOCN)** | 2024 | — | 已有 | Ch3 已有文献，1.8km 地面链路，LoRa 反馈实现功率预补偿 |

### 方向3：LEO FSO 链路预算与自适应

| 论文 | 年份 | 引用 | 匹配度 | 核心发现 |
|------|------|------|--------|---------|
| **Lognone et al., Pre-compensation Phase for GEO Feeder Uplinks (SPIE)** | 2023 | — | **极高** | GEO 上行预补偿相位优化，MMSE 方法链路裕度 +15dB。GEO→LEO 方法论可迁移 |
| **Link budget analysis bi-directional LEO/GEO optical (Nature Sci Rep)** | 2024 | — | 高 | LEO+GEO 双向光学链路预算，改进 beam wander 模型 |
| **Kotake et al., Adaptive Optical Satellite Network (AOSN)** | 2022 | 31 | 高 | 自适应光学卫星网络链路预算设计，调制/速率/功率多维度适配 |

### Ch3 A0-1 状态更新

- **检索前**：[外推]（地面 1.8km → LEO 星地）
- **检索后**：**升级为 [部分实证]**
  - Cheng 2025：地面短距模拟 LEO 长距有文献先例
  - Correia 2026：功率预补偿有实验实证（地面 FSO）
  - Nguyen 2024：卫星 FSO 自适应功率控制有仿真验证
  - Lognone 2023：卫星上行预补偿有工程验证（GEO）
  - 四者组合：Ch3 的"地面预补偿→LEO 外推"从纯外推升级为有间接实证支撑

### Ch3 反馈延迟风险评估

Nguyen 2024 (IEEE TAES) 明确指出：
- 长距离/高延迟卫星链路导致 CSI 过时是实际问题
- 但可通过 ML 信道预测（ESN）有效克服
- **Ch3 反馈延迟不是致命问题，但须配合信道预测机制**

### Ch3 新风险

无明显致命信号。未找到"LEO 反馈延迟导致预补偿不可行"的负面证据。

## 总结（初版）

### 证据强度变化

| 章 | 检索前 | 检索后 | 变化原因 |
|---|--------|--------|---------|
| Ch2 | [外推] 1篇支撑 | [外推] 4-5篇支撑 | 2024 TMLCN+2026 CNN+BiLSTM+QPSK FSO 实验，但 SP-QPSK 精确交叉仍空白 |
| Ch3 | [外推] 地面→LEO | [部分实证] | Correia 2026预补偿实验 + Nguyen 2024卫星功率控制 + Cheng 2025缩比方法论 + Lognone 2023 GEO预补偿 |

### 建议下载优先级

| 优先级 | 论文 | DOI / 来源 | 理由 |
|--------|------|-----------|------|
| P0 | Nguyen 2024 (IEEE TAES) | 10.1109/taes.2024.3403809 | 直接解决 Ch3 反馈延迟核心关切 |
| P0 | Correia 2026 (JLT) | 10.1109/JLT.2025.3640945 | 功率预补偿最新实验验证 |
| P1 | 2024 TMLCN NN CE | 待查 | Ch2 最强匹配，GG+NN CE+LEO |
| P1 | Cheng 2025 | 待查 | 缩比方法论先例 |
| P2 | Lognone 2023 (SPIE) | 10.1117/12.2648898 | GEO 预补偿工程可行性 |
| P2 | Carrillo-Flores 2025 | 10.1002/sat.1554 | LEO 功率时间序列统计 |

### 是否需要更新 S008

**是，建议局部更新**：
1. Ch3 A0-1 从 [外推] → [部分实证]，需补充 Nguyen 2024 + Correia 2026 + Cheng 2025 证据
2. Ch2 A0-1 保持 [外推]，但支撑文献数量从 1 → 4-5 需补充
3. 新增风险项：SP-QPSK 合理性、MLP 过时风险

### 搜索存档

所有搜索 JSON 保存在 `search-archive/2026-05-30/`，共 23 个文件（Ch2: 11, Ch3: 12）。

---

## 修正：物理传导链分析 + 假空白检查 + 负面证据

> 以下内容基于初版 S010 的三维度补充审查，参照 S009 的"假空白"分析范式。

### 一、物理传导链分析（7 篇论文逐篇适用性检查）

| # | 论文 | 适用性 | 关键发现 |
|---|------|--------|---------|
| 1 | Elfiky 2024 (TMLCN, c=16) | **条件适用** | GG+LEO 匹配，但 AE 端到端≠SP-QPSK；未直接对比 DL vs LS/MMSE，以 MMSE 为参考基准声称 NN CE≈MMSE |
| 2 | Mohammed 2026 (CNN+BiLSTM) | **条件适用** | GG 匹配，但疑似 IM/DD 非相干检测；低 IF 期刊 c=0 |
| 3 | Zhou 2024 (OL, c=7) | **不适用** | 自相干检测 ≠ 相干检测，pilot 直接消除了信道估计问题 |
| 4 | Chen 2024 (Photonics, c=7) | **不适用** | BPSK/QPSK 切换硬件设计，无 CE 内容 |
| 5 | **Correia 2026 (JLT)** | **不适用（核心机制不可迁移）** | 依赖双向互易性→LEO 单向下行不成立；R013 已确认严格互易性不成立；EDFA APC 方法论可参考但性能上限不可迁移 |
| 6 | **Nguyen 2024 (IEEE TAES)** | **直接适用** | 卫星 FSO+GG+延迟+自适应功率；但结论是传统方法因延迟**不够**，需 ML 预测 |
| 7 | **Cheng 2025** | **不适用** | 仅验证几何衰减缩比，未验证湍流统计等效性；PAM4/IM-DD≠SP-QPSK/相干；未涉及反馈延迟 |

**Ch2 有效支撑下调**：从"4-5 篇"修正为 **2-3 篇**（Elfiky 条件适用 + Mohammed 弱正面 + Amirabadi 原有 1 篇。Zhou 和 Chen 不适用）。

**Ch3 证据修正**：
- Correia 2026：从"正面实证"降级为"方法论参考，互易性机制不可迁移"
- Cheng 2025：从"缩比方法论先例"降级为"仅几何衰减参考，不涉及湍流统计和延迟"
- Nguyen 2024：Ch3 最强正面证据，但暗示传统方法在卫星场景增益有限

### 二、假空白检查

| 假空白假设 | 判定 | 理由 |
|-----------|------|------|
| **H1**: SP-QPSK CE 空白是因为 DP-CE 退化特例 | **部分成立** | 数学上 SP-CE 是 DP-CE 的退化（1×1 标量 vs 2×2 矩阵），但无文献显式声明。FSO 领域 SP-QPSK 不在主流路径（要么 DP 要么 IM/DD） |
| **H2**: LEO 功率预补偿空白是因为功率裕度充足 | **不成立** | Giggenbach 2022(c=7)实测 LEO 下行功率闪烁导致深度衰落；Shivkant 2025(c=3)强调概率化链路预算；LEO 真正瓶颈是多因素叠加（湍流+对准+功率），功率是其中之一 |
| **H3**: Pilot-free CE 相干 QPSK 空白是因为已被盲方法覆盖 | **成立（假空白确认）** | CMA 盲均衡 + VV/BPS 盲载波恢复已完全覆盖相干 QPSK 下的"pilot-free"功能，无独立研究价值 |

**关键修正**：
1. Ch2 应弱化"SP-QPSK"特殊性→改为"QPSK"，注明 SP 是 DP 的简化情况
2. Ch3 空白需精确化：不是"功率预补偿方向无人研究"（已有 Seifi/Nguyen/Correia），而是"SP-QPSK + LEO 场景交叉空白"
3. "Pilot-free CE in coherent QPSK"标记为假空白——Ch2 不需要研究此方向

### 三、负面证据搜索

| 方向 | 严重程度 | 核心发现 |
|------|---------|---------|
| 互易性在 LEO 局限 | 一般 | 严格互易性不成立已被 R013 确认；粗粒度功率互易性（衰落趋势相关）仍可用；前瞄角非等晕性是 LEO 特有限制 |
| LEO 功率裕度充足 | 无影响 | 文献普遍将功率视为约束因素，未找到"裕度充足"的证据。相反有大量功率自适应研究 |
| QPSK CE 太简单 | 一般 | 静态 AWGN 下 CE 简单，但湍流动态信道下仍有增益空间（2026 LEO-OFDM CE: 4-QAM 下 3-5dB 改善） |
| **DL CE 泛化性** | **严重** | 3 篇独立论文确认：SNR 范围限制、信道模型失配、移动速度失配均导致 DL CE 性能退化。S010 核心正面证据（2024 TMLCN）训练/测试同分布仿真，不代表跨场景泛化性 |

### 四、修正后总结

#### 证据强度修正

| 章 | 初版判断 | 修正后判断 | 变化 |
|---|---------|-----------|------|
| Ch2 | [外推] 4-5篇支撑 | [外推] 2-3篇支撑 | 有效支撑下调；假空白 H1/H3 部分成立 |
| Ch3 | [部分实证] 信心高 | [部分实证] 信心中 | Correia/Cheng 支撑被撤回；仅 Nguyen 2024 提供直接实证 |

#### Ch3 定位建议微调

- 当前："发射端自适应功率预补偿（反馈驱动）"
- 建议："发射端自适应功率预补偿：反馈驱动 + 延迟影响量化 + 简单预测辅助探索"
- 理由：Nguyen 2024 证实传统反馈驱动增益受延迟限制，Ch3 需正面回应而非回避

#### 新增应对策略

1. **Ch2 泛化性验证**（回应 DL CE 泛化性严重问题）：
   - 设计跨湍流强度（不同仰角→不同 Cn²）的泛化性测试
   - 考虑 MLP vs CNN+BiLSTM 的泛化性权衡（MLP 泛化性可能更好）
   - 可能成为 Ch2 额外贡献点：FSO LEO 场景下 DL CE 泛化性边界分析

2. **Ch2 调制格式策略**：
   - 弱化"SP-QPSK"→ 改为"QPSK"
   - 注明 SP 是 DP 的简化，DP-CE 论文可降维引用

3. **Ch3 互易性措辞**：
   - 区分粗粒度功率互易性（衰落趋势相关，可用）vs 细粒度波前互易性（受限）
   - Correia 定位为"EDFA APC 方法论参考"，不作为 LEO 场景实证

#### 修正后下载优先级

| 优先级 | 论文 | 理由 |
|--------|------|------|
| P0 | Nguyen 2024 (IEEE TAES) | Ch3 唯一直接实证支撑，需精读确认传统方法增益受限程度 |
| P1 | Elfiky 2024 (TMLCN) | Ch2 最强匹配，需确认是否做了 DL vs LS/MMSE 对比 |
| P1 | DL CE 泛化性论文 (Denoising 2023, One-shot 2023) | 回应严重负面证据 |
| P2 | Correia 2026 (JLT) | 方法论参考，不作为实证 |
| P2 | Lognone 2023 (SPIE) | GEO 预补偿工程可行性 |

### 搜索存档（修正版）

`search-archive/2026-05-30/`，共 47 个文件（初版 23 + 物理传导链 0 + 假空白 12 + 负面证据 12）。

## 决策引用

- 无新决策（纯检索+审查任务）

## 范围确认

- 本轮是否在 scope boundary 内：是（PROMPT-023 + 后续审查扩展）

## 后续

1. 下载 P0 论文（Nguyen 2024）并精读——确认传统方法增益受限程度，决定 Ch3 是否需引入预测机制
2. 下载 P1 论文（Elfiky 2024 TMLCN）并精读——确认 DL vs LS/MMSE 对比情况
3. 更新 S008 A0-1 状态：
   - Ch3 维持 [部分实证] 但信心下调为"中"（仅 Nguyen 2024 提供直接支撑）
   - Ch2 维持 [外推]，有效支撑 2-3 篇
   - 新增 DL CE 泛化性为严重风险项
4. Ch2 策略调整：弱化 SP-QPSK → QPSK，增加泛化性验证实验设计
5. Ch3 策略调整：增加延迟影响量化，考虑简单预测辅助
6. Pilot-free CE in coherent QPSK 标记为假空白，Ch2 不研究此方向
