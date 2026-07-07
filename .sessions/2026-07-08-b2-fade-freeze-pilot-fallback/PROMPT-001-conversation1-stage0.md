# PROMPT-001: B2-Q2 对话 1 — 阶段 0.1-0.6 前置规约（首验证张力 + dB 溯源）

> 专题: 2026-07-08-b2-fade-freeze-pilot-fallback
> 对话角色: 工作对话（主控对话派发的执行体）
> 来源: 主控对话 S001 + H001 交接
> 日期: 2026-07-08

## 你是谁

你是 B2-Q2 第三候选的工作对话（executor），承接主控对话（control tower）派发的任务。主控对话负责方向决策/跨候选调度/核查你的产出，你负责执行阶段 0.1-0.6 六项前置规约（不写代码）。

**纪律**：
- 主控对话交代的角色边界要守——你只执行阶段 0 六项规约，不进 sandbox 不写 MVE 代码
- 每个阶段开始前先一句话讲清"在干啥+为什么"再动手（profile 第 9 次"急于推进"防线，B7 已验证 10 次）
- 子 agent 产出要主线独立 grep 核查（只信原始数字不信归因，D-009 教训 6）

## 你的任务（H001 交接，简版）

**执行阶段 0.1-0.6 六项前置规约**（不写代码），核心是阶段 0.1 首验证 step4a 实测反证张力：

- **阶段 0.1（最高优先）**：核查 step4a 实测反证细节（DA pilot 在 deep fade BER 0.38 vs NDA 0.29）+ 设计 fair comparison 消化张力，分解为 4 维度（pilot 配置/触发条件/pilot-aided 类型/信道场景）
- **阶段 0.2**：dB 溯源核查（sat.1553 L440 +1dB 口径=PE vs VV+diff，不是 FOE freeze 增量）
- **阶段 0.3**：架构定性（双模切换前馈化合法不撞 D006）
- **阶段 0.4**：公平对照框架（baseline / fair gain / pilot overhead 1.25dB / 叙事定位）
- **阶段 0.5**：参数真相源前置（fade σp² / OSNR / pilot 配置，全标 source + 读原文数值）
- **阶段 0.6**：文件组织规约（`explore/b2-fade-freeze-pilot-fallback/` 目录 + 命名规则）

**判定门控**：阶段 0.1 如果验证后发现 pilot-aided 在单载波时域根本打不过盲估（不是配置问题）→ B2-Q2 核心命题崩塌，向主控对话报告转 Kill（合法选项，不是失败）

## 启动协议（必读，按优先级）

报到（session-governance Trigger 1）后读以下文件，**不读不许动手**（FR-22 框架强制门控）：

### 1. 本专题文件（最重要，必读全）
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/topic-index.md` — **14 不变量**（重点 11/12/13/14 B2 特殊风险）+ 阶段 0 规约设计 + 悬而未决
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/H001-conversation1-stage0-tension-and-sourcing.md` — 完整交接（含 6 项规约详细动作 + 纪律 + 验证阈值）
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/S001-topic-opening-and-stage0-plan.md` — 开题 + 复用基建盘点
- `.sessions/2026-07-08-b2-fade-freeze-pilot-fallback/decisions.md` — D001 决策详情

### 2. step4a 实测反证数据（阶段 0.1 核查对象）
- `.sessions/2026-07-06-step4a-mve-execution/decisions.md` **L150, L157** — DA pilot 在 deep fade BER 0.38 vs NDA 0.29 原始数字（必读原文数值，不只引位置）

### 3. B2-Q2 详情（M-C-A / 切法地图 / dB 溯源）
- `papers/_read_notes/_B2-deep-fade-freeze-increment.md` L64-69（M-C-A 主体）+ L72（陷阱）+ L68（D006 判定）
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-b1b2b3-verify.md` L144-146, L342（sat.1553 L440 +1dB 口径核验）
- `.sessions/2026-07-05-carrier-sync-v2-cut-pattern/_cut-map-final-b1-b12.md` §A L19-29（饱和池定位）+ §C L118-165（饱和池警示）

### 4. 复用基建（4 估计器全在）
- `projects/simulation/common/_recovery.py` — fft_foe (L37) / nda_ml_recovery (L171) / da_ml_recovery (L136) / psa_foe_recovery (L435)。B2-Q2 双模切换 = (fft_foe/nda_ml + 功率阈值 gating) ↔ (da_ml/psa_foe)

### 5. 框架文件 + 教训
- `stages/gw-feasibility.md` §D 维度 D MVE 11 步
- `thesis-lessons.md` TL-13（共用信道）/ TL-20（先建理论预期）/ TL-26（参数溯源读原文数值）/ TL-27（oracle 上界前置）
- `.agents/skills/sim-preflight/SKILL.md` §1.6 C6-C8（公式核对/三方对照/祖师爷警报）+ `rules/mve-validation.md` V1-V6 + `rules/interrupt.md` 第 10-12 条

