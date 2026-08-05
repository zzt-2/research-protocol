# [S001] P1 Shared M0-Power FOE–CPE Groundwork Step 1–2 执行

> 2026-08-05 | GW Step 1–2 | 完成（terminal=STEP2_READY_FOR_USER_CONFIRMATION，待用户确认）

## 目标

执行 T008：在独立新专题内完成 P1 "Shared Raised-Power Compute Graph for NDA FOE+CPE" 的
GW Step 1 检索 + Step 2 全文获取/覆盖面门，停在用户覆盖面确认门。不进 Step 3、不实现、不仿真、
不跑 MVE、不写论文 claim。

## 记录

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
- 4 个 `tools/search` 定向查询（VV/Mth-power/FF-joint、joint-CFO-CPE-lowcomplexity、hw-efficient-CPR、
  fso-sat-coherent-carrier，各 2 个子 agent 执行）：**97 去重候选**，4 API 源（S2/OpenAlex/SerpAPI/Exa），
  正式发表占比 ~97%，必读 ≥12，3 语义类全覆盖。
- Class 2 generic（"common subexpression / computation reuse / compute graph"）在领域内近乎空集
  ——对 P1 新颖性有利，但共享图数据流几乎无直接文献对标（Step 3 须精读确认）。
- Step 1 产出：`search-archive/2026-08-05/_p1-competitor-shortlist.md`（直接竞品初筛矩阵，
  metadata/abstract 级，不当精读结论）+ `r1-*.json` + `_r1_merged_shortlist.json`。

### Phase C — GW Step 2 获取/覆盖面门（✅ 12 篇合格，terminal=READY_FOR_USER_CONFIRMATION）

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
- 覆盖面 terminal = **`STEP2_READY_FOR_USER_CONFIRMATION`**（12 篇含直接竞品，仍列剩余失败项，
  不自动进 Step 3）。

### 纪律遵守

- 未进 Step 3/3.5/4a，未实现，未仿真，未跑 MVE，未写论文 claim；
- 未改 Skill / common / params / 既有算法；未重开 P2–P5 / T006 C3 / P09 / G1 / AMC / dormant campaign；
- 未用 oracle/headroom 决 Go；未把"没人题名相同"写 novelty；未做全文语义精读（Step 3 未授权）；
- 主线程未直接 WebSearch/WebReader（检索全走 tools/search + 子 agent 消化）；
- coverage report 与 receipt 不含 method/dataflow/competitor 全文语义结论。

## 决策引用

- D001：冻结研究对象与范围边界（GW Step 1–2 入口）—— 新建。
- D024（system 专题）：P1 计算图工程候选恢复与实际工具链吸收门 —— 引用，本专题承接。

## 范围确认

- 本轮是否在 scope boundary 内：**是**（严格只到 Step 2 覆盖面门，未越界）。

## 后续

- **等用户确认覆盖面**：是否接受当前 5 篇合格全文作为 Step 3 精读起点（含系统性偏差：最直接 2 篇
  竞品在 IEEE paywall 后），或要求补足后再进 Step 3。
- **未决项（Step 3 关闭，本轮不关）**：① 是否有论文在 FFT-FOE + mean-angle CPE 间显式共享单次
  raised-power；② 共享图相对 conventional refactor 是否还有可区分工程 claim；③ matched-performance
  comparator 是否有现成数据。
- **下一合法动作（待用户授权后）**：开新对话执行 Step 3 精读（读 content.md，按 gw-read 模板提取
  结构化数据），或用户先手动补 2 篇直接竞品全文。Step 3 未授权前禁读全文下方法结论。
- H001 交接已写：`.sessions/2026-08-05-shared-m0-foe-cpe-groundwork/H001-step2-coverage-ready.md`。
