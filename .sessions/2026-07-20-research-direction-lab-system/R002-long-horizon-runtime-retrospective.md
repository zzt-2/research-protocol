# [R002] Research Direction Lab 长程运行复盘

> 2026-07-23 | 关联：2026-07-20-research-direction-lab-system / D014-D015
> 审计性质：只读历史复盘；未运行实验，未修改 Skill/controller/science-scout/Pilot-Jones

## 调研问题

既有方法论、governance pilot、Research Direction Lab system 和首轮真实
science-scout 已投入大量设计、实现与验证，为什么仍在真实长跑中出现单点深挖、
治理膨胀、科学结论撤回和 current owner 冲突？哪些设计应保留，哪些只需最小修补，
下一次真实长程测试怎样才能检验“提高方法发现概率”，而不是再次只检验守规则？

## 审计边界与方法

采用 S013 冻结的“控制链全读 + 五类关键转折深读 + 原始证据按需抽查”：

1. 控制链：旧 `method-family-batch-exploration`、governance pilot、本专题
   S001-S013/D001-D015/V001-V011、science-scout S001-S014/D001-D022/
   V001-V012/H001-H015、项目 current views 和 `master-state.md`。
2. 关键转折：原批量方法论承诺；首个轻量/合法/有信息增量工作包；由轻转重；
   F1/F3 正信号撤回；current/protected/master-state/worktree 冲突。
3. Git 抽查：关键提交的路径、净增长、先后关系和 branch 可见性。
4. 不把文件行数直接等同时间成本，不把局部负面等同 family/domain 失败，不把
   verifier 的 artifact-fidelity PASS 等同科学语义 PASS。

### H005 接收核验

- worktree 为 `.worktrees/direction-lab-capability-atlas`，分支
  `codex/direction-lab-capability-atlas`，接收时 clean。
- 接收时 HEAD 为 `f0c24d4`；H005 所记 `23ed9fa` 是其直接父提交。
  `23ed9fa..f0c24d4` 只新增 H005 并更新 topic-index/registry，属于 handoff
  落盘后的预期前移，不是祖先 worktree 串线。
- S013、D014-D015 和 topic-index 均把唯一 next action 指向 R002。
- science-scout 已由 S014/D022/V012/H015 收口为 dormant/SCIENCE_FREEZE；
  `projects/thesis-fso/master-state.md:23-33,97` 将 Pilot-Jones 单独列为 formal
  Groundwork Step 3.5 PARTIAL，Step 4a 未授权。
- 本专题 `depends_on` 为 framework-evolution、dormant governance pilot 和
  simulation-foundation-rebuild，`conflicts_with: []`；本轮未改依赖专题。

## 发现

### 事实一：时间—目标—动作—证据—裁决—论文增量