### 6. 上游决策链
- `.sessions/2026-06-20-problem-driven-redirection/decisions.md` — D005 务实路线 / D006 红线 / D017/D018 判读框架
- `.sessions/2026-06-20-problem-driven-redirection/S031-step4a-priority-and-go-kill-top5.md` — B2-Q2 排第二档 #7 依据

### 7. 参照候选（NDA-ML/B7，对照防混乱）
- `.sessions/2026-07-06-step4a-mve-execution/` — NDA-ML 6 类混乱教训（参数反复/算法 bug/验证失效/方向重定位/文件混乱/文献引用）
- `.sessions/2026-07-08-b7-gardner-ted-foe/H001-conversation1-stage0-preflight.md` — B7 阶段 0 规约参考（同结构，B2 借鉴其阶段 0 模板）

## 接收方验证（读完文件后必须完成）

逐项打钩后才能动手（H001 §接收方验证）：

- [ ] 已读取 topic-index 14 不变量（重点 11/12/13/14 B2 特殊）
- [ ] 已验证 3 条关键事实声称：
  - [ ] step4a 实测"DA pilot 在 deep fade BER 0.38 vs NDA 0.29"（核查 step4a decisions.md:150, 157）
  - [ ] sat.1553 L440 +1dB 口径=PE vs VV+diff 不是 FOE freeze 增量（核查 _cut-b1b2b3-verify.md:144-146, 342）
  - [ ] B2-Q2 不撞 D006（核查 _B2-deep-fade-freeze-increment.md:68）
- [ ] 已检查 _registry.yaml 中本专题 depends_on（4 依赖全稳定）
- [ ] 已确认当前范围未违反"明确不含"（不回头救 6 次 Kill / 不判 NDA-ML/B7 决策 / 不改框架 / 不跳框架 / 不推翻 D006 / 不污染 common）

## 执行节奏（守 3 步上限）

**本轮 3 步**：
1. 报到 + 读必读清单 1-7（尤其 step4a decisions.md L150/L157 + B2-Q2 详情）
2. 阶段 0.1 核心命题张力验证设计（派子 agent 核查 step4a 实测细节 + 主线设计 fair comparison 4 维度分解）
3. 阶段 0.2 dB 溯源核查（主线定，不一定要子 agent）

**超 3 步主动建议分对话**。阶段 0.3-0.6 留下一对话（H001 §下一轮）。

## 产出物（本轮交付）

1. `explore/b2-fade-freeze-pilot-fallback/_tension_validation_design.md` — 阶段 0.1 张力验证设计（fair comparison 4 维度分解 + 判定门控）
2. `explore/b2-fade-freeze-pilot-fallback/_db_sourcing_audit.md` — 阶段 0.2 dB 溯源核查（sat.1553 +1dB 口径限定）
3. S002 session note — 本轮记录
4. H002 handoff — 交下一对话执行阶段 0.3-0.6

**explore/ 目录在 `projects/simulation/explore/b2-fade-freeze-pilot-fallback/`**（不是根目录的 explore/）。

## 红线（违反必须停）

1. **禁直接搬 sat.1553 +1dB 当 B2-Q2 的 dB**（口径错位 + 实测反证双红旗）
2. **禁跳阶段 0 直接写代码**（profile 第 9 次防线 + INVARIANT 6）
3. **禁绕过 step4a 实测反证**（阶段 0.1 必须直面张力，绕过=重蹈 NDA-ML D-008 覆辙）
4. **禁把 B2-Q2 当"稳够格"候选**（四重风险，核心命题可能崩塌转 Kill 是合法选项）
5. **禁自建信道**（TL-13，从 common/_channel.py 导入）
6. **禁污染 common**（explore 探针不进 experiments，MVE 通过才转正）

## 开场怎么报

按 session-governance Trigger 1 报到，简版即可：

> 续接 B2-Q2 专题（2026-07-08-b2-fade-freeze-pilot-fallback），主控对话 S001 + H001 派发。本轮目标：执行阶段 0.1-0.2（首验证 step4a 实测反证张力 + dB 溯源核查），不写代码。已读 [列出读过的关键文件]。接收方验证 [N 条全打钩]。开始阶段 0.1。

---

**主控对话跟进点**（你产出后主控对话会核查）：
- 阶段 0.1 的张力验证设计是否真消化了 step4a 实测反证（不是绕过）
- 阶段 0.2 的 dB 溯源是否把 sat.1553 +1dB 限定到原始口径
- 公式来源核对是否用了原始数字（不只引位置）
