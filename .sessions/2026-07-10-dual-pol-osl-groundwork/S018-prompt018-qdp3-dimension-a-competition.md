# [S018] PROMPT-018 Q-DP3 维度 A 竞争分解 — A0§1 反向论证非致命，Conditional Go 进 MVE

> 2026-07-14 | GW Step 4a 维度 A | 状态：完成
> 来源: PROMPT-018 / D024（fade 前兆验证 PASS）/ R006（Q-DP3 合并定义）/ D003（原始 Conditional Go）

## 目标

执行 Q-DP3（预测性 fade 检测驱动的跨帧 DSP 恢复）的 GW Step 4a 维度 A 正式竞争分解（四判据 + A0§1 致命项），重点回答用户核心担忧"为什么这么好却没人做"——A0§1 反向论证四解释（沉默Kill/物理不值得/社区小/RF迁移）逐一查证。Go/Kill 判决。

## 记录

### 执行方式

3 子 agent 并行 + 主控集成判定：
1. **子 agent #1（A0§1a 沉默 Kill）**：逐字精读 L-DP5/L-DP6/sat.1553 全文 content.md 的 limitations/future work 段落
2. **子 agent #2（A0§1b 物理量级）**：用现有 GG 时间模型（`common/_gg_time.py`）跑 20 seeds × 10⁷ 符号统计 fade AFD + 查 sat.1553 CMA 收敛时间 + R7 冻结无效阴影分析
3. **子 agent #3（A0§1c+d 社区/迁移）**：13 次 WebSearch 查社区规模 + RF/光纤迁移 + 负面结果

### A0§1 四解释查证结果

| 解释 | 证据强度 | 致命？ | 关键证据 |
|---|---|---|---|
| (a) 沉默 Kill | **无** | 否 | 三篇均无"试过预测性但不行"痕迹。L-DP5 纯 open problem（"requires further work"零尝试）；L-DP6 future work 方向相反（降 outage threshold）；sat.1553 L582 明确"穿过 fade 跟踪 SOP 更好"倾向主动 + L764 主动提名动态步长 |
| (b) 物理可行≠工程值得 | **中** | 否（MVE 硬约束） | fade AFD=10.12µs（实测 20 seeds）vs CMA 重收敛=40µs（sat.1553 L757-258 换算）→ 比值 0.25，CMA 重锁定对典型 fade 物理死。但压μ响应=40ns（比值 253，时间窗充足），DA-LMS=4µs（能塞进）。R7 硬冻结(μ=0)无效已证，压μ未测 |
| (c) 社区小+问题新 | **中** | 否（提供结构性合理解释） | LEO 相干光整体社区升温（非小众），但"预测性 fade 触发 DSP 恢复"交叉切口确实小众——Le Bidan 2023 仅 3 引无人接续，sat.1553 未覆盖。**这恰好解释了"为什么没人做"** |
| (d) RF/光纤迁移 | **弱（不成立）** | 否 | RF loss-of-lock 预测性方案不存在（niche 本身）；光纤 OPM 预测触发在网络层非 DSP 块；RF 长程预测触发 AMC 非 DSP。三条迁移路径均未直达 Q-DP3，新颖性保留 |

### A0§1 核心判定

**空白的结构性合理性已找到**：(c) "交叉切口小众+问题新"是"为什么没人做"的合理解释——LEO 相干光 × DSP 级 fade 管理 × 预测性检测三叉交叉确实窄，Le Bidan 2023 刚点名 open 且无人接续。用户"好得不真实"的核心担忧**在"为什么没人做"层面已解除**。

**但 (b) 的工程未知是进 MVE 的硬约束**：压μ（非冻结）能否救 BER 决定预测性检测有没有载体。R7 硬冻结无效，压μ从未测过。这不是 A0§1 致命（A0§1 问"为什么没人做"，(c) 已回答），是维度 D MVE 要验证的。

### A0 其他致命项

