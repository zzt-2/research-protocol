# [S008] P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 入口门 STRATEGIC_GATE

> 2026-08-01 | CAMPAIGN_EXPLORATION_DISPATCH / 入口门评估 | 状态：完成（入口门否决，不计有效包）

## 目标

按用户 P09 执行指令端到端执行一个新有效科学大包 P09 = `COMPUTE_CONSTRAINED_NDA_ML_SEARCH`，围绕已验证有效的 NDA-ML 做"低复杂度、性能保持"的毕业方法生产包。用户冻结研究问题为 M = 当前 full-search NDA-ML / C = 有限计算量实时接收约束 / A = 均匀穷举大量候选导致计算冗余 / 目标 = 用结构化搜索减少 objective evaluations 同时保持性能；并冻结双门 A（性能非劣 CI upper ≤0.10 dB）+ B（objective evaluations 减少 ≥4×）、最强廉价 comparator = dev-tuned uniform coarse grid；明文允许"若无法证明计算问题或 novelty boundary，终止为 STRATEGIC_GATE，不计包"。

## 记录

### 必读完成（证据指针）

1. **topic-index.md**（本轮 Read 全文）— 当前 campaign 8/10，G 族 D049 关闭，P09 须换不同机制族，forbidden 含 `NDA_ML_BODY_REOPEN`。
2. **mission-log.md**（本轮 Read 全文）— CP040 P08-R2 完成恢复 8/10；CP028/CP029 入口评估无 sprint 先例（STRATEGIC_GATE/PHYSICS_BACKED_TESTBED_UNAVAILABLE，不计包）。
3. **D049**（本轮 Read decisions.md:2975-3020）— P08-R2 三根因修复 PROBLEM_ABSENT，G 族关闭；PARTIAL reusable asset 模式；verifier 必须递归调用图 + metamorphic 门。
4. **V075**（本轮 Read verifications.md:3925-3975）— 19/19 ACCEPT，H7 递归 AST + metamorphic Δ=0.0。
5. **method-production.md**（本轮 Read 全文）— 入口四门（physical DOF / baseline failure align / named comparator / file:line），3 门 FAIL 路由 STRATEGIC_GATE/BLOCKED_TESTBED；终态集 + `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`。
6. **thesis-lessons 速查 + 最近三条**（本轮 Read）：TL-04（空白≠机会）/TL-30（框架强制 forbidden axis）/TL-31（教训复现）/TL-32（Go/Kill 标准分离）/TL-33（FR-26 证据链，自欺式跳步）。
7. **sim-preflight skill**（本轮 invoke）— 核心 5 条 + mve-validation（consistency≠correctness）；本轮无实验故不进 Execute 场景。
8. **NDA-ML 实现**（本轮 Read 源码 + Explore 子 agent agent_c9883e0a fresh context 交叉）：见下"入口门裁决"。

### 入口门裁决：STRATEGIC_GATE（承重前提 A 证伪）

源码逐行核查（主线程 Read `common/_recovery.py:171-273` + `simulator/sc_nda_ml_sim.py:173-231` + grep 零命中 + Explore 子 agent fresh context 交叉确认）证明 **NDA-ML 不是 search**：

- **`common/_recovery.py:171-273` `nda_ml_recovery`** = closed-form 解析估计器（B11 锚方法，D005 Go / D007 linewidth 统一）。三步：① `raised = rx ** M0`（M0=8，向量化升幂去调制，`:213`/`:243`）；② 频率/相位估计——`assume_df_zero=True`（生产 AWGN/turbulence 路径）用整块 `np.angle(raised.mean())`（`:232`，none 变体）或 K=8 段每段一次 `np.angle(raised[lo:hi].mean())`（`:222-225`，segmented 变体）+ unwrap+`np.interp`（`:226-229`）；`assume_df_zero=False`（Doppler 残余）用单次 FFT argmax `np.argmax(np.abs(R))`（`:249`）+ Quinn-Rife 插值（`:250-258`）+ 线性回归常相位（`:262-270`）；③ 解卷绕除 M0（`:270`/`:233`）。**全程零 candidate 枚举、零 likelihood/objective 在候选集上求值**。
- **`simulator/sc_nda_ml_sim.py:180-187` `ber_nda_awgn`** = 生产 driver，逐 256-sym 块调一次 `nda_ml_recovery(seg, ..., intra_block_tracking='segmented')`。每块成本 = 8 次闭式 mean-angle + unwrap/interp。**无 per-window objective evaluations 可数**。
- **grep 零命中**（已运行）：`grep -rniE "full.?search|exhaustive|candidate|grid_search|phase_grid|coarse|coarse.?to.?fine|hierarchical|objective.*eval|search.*space|enumerate" common/_recovery.py simulator/sc_nda_ml_sim.py simulator/_b11_params.py` → 零结果。
- **代码库唯一 exhaustive search 是 `bps_cpr`（`_recovery.py:91-118`）**：B 测试相位（`:97`）× Nw 符号滑动窗距离度量（`:102-110`）+ `np.argmin`（`:113`）。docstring "Blind Phase Search (Pfau 2009, JLT)" 证是独立算法；ADVISOR_BRIEFING 报 NDA-ML ≈ BPS 0.006-0.14 dB 证 BPS 是 comparator。**BPS 是 search 但不是 NDA-ML 的一部分**。
- **`explore/nda-awgn-tracking-sandbox/_db_caliber_and_complexity.md:51-61`**：NDA-ML 已 16 real mult/symbol（VV 24，DA-ML 5.5），评 medium-strength "advantage small"。**无 coarse-grid / coarse-to-fine / hierarchical comparator 存在**（grep `projects/thesis-fso/` 零命中）。
- **`_mve_results.json` `fr11_architecture_summary`**：action_space="NDA-ML 升 M0 次幂盲去调制（连续相位估计）"，非 search。

