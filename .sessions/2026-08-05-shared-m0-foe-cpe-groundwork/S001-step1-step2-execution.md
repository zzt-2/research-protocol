# [S001] P1 Shared M0-Power FOE–CPE Groundwork Step 1–3 执行

> 2026-08-05 | GW Step 1–2 | 完成（terminal=STEP2_ACCEPTED_READY_FOR_STEP3，T008 acceptance repair 后）
> 2026-08-05 续接（acceptance repair：V001 初审发现统计口径/措辞缺陷，V002 独立复核 PASS 后终态升级）
> 2026-08-05 续接（D002：用户显式授权仅执行 GW Step 3；V003 FAIL 后 BLOCKED/IN PROGRESS）
> 2026-08-05 续接（修复完成；V004 独立复核 PASS；科学状态仍 BLOCKED/IN PROGRESS）
> 2026-08-05 续接（D005：最后一次 bounded evidence closure；terminal=`RECENT_BASELINE_UNAVAILABLE`）

## 目标

执行 T008 的 GW Step 1–2；在 D002 新授权下续接 GW Step 3；在 D005 用户授权下仅执行最后一次
bounded `gw-search→gw-acquire→gw-read` 证据闭合。全程不进 Step 3.5/4a，不实现、不仿真、不跑
MVE、不写论文 claim。

## 记录

### GW Step 3 续接：接收验证与范围门（D002）

- 按 H001 完成接收方验证：12/12 `content.md` 均 ≥50 行且 qualified；12/12 PDF SHA256 重算与
  `_step2_receipt.json` 一致；`_r1_merged_shortlist.json` 重算 raw=100、dedup=97、published=59、
  unknown=36、preprint=2、Exa=0、实际 API 家族 3 类。依赖专题均 active，`conflicts_with=[]`。
- 初次 receipt 复核脚本把顶层 JSON 数组误当对象属性读取，输出无效；已废弃并改用
  `ConvertFrom-Json -NoEnumerate` 重新逐条核对，最终三项均 PASS。
- 用户新对话显式授权 Step 3；依 session-governance 记录 scope change 与 D002。当前仅允许精读、
  综合裁决、独立 verifier 和治理收尾，不允许 Step 3.5/4a/Contract/实现/仿真。

### 报到与门控

- 完整读取 T008 任务书 + RDL Skill/method-production + session-governance + stages（groundwork/
  gw-search/gw-acquire）+ glossary + thesis-lessons TL-22/30/31/32/33 + system topic-index（控制块
  epoch16/CP005/D024）+ P1 卡 + 4 个 caller + registry。
- task-control validator **PASS**（`validate_task_control.py T008...` → PASS）。
- caller-path 复核确认 P1 事实：`rx**M0` 真实两次（`sc_nda_ml_sim.py:150` FOE；`_recovery.py:213/243`
  CPE），route-A `run_ccisp_family1_selector_a_30seed.py:24-31` 与 route-B
  `_a4_branchrouted_30seed.py:138-148` 均串行双调用，无 JIT/CSE 证据。

### Phase A — 新建 Groundwork owner（D001）

- registry 查重：无同方向 active/dormant formal Groundwork owner；新建
  `.sessions/2026-08-05-shared-m0-foe-cpe-groundwork/`（topic-index + decisions.md D001 + voice.md）。
- 项目 owner：`projects/thesis-fso/literature_notes_shared_m0_foe_cpe.md`（GW 进度 + Step 1–2 状态，
  无伪造精读条目）+ `projects/thesis-fso/shared-m0-foe-cpe-groundwork/step2-coverage-report.md`。
- D001 冻结研究对象（M/C/A）+ 记录 caller-path 已知事实 + 未知项。

### Phase B — GW Step 1 检索（✅ 门槛全过）

- 全局索引复用筛选（Explore agent 扫 21k 行 `all-papers.jsonl`）：3 语义类 ~35 命中，含 3 篇
  HIGH-RELEVANCE（udWDM-PON 2018 shares-correlation、LUT-Free DPSK 2019、CSNDSP 2014 VV-monomial）。
- 4 个 `tools/search` 定向查询通道（VV/Mth-power/FF-joint、joint-CFO-CPE-lowcomplexity、hw-efficient-CPR、
  fso-sat-coherent-carrier，各 2 个子 agent 执行）：**raw=100 → dedup=97 候选**。实际贡献候选的 API 源只有
  3 类（Semantic Scholar / OpenAlex / SerpAPI-scholar），Exa 贡献 0；4 查询通道均被调用。
  publication_status = published 59 / unknown 36 / preprint 2；**可直接证明的正式发表率下限 = 59/97 =
  60.8%**（通过 ≥50% 门）。unknown 项不作"已发表"计入。必读 ≥12，3 语义类全覆盖。
- Class 2 generic（"common subexpression / computation reuse / compute graph"）：当前 metadata/abstract
  检索未发现明确覆盖；**不得据此判断新颖性，须由 Step 3 全文精读验证**。
