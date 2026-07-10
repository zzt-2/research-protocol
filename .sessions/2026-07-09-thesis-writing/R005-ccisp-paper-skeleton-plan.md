# [R005] CCISP 2026 投稿包结构骨架

> 2026-07-10 | 关联：专题 slug 2026-07-09-thesis-writing / 简报 v4 / D002(切换降级)/D003(10⁻⁵矛盾)/D004(口径)
> 目的：导师回复前，把"这坨东西怎么包成一篇 4-6 页会议论文"的结构定下来。不写正文，只定骨架——每节写什么、对应哪张图、引哪篇文献、哪里等导师拍板。
> 约束：CCISP IEEE 模板 4-6 页 4-6 图，7/20 截稿。守 FR-22（写作准备不跑实验）+ external-output skill（正文写时再过 C1-C10）。

## 0. 投稿定位（一句话，待导师确认口径后定稿）

星地 FSO 强湍流下，盲载波相位估计相对导频估计的优势量化与归因（+候选切换鲁棒性补丁）。

- **主卖点**：盲 vs 导频的净增益（naive 强湍流 +1.2~1.9dB / fair +2.4~3.1dB，两口径待导师定主报）
- **次卖点（待定）**：切换方法作为"让盲全工作区可用的鲁棒性补丁"（D002 降级后，是否进正文/降附录/不提，待导师定 §4-Q2）
- **场景**：星地 FSO，Gamma-Gamma 强湍流，16APSK

## 1. 结构骨架（6 节 + 图表清单）

### §I Introduction（约 0.7 页）

| 写什么 | 来源/依据 | 文献 |
|---|---|---|
| 星地 FSO 相干通信背景 + 强湍流挑战 | R002/R004 调研 | Valjus 综述 sat.1553 |
| 载波相位恢复 DA vs NDA 两种思路 + 传统认知（导频稳赢）| 简报 v4 §1 表 | Du JLT 2021（方法源头）|
| **Gap**：强湍流下导频失效（deep fade 击穿导频段），盲反而鲁棒——这个现象没人量化过 | D004 归因 + R003 物理证据 | Paillier JLT 2020（强湍流对照）|
| 本文贡献（2-3 条，按导师定的主次）| 简报 v4 §4 | — |

**贡献条候选**（待口径定稿）：
1. 量化并归因强湍流下盲估计相对导频的净增益（主卖点）
2. 提出基于块有效 SNR 的估计器切换方法（若导师认可进正文，作为鲁棒性补丁）
3. （若需第三条）线宽敏感性分析证明增益非调参花招

### §II System Model（约 0.8 页）

| 写什么 | 图 | 来源 |
|---|---|---|
| 星地 FSO 信道模型（Gamma-Gamma 湍流，3 档强度）| **图1 系统框图** | params.py（参数真相源，禁引 SPEC.md）|
| 信号模型（16APSK，块结构，导频插入 spacing=4）| 同上 | _b11_params |
| 载波相位恢复两法：DA-ML / NDA-ML 公式 | — | formulas-master.md / Du JLT 2021 |
| 公平对照坐标 γ_tot（DA +1.25dB overhead）| — | fair_comparison.py |

**⚠️ 等导师**：场景参数（σ²_R 三档值）需核对是否"该报的强湍流"——R004 提醒我们的 σ²_R 可能比 Paillier(0.684) 更深，避免审稿人质疑工况设定。

### §III Proposed Method（约 0.8 页，若切换进正文）

| 写什么 | 图 | 来源 |
|---|---|---|
| 块有效 SNR 判据（接收端自测，不需真实信道）| — | _a4_switch_30seed_fixed.py decide() |
| 两层切换逻辑（CV 门控 + γ_eff 门控）| **图2 切换机制图**（crossover）| 主实验数据 |
| 切换阈值汇聚现象（~12-14dB 跨场景一致）| 同上 | — |

**⚠️ 等导师**：这整节是否存在取决于 §4-Q2（切换进正文/附录/不提）。若降附录，本节压缩到一段；若不提，删。

### §IV Results（约 1.5 页，核心）

| 写什么 | 图 | 数据 |
|---|---|---|
| BER vs SNR 曲线（6 场景或 4 场景）| **图3 主图** BER 曲线 | 30seed 主实验 + H002 补点 |
| 净增益表（fair/naive 两口径）| 表1 | _fair_gain_summary_30seed |
| 切换 vs 固定 DA/NDA（若进正文）| 图4 或表 | _a4_switch_30seed_fixed |
| 线宽敏感性（证明非调参）| 图5（可选）| linewidth_sweep |

**⚠️ 等导师**：
- 纵轴范围（10⁻⁵ 解读 A/B）—— 决定图画到哪
- 口径主报哪个 —— 决定表里哪个数加粗
- 子图数 4 还是 6（悬而未决1）

### §V Discussion / Limitations（约 0.5 页）

| 写什么 | 依据 |
|---|---|
| 强湍流 BER 衰减慢（非地板）的诚实说明 | H002 + 不变量5 |
| naive 口径下弱湍流无显著优势的诚实承认 | D004 |
| BER→0 增益坍塌（信息论必然）| D003 |
| 切换判据不完美（AWGN 误选 NDA）| H003 债务 |

