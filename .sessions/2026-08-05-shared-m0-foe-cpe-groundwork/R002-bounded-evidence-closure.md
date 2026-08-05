# [R002] Q-P1-01 bounded evidence closure

> 2026-08-05 | 关联：2026-08-05-shared-m0-foe-cpe-groundwork / D005

## 调研问题

在不进入 GW Step 3.5/4a、实现或仿真的边界内，关闭 Q-P1-01 的两个证据债务：OFC 2016 是否覆盖
exact raised-domain lifetime/action，以及冻结预算内是否存在 2019+ 正式发表、同输入/同估计器、
task-matched 的 FOE→CFO-removal→CPE baseline，可由数据流证明重复 raised-domain 动作。

## 发现

### 1. Bounded gw-search（冻结预算 6/6）

| 组 | query / source | raw / dedup / final | 归档 |
|---|---|---:|---|
| Q1 | `Hardware optimization for carrier recovery based on Mth power schemes Th2A.43`；S2/OpenAlex/SerpAPI/Tavily/Firecrawl/Exa | 未保留 / 未保留 / 19 | `search-archive/2026-08-05/hardware-optimization-for-carrier-recovery-based-on-mth-powe.json` |
| Q2 | `joint frequency offset estimation carrier phase recovery coherent optical implementation`；S2/OpenAlex | 40 / 37 / 30 | `search-archive/2026-08-05/joint-frequency-offset-estimation-carrier-phase-recovery-coh.json` |
| Q3 | `m-th power Viterbi phase recovery frequency estimation shared reuse`；S2/OpenAlex | 22 / 22 / 14 | `search-archive/2026-08-05/m-th-power-viterbi-phase-recovery-frequency-estimation-share.json` |
| Q4 | `carrier recovery dataflow hardware architecture frequency phase estimation optical`；OpenAlex | 20 / 19 / 5 | `search-archive/2026-08-05/carrier-recovery-dataflow-hardware-architecture-frequency-ph.json` |
| Q5 | `raised power intermediate reuse lifetime CFO removal carrier phase recovery`；OpenAlex | 12 / 12 / 1 | `search-archive/2026-08-05/raised-power-intermediate-reuse-lifetime-cfo-removal-carrier.json` |
| Q6 | JLT 2018 forward citation，DOI `10.1109/JLT.2018.2831918`；OpenAlex | 13 / 13 / 13 | `search-archive/2026-08-05/doi-10-1109-jlt-2018-2831918.json` |

Q1 首次调用的外层输出中断，JSON 只保留 final=19；为守 6 组上限没有重跑。
Q2–Q6 的 raw/dedup 数来自 bounded-search worker 回执；现存 JSON 顶层只保留
`query/timestamp/sources/total/results`，没有独立 raw/dedup receipt，因此可从 artifact 直接重算的仅是
query/source/final total/results。该证据限制不以重跑第 7 组修补。

检索前全局索引为
21,398 条，确定性宽关键词命中 425 条；既有三组 P1 结果共 75 条，2019+ 语义命中 50 条（未跨文件
去重）。按同输入序列、同估计器、同 FOE→CFO-removal→CPE 任务严格复筛后，合格 recent baseline
为 **0 篇**。

### 2. OFC 2016 获取与 exact-action 裁决

- `tools/download --doi 10.1364/OFC.2016.Th2A.43`：`all_failed`，只有 398 B metadata；
- Optica 官方摘要页 HTTP 200、标题一致（95,130 B HTML）；官方 PDF 端点重定向到 Radware
  `validate.perfdrive.com`，返回 15,088 B HTML，非 PDF；按止损规则停止；
- 同线 PTL 2016（`10.1109/LPT.2016.2598443`）也未取得全文：tools/download 失败、arXiv 精确题名
  0 条、IEEE blit 两次 45 s 超时。

