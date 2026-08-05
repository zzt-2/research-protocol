# Topic Index: Shared M0-Power FOE–CPE Groundwork (Step 1–3)

> 状态: closed | 创建: 2026-08-05 | 最后更新: 2026-08-05（bounded closure；terminal=`RECENT_BASELINE_UNAVAILABLE`；D005；V005 PASS；H003）

## 专题信息

- **slug**: `2026-08-05-shared-m0-foe-cpe-groundwork`
- **title**: 共享 M0 次幂 FOE–CPE 计算图正式 Groundwork（Step 1–3）
- **性质**: 派生专题。承接 RDL system 专题 T008 / S015 / D024 / CP005；已完成 GW Step 1–2，
  D002 授权后执行 Step 3，并停在 Step 3 terminal。

## 范围边界

### 原始目标（冻结，来自 T008）

> 判断共享 M0 次幂 FOE–CPE 计算图是否构成有文献空间、真实成本动作和可验证传统对手的
> Ch5 工程方法候选。

### 当前范围

- 保留已验收的 GW Step 1 检索与 Step 2 全文获取/覆盖面门产物；
- 执行 GW Step 3：fresh-context 子 agent 全文精读至少 6 篇 HIGH/MEDIUM 论文，优先关闭
  CSNDSP 2014 与 JLT 2018 两篇直接竞品；主线程汇总七子表、baseline、复杂度、实验完备性、
  M-C-A 问题与 canonical 四判据；独立 fresh-context verifier 终审；
- 写入项目 literature notes、全局 read notes、本专题 read-log、治理 D/V/H；
- 单次统一 commit，不 push；四个既有 `p05_run*.log` 不修改、不暂存。
- 执行最后一次 bounded evidence closure：最多 6 组 query，OFC 2016 一手获取与最多 5 篇 2019+
  task-matched baseline；仅对有效全文做 targeted read，关闭 Q-P1-01 后停止。

### 明确不含

- 不进 GW Step 3.5 / 4a；不实现、不仿真、不跑 MVE、不写论文 claim；
- 不改 `.agents/skills/`、`projects/simulation/common/`、`params.py` 或既有算法；
- 不重开 P2–P5、T006 C3、P09、G1、AMC 或 dormant campaign；
- 不用 oracle/headroom 决定 Step 1–2 的 Go；
- 不把"没人题名相同"写成 novelty，不把一行实现或输出等价自动写成 rejection；
- 不创建实验合同、代码 sandbox、raw 仿真结果或论文图；
- 不宣布 `THESIS_METHOD_READY`、METHOD_SIGNAL、Go/Kill 或 active carrier；
- 修改 NDA-ML 估计器统计触发既有 `NDA_ML_BODY_REOPEN`，不属于本候选。

### 范围变更记录

- **[2026-08-05] D002**：在 Step 2 已由 V002 验收后，将当前范围从 GW Step 1–2 扩展到仅执行
  GW Step 3 精读。
  - 原因：用户在新对话显式授权 P1 Shared M0-Power FOE–CPE Groundwork 的 GW Step 3。
  - 新范围：全文精读、结构化汇总、直接竞品 collision、传统 comparator/action delta、Q# 四判据、
    独立 verifier 与 Step 3 terminal；仍禁止 Step 3.5/4a/Contract/实现/仿真。
  - 影响的未决项：允许关闭原未决项中的 joint FOE/CPE 数据流、显式共享动作、合法 comparator、
    matched-output 与复杂度证据；不授权其后的 Go/Kill 或实验判断。
- **[2026-08-05] D005**：用户授权最后一次 bounded `gw-search→gw-acquire→gw-read` 证据闭合。
  - 变更内容：冻结 6 组 query 上限，只处理 OFC 2016 exact boundary 与 2019+ task-matched baseline；
    仍禁止 Step 3.5/4a/实现/仿真。
  - 原因：关闭 D004/H002 的两个证据债务并给出 terminal；不是重开开放式检索。

## 已确认结论

### 不变量

- **冻结研究对象（仅用于检索/获取，不作为 Step 3/4a 结论）**：
  - **M**：当前串行 NDA carrier recovery 先用 M0 次幂做 FOE，再对 CFO 补偿信号重做 M0 次幂做 CPE。
  - **C**：资源受限的软件或硬件实现，要求与当前 receiver 输出/BER 匹配。
  - **A**：用一个共享 M0-domain 表示同时驱动 FOE 与 CPE；升幂域 CFO 去除必须使用
    `raised * exp(-j*M0*omega*k)`，最终在原信号域补偿 `omega*k + phi`。
- **P1 当前层级 = `THESIS_ENGINEERING_COMPONENT` 设计候选**（来自 D024），不是 METHOD_SIGNAL。
- **D005 最终层级 = `SUPPORTING_ONLY`**；`THESIS_ENGINEERING_COMPONENT` 仅为进入本专题时的历史层级，
  不再作为 active carrier 或后续执行授权。
- **廉价吸收判据**：必须在实际执行路径或工具链中存在；假想 compiler/CSE 不算。
- **Step 2 覆盖面门必须用户确认**：terminal 只能是 `STEP2_READY_FOR_USER_CONFIRMATION` /
  `STEP2_BLOCKED_BY_COVERAGE_GAP` / `ENTRY_INVALID`，或经独立 fresh-context 验收（V### PASS）后升级为
  `STEP2_ACCEPTED_READY_FOR_STEP3`；均不得自动进 Step 3（Step 3 启动须用户新对话显式授权）。
- **区分显式共享 vs 改估计器统计**：后者触发 `NDA_ML_BODY_REOPEN`，不属于本候选。

### 其他结论