| 时间/阶段 | 当时目标 | 实际动作与证据 | 当时/最终裁决 | 可确认的论文增量 |
|---|---|---|---|---|
| 2026-07-16 原批量方法论 | 从已有 runnable anchor 展开候选地图，按共享接口和因果问题批跑，稳定 winner 才晋级 | `method-family-batch-exploration/SKILL.md:15-45,55-66`；`dual-pol-osl-groundwork/S041-candidate-family-map-batch-plan.md:15-73,89-93` | anchor→map→causal batch→winner promotion 主干成立；当时只有地图、计划和压力测试 | 0；候选组织资产 |
| 2026-07-17 governance pilot 起步 | 观察最低限度哪些门必须脚本化 | 5 个硬门、receipt/EvidenceGate、4 轮 gate 压测、5 个 shadow 循环；`governance-pilot/S001:5-17,42-76`、S002-S003 | 核心隔离 PASS；跨上下文恢复仍 PARTIAL | 0；pilot 明禁论文结论 |
| 2026-07-17 B001 | 从纯治理扩到真实地基 sandbox，首跑 30-cell paired batch | `governance-pilot/verifications.md:236-241` 后验发现 CandidateMap 算术错误和 AE 预注册/实现错配 | artifact 可复现，但整体降为 `COMPLETED_SANDBOX_WITH_PROTOCOL_DEVIATION` | 只有 diagnostic |
| 2026-07-18 B002 | 用 corrected Map/Queue 和真正无标签 AE 做合法批次 | 30 cells、31/31 import closure；Queue 前 90 tests、13 类对抗变异；`governance-pilot/verifications.md:309-375` | 首个完整合法科学批次；linear/MLP `ADVANCE_SPECIFIC`，AE `RETIRE_SPECIFIC`，仅 exact contract | 有机制观察；明确不等于论文材料资格 |
| 2026-07-18 B003 | 为 v3 Queue/Registry/Runner/Validator 再验证一次 | 又跑同一 30-cell/三机制合同；`governance-pilot/verifications.md:432-465` | 治理链 PASS，但结果与 B002 重合；D007 已承认新增科学信息很少 | 近似 0 |
| 2026-07-18 P03 interface smoke | 用最小接口片验证 residual-headroom 可运行性 | 512 symbols、1 realization、1 cell，35 tests、23-file closure；`governance-pilot/decisions.md:295-345`、`verifications.md:564-607` | `SCOUT_CONTRACT_READY`，未跑性能、未进 Sandbox | 可复用接口资产，无科学性能增量 |
| 2026-07-20 system Task 1-8 | 建立 Skill-first 体系、确定性工具、投影、scheduler 审计和行为盲测 | 路径过滤口径净增 61 文件、7,404 行，0 次科学运行；提交 `cfb29f0`、`61b623d`、`e2f42e8`、`f79cb1b` | 结构/安全/五类单轮行为 PASS；V004 明写不构成长程自动化证据，见 `verifications.md:183-191` | 0；只投影旧 harvest |
| 2026-07-20 Task 9 shadow | 获取“长期”行为证据 | 实际为同一工作窗内 frozen-history replay，未生成候选、未接收真实实验反馈；派生 8 个 `promotion_block` SHADOW harvest，见 `S009:42-68` | 验证 replay 守边界，不是长期真实科学能力 | 0 新实验；旧证据再分类 |
| 2026-07-20 Task 10/消费者部署 | live activation 与消费者可达 | V006 先授权 activation，随后 S011 才发现普通根无 Skill/STATUS/Adapter、全局 Skill 不存在、旧 Skill 指针悬空；`S011:14-23` | release/consumer owner 断链靠 integration worktree 补救 | 0 |
| 2026-07-20~21 首次 SCIENCE_SCOUT | 从 CB1 headroom 进入方法候选 | 首次真实运行立即暴露任务失配/欠收敛 baseline；D010 后补 conventional-baseline 门。C01-C04 又暴露共同 anchor 冒充 task comparator、shared input 冒充 runnable；D011 后补公平性与 readiness | system 从“预设行为 PASS”转为 live failure 驱动修补 | baseline/fairness 诊断，无稳定方法 |
| 2026-07-21 C11/C04/C09 | 对合法化 signal 和 learned corrector 做批次判断 | C11 阳性在 legalization 后消失；C04/C09 的完整 provenance 链最终被外部语义审计发现目标函数存在输入无关常数最优解，见 science-scout S010:13-36 | 数字可复现；机制级负面撤回，候选改为 implementation-confounded/unresolved | 一个重要 failure mechanism/评估教训，无方法信号 |
| 2026-07-21 D012-D013 | 修复“极小探针变重”和语义晚门 | Probe→Scout→Deep Evidence、semantic smoke、current/lineage、轻量 harvest、抗膨胀布局在 `098c1a4` 才进入 Skill | 这些是 live failure 后修补，不能由此前 V004/V005 反向证明 | 0；流程资产 |
| 2026-07-22 S012/D020 | 对 F1/F3/F4 信息来源做 Probe | F1-A 报 0.1329 headroom、\|r\|=0.651；F3-A 报 MI +0.060、R² +0.036；F1-B 被列首选，见 `science-scout/S012:39-63` | 当时 F1/F3 PASS、F1-B 待一天级投资 | 短暂正信号，后撤回 |
| 2026-07-22 D021（`bf620b3` 后 2h18m38s） | 科学语义纠偏 | F1 oracle 同时用了真实 h/θ 与 TX-truth calibration，features 读未来，全程未调用合同 comparator；F3 是两个 marginal MI 最大值相减；`science-scout/S013:19-31` | F1/F3 PASS、正面候选和投资授权全部撤回；原始数字留历史 | 评估/因果边界教训 |
| 2026-07-22 F1-A0 与 D022（再过 45m40s） | 严格因果修复并决定 campaign 去留 | 110 rows；g0 8 help/13 hurt/89 tie，p≈0.38；同时发现 SOP 窗内仅 0.06°、CMA μ 债、E2 pilot/输入路径问题；`science-scout/S013:33-53` | F1 当前任务 FAIL，但 family 仅 `TESTBED_BLOCKED`；F3 `UNRESOLVED`；随后 SCIENCE_FREEZE | 无合法 main-method spine；保留局部负面和方法论材料 |
| 2026-07-22~23 控制面收口 | 回正式窄问题链 | current state/portfolio/harvest 已指 H015 和 SCIENCE_FREEZE；Pilot-Jones 由 `287002b` 单独激活为 formal GW Step 3.5 PARTIAL | science-scout dormant；Pilot-Jones 4 篇竞品全文仍 blocked，不进 Step 4a | 未新增 |

