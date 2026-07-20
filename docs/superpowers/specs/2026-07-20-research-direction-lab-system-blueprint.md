# Research Direction Lab 完整体系蓝图

> 日期：2026-07-20
> 状态：目标态设计，待用户审定；不授权修改现有控制器、运行 B004、训练 ML 或改变正式研究状态
> 唯一职责：定义未来 Research Direction Lab 的完整目标体系；当前运行事实仍由现有项目状态与历史证据拥有

## 1. 要解决的真实问题

目标不是制造一个“永远合规”的研究状态机，而是让 AI 在已有或新建研究地基上持续完成以下工作：

1. 尽可能展开相关应用点、方法族、步骤改进和组合方向；
2. 先看全景、归类和统一规划，再用共享基线成批验证；
3. 一个方向失败后自动换到其他合法方向，整批无信息后重新扩展候选空间；
4. 避免从一个狭窄 cell 外推整个 baseline、候选或方法族；
5. 保留正面、负面、局部、次级和基础设施结果；
6. 持续把结果组织成可能写进毕业论文的方法、边界分析、失败机制或设计准则；
7. 用少量入口让用户始终看懂基座、候选、批次、结果和下一步；
8. 让证据、历史和文件安全由确定性工具保护，而不是依赖 AI 记忆。

Direction Lab governance pilot 原本用于观察最低限度需要哪些强控制。后续 Portfolio Autopilot 把开放式研究判断继续编码为固定批次数、机制族覆盖、science slots 和资源匹配，V035/V037 的连续反例说明这一责任划分不成立。

## 2. 用户原话派生要求

完整原话保存在：

- `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md`
- `.sessions/2026-07-17-direction-lab-governance-pilot/voice.md`
- `.sessions/2026-07-20-research-direction-lab-system/voice.md`

本设计使用以下需求 ID；原话档案是来源，本文只做可执行翻译。

| ID | 派生要求 | 验收含义 |
|---|---|---|
| U01 | 从稳固地基向外深挖 | 先导入 baseline、资产、失败和历史结果，不默认从零发明问题 |
| U02 | 先找方向，再划分，再跑 | Candidate Portfolio 未形成前不让单候选劫持全部预算 |
| U03 | 微变体不机械重复完整 GW | 共享精读与证据资产；Deep Evidence 增量补缺，不绕过项目已有硬门 |
| U04 | 一个方向不行就换，整批不行就重想 | 局部失败不是会话终点；Skill 必须生成下一合法动作 |
| U05 | 不钻牛角尖，各处都想改进 | 候选展开覆盖处理链位置、信息接口、输出类型和机制族 |
| U06 | 一个主对话尽可能连续推进 | checkpoint 是机器状态，不是每个接口后的用户审批点 |
| U07 | 一次尽可能多推一些 | 相互依赖的小接口组成一个 Sprint；批次比较多个可解释机制 |
| U08 | baseline 不是所有条件都行 | 局部关闭前必须做 scope/axis 审计，区分 runnable 与 blocked axes |
| U09 | 次级结果也要汇总 | 每批都写入 Thesis Harvest，不只记录 winner |
| U10 | 组织整齐、抗膨胀、可恢复 | 项目只保留少量入口、机器状态和单批摘要；raw 留 artifact |
| U11 | 通用代码不含具体研究语义 | BER/SNR/CMA/pilot 等只能出现在 Profile/Adapter/项目 runner |
| U12 | AI 能判断好的不要硬约束 | 科学排序、换路、扩域和解释由 Skill 完成，不写成求解器 |
| U13 | 最终要挖出论文内容 | 治理 PASS 不计科学进展；每轮报告 harvest 增量 |
| U14 | 用户能看懂全局 | `STATUS.md` 必须一页解释 anchor、portfolio、运行、结论和 next action |
| U15 | 原话不能被执行提示词替代 | voice 中区分用户自然原话、转述和执行提示词；设计决策可溯源 |

### 2.1 对看似冲突原话的统一解释

