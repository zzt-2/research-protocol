# [S025] Contract S0-S3 执行（新颖性确认 + 瓶颈诊断 + 指标审计 + 参数溯源）

> 2026-07-15 | Contract 阶段 S0-S3 | 状态：完成

## 目标

从 GW Step 4a 进入 Contract 阶段，按 stages/contract.md S0-S5 流程冻结 Q-CMA-FADE 形态。本轮聚焦 S0-S3（前 4 步），下轮做 S4-S5-冻结。

## 记录

### Session Start + Handoff 验证

收 H010（GW→Contract handoff）。按 governance Trigger 5 验证 3 条关键事实：
- **事实 1（D022 ML 29/30, p=1.19e-6）PASS** — prompt015_unified_baseline.json 完全匹配
- **事实 2（D014 SOP=0 ratio=1.0）FAIL** — 无独立 JSON，仅 decisions.md 文字+源码确认。**触发债务处理**
- **事实 3（D029 改动1 D=B, D1/D2 0%触发）PASS** — prompt022_modification1_mve.json 完全匹配

事实 2 FAIL 是真问题：D014 是分析层核心贡献"SOP 极化串扰是 BER 真因"，论文要写但无可复现脚本。**用户决策：Contract 阶段就补脚本**（不推 Execute）。

### Contract S0：方案新颖性检索

复用条件满足（contract.md L34：literature_notes 29 篇精读 + Step 3.5 已完成）→ 跳过 0.1 系统检索。

**reframe 后增量定位冻结**：旧叙事"ML 缓解发散"已被 D014 证伪。新叙事 = 分析层 D014（SOP 极化串扰是 BER 真因）+ 方法层 D022（ML PI 优势）焊一起。

不换皮判定成立——Q-CMA-FADE 分析层 7 项稳结论（发散 μ 主导 / SOP 串扰真因 / CMMA 不降发散 / 冻结无效 / LCR 伪相关 / GG 时间模型 / swap 永久锁定）**Qin/Nasr 全空白**；方法层窄域 PI 优势 + 架构迁移诚实标注。

### Contract S1：瓶颈诊断

引用 D014（已完成瓶颈诊断）：
- **瓶颈类型**：表达力/结构性瓶颈——恒模代价多解地形 + SOP 持续旋转 → 极化锁定跳变
- **天花板估算**：SOP=0 时 CMA=oracle ratio=1.0（prompt023 复现），说明 CMA 架构本身不瓶颈；SOP>0 时 ratio 1.9-6.9×
- **解决方案匹配**：ML 固定权重绕过恒模多解（非修复 CMA）。诚实标注场景迁移非架构创新

### Contract S2：指标模型审计（FR-17/FR-19/D018）

**FR-17 子 agent 抽查 8 篇核心 + 4 篇辅助**（search-archive/2026-07-15/，67 篇去重）：
- **PI-BER 首选率 0%**（67 篇零命中"permutation-invariant BER"）——PI-BER 是 Q-CMA-FADE/D018 自定义口径，非领域标准命名
- **fixed-label BER 首选率 75%**——领域通行首选指标
- **发散概率**是领域认可指标（CA-CMA #3 显式报告）

**FR-17 处置**：触发"首选率<50% 必须补领域通行指标"。原拟 PI-BER 做主指标 → 改 **fixed-label BER 做主指标（领域首选 75%）+ PI-BER 降辅指标（Q-CMA-FADE 特色诊断口径）+ 发散概率 + PI ratio 做分析层指标**。

**FR-19 模型假设敏感性**：PI-BER 依赖穷举消歧（假设 pilot/帧头开销）；发散概率依赖 norm>10×init 判据（D010 阈值敏感性已测）。

**D018 双口径强制保留**：fixed/PI 必须并报。

### Contract S3：参数溯源审计（FR-20）

**D014 SOP=0 矩阵债务填补 PASS**（子 agent prompt023）：
- 新建 `prompt023_sop0_matrix.py`（隔离脚本，import 复用 prompt019 StandardCMA2x2 + ml_long_seq_failure gen_channel/oracle_equalize，不改 common/）
- 30 runs（5 seeds × 2 SOP × 3 f_G）428s 全跑完
- **复现矩阵（PI-BER 口径）**：SOP=0 全档 ratio=1.00-1.01，SOP=4e-7 ratio=1.12-6.93
- **方向一致性 PASS**：SOP=0 显著低于 SOP>0，D014 核心声称"SOP 是 BER 恶化主因"强化复现
- **比 D014 原矩阵更强**：SOP=0 f_G=1000 也 ratio=1.01（D014 原报 4.2×，PI 口径下纯跟踪滞后不显著）
- JSON: `results/cma-fade-divergence/prompt023_sop0_matrix.json`

**参数溯源**：所有 [ASSUMPTION] 消除。SOP_RATE=4e-7 标 sat.1553 §6.3 仿真值（已知债务：非实测，论文 limitations 标注）。

### contract.md draft 创建

`projects/thesis-fso/contract.md`（status: draft）含完整字段：Problem Reference / Hypothesis（H1 分析层强 + H2 方法层弱窄域）/ Success Signal / Failure Signal / Baselines（B1-B4）/ Metrics（M1-M4，FR-17 调整后）/ Fairness Rules（F1-F5）/ Ablation Plan（A1-A5）/ Experiment List（E1-E8）/ Simulation Config / 数据集设计 / Parameter Provenance（全标来源）/ 声称-证据映射（C1-C5）。

## 决策引用

- 无新建 D###（本轮是 Contract 流程执行 + 债务填补，无架构/方向决策变更）
- **引用现有**：D014（SOP 真因，S1 瓶颈诊断）/ D022（ML 29/30，H2 假设）/ D018（双口径强制，S2 指标）/ D023（窄域收窄，H2 适用边界）/ D029（改动1 Kill，方法层定型弱）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。Contract 阶段是 GW 原始目标"找到真问题+合法贡献形态"的自然延续（Contract 冻结 = 形态定型最后一步）。S0-S3 是 contract.md 定义的强制流程。

## 后续

**下轮（S4-S5-冻结）**：
1. **S4 端到端推演**：新建 data-flow.md（8 步推演 + FR-13 动作空间审计 + FR-16 架构信息增量审计）
2. **S5 压力测试 + 反模式审查 + 实验完备性对标**：5 问压力测试 + 反模式 4 项 + experiment_completeness_checklist.md（Tier 1 门控）
3. **Step 6 冻结**：用户确认后 contract.md status: frozen + 写 H011 handoff 交 Execute 阶段

**本轮未决项**：
- FR-17 处置需用户确认：主指标从 PI-BER 改 fixed-label BER 是否接受（PI-BER 降辅指标）。这是 Contract 字段调整，不影响假设/信号。
- H011 handoff 待下轮 Contract 冻结后写（本轮不写，因 Contract 未冻结）