### 事实二：规模与吞吐

#### 2.1 控制记录规模

- 在 `f0c24d4`、R002 落盘前的审计基准快照下，governance pilot、system、
  science-scout 三专题合计 77 个顶层文件、9,702 行控制文档。该口径不含
  raw artifacts、代码和 Skill，只证明恢复/治理面很大，不能单独证明治理导致
  科学失败。
- governance pilot 的限定路径历史净增长为 153 文件、14,506 行；其中完成
  3 个 30-cell sandbox batch（90 cells）和 1 个单-cell interface smoke，同时有
  4 轮 gate 压测、5 个 shadow 循环、13 个 D、19 个 V、三代 Queue/Registry/runner。
- system Task 1-8 的限定路径净增长为 61 文件、7,404 行、0 次科学运行；
  其中测试/fixture/盲测约 2,723 行，生产 Skill/references 约 750 行。
- science-scout 当前有 14 S、15 H、22 D、12 V，共 63 个编号记录；
  33 个顶层控制文件共 4,804 行。实际呈现接近“每个 S 对应一个 H”，和 D014
  后来明确拒绝的“每工作包 S/D/V/H 全套”一致。
- 从首次正式 science-scout 到 freeze，共 15 个提交触及 science-scout 路径；
  排除 `34ab1b0`、`850b35e`、`ac8bd1e` 三个 system/doc 修补后，可辨 12 个
  science-bearing path 提交。raw artifact 主导文件/行数增长，但最终 current
  harvest 的 primary/secondary method spine 均 withdrawn。

#### 2.2 轻量、合法、科学信息增量三条件

审计区间内没有一个早期工作包同时满足三条件：

- governance pilot B002 是首个“合法 + 有科学信息增量”的完整批次，但它背后已有
  31-file closure、90 tests、13 类对抗门和大体量 artifact，不是整体轻量。
- P03 interface smoke 是首个“轻量 + 合法”的包，但只回答接口 readiness，
  没有科学性能增量。
- F1-A0 接近新 Probe 设计，却在错误 testbed、比较路径和实现债下得到局部 FAIL；
  它的信息价值主要是及时否决 F1-B 投资，而不是方法信号。

因此，“首个同时轻量、合法并产生科学信息增量的端到端包”仍未被真实证明。

### 事实三：设计承诺与真实运行差距

| 设计承诺 | 设计/局部验证 | 真实运行 | 复盘裁决 |
|---|---|---|---|
| Science-first、论文增量优先 | 蓝图和 Skill 均明确；governance 不算 harvest | pilot B003 为验证 v3 治理链重复 B002 合同；Task 1-8 零科学；science-scout 最终无 active method spine | **未稳定兑现** |
| 自动继续 = 选择更有信息的合法动作 | Task 8 B1/B6 只判“有合法具体动作”；Task 9 replay rotation 100% | 未比较合法动作之间的信息增益；可以合法地继续深挖单点或补治理 | **验证对象错位** |
| 成本随声明升级 | D013 后文本已采用 Probe/Scout/Deep Evidence | D013 之前的轻问题已有 Queue/receipt/verifier/多记录；S012 正信号也在基本因果/任务检查后才撤回 | **方向正确，长跑未验证** |
| 语义先于完整性 | D013/evidence-and-claims 已写 semantic smoke | C04/C09 在完整 hash/receipt/verifier 后才发现常数最优；F1/F3 在 PASS/投资选择后才检查信息边界和指标含义 | **运行顺序曾反转** |
| 当前视图优先、唯一 owner | reducer/current projection 和 inactive filtering 有测试 | protected STATUS、preview adapter、science current、formal master-state 和 branch-local worktree 曾同时表达不同“当前” | **机械组件 PASS，部署合同 PARTIAL** |
| harvest 必须反映论文价值 | D013 后允许 `no_durable_harvest_reason` | Task 8/9 旧硬门却要求每案/每 replay batch 至少一个 harvest，内生鼓励造条目 | **旧合同冲突，需退役** |
| Skill-first、code-guarded、唯一 process owner | no-scheduler tests 和通用/领域隔离 PASS | AGENTS/process/README/architecture 又重复部分边界；release 可达性和项目事实仍需多载体人工拼接 | **核心保留，路由面应再收窄** |
| 局部失败不终止、候选族批量轮转 | claim ceiling/blocked-as-gap 守住 | science-scout 确实轮转，但 runtime 奖励“有下一动作”，没有奖励“新增候选区分或方法发现概率” | **续跑成立，方向质量未验证** |

