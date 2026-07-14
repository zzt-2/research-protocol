# PROMPT-018: Q-DP3 GW Step 4a 维度 A 正式竞争分解 — 四判据 + A0§1 致命项（含反向论证）

> 文件名: PROMPT-018-qdp3-dimension-A-competition.md
> 用途: 在新对话中执行。Q-DP3（预测性+即时 fade 检测驱动的跨帧 DSP 恢复）的正式方向评估，决定 Go/Kill
> 来源: D024（fade 前兆验证 PASS）+ R006（Q-DP3 合并定义 + 与 D003 子集关系）+ D003（Conditional Go 原始 4 条）
> 性质: **GW Step 4a 维度 A 竞争分解，这是 Go/Kill 判决，不是探索。** 用户明确警告"看起来这么好却没人做，感觉危险"——本任务的核心是查清"为什么没人做"。

## 0. TL;DR（先读）

你在 `projects/simulation/`（但本任务主要是文献+竞争分析，跑代码极少）。

Q-DP3 经过前置厘清（R006）+ 物理可行性验证（D024）后，到了正式 Go/Kill 判决。fade 前兆可辨识（85%，中位 9µs）+ hang-up recovery 是开放问题（Le Bidan 2023）——**看起来很好。但用户的核心担忧是对的：为什么这么好却没人做？**

**你的任务**：执行 GW Step 4a 维度 A 竞争分解（四判据 + A0§1 致命项），重点回答"为什么没人做"——如果找不到空白的结构性合理性解释，就是致命 Kill。

**最高纪律**：
1. A0§1 反向论证是本任务核心——不是"有没有先例"（R005 已查正面），是"**为什么没有**"
2. 不预设 Go。用户的危险感是合理的信号，你的默认立场应该是"找它死的原因"
3. 守 FR-25：Go 判据 = 赢传统未优化 baseline（被动冻结）；Kill 判据 = A0§1 致命 / 上界<0.5dB / MVE FAIL。Go/Kill 标准分离
4. 四判据过完才判 Go/Kill，不全过不强行包装

## 1. 必读（按优先级，全部必读）

1. `stages/gw-feasibility.md` **维度 A 全文 + A0§1 致命项 + A' 竞争维度分解**（本任务的执行规范）
2. `stages/glossary.md` **问题四判据 + 空白定义**（Go/Kill 的唯一拥有者）
3. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D003**（Q-DP3 原始 Conditional Go + 4 条 Conditional）+ **D024**（fade 前兆验证 PASS + Q-DP3 更新定义）+ **D023**（A 边 D022 收窄——B 边的相对优势）
4. `.sessions/2026-07-10-dual-pol-osl-groundwork/R006-qdp3-prerequisite-clarification.md`（Q-DP3 合并定义 P2.4 + 与 D003 子集关系 + 检测对象锁 fade）
5. `projects/thesis-fso/feasibility_report.md` **Q-DP3 评估节**（L580+，D003 原始竞争分析）
6. `projects/thesis-fso/literature_notes.md` Q-DP3 节（L842）+ L-DP5/L-DP6/sat.1553 + 角度素材占点地图
7. `thesis-lessons.md` **TL-30**（跳框架教训）+ **TL-27**（oracle 上界 Kill 工具）+ **TL-04/TL-12**（增量非填补空白）
8. `papers/_read_notes/` L-DP5（ICSOS.10490279）/ L-DP6（WiSEE.10850117）/ sat.1553 精读笔记

## 2. Q-DP3 合并定义（来自 D024 + R006 P2.4，评估对象）

- **M** = 预测性 + 即时混合 fade 检测驱动的跨帧 DSP 恢复
  - 完整方法链：前兆检测（h(t) 趋势预测 fade，85% 可辨识，中位提前 9µs）→ 状态机门控（连续 N block 触发，抑制误报）→ 触发恢复动作（压 μ/冻结/快速重锁定/模式切换）→ 性能指标（outage 概率/恢复时间/dB 增益）
  - 对无趋势的 ~15% 事件：即时检测（h 跌破阈值触发）兜底
- **C** = 双偏振星地相干 FSO（intradyne 单孔径单链路 GG 湍流 LEO，帧间衰落）
- **A** = L-DP5（Le Bidan 2023）点名"深衰落跨帧挂起恢复 open, requires further work" + L-DP6 DSP outage（BER>0.44）实证 + sat.1553 仅有响应性被动冻结无主动恢复

**关键约束**：检测对象 = fade（h 下降），不是 divergence（前兆存疑 + μ 主导用调 μ 就能防）。预测性是硬约束（否则退化 JR-CMA 响应性重置）。

