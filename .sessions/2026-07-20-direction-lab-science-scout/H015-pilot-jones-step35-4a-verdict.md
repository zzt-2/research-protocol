# Handoff: SCIENCE_FREEZE 收口；交接到 Pilot-Jones Step 3.5 终审 + Step 4a 状态裁决

> 来源: S014 | 交接目标: 主控决策 Pilot-Jones Step 3.5/4a 是否为下一权威工作
> 日期: 2026-07-22
> 文件名: H015-pilot-jones-step35-4a-verdict.md

## 到哪了（状态）

S014 执行 SCIENCE_FREEZE + campaign-level reconciliation（用户触发："经过了这么多轮，咱们是不是该整体想想？"）。D022 裁决：SCIENCE_SCOUT candidate rotation 暂停（本专题 dormant）；**当前没有合法 main-method signal**；F1=TESTBED_BLOCKED（rotation 0.06° 使 testbed 对 F1 家族近空）/ F3=UNRESOLVED（F3-A 非 conditional MI）/ F4=INFRASTRUCTURE_BLOCKED（coded chain）；**F2 pilot lineage 合并入已有 Pilot-Jones 正式 Groundwork，不建平行 Scout（F2 collision check 本轮未执行）**；负面材料只进 harvest/limitations，不 pivot 完整负面论文。修正了所有继承 D020/H013 旧结论的 stale current views（state/portfolio/harvest/topic-index/registry）。

**Pilot-Jones 链真实门控（Explore agent 只读审计，file:line 证据）**：
- Pilot-Jones 当前在 **Step 3.5（🔄 in progress）**，非 Step 4a（master-state.md:96）。
- **master-state.md:96 的"待V030"是 stale 指针**——V030 实属 P03 residual-headroom 终验（verifications.md:782），非 Pilot-Jones。
- Pilot-Jones Step 3.5 门控 = V028（verifications.md:639）+ V029（verifications.md:743），**均 PARTIAL**，显式封锁 Step 4a（V028:669 / V029:774-776）。
- **无任何 Pilot-Jones 专属终审 PASS V###**。
- 缺：(1) 一个独立终审 V### 完成 highest-citation 直接竞品 JLT2022 的 backward 引用链（V029:778-780 / S074:28）；(2) 4 个直接竞品全文精读（OE2021 已读；JLT2022-23/TCOMM2025/LCOMM2026 仅 abstract，D056：decisions.md:2929-2931）。
- EMA09 15/15 改善 + clean 0/9 不退化 = **family-level promotion 到正式 GW Step 1，非 Go**（master-state.md:91 / S065:28 / decisions.md:2893）。
- generic pilot→Jones 撞车后剩余窄问题（M-C-A）：传统 block/frame pilot Jones inversion（M）在 GG 湍流+高速 SOP+≤10% pilot budget（C）下 fixed-label 恢复不稳定（A）（S066:17 / decisions.md:2911）。

**重要 caveat**：当前授权控制面入口是 P03/Headroom-Atlas 决策点（master-state.md:25-32），**非 Pilot-Jones**（master-state.md:26 "旧 Pilot-Jones Step 3.5/4a 链也未成为当前授权入口"）。Pilot-Jones 工作实质 suspended，待用户先在 P03 routing（master-state.md:32 选项 ①②③）裁决。

## 下一步干什么

**第一件事：用户/主控裁决 Pilot-Jones Step 3.5/4a 是否为下一权威工作**（而非新 F2 collision search）。若激活 Pilot-Jones，新对话续接的具体动作：
1. 读 `projects/thesis-fso/master-state.md:66-102` 方法层重开轨表 + `decisions.md:2889-2931`（D052-D056）+ `verifications.md:639-780`（V020-V029）。
2. 完成 Step 3.5 终审：独立终审 V### 完成 JLT2022 backward 引用链（V029:778-780 指明不需第四轮关键词泛搜，只需 backward 链）。
3. 完成 Step 4a prerequisites：4 个直接竞品全文精读（子 agent，按 gw-read.md 结构化提取），对比 D056 指定的失败条件。
4. Step 4a A0/A/B/D 维度目前零起步，需按 gw-feasibility.md 从 "现有 M 在 C 下因 A 失效" 起步。

