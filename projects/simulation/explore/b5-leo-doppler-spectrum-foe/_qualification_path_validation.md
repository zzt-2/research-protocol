# 阶段 0.1 够格路径验证 — B5-Q1 范围优势在 D005 会议门槛下能否当 Go 判据

> 专题: 2026-07-08-b5-leo-doppler-spectrum-foe
> 来源: S002（工作对话对话 1）| 日期: 2026-07-08
> 纪律: INVARIANT 11（B5 特殊·够格路径首验证）+ D005 务实路线 + FR-25 Go/Kill 标准分离 + 核查机制中性双向（子 agent 产出 + 主线独立 grep 核查）+ profile 第 9 次"急于推进"防线
> 守: 阶段 0 不写代码，本文件只做够格路径分析，不进 sandbox

## 核心问题

**B5-Q1 不是 dB 增量是范围优势**（±4.5GHz vs 传统 ±312.5MHz，15× 范围扩展），D005 "赢 baseline 几 dB" 标尺下不够格（`_cut-b4b5-verify.md:64-66` 确认 B5 本体无"vs baseline 改善 X dB"对比只给绝对残频/范围指标）。

**阶段 0.1 要回答**：范围优势在 D005 会议门槛下能不能当 Go 判据？会议门槛放宽（纯仿真+鲁棒性 dB/范围/绝对指标/同族 dB 都算够格，S031 + 切法地图 §C.2）允许范围维度够格，但具体走哪条够格路径必须验证。

## 0.1a 事实底座（子 agent 核查 + 主线独立 grep 复核）

### 范围优势具体指标（全标 content.md 行号，FR-26 读原文数值）

| 指标 | B5 锚数值 | 行号 | 对照传统 FOE |
|---|---|---|---|
| 捕获范围 | ±4.5 GHz | abstract L23×2 / intro L29 / L47 / experiment L143 / L149 | 传统 ±B/8 = ±312.5MHz（L57 定义 [−B/8,+B/8]）|
| 粗补偿后残频标准差 | σ < 140 MHz | L23 / L47 | — |
| 粗补偿后残频最大值 | 250 MHz（含激光 250MHz 抖动 + 算法误差）| L149 / L167 | — |
| 精确补偿后残频 | < 5 MHz | L149 | — |
| 精估范围 | ±312.5 MHz（=B/8=2.5Gbaud/8）| L57 / L95 / L149 / L167 | 传统 FOE 即此范围 |
| BER 1e-3 接收灵敏度 | −48 dBm | L149 | — |
| 收敛迭代 | 8 点 FFT 第 4 次 / 16 点 FFT 第 3 次 | L129 / L141 | — |
| Doppler 变化率最大 | 56 MHz/s | L147 | — |
| 循环周期 | 3 s | L93 | — |
| 理论估计范围 | ±B/2 | L117 | — |
| 接收机锁定能力 | ≥9 GHz | L147 | — |
| 预补偿后残频 | 可达 500 MHz | L57 | — |
| 系数 α | 6×10⁸ | L85 | — |
| 均值滤波 | 1024 组 16 点 FFT | L87 | — |

### 主线独立 grep 核查子 agent 两个关键归因（INVARIANT 10 中性双向）

**核查 1：±4.5GHz 出现位置 + conclusion L167 是否含 ±4.5GHz**

主线 grep 结果（`grep -n "4.5 GHz" content.md`）：
- L23（abstract，两次：Doppler 范围 + capture range extended to）
- L29（intro，Doppler 物理范围）
- L47（intro，capture range [−4.5GHz,+4.5GHz]）
- L143（experiment，Doppler 范围建模自 Ref [6]）
- L149（results，compensate up to [−4.5GHz,+4.5GHz]）

主线 sed 验证 L163-168 conclusion 段：只复述 ±312.5MHz 精估范围 + ±250MHz 粗补偿残频，**无 ±4.5GHz**。

**核查结论**：子 agent 归因 **PASS**。H001 声称的"abstract/intro/experiment/conclusion 四处一致 ±4.5GHz"需修正为"**五处 L23×2/L29/L47/L143/L149，不含 conclusion**"。这是 H001 的一个小事实错误（conclusion 没复述 ±4.5GHz，只复述残频指标），但不影响范围优势核心判定——±4.5GHz 在 abstract/intro/experiment 三段确实字面一致，是 B5 的核心范围声称。

