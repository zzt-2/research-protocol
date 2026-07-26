# [S001] 长程真实运行测试激活

> 2026-07-23 | mission activation | 状态：READY_FOR_FORK，科学载体未选择
> 2026-07-23 续接 | H001 接收与 owner reconciliation | 状态：T001_READY
> 2026-07-23 续接 | T001 接收验收与下一门控判断 | 状态：AWAITING_USER_STRATEGY
> 2026-07-23 续接 | D062 带债豁免与大包粒度纠偏 | 状态：T002_READY

## 目标

建立 D017 的独立 live-test mission，使 fork 主控能在不继承 system design 写入职责的情况下，按轻量控制协议恢复、选包、派工和轮换。

## 记录

- 上游设计：system S014 记录压缩跑偏，R003 完成两轮场景演练，D017 采用小控制块和极小 T guard。
- 本 topic 只验证长程运行；它不拥有候选证据或 formal stage。
- 初始 role=`LIVE_TEST`、lane=`RECOVER_MAP`。
- 初始允许 Recover、Portfolio Map、State Reconciliation 和 T 准备。
- 初始禁止科学实验、formal stage 变化、Skill 修改和基础设施建设。
- fork 主控首先读取本 topic-index、H001 和 authority owners；不得根据继承摘要直接选择 Pilot-Jones 或其他方向。
- 设计 worktree 在最终提交后冻结；另建一个 live-test worktree，fork master 与 executor 串行写入。
- 普通工作包不新增 S/D/V/H；完整细节进入项目 worker-log 和 artifacts。
- 入口终验：仓库 RDL tests `97 passed, 1 skipped`；个人 Skill 59 个非缓存文件与 repo 镜像逐字节一致；个人 guard tests 6/6 PASS；live control smoke PASS。
- 个人 Skill 全量测试若脱离仓库根目录运行，会有 3 个项目 fixture/audit 路径失败；完整集成门已在仓库内通过，这不是 Skill 镜像差异。

### H001 接收验证

- 声称 1 PASS：live control `role=LIVE_TEST`、`epoch=1`，证据为本 topic-index 顶部控制块。
- 声称 2 PASS：初始 forbidden actions 同时包含 `SCIENTIFIC_EXPERIMENT` 与 `FORMAL_STAGE_CHANGE`。
- 声称 3 PASS：system D017 明确拒绝“设计完成即授权某个科学方向”，且不改变 science-scout/Pilot-Jones 科学状态。
- registry PASS：本 topic `depends_on=2026-07-20-research-direction-lab-system`、`conflicts_with=[]`。
- 接口 PASS：个人/仓库 guard 的定向测试 6/6 PASS。

### owner 恢复

- **system owner**：D017 只拥有长程运行接口，不提供 scientific carrier。
- **formal owner**：dual-pol-osl-groundwork D061；P03 已选选项①暂停回候选池，Pilot-Jones 是当前 formal GW 线，Step 3.5 PARTIAL/BLOCKED。
- **formal evidence**：V035 已闭合 JLT2022 backward chain；4 篇直接竞品全文仍 `BLOCKED_NO_FULLTEXT`；Step 4a 未授权。
- **Scout owner**：Direction Lab D022/current state；campaign dormant、`science_authorized=false`，不得恢复 Scout。
- **current-view 冲突**：`projects-overview.md`、Direction Lab README、`state/current.yaml`、`portfolio/current.yaml`、`harvest/current.yaml` 的 current routing/recovery/next-action 字段仍部分保留 D061 前状态，含“P03 用户决策未选”和已被纠正的 “LCOMM 2026 abstract-only”。

### 第一包选择

| 选项 | 合法性 | 信息/杠杆 | 裁决 |
|---|---|---|---|
| A. 对齐 D061/H017 到可变 current views | `STATE_RECONCILIATION`，READY | 消除真实 owner 冲突，防下一次压缩重新误路由；成本低、可逆 | **选择为 T001** |
| B. 仅整理 4 篇全文获取路径决策包 | `TASK_BRIEF_PREPARATION`，READY | 不产生新证据，最终仍需用户提供机构访问、邮件授权或显式豁免；且不消除 current 冲突 | 延后 |
| C. 恢复 P03/Scout 或直接进 Step 4a | 非法 | 违反 D061/D022/FR-22 | 排除 |