### 事实四：F1/F3 与状态冲突的完整因果链

#### 4.1 科学语义链

1. D020 的正信号首先是 privileged genie gap 与错误指标解释，不是合法 tracker
   headroom/conditional MI。
2. V009 主要确认 identity、hash、seed 和数字可复现，没有完成科学因果语义审查。
3. D021/V010/V011 将 F1/F3 撤回并用 F1-A0 重写证据基础。
4. F1-A0 的 g0 FAIL 存活，但 E2 pilot、blind-affine 输入、CMA μ、公平性和
   weak-dynamics atlas 都限制 claim ceiling；不能写成 model-prior family negative。
5. D022 正确收口为 F1 `TESTBED_BLOCKED`、F3 `UNRESOLVED`、
   F4 `INFRASTRUCTURE_BLOCKED`，而不是完整负面论文。

#### 4.2 current/protected/formal owner 链

- 当前 `state/current.yaml:27-30,223-233`、`portfolio/current.yaml:117-159`、
  `harvest/current.yaml:322-405` 已一致表达 dormant/SCIENCE_FREEZE 和 withdrawn
  spines。
- V012 的 PASS 有范围漏检：在 `170c00c` 后，authorization 字段仍曾写
  `SCIENCE_SCOUT/science_authorized:true`，到 `287002b` 才修正。因此 V012
  证明已检查字段和本轮 byte identity，不证明“所有 stale current 字段均已修正”。
- `STATUS.v1.md:2-9` 仍写 D020/F1-B 首选；它是
  `STALE_PROTECTED`，不得作为 routine current entry。
- 所谓 protected byte-identical 只表示 S014 未继续改写当时基准。历史 Git 表明
  campaign 已多次改过 STATUS；不能把 V012 的相对 MD5 当成恢复到最初 protected
  identity。
- `project.v1.yaml:18-25` 仍是 `READ_ONLY_MIGRATION_PREVIEW`；形式授权在
  `master-state.md`，Direction Lab 科学投影在 `state/current.yaml`。当前可人工拼对，
  但 adapter/STATUS/current/formal authorization 的机器 owner 仍未完全收敛。
- `170c00c`、`287002b` 只在当前 capability-atlas 分支可见。current 是 branch-local
  事实，不是所有 worktree 自动共享事实。

## 结论

### 主要根因与首次出现位置

#### R1 验收对象错位：把合规输出当长程科学能力

- **首次明确位置**：Task 8 R001/V004。五个单轮 fixture 直接提供 allowed actions
  和 claim ceiling；scorer 能检查守边界，不能比较哪个合法动作信息增益最高。
- **后续复现**：Task 9 用 frozen replay 取得“长期”PASS；没有候选生成、真实实验
  反馈、跨上下文漂移或资源摩擦。
- **因果结论**：这解释了为何大量设计/测试没有在激活前发现 baseline、
  semantic-smoke、current-owner 问题。不是测试造假，而是它们回答了更窄的问题。

#### R2 科学语义门晚于证据完整性门

- **首次明确位置**：governance pilot B001 的 AE 合同偏差；science-scout 中又在
  C11、C04/C09、F1/F3 连续复现。
- **机制**：hash、receipt、source closure、paired seeds 和 verifier 证明“坏任务被
  忠实执行”；它们不能证明 objective/label/output/metric、平凡解、因果信息和
  comparator 语义正确。