**核查 2：B5 锚全文是否含 "7 dB" / "penalty" / "Leven" / "[60]"**

主线 grep 结果：`grep -ni "penalty\|leven\|7 dB\|\[60\]"` exit=1（0 命中）。B5 参考文献最大编号 [28]（L249 C. Ju et al. Opt Lett 49(4) 2024）。

**核查结论**：子 agent 归因 **PASS**。`_B5-short-time-spectrum-cfo-increment.md:43` 提到的"[60] Leven differential decoding 500MHz 致 7 dB penalty"数字**不来自 B5 锚全文**，是详评笔记从 sat.1553 综述或 [60] Leven 原文引入的对照数字。**0.2 阶段需到 sat.1553 / [60] Leven 原文溯源，不能归因于 B5 锚**。

### B5 vs 传统 baseline 对比形态（核查"本体无 dB 对比"声称）

子 agent 核查 + 主线确认：
- B5 自定位为 4 类 FOE 算法第 4 类（谱分析），四类列举在 L33-35
- B5 相对前三类优势描述：L47 "blind... enhances data throughput without requiring pilot data... consumes fewer logic resources compared with the traditional frequency offset compensation algorithm" + L167 "low algorithmic complexity, low logic resource consumption, and no dependence on DSP compared with the traditional algorithm"
- **定性对比（"低复杂度/无 pilot/不依赖 MIMO DSP"），无"vs 某 baseline 改善 X dB"定量对比**
- 全文 dB 数字均为绝对接收功率（−51/−48/−45/−25/−10/−3 dBm）或 3dB 带宽（1.33 GHz L115），无任何增量 dB 表述

**结论**：`_cut-b4b5-verify.md:64-66` 关于"B5 本体无 vs baseline 改善 X dB 对比只给绝对残频/范围指标"的声称 **PASS**（原文验证成立）。B5 的优势叙事属于**绝对指标 + 范围扩展 + 鲁棒性**三类混合，不含 dB 增量类。

### B5 实验形态核查（BUPT 模板对标相关）

子 agent 核查 + 主线确认：
- **B2B 实验**（L91 "real-time back-to-back (B2B) verification experiment"）非星地实测/湍流信道仿真
- **Intel Arria 10 FPGA**（L93 Tx 端 + L95 Rx 端 + L109 Fig.2 caption）
- **无湍流建模**（L29 intro 仅背景提"atmospheric turbulence... affect the optical signal"，实验章节 Section 3-4 无湍流信道/AO/湍流参数）
- **PM-QPSK 2.5-GBaud**（L23/L47/L89/L91/L93/L109/L167）
- 卫星下行链路是"建模"进 B2B 的（L143 "The modeling scheme of the satellite downlink system mentioned in Ref. [6] is implemented in the experiment"），非真实星地链路

**B5 vs B4 实验形态对照**（`_cut-b4b5-paillier-pool.md:27,41,47` + `_cut-map-final-b1-b12.md:68,142`）：
- B4/B5 **同 BUPT 团队**（Na Liu / Cheng Ju / Jiamin Fan，青岛大学+CETC 34 所）
- B4/B5 **同 Intel Arria 10 FPGA 实时 demo 模板**
- B4/B5 **同 B2B 无湍流信道**
- **差异**：B4 有"±920 MHz @ 0.5 dB 灵敏度代价"（内部对照 dB，`_cut-b4b5-paillier-pool.md:30`），B5 连内部对照 dB 都没有（纯绝对指标）——**B5 比 B4 在 dB 维度更弱**

**切法地图判定**（`_cut-map-final-b1-b12.md:50`）：B5 落"绝对指标无外部 dB ~5 篇 → 不够格"档。

## 0.1b 够格路径 3 选项分析

### 路径 A：BUPT Arria 10 FPGA demo 会议模板（绝对指标够发会议）

**论证**：

