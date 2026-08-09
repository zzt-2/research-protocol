# Verifications — RML-FSTS Groundwork

## V001: T003 Step 1–2 独立终验

> status: PASS
> date: 2026-08-08
> 关联：S001 / D002 / R001 / R002
> verifier: fresh-context `/root/final_verifier`

### 验证范围

按 T003 §4.2 独立检查 12 项：专题结构与 registry、H003 三事实、Step 1 JSON/receipt、查询轮次与路线、Step 2 全文 identity/provenance/hash/bytes/lines、CORE 覆盖、terminal、literature owner/master-state、证据边界、Step 3+ 禁止项、上游历史保护、git/YAML/p05/no-push。

### 初审

`PARTIAL`，P0/P1/P2=`0/1/0`。唯一 P1 是 `121 unique / 71 published / 58.68%` 缺少可独立复算的 canonical identity ledger，且 Q1/Q2 的 raw/dedup 只有 receipt 记录、未明确说明 raw artifact 未持久化。其余 11 项 PASS。

### 唯一最小修复

未重跑检索、未增加 query、未改变 scientific terminal。新增正式 staged canonical ledger 与 Q1/Q2/Q3 retained 中间产物；receipt 明确 Q1/Q2 raw/dedup 是执行时同步记录的 stdout observation，不冒充不存在的 raw artifact。ledger 逐条记录 131 个合并输入、10 个重复移除、121 个唯一身份、71 个正式发表判定及本地索引指针。

### 复核结果

`PASS`，P0/P1/P2=`0/0/0`。独立复算 `123 + 8 = 131`、`131 - 10 = 121`、published=`71`、`71/121 = 0.586776… → 0.5868`；71 个正式发表 identity 的本地索引指针、123 个 query-origin ref、priority inputs 与三份 retained 中间产物 SHA256 均匹配。原 12 项全部回归 PASS。

### 结论

PASS。允许按 T003 一次性提交 Step 1–2 与治理同步；不授权 Step 3/3.5/4a、smoke、实现或仿真，不改变 object/package failure=`0/0`，不得 push。

## V002: T001 Groundwork Step 3 独立终验

> status: PASS
> date: 2026-08-09
> 关联：S002 / D004 / R003
> verifier: fresh-context `/root/step3_verifier`
> 证据报告：`projects/thesis-fso/worker-logs/step-3-rml-fsts-verifier.md`

### 验证范围

按 T001 §7.1 独立检查 12 项：仅 Step 3 边界；五篇 title/DOI/path/SHA/bytes 与 Yu adapter；5×标准字段、7 子表、通信参数与非 DRL N/A；五篇实验完备性与三篇写作架构；read-notes/read-log/literature owner 一致性；source/target 与 C3/C4 角色；缺失竞品承重边界；canonical Q# 四判据；Step 3 状态；literature/master/topic/registry/D004/H002 同步；failure=`0/0`；git/YAML/JSON/p05/禁区。

### 初审

`PARTIAL`，P0/P1/P2=`0/2/1`。两个 P1 分别为 L01/L02/L04 的 owner/read-log 相对 source path 无法无歧义解析到 receipt 冻结文件，以及 L02/L04 reader 将强制 Verification/Validation/Uncertainty 三轴误写成 Validity/Verifiability/Utility；一个 P2 是 Step 2 历史段仍以“当前状态”描述旧状态。其余 identity、字段、边界、Q1、机械门均通过。

### 唯一最小修复

未补文献、未改科学结论、未进入下游步骤。将 L01/L02/L04 owner/read-log 路径改为 receipt 的 shared absolute canonical，并在 L04 read-note 明确排除 worktree 内不同哈希副本；将 L02/L04 reader 统一为 Verification/Validation/Uncertainty=`2/2/2` 与 `2/2/1`；把旧状态句标明为“Step 2 结束时状态”。

### 复核结果

`PASS`，P0/P1/P2=`0/0/0`。三篇 shared canonical 3/3 存在且 hash/bytes 与 receipt 一致；五篇 reader 5/5 使用统一三轴并与 owner/read-note 汇总一致；literature/master/topic/registry/D004/H002 current view 一致；`git diff --check`、YAML/JSON parse、staged=0、四个 p05 日志 hash/no-stage、禁止路径 diff 全部通过。

### 结论

PASS。允许按 T001 一次性提交 Groundwork Step 3 产出与治理同步；Step 3.5 保持 NOT_STARTED，不授权 Step 3.5/4a、smoke、实现、仿真或 MVE，不改变 research-object/method-package failure=`0/0`，不得 push。

## V003: Step 3 主控接收语义纠偏复核

> date: 2026-08-09
> 关联：D005 / R003 / H003
> verifier: fresh-context `/root/q1_semantic_critic` + `/root/step3_integrity_audit`

### 验证项

