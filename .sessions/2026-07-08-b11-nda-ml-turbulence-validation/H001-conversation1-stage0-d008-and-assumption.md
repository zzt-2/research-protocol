# Handoff: 对话 1 — 阶段 0.1-0.6 前置规约（D-008 耦合门控 + B11 行 33 假设核查 + 架构 + 公平对照 + 参数 + 文件）

> 来源: S001（主控对话开题）| 交接目标: 新工作对话执行阶段 0.1-0.6 六项规约
> 文件名: H001-conversation1-stage0-d008-and-assumption.md
> 日期: 2026-07-08

## 到哪了（状态）

主控对话开题完成（D001），阶段 0 六项规约设计完成。**未写代码，未进 sandbox**。

**关键依赖（工作对话首核查）**：
- B11-Q2 依赖 NDA-ML D-008 双 bug 修复（漏 ML 加权 + 升幂未归一化）
- D-008 修复前禁跑 B11-Q2 sandbox（vs VV 持平是 bug，bug 没修跑湍流验证无意义）
- 阶段 0 规约设计不依赖 D-008 修复，可并行推进

## 不要做什么

1. **不要 D-008 修复前跑 sandbox**：vs VV 持平是 bug，bug 没修跑湍流验证等于在错误基础上加验证维度
2. **不要跳阶段 0 直接写代码**：profile 第 9 次防线 + INVARIANT 6
3. **不要走环路 TF 联合建模**：B11 是前馈闭式 ML，B11-Q2 必须走前馈路径（合法不撞 D006）
4. **不要把 B11-Q2 当从零开始的独立候选**：是 NDA-ML B11-Q1 的湍流验证延伸，复用 nda_ml/da_ml + 湍流信道
5. **不要自建信道**：从 common/_channel.py 导入（TL-13）
6. **不要污染 common**：explore 探针不进 experiments

## 必读（按优先级）

