# PROMPT-018 研究报告：Q-DP3 维度 A 竞争分解

> 日期: 2026-07-14 | 来源: PROMPT-018 / D024 / R006 / D003
> 执行方式: 3 子 agent 并行（全文核查 + 物理量级 + 社区/迁移 web 调研）+ 主控集成判定
> 性质: GW Step 4a 维度 A 竞争分解，Go/Kill 判决

## TL;DR

**Conditional Go（进维度 D MVE 验证恢复动作 dB 量级）。**

A0§1 "为什么没人做" 的核心担忧**未触发致命**——四个解释无一致命：(a) 沉默 Kill 无证据（三篇均无负面措辞，sat.1553 反而倾向主动）；(b) 物理可行≠工程值得为**中度风险**（fade AFD 10µs < CMA 重收敛 40µs，但压μ/切换轻量响应时间窗充足，R7 冻结无效但压μ未测）；(c) 社区小+问题新**部分成立**（"预测性 fade 触发 DSP 恢复"交叉切口确实小众，Le Bidan 2023 仅 3 引无人接续——这恰恰提供了空白的结构性合理解释）；(d) RF/光纤迁移**不成立**（三条迁移路径均未直达 DSP 块级，新颖性保留）。

**空白的结构性合理性已找到**：(c) 的"交叉切口小众+问题新"是"为什么没人做"的合理解释——LEO 相干光通信 + DSP 级 fade 管理 + 预测性检测三者的交叉确实窄，Le Bidan 2023 刚点名 open 且无人接续。这解除了"好得不真实"的核心担忧。

**但有一个 MVE 前置硬约束**：A0§1(b) 揭示恢复动作载体存在工程未知——R7 硬冻结(μ=0)已证完全无效，压μ（非冻结）从未测过，"预测性检测触发压μ能否救 BER"是空白。**进维度 D MVE 的第一优先验证 = 压μ（非冻结）在 fade 期间的 BER 增益**，若压μ也救不了 BER，预测性检测就没有载体（物理 Kill）。

## A0§1：为什么没人做？（四解释逐一查证）

### (a) 沉默的 Kill — 有人试过但不行

**证据强度：无。**

3 子 agent 逐字精读 L-DP5/L-DP6/sat.1553 全文 content.md 的 limitations/future work/discussion/conclusion 段落：

- **L-DP5**（Le Bidan 2023 ICSOS）：L765-771 "deep fades will ineluctably appear and possibly span many frames... stay locked as long as possible... recover quickly from hang-up, requires further work" ——**纯 open problem 提名，零尝试零否决**。future work（L787-792）三个方向全是正向改进（refine CFO / supplement clock recovery / more accurate phase tracking），无 "predictive/proactive/marginal/not worth" 任何负面词。
- **L-DP6**（Johst 2024 WiSEE）：L209-211 future work 明确 "further improvements to the DSP algorithms should be investigated to **reduce the DSP outage threshold** towards even lower SNRs" ——**方向与"沉默 Kill"假设相反**（作者要进一步降 outage，不是否定恢复价值）。对 SNR<-1dB 的处理是 multi-aperture 场景下"discard for combining"，非单链路主动恢复的否决。
- **sat.1553**（Valjus 2025 综述）：L582 "turn off tracking when incoming signal power is low [79]. **However, if the SOP changes significantly during each fade, then being able to still track the SOP through the fades would be advantageous.**" ——**作者温和批评被动冻结，明确倾向主动**。L764 主动提名"variable step size... attractive option for OSL through the atmospheric channel"；L440 主动提名"dynamically adjusting the phase estimation window... Further research is necessary"。

**三篇均无** "predictive/proactive/anticipatory/fade forecast/early warning" 任何词汇，均无 dB 增量过小/误报/物理不可行的负面讨论，均无 CMA 重收敛时间 vs fade 持续时间比值的定量分析（sat.1553 L757-758 给了 CMA 收敛 <4µs vs 相干时间 >1ms 的有利比值，但论证的是"被动冻结后重收敛可行"，未扩展到预测性触发）。