### 判据映射

| 用户冻结合同要素 | 源码事实 | 结论 |
|---|---|---|
| M = "当前 full-search NDA-ML" | NDA-ML 是 closed-form 升幂+mean-angle/单正弦 FFT-ML，非 search | 不存在 "full-search NDA-ML" |
| A = "均匀穷举大量候选导致计算冗余" | 无候选、无 objective 求值 | **A 证伪** |
| 双门 B：objective evaluations 减少 ≥4× | 无 objective evaluation 可数 | primary cost metric 无定义 |
| 最强廉价 comparator：dev-tuned uniform coarse grid | 无网格可 coarse 化 | comparator 无可作用对象 |
| Phase A 终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_COARSE_SEARCH | 触发前提是有 search 被 coarse grid 解决 | 不适用（连 search 都没有） |

唯一可裁剪的"重复成本"是逐块从零重算 closed-form DSP（无块间状态复用/无 early-stop），但减少它 = **替换估计器**（跳块/状态复用/换升幂/减 K 段数），非"对同一 objective 做结构化搜索减少 evaluations"——这是不同研究对象，违反问题定义，且动 NDA-ML 估计器本体 = 触发 `NDA_ML_BODY_REOPEN`（forbidden，TL-30）。双重禁止。

### 适用条款

- 用户合同："若无法证明计算问题或 novelty boundary，终止为 STRATEGIC_GATE，不计包"。
- method-production.md 入口四门：门1（NDA-ML 估计器内无 search 自由度可裁剪）FAIL / 门2（无 lever 可作用）FAIL / 门3（coarse grid 无网格可 coarse 化）FAIL / 门4（file:line 已举）；3 门 FAIL 路由 STRATEGIC_GATE 而非 factory task。
- FR-23：研究起点须 baseline 具体不足（M-C-A），A 证伪 = 问题不成立。
- FR-22 + topic-index forbidden `NDA_ML_BODY_REOPEN`：动估计器本体禁止。
- FR-26/TL-33：宣告前必查源码（已 Read + grep + Explore 子 agent 交叉），不脑补 "NDA-ML 是 search"。

### 终态

**`STRATEGIC_GATE`**——唯一合法终态（EXECUTION_INVALID 不适用因无执行；EVIDENCE_INSUFFICIENT 不适用因非数据不足而是前提证伪；NO_DIAGNOSTIC_METHOD_SIGNAL/COMPUTE_EFFICIENT_METHOD_SIGNAL 要求实验产物，本轮无 sprint）。**P09 不计有效包**（count_excludes=entry_preflight_only，同 CP028/CP029 无 sprint 先例）。campaign 维持 8/10。本轮无 sprint/无 held-out seed/无 artifact/无 commit 之外产物。

## 决策引用

- D050（新建）：P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 入口门 STRATEGIC_GATE，承重前提 A 证伪，不计包，campaign 维持 8/10。
- V076（新建）：P09 入口门独立 verifier 13/13 ACCEPT（源码事实核查 + grep 复算 + 双门失效分析 + 终态合法性）。
- D049：引用（P08-R2 结论维持，G 族关闭，PARTIAL asset 模式）。
- 无其他新决策。

## 范围确认

- 本轮是否在 scope boundary 内：**是**。P09 是 D039 campaign 授权下的有效包探索；入口门否决是用户合同明文允许的合法终态（"若无法证明计算问题，终止为 STRATEGIC_GATE，不计包"）。未重开任何 forbidden axis（NDA_ML_BODY_REOPEN / 已关闭 A/E/F/G 族均未触碰）。未做 protected owner/formal/Skill/thesis framework 改动。

## 后续

- **不重提 P09 同对象**：COMPUTE_CONSTRAINED_NDA_ML_SEARCH 承重前提证伪，换名重提（NDA-ML-low-complexity / compute-constrained-NDA-ML / NDA-ML-coarse-grid 等）属 TL-30 禁换名重开。
- **下一合法动作**：重新指定 P09 入口（须过 problem-bearing 入口四门；禁重开已关闭 A/E/F/G 族及 NDA_ML_BODY_REOPEN/FOE-residual cascade 等所有 forbidden axis），或用户授权 P10 campaign-level 裁决（提前到第 9-10 包做 portfolio pivot/continue 决策）。
- **TL 教训候选**：本轮无新方法论教训（"承重前提须源码核查"已被 TL-33/FR-26 + V075"consistency≠correctness 递归核查"覆盖）；入口门源码核查模式同 CP028/CP029 先例。
- **campaign 进度**：8 包全 honest negative 0 signal（P01-P08-R2 verdict 序列），族覆盖 7 族（A/E/F/G 关闭，B/C/D 连续=1），仍 0 active carrier。P09 入口门否后剩 2 有效包预算（P09 重指定 + P10），或 P10 campaign 裁决。