T001 只修可变 current views 和写 worker-log，不修改 protected history、formal state、科学结论或 Skill；完成后主控再判断第二包。

### T001 接收验收

- 执行提交：`4a0d4a48ad3a817a2a1dc92ad4641b0fb9d47727`；worker-log：`projects/thesis-fso/worker-logs/step-001-current-owner-reconciliation.md`。
- 路径边界 PASS：相对 T001 基线只修改 5 个指定 current views，并新增 1 个指定 worker-log；protected/formal/Skill/live-control 文件均无差异。
- 语法与语义 PASS：3 个 YAML 可解析；5 个 current views 均指向 D061/H017，写明 P03 `PAUSED_RETURNED_TO_PORTFOLIO`、Pilot-Jones Step 3.5 `PARTIAL/BLOCKED`、V035 PASS、OE 2021 + LCOMM 2026 已全文精读、4 篇真实缺失全文及 Step 4a 未授权。
- stale 检查 PASS：不再残留“P03 用户决策未选”“missing independent terminal verification”或“LCOMM 2026 abstract-only”。
- 执行方未能使用独立 verifier，已在 worker-log 如实标记 `INDEPENDENT_VERIFIER_UNAVAILABLE`；主控用提交 diff、受保护路径 diff、YAML 解析和字段断言完成独立接收验收。

### 第二包判断

current owner 收敛后，唯一未闭合门是 D056 的 4 篇直接竞品全文。D061/H017 已证明公开获取路径耗尽，并明确把以下动作交给用户裁决：机构访问、联系作者、带债豁免或等待/替换。

在当前 epoch 内：

- 重做 OA 搜索或再整理同一决策表不会增加科学信息；
- 用摘要代替全文或直接进入 Step 4a 违反 D056/FR-22；
- 恢复 P03/Scout 会改变 D061 的 formal routing；
- 发邮件、使用私有机构权限或豁免门控都需要新授权。

因此没有合法且非重复的 T002。live test 进入真实的 `AWAITING_USER_STRATEGY`，不以文书型假任务维持表面连续派工。主控建议选择“带债豁免”：以现有 2 篇全文、V035 backward 证据和 4 篇摘要级证据进入 Step 4a，同时将 4 篇未精读保留为阻断性债务；该选择仍须用户显式授权。

### 用户授权与包粒度纠偏

用户指出 T001 “干得太少”。事实核对：T001 只协调 5 个 current views，没有关闭科学问题、形成方法或运行验证，因此只计一次性 bootstrap overhead，不计普通研究包。

用户随后同意“按大包带债推进”。主控据此：

- 在 formal owner 建立 D062，选择 H017 选项 (c)；
- 4 篇全文仍为 `BLOCKED_NO_FULLTEXT`，Step 3.5 不改写为 PASS；
- 授权 T002 单对话关闭“Pilot-Jones 是否值得继续”这一科学不确定性；
- T002 可包含 A0/A′/A/B、方法族比较、bounded source recovery、前置上界、条件式 MVE、双审查和 provisional verdict；
- 只有真实致命门、无法闭合的基础资产或预算终点才能提前停止，不得停在纯方法列表或 MVE 计划；
- 正面最高 Conditional Go，主控验收后仍须用户确认，不进入 Step 5。

## 决策引用

- system D017：采用轻量前台控制块与 T 授权 guard。
- formal D062：D056 一次性带债豁免，授权 Pilot-Jones Step 4a 大包。

## 范围确认

- 本轮是否在 scope boundary 内：是。
- 本轮没有运行科学实验或修改 protected history；根据用户授权在 formal owner 新建 D062，将 formal stage 内的合法步骤从 Step 3.5 带债阻断更新为 Step 4a 已授权进行中。该变化是显式 gate 决策，不是执行方自行推进。

## 后续

T002 自包含任务书、control guard 和范围验证已完成；下一步交给用户转发 GLM 执行。

> 2026-07-23 续接 | T002 主控验收与 T003 授权 | 状态：T003_READY

### T002 主控接收验收

