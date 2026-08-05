# Decisions — Shared M0-Power FOE–CPE Groundwork

> 本专题决策记录。D### 按编号排列，旧决策标 superseded 不删。

## D001: 冻结研究对象与范围边界（GW Step 1–2 入口）

> status: active
> date: 2026-08-05
> 取代：无
> 扩展：承接 RDL system 专题 D024 / CP005 / T008（P1 计算图工程候选恢复与实际工具链吸收门）
> 被取代：无
> 依据：T008 任务书 §2（冻结研究对象）+ D024（P1 survivor 恢复）+ caller-path 证据复核

### 决策

本专题作为 P1 "Shared Raised-Power Compute Graph for NDA FOE+CPE" 的正式 Groundwork owner，
本轮只执行 GW Step 1 检索 + Step 2 全文获取/覆盖面门。冻结研究对象（M/C/A）见 topic-index
不变量段，仅用于检索与获取，不作为 Step 3/4a 结论。

确认关键已知事实（caller-path 已复核，证据指针见下）：

- `[FACT]` 升幂 `rx**M0` 在 NDA 路内被计算两次：FOE 在
  `projects/simulation/simulator/sc_nda_ml_sim.py:150`（`raised = rx ** M0_power`，FFT 找频峰）；
  CPE 在 `projects/simulation/common/_recovery.py:213`（`assume_df_zero` 分支 `raised = rx ** M0`，
  mean-angle）与 `:243`（FFT-df 分支 `raised = rx ** M0`）。
- `[FACT]` 两次跨独立 Python 函数调用（CPython/NumPy），无 JIT/graph optimizer/CSE 证据。
- `[FACT]` route-A caller `run_ccisp_family1_selector_a_30seed.py:24-31` 在 `per_block_nda_receiver_output`
  串行调 `fft_foe_m0_omega` → `nda_ml_recovery(assume_df_zero=True)`。
- `[FACT]` route-B caller `_a4_branchrouted_30seed.py:138-148` `per_block_nda` 同串行双调用。
- `[FACT]` 升幂域 CFO 去除可用 `raised * exp(-j*M0*omega*k)`，原信号域补 `omega*k + phi`。

未知项（必须由 Step 1–2 关闭或标 blocker，见 topic-index 未决项）。

### 理由

D024 已确认 P1 在实际 CPython/NumPy caller 中存在真实重复升幂，假想 compiler/CSE 不构成
廉价替代，恢复为 `THESIS_ENGINEERING_COMPONENT` 设计候选。但 survivor 不是 METHOD_SIGNAL，
必须回正式 GW Step 1–3/3.5/4a。本轮（T008）只推进 Step 1–2，停在用户覆盖面确认门。

### 排除的替代方案

- 不把 P1 升级为 METHOD_SIGNAL / active carrier / 论文结论；
- 不在 Step 1–2 阶段用 oracle/headroom 决定 Go；
- 不修改 NDA-ML 估计器统计（触发 `NDA_ML_BODY_REOPEN`）；
- 不跳过覆盖面用户确认门自动进 Step 3。

### 影响范围

新建本专题；新建项目 owner
`projects/thesis-fso/literature_notes_shared_m0_foe_cpe.md`（GW 进度 + Step 1–2 状态）与
`projects/thesis-fso/shared-m0-foe-cpe-groundwork/step2-coverage-report.md`。不触动既有科学
verdict、common/params、Skill 与正式论文。

### 来源

T008 任务书；RDL system 专题 D024/CP005/S015。触发原话：无（技术推导；派生自 D024，用户仅
确认执行 T008）。
