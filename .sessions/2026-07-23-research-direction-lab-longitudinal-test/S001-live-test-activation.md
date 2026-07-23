# [S001] 长程真实运行测试激活

> 2026-07-23 | mission activation | 状态：READY_FOR_FORK，科学载体未选择
> 2026-07-23 续接 | H001 接收与 owner reconciliation | 状态：T001_READY
> 2026-07-23 续接 | T001 接收验收与下一门控判断 | 状态：AWAITING_USER_STRATEGY

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

## 决策引用

- system D017：采用轻量前台控制块与 T 授权 guard。

## 范围确认

- 本轮是否在 scope boundary 内：是。
- 本轮没有运行科学工作、改变 formal 状态或修改 protected history。

## 后续

等待用户选择 D061/H017 的全文获取路径。用户授权后，主控先递增 control epoch、绑定对应 action class，再生成下一份 T；授权前不运行全文工作、Step 4a、实验或 formal routing 变化。
