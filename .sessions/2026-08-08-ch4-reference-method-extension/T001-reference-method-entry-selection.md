# Task Brief: Ch4 reference-method 入口选择

> 来源: S001 | 产出位置: `.sessions/2026-08-08-ch4-reference-method-extension/R001-entry-selection.md`
> 日期: 2026-08-08
> 唯一文档: 执行方必须完整读取本文件；可读取本文件列出的本地证据，但不得自行扩大任务

---

## 0. TL;DR（执行方先读）

你在 worktree `D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`。Ch3 已有 CCISP 主方法，Ch5 已有 select-before-execute 工程方法；Ch4 仍缺一个真实方法章。

**你的任务**：只利用仓库现有论文、代码、历史 inventory 与结果，比较最多 3 个机制不同的 research object / reference baseline，推荐至多 1 个进入后续正式 Groundwork 的入口。

**产出**：`R001-entry-selection.md`；无论有无 survivor 均追加 D002，并更新 topic-index 与 registry current view，但本轮不得启动 Groundwork、检索、实现或仿真。

**最高纪律（违反一条就废了）**：

1. 候选必须从“可复现 reference baseline + 可观察/可复现 defect”出发，不从 supporting leftovers 反推方法名。
2. 最多比较 3 个对象，推荐至多 1 个；不得制造第 4 个候选补数量。
3. 廉价替代必须作为 comparator 进入后续实验；只有已有证据证明 exact existing-action collision，才允许入口期拒绝。
4. 基础设施工作量只作预算判断，不作科学 Kill；唯一胜者允许预计 3–7 天最小 testbed。
5. 本轮只做本地只读证据审计和入口裁决：不运行 `tools/search`、不下载/精读新论文、不改科学代码、不跑仿真、不进入 GW Step 1/4a。
6. `SUPPORTING_ONLY` / `REJECT` 不能关闭 Ch4，也不能继续消耗包装轮次。
7. 每个 research object 最多执行 2 个 method-bearing package；两个机制不同对象均无方法增量时，立即停止并交回用户作战略范围决策，不得自行开启下一对象或继续包装。

---

## 1. 背景（了解即可，不要在产出中重复复盘）

旧流程长期从内部残余资产、同一 caller 邻域和假想廉价替代出发，形成大量可信负面，却很少抵达可写方法。CCISP 成功时具备四个条件：可复现 baseline、实际缺陷、receiver-visible action、成熟 testbed。D001 因此冻结 reference-method extension：在 coherent FSO 总伞内改变 research object，先选 reference baseline，再复现 defect，只加入一个可部署动作，并与强传统 comparator 公平比较。

以下对象不得改名重开为 Ch4：

- P1 shared-M0 reuse（最多是 Ch5 内部优化）；
- decoder-feedback / extrinsic / syndrome / callback coded-chain 基建；
- CCISP selector threshold、region calibration 或同类标量调参；
- C3 adaptive segmented CPE；
- oversampled joint-sync Q1 当前实例；
- coded burst/interleaving 4b#1 当前实例；
- AMC Q-A/Q-B 当前实例；
- G1、P09 等已 invalidated artifact。

这些排除只阻止 exact object/action 复活，不得被扩大成“整个接收机/整个同步/整个编码方向都不能做”。

---

## 2. 任务详情

### 2.1 启动与恢复验证

开始前必须：

1. 读取本专题 `topic-index.md`、`decisions.md` D001、`H001-reference-method-entry-selection.md`；
2. 核对 `.sessions/_registry.yaml`：旧 RDL system 为 dormant，本专题为 active；
3. 回答防偏三问并写入 R001：
   - 当前工作是否直接产生或裁决一个方法？
   - 它是否是最小构造前不可缺的步骤？
   - 是否已触发“每对象 2 包 / 两对象失败”的停止条件？

任一恢复事实 FAIL，停止并报告，不自行修治理。

### 2.2 并行本地审计

允许最多 3 个 fresh-context subagent，并行承担以下互不重叠的只读任务：

1. **baseline/reproducibility**：从本地论文、代码和结果中找 1–3 个可复现 reference baseline，核实论文身份、实现/参数/runner 入口与重建成本；
2. **defect/action**：核实每个对象是否已有实际 defect 证据或可在最小复现中明确观察，并提出恰好一个 deployable action；
3. **collision/packaging**：核对历史 dead ends、exact action collision、合法 comparator，以及能否形成方法名、算法流程、主图、消融、复杂度和边界。

主线程只整合和裁决，不重新大规模通读全部历史。所有承重判断必须给 `file:line` 或精确路径；找不到证据就写 UNKNOWN。