- **“按流程不跳步”**：不可跳过全景、共享基线、证据检查、scope 限定和结果沉淀；不等于每个微变体跑完整 GW。
- **“一直推，别停”**：有合法替代工作时必须换路；不等于绕过历史保护、伪造证据或静默扩大论文范围。
- **“代码完全通用”**：通用工具不懂具体领域；领域知识仍通过可替换 Profile 和 Adapter 存在。
- **“尽可能多跑”**：提高每轮科学信息量，不通过拆小批次、重复 artifact 或刷计数制造进度。
- **“先全景”与“深耕一个点”**：anchor 决定深耕范围；全景是在 anchor 周边展开机制族和条件轴，不是无限跨题搜索。

### 2.2 极简术语表

- **cell / slice**：单一条件格 / 一组相关条件；**contract**：一次批次的预注册问题、比较和退出约定；**family**：共享机制的一组候选。
- **source closure**：结果所依赖源码、参数与输入均可定位并校验；**claim ceiling**：现有证据允许声称到的最高范围。
- **harvest**：从批次沉淀的论文素材或可复用资产；**Deep Evidence**：候选晋级后对证据缺口的增量补强。

## 3. 设计原则

1. **Skill-first, code-guarded**：Skill 驾驶，代码护栏。
2. **Science-first**：论文价值与机制信息是进度；治理活动只是成本。
3. **Open-world reasoning**：科学空间不能由固定 schema 宣称完整，也不能由资源匹配器决定下一方向。
4. **Deterministic integrity**：hash、receipt、stale、历史保护、路径边界和聚合必须可测试。
5. **Portfolio before fixation**：先形成候选组合，再给单候选预算。
6. **Scope before closure**：局部证据只关闭局部；域级结论必须处理 runnable axes、blocked axes 和历史反例。
7. **Harvest every run**：正负结果都进入可查询的论文素材分类。
8. **One owner per fact**：流程、项目事实、运行事实、原话和论文收获分别只有一个拥有者。
9. **Progressive disclosure**：日常恢复只读少量文件，详细历史按需加载。
10. **Adaptive heuristics, fixed invariants**：排序和探索启发式可变；证据和历史不变量固定。

## 4. 责任分层

### 4.1 主 Skill：研究驾驶员

Skill 负责：

- 恢复用户意图、anchor、候选组合和历史结论；
- 从零或从地基选择入口；
- 展开 Candidate Portfolio、识别缺口、归类和排序；
- 设计批次、Sprint、代表条件和退出判据；
- 判断局部阻断后换候选、建共享能力还是扩候选空间；
- 解释结果、限定 claim scope、维护 thesis spine；
- 把每批结果收获为方法、边界、负面、基础设施或写作素材；
- 决定何时调用轻量检索、Deep Evidence、仿真或独立 critic；
- 生成下一合法动作并持续推进。

Skill 不负责伪造运行事实，也不能绕过脚本返回的完整性失败。

### 4.2 通用代码：安全内核与小工具

通用代码只负责：

- 计算文件、配置、source closure 和 artifact hash；
- 验证路径边界、历史只读区和 component identity；
- 创建/校验 manifest 与 receipt；
- append-only 写入事件，拒绝 replay 和冲突 head；
- 标记 duplicate、stale、orphan/untrusted；
- 从事件确定性重建投影视图；
- 运行项目声明的命令并记录退出码；
- 重新计算确定性指标和生成索引；
- 输出事实报告，不输出科学方向选择。

通用代码明确不负责：

- candidate 排名、机制族覆盖充分性或论文价值；
- 固定最小批次数、science slots、资源匹配或 work-conservation；
- 判断何时“研究已经充分”；
- 自动将局部结果提升为 domain/candidate/family 结论；
- 选择下一个科学方向。

### 4.3 Domain Profile：领域规则

Profile 描述一个领域中重复出现的知识：

- 合法指标、单位、估计量和统计约定；
- 训练/运行/评估/oracle 信息边界；
- 常见处理链位置、输出类型和 comparator 类型；
- 常见 domain axes、反模式和 scope 风险；
- 该领域论文通常接受的贡献与证据形态。