负面结果检索（web 子 agent 13 查询）：未找到任何 "fade-triggered equalizer / proactive DSP recovery / predictive CMA restart + negative result" 的明确负面结论论文。

**判定**：(a) 不成立。无人做过预测性 fade 检测，也没有人试过并发现不行。

### (b) 物理可行 ≠ 工程值得（dB 增量）

**证据强度：中。**

子 agent 用现有 GG 时间模型（`common/_gg_time.py`）跑 20 seeds × 10⁷ 符号统计 fade AFD：

| 指标 | 值 | 来源 |
|---|---|---|
| **fade AFD（h<0.3, f_G=100Hz, strong）** | **10.12 µs = 253 blocks** | 实测 pooled 20 seeds |
| fade 中位持续时间 | 0.16 µs（4 blocks） | 同上 |
| fade p95 / p99 | 15.2 µs / 184 µs | 同上 |
| CMA 冷启动重收敛（10⁵ sym @2.5GBaud） | 40 µs | sat.1553 L757-758 换算 |
| DA-LMS 重收敛（10⁴ sym） | 4.0 µs | 同上换算 |
| 压μ/冻结响应延迟 | 40 ns（1 block） | 即时门控 |

**关键比值**：
- AFD / CMA 重收敛 = **0.25**（<1）→ 典型 fade 内 CMA **来不及冷启动重锁定**
- AFD / DA-LMS 重收敛 = **2.5**（>1）→ DA-LMS 能塞进一次平均 fade
- AFD / 压μ响应 = **253**（>>1）→ 压μ时间窗极充足
- AFD p99 / CMA 重收敛 = 4.6（>1）→ 仅最深 1% 长 fade 够 CMA 重收敛

**R7 冻结无效阴影**：D010/S008 证明硬冻结（μ=0）全 24 组合 ΔP_div=0，完全无效。但**压μ（降低非冻结，μ→μ/k）从未测过**（全代码库 grep `mu_compress/variable_step_size` 零命中）。R7 理论暗示：R1 漂移模型 drift=μ·R²·σ_n·√(AFD/(block·T_S)) 线性正比于 μ，压μ直接降漂移。**但漂移防护 ≠ BER 救回**——R7 冻结把漂移降到 0 都没救回 BER，说明 BER 恶化主因可能不是 fade 期间权重漂移，而是更根本的（fade 期间噪声驱动 CMA 误差曲面变形，或恢复后 SOP 已偏——R7 实验B测到冻结期 SOP 累计漂移最高 1774°）。

**判定**：(b) 为**中度风险，不直接致命**。时间尺度物理硬约束已坐实（典型 fade 短于 CMA 重收敛，CMA 重锁定路径对均值/p95 fade 物理死），但：
1. 轻量恢复动作（压μ/模式切换）时间窗充足（比值 253）
2. DA-LMS 重收敛能塞进 fade
3. **压μ能否救 BER 是空白**——这是 MVE 第一优先验证项

若 MVE 证明压μ也救不了 BER（像 R7 冻结一样），预测性检测就没有载体 → 物理 Kill。

### (c) 社区小 + 问题新

**证据强度：中。**

web 子 agent 13 查询调研：

- **LEO 相干光通信整体社区不小且在升温**：Horst 2023（引 140）、Guiomar 2022 review、Valjus sat.1553（引 11）、NICT 2025 2Tbit/s 演示、Nature npj 2025 100Gbps。2023 起进入"演示+综述井喷"扩张期。
- **但"预测性 fade 触发 DSP 恢复"交叉切口确实小众+新**：
  - Le Bidan 2023（hang-up recovery open problem）仅被引 **3 次**，且无人接续做"预测性 fade 触发 DSP"
  - sat.1553 综述未覆盖"预测性触发"方向
  - 除 L-DP5/L-DP6/sat.1553/JR-CMA 外，无专门做"DSP 级 fade/hang-up/cycle-slip 管理触发恢复"的工作
  - Lauinger 2022 VAE-LE 选择"换均衡器结构"而非"预测触发重启"，可解读为社区默认重启不如换结构