1. **本 H001 + topic-index**（14 不变量，重点 11/12/13/14 B11-Q2 特殊）
2. **S001** 开题 + 复用基建盘点
3. **NDA-ML D-008 决策**（`.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-008 完整条目）—— 阶段 0.1 核查对象
4. **B11 锚论文全文**（`papers/doi/10.1109_lpt.2024.3523478/content.md`）—— 阶段 0.2 核查行 33 假设
5. **NDA-ML B11-Q1 基建**：
   - `projects/simulation/common/_recovery.py` — nda_ml_recovery (L171) + da_ml_recovery (L136)
   - `projects/simulation/common/_channel.py` — gg_block + doppler_phase + generate_shared_realization_apsk
   - `projects/simulation/simulator/sc_nda_ml_sim.py` — fft_foe_m0_omega (L137) 两阶段粗估
6. **sim-preflight v1.3.0**：rules/mve-validation.md V1-V6 + rules/interrupt.md 10-12 + SKILL.md §1.6 C6-C8
7. **框架文件**：stages/gw-feasibility.md §D + thesis-lessons TL-13/20/26
8. **上游决策链**：`.sessions/2026-06-20-problem-driven-redirection/decisions.md` D005/D006/D017/D018
9. **B2 Kill 教训**：`.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/decisions.md` D004/K001 — 前馈化导致测度失效的教训对 B11-Q2 有警示

## 下一步干什么（对话 1 = 阶段 0.1-0.6，不写代码）

### 步骤 1：报到 + 重读关键文件

报到（session-governance Trigger 1）+ 读必读清单 1-9。

### 步骤 2：阶段 0.1 D-008 耦合依赖门控（B11-Q2 最高优先）

> INVARIANT 11（B11-Q2 特殊）前置。

**0.1a 核查 NDA-ML D-008 修复状态**（派子 agent，≤15 分钟）：
- 读 `.sessions/2026-07-06-step4a-mve-execution/decisions.md` D-008 完整条目
- 核查 D-008 status（pending_fix / in_progress / fixed）
- 核查 NDA-ML 方法方向 X/W 是否已拍板（X=换改进 VV / W=segmented+高线宽）
- 核查 sandbox 验证是否已跑（D-008 修复后的 sandbox 结果）

**0.1b 判定 B11-Q2 sandbox 前置条件**：
- D-008 已修复 + sandbox 验证 NDA-ML 修复版 vs VV 不再持平 → B11-Q2 可进 sandbox（阶段 0 做完后）
- D-008 未修复 / 方法方向未拍板 / sandbox 未跑 → B11-Q2 阶段 0 做完等 D-008 修复
- 输出 `explore/b11-nda-ml-turbulence-validation/_d008_dependency_check.md`

### 步骤 3：阶段 0.2-0.6（主线定）

**0.2 B11 行 33 假设核查**（INVARIANT 13 B11-Q2 特殊）：
- 读 B11 锚论文全文（`papers/doi/10.1109_lpt.2024.3523478/content.md`）
- 核查行 33 "湍流/Doppler/CFO 已补偿"的具体含义
- 判定：仿真简化（B11 没测湍流，加湍流是真实缺口）还是物理假设（B11 假设湍流可前置补偿，需评估前置补偿可行性）
- 输出 `explore/b11-nda-ml-turbulence-validation/_b11_assumption_audit.md`

**0.3 架构定性**（INVARIANT 12 B11-Q2 特殊 + D006）：
- B11 是前馈闭式 ML（无环路 TF），前馈 ML 似然纳入湍流 |R(k)| 时变不撞 D006
- 确认 B11-Q2 走前馈路径
- 输出 `explore/b11-nda-ml-turbulence-validation/_architecture_decision.md`

**0.4 公平对照框架**：
- baseline 是 DA-ML（B11-Q1 用过）还是 NDA-ML 无湍流版（B11-Q1 AWGN 结果）？
- fair gain @ HD-FEC 3.8e-3（跟 NDA-ML/B7/B5 跨候选可比）
- 输出 `explore/b11-nda-ml-turbulence-validation/_fair_comparison_framework.md`

**0.5 参数真相源前置**（TL-26 + FR-26）：
- 湍流参数 Cn²/σ²（参考 Paillier / sat.1553，读原文数值）
- 线宽 + 符号率 + (8,8)-16APSK 配置（跟 NDA-ML 统一，D-007 LASER_LW 单字段）
- 输出 B11-Q2 Params 草稿

**0.6 文件组织规约**：
- `explore/b11-nda-ml-turbulence-validation/` 目录 + 命名规则
- 下游引用同步清单

## 纪律

1. **profile 第 9 次防线 + INVARIANT 6**：阶段 0 六项规约全做完才进 sandbox
2. **INVARIANT 11 D-008 耦合依赖门控**（B11-Q2 特殊）：D-008 修复前禁跑 sandbox
3. **INVARIANT 12 D006 边界确认**（B11-Q2 特殊）：前馈 ML 不撞 D006，禁环路 TF
4. **INVARIANT 13 B11 行 33 假设核查**（B11-Q2 特殊）：仿真简化 vs 物理假设必须查清
5. **INVARIANT 14 复用基建**（B11-Q2 特殊）：nda_ml/da_ml + 湍流信道全有，不需新建
6. **sim-preflight v1.3.0 C6-C8 + V1-V6**
7. **TL-26 参数溯源 + 读原文数值**
8. **TL-13 共用同一信道**
9. **核查机制中性双向**

## 接收方验证

- [ ] 已读取 topic-index 14 不变量（重点 11/12/13/14 B11-Q2 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] NDA-ML D-008 双 bug（漏 ML 加权 + 升幂未归一）（核查 step4a-mve-execution/decisions.md D-008）
  - [ ] B11 行 33 假设"湍流/Doppler/CFO 已补偿"（核查 B11 锚 content.md 行 33）
  - [ ] B11 前馈 ML 不撞 D006（核查 _recovery.py nda_ml_recovery L171 是前馈闭式）
- [ ] 已检查 _registry.yaml 中本专题 depends_on
- [ ] 已确认当前范围未违反"明确不含"

## 下一轮

**对话 2**（阶段 0.1-0.6 完成后 + D-008 修复后）：
- 阶段 1 sandbox（NDA-ML 修复版 vs DA-ML 在湍流下三方对照）
- 守 sim-preflight v1.3.0 V2 三方对照 + V3 祖师爷警报
- sandbox 发现 NDA-ML 在湍流下 +2dB 消失 → 红线警报（核心命题崩塌）

**对话 3**（sandbox 通过后）：
- 阶段 2 TL-20 理论预期表 + 阶段 3 MVE + consistency
