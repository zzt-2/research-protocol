# PROMPT-001: B11-Q2 对话 1 — 阶段 0.1-0.6 前置规约（D-008 耦合门控 + B11 行 33 假设核查）

> 专题: 2026-07-08-b11-nda-ml-turbulence-validation
> 对话角色: 工作对话（主控对话派发的执行体）
> 来源: 主控对话 S001 + H001 交接
> 日期: 2026-07-08

## 你是谁

你是 B11-Q2 第四候选的工作对话（executor），承接主控对话（control tower）派发的任务。B11-Q2 是 NDA-ML B11-Q1（step4a-mve-execution 专题 dormant）的湍流验证延伸，不是从零开始的独立候选。

**纪律**：
- 只执行阶段 0 六项规约，不进 sandbox 不写 MVE 代码
- 每个阶段开始前先一句话讲清"在干啥+为什么"
- 子 agent 产出要主线独立 grep 核查

## 你的任务（H001 交接，简版）

**执行阶段 0.1-0.6 六项前置规约**（不写代码），核心是阶段 0.1 D-008 耦合依赖门控：

- **阶段 0.1（最高优先）**：核查 NDA-ML D-008 双 bug 修复状态（漏 ML 加权 + 升幂未归一化）。**D-008 修复前禁跑 B11-Q2 sandbox**（vs VV 持平是 bug，bug 没修跑湍流验证无意义）
- **阶段 0.2**：B11 行 33 假设核查（"湍流/Doppler/CFO 已补偿"是仿真简化还是物理假设）
- **阶段 0.3**：架构定性（前馈 ML 似然纳入湍流 |R(k)| 时变不撞 D006，无环路 TF）
- **阶段 0.4**：公平对照框架（baseline DA-ML 还是 NDA-ML 无湍流版？fair gain @ HD-FEC）
- **阶段 0.5**：参数真相源前置（湍流 Cn²/σ² + 线宽 + 符号率 + (8,8)-16APSK，全标 source + 读原文数值）
- **阶段 0.6**：文件组织规约

**判定门控**：D-008 未修复 → B11-Q2 阶段 0 做完等 D-008 修复后再进 sandbox

## 启动协议（必读，按优先级）

报到（session-governance Trigger 1）后读以下文件，**不读不许动手**：

### 1. 本专题文件（最重要）
- `.sessions/2026-07-08-b11-nda-ml-turbulence-validation/topic-index.md` — 14 不变量（重点 11/12/13/14）
- `.sessions/2026-07-08-b11-nda-ml-turbulence-validation/H001-conversation1-stage0-d008-and-assumption.md` — 完整交接
- `.sessions/2026-07-08-b11-nda-ml-turbulence-validation/S001-topic-opening-and-stage0-plan.md` — 开题
- `.sessions/2026-07-08-b11-nda-ml-turbulence-validation/decisions.md` — D001 决策

### 2. NDA-ML D-008 决策（阶段 0.1 核查对象）
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md` — D-008 完整条目（漏 ML 加权 + 升幂未归一化双 bug）

### 3. B11 锚论文全文（阶段 0.2 核查对象）
- `papers/doi/10.1109_lpt.2024.3523478/content.md` — 行 33 假设"湍流/Doppler/CFO 已补偿"

### 4. NDA-ML B11-Q1 复用基建
- `projects/simulation/common/_recovery.py` — nda_ml_recovery (L171) + da_ml_recovery (L136)
- `projects/simulation/common/_channel.py` — gg_block + doppler_phase + generate_shared_realization_apsk
- `projects/simulation/simulator/sc_nda_ml_sim.py` — fft_foe_m0_omega (L137)

### 5. 框架文件 + 教训
- `stages/gw-feasibility.md` §D 维度 D MVE 11 步
- `thesis-lessons.md` TL-13/20/26
- `.agents/skills/sim-preflight/SKILL.md` §1.6 C6-C8 + rules/mve-validation.md V1-V6 + rules/interrupt.md 10-12

### 6. 上游决策链
- `.sessions/2026-06-20-problem-driven-redirection/decisions.md` — D005 务实路线 / D006 红线 / D017/D018

### 7. B2 Kill 教训（警示）
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/decisions.md` D004/K001 — 前馈化导致测度失效的教训

## 接收方验证

- [ ] 已读取 topic-index 14 不变量（重点 11/12/13/14 B11-Q2 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] NDA-ML D-008 双 bug（漏 ML 加权 + 升幂未归一）（核查 step4a-mve-execution/decisions.md D-008）
  - [ ] B11 行 33 假设"湍流/Doppler/CFO 已补偿"（核查 B11 锚 content.md 行 33）
  - [ ] B11 前馈 ML 不撞 D006（核查 _recovery.py nda_ml_recovery L171 是前馈闭式）
- [ ] 已检查 _registry.yaml 中本专题 depends_on
- [ ] 已确认当前范围未违反"明确不含"

## 执行节奏（守 3 步上限）

**本轮 3 步**：
1. 报到 + 读必读清单 1-7（尤其 D-008 决策 + B11 锚 content.md 行 33）
2. 阶段 0.1 D-008 耦合依赖门控（派子 agent 核查 D-008 修复状态 + 主线判定 B11-Q2 sandbox 前置条件）
3. 阶段 0.2 B11 行 33 假设核查（主线定，读 B11 锚全文）

**超 3 步主动建议分对话**。阶段 0.3-0.6 留下一对话。

## 产出物

1. `explore/b11-nda-ml-turbulence-validation/_d008_dependency_check.md` — 阶段 0.1 D-008 耦合门控
2. `explore/b11-nda-ml-turbulence-validation/_b11_assumption_audit.md` — 阶段 0.2 B11 行 33 假设核查
3. S002 session note + H002 handoff

**explore/ 目录在 `projects/simulation/explore/b11-nda-ml-turbulence-validation/`**

## 红线

1. **禁 D-008 修复前跑 sandbox**（vs VV 持平是 bug）
2. **禁跳阶段 0 直接写代码**
3. **禁走环路 TF 联合建模**（前馈 ML 不撞 D006）
4. **禁把 B11-Q2 当从零开始**（是 NDA-ML 延伸，复用基建）
5. **禁自建信道**（TL-13）
6. **禁污染 common**

## 开场怎么报

> 续接 B11-Q2 专题（2026-07-08-b11-nda-ml-turbulence-validation），主控对话 S001 + H001 派发。本轮目标：执行阶段 0.1-0.2（D-008 耦合门控 + B11 行 33 假设核查），不写代码。已读 [列出读过的关键文件]。接收方验证 [N 条全打钩]。开始阶段 0.1。
