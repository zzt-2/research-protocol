# [S014] R002 后首次真实恢复跑偏与设计阶段冻结

> 2026-07-23 | 长程运行协议设计前审计 | 状态：现场故障已记录，v0.1 详细设计见 R003
> 2026-07-23 续接：自动压缩后按 control block 恢复，进入终验

## 目标

1. 记录 R002 完成后主控在上下文压缩恢复中的真实跑偏。
2. 区分已冻结的长期协作原则与尚未设计完成的运行机制。
3. 冻结工作方式：先在当前对话仔细设计和演练，再 fork 做真实运行；此前不派具体科学方向。

## 记录

### 1. 现场故障

R002 完成后，主控在压缩摘要中继承了“Pilot-Jones 是当前 formal candidate”这一真实事实，并将其错误推导成“下一步应推进 Pilot-Jones”，直接提出 Step 3.5 带债豁免和 Step 4a Probe。

这与磁盘权威状态冲突：

- system `topic-index.md` 要求先处理长期运行协议与 owner/current 问题；
- R002 明确“不指定新科学候选、不改变 Pilot-Jones”；
- D015 的入口是历史复盘及后续最小修补判断，不是科学派工。

用户指出后，主控重新读取 S013、D013–D015、R002 和 topic-index，撤回建议。没有实验、Skill 修改或科学状态变更。

### 2. 故障机制

故障链为：

`context compression → formal candidate 被误当作 current next action → 跳过 system-design gate`

这不是日志不存在，而是多个局部正确 owner 之间缺少对当前主控有约束力的“前台 lane”。摘要中的真实事实覆盖了持久文件中的未决设计门。

### 3. 已定与未定

已定：

- D013：Probe/Scout/Deep Evidence、语义先行、current projection；
- D014：当前快照、长程 S、worker-log、raw artifacts 四层记忆；
- T 是任务书，H 只用于主控续接，普通包不生成 S/D/V/H 全套；
- 用户只中转极短索引，主控承担状态、科学和战略判断。

未定：

- 主控怎样选最高科学信息增量的下一工作；
- FAIL/BLOCKED/SATURATED 后怎样修补、轮换、扩图或停止；
- 候选变化、formal 晋级与新 topic 的边界；
- 压缩/fork 后怎样让磁盘 gate 约束任务生成；
- 一个 GLM 对话应关闭多大的科学不确定性；
- 哪些缺口改 RDL Skill，哪些属于 session-governance、current owner 或 T/worker-log；
- 怎样以真实长跑而非单轮 fixture 验收。

### 4. 当前设计工作

本对话只做分析、候选架构比较和历史场景演练。详细结果下沉到：

- `R003-lightweight-long-horizon-protocol-design.md`

R003 两轮演练当前领先方案是：

- RDL mission 的 `topic-index.md` 顶部维护一个很小的前台控制块；
- system design 与 longitudinal live test 分属两个 mission topic；
- H 绑定主控/fork，T 绑定单个科学决策包，worker-log 保存完整执行；
- candidate 轮换留在同一 exploration topic，正式晋级才新建/恢复 formal topic；
- 不采用 checklist-only、per-fork manifest 或强 controller；
- S014 已构成真实越 gate 证据，因此 v1 建议配一个只校验 control ref/epoch/action class 的极小 T guard；
- 设计 worktree 冻结为审查基线，另建一个 live-test worktree；fork 主控和 executor 在其中串行工作，不为每包建 worktree。

该方案仍是草案，尚未授权实施。

### 5. 记录分层纠偏

初次分析一度把 S014 写到 349 行，已经违背“长程 S 只记裁决和轨迹”。当场纠正：

- S014 只保留故障、主线、已定/未定和 R003 指针；
- R003 保存能力分析、候选架构、两轮场景演练、v0.1 与风险；
- 不再把详细设计继续堆进长程控制日志。

### 6. 首次真实恢复事件

在 D017 实现和 live-test 入口写入后，本对话发生自动上下文压缩。主控没有直接按摘要续做，而是重新读取 system control block、D017、live-test control block 和 registry，恢复出：

- system role=`SYSTEM_DESIGN`、epoch=`2`、lane=`PROTOCOL_IMPLEMENTATION`；
- 当前只允许协议实现、验证和 live-test 准备；
- live-test epoch=`1` 只允许 Recover/Map/Reconcile/T 准备，明确禁止科学实验。

随后继续的动作仅为 Skill 审查和终验，没有跨入科学派工。这是一个真实正向恢复样本，但只有 `1/1`，不能据此宣称长程机制已经 PASS。

## 决策引用

- D013：三层工作强度、语义先行与单一当前投影。
- D014：四层记忆与极短中转。
- D015：R002 前暂停科学派工，先做历史复盘。
- D016：先在当前对话完成轻量运行协议设计，再 fork 真实运行（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。
- 明确未触碰：Skill/controller、科学实验、Pilot-Jones 正式状态、science-scout、protected history。
- 膨胀检查：本专题共有 14 个 S 文件，超过警戒线但未达到阻断线；后续设计继续写 R003，不再新建 S。

## 后续

向用户汇报 R003 v0.1 的核心设计与仍未确认风险。用户认可设计方向后，再逐项确认 owner、T guard、worktree 和 promotion 接口；全部确认前不实施、不生成科学提示词。