- **应复用教训**：TL-20/TL-22/TL-23/TL-29/TL-33 和 D013，不能再新造一套。

#### R3 工作强度由流程完整度驱动，而非活跃科学不确定性

- **首次无歧义位置**：B002 已给出合法 exact-contract 结果后，B003 为 v3
  Queue/Registry/Runner/Validator 重跑同一合同；D007 已记录科学增量很少。
- **后续复现**：轻量接口/Probe 机械生成 S/D/V/H、receipt、verifier、synthesis；
  science-scout 14 S 对应 15 H。
- **因果结论**：所谓“极小”只缩小了计算，不一定缩小端到端工作包。

#### R4 自动继续优化了 work conservation，不等于优化方法发现概率

- **证据**：Task 8/9 以“存在具体下一动作”“每批有 harvest”“合法 alternatives
  100% 续跑”为 PASS；没有记录候选排序是否因新事实改变、是否重复同一机制、
  是否更接近 method spine。
- **结果**：失败后系统往往能继续，但继续内容可能是补治理、补 verifier、修状态，
  而不是换机制族或回答最便宜的 scientific uncertainty。

#### R5 current/release/formal authorization 没有同一原子切换边界

- **首次明确位置**：Task 10 live activation 后才发现消费者路径断链；随后
  science-scout 又出现 protected STATUS、preview adapter、current YAML、
  master-state 和多 worktree 的 visibility/ownership 分裂。
- **因果结论**：唯一 owner 在设计上存在，但部署和 branch cutover 没有被当作同一
  transaction 验收。

#### R6 orchestration 粒度过细，主控/执行者/会话治理职责重叠

- **证据**：一个 science work package 常同时留下 S、D、V、H 和 artifact；
  没有稳定使用 `worker-logs/` 承接命令、尝试和偏离，H 兼任工作包交接。
- **结果**：主控恢复需要扫描大量同层 prose；用户仍被迫中转上下文；D014
  到最后才冻结四层记忆和 T/worker-log/H 分工。

### 不能从本复盘推出的结论

- **不能证明候选本身一定足够好。** 科学问题可能确实困难，但多条路线先死于
  comparator、目标、信息或 testbed，无资格据此宣布“候选质量差是主因”。
- **不能证明治理是无方法结果的唯一原因。** 本复盘只证明治理/验证没有及时截断
  若干无效投资，并占用了大量工作面。
- **不能证明 Direction Lab 核心主干应废弃。** anchor、open portfolio、causal batch、
  claim ceiling、explicit disposition 和 rotate/deepen 均有可复用价值。
- **不能把 F1/F3/F4 写成 family/domain negative。** 当前分别是 blocked、
  unresolved、blocked。
- **不能把 Task 8/9 PASS 改写成 FAIL。** 它们对各自窄合同成立；应删除的是
  “它们足以证明长期科学产能”的解释。

### 保留 / 修正 / 删除或退役 / 尚未验证

#### 保留

- anchor→map→causal batch→winner promotion 的原方法主干。
- baseline 充分性、task-specific comparator、公平调参与 semantic smoke。
- claim ceiling、blocked-as-gap、protected-history、explicit disposition 和
  current/lineage 分离。
- Probe→Scout→Deep Evidence 的成本方向；assessment 必做、harvest item 非必做。
- B001 protocol deviation、B002 exact-contract、B003 governance-only repeat、
  C04/C09 constant collapse、F1/F3 retraction 等负面教训和原始数字。

#### 修正（建议，尚未授权实施）

1. 把“新增科学信息”设为每个工作包的第一验收项：候选排序改变、机制假设被区分、
   合法 comparator 被确认/否定、或明确 `no_durable_harvest_reason`。
2. semantic smoke 必须在 cells×seeds、receipt、独立 verifier 和完整 synthesis 前；
   失败即以一个 compact Probe record 收口。
3. verifier 分开写 execution integrity 与 scientific criticism；前者 PASS 不得自动
   触发 promotion。
4. activation 必须原子验收 Skill 可达、Project Adapter/current views、
   formal authorization 和实际用户 worktree。
5. 落实 D014：主控用持续 S 记裁决，GLM 每包只写 worker-log，T 是不可变任务书，
   H 仅用于主控换对话；普通 Probe 不生成 S/D/V/H 全套。

#### 删除/退役（从 active path 删除，不删除历史）