Communications Profile 可以包含 BER/FER/GMI、调制、CSI、coded/soft output 等，但不能绑定双偏振 OSL 的具体参数或文件。

### 4.4 Project Adapter：项目事实

Adapter 描述当前项目：

- 正式目标、论文约束和 anchor；
- baseline/component ID、仿真入口和冻结参数来源；
- 当前可运行 axes、blocked axes 和历史反例；
- 现有 runner、evaluator、数据和代码资产；
- 正式材料、sandbox 和历史只读目录；
- 项目专属的 capability 与成本事实。

Adapter 不实现研究调度，也不复制通用流程。

### 4.5 用户：重大策略权

用户只在以下情况拍板：

- 改变论文题目、核心场景或贡献主线；
- 多条都可写的论文路线需要战略选择；
- 明显扩大算力、时间或基础设施投入；
- 需要导师意见、私有材料或只有用户知道的事实；
- 所有合法替代路线都被证据化耗尽。

### 4.6 责任判定测试

| 问题 | 放置位置 |
|---|---|
| 相同输入必须得到相同答案，且错误代价高 | 通用代码 |
| 依赖不完整证据、科学意义或上下文权衡 | Skill |
| 某领域长期稳定的指标/反模式 | Domain Profile |
| 当前项目的 baseline、参数、路径和资产 | Project Adapter |
| 改变论文战略或投入边界 | 用户 |

## 5. 目标架构

```text
User voice / thesis constraints
              │
              ▼
     Research Direction Lab Skill
 recover → map → batch → interpret → harvest → rotate
        │                 │                 │
        ▼                 ▼                 ▼
 Domain Profile      Project Adapter     Deep Evidence
        │                 │
        └────────┬────────┘
                 ▼
       project-specific runners
                 │
                 ▼
       deterministic safety tools
 hash / receipt / history / stale / reducer / index
                 │
                 ▼
 artifacts + evidence ledger + thesis harvest + STATUS
```

不存在一个“通用研究 scheduler”作为额外大脑。Skill 根据状态和证据做下一步判断；脚本只返回可验证事实、允许的安全操作和明确错误。

## 6. 两个入口

### 6.1 从已有地基开始（默认）

```text
Recover voice and thesis constraints
→ Anchor Audit
→ Baseline Revalidation
→ Import Existing Evidence
→ Rebuild Candidate Portfolio
→ Batch Portfolio
```

Anchor 至少包含：场景、正确 baseline、指标口径、参数来源、代码身份、已知 bug、历史正负结果、blocked axes 和论文约束。旧结果按 `VALID / STALE / UNKNOWN / INVALID` 分类，不能自动继承旧结论。

### 6.2 从零开始

```text
Project Intake
→ Prior Asset and Literature Scan
→ Problem/Failure Map
→ Broad Candidate Portfolio
→ Minimal Baseline Foundation
→ Batch Portfolio
```

从零入口必须先得到可运行 baseline 和问题/失败地图，不能直接从模型名称生成候选。

## 7. 核心长期循环

### Phase A：Recover

读取 `STATUS.md`、`project.yaml`、当前 portfolio、最近 batch synthesis 和 harvest 摘要。检查 voice/profile 是否有新纠偏。恢复必须得到：anchor、当前位置、未完成批次、下一动作和不可触碰历史。

### Phase B：Map

围绕 anchor 从五个正交维度展开候选：

1. **processing point**：发送端、信道估计、同步、均衡、检测、译码、控制、监测；
2. **information access**：raw、pilot、receiver trace、历史窗口、decoder feedback、oracle/evaluation-only；
3. **output type**：估计、检测、软信息、动作、回退、资源参数、生成模型；
4. **mechanism family**：解析、监督、SSL、无监督、生成式、在线适应、混合、控制；
5. **domain axis**：SNR、调制、CSI、长度、动态速率、湍流、coded/uncoded、hard/soft。

Candidate Portfolio 是开放地图，不宣称数学完备。Skill 记录已覆盖角度和明显空白；只有确认当前 portfolio 足以进行有信息量比较后才进入 Batch。