切法地图 §C.2 明确（`_cut-map-final-b1-b12.md:142`）："B4/B5 同 BUPT 团队 Arria 10 FPGA demo 是会议级模板（绝对指标够发会议）"。会议门槛放宽（S031 + 切法地图 §D "会议级别门槛放宽：纯仿真档 + 鲁棒性 dB / 绝对指标 / 同族 dB 都够发会议"）。

B5 的绝对指标组合：
- **范围扩展 15×**：±4.5GHz vs 传统 ±312.5MHz（覆盖 LEO Doppler 全量程）
- **绝对残频指标**：σ<140MHz / 精确补偿后 <5MHz（落精估范围 ±312.5MHz 内保证后续 DSP 可接）
- **BER 1e-3 接收灵敏度 −48 dBm**（绝对灵敏度指标）
- **实时 FPGA demo**（Arria 10 + 5GSa/s ADC + 2.5GBaud PM-QPSK，跟 B4 同模板）

**对标 B4**：B4 报 ±920MHz @ 0.5dB（内部对照 dB），B5 报 ±4.5GHz 范围扩展（无 dB 但范围远大于 B4 的 ±920MHz）。会议级别下 B5 的"15× 范围扩展 + 绝对残频 <5MHz"对标 B4 的"±920MHz @ 0.5dB"是**同模板不同维度**——B4 走 dB 维度，B5 走范围维度。

**路径 A 成立条件**：
1. ✅ 会议门槛放宽允许绝对指标够格（S031 + 切法地图 §C.2/§D 明确）
2. ✅ B4/B5 同 BUPT Arria 10 FPGA demo 是会议级模板（切法地图 §C.2 确认）
3. ✅ B5 范围扩展 15× 是结构性优势（±4.5GHz 覆盖 LEO Doppler 全量程，传统 ±312.5MHz 无法覆盖）
4. ✅ B5 绝对残频指标齐全（σ<140MHz / <5MHz / BER 1e-3 −48dBm）
5. ⚠️ **但 B5 本体已发期刊**（Optics Communications 572 (2024)，青岛大学+CETC 34 所）—— B5 锚论文本身就是期刊级，不是"会议级模板"的候选。**B5-Q1 是在 B5 锚基础上做改进型 MVE**，不是复现 B5 发会议。路径 A 的"对标 BUPT 模板发会议"逻辑需重新审视：B5-Q1 的够格不是"发会议"，是"在 B5 锚基础上做出够格的增量贡献"。

**路径 A 判定**：**部分成立但有缺陷**。会议门槛放宽 + BUPT 模板对标确认了"绝对指标+范围扩展"在会议级别算够格形态。但 B5 锚已发期刊，B5-Q1 不能简单"对标 B4 发会议"——B5-Q1 的够格必须是在 B5 锚基础上做出**可验证的增量贡献**（加湍流 / vs baseline dB / 鲁棒性维度）。路径 A 单独不足以够格，需叠加路径 B 或 C。

### 路径 B：补 dB 对比（在星地湍流信道下 vs [60] Leven 做 dB 对比）

**论证**：

B5 本体无湍流无 dB（`_B5-...-increment.md:144` 自承"未涉湍流仅 B2B 实验" + `_cut-b4b5-verify.md:64-66` 确认无 dB 对比）。若在星地湍流信道下 vs [60] Leven Mth-power 做 dB 对比，能直接落 D005 "赢 baseline 几 dB" 标尺。

**但强补 dB 对比可能不真实**：
1. B5 本体是粗 CFO 估计（残频落 ±312.5MHz 精估范围即完成任务），不是精细同步算法。粗 CFO 的贡献维度是"范围 + 收敛"不是"残频 dB"。强补"vs [60] Leven 残频 dB"可能错位——[60] Leven 是时域 Mth-power 精细 FE（OSNR <9dB 近乎与频偏无关），跟 B5 粗 CFO 不是同一任务环节。
2. B5 本体 B2B 无湍流，加湍流后功率波动会污染正负功率谱面积比（INVARIANT 13 D006 边界残留）——前馈归一化能处理但范围优势可能衰减。补 dB 对比的结果可能是"B5 在湍流下残频 dB 不如 [60] Leven"（因为 [60] Leven 时域 Mth-power 对幅度波动更鲁棒）。
3. [60] Leven 7 dB penalty 数字来自 differential decoding 无 FE 场景（`_B5-...-increment.md:43`），不是 B5 vs [60] Leven 的直接对比基线。B5 vs [60] Leven 的 dB 对比需重新设计实验。

