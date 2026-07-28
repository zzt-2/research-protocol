# [S002] Goal 十七包零方法与 pre-formal 方法工厂重定向

> 2026-07-28 | 长程阶段审计 / 运行范式纠偏 | 状态：METHOD_FACTORY_SKILL_UPDATE

## 目标

冻结 T018/Q14 形式化链，记录长期 Goal 的实际投入产出，解释为什么现有控制面
运行成审计/形式化流水线，并为受限的 pre-formal method-factory lane 冻结最小设计。

## 记录

### 1. 实际结果

- mission 已到 CP017，`mission_method_delta` 17/17 为 `NONE`；
- `METHOD_SIGNAL=0`、`PROMOTION_READY=0`，formal active scientific carrier
  仍为 `NONE`；
- CP009–CP017 继续经历 A4/B10/C15/B9/B12/C16 等 identity、coverage、
  evaluator、physical lifecycle、novelty collision 与 task-interface 阻断；
- T018/Q14 只准备 mandatory Step 3.5/problem-evidence workline，预注册 delta
  仍为 NONE，尚未执行，也没有 CP018 或 step-018 worker log。

这些包阻止了假增益、假 Kill 和不合法论文结论，具有科学安全价值；但原 mission
是“稳定推进并积累可用方法材料”，因此十几个小时的核心产出目标未达成。

### 2. 核心失败机制

当前 Goal 把“formal readiness 最接近”当作“最可能产方法”。当 remap 得到
`READY=0 / NEEDS_SMALL_ADAPTER=0 / HYPOTHESIS_ONLY>0` 时，它没有识别为战略
阻塞，而是把 hypothesis-only 候选逐个送入 source coverage、DOI identity、
Step 1–3 与 final-binding。局部 blocker 总有下一个合法动作，Goal 因而可以长期
自动继续，却始终到不了方法构造。

RDL 的 method-production 规则虽要求记录 no-method streak，但仍把
`CANDIDATE_FORMALIZATION` 允许为独立 package；FR-22 又把任何“试新方法”放在
完整 Step 3/4a 之后。二者组合使“方法”成为不可达的最后一步。

### 3. 用户裁决

停止 T018，不修 final-binding，不执行 Q14 Phase A。取消当前长期 Goal 的端到端
自动继续方式，恢复“主控给普通 GLM 提示词—用户中转极短回执—主控验收并给下一
提示词”的协作接口。

采纳推荐方案：显式建立受限的 `PREFORMAL_METHOD_FACTORY` lane，而不是暗中绕过
FR-22。

### 4. 最小设计

1. **入口**：无 active carrier，且 portfolio remap 得到
   `READY=0 / NEEDS_SMALL_ADAPTER=0` 时，禁止继续串行形式化
   hypothesis-only 候选；进入方法工厂或交用户战略裁决。
2. **底座**：只用一个已经验证的 simulator/evaluator、一个正确且广泛采用的传统
   baseline、共享 seeds/realizations；不为候选新建整套基础设施。
3. **一个 sprint**：同包实现并比较 3–5 个机制不同的小构造。身份 smoke 限于
   signal order、物理 timescale、baseline/evaluator population，且必须与方法构造
   同包；不另立纯 smoke/formalization checkpoint。
4. **方法动作下限**：每个 method-factory package 至少产生
   `CONSTRUCT_CREATED` 或 `FAIR_COMPARISON_RUN`。预期 delta 固定为 NONE 的
   source/formalization/problem-evidence 包不得成为该 lane 的下一包。
5. **claim ceiling**：工厂结果仅为 `DIAGNOSTIC_METHOD_SIGNAL` 或
   `NO_DIAGNOSTIC_SIGNAL`，不能写论文、不能作 formal Go/Kill、不能自动晋级。
6. **信号后正式化**：只有诊断胜者再补 Step 1–3、全文碰撞、正式 comparator 与
   MVE；无信号则换一个共享构造批次，不逐候选补 metadata。
7. **退出**：底座身份失败则暂停并修共享底座；一批无信号则 harvest/轮换；出现
   诊断信号则返回正式 Groundwork；需要改变场景/目标/大基建时交用户。

### 5. 轻量实现边界

- `research-direction-lab/references/method-production.md` 拥有完整方法工厂合同；
- RDL `SKILL.md` 只增加入口/出口路由；
- `stages/groundwork.md` 为 FR-22 增加窄例外：该 lane 不是 MVE，不形成科学
  结论，胜者必须重新进入正式 Groundwork；
- `AGENTS.md` 只更新 FR-22/FR-27 索引说明；
- 不新增 controller、scheduler、manifest 或新的通用日志层。

## 决策引用

- D026：停止 T018 与 Goal 形式化链，建立 pre-formal 方法工厂并恢复 GLM 中转
  （新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。属于 live-test 对长期运行结果的阶段审计与
  流程纠偏；当前不执行科学实验，不修改 T018 科学内容，不创建 CP018。

## 后续

按本记录更新 RDL Skill、FR-22 窄例外与当前状态；完成最小结构检查后，向用户交付
一个普通 GLM 对话提示词，由 GLM 执行首个 method-factory sprint 的底座选择与批次
设计/实现，不创建 Goal。

> 2026-07-28 续接：T019 已完成，产出在
> `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-001/`，
> commit `e1c479e`。V052/D027 部分接收：工程比较与
> `FAIR_COMPARISON_RUN` 成立；因旧 `μ=0.001` baseline、M3/M5 非因果、
> smoke receipt 缺失与机制归因越界，广义 `NO_DIAGNOSTIC_SIGNAL` 拒收。M5
> 只保留为一次 corrected-baseline/fresh-seed 扩展的弱种子。

> 2026-07-28 续接：T020 已完成，产出在
> `projects/thesis-fso/direction-lab/scout/preformal-method-factory-sprint-002/`，
> commit `5cf76d5`。V053/D028 以 PARTIAL 接收 M4 为工厂级
> `DIAGNOSTIC_METHOD_SIGNAL`：主数字可复算、严格 prefix-only、P0=0；但 gate
> receipt、完整四分类和 comparator gate 实现仍有债，信号主要集中在 7/20 个
> CMA collapse seeds。方法工厂到此结束，M4 暂登记为 Q15；下一轮 T021 只做
> Groundwork Step 1–2，coverage-gap report 后暂停。

> 2026-07-28 续接：T021 已完成，commit `287fb6a`。V054/D029 部分接收：
> 129 unique、121/129 published、11 必读和六篇独立核心+两篇补充全文成立；
> 但 merged raw 实际仅两源，IEEE 第三源无结构化 receipt，五篇 blit 未进
> papers index。T022 不单开纯修复包，而是先闭合这两项收据，随后同包完成
> Q15 Step 3 精读。D1/C1/C4 保留为 Step 3.5 mandatory debt。

> 2026-07-28 续接：T022 已完成，实际 commit
> `f3a47260f732e0987743f32bffc6d21d7f92e6aa`。V056/D030 接收六篇独立核心
> Step 3 内容与 `mission_method_delta=NONE`，但拒收“8/8 全结构 PASS”和
> “只差 D1/C1/C4”。独立源码复核发现 T020 M1 把功率比直接作为复振幅乘子，
> 正确 conventional normalization 应取平方根；evaluator 不恢复尺度。Q15
> 判据改为 1/2 PARTIAL、3/4 PASS。T023 是唯一终局包：先 Step 3.5 纳入公开
> D1 与定向 normalization/MMA 证据；四判据全过后才同包进入 Step 4a 正确
> baseline 审判，失败/blocked 均退出且不再 repair。