### §VI Conclusion（约 0.3 页）

贡献重述 + 未来工作（消融/实测/其他调制）。

### 参考文献（约 0.5 页，估 15-20 条）

| 角色 | 文献 | 状态 |
|---|---|---|
| 方法源头 | Du JLT 2021 | ✅ 有 |
| 强湍流对照 | Paillier JLT 2020 | ✅ 有 |
| 综述 | Valjus sat.1553 | ✅ 有 |
| 导频理论 | Gävert TCOM 2022 | ✅ 有 |
| 导频类背景 | Zhou JLT 2013 | ✅ 有 |
| 同族盲(VV/BPS) | V&V 1983 / BPS 2009 | ✅ 有 |
| DPLL 异族 | Paillier JLT 2020（同上）| ✅ |
| **主对比方法** | ⏳ **候选已补搜，待核实+导师定** | 见下 |

### 主对比方法补搜候选（2026-07-10 tools/search，abstract 级未深核实）

搜"satellite FSO pilot-aided carrier phase recovery turbulence"得 15 篇，筛出 4 个最值得核实的候选：

| 候选 | 标题 | 年份/刊 | 相关性 | 备注 |
|---|---|---|---|---|
| **L009** | Phase and Channel Estimation for Phase-Asynchronous Mode-Division | 2024 JLT | 高 | JLT 顶刊+近年，相位估计，但偏 mode-division |
| **L010** | Enhanced frame synchronization and carrier recovery in coherent FSO | 2024 OE | 高 | **相干 FSO + 载波恢复**，场景最契合；R004 提到过"Wang OE 2024 未定位"可能即此 |
| L008 | A Noise-Tolerant Carrier Phase Recovery for Inter-Satellite Coherent | 2025 Electronics | 中 | 星间相干 CPR，但 Electronics 非顶刊 |
| L011 | A Low-Complexity Joint Compensation of Carrier Recovery for Coherent Free | 2023 Photonics | 中 | 相干 FSO 载波恢复，但 Photonics 非顶刊+2023 |

**判断**：L010（Wang OE 2024）场景最契合（相干 FSO + 载波恢复 + 近年）。但这些都是 abstract 级判断（守 R004 教训：web 断言需交叉验证全文）。**深核实等导师定了"主对比要什么类型"再做**——现在带候选清单给导师，比空等强。

## 2. 图表清单（4-6 图，待定稿）

| # | 图 | 类型 | 数据 | 状态 |
|---|---|---|---|---|
| 1 | 系统框图（场景+算法）| 框图 | — | ⏳ 待画（design-paper-figures）|
| 2 | 切换机制图（crossover）| 机制图 | 主实验 | ⏳ 待画 |
| 3 | BER vs SNR 主图 | 数据图 | 30seed+H002 | 🟡 有初版 fig2_ber_ext_merged，需重排 |
| 4 | 净增益 vs 湍流强度 | 数据图 | fair_gain summary | ⏳ 待画 |
| 5 | 线宽敏感性（可选）| 数据图 | linewidth_sweep | ⏳ 待画 |

**导师上次说**：框图（场景+系统，可合可分）+ 3-4 仿真图，效果好优先。按 asking.md 不能空问怎么画，得画初版再问。

## 3. 等 vs 不等导师的清单

**必须等导师（3 项，卡标题/主图/主对比）**：
- 10⁻⁵ 含义 A/B → 决定主图纵轴 + 主卖点成立性
- 口径主报 fair/naive → 决定标题数字 + 表加粗
- 主对比文献 → 决定参考文献核心一条

**不等导师，现在能做（本骨架已列）**：
- 结构骨架 ✅（本文件）
- 系统框图初版（design-paper-figures skill）
- BER 主图重排（数据齐）
- 净增益表整理（数据齐）
- 补搜主对比文献（tools/search）

## 4. 风险与债务

| 项 | 风险 | 处理 |
|---|---|---|
| 若导师=解读A（10⁻⁵要增益）| 主卖点绝症，需重找卖点 | 预案：转"工作范围鲁棒性"叙事，但需导师认可 |
| 切换降级后卖点够不够 CCISP | 单靠净增益量化归因是否够格 | 等导师 §4-Q5 |
| 主对比文献找不到 | 3 篇都不适合 | 补搜 + 请导师指 |
| σ²_R 工况设定被质疑 | R004 提醒可能比 Paillier 深 | §II 核对参数 |
| 7/20 截稿只剩 10 天 | 时间紧 | 骨架先搭，图并行画 |

## 5. 下一步执行顺序

1. **补搜主对比文献**（tools/search，现在做，结构化不爆上下文）
2. **画系统框图初版**（design-paper-figures skill，给提示词去新对话或子agent）
3. **BER 主图 + 净增益表重排**（数据齐，可子agent画）
4. 等导师 3 项反馈回来 → 填标题/主图纵轴/参考文献 → 过 external-output skill 写正文