- B003 型“为验证新治理链而重跑同一科学合同”的默认路径。
- Task 8/9 “每案/每 replay batch 必须新增 harvest item”的旧硬门；改为必须 assessment，
  允许 `no_durable_harvest_reason`。
- 把 B1/B6 关键词匹配、合法动作存在或 replay 100% continuation 解释成战略质量证明。
- `STATUS.v1.md`、`project.v1.yaml`、`canonical-state.yaml` 作为 routine current
  owner 的角色；继续保留为 historical/protected。
- 每工作包机械生成 Queue/Registry/fingerprint/S/D/V/H 全套。

#### 尚未验证

- Skill 是否能在真实多轮中维持两个以上机制分支并主动截断无信息深挖。
- 首个真正轻量、合法、有科学信息增量的 Probe 端到端成本。
- Probe→Scout→Deep Evidence 在真实 artifact 上的晋级/降级。
- current view 在多 worktree、旧 handoff、并行执行和 disposition 冲突下能否
  五分钟恢复。
- 四层记忆/worker-log 协议经过完整主控—GLM 窗口后是否真能降低上下文和治理成本。
- harvest 是否能形成论文段落，而不是分类更完整的台账。

### 最小修补清单与唯一 owner

> 以下是 R002 建议，不是实施授权。优先复用 D013/D014，避免“发现问题→再造平行体系”。

| 优先级 | 最小修补 | 唯一 owner | 现在是否改 |
|---|---|---|---|
| P0 | 实际采用 T + worker-log + 长程 S + 极短四项回传；普通包禁 S/D/V/H 全套 | D014 + `session-governance` task-brief/本项目 `AGENTS.md` worker-log 路由 | **不改规则，先按现有合同实测** |
| P0 | formal authorization、Direction Lab scientific current、historical protected 三类角色显式分开；routine entry 不再读 stale `*.v1` | 项目 Adapter/current STATUS；formal stage 继续只由 `master-state.md` 拥有 | 下一次 Direction Lab 激活前修 |
| P1 | 将 Task 8 scorer 降级为 single-turn safety smoke；增加真实纵向测试 | `.agents/skills/research-direction-lab/tests/forward/` | 先冻结测试合同，R002 不改 |
| P1 | 移除“必须造 harvest item”旧门，统一为 assessment + 可记录无 durable harvest 原因 | `references/thesis-harvest.md` + 旧 scorer/fixture | 有失败测试证据后改 |
| P1 | 工作包验收记录 scientific action、governance action、新增事实和重复机制 | T### 验收字段 + `projects/{project}/worker-logs/` | 首次测试包直接采集，不建 scheduler |
| P2 | 若真实测试仍重复治理-only work，再在 core loop 增加“同合同/同机制/同有效域无新信息则不重复” | `references/core-loop.md` | **条件修补**，不预先加规则 |
| P2 | receipt/verifier/full closure 只按历史 mutation、provenance 和 claim risk 升级 | `references/evidence-and-claims.md` | 现有文本已大体覆盖，先测再改 |

### 下一轮真实长程测试场景

#### 目标

验证 D013/D014 的现有设计能否在真实科学反馈和跨对话恢复下，同时做到：

1. 每个 GLM 对话关闭一个科学不确定性；
2. 局部失败后换到更有信息的机制，而不是补治理；
3. 普通 Probe 只留下 compact record + worker-log；
4. 主控只凭四项回传和磁盘指针，在五分钟内恢复；
5. current view、formal authorization 和实际 worktree 始终一致。

#### 前置条件

- 本 R002 不激活该测试，不指定新科学候选，不改变 Pilot-Jones。
- 若使用 Pilot-Jones 作为真实载体，必须先按其 formal lane 解决 4 篇直接竞品全文
  获取/显式豁免，闭合 Step 3.5；Step 4a A0/A/B/D 未通过前不得实验。
- 若未来由另一个 Direction Lab candidate 承载，必须先有合法 conventional
  comparator、runnable interface 和明确 authorization；不得复活 frozen
  science-scout 旧 next action。

#### 纵向测试链（局部测试合同，不升级为全局固定批次数）

1. **Recover/Map 包**：从唯一 current view 恢复，保持至少两个机制不同的 ready
   备选，给出为何首选问题信息增益最高。
2. **Semantic Probe 包**：只检验一个最便宜的 prerequisite，先做 trivial/identity/
   output-support/causal-prefix/comparator smoke；FAIL 立即 compact 收口并轮转。
