# CCISP 先选后算单分支接收机架构：Ch5 方法包

> 2026-08-07 | 目标读者：学位论文导师与评审 | 用途：Ch5 直接写作与证据审计
> 方法身份：**CCISP select-before-execute single-branch receiver architecture**
> Terminal：`THESIS_ENGINEERING_METHOD_READY`

## 1. 权威协调

历史“2B”把两条可分离的证据链装在同一候选名下：一条是先选后算的 scheduling-only 执行架构，另一条是
Q(8,6) 定点控制器。T005 的正式 disposition 实际已给出 scheduling verifier=`PASS`，而 fixed-point
verifier=`FAIL / SUPPORTING_ONLY`；后续 D023 又指出 scheduling 动作与既有 CCISP 动作重复，因而不能另立
一个“新 2B selector”。这三个判断并不矛盾：**动作归属 CCISP，不另造 selector；scheduling 科学与工程证据
有效；定点失败不得连带否定 scheduling。** D036 据此取代 D023 中把整个 T005 scheduling lineage 一并降为
支持材料的过宽解释，历史记录保留。

本章只使用 scheduling-only 证据。Q(8,6)、字长选择、定点 BER、LUT/DSP、功耗与综合结果均不进入方法链、
主图、主表或贡献声明。

## 2. 问题、M-C-A 与贡献层级

### 2.1 Baseline defect

公平基线 route A 在同一个接收窗口上先后执行 DA 与 NDA 两条载波恢复分支，再用 CCISP selector 的命令
从两份结果中选一份送入公共检测链。未选分支的全部估计计算已经发生，造成确定性的部署计算冗余；该冗余
不改善 selector、相位估计器或 BER。

### 2.2 M-C-A

- **M（现有机制）**：route-A dual-branch-then-select。
- **C（目标条件）**：selector 仅使用当前窗口 receiver-visible 信息，且 branch command 在恢复分支执行前可得。
- **A（失效原因与动作）**：双分支计算把“选择哪一支”和“执行哪一支”的顺序倒置；将 selector 前移，先产生
  branch command，再且仅执行被选恢复分支，最后进入相同的公共检测器。

贡献层级限定为**学位论文工程方法 / 接收机执行架构**；项目 canonical contribution tier 记为
`THESIS_ENGINEERING_COMPONENT`，本轮用户冻结的 terminal 记为 `THESIS_ENGINEERING_METHOD_READY`，两者
不混为同一枚举。不声称新 selector、新 CPR estimator、定点方法、FPGA 资源或功耗结果，也不推广为
任意双专家系统的通用加速原理。

## 3. 方法动作链与实现真相

动作链固定为：

`receiver-visible selector → branch command → only selected recovery branch → common downstream detector`

实现真相三联卡：

| 项 | 冻结合同 |
|---|---|
| information access | selector 仅访问当前 raw receiver window、配置的 nominal SNR 与 DA pilot；TX payload truth、事后 BER 和未选分支输出不进入在线决策 |
| metric signature | 每 cell 400 窗；比较 command、selected output、errors/bits、typed operations 与隔离 CPU timing；性能与计时各 990 shards |
| state lifecycle | 每窗从同一份冻结输入独立启动；不声明跨窗 tracking、缓存或状态复用；统计 CI 时按 seed 聚类，先平均每 seed 的 3 scenes×11 SNR cells |

### 3.1 伪代码

```text
Algorithm: CCISP Select-Before-Execute Single-Branch Receiver
Input : current received window r, receiver configuration c, DA pilots p
Output: detected symbols b_hat

1  s <- CCISP_ReceiverVisibleStatistic(r, c, p)
2  u <- CCISP_Selector(s)                 # u in {DA, NDA}
3  if u == DA then
4      z <- DA_CarrierRecovery(r, c, p)
5  else
6      z <- NDA_CarrierRecovery(r, c)
7  end if
8  b_hat <- CommonDownstreamDetector(z, c)
9  return b_hat
```

这里没有改变步骤 1–2 的 selector，也没有改变步骤 4 或 6 的恢复估计器；唯一方法动作是把 branch command
变为执行命令，使未选分支不被调用。

## 4. 公平 comparator

| 冻结项 | route A：dual-branch-then-select | 本方法：select-before-execute |
|---|---|---|
| 输入、窗口顺序、seed、场景、SNR | 相同 | 相同 |
| selector 输入与 branch command | 相同 | 相同 |
| DA/NDA 分支实现 | 相同 | 相同 |
| 执行顺序 | 依次执行 DA 和 NDA，再 mux | 先发 command，只执行 DA 或 NDA |
| 计时边界 | controller + 两分支 + mux | controller + 被选分支 + mux |
| 下游检测与 BER 统计 | 相同 | 相同 |

route A 使用真实串行双分支 caller path；没有通过并行化、重复 I/O 或额外等待人为劣化基线。990 个 timing
shards 均为单 CPU affinity `[2]`、四类数值线程数均为 1、3 次 warm-up 与 5 次 measured repetition；正式
before/after 污染门的 1,980 个快照均未判 contention。三个非门控 post-timing CPU-load 样本超过 60%，但不
触发冻结 runner 的 fail-closed 规则；因此数字用于同机软件执行时延，不外推硬件吞吐或功耗。

## 5. 确定性证据

### 5.1 口径

- `990/990`：3 scenes × 11 SNR cells × 30 seeds 的完整 cell/shard 覆盖；性能与 timing 各有 990 份。
- `396,000 windows`：990 cells × 400 windows/cell，是 command 与 selected-output identity 的逐窗口总体。
- `304,128,000 bits`：396,000 windows × 768 bits/window，是 pooled BER 的 bit 总体。