- 执行提交 `0b642e9317d4494c481ecf4f1e8ceb07c866c04c`，新增/修改 18 个授权文件；protected diff 为空，worktree clean。
- fresh pytest `10 passed`；raw 重算 B1=`0.0053083`、P=`0.0053355`、oracle=`0.0044654`，P 胜 B1=`0/10`、tie=`6/10`、B1 胜 P=`4/10`。
- 核心结构事实成立：canonical generator 只有 `sqrt(h) × real unitary rotation`，真实 Jones 条件数恒为 1，因此当前“ill-conditioned Jones stabilization”M-C-A 不成立。
- V036 有两项漏审：contract 仍写 7 tie/3 loss；`BER≤2×oracle` 未证明等价 `<0.5dB`。故按 V037 只接收 `UNITARY_REAL_ROTATION_MCA_KILLED`，不接收 family Kill。
- 本轮大包有真实科学产出：发现模型—问题错配、形成可复用 runner/baseline/tests/局部负面材料；不按失败包或纯治理包计。

### T003 设计选择

比较三条后选择信息价值最高的 bounded salvage：

1. **选择**：complex Jones/PMD/PDL 模型充分性 + 方法救活大包。先证实物理必要性，再做隔离模型、task-matched conventional baseline、oracle/headroom；门通过时同包跑方法比较。
2. 排除：接受局部 Kill 后立即轮换其他 formal 候选——会留下 V036 指出的唯一物理救活轴未检验。
3. 排除：在 unitary real-rotation 上补跑完整 MVE——结构轴缺失，额外 cells 不增加机制信息。

用户回复“随便，多做点”，授权采用方案 1。formal D063 已记录：不建设通用框架、不改 shared canonical generator、不进 Step 5；一个包直接关闭“更真实复数 Jones 是否救活方法空间”。

## 决策引用

- formal D063：接收 unitary-real-rotation 局部 Kill，授权 complex-Jones salvage 大包（新建）。
- V037：T002 主控接收验收，结论 PARTIAL（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是；这是 live-test 对真实局部失败的自动轮换与同一 formal family 的 scope-expansion Probe/Scout。
- 未运行新科学实验，未进入 Step 5，未修改 protected history、Skill/controller 或 dormant Scout/P03。

## 后续

T003 自包含任务书、epoch 5 control guard 和 current-owner 同步已完成；交用户转发 GLM。

> 2026-07-23 续接 | T003 主控验收与 T004 授权 | 状态：T004_READY

### T003 主控接收验收

- 执行提交 `5445a2e8899928b8f69d9df811212e913155f8f9`；fresh directed tests
  `13 passed`，protected diff 为空，raw/result 可解析。
- V038 没有继承执行者的 PASS：新增 PDL/PMD 作用在已经含 AWGN 的 canonical RX，
  使 inverse 同时还原 signal/noise；PDL flat headroom 是代码恒等而非物理发现。
- PMD pilot 用 memoryless `J @ pilot` 重合成，未经过 PMD FIR；B3 tapped 以 RX
  window 预测 RX center，不是 RX→known-TX equalizer。
- PMD oracle 被部署型 B1 反超：6 ps/40 ps 两格 B1 BER 分别比 oracle 低
  35.7%/33.4%；160 ps 中 B1 比 B3 低 43.0%。因此 oracle ceiling 与 strongest B3
  两个基础前提均失败。
- decision code 又把 `problem_survives` 与 `P1 beats B3` 取 AND。当前 P1 失败不能
  推出物理模型没有问题。T003 的 `PIVOT_MODEL_NOT_JUSTIFIED` 被 D064 正式否决，
  complex/PMD/PDL 继续 `UNRESOLVED`。
- `git diff --check` 仍报 `_registry.yaml` trailing whitespace，与 worker-log PASS
  不一致；作为执行验收缺陷记录，不把它夸大成科学根因。

### T004 包选择

1. **选择**：一个 semantic repair + paired retest 大包。先用可失败的行为测试锁定
   signal/noise 顺序、pre-channel pilot、RX→TX tapped baseline 和真正 PMD/M4
   oracle；全过后统一重跑 M0–M4。
