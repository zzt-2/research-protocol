# [S005] Step 4a 重开输入恢复

> 2026-08-09 | Groundwork Step 4a blocker-recovery Probe | VERIFIED_TERMINAL

## 目标

在 D012 的受限范围内关闭 H006 的两项唯一重开输入：source receiver/channel executable configuration 与 action-before protocol。只有两项都闭合并经 fresh-context verifier 接收，才允许重冻结 D009 semantic-smoke 合同；否则保持 D011 terminal 5 并停止。

## 记录

### 恢复与 H006 接收

- 当前 HEAD=`4fd6d348b9eda09ecaa022d274cc2eddd5d5f763`，branch=`codex/rdl-method-production-v2`；tracked/staged diff 为空，仅四个既有未跟踪 `p05_run*.log`。
- 接收声称 1 独立复核：`contract.json` fresh parse 得 `status=REJECTED_PRE_RUN`、`terminal_authority=NONE`；D010 没有 terminal authority。
- 接收声称 2 独立复核：terminal receipt fresh parse 得 grid=`NOT_RUN`、MVE=`NOT_RUN`、scientific raw rows=`0`，B0/B1/B2/O1/C1 均为 `N/A (NOT_RUN)`；Step 4a 隔离目录只有 rejected contract 与 terminal receipt 两个文件。
- 接收声称 3 独立复核：receipt 的 blocker id 为 `STRUCTURAL_ACTION_BEFORE_CAUSALITY`、`SOURCE_CHANNEL_NON_EQUIVALENCE`、`DBM_TO_DISCRETE_NOISE_NON_IDENTIFIABLE`，并逐字列出 source config、action-before protocol 与 scope change 三项重开输入。
- 四个 protected log 的 bytes/SHA-256/mtime 与 V007 完全一致：`641/7843b048...a4f11`、`2417/735e4650...ac38b`、`929/c76887c...b1344d`、`1430/95a1d184...a621de`；均保持 untracked/unstaged。
- registry 依赖仍为稳定 dormant source owner `2026-08-08-ch4-reference-method-extension`，`conflicts_with=[]`；本专题此前 S001–S004 共 4 个 S 文件。S004 是已验证 terminal，本轮内容性质转为 blocker recovery，故新建 S005 而非改写 terminal note。
- profile 无需更新；用户“你做吧”与既有“技术判断委托主线、无需逐项停问”的 durable 模式一致，但本次原话作为 D012 scope-change authority 单独写入本专题 `voice.md`。

### RDL 恢复路由检查

1. 下一动作不直接创建、比较、晋级或写作方法；它只恢复可执行科学比较所需的 source/config 与 causal protocol。
2. 该动作不可跳过：缺 SC1 时 receiver-power/turbulence 数字不可解释，缺 AB1 时 B2 只能是 action-after/oracle-like lookup，二者都会在任何 scientific row 前使 Step 4a 无效。
3. 这是 H006 后第一次精确 blocker-recovery，且用户已显式授权；它比轮换到无关 READY 方向更直接服务当前 Q1。上游 epoch 37 / CP024 的 `NEW_TOPIC_RECOVERY` 允许该动作，旧 system 专题继续只读，不新增其 S/D/V。

### 冻结 Probe 设计

- source-config 路径：优先作者/出版方 supplement、作者公开代码/数据、同一实验链的一手可执行配置；以 D012 SC1 字段表逐项闭合。只恢复图轴或找到相似 receiver 不能 PASS。
- action-before 路径：并排审计 previous-frame 与 action-independent common-probe；按因果性、观测不变性、latency/coherence、overhead、state lifecycle、fallback 与 caller→callee 可审计性选择唯一最小 primary protocol。
- 两路独立并行；executor 只能写指定 T/worker-log/artifact，不改 owner。主控接收后执行 `REOPEN_INPUTS_READY` / `REOPEN_INPUTS_NOT_CLOSED` reducer，再派 fresh-context verifier。

### 假设与否决条件

- H5：公开/一手材料能闭合 Wang-equivalent phase-screen/SMF 与 dBm→discrete-noise source config。否决条件：止损搜索后仍缺任一 SC1 必需字段，或只能用相似系统/典型值/结果拟合补齐。
- H6：能定义不依赖当前 action-specific FSTS 的 receiver-visible action-before protocol。否决条件：观测仍 action-after/action-dependent，或 coherence/feedback/overhead/state/fallback 不能形成可证伪完整合同。
- H7：两项闭合后可重冻结 B0/B1/B2/O1 公平比较。否决条件：source config 与 protocol 的 reference plane、state lifecycle 或 action key 不能在同一 caller→callee 数据流中对齐。

### 迭代计数器

- H006 receive verification：`1/1 PASS`
- source-config recovery：`1/1`（T020=`SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`；SC1 fields exact-closed=`0/7`）
- action-before protocol closure：`1/1`（T021 evidence=`AB1_NOT_CLOSED`；两方案均无 executable caller path）
- performance grid：`0`（禁止）
- diagnostic structural run：`0`（禁止）
- bounded MVE：`0`（禁止）
- independent reopen-input verification：`1/1 PASS`（V008；P0/P1/P2=`0/0/0`）

### Probe 结果与独立验证

- T020 三类公开 surface 均已止损；未发现 exact supplement/code/data/source backend。论文 identity 被纠正为 IEEE document `10097873`（`10101698` 是 issue/media id），但 SC1 必需 1–7 字段 `EXACT_CLOSED=0/7`。
- T021 fresh child 完成 Wang 455 行全文读，确认 source 无 action-before protocol。parent executor 超过止损后中断，主控用 delegated read + Valjus/WiSEE/JLT primary line checks合成 worker log；该 provenance 已写入日志并必须由 T022 fresh verifier独立审查。
- previous-frame 与 common-probe 都只有 causal skeleton：前者缺 measurement invariance/frame trajectory/feedback，后者缺 probe contract且同样缺 feedback/freshness/cost。JLT 2023 给出直接反馈时延边界，反驳“generic `>1 ms` 自动够用”。
- D012 reducer 因 SC1、AB1 均未 PASS，唯一 recovery terminal=`REOPEN_INPUTS_NOT_CLOSED`；D011 scientific terminal保持不变。没有评价 crossover、B2 absorption或 residual，所有 performance 数字继续 NOT_RUN。
- T022 fresh-context verifier 独立重放 SC1 exact identity/字段矩阵、AB1 Wang/Valjus/WiSEE/JLT 因果边界、D012 reducer、owner/receipt/hash/protected scope；V008=`PASS, P0/P1/P2=0/0/0`。verifier log SHA-256=`50bf4d208d9018874190e8b289616db57531a5802f47ea71112ec3203b9c3038`。该 PASS 只接收 recovery terminal，不是 performance/scientific correctness PASS。

## 决策引用

- D011：既有 Step 4a terminal 5；两项重开输入的来源。
- D012：受限重开 source-config/action-before 输入恢复（新建）。
- D013：重开输入未闭合、保持 terminal 5（新建；V008 已接收）。

## 范围确认

- 本轮是否在 scope boundary 内：是（用户“你做吧”显式授权；见 D012 与 topic-index scope-change record）。

## 后续

V008 已接收 D013；同步 verified/dormant owners与 H007 后一次统一 commit。下一科学动作只在作者/source backend与 executable feedback/time-series testbed同时新增后再做 scope change；当前不联系作者、不运行 performance repair。