**路径 B 成立条件**：
1. ⚠️ 需在星地湍流信道下设计 B5 vs [60] Leven 的公平对照（[60] Leven 是精细 FE 不是粗 CFO，任务环节不同需论证对比公平性）
2. ⚠️ 需论证前馈归一化后 B5 范围优势在湍流下仍成立（阶段 0.3 架构定性前置）
3. ⚠️ 需 [60] Leven 原文溯源 7 dB penalty 数字（0.2 阶段做，核查是否真能作 B5 对照基线）
4. ⚠️ 补 dB 对比结果可能不利（B5 粗 CFO 在湍流下残频 dB 可能不如 [60] Leven 精细 FE）

**路径 B 判定**：**风险路径，单独不成立**。强补 dB 对比有任务环节错位风险 + 结果可能不利风险。路径 B 不能作为主够格路径，只能作为路径 A/C 的补充维度（若 sandbox 阶段 B5 在湍流下 vs [60] Leven 确实有 dB 增量，则叠加够格；若无则靠路径 A/C）。

### 路径 C：鲁棒性维度（范围扩展 + Doppler rate 跟踪稳定性够格）

**论证**：

切法地图 §B.1 明确稀池点 dB 偏鲁棒性/范围维度（`_cut-map-final-b1-b12.md:83` "4 点里 3 点 dB 形态偏'失效区/范围/鲁棒性'非'赢 baseline 几 dB'"）。B7 就是走这条路（0.6dB + 1.9×范围 + OSNR 10dB，OFC 2026 已发，`_cut-map-final-b1-b12.md:87`）。

B5 的鲁棒性维度组合：
- **范围扩展 15×**：±4.5GHz vs 传统 ±312.5MHz（结构性优势，传统 FOE 无法覆盖 LEO Doppler 全量程）
- **Doppler rate 跟踪稳定性**：56MHz/s 最大变化率下仍可跟踪补偿（L147 "the proposed scheme can also track and compensate the Doppler frequency shifts well" under "large Doppler frequency shifts"）
- **低接收功率鲁棒性**：−48 dBm @ BER 1e-3 + −51 dBm 仍可跟踪（L149 "in the case of low ground received optical power, this scheme can effectively improve the accuracy of frequency offset tracking"）
- **收敛稳定性**：3-4 次迭代收敛，不受接收功率显著影响（L141 "the rate of convergence of the frequency offset estimation is not significantly affected by the received power"）

**对标 B7**：B7 走"0.6dB + 1.9×范围 + OSNR 10dB"三维鲁棒性够格 OFC。B5 走"15× 范围扩展 + 56MHz/s 跟踪 + 低接收功率鲁棒性"三维鲁棒性，范围维度比 B7 更强（15× vs 1.9×），但无 dB 维度（B7 有 0.6dB）。会议级别下 B5 的鲁棒性三维组合够格——**跟 B7 同模式（范围+鲁棒性+绝对指标），维度更强（范围 15× vs 1.9×）但缺 dB 维度**。

**路径 C 成立条件**：
1. ✅ 切法地图 §B.1 确认稀池点鲁棒性维度够格（B7 OFC 已发先例）
2. ✅ B5 范围扩展 15× 是结构性优势（远超 B7 的 1.9×）
3. ✅ B5 Doppler rate 跟踪 + 低接收功率鲁棒性有原文支撑（L147/L149）
4. ⚠️ B5 无 dB 维度（B7 有 0.6dB）——需论证"范围 15× + 鲁棒性三维"在会议门槛下够抵消无 dB 的劣势
5. ⚠️ B5 鲁棒性指标是 B5 锚论文已报的，B5-Q1 需做出**增量贡献**（加湍流验证鲁棒性 / vs baseline 鲁棒性对比），不能只复现 B5 锚的鲁棒性指标