**注意**：本专题（science-scout）dormant，不在本专题内推进 Pilot-Jones。Pilot-Jones 在 dual-pol-osl-groundwork 专题。

## 纪律（和下一步直接相关）

- **F2 collision check 本轮未执行**（SCIENCE_FREEZE 明禁）；F2 pilot lineage 合并入已有 Pilot-Jones 正式 GW，不建平行 Scout。
- 不复活 D018 blind-router、p03 pilot→Jones→inverse 微变体、C12 全局-σ² oracle、C16 非-FIR HOS。
- F1=TESTBED_BLOCKED 非"model-prior 无价值"普适结论；若重测须先换 high-SOP-rate atlas + μ-tuned CMA + raw-stream blind_affine + persistence/AR(1) baseline（本轮不授权重建）。
- EMA09 15/15 + clean 0/9 是 family-promotion-to-Step1，**非 Go**；Step 2/3/3.5/4a 仍硬门。
- protected 文件不改：STATUS.v1.md = STALE_PROTECTED（不是当前科学事实源，其头部仍写 F1-B 首选已被 D021 撤回）；project.v1.yaml = historical read-only-preview adapter（不是当前授权 owner）。当前可信事实源 = 修正后的 state/current.yaml + D022/H015。
- 不把局部负面包装成完整负面论文（H060 全域 5 宣称已被 D017 invalidated，证据仅 LOCAL_SLICE）。
- oracle 上界只作 Kill 工具不作 Go 判据（FR-21/FR-25）。

## protected 文件角色声明（本轮不改文件，仅标记）

| 文件 | 角色 | 理由 |
|------|------|------|
| STATUS.v1.md | STALE_PROTECTED — 不是当前科学事实源 | 头部（line 1-8）仍写 "F1-B 第一个正面候选 / 需一天基建"，已被 D021 撤回。bf620b3 有 +9/-4 diff（D021 gap #10）。本轮 byte-identical 未改。 |
| project.v1.yaml | historical read-only-preview adapter — 不是当前授权 owner | authorized_actions 仍 READ_ONLY_MIGRATION_PREVIEW；controller ownership 与 state/current.yaml 投影冲突未解（D021 gap #11）。本轮 byte-identical 未改。 |
| canonical-state.yaml | machine projection only — 非正式研究授权源 | formal_research_state.status: BLOCKED（master-state drift + Step3.5 未独立闭合）。本轮未改。 |
| 当前可信事实源 | state/current.yaml（已 D022 修正）+ D022/H015 | —— |

## 接口变更（如有代码改动）

无代码改动。本轮只修改 governance 文档（state/portfolio/harvest/current.yaml + topic-index + _registry + decisions/voice）+ 新建 S014/H015/V012。无仿真器/tracker/pilot 代码。

## 失败数据附录（无新科学实验；campaign-level 收口数据）

本轮无新科学实验/Probe。campaign 收口的关键历史失败数据（保留自 S013/D021/H014，不重跑）：
- F1-A0 g0 FAIL：plugin 0.1685 vs nopred 0.1683，binomial p≈0.38（8 help/13 hurt/89 tie）。
- SOP rotation 256-symbol window = 0.06°（sop_rate=4e-6）→ 预测任务近空。
- CMA μ 债：μ=0.01→0.083 vs μ=0.03→0.369。
- D018 hybrid-router oracle headroom = 0.003693（< 0.03 threshold）。