3. **Scout 包**：仅在 Probe PASS 后，对小批 mechanism-distinct 方案做共享公平比较；
   receipt/verifier 按风险条件触发，不按目录完整度触发。
4. **跨对话恢复包**：新主控只收到状态、commit、worker-log 路径和一句异常，验证
   五分钟内能否读盘恢复、纠正 stale 指针并给出下一合法动作。

#### 单个 GLM 工作包模板

```markdown
# T###: 单科学不确定性工作包

## 起点
- worktree / branch / starting HEAD:
- formal authorization owner:
- current scientific projection:
- 只读历史与 protected paths:

## 科学合同
- question:
- hypothesis:
- falsifier:
- minimum information needed:
- legal information boundary:
- conventional comparator:
- semantic smoke:
- local budget:
- stop/rotate condition:
- maximum claim ceiling:

## 允许产出
- 一个 artifact 目录（如需要）
- 一个 `projects/{project}/worker-logs/step-{N}-{slug}.md`
- 一个 commit

## 禁止
- 普通包不得新建 S/D/V/H、Queue、Registry 或平行 current view
- 不因格式完整而扩 cells/seeds/models
- integrity PASS 不得写成 scientific PASS

## 四项回传
1. status:
2. commit:
3. worker-log:
4. one-line anomaly:
```

#### 测试停止条件

- semantic smoke FAIL、平凡解成立、信息边界违法或 comparator 不充分：当前包立即停，
  不扩证据链。
- 一个修补后仍无法形成合法 runnable interface：标 local blocked，轮转；不在同包
  继续建设共享基础设施，除非它明确解锁多个高价值候选。
- 新结果没有改变候选排序、机制判断、baseline 充分性或 thesis harvest disposition：
  记 `no_new_scientific_information`，禁止同合同 governance-only repeat。
- current views/authorization/worktree 任两者不一致，或新主控不能在五分钟内恢复：
  纵向测试判 FAIL，先修 owner/release，不继续科学运行。
- 只有在 legal ready work、合理适配和有信息的范围扩展均有证据地耗尽时，才请求用户
  战略裁决；局部失败不升级为全局停止。

#### 测试成功判据

- 每个工作包关闭一个明确科学问题，且治理动作没有替代科学动作；
- 至少一次局部失败后，下一包转向不同机制或更便宜的决定性问题；
- 每包只有一个 worker-log，普通包没有 S/D/V/H 套件；
- 新主控仅凭四项回传，在五分钟内准确复述目标、dead ends、唯一下一步和 claim ceiling；
- campaign 结束时，至少有一项候选排序/机制判断/论文 disposition 被新证据改变；
  没有 durable harvest 时如实记录原因，不制造条目。

### 综合裁决

1. **应保留的是科学主干，不是旧治理重量。** anchor、开放候选地图、因果批次、
   claim ceiling、显式撤回和 rotate/deepen 均有价值。
2. **主要失效不是规则缺失，而是验证对象和运行顺序错位。** 单轮合规/replay/
   provenance 被用来替代多轮科学优先级；semantic smoke 又晚于完整证据链。
3. **D013/D014 已覆盖大部分正确修补。** 当前最小动作不是继续写 Skill/controller，
   而是先按三层强度和四层记忆完成一次真实纵向测试。
4. **状态 owner 在再次激活前必须收敛。** formal authorization 属
   `master-state.md`，Direction Lab scientific current 属非 protected current
   projection，旧 `*.v1/canonical` 只保留历史角色。
5. **当前科学状态不变。** science-scout 继续 dormant/SCIENCE_FREEZE；
   Pilot-Jones 继续 formal GW Step 3.5 PARTIAL，Step 4a 未授权。本 R002 不创建
   下一科学任务，不运行实验。

## 对决策的影响

本复盘不新建 D###，因为它没有授权修改方向、架构或接口；它为 D015 要求的后续拍板
提供证据。建议下一次决策只在两件事间选择：

1. 先做 P0 的 owner/current release 收敛，再运行纵向真实测试；或
2. 若现有 current 入口能在只读核验中满足测试前置，直接按 D013/D014 运行纵向测试，
   只有观察到具体失败后再修改对应 owner。

无论选择哪项，都不应先重写 Skill、恢复 frozen science-scout 或建立新 controller。