**路径 C 判定**：**主够格路径，成立但有增量要求**。B5 的范围+鲁棒性三维组合在会议门槛下够格（B7 同模式已发 OFC），但 B5-Q1 必须在 B5 锚基础上做出增量贡献——最自然的增量是**加星地湍流信道验证 B5 范围优势+鲁棒性是否仍成立**（B5 锚 B2B 无湍流，加湍流是天然切口，跟 B11 加 FSO 湍流同模式）。这个增量既验证 B5 范围优势的鲁棒性（路径 C），又可能产出 vs baseline dB 对比（路径 B 补充），还对标 B5 锚的工程可用性（路径 A 补充）。

## 0.1c 判定门控

### 三条够格路径判定汇总

| 路径 | 判定 | 理由 |
|---|---|---|
| A（BUPT Arria 10 FPGA demo 会议模板）| **部分成立有缺陷** | 会议门槛放宽 + BUPT 模板对标确认绝对指标够格形态，但 B5 锚已发期刊，B5-Q1 不能"对标发会议"需做出增量贡献 |
| B（补 dB 对比）| **风险路径单独不成立** | 任务环节错位风险（粗 CFO vs 精细 FE）+ 结果可能不利风险（湍流下 B5 残频 dB 可能不如 [60] Leven）|
| C（鲁棒性维度）| **主够格路径成立有增量要求** | 范围 15× + 鲁棒性三维组合会议够格（B7 同模式 OFC 已发），但需在 B5 锚基础上做增量（加湍流验证）|

### 够格路径结论：B5-Q1 够格，走路径 C 为主 + 路径 A/B 补充

**判定**：B5-Q1 **够格**，不转 Kill。走**路径 C（鲁棒性维度）为主够格路径**，叠加路径 A（绝对指标对标 BUPT 模板）+ 路径 B（补 dB 对比作 sandbox 验证维度，不作主判据）。

**够格叙事框架**（会议级别）：
- **主叙事**（路径 C）：B5 短时谱 FOE 在星地 LEO Doppler 场景下实现 15× 范围扩展（±4.5GHz vs 传统 ±312.5MHz）+ 56MHz/s 跟踪稳定性 + 低接收功率鲁棒性，验证 B5 范围优势在湍流信道下仍成立
- **增量贡献**（B5 锚 B2B 无湍流 → B5-Q1 加湍流验证）：在星地湍流信道下验证 B5 范围优势+鲁棒性是否仍成立（对标 B11 加 FSO 湍流同模式）
- **辅助维度**（路径 A）：绝对指标对标 BUPT Arria 10 FPGA demo 会议模板（B4/B5 同模板）
- **sandbox 验证维度**（路径 B）：在湍流下 vs [60] Leven 做残频/BER 对比，若 B5 有 dB 增量则叠加够格，若无则靠路径 C/A

**判定依据**：
1. INVARIANT 11 够格路径首验证 — 路径 C 成立（鲁棒性维度会议够格），不转 Kill
2. D005 务实路线 — 会议门槛放宽允许范围/绝对指标/鲁棒性够格（不只 dB）
3. FR-25 Go/Kill 标准分离 — Go 标准=赢传统 baseline（B5 范围 15× 超传统 ±312.5MHz 是结构性优势）+ 会议门槛放宽
4. 切法地图 §B.1 + §C.2 — B7 OFC 已发确认鲁棒性维度够格路径，B5 范围 15× 比 B7 的 1.9× 更强
5. profile"务实可毕业>理论最优" — B5-Q1 走路径 C 是务实路线落地

**不转 Kill 的理由**：三条够格路径并非都不成立——路径 C 明确成立（B7 同模式 OFC 已发先例 + B5 范围 15× 比 B7 更强），路径 A 部分成立（BUPT 模板对标），路径 B 虽风险但可作 sandbox 验证维度。B5-Q1 够格转进 0.2。

