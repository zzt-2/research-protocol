# PROMPT-001: B3-Q2 对话 1 — 阶段 0.1-0.6 前置规约（4 支路迁移验证 + A1 归属核查）

> 专题: 2026-07-08-b3-joint-estimation
> 对话角色: 工作对话（主控对话派发的执行体）
> 来源: 主控对话 S001 + H001 交接
> 日期: 2026-07-08

## 你是谁

你是 B3-Q2 第三候选的工作对话（executor）。B3-Q2 是子系统协同联合估计，特长场景=强湍流分集接收下联合估计 vs 分立管线（导师"特长场景"标准）。

**纪律**：
- 只执行阶段 0 六项规约，不进 sandbox 不写 MVE 代码
- 每个阶段开始前先一句话讲清"在干啥+为什么"
- 子 agent 产出要主线独立 grep 核查

## 你的任务（H001 交接，简版）

**执行阶段 0.1-0.6 六项前置规约**（不写代码），核心是阶段 0.1 验证 4 支路迁移风险：

- **阶段 0.1（最高优先）**：验证星地多孔径阵列是否真实工程场景 + FR-21 单链路 CRB 上界前置。B3-Q2 +2~3dB 是 4 支路 MRC 强湍的，单支路 ~1dB，星地单孔径难堆叠多望远镜
- **阶段 0.2**：A1 归属核查（jphot+oe BUPT 课题组是否已发星地分集续作）
- **阶段 0.3**：架构定性（前馈开环不撞 D006 vs 环路 TF 撞转 B3-Q3）
- **阶段 0.4**：公平对照框架（baseline=分立管线，4 支路 vs 单链路双场景）
- **阶段 0.5**：参数真相源前置（望远镜口径/间距/Cn² + 调制格式，全标 source + 读原文数值）
- **阶段 0.6**：文件组织规约（MRC/帧同步/多支路管线接口）

**判定门控**：星地多孔径阵列不是真实场景 + 单链路 CRB <0.5dB → B3-Q2 转 Kill（特长场景不成立）

## 启动协议（必读，按优先级）

报到（session-governance Trigger 1）后读以下文件，**不读不许动手**：

### 1. 本专题文件（最重要）
- `.sessions/2026-07-08-b3-joint-estimation/topic-index.md` — 15 不变量（重点 11/12/13/14/15）
- `.sessions/2026-07-08-b3-joint-estimation/H001-conversation1-stage0-migration-and-a1.md` — 完整交接
- `.sessions/2026-07-08-b3-joint-estimation/S001-topic-opening-and-stage0-plan.md` — 开题
- `.sessions/2026-07-08-b3-joint-estimation/decisions.md` — D001 决策

### 2. B3-Q2 详评（阶段 0.1 核查对象）
- `papers/_read_notes/_B3-subsystem-coordination-increment.md` L32,74-76,77,85
- `papers/_read_notes/10.1109_jphot.2023.3265847.md` L17,56（4 支路 + 星地迁移风险）
- `papers/_read_notes/10.1364_oe.520452.md` L16,51（BUPT 课题组姊妹工作）
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b1b2b3-verify.md` L258-291（dB 出处）
- `.sessions/2026-06-20-problem-driven-redirection/S031-step4a-priority-and-go-kill-top5.md` L33-39,161-169,213

### 3. 复用基建
- `projects/simulation/common/_recovery.py` — 单支路估计器（fft_foe/vv_cpr/bps_cpr/da_ml）

### 4. 框架文件 + 教训
- `stages/gw-feasibility.md` §D
- `thesis-lessons.md` TL-13/20/26/27
- `.agents/skills/sim-preflight/SKILL.md` §1.6 C6-C8 + rules

### 5. 上游决策链 + 导师标准
- `.sessions/2026-06-20-problem-driven-redirection/decisions.md` D005/D006
- `.sessions/2026-07-08-b3-joint-estimation/voice.md`（导师"特长场景"标准）

### 6. B2 Kill 教训
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/decisions.md` D004/K001

## 接收方验证

- [ ] 已读取 topic-index 15 不变量（重点 11/12/13/14/15 B3-Q2 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] B3-Q2 +2~3dB 是 4 支路 MRC 强湍，单支路 ~1dB（核查 `_cut-b1b2b3-verify.md:258-291`）
  - [ ] 星地单孔径终端难以堆叠多望远镜（核查 jphot 笔记 L56）
  - [ ] jphot+oe BUPT 课题组已完成 FS+FOE+MRC 联合（核查 `_B3-...md:32,76`）
- [ ] 已检查 _registry.yaml 中本专题 depends_on
- [ ] 已确认当前范围未违反"明确不含"

## 执行节奏（守 3 步上限）

**本轮 3 步**：
1. 报到 + 读必读清单 1-6（尤其 jphot/oe 笔记 + S031 B3-Q2 详评）
2. 阶段 0.1 星地多孔径阵列场景验证 + 单链路 CRB 上界（派子 agent 查文献 + 主线算 CRB）
3. 阶段 0.2 A1 归属核查（主线查 BUPT 课题组续作）

**超 3 步主动建议分对话**。阶段 0.3-0.6 留下一对话。

## 产出物

1. `explore/b3-joint-estimation/_diversity_migration_validation.md` — 阶段 0.1 4 支路迁移验证
2. `explore/b3-joint-estimation/_a1_attribution_audit.md` — 阶段 0.2 A1 归属核查
3. S002 session note + H002 handoff

**explore/ 目录在 `projects/simulation/explore/b3-joint-estimation/`**

## 红线

1. **禁跳过 4 支路迁移验证直接跑 MVE**
2. **禁跳阶段 0 直接写代码**
3. **禁走环路 TF 联合建模**（前馈开环不撞 D006，环路撞转 B3-Q3）
4. **禁忽视 A1 归属**（jphot+oe 已做联合）
5. **禁自建信道**（TL-13）
6. **禁污染 common**

## 开场怎么报

> 续接 B3-Q2 专题（2026-07-08-b3-joint-estimation），主控对话 S001 + H001 派发。本轮目标：执行阶段 0.1-0.2（4 支路迁移验证 + A1 归属核查），不写代码。已读 [列出读过的关键文件]。接收方验证 [N 条全打钩]。开始阶段 0.1。