### Phase C：Plan a batch portfolio

一次规划多个相互独立或共享接口的科学问题。批次按共享 baseline、realization、指标和因果问题组织，不按论文标题或单个模型组织。

每个 Batch Card 只需要：

`question | candidates | shared baseline | domain slice | comparator | diagnostics | cost | dependencies | exit | claim ceiling`

相互依赖的 adapter、evaluator、closure 和 smoke 合成一个 Sprint；不在每完成一个小接口后停止汇报。

### Phase D：Prepare and run

Skill 生成批次合同，调用项目 runner 和确定性工具。运行前必须保护：baseline identity、source closure、信息边界、指标口径、历史路径和预注册退出条件。

一个批次通常比较：

- no-change baseline；
- strongest legal simple comparator；
- 一小组共享接口的机制变体；`2–6` 仅是 shadow 初始启发式，不是批次合法性硬门；
- 必要的一轴 ablation 或显式 interaction hypothesis。

批量大小由信息量与成本决定，不用固定的全局批次数作为合法性门。

### Phase E：Synthesize

Skill 横向回答：

- 哪个机制诊断按预期变化；
- 主指标是否同步改善；
- 正信号是否可能修 bug、利用额外信息或来自统计噪声；
- 负信号关闭的是 cell、slice、contract、candidate 还是 family；
- 哪些 blocked axes 恰好包含历史反例；
- 下一步是扩域、换候选、建共享能力还是晋级。

独立 verifier 检查运行真实性；独立 science critic 检查统计、scope 和 comparator，但二者只返回审查意见，不接管主循环。

### Phase F：Harvest

每批至少进入一个收获类别：

- `METHOD_SIGNAL`：可继续发展的机制；
- `BOUNDARY_RESULT`：baseline/候选在什么条件下成立或失败；
- `LOCAL_NEGATIVE`：明确有效域的负面结果；
- `FAILURE_MECHANISM`：为什么失败；
- `EVALUATION_INSIGHT`：指标、oracle、统计或 scope 的方法学发现；
- `REUSABLE_ASSET`：runner、adapter、数据、comparator、测试；
- `INFRASTRUCTURE_GAP`：阻断多个候选的共享能力；
- `WRITING_MATERIAL`：可进入论文背景、实验设计、讨论或局限性的素材。

没有 winner 的批次仍可能产生论文价值；“无任何新收获”才是真正低信息批次。

### Phase G：Rotate or deepen

优先级由 Skill 判断：

1. 修一次低成本且不改变科学合同的问题；
2. 运行同批其他 ready 候选；
3. 切换到另一个机制族；
4. 建设服务多个候选的共享能力；具体候选数由 shadow 观察，不作硬门；
5. 对局部结论进行 domain atlas 扩展；
6. 重新展开 Candidate Portfolio；
7. 将稳定 winner 晋级 Deep Evidence。

每次必须写出下一动作及理由，但不需要脚本证明“工作守恒”。

## 8. Scope 与 Headroom Atlas

局部 negative 或 baseline 近 oracle 时，不立即关闭候选族。Skill 先生成 Scope Assessment：

- 已运行条件；
- runnable 但未覆盖条件；
- infrastructure-blocked 条件；
- 历史正/负反例；
- 当前 claim ceiling；
- 最有信息量的下一轴。

Atlas 分两级：

- **Stage A covering array**：少量代表 cell 横跨已支持 axes，定位可能的 headroom 区；
- **Stage B targeted expansion**：只在 Stage A 出现机制相关区域时增加 seeds、细化轴或训练 ML。

Blocked axis 不是 candidate failure。若历史反例恰好落在 blocked axis，DOMAIN/CANDIDATE/FAMILY 必须保持 OPEN 或 UNRESOLVED。

## 9. Deep Evidence 的调用时机

完整 Groundwork/Contract/正式实验不是每个微变体的前置税，而是晋级模块。以下情况触发：