- **A0§6 物理量级**：轻量响应（压μ/切换）时间窗充足（AFD/压μ=253），CMA 重锁定路径物理死。Q-DP3 恢复动作必须限定为轻量响应，与 R006 P2.4 一致。
- **A' 竞争维度**：Q-DP3 竞争的"预测性 fade 检测驱动恢复"维度先验覆盖度**最低**（D003 原判 + R005 确认 + A0§1(c) 证实交叉切口小众）。R005 判断经 A0§1 反向论证后仍成立——(a) 无沉默 Kill、(d) 非简单迁移均未修正。

### 四判据（全过）

| 判据 | PASS/FAIL | 证据 |
|---|---|---|
| ① 具体技术矛盾 | PASS | M-C-A 明确（R006 P2.4 合并定义） |
| ② 有方法产出形态 | PASS | 恢复机制设计 = 可复用 design rule |
| ③ 有近期 baseline | PASS | L-DP5 被动冻结 = 传统未优化 baseline（FR-25） |
| ④ 能做可量化对标 | PASS | 恢复时间/outage 概率/dB 增益 |

### Go/Kill 判定：Conditional Go（进维度 D MVE）

**Go 标准**（赢传统未优化 baseline 前景）：四判据全过 + A0§1 非致命 + A' 先验覆盖度最低 + FR-21 不触发（outage 50%→0 量级改善）+ 轻量响应时间窗充足。

**Kill 标准**：A0§1 不致命 / 四判据全过 / FR-21 不触发 → **不 Kill**。

**Conditional 条件**（进 MVE 前必须验证）：**压μ（非冻结）在 fade 期间的 BER 增益**——第一优先验证项，决定方向生死。若压μ也救不了 BER（像 R7 冻结一样），预测性检测没有载体 → 物理 Kill。

### MVE 设计建议

1. **生死验证**：CMA 常规 μ=1e-3 vs CMA fade 期间压 μ=1e-4（功率阈值触发）vs oracle。PASS=压μ显著低于常规且接近 oracle。
2. **若压μ PASS**：预测性压μ vs 响应性压μ vs 常规（三对照），验证预测性增量（区分 vs JR-CMA 响应性）。
3. **oracle 上界**（FR-21）：fade 期间最优 MMSE vs 被动冻结 BER 差 = 恢复上界，需用真实 GG 时间模型估算。

详见 `PROMPT_018_REPORT.md`。

## 决策引用

- D003：Q-DP3 原始 Conditional Go（4 条 Conditional，本任务验证第 4 条 fade 前兆可辨识性已 PASS via D024，A0§1 非致命补强）
- D024：fade 前兆验证 PASS（85% 事件提前 ≥2µs）——本任务前置
- R006：Q-DP3 合并定义 P2.4 + 与 D003 子集关系——本任务评估对象来源
- D023：ML 优势 N=2M 不普适——本任务方法层战略判断背景（Q-DP3 天花板未受影响）
- **D025（新建）**：Q-DP3 维度 A 竞争分解 Conditional Go——A0§1 非致命 + 四判据全过 + 压μ能否救 BER 为 MVE 生死前置

## 范围确认

- 本轮是否在 scope boundary 内：**是**（GW Step 4a 维度 A 候选评估，属原始目标"GW Step 1-4a 完整流程"范围）

## 后续

1. **用户确认 Q-DP3 Conditional Go**（守 FR-22 + 4a 决策必须用户确认）
2. 若确认 → **维度 D MVE 第一优先**：压μ（非冻结）fade 期间 BER 增益验证（1 天内可出，决定方向生死）
3. 若压μ PASS → 预测性 vs 响应性增量验证（Q-DP3 核心创新点）
4. 方法层战略：压μ PASS → Q-DP3 优先（天花板未受 D023 影响）；压μ FAIL → Q-DP3 Kill，回路线 A（D022 + 改动1）保底
5. **feasibility_report Q-DP3 节需更新**：补 A0§1 反向论证结论 + 压μ MVE 前置 + sat.1553 L757-258 有利证据 + AFD 数据修正（feasibility_report 原记帧时长有误，topic-index 已记债务）
