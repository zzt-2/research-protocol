# [S001] Step 1 启动与旧方向 reopen gate

> 2026-08-07 | Groundwork Step 1 | STOPPED — `STEP1_EVIDENCE_INSUFFICIENT`

## 目标

在不运行仿真、不进入 Step 2 的前提下，完成 registry 查重、历史碰撞审计、最多 6 组定向检索、物理来源分级、候选预卡、outage-vs-burst 语义门和只读 testbed BOM；只有全部承重条件成立才进入 Step 2。

## 记录

### 启动事实

- evidence worktree：`D:\code\study\research-protocol\.worktrees\rdl-method-production-v2`
- 启动 HEAD：`12c54b3409dcc46c3bf4bf202380a38eae069562`
- worktree 含四个用户未跟踪 `p05_run*.log`；本专题禁止接触。
- registry 查重：未发现 `strong-turbulence/coded-burst` 同向专题；建议 slug 可用。
- 依赖状态：旧 4b#1 专题 `closed`；RDL 长程测试 `dormant`；两者 `conflicts_with=[]`。

### 当前步骤与硬门

当前为新专题 GW Step 1。Step 2 的必要条件不是“找到若干关键词命中”，而是至少一张候选预卡同时通过六项 reopen gate，并通过 outage-vs-burst 语义门。任一承重条件失败即停在 Step 1 合法 terminal。

### Step 1 查询预算

最多 6 组定向 query，覆盖：

1. satellite/space-ground FSO low-elevation strong turbulence Gamma-Gamma；
2. temporal correlation/coherence/burst-error statistics；
3. coded FSO interleaving under correlated fading；
4. adaptive or channel-aware interleaver/codeword mapping；
5. parity/bit mapping across fading blocks；
6. recent coded-FSO baseline and direct competitors。

### 假设与否决条件（Lane B）

- **假设 H1**：合法低仰角星地 FSO 条件存在一手证据支持的强湍流/时间相关 GG 切片。
  - **否决条件**：只有仿真 stress 参数，或无法把 GG/闪烁/相关参数追溯到目标链路条件。
- **假设 H2**：相关/burst span 可接近或超过固定 interleaver/codeword span，并造成可恢复的码字内错误聚集。
  - **否决条件**：span 明显短于固定 span，或整 coherence block 在 finest oracle 下仍不可恢复。
- **假设 H3**：存在区别于 depth switching、LLR calibration、MCS 的真实 placement/segmentation action，并有 2019+ task-matched baseline。
  - **否决条件**：action 仅改 B/depth、改 LLR 标定、选 MCS，或找不到近期 task-matched baseline。

### 执行结果

- T001 → R001：2 组本地 query；physical-support 与 temporal-span 均 UNKNOWN。
- T002 → R002：4 组 `tools/search` query，S2+OpenAlex 结果 20/7/20/0；严格 2019+ task-matched baseline 仅 1 篇。
- T003 → R003：静态 BOM 完成；lifecycle=PARTIAL、interleaver controllability=NO、schema=PARTIAL、delay/overhead metric=NO；最小 adapter 3.75–5.0 人日，完整 testbed 8.5–12.0 人日。
- R004：三张预卡均未通过六项 reopen gate；outage-vs-burst 语义门 `NOT_PASSED/UNKNOWN`。
- D002：terminal=`STEP1_EVIDENCE_INSUFFICIENT`；Step 2 不执行。
- T004 → R005/V001：fresh independent verifier 14/14 PASS，13 条事实抽查，`ACCEPT`、blocker=0。

## 决策引用

- D001：授权物理条件 scope change，同时冻结旧方向 reopen gate 与禁止项（新建）。
- D002：Step 1 证据不足，禁止进入 Step 2（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。用户已显式授权物理条件 C 的 scope change；其余旧方向与仿真边界不变。

## 后续

V001/H001 已闭合。下一合法科学动作只能是出现新一手 target occurrence+AFD 证据与第二篇 2019+ strict task-matched baseline 后，显式重开 Step 1 缺口补证。