**判定**：(c) **部分成立**。"整个 LEO 相干光社区小众"不成立（社区升温），但"预测性 fade 触发 DSP 恢复"交叉切口确实小众+新。**这恰恰提供了空白的结构性合理解释**——为什么没人做：因为这个三叉交叉（LEO 相干光 × DSP 级 fade 管理 × 预测性检测）确实窄，Le Bidan 2023 刚点名 open 且无人接续。

### (d) RF/光纤有迁移

**证据强度：弱（倾向不成立）。**

web 子 agent 查证三条迁移路径：

1. **RF loss-of-lock 预测性检测**：**无成熟预测性方案**。WebSearch 明确返回"该组合 underrepresented/niche"。现有 RF 工作全是响应式（lock detector 超阈后重捕获；US5905410A 专利 reactive；Navipedia "一旦失锁则重捕获"）。"预测性（趋势预测失锁）→ 触发重捕获"本身也是 niche，Q-DP3 不是从 RF 平移搬来。
2. **光纤 OPM 预测性检测**：有大量"预测"（Kilper 2004 引 620+；Nature 2026 软失效预测），但触发动作是**网络层重路由/运维告警**，不是"预测 fade → 触发接收端均衡器/CPR 跨帧重启"。与 Q-DP3 的物理层 DSP 块级触发**不同层**。
3. **RF 长程预测**（Adeogun 2025 / Heidari 2006）：做到"预测信道统计 → 触发 AMC/MCS 切换"（传输格式层），**未做到"预测 → 触发 DSP 块重配置"**。把"预测"接到"光相干 DSP 块级响应"需要重新定义触发动作与 DSP 接口，非平凡。

**判定**：(d) **不成立**。三条迁移路径均未直达 Q-DP3 的"预测 fade → 光相干 DSP 跨帧恢复"，"迁移非原创"攻击线不成立，Q-DP3 新颖性保留。但需注意：光纤软失效预测+触发、RF AMC 预测这两个相邻成熟领域存在，审稿人可能据此质疑"只是把已知预测换了触发对象"——论文须明确区分触发层（物理层 DSP 块 vs 网络/AMC）并论证非平凡性。

### A0§1 判定

| 解释 | 证据强度 | 是否致命 |
|---|---|---|
| (a) 沉默 Kill | 无 | 否 |
| (b) 物理可行≠工程值得 | 中 | **否（但有 MVE 前置约束）** |
| (c) 社区小+问题新 | 中 | 否（反而提供结构性合理解释） |
| (d) RF/光纤迁移 | 弱（不成立） | 否 |

**最可能的解释 = (c) + (b) 组合**：为什么没人做？因为这个三叉交叉切口确实小众+新（c），且恢复动作的工程价值存在未知（b 悬而未决）。**A0§1 不致命**——空白的结构性合理性已找到（交叉切口小众+问题新），用户的"好得不真实"担忧在"为什么没人做"层面已解除。

**但 (b) 的工程未知是进 MVE 的硬约束**：压μ能否救 BER 决定预测性检测有没有载体。这不是 A0§1 致命（A0§1 问的是"为什么没人做"，(c) 已回答），是维度 D MVE 要验证的。

## A0 其他致命项

### A0§6 物理量级

承接 A0§1(b) 的 fade vs 恢复时间比：