**不直接当 Go 跑 MVE 的理由**（守红线 1）：够格路径验证通过 ≠ 直接当 Go 跑 MVE。阶段 0.2-0.6 前置规约必须全做完才进 sandbox（INVARIANT 6 + profile 第 9 次防线）。特别是：
- 阶段 0.2 dB/范围溯源核查（[60] Leven 7dB penalty 溯源 + 残频指标全读原文数值）
- 阶段 0.3 架构定性（前馈归一化走前馈路径不撞 D006，且需论证前馈归一化后范围优势仍成立——这是路径 C 的关键前提）
- 阶段 0.4 公平对照框架（baseline [60] Leven 还是传统 FFT FOE？范围 fair gain 定义？工作点 BER 1e-3 还是 HD-FEC？LEO Doppler 主题跟 B7/B4 差异化）

## 风险标注（诚实声明）

1. **路径 C 增量贡献风险**：B5-Q1 加湍流验证后，范围优势可能衰减（湍流致功率波动污染正负功率谱面积比，前馈归一化能处理但效果未知）。若 sandbox 阶段发现范围优势消失 → 红线警报（核心机制崩塌，H001 失败数据附录已标）
2. **路径 B 任务环节错位风险**：B5 粗 CFO vs [60] Leven 精细 FE 任务环节不同，补 dB 对比需论证公平性。若 sandbox 阶段发现 B5 vs [60] Leven 残频 dB 不利 → 不能作主判据，靠路径 C/A
3. **饱和池竞争风险**（INVARIANT 12）：B5 跟 B4 共锚 Paillier 43 篇大池，切法地图 §C 警示"饱和池是 dB 最难出区"。B5 走范围维度能否绕开此警示需 sandbox 验证——路径 C 的范围 15× 是结构性优势，不直接跟饱和池的 dB 竞争，但需确认范围维度在会议够格下不被饱和池 dB 竞争压倒
4. **B5 锚已发期刊的 A1 归属风险**：B5 锚是青岛大学+CETC 34 所已发期刊（Optics Communications 572 (2024)），B5-Q1 的增量贡献必须是论文外改进（加湍流 + vs baseline + 鲁棒性验证），不能是复现 B5 锚。路径 C 的"加湍流验证"是天然论文外切口（B5 锚 B2B 无湍流）

## 下一步

阶段 0.1 够格路径验证完成（B5-Q1 够格走路径 C），进阶段 0.2 dB/范围溯源核查：
1. [60] Leven 7 dB penalty 数字溯源（B5 锚外，到 sat.1553 / [60] Leven 原文核查）
2. ±4.5GHz 出处 + 残频指标全读原文数值（0.1a 已读，0.2 整理成溯源表）
3. 输出 `_db_range_sourcing_audit.md`

阶段 0.3-0.6 留下一对话（守 3 步上限）：
- 0.3 架构定性（前馈归一化 vs 环路 TF，路径 C 范围优势前提验证）
- 0.4 公平对照框架（baseline 选定 + 范围 fair gain 定义 + LEO Doppler 主题差异化）
- 0.5 参数真相源前置（B5Params 草稿）
- 0.6 文件组织规约（short_time_spectrum_foe 接口定义）

## 来源

- S002（本轮工作对话）
- 子 agent 0.1a 核查产出（B5 锚全文范围优势指标 + 四处 ±4.5GHz 一致性 + B5 vs 传统 baseline 对比形态 + 实验场景核查 + [60] Leven 7dB penalty 溯源）
- 主线独立 grep 核查（conclusion L167 不含 ±4.5GHz + B5 锚全文无 7dB/penalty/Leven/[60]）
- `_cut-b4b5-verify.md:64-66`（B5 本体无 dB 对比声称）
- `_cut-b4b5-paillier-pool.md:27,41,44,47`（B4/B5 同 BUPT 团队 + 同 Arria 10 模板 + B5 dB 形态）
- `_cut-map-final-b1-b12.md:50,68,83,87,142`（切法地图 §A.3 B5 落不够格档 + §C.2 BUPT 模板会议级 + §B.1 稀池鲁棒性维度 + B7 OFC 先例）
- `_B5-short-time-spectrum-cfo-increment.md:43,144,145,162`（[60] Leven 7dB penalty + B5 未涉湍流 + D006 边界）
- D005 务实路线 + D006 红线 + D009 checklist + S031 B5-Q1 排第二档 #6