2. 若合法传统 baseline 到 oracle 的问题 gap 在 verified range 存活，同包扫描
   A1–A6 并比较 2–3 个机制候选；若问题不存活，才形成 scoped negative。
3. 排除只补 oracle 或立即换方向：前者留下另外三项结构缺陷，后者会把 T003
   invalid verdict 留成压缩后可继承的假状态。

本事件是 live test 的真实价值点：worker 一次完成 19k 行资产、tests/SHA/provenance
均绿，仍因 semantic smoke 设计不充分产生错误科学结论；foreground master 成功在
接收门阻断，没有把“包很大/流程很全”误当可晋级证据。

## 决策引用

- formal D064：T003 科学结论不接收，授权 T004 semantic repair + retest（新建）。
- V038：T003 主控科学语义验收 FAIL / 工程 PARTIAL（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是；仍在 Pilot-Jones formal GW Step 4a 内修复
  证据语义，不进 Step 5，不修改 protected history/Skill/controller，不恢复 Scout。

## 后续

T004 自包含任务书与 epoch 6 control guard 完成后交用户转发 GLM。用户把当前阶段
明确视为真实运行测试，运行一段后回原 system design 对话做磁盘证据审计。

> 2026-07-24 续接 | T004 主控验收与 T005 授权 | 状态：T005_READY

### T004 主控接收验收

- 执行提交 `9a250e1589bdd583ad2df2ca788eaa43c71aadfd`，fresh tests
  `25 passed`；T003 五项中 signal/noise、passive PDL、pre-channel pilot、
  RX→TX target、gate separation 的工程修复成立。
- V039 发现第六项上游语义：M2/M4 每 64 symbols iid 重抽 component Jones
  U/V，而 T003/T004 自己把 PDL/PMD 定位为器件/光纤损伤；canonical R(theta)
  已负责 SOP 动态。该 25.6 ns 跳变无物理来源。
- 固定器件反事实使 1 dB PDL 的 impairment-added headroom 从原报告
  0.69–0.91 dB 降到 validation/test 的 0.0146/0.00445 dB，正面 problem gate
  被推翻。
- 另发现 same-seed 跨 Python process 不同（内建 hash seed）、contract
  N=50000/runner 20000、10-seed/8-seed 和假 contract SHA。故 T004 只按
  `PARTIAL_REUSABLE_SEMANTIC_REPAIR` 接收，科学 provisional verdict FAIL。
- 这是 live test 的第二次真实接收阻断：大包和 25 tests 没能替代“新增随机过程
  的时间尺度是否物理正确”检查；前台 master 没把 PARTIAL 当作继续找方法的理由。

### T005 包选择

1. 只做 fixed/有来源慢变 component 的 temporal-semantics 终审、deterministic
   seed/SHA 闭包与正式 paired headroom；不再增加方法候选。
2. 同包覆盖 operational 与 adversarial 两个已注册条件、4/6 pilots、M0/M2/M3
   和 10+10 fresh seeds。primary fixed component 若关闭 <0.5 dB 余量，就关闭
   complex component rescue axis。
3. 排除修补 T004 原目录和继续试 P4/P5：旧 T004 必须保留为失败证据；其正面门
   已被时间模型伪影解释。

## 决策引用

- formal D065：T004 正面门失效，授权 T005 temporal adjudication（新建）。
- V039：T004 主控接收 FAIL scientific / PARTIAL engineering（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是；仍为 Pilot-Jones formal GW Step 4a 的模型
  充分性终审，不进 Step 5，不修改 protected history/Skill/controller，不恢复 Scout。

## 后续

T005 自包含任务书与 epoch 7 control guard完成后交用户转发 GLM。

> 2026-07-25 续接 | T005 主控验收与 T006 方法载体切换 | 状态：T006_READY

### T005 主控接收验收

- 执行 commit `8f7dd0d323c8c35c47842ed34e6f68e9d4e9d4b3` 边界正确；legacy
  T003/T004 `38 passed`，T005 在 `PYTHONUTF8=1` 下 `17 passed`。
- raw 240 行独立重算 bit-identical，8/8 primary cells point 与 CI upper 均低于
  0.5 dB；最大 point=`0.0804126817 dB`、最大 upper=`0.2371961896 dB`。