- **fade AFD 10µs vs CMA 重收敛 40µs**：比值 0.25，CMA 重锁定对典型 fade 物理死
- **fade AFD 10µs vs 压μ响应 40ns**：比值 253，轻量响应时间窗充足
- **fade AFD 10µs vs DA-LMS 4µs**：比值 2.5，DA-LMS 能塞进
- **sat.1553 L757-758 有利证据**：CMA 收敛 <4µs @28GBaud << 相干时间 >1ms（比值 0.004），作者论证"即使完全信号丢失也能在相干时间内重收敛"——但这是 vs 相干时间，不是 vs 单次 fade AFD

**A0§6 判定**：物理量级**部分通过**——轻量响应（压μ/切换）时间窗充足，但 CMA 重锁定路径物理死。Q-DP3 的恢复动作必须限定为轻量响应（压μ/冻结/模式切换），不能是 CMA 重锁定。这与 R006 P2.4 合并定义一致（"响应动作=轻量，不含重训练 ML"）。

### A' 竞争维度

Q-DP3 竞争的"深衰落恢复"维度先验覆盖度：

| 方法 | 深衰落恢复策略 | 预测性？ | 覆盖度 |
|---|---|---|---|
| sat.1553 L582 [79] | 被动冻结（功率低→停更新） | 否（响应性） | 低（唯一被点名的被动策略，且被作者温和质疑） |
| L-DP5 | open problem（"requires further work"） | — | 零（未解决） |
| L-DP6 | 丢弃坏支路（multi-aperture 场景） | 否（响应性） | 低（不同场景） |
| JR-CMA (L-DP8) | 误差阈值重置 + AGC + 自适应步长 | 否（响应性，error 超阈后重置） | 中（三机制占点，但响应性） |
| **Q-DP3** | **预测性 fade 检测 → 轻量恢复** | **是** | **零（无先例）** |

**A' 判定**：Q-DP3 竞争的"预测性 fade 检测驱动恢复"维度先验覆盖度**最低**（D003 原判 + R005 确认 FSO 算法层无先例 + A0§1(c) 证实交叉切口小众）。R005 的判断**经 A0§1 反向论证后仍成立**——(a) 无沉默 Kill、(d) 非简单迁移，均未修正"先验覆盖度最低"的判断。

创新声称建立在"预测性检测 + 轻量恢复"维度上，该维度先验覆盖度低 + ML/物理信号改善空间存在（h 趋势预测 → fade 深度/持续时间非线性映射）。**A' 通过**。

## 四判据（glossary.md 唯一拥有者）

| 判据 | Q-DP3 现状 | 证据 | PASS/FAIL |
|---|---|---|---|
| ① 具体技术矛盾（M-C-A 明确） | M=预测性 fade 检测驱动跨帧 DSP 恢复 / C=双偏振星地 GG 湍流 LEO / A=L-DP5 点名 hang-up recovery open + L-DP6 DSP outage + sat.1553 仅被动冻结 | R006 P2.4 合并定义 + D024 fade 前兆验证 + L-DP5 L765-771 原文 | **PASS** |
| ② 有方法产出形态 | 恢复机制设计（fade 检测阈值 vs 恢复时间 vs outage 概率权衡曲线 = 可复用 design rule） | glossary 判据 2 认可"可被后续工作复用的 design rule"；L-DP5/L-DP6 outage 概率框架（BER>0.44）已建立，Q-DP3 加恢复维度 | **PASS** |
| ③ 有近期 baseline 可对标 | L-DP5（2023）被动冻结 + hang-up 后慢恢复 = 传统未优化 baseline（FR-25） | L-DP5 L765-771 + sat.1553 L582 [79] Matsuda 2020 | **PASS**（确认是"传统未优化"非"已优化强 baseline"——JR-CMA 是更强 baseline，MVE 阶段碰） |
| ④ 能做可量化对标 | 恢复时间（hang-up → 重新锁定）/ outage 概率（fade 期间 BER>0.44 比例）/ dB 增益 vs 被动冻结 | L-DP6 outage 框架 + D024 fade 前兆验证数据 | **PASS** |