## 已知债务（原则与现实差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| STATUS.v1.md "protected unchanged" vs bf620b3 +9/-4 diff | protected history 不可改 | 矛盾记录在 D021 gap #10，本轮不改 | 主控裁决（回退 diff 或承认 STATUS 非 protected）|
| canonical/project.v1 vs SCIENCE_SCOUT projection ownership | 单一 controller | 冲突未解，D021 gap #11 | 主控裁决 ownership |
| master-state.md:96 "待V030" stale 指针 | 恢复指针准确 | V030=P03 非 Pilot-Jones，本轮在 H015 标记但未改 master-state（它属 thesis-fso 项目级，非本专题）| 主控裁决是否修 master-state:96 |
| F1-A0 artifact 未存 ridge 权重/prefix features/per-sample h/θ | raw rows 可重算 | V011 标记 | 若重测 F1 须补 raw-rows 字段 |

## 验证阈值（验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| stale current views 不再写 F1/F3 为当前 PASS | 0 处 PASS 残留 | D022 + 提示词 §三 | V012 复核（本轮）|
| H013 不再作为 latest recovery | state/portfolio/harvest 均指 H015 | D022 | V012 复核（本轮）|
| F1-B 不再是 active thesis spine | harvest current_valid_spines PRIMARY = WITHDRAWN | D022 | V012 复核（本轮）|
| F2 未被创建为新平行 Scout | 无新 F2-A Probe 目录 | D022 | V012 复核（本轮）|
| protected 文件 byte-identical | STATUS.v1.md / project.v1.yaml / canonical-state md5 不变 | D022 禁令 | V012 复核（本轮）|

## 用户/advisor voice（关键指令，verbatim）

- "经过了这么多轮，咱们是不是该整体想想？" → D022（campaign-level 收口触发）

（其余本轮执行约束见提示词 §一-§六；完整历史原话见 voice.md。）

## 必读（不超过 8 个）

1. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（不变量 + 当前位置 S014/D022/H015）
2. 本文件 `H015-pilot-jones-step35-4a-verdict.md`
3. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` 的 D022 + D021
4. `.sessions/2026-07-20-direction-lab-science-scout/S014-campaign-level-science-freeze.md`（§四 Pilot-Jones 审计 + §五 仍有效结论）
5. `projects/thesis-fso/direction-lab/state/current.yaml`（修正后；F1/F3 invalidated + SCIENCE_FREEZE）
6. `projects/thesis-fso/master-state.md:66-102`（Pilot-Jones Step 3.5 🔄 / Step 4a ⛔ 门控表；注意 :96 "待V030" stale）
7. `.sessions/2026-07-10-dual-pol-osl-groundwork/verifications.md:639,743,782`（V028/V029 PARTIAL + V030=P03）
8. `projects/thesis-fso/direction-lab/STATUS.v1.md`（STALE_PROTECTED，不改；角色见上方声明表）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落。
- [ ] 已验证至少 3 条关键事实：
  - V030 属 P03 非 Pilot-Jones → 读 `verifications.md:782`（标题 "P03 residual-headroom Scout 最终独立终验"，关联 S075/D057）；
  - master-state.md:96 "待V030" stale → 读 `master-state.md:96` + 对比 `verifications.md:782`；
  - state/current.yaml F1/F3 validity 已 invalidated → 读 `state/current.yaml` effective_conclusions F1A/F3A 条目。
- [ ] 已检查 `_registry.yaml` 的 depends_on/conflicts_with（本专题 status=dormant，depends_on 含 dual-pol-osl-groundwork）。
- [ ] 已确认当前范围不含：F2 collision check、新仿真/Probe、tracker/pilot/ML/testbed 实现、protected 文件修改、完整负面论文 pivot、自动轮转、push。

## git 状态

- worktree: `D:/code/study/research-protocol/.worktrees/direction-lab-capability-atlas`
- branch: `codex/direction-lab-capability-atlas`
- 本轮 consolidated commit 待提交（不 push）。接收时以 `git log -1` 核验实际 SHA。

## 下一轮

用户/主控裁决 Pilot-Jones Step 3.5/4a 是否为下一权威工作（vs 在 P03 routing 先裁决，master-state.md:32 选项 ①②③）。若激活 Pilot-Jones：完成 V029 backward-chain 终审 + 4 竞品全文精读，非新 F2 collision search。