- 批次出现稳定、机制一致的正信号；
- 候选准备形成新颖性或论文贡献声明；
- 跨入新领域或现有文献资产明显不足；
- 需要正式参数溯源、竞品闭合或大样本统计；
- 局部负面准备升级成 domain/candidate 级主张。

Deep Evidence 应增量复用已有论文、read notes、结果和 failure registry，只补证据缺口。

## 10. 自动继续与停止

### 10.1 不允许停机的局部事件

- 单候选失败或一个 slice 没 headroom；
- 一个接口/closure 缺失但其他候选 ready；
- science critic 拒绝某份 synthesis；
- 一次可修复的 provenance 问题；
- Stage B 未触发；
- 一个候选出现局部正信号；
- 上下文切换、定时汇报或单个 Sprint 完成。

### 10.2 允许请求用户决策

- 需要改变论文主线、场景或贡献定位；
- 多条 thesis spine 都已形成，需战略选择；
- 下一共享能力是明显的大型投资；
- 所有 ready、small-adapter 和合理扩域路径均已证据化处理；
- 历史/证据 P0 无安全替代路径；
- 需要用户、导师或私有材料才能继续。

### 10.3 防循环

- 同一 batch 默认只做一次不改变科学合同的修复；这是待 shadow 校准的防循环启发式，不是生产硬门；
- 同一微变体连续两轮改善小于 10%，退出微调（项目安全上游：`AGENTS.md`「分层试错法」P2）；
- 同一机制族默认连续两批无新机制信息后换族；“两批”是待 shadow 校准的启发式，不是生产硬门；
- 同一 blocker 连续出现时，判断是否是共享 capability；不是则 defer，不继续补接口；
- 治理/基础设施工作若持续一个 Sprint 仍未解锁多个候选，默认停止建设并回 portfolio；“一个 Sprint / 两个候选”只作 shadow 观察启发式，不作硬门。

## 11. 文件与状态体系

### 11.1 Skill 包

```text
research-direction-lab/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── core-loop.md
│   ├── candidate-portfolio.md
│   ├── batch-and-atlas.md
│   ├── evidence-and-claims.md
│   ├── thesis-harvest.md
│   ├── recovery-and-rotation.md
│   ├── project-layout.md
│   └── profiles/
│       └── communications.md
├── scripts/
│   ├── hash_bundle.py
│   ├── validate_receipt.py
│   ├── append_event.py
│   ├── rebuild_state.py
│   └── render_status.py
└── tests/
    ├── cases/
    └── test_structure.py
```

`SKILL.md` 保持精简，只放触发条件、责任边界、主循环、停止条件和 reference 路由。详细方法按需加载，不建立 README/CHANGELOG 等平行解释文档。

### 11.2 项目实例

```text
projects/<project>/direction-lab/
├── STATUS.md                 # 唯一人类入口，一页全局状态
├── project.yaml              # Project Adapter：anchor、路径、组件、axes
├── state/
│   ├── events.jsonl          # append-only 运行/处置事实
│   └── current.yaml          # 可重建投影
├── portfolio/
│   ├── candidates.yaml       # 当前候选卡与 lineage
│   └── batches.yaml          # 当前批次组合与依赖
├── batches/
│   └── B###-slug/
│       ├── manifest.yaml
│       ├── artifacts/
│       ├── receipt.json
│       ├── verifier.md
│       └── synthesis.md
├── harvest/
│   ├── ledger.yaml           # 所有级别的论文收获
│   └── thesis-spines.md      # 少量候选论文主线
├── registries/
│   ├── components.yaml
│   └── failures.yaml
├── tools/                    # 项目专属 runner/adapter/evaluator
├── tests/
└── archive/
```

### 11.3 索引与抗膨胀规则

- 日常恢复只读 `STATUS.md`、`project.yaml`、`state/current.yaml`、`portfolio/batches.yaml` 和 harvest 摘要；
- 默认每批聚合为一个 verifier 和一个 synthesis，逐 seed/cell 不建 Markdown；“一个”是抗膨胀 shadow 约定，不是生产合法性硬门；
- raw 数据只在 artifacts，ledger 只存 ID、scope、hash 和 pointer；
- `.sessions/` 只记录里程碑、决策、原话和 handoff，不承载逐接口运行状态；
- 旧 portfolio 进入 archive，不在根级保留 v1/v2/v3 多个活跃版本；
- 状态文件不保存流程说明，Skill 不保存项目当前状态。

