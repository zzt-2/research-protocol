# 验证记录

## V001：GW Step 1 检索与 collision 综合终验

- 日期：2026-08-11
- 关联：S001 / D001 / R001 / T003
- 验证方：fresh-context child verifier（与作者/两路初筛分离）
- 状态：PASS
- 严重度：P0/P1/P2=`0/0/0`

### 验证对象

- q1–q6 原始 JSON、search receipt、27-entry candidate/collision matrix。
- R001 synthesis、provenance receipt、topic/decision/master-state 控制面。
- registry/master-state/topic diff 与 Step 1 scope。

### 验证结果

| 组 | 结论 | 独立证据 |
|---|---|---|
| A counts/sources | PASS | `0+18+50+48+22+31=169`；DOI/title unique=`157`；matrix 27、24 formal+3 unknown、8 must-read；贡献源仅 S2/OA/Tavily。 |
| B identity/provenance | PASS | 2019 行 10860 SHA=`9c35292e...651e4e8`；Geisler 行 15493 SHA=`3d26dd2f...7bddfab4`；Johst/Wang 边界与 OFC 错配隔离成立。 |
| C collision/terminal | PASS | hard 与宽泛 soft 先例已降 comparator/neighbor；2019 direct exact=`UNRESOLVED`；未写 novelty PASS；terminal 被接受。 |
| D scope/diff | PASS | Step 2=`NOT_AUTHORIZED`；未下载、精读、实现、仿真、smoke 或修改 b3/coded topic。 |

### 失败与修复血缘

第一次 fresh 终验为 `FAIL 0/1/1`：专题未绑定既有全局索引的 2019/Geisler 记录，且 receipt 残留“26 项”。唯一窄修新增 provenance receipt、绑定两行哈希并修为 27；未新增 query。第二个 fresh context 在最终文件上给出 `PASS 0/0/0`。

### 结论

`STEP1_PASS_READY_FOR_STEP2_CONFIRMATION`。该结论只接收 Step 1 检索质量和后续获取必要性；Q#、Go/Kill、METHOD_SIGNAL、method/thesis delta 均未产生。

## V002：GW Step 2 acquisition 与 coverage 终验

- 日期：2026-08-11
- 关联：S002 / D002 / R002 / R003 / T006
- 验证方：fresh-context child verifier（与获取/转换执行分离）
- 状态：PASS
- 严重度：P0/P1/P2=`0/0/0`

### 验证对象

- 四篇 claimed qualified 的 canonical/shared-root source/content 与 metadata。
- 五篇 claimed unavailable 在 worktree、共享根、canonical DOI、downloads/manual 的可验证资产。
- R002/R003/topic-index/master-state/registry 的 coverage 数字、terminal 与 scope。
- 本轮 diff、git staging 与 unrelated dirty files 的隔离。

### 验证结果

| 组 | 结论 | 独立证据 |
|---|---|---|
| A identity/hash/lines | PASS | WiSEE 2024、Wang 2023、ICCC 2022、JPHOT 2020 的 bytes/SHA/总行/非空有效行与 R003 全部一致；标题/DOI 闭合。 |
| B content quality | PASS | 四篇反爬文本命中 0；前三篇 U+FFFD=0；JPHOT 2020 的 39 个替换符仅分布在 18 行公式符号，未构成大面积乱码。 |
| C unavailable/coverage | PASS | 五篇均无 target source/content；P0 仍 unavailable。targeted qualified=`4/9`，optical CORE=`2/5`，ICCC/JPHOT 2020 未被计入 CORE。 |
| D terminal/control plane | PASS | R002/R003/topic/master/registry 一致：`STEP2_BLOCKED_CRITICAL_DIRECT_COMPETITOR_FULLTEXT`；Step 3=`NOT_AUTHORIZED`。 |
| E scope/diff | PASS | 无正向动作签名、碰撞裁决或后续科学门产出；无实现/仿真/b3 repair；staging 为空，unrelated dirty files 未纳入。 |

### 结论

接受 Step 2 acquisition/coverage 终态。下一合法动作只有用户手动补 P0 后重跑 Step 2 gate，或用户显式接受 coverage/claim limitation 并另行授权 Step 3；当前不得继续。

## V003：GW Step 2 repair 与 Step 3 全文综合终验

- 日期：2026-08-11
- 关联：S003 / D003 / D004 / R002–R004 / T007–T010
- 验证方：independent fresh-context verifier（未参与本轮五篇精读与主线综合）
- 状态：PASS
- 严重度：critical/major/minor=`0/0/0`

### 验证对象

- JLT 2023 replacement CORE 的 identity/hash/lines 与 Step 2 qualified=5。
- 五篇 title gate、15+字段、7结构段、通信参数、实验完备性与三篇写作架构。
- direct-competitor action matrix、Q001 M-C-A/四判据、2019 exact-action limitation。
- 五篇 read-note source/persistence/casing 链、read-log/topic/master/registry 与 scope。

### 验证结果

| 组 | 结论 | 独立证据 |
|---|---|---|
| A Step 2 repair | PASS | JLT source/content bytes、SHA、270/114 行与 R003 一致；五篇均为真实 qualified fulltext，2019 未计全文。 |
| B read structure | PASS | 五篇各 title gate + 15/15 fields + 7/7 sections + communication params + completeness；Wang/Liu/Johst 有三份 writing architecture。 |
| C action matrix | PASS | 2019 broad unknown、Liu estimator-changing、Johst hard discard、Tu known-OSNR admission、Yang pilot soft weight、Wang branch-local DSP→MRC 的位置边界一致。 |
| D Q001/collision | PASS | Q001 收窄到 Wang 实证的 branch-local FS/phase-correction→MRC 边界后 4/4 PASS；完整 post-all-FS/CE/CPE 版本与 2019 exact action 留作 Step 3.5 debt。 |
| E persistence/scope | PASS | 五篇 canonical notes 均在 `git ls-files`，五个 source path 均存在；diff checks 通过；scope violation=0。 |