- [x] 完整性：5/5 receipt/path/SHA/bytes、read-notes/read-log/owner 与 22 文件提交范围 → PASS。
- [x] Q1 A 方向：旧写法存在“稳定/足够=问题不存在”的 P1 歧义；改为 M 隐含依赖同一 lag 近似最优、该假设在 C 下被违反时 M 不足 → PASS。
- [x] 判据 3：Wang 2023 能承担 exact recent M；Enhanced 2024 是 2024 Optics Express task-matched comparator；项目既有 authority 明列 Optics Express 为光通信顶刊/允许保留的顶会顶刊，因此由 L02 闭合 2019+ 顶刊门，不依赖 Wang venue 等级 → PASS。
- [x] 阶段边界：A 仍 INFERENCE，crossover/failure/headroom 仍 UNKNOWN；Step 3.5/4a/实验均未启动 → PASS。

### 证据

`stages/glossary.md:18`；`projects/thesis-fso/master-state.md:190`；`.sessions/2026-06-20-problem-driven-redirection/decisions.md:983`；`.sessions/2026-06-04-advisor-review-revision/topic-index.md:94`；L01 `content.md:208,299`；L02 `content.md:404` 与 owner 的 L02 identity（Optics Express 32(15), 2024）；L04 `content.md:170`；critic 回执 `PARTIAL, P0/P1/P2=0/2/0`；integrity auditor 在 venue authority 闭合后的最终回执为 `PASS, P0/P1/P2=0/0/0`。修复后确定性 grep 显示 Q1 在 R003/owner/H003 同义，且未把 Wang venue 冒充顶刊。

### 结论

PASS。V002 的完整性/合同一致性结论保留；其 Q1 科学语义验收由 V003 修正。Step 3 completed 可维持，进入 Step 3.5 前置语义债已关闭。

## V004: Groundwork Step 3.5 独立终验

> status: PASS
> date: 2026-08-09
> 关联：S003 / R004 / D006-D007 / H004
> verifier: fresh-context `/root/rml_step35_verifier`
> 证据报告：`projects/thesis-fso/worker-logs/step-3-5-rml-independent-verifier.md`

### 验证范围

按 T010 独立检查 10 项：scope change 与禁区；R1 8-query matrix、实际来源和 R2/R3 轮次；Wang/Enhanced 双向引用链；qualified fulltext identity/path/SHA/bytes/action；竞品分类；conditioned single-lag cheap alternative；唯一合法 terminal；Step 4a 与禁止改动；current views 一致性；JSON/YAML/git/p05/cache 机械完整性。

### 初审纠偏

Verifier 一度将 5 个 `cpython-312.pyc` 的“存在”初判为 P1；独立复算确认它们是 HEAD 已跟踪基线，`git hash-object` 与 `HEAD:<path>` 5/5 一致且目录 status 为空，因此不是任务残留，撤回 P1。

### 复核结果

`PASS`，P0/P1/P2=`0/0/0`，10/10 gates PASS。19/19 receipt 引用 raw 存在且 SHA256 匹配；R1=`27`、引用链=`63→51 unique`、R2=`63=15+48`、R3 timeout 非零命中语义均可复算。四篇 qualified fulltext 的 identity/hash/bytes/action 与两条 `papers/index.json` success entry 一致；8 项缺全文保持 UNKNOWN。四个 `p05_run*.log` 的 size/mtime/SHA 与基线一致且未暂存。

### 结论

PASS。唯一证据支持的 Step 3.5 terminal 是 `EVIDENCE_BLOCKED`；Step 4a=`NO ENTRY`。允许把本轮预定证据、current views 与 verifier log 一次性提交；不得暂存四个 p05 日志，不得 push。下一科学动作仅限取得一个或多个未决一手全文后，重开 Step 3.5 action-level 裁决。

## V005: 主控接收科学语义与共享 canonical 复核

> status: PASS
> date: 2026-08-09
> 关联：R004 / D008 / H005
> verifier: fresh-context `/root/step35_science_critic` + `/root/step35_blocker_feasibility`；机械一致性参考 `/root/step35_integrity_audit`

### 验证项

- [x] R1/R2/引用链/timeout/三轮止损：机械数字与 receipts 一致，V004 的完整性结论保留。
- [x] canonical gate：`gw-supplement.md` 允许三轮上限后记录未覆盖方向；不要求所有候选全文齐备，D007 的 NO ENTRY 无框架依据。
- [x] shared canonical：130981 PDF/content 实际存在；含 2026-07-04 全文增量核验的有效 read-note 为 `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md`，DOI 同名旧 note 仍是 stale 下载失败记录；执行 receipt 的 FULLTEXT_UNAVAILABLE 是 stale false negative。
- [x] action read：130981 是固定 STFT/FFT coarse FOE，received power/FFT points 为评测或离线参数，不是 condition→lag/`B_L`/window selector。
- [x] blocker 分层：SSRN=高风险 UNKNOWN；ACP=次级 comparator；其余为非阻断任务/条件/架构邻接或 generic prior-art 边界。
- [x] claim boundary：Q1 仅 provisional survivor；不宣称首次、novelty closure、Go、METHOD_SIGNAL 或方法成立。