## 12. 一页状态要求

`STATUS.md` 固定回答：

1. 正式论文目标与当前授权；
2. anchor/baseline 是什么；
3. 当前 portfolio 有多少候选、机制族和 blocked axes；
4. 最近完成了哪一批，科学上得到什么；
5. 当前正在执行还是仅规划/被阻；
6. 当前 thesis harvest 有哪些可写素材；
7. 下一自动动作是什么；
8. 什么条件才会需要用户拍板。

不允许用户通过猜 batch 名、翻 session 或阅读 controller 日志判断是否在跑。

## 13. 现有资产迁移

### 13.1 保留

- `method-family-batch-exploration` 的 anchor、candidate map、batch、promotion 思路；
- manifest、source closure、component identity、result hash、receipt；
- append-only completion event 与 deterministic reducer 的实现经验；
- duplicate/replay/stale/orphan/history/path boundary 检查；
- claim-scope 层级、P03 Atlas、existing runners/evaluators；
- Communications Profile 与 Project Adapter 的分层概念；
- B001–B003/P03 的全部历史证据和负面结论。

### 13.2 吸收到主 Skill

- Scout/Sandbox/Promotion 的导航；
- Candidate Portfolio 展开和批量排序；
- capability triage、换族、扩域和 atlas 设计；
- Deep Evidence 调用时机；
- thesis harvest、恢复和长跑 checkpoint；
- 全局停止与用户升级判断。

### 13.3 降级或移除

- `science_slots`、候选资源匹配和 work-conservation 求解；
- 固定 `min_valid_batches/min_evidence_families` 作为生产合法性门；
- campaign code 对候选完整性、科学充分性和下一方向的判断；
- 为每个微接口建立 Queue/Registry/fingerprint 的做法；
- `process.md` 作为未来流程 owner 的角色；Skill 激活后它只保留项目实例说明或归档指针；
- 重复 CandidateMap v1/v2/v3 作为多个活跃真相源。

### 13.4 逐函数审计后再决定

`campaign_core.py/campaignctl.py` 不整块保留或整块删除。实施阶段按责任测试逐函数分类：

- 确定性完整性函数 → 提取到小工具；
- 科学调度/覆盖/停止函数 → 删除或改为事实报告；
- 项目语义 → 移入 Adapter；
- 无调用或只为旧 schema 服务 → 归档。

## 14. Skill 验收

### 14.1 结构测试

- SKILL.md 能清楚路由 references，主体不过度膨胀；
- 通用 scripts/core 不出现 BER、SNR、CMA、pilot、OSL 等领域词；
- 项目状态与 Skill 内容互不复制；
- 没有两个文件同时声称拥有同一流程或状态。

### 14.2 历史重放

用 B001–B003、P01、P03 和 Headroom Atlas 作为只读场景，验证 Skill 是否会：

- 识别 pilot-Jones 正信号可能只是修 current-CMA bug；
- 在 P01 action effect 不可观测时换路，而不是继续补 U24 runner；
- 把 P03 QPSK/CSI_NONE/hard-decision 结论限定为 local；
- 识别 16QAM、receiver-CSI、coded-output blocked axes；
- 保存 residual-energy 与 BER 分离等次级结果；
- 不把治理 PASS 写成科学进展。

### 14.3 前向行为测试

给新 agent 最小上下文和真实项目入口，不泄露预期答案。至少观察：

- 先 map 后 run；
- 一个局部 blocker 后自动换候选；
- 一次 Sprint 补齐相互依赖的小接口；
- 没有 headroom 时先做 scope assessment；
- 每批更新 harvest 与 STATUS；
- 在 timeboxed shadow 窗口内记录无意义停机和逐项请求用户拍板的次数；窗口长度在 shadow 前另行确认，不在蓝图中预设无来源阈值；
- 文档增长默认聚合为批次级 synthesis，不产生逐 cell 日志；单批文档数量作为 shadow 观察项，不作硬门。