- **统计口径（实测，来源 `search-archive/2026-08-05/_r1_merged_shortlist.json`）**：raw=100，dedup=97；
  实际贡献候选的 API 源 3 类（Semantic Scholar / OpenAlex / SerpAPI-scholar），4 查询通道均调用但
  Exa 贡献 0；publication_status = published 59 / unknown 36 / preprint 2；**可直接证明的正式发表率
  下限 = 59/97 = 60.8%**（通过 ≥50% 门）。
- **Step 2 覆盖面已验收（V002 PASS）**：12 篇合格全文（12/12 identity/≥50 行/SHA256 全过），含
  2 篇 HIGH★ 直接竞品（CSNDSP 2014 method-level、udWDM-PON 2018 implementation-level）。无需再补
  直接竞品全文；剩余 Optica/SPIE/MDPI 失败项为中等/低相关，非阻塞。
- **Step 1–2 级不做方法/数据流/竞品全文语义结论**（属 Step 3，未授权）。"metadata 级未发现明确覆盖"
  不得当作新颖性证据。
- **Step 3 直接竞品裁决（D003）**：CSNDSP 2014 不是 same-sequence sharing；JLT 2018 已实现
  shared correlation，并记载 OFC 2016 已共享 m-th power。generic P1 action 已 collision。
- **P1 窄 delta/层级**：仅余 raised-domain CFO-removal/lifetime + matched-output 候选；最多保持
  `THESIS_ENGINEERING_COMPONENT`，不能作 novelty/Go/Kill。
- **Q-P1-01**：canonical 判据 1/2/4 PASS、3 FAIL（缺 2019+ task-matched recent baseline）；无合法
  Q# 时必须停留在 Step 3，不能使用自造 terminal（D004）。
- **Bounded closure（D005/R002）**：6/6 query + 引用链 + 全局索引严格复筛为 0 篇合格 recent
  baseline；OFC exact action=`UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`；terminal=
  `RECENT_BASELINE_UNAVAILABLE`，P1=`SUPPORTING_ONLY`，专题关闭。

## 进展线索

- **S001**：Phase A 建专题 + Phase B Step 1 检索（raw=100 → dedup=97，4 查询通道均调用、实际贡献
  候选 API 源 3 类 S2/OpenAlex/SerpAPI（Exa 贡献 0），published 59/unknown 36/preprint 2，正式发表率
  下限 59/97=60.8%，3 语义类全覆盖，门槛全过）+ Phase C Step 2 获取/覆盖面门（**12 篇合格全文**，含
  2 篇 HIGH★ 直接竞品；blit 第三轮补取 7 篇 IEEE；V001 PARTIAL→V002 PASS 后
  terminal=`STEP2_ACCEPTED_READY_FOR_STEP3`）。H001 已交接。
- **D001**：冻结研究对象与范围边界（本专题新建，依据 T008/D024）。
- **D002**：显式授权仅执行 GW Step 3。
- **R001**：九篇精读、直接竞品、comparator、action delta 与 Q# 综合。
- **D003**：generic action collision；P1 无合法 Q#；Step 3 partial terminal。
- **V003**：初版 verifier FAIL；科学主结论 PASS，但笔记结构/终态/治理 FAIL。
- **D004**：撤销自造 terminal，Step 3 保持 BLOCKED/IN PROGRESS。
- **V004**：修复后 fresh-context 终审 PASS（9 篇、135/135 字段、72/72 规范段落）。
- **H002**：交接无合法 Q# 的 blocked 状态与回 search 恢复路径。
- **R002**：最后一次 bounded search/acquire/read 证据闭合；Q-P1-01 仍为 1/2/4 PASS、3 FAIL。
- **D005**：触发 `RECENT_BASELINE_UNAVAILABLE`，P1 降为 `SUPPORTING_ONLY` 并停止该方向。
- **H003**：closed-state handoff；下一轮回上游 RDL 轮换机制不同的新候选，不得改名重开 P1。
- **V005**：bounded closure fresh-context 复验 PASS；六 JSON、acquire、三篇全文、Q/terminal、治理与 git 边界全过。

## 未决项

- OFC 2016 一手全文与 exact implementation boundary 仍是覆盖缺口；因本专题已触发冻结预算硬停止，
  该缺口只作历史证据边界，不再触发继续检索或 P1 重开。
- 下一轮由上游 RDL 轮换机制不同的新候选；不在本专题改名复活 P1。

## 当前位置

GW Step 1–2 已验收；原 Step 3 九篇精读由 V004 结构复核 PASS。最后一次 bounded closure 已执行
`gw-search→gw-acquire→gw-read`：6/6 query 用尽，OFC/PTL 未取得有效全文，三篇 recent 有效全文均
非 task-matched，合格 2019+ baseline=0。Q-P1-01 仍为 1/2/4 PASS、3 FAIL，terminal=
**`RECENT_BASELINE_UNAVAILABLE`**；P1=`SUPPORTING_ONLY`，专题 closed。

**P1 的 generic action 已碰撞，窄 delta 未形成合法 Q；停止该方向，下一轮轮换新候选，不再改名重开。**

> **修订**（2026-08-05）：① Step 2 初版误判 blit 跳过 IEEE 第三轮通道（用户纠正），补跑 blit 后取回
> 7 篇高优先 IEEE 全文（含 2 篇最高优先直接竞品），合格全文 5→12 篇。② T008 acceptance repair
> （V001/V002）修正统计口径（raw/dedup、3 API 源非 4、正式发表率下限 60.8% 而非 ~97%）、降级 novelty
> 倾向措辞、清除残留 stale "5 篇/补两篇/手动获取"口径，详见 S001 acceptance repair 段与
> `verifications.md` V001/V002。终态由 `STEP2_READY_FOR_USER_CONFIRMATION` 升级为
> `STEP2_ACCEPTED_READY_FOR_STEP3`。