- Step 1 产出：`search-archive/2026-08-05/_p1-competitor-shortlist.md`（直接竞品初筛矩阵，
  metadata/abstract 级，不当精读结论）+ `r1-*.json` + `_r1_merged_shortlist.json`。

### Phase C — GW Step 2 获取/覆盖面门（✅ 12 篇合格，terminal=STEP2_ACCEPTED_READY_FOR_STEP3）

- 选 12 篇必读/建议读做 `tools/download --dry-run` → 多轮获取：
  - Round 1（batch shortlist）：2 成功（LUT-Free DPSK 2019、Single-Carrier DSP 2009）。
  - Round 2（直接 `--doi` + OA+pdf_url 重试）：3 成功（Frontiers FSO 两阶段、Atlantis CPE 16QAM、
    eLight platicon）。
  - **Round 3（blit-ieee 校园网，用户纠正后补跑）**：7 成功（CSNDSP 2014、udWDM-PON 2018、
    TSP 2021、PTL 2016、ISCAS 2022、CL 2026、PhotonicsJ 2022）。
- **初版错误**：误判 `tools/blit` "不支持单 DOI 故跳过第三轮"。用户指出后实测——blit 是 query 驱动
  （`--download DIR` + query 关键词），在校园网代理 `127.0.0.1:7897` 下是 IEEE 付费墙有效通道。
  凭 `--help` 推断跳过实测 = **TL-33 自欺式核查**（"以为查了证据比没查更危险"）。
- **12 篇全部合格**（identity ✅ / ≥50 行 ✅ / 非反爬 ✅ / SHA256 ✅），含 2 篇 HIGH★ 直接竞品
  （CSNDSP 2014 method-level、udWDM-PON 2018 implementation-level），原 IEEE paywall 系统性偏差
  已消除。receipt 见 `search-archive/2026-08-05/_step2_receipt.json`，覆盖面报告见
  `projects/thesis-fso/shared-m0-foe-cpe-groundwork/step2-coverage-report.md`。
- **剩余失败项**：Optica/SPIE/MDPI 为主（P1 相关度中等或偏低），类别已有合格全文覆盖。
- 覆盖面 terminal（acceptance repair 后）= **`STEP2_ACCEPTED_READY_FOR_STEP3`**（12 篇含两篇 HIGH★
  直接竞品；仍列剩余失败项；本 acceptance repair 由独立 fresh-context V002 PASS 后终态升级，不自动进 Step 3，
  Step 3 启动须用户新对话显式授权并先读 `stages/gw-read.md`）。

### 纪律遵守

- 未进 Step 3/3.5/4a，未实现，未仿真，未跑 MVE，未写论文 claim；
- 未改 Skill / common / params / 既有算法；未重开 P2–P5 / T006 C3 / P09 / G1 / AMC / dormant campaign；
- 未用 oracle/headroom 决 Go；未把"没人题名相同"写 novelty；未做全文语义精读（Step 3 未授权）；
- 主线程未直接 WebSearch/WebReader（检索全走 tools/search + 子 agent 消化）；
- coverage report 与 receipt 不含 method/dataflow/competitor 全文语义结论。

### Acceptance repair（续接，T008 收尾）

V001 初审（本对话主线程，PARTIAL）发现 Step 1–2 产物存在统计口径与措辞缺陷，详见
`verifications.md` V001：

1. **统计口径虚高**：原写"4 API 源（S2/OpenAlex/SerpAPI/Exa）+ 正式发表占比 ~97%"。实测
   `search-archive/2026-08-05/_r1_merged_shortlist.json`：raw=100，dedup=97；4 查询通道均被调用，
   但实际贡献候选的 API 源只有 3 类（Semantic Scholar / OpenAlex / SerpAPI-scholar），Exa 贡献 0；
   publication_status = published 59 / unknown 36 / preprint 2；**可直接证明的正式发表率下限 =
   59/97 = 60.8%**（仍过 ≥50% 门，unknown 不计入分母）。
2. **过度措辞**：原"领域内近乎空集 / 对 P1 新颖性有利 / 没有论文显式提出 …"等 novelty 倾向性表述，
   统一降级为"当前 metadata/abstract 检索未发现明确覆盖；不得据此判断新颖性，须由 Step 3 全文精读验证"。
3. **残留 stale 口径**：S001 后续段、H001 多处、topic-index 未决项仍写"当前 5 篇 / 仍需补两篇直接竞品 /
   用户需手动获取直接竞品"。修正为统一事实：**12 篇合格全文，含 2 篇 HIGH★ 直接竞品**（CSNDSP 2014
   method-level、udWDM-PON 2018 implementation-level，blit 第三轮已补取）。

修复后由独立 fresh-context verifier 做了 V002 复核（独立 agent，12/12 PDF SHA256+行数+identity+统计
口径+current-view 一致性+Step 3 未越界+禁区未污染）。V002 PASS → 终态由
`STEP2_READY_FOR_USER_CONFIRMATION` 升级为 **`STEP2_ACCEPTED_READY_FOR_STEP3`**。验收记录见
`verifications.md` V001/V002。