**四判据全过。**

## Go/Kill 判定（FR-25 标准分离）

### Go 标准（赢传统未优化 baseline 的前景）

- ✅ 四判据全过
- ✅ A0§1 找到空白的结构性合理解释（(c) 交叉切口小众+问题新）——非致命
- ✅ A' 竞争维度先验覆盖度最低，预测性检测 + 轻量恢复有 ML/信号处理改善空间
- ✅ 对手 = L-DP5 被动冻结（传统未优化 baseline，FR-25）——赢它的前景：预测性检测比被动冻结提前触发恢复，理论上能降低 outage 概率 / 缩短恢复时间
- ✅ A0§6 轻量响应时间窗充足（AFD/压μ响应 = 253）
- ⚠️ 但恢复动作 dB 量级未知——R7 冻结无效阴影，压μ未测

### Kill 标准（A0§1 致命 / 上界<0.5dB / 四判据不全）

- ❌ A0§1 不致命（(c) 提供结构性合理解释）
- ❌ 四判据全过
- FR-21 上界：outage 从 ~50%（L-DP6 SNR<-6dB）降到接近 0 = 量级改善远 >0.5dB 等效 → **不触发 Kill**（D003 原判不变）。但 caveat：这是上限估算，实际取决于压μ能否救 BER

### 判定：Conditional Go（进维度 D MVE）

**理由**：A0§1 核心担忧"为什么没人做"已解除——(c) 提供结构性合理解释（交叉切口小众+问题新，Le Bidan 2023 刚点名无人接续），(a) 无沉默 Kill，(d) 非简单迁移。四判据全过，A' 先验覆盖度最低，FR-21 不触发。**但 (b) 的工程未知（压μ能否救 BER）是 MVE 硬前置**——这是 Go 进 MVE 的条件，不是 A0§1 Kill 的条件。

**Conditional 条件**（进维度 D MVE 前必须验证）：
1. **压μ（非冻结）在 fade 期间的 BER 增益**——若压μ也救不了 BER（像 R7 冻结一样），预测性检测没有载体 → 物理 Kill。这是**第一优先验证项**，决定方向生死。
2. 若压μ有效，再验证预测性检测（提前压μ）vs 响应性检测（fade 触底后压μ）的增量——这是 Q-DP3 的核心创新点（预测性 vs JR-CMA 响应性的界线）。

## 若 Go：维度 D MVE 的设计建议

### MVE 核心：压μ能否救 BER（生死验证）

**假设**：fade 期间压 μ（μ→μ/k，非冻结）能降低 CMA 权重漂移从而改善 BER。

**最小实例**：
- 参数：f_G=100Hz, strong, N=5M, QPSK, SNR=20dB, CMA μ=1e-3（安全区，不发散，但有跟踪滞后）
- 对比：CMA 常规 μ=1e-3 vs CMA fade 期间压 μ=1e-4（功率阈值触发）vs oracle（fade 期间完美 MMSE）
- 指标：PI-BER（排列不变，D018 双口径）

**PASS 标准**：压 μ 的 PI-BER 显著低于常规 μ（配对 Wilcoxon p<0.05, ≥5 seeds），且接近 oracle。

**FAIL 标准**：压 μ 与常规 μ 无显著差异（像 R7 冻结一样），或压 μ 反而更差。

### 若压 μ PASS：验证预测性 vs 响应性的增量

**假设**：预测性检测（fade 前兆期压 μ，D024 验证 85% 事件提前 ≥2µs）比响应性检测（h 跌破阈值后压 μ）多救 BER。

**对比**：预测性压 μ vs 响应性压 μ vs 常规 μ（三对照）

**PASS 标准**：预测性 > 响应性 > 常规，且预测性 vs 响应性显著（这是 Q-DP3 的核心增量，区分 vs JR-CMA）。

### oracle 上界估算（FR-21）

