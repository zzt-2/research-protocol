# Topic Index: Shared M0-Power FOE–CPE Groundwork (Step 1–2)

> 状态: active | 创建: 2026-08-05 | 最后更新: 2026-08-05（T008 Phase A 建专题；GW Step 1–2 执行中）

## 专题信息

- **slug**: `2026-08-05-shared-m0-foe-cpe-groundwork`
- **title**: 共享 M0 次幂 FOE–CPE 计算图正式 Groundwork（Step 1–2）
- **性质**: 派生专题。承接 RDL system 专题 T008 / S015 / D024 / CP005；只执行 GW Step 1 检索 +
  Step 2 全文获取/覆盖面门，停在用户确认门，不进 Step 3。

## 范围边界

### 原始目标（冻结，来自 T008）

> 判断共享 M0 次幂 FOE–CPE 计算图是否构成有文献空间、真实成本动作和可验证传统对手的
> Ch5 工程方法候选。

### 当前范围

- 在新专题内执行 GW Step 1 检索（复用 `search-archive/_index/all-papers.jsonl` + 现有
  carrier-sync/CPR 论文库 + 历史 search-archive，覆盖不足时补 `tools/search`）；
- 执行 GW Step 2 全文获取与覆盖面门（身份/内容质量判定），写 receipt 与 coverage report；
- 形成直接竞品初筛矩阵（metadata/abstract 级，不当精读结论）；
- 单次统一 commit，不 push；四个既有 `p05_run*.log` 不修改、不暂存。

### 明确不含

- 不进 GW Step 3 / 3.5 / 4a；不实现、不仿真、不跑 MVE、不写论文 claim；
- 不改 `.agents/skills/`、`projects/simulation/common/`、`params.py` 或既有算法；
- 不重开 P2–P5、T006 C3、P09、G1、AMC 或 dormant campaign；
- 不用 oracle/headroom 决定 Step 1–2 的 Go；
- 不把"没人题名相同"写成 novelty，不把一行实现或输出等价自动写成 rejection；
- 不创建实验合同、代码 sandbox、raw 仿真结果或论文图；
- 不宣布 `THESIS_METHOD_READY`、METHOD_SIGNAL、Go/Kill 或 active carrier；
- 修改 NDA-ML 估计器统计触发既有 `NDA_ML_BODY_REOPEN`，不属于本候选。

### 范围变更记录

（暂无）

## 已确认结论

### 不变量

- **冻结研究对象（仅用于检索/获取，不作为 Step 3/4a 结论）**：
  - **M**：当前串行 NDA carrier recovery 先用 M0 次幂做 FOE，再对 CFO 补偿信号重做 M0 次幂做 CPE。
  - **C**：资源受限的软件或硬件实现，要求与当前 receiver 输出/BER 匹配。
  - **A**：用一个共享 M0-domain 表示同时驱动 FOE 与 CPE；升幂域 CFO 去除必须使用
    `raised * exp(-j*M0*omega*k)`，最终在原信号域补偿 `omega*k + phi`。
- **P1 当前层级 = `THESIS_ENGINEERING_COMPONENT` 设计候选**（来自 D024），不是 METHOD_SIGNAL。
- **廉价吸收判据**：必须在实际执行路径或工具链中存在；假想 compiler/CSE 不算。
- **Step 2 覆盖面门必须用户确认**：terminal 只能是 `STEP2_READY_FOR_USER_CONFIRMATION` /
  `STEP2_BLOCKED_BY_COVERAGE_GAP` / `ENTRY_INVALID`，不得自动进 Step 3。
- **区分显式共享 vs 改估计器统计**：后者触发 `NDA_ML_BODY_REOPEN`，不属于本候选。

### 其他结论

（Step 1–2 完成后填充；本轮不写方法/数据流/竞品全文语义结论）

## 进展线索

- **S001**：Phase A 建专题 + Phase B Step 1 检索（97 去重，3 语义类，门槛全过）+ Phase C Step 2
  获取/覆盖面门（**12 篇合格全文**，含 2 篇 HIGH★ 直接竞品；blit 第三轮补取 7 篇 IEEE，
  terminal=`STEP2_READY_FOR_USER_CONFIRMATION`）。H001 已交接。
- **D001**：冻结研究对象与范围边界（本专题新建，依据 T008/D024）。

## 未决项

- 传统 joint frequency/phase estimator 是否早已使用一次 Mth-power 序列（待 Step 1 初筛 + Step 3 关闭）；
- coherent optical/FSO 中是否有同数据流、同动作的直接实现；
- 共享图相对显式 conventional refactor 是否还有可区分工程 claim；
- 哪些论文能提供 operation count、latency、hardware/dataflow 或 matched-performance comparator；
- Step 2 覆盖面是否达标（≥5 篇身份+内容质量合格）——待用户确认。

## 当前位置

T008 已完成：GW Step 1（✅ 门槛全过）+ Step 2（✅ **12 篇合格全文**，含 2 篇 HIGH★ 直接竞品，
待用户确认覆盖面）。terminal = **`STEP2_READY_FOR_USER_CONFIRMATION`**。停在覆盖面确认门，
**Step 3 未授权**。下一合法动作 = 用户确认覆盖面后开新对话执行 Step 3（启动前必读
`stages/gw-read.md`）。

> **修订**（2026-08-05）：Step 2 初版误判 blit 跳过 IEEE 第三轮通道（用户纠正），补跑 blit 后取回
> 7 篇高优先 IEEE 全文（含 2 篇最高优先直接竞品），合格全文 5→12 篇。详见 S001 修订段与
> coverage report 修订说明。