### 2.3 候选入口门

每个候选必须逐项填写：

| 门 | PASS 标准 |
|---|---|
| G1 Reference identity | 有具体论文/权威方法名，不是内部 leftovers 的重新命名 |
| G2 Reproducibility | 本地已有 runner/实现，或最小重建预计不超过 3 天，并能在 3–7 天总预算内完成方法包 |
| G3 Observed defect | 有本地证据，或有明确、低成本、可证伪的 defect reproduction；不得用“没人做过”代替 |
| G4 One action | 恰好一个 receiver/deployment-visible action，非纯标量 retune、纯审计或计算记账 |
| G5 Fair comparator | 有目标 baseline 和最强廉价替代；廉价替代进入比较，不凭想象预杀 |
| G6 Chapter closure | 若后续结果成立，可自然产出方法名、流程/公式、主图/表、消融、复杂度与适用边界 |
| G7 Collision | 无已证实 exact existing-action collision；邻近工作或 generic prior art 只限制 claim，不自动 Kill |

只有 7 门全过才可推荐。若多个全过，按“defect 证据强度 > testbed readiness > action 区分度 > chapter closure > 预计工期”选唯一胜者。若无全过，terminal=`NO_ENTRY_SURVIVOR`，诚实停止，不追加候选。

### 2.4 本轮结束边界

- 选出胜者只代表 `SELECTED_FOR_GW_STEP1`，不是 Q#、Go、METHOD_SIGNAL 或方法成立。
- 不执行后续 Groundwork；下一轮必须新对话并重读 `stages/groundwork.md`。
- 不改 Skill、旧 dormant topic、科学代码、正式论文正文或 protected history。
- 只允许一次统一 commit，不 push；四个既有 `p05_run*.log` 不修改、不暂存。

---

## 3. 产出格式（强制）

`R001-entry-selection.md` 必须包含：

1. **恢复验证与防偏三问**；
2. **候选来源说明**：为什么只选这至多 3 个；
3. **候选对比总表**：reference、defect、one action、comparators、7 门、预算、证据指针；
4. **逐候选分析**：区分 FACT / INFERENCE / UNKNOWN；
5. **唯一推荐或 NO_ENTRY_SURVIVOR**；
6. **方法章最小成品预演**：仅对胜者列方法名占位、动作链、主图、消融、复杂度和边界，不设计具体算法；
7. **下一合法动作与禁止动作**。

如有胜者：新增 D002，terminal=`ONE_REFERENCE_METHOD_ENTRY_SELECTED_FOR_GW_STEP1`；无胜者：新增 D002，terminal=`NO_ENTRY_SURVIVOR_STRATEGIC_DECISION_REQUIRED`。更新 topic-index 与 registry current view，并由独立 fresh-context verifier 检查全部入口门和范围纪律。

最终回复只给五项：

1. terminal；
2. 至多 3 个候选及 7 门结果；
3. 唯一推荐与理由，或无 survivor 的具体缺口；
4. 是否形成方法、是否运行检索/实现/仿真；
5. R/D/V/H 路径、verifier、commit SHA。

---

## 4. 已知陷阱

- 不要因为 reference baseline 有 prior art 就否定扩展；要判断新增动作是否 exact collision。
- 不要因为需要几天 adapter 就判科学失败；先判断是否值得投入。
- 不要把“有代码”当 defect 证据，也不要把 oracle/headroom 当 Go。
- 不要选三个都来自 CCISP selector/CMA/CPR 同一局部邻域的伪多样候选。
- 不要为了保证有 winner 而降低入口门；本轮允许 `NO_ENTRY_SURVIVOR`。
- 不要把 entry selection 写成长篇 campaign 复盘；只保留影响选择的证据。

---

## 5. 验收

- [ ] 启动恢复三项事实和防偏三问已验证；
- [ ] 候选数 1–3，机制不同；
- [ ] 每个候选 7 门齐全且有证据边界；
- [ ] 至多 1 个推荐；
- [ ] 无 supporting leftovers 重包装或 forbidden object 复活；
- [ ] cheap alternative 被保留为 comparator；
- [ ] 未检索、未下载、未实现、未仿真、未进入 GW；
- [ ] 独立 verifier 与一次统一 commit 完成；
- [ ] p05 日志未触碰，未 push。

---

## 附：产出回传位置

- 主产出：`.sessions/2026-08-08-ch4-reference-method-extension/R001-entry-selection.md`
- 决策：同专题 `decisions.md` 的 D002
- 验证：同专题 `verifications.md` 的 V002
- 交接：如产生下一轮入口，新增 H002；无 survivor 则 H002 交回战略决策