未越界：repair 只动 current-view 文档措辞与统计口径，未进 Step 3、未新增检索、未下载论文、未实现、
未仿真、未改 Skill/common/params、未动 4 个 `p05_run*.log`、未 amend 3495bb4。

### GW Step 3 精读综合（D003）

- 三个 fresh-context worker 共全文精读 9 篇；全部完成 title 自检、标准条目、七子表、baseline、
  complexity、实验完备性与 M-C-A，逐篇笔记写入 `papers/_read_notes/`，项目 read-log 追加 9 行。
- CSNDSP 2014 不是 same-sequence sharing：FOE 用相邻符号乘积的相位增量，CPR 用符号本身，最佳
  monomial 阶数也不同；其“could possibly be shared”没有实现/资源证据。
- JLT 2018 已明确共享单一 correlation node，且正文追溯 OFC 2016 已共享 differential m-th-power FE
  与 Viterbi PR 的 m-th power；generic P1 action 发生 existing-action collision。
- P1 仅余窄 raised-domain CFO-removal/lifetime + matched-output 候选；但缺 OFC 2016 一手全文与
  2019+ task-matched recent baseline。Q-P1-01 判据 1/2/4 PASS、3 FAIL。
- 初版自造 terminal 已被 V003 证伪；D004 修正为 Step 3 BLOCKED/IN PROGRESS。不是 Go/Kill，不构成
  novelty claim。综合见 R001 与 `projects/thesis-fso/literature_notes_shared_m0_foe_cpe.md`。

### 最后一次 bounded evidence closure（D005 / R002）

- H002 接收验证三项 PASS：CSNDSP 2014 不同输入/不同阶数、仅潜在共享；JLT 2018 正文支持 generic
  shared-m-th-power collision；Q-P1-01 owner 仍为 1/2/4 PASS、3 FAIL。registry 依赖存在且
  `conflicts_with=[]`，本轮范围由用户显式授权。
- bounded gw-search 用满 6/6 组，final 结果数为 19/30/14/5/1/13；全局索引 21,398 条、宽命中
  425 条、既有 P1 结果 75 条、2019+ 语义命中 50 条（未跨文件去重），严格按同输入/同估计器/
  同 FOE→CFO-removal→CPE 任务复筛后合格 recent baseline=0。未运行第 7 组 query。
- OFC 2016：tools/download 失败；Optica 摘要页 200 但 PDF 端点返回 Radware HTML。PTL 2016 同线
  扩展文也经 tools/download/arXiv/IEEE blit 三轮止损失败。两者都没有有效全文，因此没有冒充
  gw-read；OFC exact action=`UNRESOLVED_PRIMARY_FULLTEXT_UNAVAILABLE`。
- fresh-context worker 对三篇已有有效 recent 全文做 targeted dataflow re-read：JLT 2019 的 correlation
  重复已被 conventional refactor 吸收且提出方法改变 estimator；ISCAS 2022、LCOMM 2026 都是
  CPE-only。三篇 title 均 PASS，但没有一篇是 P1 合法 M。
- Q-P1-01 重判仍为 1/2/4 PASS、3 FAIL，触发 terminal=`RECENT_BASELINE_UNAVAILABLE`；P1=
  `SUPPORTING_ONLY`，`mission_method_delta=NONE`。本结论关闭 Step 3 canonical Q 空集，不是 Step 4a
  Go/Kill 或 METHOD_SIGNAL。

**P1 的 generic action 已碰撞，窄 delta 未形成合法 Q；停止该方向，下一轮轮换新候选，不再改名重开。**

## 决策引用

- D001：冻结研究对象与范围边界（GW Step 1–2 入口）—— 新建。
- D002：用户显式授权仅执行 GW Step 3 —— 新建。
- D003：generic shared-compute action 碰撞；无合法 Q#，Step 3 partial terminal —— 新建。
- D004：撤销 D003 自造 terminal，Step 3 保持 BLOCKED/IN PROGRESS —— 新建。
- D005：bounded evidence closure 触发 `RECENT_BASELINE_UNAVAILABLE`，P1 降为 `SUPPORTING_ONLY` —— 新建。
- D024（system 专题）：P1 计算图工程候选恢复与实际工具链吸收门 —— 引用，本专题承接。

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D002/D005 后严格只执行 Step 3 与 bounded
  search/acquire/read closure；未进入 Step 3.5/4a/实现/仿真）。

## 后续

- P1 已以 `RECENT_BASELINE_UNAVAILABLE` 关闭，exact OFC 一手缺口只保留为证据边界，不再触发扩检索。
- 下一轮由上游 RDL 轮换机制不同的新候选；不得改名重开 P1，也不得进入 Step 3.5/4a/实现/仿真。
- V004/H002 保留为 blocked 历史；H003 closed-state handoff 已完成。首轮 closure verifier 为
  PARTIAL（科学/边界 PASS，治理模板 FAIL）；按最小清单修复后，第二个 fresh-context verifier 已以
  V005 PASS 关闭六 JSON、acquire、三篇全文、Q/terminal、治理与 git 边界。