三种口径分别回答覆盖、逐窗身份和 BER 统计问题，不互换、不相加。

### 5.2 输出等价性与时延

| 指标 | route A | 本方法 | 结论 |
|---|---:|---:|---|
| command mismatch / 396,000 窗 | 0 | 0 | selector command identity |
| selected-output mismatch / 396,000 窗 | 0 | 0 | 输出逐窗 identity |
| pooled errors / bits | 32,589,134 / 304,128,000 | 32,589,134 / 304,128,000 | BER 均为 0.1071559804 |
| 每 400 窗平均批时延 | 271.6841 ms | 145.4035 ms | 软件 caller path |
| 每窗平均时延 | 679.2102 μs | 363.5087 μs | 同上 |
| BF/AF seed-cluster ratio | 1 | 0.5424 | 降低 45.76% |
| BF/AF 单侧 95% t-CI 上界 | — | 0.5473 | 上界仍低于 1 |

cluster 定义为 seed：每个 seed 先平均 3 scenes×11 SNR cells，再对 30 个 seed-cluster 计算 t-CI。

### 5.3 分支调用与主要操作数

route A 每窗调用 DA 和 NDA，共 792,000 次；本方法按命令调用 DA 144,286 次、NDA 251,714 次，共
396,000 次，**分支调用总数降低 50.00%**。

| typed operation | route A | 本方法 | 降低 |
|---|---:|---:|---:|
| complex multiply | 1,140,480,000 | 690,559,360 | 39.45% |
| complex add | 328,284,000 | 174,401,374 | 46.87% |
| divide | 231,978,923 | 113,016,655 | 51.28% |
| compare | 205,842,923 | 103,278,923 | 49.83% |
| real multiply | 456,192,000 | 248,722,176 | 45.48% |
| FFT call | 396,000 | 251,714 | 36.44% |
| sqrt/log/LUT | 26,850,923 | 10,452,655 | 61.07% |
| dispatch/mux | 396,000 | 396,000 | 0.00% |

dispatch/mux 不下降，说明收益来自跳过未选恢复分支，而不是省略共同控制工作。峰值软件 live storage 仅由
104,448 B 降至 100,352 B，不作为主贡献数字。

## 6. Ch5 主图、主表与消融

### 主图

使用 [CCISP 先选后算单分支架构图](../../../simulation/figures/ccisp_select_before_execute_single_branch.svg)：
左侧给出公平基线“同窗双分支→选择”，右侧给出“receiver-visible selector→branch command→互斥单分支→
common detector”，控制流用虚线，数据流用实线。图中不得出现定点、LUT/DSP 或硬件功耗块。

### 主表

本文件 §5.2 为性能等价性与时延主表，§5.3 为复杂度主表。正文 headline 只使用：0/396,000 output
mismatch、BER identity、BF/AF=0.5424（单侧 95% 上界 0.5473）、分支调用下降 50.00%，以及可审计的
typed-operation 降幅。

### 消融清单

1. route A 双分支执行 vs 本方法单分支执行（主消融）。
2. 按 DA-command 与 NDA-command 分层报告调用次数和 identity，防止收益由单一分支占比掩盖。
3. controller/dispatch 固定成本 vs recovery-branch 可省成本的 operation breakdown。
4. 3 scenes、11 SNR 与 30 seeds 的分层 ratio/identity，检查收益是否仅来自单个工作点。
5. 如未来出现真实硬件实现，另立综合合同；不得用当前软件 operation proxy 替代 LUT/DSP/power。

## 7. 适用边界

方法成立需要 selector command 在分支计算前可由 receiver-visible 信息得到，且 DA/NDA 分支共享相同的下游
接口。若 selector 必须读取两支的完整输出才能决策、两支需要联合计算、硬件并行双支路吞吐而非串行 caller
时延是目标，或未选分支承担必要的跨窗状态更新，则本方法的 45.76% 软件时延收益不可直接外推。

## 8. Ch5 可直接采用的 contribution statement

> 针对传统双分支自适应载波恢复“先完整计算 DA 与 NDA 两支、再选择输出”所造成的部署计算冗余，本文提出
> 一种 CCISP 先选后算单分支接收机架构。该架构利用既有接收端可见选择统计量预先生成分支命令，每个窗口
> 仅执行被选中的恢复分支，并复用统一的后续检测链。在 3 类信道场景、11 个 SNR 工作点和 30 个随机种子
> 构成的 396,000 个窗口上，该架构与双分支基线保持逐窗口选择输出一致，pooled BER 完全相同；同时将恢复
> 分支调用次数降低 50.00%，使同机软件执行时延降至基线的 0.5424，且该比值的单侧 95% 聚类置信上界为
> 0.5473。主要复乘、复加、除法和 FFT 操作分别降低 39.45%、46.87%、51.28% 和 36.44%，从而在不改变
> selector 与 CPR 估计器的前提下，实现了可审计的接收机计算流程优化。

## 9. 证据指针

- 原始 immutable artifacts：commit `67970307a051dd8149e1a750498a20674dfcfe6f` 下
  `projects/simulation/results/2b_fixed_point_branch_routed_cpr_closure/{performance-*,timing-*}.json`
- scheduling-only 复算：[recomputed-evidence.json](../../../simulation/results/ccisp_single_branch_authority_reconciliation/recomputed-evidence.json)
- 确定性复算器：[recompute_ccisp_single_branch_evidence.py](../../../../tools/recompute_ccisp_single_branch_evidence.py)
- 独立 verifier：[independent-verifier-report.md](../../../simulation/results/ccisp_single_branch_authority_reconciliation/independent-verifier-report.md)
- 权威裁决：RDL D036 / V020；历史 T005、V016 与 D023 保留。