### 证据

- `stages/gw-supplement.md`“检索充分性判据/不达标时”。
- 共享 `papers/doi/10.1016_j.optcom.2024.130981/source.pdf`：2,896,299 bytes，SHA256 `2a5728193de8fac0ffbd1c55f60847fe44b9d462c70e13c8325c798c84feefc2`。
- 共享 `content.md`：38,504 bytes，SHA256 `67fa0ea9f1c8b8c37b48bc87474c4a7d7b565b2ebe3f0c12b44cca9d8aa66ecb`，承重行 47、71–87、127–141。
- scientific critic 初审：`FAIL, P0/P1/P2=0/2/0`；blocker audit：8 项 blanket block 不成立。

### 结论

PASS。V004 的 receipts/hash/范围一致性仍有效，但其“唯一 terminal=EVIDENCE_BLOCKED / Step 4a NO ENTRY”科学语义被 V005 取代。D008 修订后的唯一当前状态为 provisional survivor with fulltext limitations；Step 4a 可在用户授权的新对话启动。

## V006: D010 semantic-smoke 合同 pre-run 独立审查

> status: FAIL
> date: 2026-08-09
> 关联：S004 / D009-D010 / T014
> verifier: fresh-context `/root/rml_contract_critic`

### 验证范围

只读检查 D010、immutable contract、T014 与 T011–T013 三份独立审计，覆盖方法身份、same-realization pairing、B2 可部署 power proxy、物理 provenance/calibration、MSE/outage oracle、crossover/reducer 与 terminal 唯一性；未运行实验、未联网、未修改文件。

### 结果

`FAIL`，P0/P1/P2=`2/5/2`。

- P0-1：原 Q1 action 是联合 `(B_N,B_L)`，改变 `B_L` 必须重建发端 FSTS；D010 固定发端后扫描 known-TS de-rotated `L_rx`，只在 default 点退化 Wang，off-default 是不同 estimator family。其结果无权发原 Q1 terminal。
- P0-2：`10/20 dB` 明标未验证，weak/strong 采用 Gu scalar-GG transfer而非 Wang `C_n^2` phase-screen calibration；缺 source power/SNR anchor、精确 channel equation 与 B0 qualitative anchor，局部 diagnostic 无权 Kill/Resolve Q1。
- P1：off-default statistic 未唯一冻结；B2 power proxy/bin/fallback 未完全定义；MSE/outage 共用单 O1 不成立且缺 MDE；reducer/crossover/observability/扩容规则不可唯一执行；master seed/canonical cell 未冻结。
- P2：GG provenance 应进 immutable contract；Wang 公式仅 HTML/MathJax，必须持续标 provenance limited。

### 处置

在首次 RED/scientific grid 前中断 T014 executor；D010 标 `rejected`。允许一次 pre-result 合同重构：保留 structural `B_L` 方法对象，action-specific waveform 只共享 exogenous latent seeds；补 source condition/calibration与独立 B0 anchor；拆 MSE/outage oracle并把 reducer写成可执行真相源。若无法闭合，才使用 D009 terminal 5。

### 结论

FAIL 是合同验证失败，不是 Q1 scientific Kill/Resolved，也不计 semantic-smoke 迭代。没有科学 raw rows 或 terminal 产出。

## V007: Step 4a terminal 5 fresh-context 独立终验

> status: PASS
> date: 2026-08-09
> 关联：S004 / D009-D011 / T011-T019 / H006
> verifier: fresh-context `/root/rml_step4a_verifier`

### 验证范围

独立重放起点恢复、130981 action identity、A0 §0–§6、D010 pre-run P0、Wang structural `(B_N,B_L)` 公式身份、action-before 因果边界、phase-screen/SMF→scalar-GG 保真差异、dBm→离散噪声可辨识性、B0 calibration gate、D009 五终态排他性、owner/receipt 一致性、JSON/YAML/hash/git 与四个 protected `p05_run*.log`。未运行 estimator、performance grid、diagnostic structural run 或 MVE，未修改 owner/合同/artifact、未提交或 push。

### 结果

`PASS`，P0/P1/P2=`0/0/0`。独立 verifier 日志：`projects/thesis-fso/worker-logs/step-4a-rml-fsts-independent-verifier.md`，SHA-256=`9f855b33e2d5785682e9c4dcea3a8bd7eab9659355d80c12504159e04c9f744d`。

