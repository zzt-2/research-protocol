# [S001] 过采样相干 FSO 同步前端 Step 1–2

> 2026-08-06 | Groundwork | 完成（D007/V005：Q1 survivor；Step 3.5 fulltext-blocked terminal；专题 closed）

## 目标

完成 Phase 0 authority reconciliation；执行 GW Step 1；若硬门通过则执行 Step 2，并停在用户覆盖面确认门。

## 记录

- 证据 worktree：`D:/code/study/research-protocol/.worktrees/rdl-method-production-v2`；起始 HEAD
  `0ac0119c4982b539c322b79773c563cafdbbd9a6`。
- 起始工作区仅有四个未跟踪 `p05_run*.log`，本轮禁止修改或暂存。
- 注册表查重未发现同名或同研究对象 active/dormant 专题；建立本专题。
- Phase 0 已依据 T004 commit `1140134e...`、T005 commit `67970307...` 与 D023 修订
  `internal-method-kernel-inventory.yaml`：2A=`REJECT`；2B=`SUPPORTING_ONLY`，其中 scheduling
  是 CCISP 既有 select-before-execute 动作的部署证据，Q(8,6) 仅保留支持性负面边界。
- 2026-08-06 11:45 的阶段快照：当时执行 GW Step 1，尚未进入 Step 2；随后进展见下列记录。
- GW Step 1 使用 6 组 query，得到 140 raw / 130 unique，2019+ 39 unique；形成 Q1 sample-level
  acquisition 与 Q2 fade+SCO maintenance/reacquisition 两张机制不同预卡，六个停止条件均未触发。
- 静态 BOM：完整对象 11–14 日；Q1 acquisition slice 5.5–7.5 日；Q2 maintenance slice 7–9 日。
  两个最小切片都不是完整通信平台重建，未触发工程停止门。
- GW Step 2 首轮核验 6 篇 CORE；独立 V001 因最近直接竞品角色缺失判 FAIL。定向补证后，JLT 2025
  官方 arXiv 全文成为第 7 篇 CORE；JOCN 2026 三路径失败，保留为用户确认的高风险缺口。
- 7 篇 CORE 均完成 identity、provenance、SHA256、≥50 行与非拦截页检查；未获取文献未用摘要替代
  exact collision 判断。
- 当前 terminal=`STEP2_READY_FOR_USER_CONFIRMATION`；未进入 Step 3、Step 3.5、Step 4a、代码或仿真。

## 决策引用

- D001：冻结新研究对象与 Step 1–2 边界（新建）
- D002：接收 Step 1 gate 与 Step 2 覆盖，停在用户确认门（新建）
- D003：补齐最近直接竞品后重裁 Step 2（新建；取代 D002）

## 范围确认

- 本轮是否在 scope boundary 内：是（承接 RDL system D028 的显式 research-object scope change）

## 后续

- 用户已接受 7 篇 CORE 与 JOCN 2026 高风险缺口，D004 解除 Step 3 禁令。
- 本轮通过子 agent 精读 7 篇 CORE；Q1/Q2 分开形成 M-C-A 和四判据表。
- 只有至少一个 Q# 全过才执行 Step 3.5；Step 3.5 完成后停止，不进入 Step 4a、实现或仿真。

## 2026-08-06 续接：Step 3 / Step 3.5

### 目标

完成 7 篇 CORE 全文精读与 Q1/Q2 canonical 四判据裁决；仅对 survivor 执行有界 Step 3.5。

### 记录

- 起始 HEAD：`50b4b474f822e253f02ad44fd47ba37afea6dddf`；四个 `p05_run*.log` 仍为唯一未跟踪项并受保护。
- Handoff 事实核验：7 篇 CORE、JOCN 2026 三路径失败、`STEP2_READY_FOR_USER_CONFIRMATION` 均由
  `step2-coverage-report.md`、V003 与实际 HEAD 交叉确认。
- D004 已登记本轮 scope change；精读与检索结果待追加。
- T001–T003 已完成 7 篇 CORE 全文精读，结构化产出位于
  `projects/thesis-fso/worker-logs/step-3-sync-read-{a,b,c}.md`，并沉淀为 7 份全局 read notes。
- Q1 判据 1 FAIL：GEO 2023 已给出 2-sps timing/SCO→frame→CFO 完整顺序链，而 CORE 未证明其
  在目标条件下失效；共享 preamble/调序不构成已证实 joint action。
- Q2 判据 1、3 FAIL：没有共同失锁或 shared-freeze+fixed-restart 不足的正文证据，也没有 2019+
  integrated maintenance comparator。
- survivor=0，D005 固定 terminal=`STEP3_NO_VALID_PROBLEM`；Step 3.5 条件门未触发，JOCN 2026
  未重抓，仍为 `UNRESOLVED_HIGH_RISK`。
- 独立 verifier 初审发现 4 个交付/状态阻断项；最小修复后 V004 完整复验 PASS，T004 九项全过，
  阻断项 0。H001 已完成，专题转 `closed`。

### 决策引用

- D004：接受 7 篇 CORE 并授权 Step 3→条件式 Step 3.5（新建）
- D005：Step 3 无 canonical survivor，禁止触发 Step 3.5（新建）

### 范围确认

- 本轮是否在 scope boundary 内：是（用户显式授权，见 D004 与 topic-index 范围变更记录）

