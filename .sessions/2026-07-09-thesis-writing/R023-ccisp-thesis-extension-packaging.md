# [R023] CCISP adaptive CPR 会议稿→学位论文 extension packaging 诊断与包装合同

> **SUPERSEDED / PAUSED — D025→D026 (2026-08-03)：本文件保留为旧包装证据，不再代表最终 thesis contract。当前唯一条件式 spine 见 D026；禁止据此执行 D024 或开始正式 Ch4 写作。**

> 2026-08-03 | 阶段: paper-writing DIAGNOSE/PROPOSE | 状态: 完成（只诊断，不进 WRITE）
> 关联: thesis-writing 专题 2026-08-03 范围扩展 / campaign-level-thesis-contribution-synthesis / D023 / D024

## 调研问题

以已完成的 CCISP 2026 会议稿为成熟主锚，将长程 campaign 资产重新映射为鲁棒性/部署实现/可信验证扩展，判断哪些进学位论文、哪些可成 journal extension，找出真正只差的小实验，输出唯一推荐包装蓝图 + 下一执行包。

## 发现

### 投稿状态核实

- 全量检索 `projects/simulation/paper/ccisp2026/` 与 `.sessions/2026-07-14-ccisp-content-expansion/`：**未发现真实投稿编号、投稿系统回执、录用通知**。
- 状态记录为 `CONFERENCE_MANUSCRIPT_COMPLETE / SUBMISSION_STATUS_UNKNOWN`。会议稿本身完整（V026/V027/V028 = 5 页权威构建 PASS），但投稿动作无证据。
- 当前 worktree 的 tracked `main.pdf`（hash `56f2fb…`）**与权威终稿不一致**（≠ V026 `D5EC13FE…` ≠ V028 `06D45979…`），**非权威终稿**；权威 = 当前 LaTeX 源 + V026–V028（5 页）。

### 会议稿合法口径（brief 主控纠偏）

三档 downlink GG / 9 dB / 相对 fixed NDA / common-payload BER-ratio / 0.8–1.5 dB / 30 seeds × 400 windows / 两阶段 selector（CV gate + fixed 13 dB effective-SNR）/ 每 256 样本先选后执行 DA/NDA。禁止复活：26/29、uplink、1.2–1.9 dB、3.1 dB、旧 error-floor、旧 Fig.5 轴名。

### Phase A 贡献合同（见 conference-to-thesis-map.md §3）

problem/baseline/method action/information source/core mechanism/primary metric/headline/claim ceiling/图职责/5 页限制未展开项 全部提取。`conference_claim → thesis_extension_question → available_asset → missing_evidence` 映射建立。

### Phase B 按 P0–P5 重聚类（见 conference-to-thesis-map.md §4）

- P0 会议稿已答（Fig.3 翻转 + Fig.4 crossover）。
- P1（SNR 失配）：P01 5-cell 0.32–0.70 dB 损害，adapter 恢复 4/5，`NO_DIAGNOSTIC_SIGNAL`（D040 A-family 封顶）。
- P2（连续 GG）：P04 held-out pooled +0.146 dB < MDE 0.15，**非 OOD-specific**，`ABSENT_ON_CONTINUOUS_GG`（D042 C-family 首包）。
- P3（先选后跑）：branch-routing 990/990 bit-exact（V011 旧参 + V015 formal）；74.6% 单条件不可写；non-genie BLOCKED。
- P4（定点）：P03 gain-bearing regret 约 +0.027 dB < MDE；**无 FPGA 数据，无 float-vs-Q 端到端 BER**。`2026-08-13 D033 纠错`：0/132000 identity 属于 Q(64,40) float-bypass，不属于 Q(8,6)；Q(8,6) 不得写逐窗 identity。
- P5（coded）：P08-R2 完整工具链但 chronology PARTIAL（D051 无 freeze receipt）；通用验证设施非主线。

### Phase C 四包装评估 + 唯一推荐（见 journal-extension-readiness.md）

- **Package A（学位论文扩展）= 唯一推荐**。
- Package B（journal extension）：venue=N/A，当前不足（无新机制/重复过高/Ch5 ceiling 受限），不投。
- Package C（engineering note）/ Package D（边界论文）：独立成稿缺关键证据，归入 Package A 的 Ch5/Ch4。

### Phase D 唯一 thesis blueprint（见 conference-to-thesis-map.md §5）

Ch1 绪论 / Ch2 系统模型 / Ch3 CCISP 主方法（会议主锚）/ Ch4 selector 鲁棒性边界 / Ch5 branch-routed+定点+coded 实现 / Ch6 结论。Ch4 = 鲁棒性贡献（成立非新算法）；Ch5 = 实现贡献（成立限定实现可行性）。**不需要第二算法**。

### Phase E gap-to-package map（见 bounded-package-recommendation.md）

五级分类完成。READY：headline 复算、P02/P04/P11 数字、branch-routing 990/990、P03 identity。SMALL_VALIDATION：统一鲁棒性表（P01+P04）。RECOMPUTE_ONLY→SMALL_VAL：full-grid formal branch-compute timing。NEW_INFRASTRUCTURE：float-vs-Q BER、coded freeze rerun。INVALIDATED：G1/P09、AMC。

### Phase F 唯一小包

统一鲁棒性表（P01 adapter + P04 continuous GG），直接增强 Ch4，预注册 PASS/FAIL，失败仍合规。

### 关键交叉验证修正

1. **全网格 branch-compute timing 存在但仅在 OLD-params 诊断 JSON**（`_a4_branchrouted_30step2.json`，authority=NONE）；**formal B JSON（authority）无 timing 字段**。→ full-grid formal timing = 新跑（RECOMPUTE_ONLY→SMALL_VAL），非 READY。
2. **headline 数字 machine-checkable**：修正 synthesis 过悲观标注——selector_a JSON 每 cell 含 selected_errors/fixed_nda_errors/n_bits=768，G_C 可一行确定性复算 0.8–1.5 dB。

## 结论

CCISP→学位论文 extension packaging 诊断完成。5 个 dossier 文件落盘 `projects/thesis-fso/direction-lab/harvest/`，唯一推荐 Package A（学位论文扩展）+ 唯一小包（统一鲁棒性表）。本轮不改正式论文正文、不跑新实验、不修 Skill、不复活旧口径。投稿状态 = MANUSCRIPT_COMPLETE/SUBMISSION_UNKNOWN，不得声称已投/已录。

## 对决策的影响

- **D023（新建）**：唯一推荐 thesis blueprint（Ch1–Ch6，不产第二算法）。
- **D024（新建）**：唯一推荐小包 = 统一鲁棒性表（P01+P04）。
- 不推翻既有决策；与 D058（campaign 饱和）、D009（AMC 冻结）、D040/D042（A/C-family 封顶/首包）、CCISP D018/D019（三档下行正式闭环）一致。
- 范围扩展属 thesis-writing 专题 2026-08-03 已登记扩展（topic-index 已有记录），本次为该扩展的产物落地，不另开专题。

## 后续

- **下一合法动作**：用户审阅 5 个 dossier + D023/D024；若批准 D024 小包，新对话+新合同(T###)执行统一鲁棒性表（守 FR-22 + D040/D042 + sim-preflight）。
- 若用户要推 journal extension（Package B）：需先补新机制（AMC 需新 GW 授权）或 Ch5 硬件复杂度 + coded freeze，本轮不预设 venue。
- 本轮 commit 一次统一提交（不 push，不动 4 个 p05_run*.log）。