### 14.4 成效指标

| 指标 | 目标 | 合格来源 |
|---|---|---|
| 存在合法替代工作时的自动续跑率 | 100% | 用户原话：U04/U06 |
| 局部证据错误外推次数 | 0 | 证据完整性：U08 / §8 claim-scope 保护 |
| 历史证据污染/伪造 trusted receipt | 0 | 项目安全：D001 的 history/receipt 不变量 |
| 用户因“不知道在干什么”而纠偏 | 0 | 用户原话：U14 |
| 每批产生至少一种可验证 harvest | 100% | 项目范围：`topic-index.md:41`；U13 |
| 治理/基础设施时间占比 | shadow 只记录基线；目标值须依据实测基线另行审定 | shadow heuristic，不作硬门 |
| 通用代码中的领域语义 | 0 | 用户原话：U11；职责边界：§4.2–4.4 |

## 15. 分阶段启用

1. **Blueprint freeze**：审定本文、原话映射、责任边界和迁移表。
2. **Skill skeleton**：建立主 Skill 和 progressive disclosure references，不改现有运行授权。
3. **Thin safety tools**：从现有代码提取必要的 hash/receipt/event/state/status 小工具；不建 scheduler。
4. **Project adapter migration**：把双偏振 OSL 事实映射到新 project.yaml，历史资产只读导入。
5. **Historical replay**：用旧场景验证 Skill 决策，不运行新科学实验。
6. **Timeboxed shadow**：在隔离工作区真实运行一段时间，重点观察持续推进、scope 和组织，不追求治理 schema 数量。
7. **Live activation**：通过后才让 Skill 接管新 batch；旧流程保留只读回退期。
8. **Retirement**：确认新入口稳定后，再归档旧 process/campaign 控制面，禁止提前删除。

## 16. 明确不建设的内容

- 通用 DAG/插件平台；
- 通用科学资源调度或 matching solver；
- 用固定批次数证明 portfolio 完整；
- 自动把所有论文检索、GW、Contract 串成不可变状态机；
- 加密签名、外部不可变 registry 或分布式并发 campaign；
- 一个可以理解所有领域科学语义的 Universal Core；
- 为每个历史失败增加一条新硬门。

这些能力只有在真实使用出现重复、确定、无法由 Skill 判断的失败后，才可重新评估。

## 17. 蓝图完成判据

本文只有同时满足以下条件才可进入实施：

- 用户原话的核心要求均有需求 ID 和验收场景；
- Skill、代码、Profile、Adapter、项目状态和用户权力无重叠 owner；
- 从零、从地基、批量运行、扩域、换路、Deep Evidence 和 harvest 全闭环；
- 文件体系给出唯一入口、状态恢复和抗膨胀策略；
- 现有资产有明确保留/吸收/降级/待审计分类；
- 实施顺序先历史重放、后 shadow、最后激活；
- 未把开放式科学判断重新编码为硬求解问题。

## 18. U01–U15 需求溯源附录

### 18.1 来源与拥有者

本表只保存来源指针和设计翻译，不复制历史原话。未加前缀的指针指向用户自然原话；历史 voice 中由执行任务文本复制而来的条目统一标为 `[转述:执行提示词]`，只能作为辅助来源。行号以 Blueprint freeze 时三份已引用 `voice.md` 为准。