- 三类 hard blocker 均经原文/代码重放成立：structural action-before causality；Wang phase-screen/0.2 m aperture/SMF/branch joint statistics 与 Gu scalar-GG 非等价；Wang dBm receiver power 到 post-ADC complex-noise variance 不可唯一。B0 numeric calibration gate因此不可执行。
- Fig. 8/10/11/12 的 IEEE 403 只属 recoverable gap；即使恢复图也不能自动消除上述 hard blockers。
- D010=`REJECTED_PRE_RUN`、`terminal_authority=NONE`；scientific raw rows=`0`，B0/B1/B2/O1/C1、paired delta/CI均=`N/A (NOT_RUN)`，C1与bounded MVE不存在。
- terminal 1/2/3/4分别需要合法 crossover、B2评分、稳定 residual/observability 或 fresh held-out MVE；当前均无数据权限。唯一合法终态是 terminal 5。
- owner/artifact、信息边界、failure count=`0/0`、SSRN 6293357 债务、strongest cheap comparator 与重开条件一致；source-log hash=`6/6`、protected-log hash=`4/4`、JSON/YAML/路径/diff/staging均 PASS。

### 结论

接收 D011：Groundwork Step 4a terminal=`STEP4A_INCONCLUSIVE_INVALID_OR_BLOCKED_TESTBED`；Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献层级=`NONE`。这不是 Kill/Resolved/Go，也不构成性能结果。专题可转 dormant；只有取得 authors/source receiver+channel config并显式定义 action-before protocol、经 scope change 后，才可重开 Step 4a。Contract、Execute 与论文写作继续禁止。

## V008: Step 4a 重开输入 fresh-context 独立终验

> status: PASS
> date: 2026-08-09
> 关联：S005 / D012-D013 / T020-T022
> verifier: fresh-context `/root/rml_reopen_input_verifier`
> 证据报告：`projects/thesis-fso/worker-logs/step-4a-rml-fsts-reopen-input-verifier.md`

### 验证范围

独立重放四门：SC1 的三类 public-source surface、exact paper identity/hash 与字段 1–7；AB1 的 Wang structural pre-TX action、previous-frame/common-probe caller path及 Wang/Valjus/WiSEE/JLT 一手边界；D012 fail-closed reducer、D011 scientific terminal唯一性与 strongest cheap comparator；owner/receipt/JSON/YAML/path/hash/git/protected-log 机械完整性。未联网扩检索，未运行 estimator、performance grid、diagnostic structural run、C1 或 MVE，未修改 verifier log 以外文件，未 commit/push。

### 结果

`PASS`，P0/P1/P2=`0/0/0`，G1–G4 全部 PASS。verifier log SHA-256=`50bf4d208d9018874190e8b289616db57531a5802f47ea71112ec3203b9c3038`。

- SC1：bounded search 覆盖 publisher/DOI、author/institutional、code/data repository，未扩大为全网不存在声称；IEEE document=`10097873`、issue id=`10101698`、article sequence=`7302313`。exact config fields 1–7 为 `0/7`，接收 `SC1_NOT_CLOSED_PUBLIC_SOURCE_EXHAUSTED`。
- AB1：Wang `(B_N,B_L)` 在 transmitter FSTS construction 前冻结，正文无 previous-frame/common-probe/RSSI/feedback/ACK/action-signaling/lifecycle caller。两方案在 action-invariant observation、time-series、feedback/freshness、state/fallback、overhead或paired unit上均未闭合；接收 `AB1_NOT_CLOSED`，primary=`NONE`、applicable tests PASS=`0`。
- reducer：SC1/AB1 任一未闭合即 `REOPEN_INPUTS_NOT_CLOSED`，不存在 partial diagnostic出口。D013只关闭 recovery Probe；D011/V007 scientific terminal保持唯一有效。
- scientific boundary：Q1=`INCONCLUSIVE`、`METHOD_SIGNAL=NONE`、贡献=`NONE`、failure=`0/0`；B0/B1/B2/O1/C1与paired delta/CI均 `N/A (NOT_RUN)`，scientific raw rows=`0`。ranking crossover与conditioned-lookup absorption均 `NOT_EVALUATED`。
- integrity：两份 recovery log hash 2/2、JSON/YAML/path、原 terminal receipt、protected logs 4/4、禁区 diff与空暂存区均 PASS。T021 master-synthesis provenance已显式降级并由本轮 fresh fulltext/primary-line read独立复核。

### 结论

接收 D013 recovery terminal=`REOPEN_INPUTS_NOT_CLOSED`。本 PASS 只确认 recovery reducer与证据边界，不是 scientific/performance/novelty PASS。专题恢复 dormant；下一次科学重开必须同时取得 executable phase-screen/SMF/receiver-noise source backend与 executable feedback/time-series testbed。联系作者或提交外部请求须另获用户授权；在此之前继续禁止 grid、diagnostic、MVE、C1与下游。