因此 OFC 2016 的一手 exact boundary 裁决为
**`UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`**。Optica 摘要与 JLT 2018 二手陈述只支持 generic
shared-m-th-power collision；不得把 PTL 元数据或摘要冒充 OFC 全文，也不能据此判定 exact
`raised*exp(-j*M0*omega*k)` lifetime 已覆盖或未覆盖。

### 3. 2019+ 近邻全文数据流审计

合格 task-matched baseline 清单为 **0 篇**。以下三篇已有有效全文仅用于解释排除边界：

| 论文 | 全文数据流事实 | 裁决 |
|---|---|---|
| JLT 2019，`10.1109/JLT.2019.2892901` | full CR；传统链为 differential m-th-power FE + differential PR（`content.md` L21, L43），相邻样本 correlation 的重复已由 P=1 shared-correlation refactor 吸收；提出架构进一步去除 m-th power/LUT（L23, L80） | `NEAR_MISS_ESTIMATOR_CHANGE`：不是串行 NDA `x^M0` FOE→CFO-removal→VV/CPE，不能证明 P1 raised-domain 过早丢弃 |
| ISCAS 2022，`10.1109/ISCAS48785.2022.9937906` | CPE-only VV4E；`x_k^4`→buffer→adder→CORDIC→phase compensation（L35, L59–63, L79–81, L97–101），实验明确忽略 frequency offset（L182） | `NEAR_MISS_CPE_ONLY`：没有 FOE/CFO-removal 边界，raised 量只在单级 CPE 正常消费 |
| LCOMM 2026，`10.1109/LCOMM.2026.3653195` | CPE-only；第一级对约 18.75% QPSK-like 子集做 mVV，第二级对全体符号先 CT 再 VV（L57, L67）；prefix-sum 重构数据流并把第二级换成 MLE（L75–77, L95–101, L119–131） | `NEAR_MISS_CPE_ONLY`：两级输入不同且更换估计器，不是同序列重复，也不能冒充 P1 conventional refactor |

其余 metadata 近邻同样因 pseudo-pilot、CO-OFDM joint ML、pilot-tone 或 generic 跨模块复用而排除。
本轮不要求论文作者显式写出 failure A；排除依据是公式/框图/数据流不能建立同任务重复动作。

### 4. Q-P1-01 四判据重判

| canonical 判据 | 结果 | 依据 |
|---|---|---|
| 1. M/C/A 具体 | PASS | 本地串行 NDA caller 可具体指出两次 `rx**M0`；A 可由实际执行路径定义，不依赖作者显式命名 |
| 2. 有可复用方法产出 | PASS | shared raised-domain graph、lifetime contract 与 matched-output protocol 形态明确 |
| 3. 有近期 task-matched baseline | **FAIL** | 6/6 query + 引用链 + 现有索引严格复筛为 0；三篇有效 recent 全文均为估计器改变或 CPE-only |
| 4. 可量化对标 | PASS | output error、BER/SNR、op/memory/latency/throughput/PPA 均可量化 |

## 结论

冻结检索预算内没有 2019+ 合格 task-matched baseline，触发
**`RECENT_BASELINE_UNAVAILABLE`**。Q-P1-01 仍为 1/2/4 PASS、3 FAIL，不构成 canonical Q#；P1
降为 **`SUPPORTING_ONLY`**。OFC 2016 exact action 因一手全文不可得保持未决，但这一未决不能推翻
recent-baseline 硬停止，也不授权继续检索。

**P1 的 generic action 已碰撞，窄 delta 未形成合法 Q；停止该方向，下一轮轮换新候选，不再改名重开。**

本结论是 Step 3 canonical Q 空集关闭，不是 Step 4a Go/Kill、METHOD_SIGNAL 或论文 novelty 声称。

## 对决策的影响

新建 D005：取代 D004 的 blocked-waiting 状态，关闭本专题；保留 R001/D003 的 generic collision
历史和本 R002 的 OFC primary-source 覆盖缺口。下一轮只能在上游 RDL 候选池轮换机制不同的新候选，
不得以 P1 改名重开或进入 Step 3.5/4a/实现/仿真。