- 没有照单全收执行者的 PARTIAL：发现 M3 contract 冻结 exact recovery `1e-10`，
  实现却用 MMSE regularized reference 且 tests 接受 `<1e-4`；Windows 默认 GBK
  另有 3 个 encoding failures。
- 真 unitary exact inverse 重算 40 个 M3 test realizations 与 stored BER 40/40
  一致，无噪误差 `1.13e-15`。因此 scientific scoped Kill PASS，integrity PARTIAL。
- formal D066/V040 关闭 `COMPLEX_COMPONENT_RESCUE_AXIS_TEMPORAL_PRIMARY`，但不杀
  整个 family、不抹去 4 篇全文债。Pilot-Jones 退出当前 carrier。

### 下一 carrier 比较与选择

比较三条可用路径：

1. **选择** B10/B12 高阶调制 CPR 组合方法：已有 Step 1–3 全文/精读、16/256-QAM
   方法链和 CPR 仿真资产；headroom 存活时可在同包形成 cascade、confidence gate、
   adaptive forgetting 三个务实方法。
2. residual/CMA correction 暂不选：此前 receiver-visible information increment
   仍不足，容易回到同信息源补丁。
3. P03 暂不选：当前价值主要在 infrastructure/domain closure，离方法形成更远。

用户同意方案 1。carrier owner D012 已明确：先做合法 problem/headroom，`<0.5 dB`
立即 Kill；门通过则同一个 GLM 对话完成方法、paired test、raw/CI 和裁决。

## 决策引用

- formal dual-pol D066：接收 T005 scoped Kill，Pilot-Jones 退出 carrier（新建）。
- formal carrier-sync D012：授权 B10/B12 高阶 CPR 组合方法 T006（新建）。
- V040：T005 scientific PASS / integrity PARTIAL（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。live-test mission 本就授权在局部失败后合法
  换 carrier；新动作引用已有 formal Step 1–3 owner，且仍止于 GW Step 4a。

## 后续

T006 自包含任务书与 epoch 8 control guard 完成后交用户转发 GLM。用户仍只需返回
四行索引，不需要读取实验细节。

> 2026-07-25 续接 | T006 主控验收与 T007 载体切换 | 状态：T007_READY

### T006 主控接收验收

- 执行 commit `21bfbda353e1779a26d498b43f6353fe458f494f` 边界与落盘范围正确；
  `PYTHONUTF8=1` 下 T006 `32 passed`、Pilot-Jones regression `65 passed`。
- Windows 默认 locale 实际为 `30 passed, 2 failed`，与 worker-log 的双 locale
  PASS 声称不符；T006 任务文件还缺 `RDL-TASK-CONTROL` marker，epoch 8 guard
  没有真实闭包。
- B10 源语义不成立：论文连续 128 pilots 训练后才切 DD，代码见第一个 sparse
  pilot 就启用 DD 并过早冻结 F。纯 CFO+20 dB AWGN probe 即使连续 128 pilots
  仍有 0.158–0.404 BER，故 9–20 dB 退化不能归因为真实机制。
- B12 的 joint ML/MAP 关键公式 image-only，代码自行采用
  `angle(Sigma_phi @ z_unit)`；不能用它 Kill 发表方法。
- pilot 与 data 经过不同通道，seed 7700/7708 的 pilot-channel relative RMSE
  分别约 0.171/0.646；oracle 另把 SOP mixing angle 当 scalar phase。
- 唯一 headroom survivor 的 mean 0.6059 dB 被单个 collapse seed 主导 91.7%；
  median 0.0447 dB，drop-max mean 0.0560 dB。V001 因此拒收科学 verdict，
  T006 只作 PARTIAL 工程资产，B10/B12 family 保持 UNRESOLVED。

### 下一 carrier 比较与选择

1. **选择 B1 adaptive phase window**：已有 Step 1–3 与 sat.1553 明示 open
   problem；复用 VV/pilot CPE，只增条件估计、有限窗集合与 hysteresis，一个
   对话可完成结构门、三方法与正式 paired test。
2. 不修 T006：方法身份、物理通道和统计门同时失效，修复不是局部事件。
3. 不立即做 B9 DRE：需另建 oversampled waveform/DAC/MF/Viterbi 链，当前更容易
   重演“关键链路没实现却先跑结果”。

