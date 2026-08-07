# CCISP scheduling-only fresh-context independent verifier report

> 2026-08-07 | verifier scope: scheduling-only authority reconciliation | raw source commit: `67970307a051dd8149e1a750498a20674dfcfe6f`

## 1. Verdict

**Final re-verification: PASS。P0/P1/P2=`0/0/0`。**

- scheduling-only 的逐窗身份、BER、caller-path timing、分支调用与 typed-operation 证据可独立复现，足以支持本轮用户显式四选一中的 **`THESIS_ENGINEERING_METHOD_READY`**。
- current owners 已明确字段分账：canonical contribution tier=`THESIS_ENGINEERING_COMPONENT`；task-local terminal=`THESIS_ENGINEERING_METHOD_READY`。前者服从 RDL 三层 contribution contract，后者服从本轮用户显式终态合同，不构成新 contribution tier。
- active RDL 与 thesis-writing 的 topic-index/registry、D036/S017/CP019、方法包、inventory 与 spines 已一致；历史复合 2B 和 Q(8,6) 失败记录均保留。

### 首轮 FAIL 与纠正轨迹

首轮报告曾判 `FAIL`（P0/P1/P2=`0/2/1`）：当时 verifier 错把旧 D021/D022 的通用包装枚举当成本轮 terminal authority，因而误将 `THESIS_ENGINEERING_METHOD_READY` 判成第五个非法值，并建议 `THESIS_METHOD_READY`。随后收到本轮用户显式合同原文：本轮 terminal 只能四选一
`THESIS_ENGINEERING_METHOD_READY / NEEDS_ONE_BOUNDED_TIMING_CONFIRMATION / SUPPORTING_ONLY / EXECUTION_INVALID`；该合同时间更晚且任务更具体，优先于旧 D022。主控同时完成最小 projection 修复：D036 明确 tier/terminal 分账，current owners 统一 canonical tier，active thesis-writing topic-index/registry 删除陈旧复合 2B pending。fresh re-verification 证明三项首轮 finding 全部关闭。首轮 FAIL 保留在本段作为审计轨迹，不再代表当前 verdict。

## 2. 证据源与独立方法

本报告没有把 `recomputed-evidence.json` 或现有复算脚本的数值当作证据。独立方法为：

1. 直接对 commit `6797030...` 的 Git tree 做流式 archive 读取，只解析 `performance-*.json` 与 `timing-*.json` raw blobs；未 checkout、未改写 raw artifact。
2. 以 `(scene, snr_db, seed_index)` 建独立键集，检查 performance/timing 覆盖、schema、每 cell 窗数和键集一致性。
3. 从每个 performance blob 的 A-F/B-F 行独立累加 errors、bits、branch command counts 与 typed operations；同时逐 shard 比较 command/output SHA，并累加 raw mismatch 字段。
4. 从 timing `repetitions` 独立重算每方法 5 次中位数、逐 cell `B-F/A-F`，再按 seed 先平均 33 个 scene×SNR cell，最后以 30 个 seed cluster 计算均值及单侧 95% Student-t 上界：`mean + t(0.95,29)*s/sqrt(30)`。
5. 只用 commit 中 runner/core 源审计字段语义：`run_af` 每窗顺序执行 DA、NDA 各一次后 mux；`run_bf` 先取得相同 command，再仅调用所选分支；`assert_idle()` 是正式 before/after fail-closed 门，`platform_snapshot().cpu_load_percent` 在 post gate 之后采集，属于非门控描述字段。

## 3. 独立复算表

### 3.1 覆盖、身份与 BER

| 项 | 独立结果 | 判定 |
|---|---:|---|
| performance shards | 990/990 | PASS |
| timing shards | 990/990 | PASS |
| cell 结构 | 3 scenes × 11 SNR × 30 seeds | PASS |
| performance/timing unique key sets | 990 / 990，完全相同 | PASS |
| windows/cell | 400（990/990） | PASS |
| identity 总体 | 990×400=`396,000` windows | 与 990/990 shard 覆盖口径严格区分 |
| command mismatch | 0/396,000；A-F/B-F command SHA 990/990 相同 | PASS |
| selected-output mismatch | 0/396,000；A-F/B-F output SHA 990/990 相同 | PASS |
| A-F errors/bits | 32,589,134 / 304,128,000 | BER=`0.1071559803766835` |
| B-F errors/bits | 32,589,134 / 304,128,000 | BER=`0.1071559803766835`，与 A-F 完全相同 |

`990/990` 是 shard/cell 覆盖；`396,000` 是逐窗口 identity 总体；`304,128,000` 是 396,000×768 的 BER bit 总体。三者不能互换。

### 3.2 Timing