### 后续

- 无。后续只有用户显式 scope-change 才能重启；不自动继续研究动作。

## 2026-08-06 续接：D006 语义纠偏与 Step 3.5

### 目标

纠正 D005/V004/H001 的 semantic-gate misapplication；按 canonical glossary 重判 Q1/Q2，并对 survivor
执行最多三轮 Step 3.5。完成后停止，不进入 Step 4a、实现、testbed、MVE 或仿真。

### 记录

- 起始 HEAD：`6874249530928616c13aa5a6107bc55d08fae939`；四个 `p05_run*.log` 仍为既存未跟踪
  protected paths，SHA 与内容不得修改。
- 逐字复核 `glossary.md` L22-31、`gw-read.md`、`gw-supplement.md`、AMC D005、formal D004/D005、
  Step 3 report、literature notes 与 H001，确认 D005 把 Step 4a/MVE 的 problem-truth 责任前移。
- D006 取代 D005 的 terminal 与 Q1/Q2 判据 1：Q1 四判据 PASS，成为唯一 survivor；Q2 仅判据 3
  FAIL，不能用 Gu/Paillier/Valjus 跨论文拼接 integrated baseline。
- T005–T007 已派发：分别执行系统关键词矩阵、Sun 双向引用链+JOCN 有界获取、Q2 baseline 独立裁决。

### 决策引用

- D006：Step 3 canonical 语义门纠偏并启动 Q1 Step 3.5（新建；部分取代 D005）

### 范围确认

- 本轮是否在 scope boundary 内：是。用户显式重开，且 current scope 原已包含 survivor 后的有界 Step 3.5。

### 后续

- 等待 T005–T007 产出；对新高相关论文执行 acquire→read；完成后写 Step 3.5 terminal、独立 verifier 与 H002。

### Step 3.5 收口记录

- T005 Round 1 完成 6/6 query，80 unique、must=5/should=6；T011 Round 2 完成 3/3 query，25 unique，
  真正新增 must/should=0，达到收敛门，未启动 Round 3。
- T006 完成 Sun 2025 双向引用链：forward=8、backward=35；JOCN 2026 有界获取仍失败。
- T008–T010 对新增高相关论文执行 acquire→read：Zhou 2025 为分区 preamble 顺序链；LPT 2017 为
  joint integer frame+CFO、无 fractional τ；JLT 2021 为 joint τ+CFO+CPO、无 frame；均非 exact collision。
- JOCN 2026 与 JLT 2025 IQ-skew 无全文，exact-action novelty closure 继续 blocked。
- D007 固定 terminal=`STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED`；Q1 保留
  survivor，Q2 仅判据 3 FAIL。未进入 Step 4a、实现、testbed、MVE 或仿真。

### 决策引用（收口）

- D007：完成 Q1 Step 3.5 并冻结 exact-action 全文 blocker（新建）

### 后续（收口）

- fresh-context verifier 初审发现 literature notes 两处 stale-current，主控仅修这两处；同一 verifier
  全量重跑后 semantic/deterministic 均 PASS、blocker=0，登记为 V005。
- H002 已写入并取代 H001；专题以
  `STEP3_5_COMPLETE_Q1_SURVIVOR_EXACT_ACTION_FULLTEXT_BLOCKED` 关闭。处理两个全文缺口前无 Step 4a 入口。

## 2026-08-06 续接：用户提供 JLT 2025 全文

### 目标

只处理 D007 的两个 primary-fulltext blocker：对用户提供的 JLT 2025 IQ-skew PDF 执行 acquire→read；
按用户访问结果处置 JOCN，不进入 Step 4a、实现或仿真。

### 记录

- 用户 PDF identity PASS：10 页、1,945,015 bytes、DOI/标题一致；source SHA256=`0a5c8865...311d`。
- `tools/convert` 的 Windows CRLF wrapper 直接失败；未改工具文件，以只读去 CR 运行同一 wrapper，
  产出 canonical content 344 行、SHA256=`56dd39ff...93b1`；10 页渲染目视可读。
- T013 fulltext read：shared TS-A 顺序执行 frame detection/IQ-skew/SOP/timing/FOE，TS-B 再做 frame
  synchronization/channel estimation；Eq. 16–23 的 IQ-skew tone/Godard estimator 不含 frame/timing/CFO
  共同 objective。verdict=`NO_EXACT_Q1_COLLISION_SHARED_PREAMBLE_SEQUENTIAL_OR_EXTRA_ACTION`。
- 用户明确“我拿不到就是拿不到了”且只取得 JLT；JOCN 记为 `USER_CONFIRMED_FULLTEXT_UNAVAILABLE`，
  停止重试但保留 scientific coverage limitation。
- D008 更新 terminal；H003 成为下一恢复入口。本轮未进入 Step 4a、实现、testbed、MVE 或仿真。

### 决策引用

- D008：接收用户提供 JLT 2025 全文并关闭 coverage-decision gate（新建）

### 范围确认

- 本轮是否在 scope boundary 内：是；属于 D007/H002 明确列出的 USER_FULLTEXT_PROVISION/coverage decision。

### 后续

- 独立 V006 已 PASS、blocker=0；专题维持 closed。下一合法动作仅为新会话 Step 4a preflight
  discussion。