## 3. 要执行的评估（维度 A 完整流程）

### Step A0：致命项检查（FR-01，最重要）

**A0§1 空白的结构性合理性 —— "为什么没人做？"（用户的核心担忧，本任务重点）**

空白"看起来太干净"时的强制检查：如果这个空白如此明显且可行，必须找到**结构性原因**解释为什么前人没做。找不到 = 致命 Kill。

候选解释（逐一查证，不预设哪个对）：

- **(a) "沉默的 Kill"——有人试过但不行**：查 L-DP5/L-DP6/sat.1553 的**全文**（不只 abstract），看有没有"我们考虑过预测性检测但发现 dB 增量太小/误报太多/不值得"的讨论。查 L-DP5 的 "future work" / "limitations" / "discussion" 段落原文。查是否有相关会议论文做了 fade-triggered DSP 但结论负面。
  - 检索关键词：fade-triggered equalizer、proactive DSP recovery、predictive CMA restart、channel-aware equalizer reconfiguration（+ negative result / limitation / not worth / marginal improvement）
  - **这是最危险的解释——如果有人做过且结论是"不行"，论文通常不会明说，要从 limitations/future work 的措辞里嗅出来**

- **(b) "物理可行 ≠ 工程值得"——dB 增量可能太小**：R7（冻结 μ=0 完全无效）的阴影。如果 fade 期间压步长/冻结本身就救不了多少 BER，预测性的增量价值就有限。查：光通信 DSP 恢复的 dB 增益文献，CMA 重锁定/重训练的恢复时间 vs fade 持续时间的比值。如果典型 fade 持续时间（τ_c 量级，f_G=100 时 ~1.6ms）远短于 CMA 重收敛时间（~10⁴-10⁵ 符号），那"检测到 fade 也来不及恢复"——这是物理 Kill。
  - 查 fade 持续时间分布（S004 的 GG 时间模型可估算 AFD）vs CMA 重收敛时间（文献）

- **(c) "社区小 + 问题新"——真空白**：LEO 相干光通信 + DSP 级 fade 管理这个交叉确实小众。验证：相关论文数量（L-DP5/L-DP6/sat.1553/JR-CMA 就几篇）、社区活跃度、技术成熟度（LEO 相干光通信是否刚起步）。如果社区确实小 + Le Bidan 2023 刚列为 open，这个解释成立。
  - 但注意：这个解释最乐观也最需要证据支撑，不能因为"我希望它对"就采信

- **(d) "有人做了但不在光通信"——RF/光纤有迁移可能**：RF 通信的 loss-of-lock 检测 + 恢复、光纤的 OPM（optical performance monitoring）+ 告警。查这些领域有没有"预测性检测 + 触发"的成熟方案，如果有，Q-DP3 可能只是迁移非原创。
  - R005 提到 RF 长程预测（Adeogun 2025/Heidari 2006）是成熟范式——查它们有没有做到"预测 → 触发 DSP 响应"

**A0§1 产出**：四个解释各给证据强度（强/中/弱/无）+ 判定（哪个最可能）。如果 (a) 或 (b) 强，A0§1 致命。

**A0 其他致命项**：
- A0§6 物理量级：fade 持续时间 vs 恢复时间的比值（承接 b）——如果 fade 比 CMA 重收敛短太多，物理死
- A' 竞争维度：Q-DP3 竞争的"深衰落恢复"维度先验覆盖度（D003 原判"最低"，R005 确认 FSO 算法层无先例——但本任务的 A0§1 反向论证可能修正这个判断）

### Step 1：四判据（glossary.md 唯一拥有者）

完成 A0 后过四判据：

| 判据 | Q-DP3 现状 | 要查/补的 |
|---|---|---|
| ① 空白真实性 | R005 确认 FSO 算法层无先例 | A0§1 反向论证可能修正 |
| ② 增量可定义 | "被动冻结 → 主动预测性恢复" | 须区分 vs JR-CMA 响应性 + vs sat.1553 被动冻结 |
| ③ 物理基础 | D024 验证 fade 前兆可辨识 | A0§6 fade vs 恢复时间比 |
| ④ 对手存在 | L-DP5 被动冻结（传统未优化 baseline，FR-25）| 确认是"传统未优化"非"已优化强 baseline" |

### Step 2：Go/Kill 判定（FR-25 标准分离）

- **Go** = 四判据全过 + A0§1 找到空白的结构性合理解释（非致命）+ 赢传统未优化 baseline（被动冻结）的前景
- **Kill** = A0§1 致命（沉默 Kill / 物理不可行 / 纯迁移非原创）/ 上界 <0.5dB（FR-21，TL-27）/ 四判据不全过