| 项 | A-F (before) | B-F (after) | 判定 |
|---|---:|---:|---|
| 990 个 shard 的平均 400-window median batch time | 271.684075 ms | 145.403487 ms | PASS |
| 平均每窗 | 679.210189 μs | 363.508716 μs | PASS |
| seed-cluster BF/AF mean | — | `0.5424435601792953` | PASS |
| seed-cluster sample SD | — | `0.0155967504322433` | 30 clusters |
| 单侧 95% t upper | — | `0.5472819331515957` | `<1`，PASS |
| cluster min/max | — | `0.5127364566 / 0.5713540102` | 非单 seed 驱动 |

### 3.3 分支调用与主要 typed operations

raw `branch_counts` 是 selector command 数，不是 A-F 实际 caller 次数；实际调用数由同 commit 的 `run_af`/`run_bf` caller path 与 396,000 窗确定。A-F 每窗 DA+NDA 各一次，B-F 每窗只执行 command 对应的一支。

| 项 | A-F | B-F | 降低 |
|---|---:|---:|---:|
| DA actual calls | 396,000 | 144,286 | 63.56% |
| NDA actual calls | 396,000 | 251,714 | 36.44% |
| total recovery-branch calls | 792,000 | 396,000 | 50.00% |
| complex multiply | 1,140,480,000 | 690,559,360 | 39.4501% |
| complex add | 328,284,000 | 174,401,374 | 46.8748% |
| divide | 231,978,923 | 113,016,655 | 51.2815% |
| compare | 205,842,923 | 103,278,923 | 49.8263% |
| real multiply | 456,192,000 | 248,722,176 | 45.4786% |
| FFT call | 396,000 | 251,714 | 36.4359% |
| sqrt/log/LUT | 26,850,923 | 10,452,655 | 61.0715% |
| dispatch/mux | 396,000 | 396,000 | 0.00% |

补充：`abs_sq` 下降 23.2564%，`real_add` 下降 35.5927%；`quantize`、`saturate` 在 A-F/B-F 都为 0。共同 dispatch 不下降与“仅跳过未选恢复分支”的机制一致。

## 4. Formal timing 合法性与污染门

990/990 timing blobs 均满足：

- schema=`t005.timing-shard.v1`；每方法 5 次 measured repetitions，raw repetitions 重算中位数与 `medians_ns` 990/990 精确一致，`rt_sched` 990/990 精确一致；
- 3 次 warm-up；A-F/B-F 采用固定交替 paired order；Q(8,6) 单独计时，不参与 scheduling headline；
- CPU affinity 全部为 `[2]`；`OMP/MKL/OPENBLAS/NUMEXPR` 全部为 `1`；
- 正式 before/after 共 1,980 个 `assert_idle()` snapshot，`contended=false` 且 heavy Python process 数为 0；最大正式门控 system load 为 54.9%，无一超过 60%。

三个超过 60% 的值来自 `platform.cpu_load_percent`，其调用在 post `assert_idle()` 之后，故不是冻结 runner 的 fail-closed 输入：

| scene | SNR | seed | post-timing cpu_load_percent |
|---|---:|---:|---:|
| weak | 5 | 21027 | 87.3% |
| weak | 25 | 21020 | 64.2% |
| moderate | 13 | 21021 | 61.6% |

结论：这 3 个描述性样本应保留披露，但不能反向污染已通过的正式 before/after 门；现有 timing 只支持同机、冻结软件 caller path 的相对时延，不支持硬件吞吐、功耗或 PPA 外推。

## 5. Authority reconciliation

### PASS findings

- 方法包把动作冻结为 `receiver-visible selector → branch command → only selected recovery branch → common downstream detector`，明确不改变 selector 或 CPR estimator。
- `internal-method-kernel-inventory.yaml` 已将 `branch_route_b` 归入既有 CCISP；顶层 reconciliation authority 指向 D036；旧复合 `2B` 条目仍保留为 `SUPPORTING_ONLY / SUPERSEDED_COMPOSITE`。
- Q(8,6)/P03 fixed-point 条目和失败边界仍保留；没有删除 459 次 stage-2 漏记、13 dB 状态不可表示及无真实综合等历史。
- `thesis-method-spines.md` 把 Ch5 与 Ch3 区分为执行 schedule vs selector 决策，并明确 Q(8,6) 不进入 Ch5。
- D023 原文保留，并以“只取代过宽解释”的方式被 D036 部分取代；D036、S017、CP019 都保持 scheduling/fixed-point 分账。
- SVG 是可编辑、可解析的原生 SVG；左右公平 comparator、实线数据流/虚线 command 控制流、相同 selector/分支/公共检测链均有明确编码，未出现定点、硬件或 PPA 图元。

