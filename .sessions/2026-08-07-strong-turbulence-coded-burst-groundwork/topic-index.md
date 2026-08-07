# Topic Index: 低仰角强湍流 coded-burst reliability Groundwork

> 状态: closed | 创建: 2026-08-07 | 最后更新: 2026-08-07（D002：`STEP1_EVIDENCE_INSUFFICIENT`）

## 专题信息

- **slug**: `2026-08-07-strong-turbulence-coded-burst-groundwork`
- **title**: 低仰角强湍流 coded-burst reliability Groundwork
- **depends_on**:
  - `2026-06-19-4b1-adaptive-interleaving-groundwork`（closed；继承旧 4b#1 永久事实和排除边界）
  - `2026-07-23-research-direction-lab-longitudinal-test`（dormant；继承 P08/P08-R2 coded-chain 与 outage 边界）
- **conflicts_with**: 无

## 范围边界

**原始目标**：判断在具有一手物理依据的低仰角强湍流/时间相关 GG 条件下，固定交织、连续码字映射或固定 parity placement 是否因 burst duration/coherence mismatch 产生真实失败，并能否形成区别于 LLR calibration、MCS 和旧 B=27 自适应交织的可复用方法问题。

**当前范围**：GW Step 1 定向检索、历史碰撞审计、物理参数来源分级、最多三张机制不同的候选预卡、旧方向 reopen gate、outage-vs-burst 语义门，以及 P08-R2/Sionna coded-chain 资产的只读静态 BOM。只有至少一个候选同时通过全部 Step 1 承重门，才进入 Step 2 获取与 CORE 判定；Step 2 完成后停在用户确认门。

**明确不含**：

- 不捏造极端 Gamma-Gamma `α/β`、闪烁、相关或 burst 参数。
- 不换名重开旧 B=27 adaptive-interleaving/depth-switching。
- 不重开 P08 coded-LLR calibration。
- 不做 AMC/MCS 或码率/调制选择。
- 不运行 coded-chain、MVE 或任何仿真，不修改脚本。
- 不把不可恢复 outage 包装成交织、placement 或 segmentation 问题。
- 不修改 `common/`、`params.py`、旧 raw/result、Skill 或四个 `p05_run*.log`，不 push。

**范围变更记录**：

- **[2026-08-07] D001**：允许将物理条件 C 从旧 4b#1 的“LEO 中弱湍流”改为“有真实文献依据的低仰角强湍流/outage 切片”。
  - 原因：旧 4b#1 在中弱湍流下 B=27 已覆盖全部可见 burst，不能回答强湍流/相关衰落下是否存在不同的错误聚集机制。
  - 新范围：仅考察一手证据支持、且可区分可恢复 burst 与不可恢复 outage 的低仰角强湍流/时间相关 GG 切片。
  - 影响的未决项：是否存在合法物理切片、2019+ task-matched baseline，以及 interleaving/placement 是否能改变译码输入错误分布。

## 已确认结论

### 不变量（动任何一条必须重新讨论）

1. 旧 4b#1 永久事实保持有效：中弱湍流 `Lburst=60–428`；B=27 容量约 810；0/15 仰角超容；adaptive-vs-static BER 上界 0 dB。
2. 新候选必须同时通过六项 reopen gate：一手物理依据；burst/correlation span 接近或超过固定 span；失败不是整个 coherence block 不可恢复 outage；action 能改变译码输入错误分布；存在 2019+ task-matched baseline；action 不等同旧 B=27 depth switching。
3. outage-vs-burst 语义门先于方法判断。若 finest oracle LLR/decoder 仍整码字失败且 placement/interleaving 不改变可恢复信息量，terminal=`OUTAGE_NOT_INTERLEAVING_PROBLEM`。
4. 检索证据必须区分外场测量、链路预算/物理推导、仿真设计参数和人为 stress 参数；仿真强湍流参数不能冒充真实低仰角 occurrence。
5. 当前在新专题 GW Step 1；未通过硬门不得进入 Step 2，未完成 Step 3/3.5/4a 不得运行 MVE、coded-chain 或形成 Go/METHOD_SIGNAL/论文 claim。
6. P08-R2 只作为工程资产与负面历史边界，不继承其方法 verdict；任何 receiver 侧方案不得消费 hidden SNR/GG truth。

### 其他结论

- 用户已显式授权上述物理条件 scope change；该授权不恢复旧 4b#1/P08/AMC，也不授权仿真。
- 方法类型暂定为编码/映射设计类，须由后续 CORE 精读中的真实 M-C-A 再确认。

## GW Progress

| Step | 状态 | 日期 | 证据 | 下游门控 |
|---|---|---|---|---|
| 1 search | 🛑 STOPPED | 2026-08-07 | S001/R001–R004/D002 | `STEP1_EVIDENCE_INSUFFICIENT`；无候选六项全过 |
| 2 acquire | NOT_RUN | — | D002 | Step 1 未通过，禁止 |
| 3 read | ⬜ FORBIDDEN | — | — | Step 2 用户确认前禁止 |
| 3.5 supplement | ⬜ FORBIDDEN | — | — | Step 3 未完成前禁止 |
| 4a feasibility | ⬜ FORBIDDEN | — | — | Step 3/3.5 未完成前禁止 |

## 进展线索

- **S001 + D001**（2026-08-07）：registry 查重通过；新专题建立；冻结 scope change、旧方向 reopen gate、outage 语义门和 Step 1 限定。
- **R001–R004 + D002**（2026-08-07）：6/6 query 收口；目标强条件 occurrence/AFD 与 recoverable span 未闭合；严格 2019+ task-matched baseline 仅 1 篇；三预卡均未过 reopen gate；terminal=`STEP1_EVIDENCE_INSUFFICIENT`，Step 2 不执行。
- **R005 + V001 + H001**（2026-08-07）：fresh verifier 14/14 PASS、13 条承重事实抽查，`ACCEPT`、blocker=0；专题关闭与未来重开条件交接完成。

## 未决项

- 是否存在一手物理证据支持的合法低仰角强湍流/时间相关 GG 切片。
- 相关/burst span 是否达到固定 interleaver/codeword span，而非只改变平均衰落强度。
- 是否存在 2019+ task-matched baseline，且 action 与旧 B=27 depth switching、LLR calibration、MCS 明确不同。
- P08-R2/Sionna 资产能否以不超过约 5 天的最小 adapter 支撑后续 testbed（本轮只读估算）。

## 当前位置

专题以 `STEP1_EVIDENCE_INSUFFICIENT` 关闭。Step 2 未执行。下一合法动作：只有出现新一手 target evidence（真实低仰角强条件 occurrence + threshold-conditioned AFD/相关尺度）和第二篇 2019+ strict task-matched baseline，才可由用户显式重开 Step 1 缺口补证；不得直接进入 Step 2 或 coded-chain。