| ID | 来源 voice 位置 / 独立依据 | 依据性质 | Primary owner（唯一） | Supporting / storage（非 owner） | 冻结结果 |
|---|---|---|---|---|---|
| U01 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:65-66`；`.sessions/2026-07-17-direction-lab-governance-pilot/voice.md:15` | 用户原话 | §6.1「从已有地基开始」 | §4.4 Adapter 存项目事实 | 接受 |
| U02 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:33,42,66` | 用户原话 | §7 Phase B「Map」 | Phase C 消费 map | 接受 |
| U03 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:13,66`；`AGENTS.md:104-105` | 设计推导：原话要求积累精读材料且不机械重复；项目安全硬门禁止跳过 Step 3/4a | §9「Deep Evidence 的调用时机」 | §7 Phase D 执行批次 | 接受为增量复用规则，不授权跳过项目硬门 |
| U04 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:62,65` | 用户原话 | §10「自动继续与停止」 | §7 Phase G 实现换路 | 接受 |
| U05 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:29,41-42,62` | 用户原话 | §7 Phase B「Map」 | 无 | 接受 |
| U06 | `.sessions/2026-07-17-direction-lab-governance-pilot/voice.md:7`；`.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:65` | 用户原话 | §10「自动继续与停止」 | §12 提供可读 checkpoint | 接受 |
| U07 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:42,80`；`.sessions/2026-07-17-direction-lab-governance-pilot/voice.md:53` `[转述:执行提示词]` | 用户原话；执行提示词辅助 | §7 Phase C「Plan a batch portfolio」 | Phase D 执行计划 | 接受；Sprint 不是固定全局批次数 |
| U08 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:74-76` | 用户原话；证据完整性 | §8「Scope 与 Headroom Atlas」 | 无 | 接受 |
| U09 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:13`；`.sessions/2026-07-20-research-direction-lab-system/topic-index.md:15,41` | 设计推导：原话要求“攒材料”；冻结范围要求持续积累论文素材且每批形成收获/资产 | §7 Phase F「Harvest」 | §11.2 `harvest/` 只负责存储 | 接受 |
| U10 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:48,54,62`；`.sessions/2026-07-17-direction-lab-governance-pilot/voice.md:55-57` | 用户原话；项目安全 | §11「文件与状态体系」 | §12 提供人类入口 | 接受 |
| U11 | `.sessions/2026-07-20-research-direction-lab-system/voice.md:7` | 用户原话 | §4.2「通用代码」 | §4.3 Profile / §4.4 Adapter 承载领域与项目语义 | 接受 |
| U12 | `.sessions/2026-07-20-research-direction-lab-system/voice.md:7`；`.sessions/2026-07-17-direction-lab-governance-pilot/voice.md:5` | 用户原话；D001 的 V035/V037 证据链 | §4.1「主 Skill」 | §4.2 只提供确定性护栏 | 接受 |
| U13 | `.sessions/2026-07-10-dual-pol-osl-groundwork/voice.md:13,21,65`；`.sessions/2026-07-20-research-direction-lab-system/topic-index.md:15,41` | 用户原话；冻结项目范围 | §7 Phase F「Harvest」 | §14.4 只测量成效 | 接受 |
| U14 | `.sessions/2026-07-17-direction-lab-governance-pilot/voice.md:55-57` | 用户原话 | §12「一页状态要求」 | 无 | 接受 |
| U15 | `.sessions/2026-07-20-research-direction-lab-system/voice.md:8-9`；`AGENTS.md`「voice.md」治理规则 | 用户原话；项目安全 | §2「用户原话派生要求」 | 各专题 `voice.md` 存原话；§18 存指针 | 接受 |

### 18.2 设计规则准入与拒绝

后续实现只能接收三类来源：用户原话、证据完整性、项目安全。用户自然原话保持无前缀；执行提示词只能以 `[转述:执行提示词]` 标记后作为辅助来源，不能单独创建设计要求。架构章节拥有目标行为，`voice.md` 拥有原话，本文不成为第二份原话档案。

本次 freeze 将所有无独立来源的精确数值降为 shadow heuristic：批次 `2–6` 个变体、单 batch 一次修复、机制族两批换路、一个 Sprint/两个候选、每批一个 verifier/synthesis、固定 60 分钟与治理占比 20%。它们只用于 shadow 观察，待实测基线和用户审定后才可成为硬门。唯一保留的“连续两轮改善小于 10%”直接继承 `AGENTS.md` P2；成效表中的绝对安全/质量目标逐项列出上游来源。