### 首轮 findings 的关闭状态

1. **原 P1（terminal ontology）：CLOSED。** 首轮采用了错误 authority。D036 现已逐字登记本轮用户显式四选一，并说明其晚于且特异于 D021/D022；D036、S017、CP019、RDL topic-index、方法包、inventory、spines、两个 active registry projection 均一致使用合法 terminal `THESIS_ENGINEERING_METHOD_READY`。
2. **原 P1（contribution-tier ontology）：CLOSED。** D036、S017、方法包与 inventory 已明确 canonical contribution tier=`THESIS_ENGINEERING_COMPONENT`，没有把 task-local terminal 当成第四种 contribution tier。定向扫描未发现 current owner 仍使用独立 tier `THESIS_ENGINEERING_METHOD`。
3. **原 P2（active thesis-writing projection stale）：CLOSED。** `.sessions/2026-07-09-thesis-writing/topic-index.md` 已将原 2B pending 划销并指向 D036/V020；`.sessions/_registry.yaml` 对应 active 条目已改为 scheduling-only ready、Q(8,6) SUPPORTING_ONLY、不跑新实验。

复验同时确认 `.sessions/_registry.yaml` 与 `internal-method-kernel-inventory.yaml` 均可由 YAML parser 完整加载，SVG 可由 XML parser 加载；current claim ceiling 中 74.6%、FPGA/PPA 等命中均位于明确禁止声称段，而非正向声明。

## 6. Claim ceiling findings

| 禁止声称 | 检查结果 |
|---|---|
| 新 selector | PASS：明确归属既有 CCISP，未改 selector；不得以 2B 另立 selector |
| 新 CPR estimator | PASS：DA/NDA estimator identity 冻结，贡献只在执行 schedule |
| fixed-point method | PASS：Q(8,6) 与 scheduling 分账，继续 SUPPORTING_ONLY |
| FPGA/PPA/LUT/DSP/power/throughput | PASS：均明确排除；现有 operation count 与 CPU timing 未冒充综合结果 |
| 74.6% 总接收机复杂度 | PASS：列入禁止复活；当前只报分支调用与逐类 typed operations |
| 通用双专家加速 | PASS：方法包明确不推广；成立条件限定 command 可在分支执行前由 receiver-visible 信息得到 |

方法包 contribution statement 的 0/396,000 mismatch、BER identity、BF/AF=0.5424、单侧上界 0.5473、分支调用 -50% 与主要操作降幅均有 raw 证据。不得把这些软件 caller-path 数字扩大到 FAMILY/DOMAIN、任意专家路由或硬件结论。

## 7. Comparator fairness 与 terminal recommendation

route A 与 B-F 使用相同 raw window、配置、pilot、selector/controller、branch command、DA/NDA 实现和公共下游；差异仅为 route A 先执行两支再 mux，B-F 先 command 后只执行一支。A-F/B-F 990/990 command SHA 相同、990/990 selected-output SHA 相同、逐窗 mismatch=0、pooled BER 完全相同。route A 是真实串行 caller path，A/B 计时有交替 paired order、相同 warm-up/repetition 和正式污染门。因此 comparator 对“执行调度是否减少真实软件 caller-path 工作且保持输出等价”这一窄 claim 是公平且充分的。

**Terminal recommendation（本轮四选一）：`THESIS_ENGINEERING_METHOD_READY`。**

这一推荐不支持新算法/新 selector 的 scientific-method 主张；它表示一个合法 canonical `THESIS_ENGINEERING_COMPONENT` 已有完整动作链、公平 comparator、输出等价、真实 caller-path cost reduction、主图/主表/消融和明确边界，足以闭合学位论文工程方法章。`NEEDS_ONE_BOUNDED_TIMING_CONFIRMATION` 不成立，因为 990/990 formal timing shards、污染门和单侧聚类上界均已闭合；`SUPPORTING_ONLY` 会错误连带 fixed-point 失败；`EXECUTION_INVALID` 与 raw identity、合法 timing 及 caller trace 相矛盾。

## 8. Blocker counts

| severity | count | closure |
|---|---:|---|
| P0 | 0 | raw evidence、信息边界、comparator 与 timing integrity 无 blocker |
| P1 | 0 | 首轮两项 P1 已关闭：task-local terminal authority 与 canonical contribution tier 已正确分账并同步 current owners |
| P2 | 0 | active thesis-writing topic-index/registry 的复合 2B pending 陈旧投影已关闭 |

**最终验收：PASS。** 允许的下一步仍仅为把冻结 Ch5 方法包、主图与主表整合进正文；本 PASS 不授权修改算法、恢复 fixed-point、补跑实验或扩大 claim。