## 决策引用

- formal D013：拒收 T006 科学裁决，激活 B1 自适应相位窗（新建）。
- formal V001：T006 scientific FAIL / engineering PARTIAL（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。B1 已在 formal Step 1–3 候选池且由既有
  不变量明确保留；切换后仍止于 GW Step 4a。

## 后续

T007 必须带真实 epoch 9 task-control marker 并过 guard。先验证“最优窗随条件变化
且无普适固定窗”；门失败立即 Kill，门成功同包完成三方法和 paired test。

> 2026-07-26 续接 | Goal campaign remap 与 A4 carrier 激活 | 状态：T009_READY

## 目标

严格接收 H002 后，回顾 CP001–CP008，比较至少三条具有 formal 证据链的 carrier，
选择比两个替代项更可能产生 `METHOD_SIGNAL` 的下一包；本轮不运行科学实验。

## 记录

- H002 接收方验证逐项完成：
  1. **PASS — 接收时控制权威**：live `verifications.md#V003` 与
     `topic-index.md` 的接收快照共同确认 epoch 13 / CP008 / D002 是 H002
     接收时权威；本轮通过 D003/D015 才合法升级为 epoch 14。
  2. **PASS — T008 身份**：formal
     `.sessions/2026-07-06-step4a-mve-execution/verifications.md#V002` 与
     `decisions.md#D014` 均将 T008 记为
     `BLOCKED_IDENTITY / SCIENCE_VERDICT_REJECTED`，不是 Kill，也没有方法增量。
  3. **PASS — 接收时无 active carrier**：live `verifications.md#V003`、
     formal `decisions.md#D014` 与 `projects/thesis-fso/master-state.md` 的接收
     快照一致确认 no-active-carrier；D015 是接收验证通过后新建的 carrier 激活。
  4. **PASS — 依赖与冲突**：`.sessions/_registry.yaml` 显示本专题仅依赖
     research-direction-lab-system，`conflicts_with: []`；依赖专题处于 active，
     无冲突专题。
  5. **PASS — scope**：本轮仅做 campaign remap、formal/control/task 落盘和
     独立审查，仍止于 thesis-fso GW Step 4a；没有运行实验、修 T008/B1 或派 T009。
- 按用户要求调用 `create_goal` 时，工具返回本 task 已有 unfinished Goal；
  `get_goal` 确认 `/goal` 入口已自动建立 active Goal，objective 包含本轮完整长期
  使命与八条运行约束，因此复用现有 Goal，不把单包完成标为 Goal 完成。
- 比较 A4、B10/B12、B1，六维明细见 R001。A4 排第一，不是因为旧论文已经证明
  方法，而是它已有方法动作、可运行分支和写作结构，剩余债可压成一次可失败
  identity adjudication；B10/B12 要先重建 source-native estimator，B1 则会成为
  第三个同轴 evaluator repair。
- B2/B3/B7 已有专题级 Kill；C15 缺新候选 Step 1–3；B9 缺 executable chain 与
  formal activation；Pilot-Jones/P03/Scout 当前无正向 method contract。
- formal D015 激活 A4，live D003 将 control 升至 epoch 14。T009 只有在统一
  waveform/common payload、deployable information 与 strongest-fixed comparator
  身份通过后，才运行 P1–P3。
- 独立 verifier 经两轮 FAIL 驱动修正：先把 S011 DPLL 纳入 B*/B-cond，再把
  16-APSK hard decision、跨 block 连续 VCO、validation-only tuning 与 AWGN
  working-region smoke 写成硬门；V004 终验 PASS，P0/P1/P2 均为 0。
- 本轮没有运行仿真、修改实验参数或预支科学结论。

## 决策引用

- D003：campaign remap 激活 A4 deployable adaptive CPR（新建）
- formal D015：A4 GW Step 4a 方法生产包授权（新建）
- V004：campaign remap、formal 激活与 T009 独立终验 PASS（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

用户只需把 T009 路径转发给 GLM。主控接收执行包后独立验收科学身份，更新 CP009
的 method delta、same-axis/repair/no-method streak 与 drift；无论正负都继续 Goal。