### 失败与修复血缘

首验=`PARTIAL 0/2/0`：①把 Wang MRC 错写成所有独立 DSP 后，criterion 3 baseline 位置不匹配；②Wang source 指针无效，四个新 notes 尚未持久化。bounded repair 将 Q001 改到原文真实 pre-MRC branch-local 边界，把更宽 post-all-FS/CE/CPE 版本降为 Step 3.5 debt；同时修绝对 source path、统一 lowercase canonical note path并 force-add。repair verification=`PASS 0/0/0`。

### 结论

接受 terminal=`STEP3_Q_SURVIVES_READY_FOR_STEP3_5`，仅针对收窄的 branch-local Q001。这是 Step 3 problem-survival，不是 novelty closure、Go/Kill、METHOD_SIGNAL 或 Step 3.5 授权。

## V004：GW Step 3.5 exact-action closure 终验

- 日期：2026-08-11
- 关联：S004 / D005 / D006 / R005 / T011–T016
- 验证方：independent fresh-context verifier（未参与检索、获取、全文精读或主线综合）
- 初验状态：PARTIAL
- 初验严重度：critical/major/minor=`0/1/2`

### 初验结果

| 组 | 结论 | 独立证据 |
|---|---|---|
| A counts/sources | PASS with minor | 8+7+6 official receipts 存在；45/121/4 unique 可复算；整体 S2+OpenAlex 实际贡献；provider-raw 115/6 仅存 worker stdout receipt 表。 |
| B identity/action | PASS | Zhang title/DOI/SHA/lines 闭合且为 estimator-changing neighbor；Sun/Xie/Chen/Qiu/Li 无 primary fulltext，unknown 字段未被脑补。 |
| C terminal | PASS | 无 confirmed exact collision，但 Xie/Qiu 等承重 direct action 未闭合；`EVIDENCE_BLOCKED` 符合 D005，非 Kill/novelty/METHOD_SIGNAL。 |
| D scope | PASS | Step 4a/implementation/simulation/method design=0；broader post-all-FS/CE/CPE 保持 excluded。 |
| E control plane | PARTIAL | V004 尚未形成是唯一 major；owner 有两处 Step 3 陈旧措辞。 |

### Bounded repair

- 创建本 V004，闭合 H004/控制面血缘。
- R005 显式登记 provider-raw stdout-only 的可复现性限制，不把 46/4 retained JSON 冒充 115/6 provider raw。
- literature owner 将“Step 3 未授权”修为 Step 3.5，并把 Sun-only limitation 扩为 Sun/Xie/Qiu bearing debts。
- 未重开搜索、改变 terminal、进入 Step 4a 或修改代码。

### Final check

T016 fresh follow-up final verdict=`PASS`，critical/major/minor=`0/0/0`。三项 bounded repair 全部闭合；科学 terminal 保持 `EVIDENCE_BLOCKED`，Step 4a 继续 `NOT_AUTHORIZED`。本 PASS 只接收证据与治理闭合，不产生 collision/non-collision、novelty、Kill 或 METHOD_SIGNAL。

## V005：GW Step 4a defect smoke 独立终验

- 日期：2026-08-12
- 关联：S005 / D007 / D008 / R006 / commit `cbb8a2d`
- 验证方：independent fresh-context verifier（未参与 test 分批运行、合并或主线裁决）
- 状态：PASS
- 严重度：critical/major/minor=`0/0/1`

### 独立验证结果

| 组 | 结论 | 独立证据 |
|---|---|---|
| chronology/freeze | PASS | Commit 1=`cbb8a2d` 在首个 held-out batch 前；receipt=`test_started=false`，七项 hash 与冻结源码/dev 资产一致；test 后未调参。 |
| raw/schema/pairing | PASS | 五 part hash 与 metadata 一致；merged raw SHA=`eb964eee...`，12600 rows=`5400 branch+7200 method`，100 seeds×18 cells=`1800` exact pair/hash；仅 B0/B1=-8/B2=L=K/O1。 |
| information boundary | PASS | 43 tests；递归 AST reachable clean；固定 RX 翻转全部 truth 字段后 B0/B1/B2 features/subset/no-valid/complex output bit-exact。 |
| raw recomputation | PASS | G1=`3.1111% [2.3333%,3.9444%]`；G2 regret=`0.1114% [-0.3785%,0.4947%]`、outage=`0`；G3/G4 与发布 aggregate 一致。 |
| terminal/claim | PASS | first fail-stop=`PROBLEM_ABSENT_OR_TOO_SMALL`；不恢复 problem-bearing candidate，novelty debt preserved，无 soft method/METHOD_SIGNAL。 |

### Minor limitation

冻结源码的 direct strict aggregate caller 把 `expected_cells` 作为 one-shot generator 传入，导致 coverage validator 在第一 seed 后耗尽。官方聚合仅用 process-local adapter 将 iterable 物化为 tuple；未改 raw、frozen、metric、bootstrap、源码或 receipt。独立 verifier 以同一 raw 独立重算完全吻合。该复现限制记录在案，不为修复它改写已冻结合同或 scientific result。

### 结论

接受 D008 与唯一 terminal。此次 PASS 是证据接收 PASS，不是科学门 PASS；Q001 scientific result 为 negative，`mission_method_delta=NONE`。