**注意**：这里的 Go 是"进入维度 D MVE"的 Go，不是"方向成功"的 Go。Go 之后还要 MVE 验证 dB 增益。

## 4. 执行方式

- **主要是文献分析**（L-DP5/L-DP6/sat.1553 全文精读 + 检索）
- 文献：`tools/search` + `tools/search --source cnki` + 已有论文库 `papers/_read_notes/` + `papers/` 下原文
- **L-DP5/L-DP6 全文必读**（不只 abstract）——A0§1(a) 沉默 Kill 的证据在 limitations/future work 段落
- web 检索在子 agent 里做（AGENTS.md 上下文管理规则），每篇 ≤500 词摘要
- 代码：若需估算 fade 持续时间 vs CMA 重收敛时间，用现有 GG 时间模型（`common/_gg_time.py`）算 AFD，不跑均衡器

## 5. 已知陷阱（本任务专属，从教训来）

1. **PROMPT-011 教训**：DD-CMA/酉约束是成熟先例，直接实现翻车。Q-DP3 的"恢复"部分如果只是已有方案的组合（JR-CMA 重置 + sat.1553 冻结），要标"非原创"
2. **A0§1 不要自我安慰**：用户说"感觉危险"是对的。你的默认立场是找它死的原因，不是找它活的理由。如果四个解释都不成立（既没沉默 Kill、物理也行、社区不小、RF 也没迁移），那"空白如此干净"本身就是 A0§1 致命信号——**好得不真实**
3. **R7 冻结无效的阴影**：D003 风险③ + A0§6。冻结 μ=0 完全无效（S008 R7）。Q-DP3 的恢复动作如果包含冻结，R7 说不行。压 μ（非冻结）未测但可能也不行。**如果恢复动作本身救不了 BER，预测性检测就没有载体**——这是物理 Kill
4. **fade vs divergence 别混**（R006 前置1）：Q-DP3 检测的是 fade 不是 divergence。divergence 由 μ 主导（调 μ 就防），不需要预测。评估时别把两者混为一谈
5. **FR-25 对手标准**：Go 判据的对手 = 传统未优化 baseline（L-DP5 被动冻结）。JR-CMA（误差阈值重置）是更强的 baseline，Q-DP3 要赢它才真有增量——但 Go 阶段先用弱对手，MVE 阶段再碰强对手
6. **TL-27 上界**：若可解析估算恢复的 dB 上界（如 fade 期间最优 MMSE vs 被动冻结的 BER 差），<0.5dB 直接 Kill 不跑 MVE

## 6. 产出格式（强制）

```
# PROMPT-018 研究报告：Q-DP3 维度 A 竞争分解

## TL;DR
[Go / Kill + 一句话理由 + A0§1 的判定]

## A0§1：为什么没人做？（四解释逐一查证）
### (a) 沉默的 Kill
[L-DP5/L-DP6/sat.1553 全文 limitations/future work 原文 + 检索负面结果]
### (b) 物理可行 ≠ 工程值得（dB 增量）
[fade 持续时间 vs CMA 重收敛时间 + R7 阴影]
### (c) 社区小 + 问题新
[论文数量 + 社区活跃度 + 技术成熟度]
### (d) RF/光纤有迁移
[loss-of-lock / OPM 预测性检测成熟方案]
### A0§1 判定
[哪个解释最可能 + 证据强度 + 是否致命]

## A0 其他致命项
### A0§6 物理量级
[fade vs 恢复时间比]
### A' 竞争维度
[Q-DP3 维度先验覆盖度，R005 判断 + A0§1 修正]

## 四判据
[①②③④ 逐项 PASS/FAIL + 证据]

## Go/Kill 判定
[按 FR-25 标准分离 + 引用具体证据]

## 若 Go：维度 D MVE 的设计建议
[MVE 该验证什么（dB 增益 / 误报率 / 恢复时间）+ oracle 上界估算（FR-21）]
## 若 Kill：死因 + 可复用部分

## 对主控决策的建议
[方法层战略：Q-DP3 vs Q-CMA-FADE 的最终判断]

## 检索记录 + 全文精读记录
```

## 附：决策上下文（你了解即可）

- 路线 A（Q-CMA-FADE ML）已 Go 但被 D023 收窄（ML 优势 N=2M 多参数点不普适）
- 路线 B（Q-DP3）是天花板更高的候选，但用户担心"好得不真实"
- 若 Q-DP3 也 Kill，方法层只剩 A 保底（低天花板）或回候选池重选
- 分析层（发散 μ 主导 + SOP 交换 + GG 时间模型）无论 A/B 都稳，是最确定的论文产出