fade 期间最优 MMSE vs 被动冻结的 BER 差 = 恢复上界。若 <0.5dB 直接 Kill 不跑 MVE。
- L-DP6 给 SNR<-6dB outage ~50%，完美恢复 outage→0 = 量级改善 >>0.5dB
- 但需用真实 GG 时间模型估算（不是 SNR 扫描），AFD 10µs 内能恢复多少

## 若 Kill：死因 + 可复用部分

**死因（若压μ FAIL）**：fade 期间压 μ 救不了 BER（R7 冻结无效的延伸），预测性检测没有载体——检测到 fade 也没有有效的轻量恢复动作。恢复动作本身物理死，不是检测问题。

**可复用部分**：
1. fade 前兆可辨识（D024，85% 事件提前 ≥2µs）——可作分析层贡献独立发表
2. GG 时间域衰落模型 + AFD/LCR 统计——共享基建，Q-CMA-FADE 分析层已用
3. A0§1 竞争分解方法（"为什么没人做"四解释框架）——可复用于其他方向评估
4. sat.1553 L582 主动恢复倾向 + L764 动态步长 open problem 的文献定位——可作论文 motivation

## 对主控决策的建议

### 方法层战略：Q-DP3 vs Q-CMA-FADE 的最终判断

**当前格局**：
- **路线 A（Q-CMA-FADE ML 加固）**：D022 GO 但 D023 收窄（ML 优势 N=2M 不普适，f_G=1000 反转），改动1 新颖性 PASS 但收益空间受限。方法层单独不足以支撑强贡献。
- **路线 B（Q-DP3）**：维度 A Conditional Go，天花板未受 D023 反预期影响。**但 (b) 压μ能否救 BER 是生死未知**——若 FAIL，Q-DP3 死，方法层只剩 A 保底。

**建议**：
1. **优先验证 Q-DP3 的压μ生死问题**（MVE 第一优先，1 天内可出结果）——这是决定方法层战略的关键实验。
2. 若压μ PASS → Q-DP3 是更有潜力的方向（预测性 + 天花板未受影响），优先推进。
3. 若压μ FAIL → Q-DP3 Kill，回路线 A 保底（D022 + 改动1），接受"ML 优于 standard-CMA 在限定参数域"的弱卖点。
4. **两者结合的可能**：Q-DP3 的预测性 fade 检测 + Q-CMA-FADE 的 ML 均衡器（fade 期间切换到 ML 前馈，避免 CMA 跟踪滞后）——但这需 Q-DP3 压μ PASS 后再评估，不在当前任务范围。

### 分析层（确定产出）

无论 A/B：发散 μ 主导（D006/D010）+ SOP 极化串扰机制（D014）+ GG 时间模型（S004）+ fade AFD/LCR 统计（本报告）+ fade 前兆可辨识（D024）——是最确定的论文产出。

## 检索记录 + 全文精读记录

| 类型 | 查询/文件 | 命中 | 日期 |
|---|---|---|---|
| 全文精读 L-DP5 content.md | limitations/future work 段 | L765-771, L787-803 | 2026-07-14（子 agent） |
| 全文精读 L-DP6 content.md | future work/outage 段 | L106-138, L207-211 | 2026-07-14（子 agent） |
| 全文精读 sat.1553 content.md | §6.3 open problem + fade 策略 | L558, L582, L764, L778, L790 | 2026-07-14（子 agent） |
| GG 时间模型 AFD 统计 | 20 seeds × 10⁷ 符号 | AFD=10.12µs, LCR=30337/s | 2026-07-14（子 agent） |
| Web 检索（社区规模） | 5 查询 | ~40 条 | 2026-07-14（子 agent） |
| Web 检索（RF/光纤迁移） | 5 查询 | ~35 条 | 2026-07-14（子 agent） |
| Web 检索（负面结果） | 3 查询 | ~15 条 | 2026-07-14（子 agent） |
