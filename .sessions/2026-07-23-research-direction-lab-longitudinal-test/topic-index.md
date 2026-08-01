# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 78
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: CAMPAIGN_EXPLORATION_DISPATCH
  authority_pointer: .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D051
  decision_gate: CP029/D038 段A 终止后，用户授权 10-有效包探索 campaign（D039）。在完成 10 个有效科学大包前不因 portfolio 0 READY 要求 thesis pivot。对已完成方法（DA-NDA 选择器等）的新失效条件/鲁棒性做子问题探索；每个 package 遵守 problem-bearing probe → conventional adapter → 条件式 method factory 三阶段门控；至少 5 机制族、同族≤2 连续、第 5 包内部校准不停线、第 10 包 campaign-level 裁决。**D051（2026-08-01）计数纠正（chronology 缺陷 fail-closed）——P08-R2 缺独立 pre-test freeze receipt（单一 commit `a21fdba` 同时含 runner+dev workspace+test raw 8000-8039+verifier+result+治理；`p08r2_run.py:99 main()` 同进程顺序 Step 0→7 无跨进程 immutable freeze；grep freeze/receipt/hash/test_started 零命中；V075 verifier `:332-335` 只验 seed 不相交未核 chronology 闭合），按 confirmatory evidence fail-closed 取代 D049/V075"恢复第 8 包"效力，campaign accepted_valid 8→7，G 族 STOPPED_WITH_PARTIAL_ASSET（D049/V075 engineering asset 维持，不允许 P08-R3/coded/interleaving 换名重开）；D050/V076 NDA-ML STRATEGIC_GATE 维持不动；纠正本身不计有效包（count_excludes=science_integrity_repair）。完成纠正后立即进入重定向 P09 = H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH（换机制族：16APSK BPS search 复杂度优化，对象=`bps_cpr` 真实 B×N exhaustive search 非 NDA-ML body）/CP042/V077**。
  allowed_actions:
    - RECOVER
    - PORTFOLIO_MAP
    - PROBLEM_BEARING_PROBE
    - PREFORMAL_METHOD_FACTORY   # D039 解禁，为本 campaign 服务（problem-first 三阶段门控内）
    - CONDITIONAL_INFRASTRUCTURE  # 有界、独立验证、按需
    - CODED_CHAIN_BUILD   # D047 解禁：仅本 P08-P10 coded-layer package，source-auditable 最小真实 coded baseline
  forbidden_actions:
    - CLOSED_AXIS_REOPEN
    - FREQUENCY_DOMAIN_SUBBAND_FAMILY
    - CB1_COLLAPSE_RECOVERY_FAMILY
    - NDA_ML_BODY_REOPEN          # 已完成赢家（_mve_results.json 全正增益），TL-30
    - G1_SCIENCE_REPAIR           # CP024 bounded asset 已结，TL-30
    - PILOT_JONES_SMALL_AXIS_REOPEN
    - FIBER_IMPAIRMENT_RELOCATED_TO_STAR_GROUND  # D038 段A PHYSICS_BACKED_TESTBED_UNAVAILABLE
    - SUB_SYMBOL_JONES_AXIS_REOPEN        # D066:3415-3416 已关闭
    - FOURTH_IMPAIRMENT_MANUFACTURE       # D038 已穷尽 fiber→星地移植路径
    - FOE_RESIDUAL_CPR_CASCADE_FAMILY     # D041：T030 撤回（1MHz 是 FOE 前 warning 参数非 post-FOE residual；历史多普勒量级远低于 FOE 分辨率；A3 Kill D010 物理）
    - PRIVATE_FULLTEXT_ACQUISITION
    - ABSTRACT_AS_FULLTEXT
    - POST_STEP4A_ADVANCE
    - PROTECTED_HISTORY_EDIT
    - PROTECTED_OWNER_MODIFY
    - FORMAL_MVE
    - PAPER_CLAIM
    - ORACLE_GAP_AS_GO
    - REPRODUCTION_AS_NEW_METHOD   # FR-23：复现旧结果不当新方法，须注入新失效条件
    - A_CPR_SELECTOR_ROBUSTNESS_FAMILY_REOPEN   # D040：A 族达同族上限 2，P01 SNR-mismatch + P02 cand_rank 工作区子轴全关闭（TL-30 禁换名重开 cand_rank/weakretune/region-retune）
    - E_CAUSAL_CROSS_FRAME_HISTORY_FAMILY_REOPEN   # D044：E 族首包 P06 NO_CAUSAL_HISTORY_INCREMENT 后关闭，绑定裁决禁第二个 evaluator-repair 包（TL-30 禁换名重开 cross-frame history / F3-A-repair / temporal-prediction）
    - F_AGC_ADC_DYNAMIC_RANGE_FAMILY_REOPEN   # D046/V072-PART2：P07-R 修复后 PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION（旧 +0.91dB 是 H1 SCALE artifact，corrected 链 W8/W10 regret +0.03~+0.07dB≪MDE；静态低增益即解决，无方法空间），F 族关闭
    - G_CODED_LLR_CALIBRATION_FAMILY_REOPEN   # D051/V077（chronology fail-closed 取代 D049/V075"恢复第 8 包 / G 族关闭"效力）：P08-R2 缺独立 pre-test freeze receipt（单一 commit `a21fdba` 同时含 runner+dev+test raw 8000-8039+verifier+result+治理，`p08r2_run.py:99` 同进程无 immutable freeze，grep freeze/receipt/hash/test_started 零命中，V075 verifier 只验 seed 不相交未核 chronology 闭合）；campaign accepted_valid 8→7，G 族 = STOPPED_WITH_PARTIAL_ASSET（D049/V075 corrected-chain engineering asset 维持：receiver-visible σ²_pre prefix-LS + γ_vis MMSE + metamorphic 门 Δ=0.0 + AST 递归 + 先验 MDE + 去 min(B1,B2)；本地诊断证据 coded loss 主导突发深衰落保留为 PARTIAL diagnostic）；不允许 P08-R3，禁 coded/interleaving 换名重开（TL-30）；若恢复须独立 freeze receipt 重跑
  mission_log_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/mission-log.md
  mission_checkpoint: CP042   # 计数纠正（D051/V077 chronology fail-closed）：P08-R2 缺独立 pre-test freeze receipt（`a21fdba` 单 commit 含 runner+dev+test raw 8000-8039+verifier+result+治理；`p08r2_run.py:99` 同进程 Step 0→7 无 immutable freeze；grep 零命中；V075 `:332-335` 只验 seed 不相交未核 chronology 闭合）→ 按 confirmatory evidence fail-closed 取代 D049/V075"恢复第 8 包"效力，campaign accepted_valid 8→7，G 族 STOPPED_WITH_PARTIAL_ASSET；D049/V075 engineering asset 维持；D050/V076 NDA-ML STRATEGIC_GATE 维持不动；纠正本身不计有效包（count_excludes=science_integrity_repair）。完成纠正后进入重定向 P09 = H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH（换机制族，对象=`bps_cpr` 真实 B×N exhaustive search）。
  next_legal_action: 端到端执行重定向 P09 = H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH（M=16APSK full blind phase search `bps_cpr`；C=有限实时计算预算；A=每 window 对全部相位候选计算星座距离存在 B×N 搜索开销；目标=相同 receiver-visible 信息/相同延迟/相同 BPS objective 下减少 distance/objective evaluations 同时保持 full BPS 性能；换机制族非 NDA-ML body 非 coded/interleaving 轴，过 problem-bearing 入口四门 + 独立 pre-test freeze receipt，Phase A→B→C 门控，独立 verifier 11 项）。禁重开已关闭 A/E/F/G 族及 NDA_ML_BODY_REOPEN/FOE-residual cascade 等所有 forbidden axis；P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 同对象禁换名重提（TL-30）。
```
<!-- RDL-CONTROL:END -->

<!-- RDL-CAMPAIGN-STATE:START — campaign counters (not part of strict control schema) -->
```yaml
rdl_campaign:
  exploration_budget_valid_packages: 10
  accepted_valid_packages: 7   # CP042/V077（chronology fail-closed）：P08-R2 缺独立 pre-test freeze receipt（单一 commit `a21fdba` 同时含 runner+dev+test raw 8000-8039+verifier+result+治理；`p08r2_run.py:99` 同进程无 immutable freeze；grep freeze/receipt/hash/test_started 零命中；V075 verifier `:332-335` 只验 seed 不相交未核 chronology 闭合）→ 按 confirmatory evidence fail-closed 取代 D049/V075"恢复第 8 包"效力，campaign 8→7，G 族 STOPPED_WITH_PARTIAL_ASSET（D049/V075 engineering asset 维持）；D050/V076 P09 NDA-ML STRATEGIC_GATE 维持不计包（count_excludes=entry_preflight_only）；纠正本身不计有效包（count_excludes=science_integrity_repair）
  current_package: P09   # 重定向 P09 = H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH（换机制族，对象=`bps_cpr` 真实 B×N exhaustive search 非 NDA-ML body 非 coded/interleaving 轴；过 problem-bearing 入口四门 + 独立 pre-test freeze receipt + Phase A→B→C 门控）；旧 P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 已 STRATEGIC_GATE 不重提同对象
  mechanism_families_min: 5
  same_family_consecutive_max: 2
  count_excludes: [setup, governance, task_preparation, interface_repair, pure_reproduction, entry_preflight_only, science_integrity_repair]
  mid_calibration_at: P05   # P05 校准已完成（不停线，S005 §mid-calibration）：5 包全 honest negative 0 signal，但族覆盖健康（4 族 A/B/C/D），P05 首个换对象包
  campaign_level_decision_at: P10
  families_started: [A_CPR_SELECTOR_ROBUSTNESS, B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN, C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS, D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION, E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION, F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG, G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL]   # A 关闭(P01+P02)；B/C/D 连续=1；E 关闭(P06)；F 关闭(P07-R)；G STOPPED_WITH_PARTIAL_ASSET(P08-R2 chronology fail-closed，D049/V075 engineering asset 维持，禁 P08-R3)；"≥5 族"已达成（7 族）
  same_family_consecutive: 0   # G 族 STOPPED_WITH_PARTIAL_ASSET 后 P09 重定向换不同机制族（16APSK BPS search 复杂度优化）
    rolling_queue: [P01 DONE CPR-selector-SNR-mismatch-robustness-NO_SIGNAL, P02 DONE cand_rank-operating-regime-PROBLEM_RESOLVED_BY_REGION_RETUNING, P03 DONE fixed-point-codesign-PROBLEM_RESOLVED_BY_UNIFORM_PRECISION, P04 DONE continuous-gg-ood-PROBLEM_ABSENT_ON_CONTINUOUS_GG, P05 DONE ml-equalizer-ood-online-adaptation-PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER, P06 DONE causal-cross-frame-history-NO_CAUSAL_HISTORY_INCREMENT-E-family-closed, P07 INVALIDATED-then-P07R-DONE-PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION-F-family-closed, P08 INVALIDATED-then-P08R-INVALIDATED-then-P08R2-CHRONOLOGY-DEFECT-PARTIAL-ASSET-G-family-STOPPED_WITH_PARTIAL_ASSET, P09 ENTRY-GATE-STRATEGIC-GATE-NOT-COUNTED(COMPUTE_CONSTRAINED_NDA_ML_SEARCH-NDA-ML-closed-form)-then-REDIRECTED-TO H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH-IN-PROGRESS]
```
<!-- RDL-CAMPAIGN-STATE:END -->

> 状态: active（CP042/计数纠正→V077：**campaign accepted_valid 8→7（chronology fail-closed）**——P08-R2 缺独立 pre-test freeze receipt：单一 commit `a21fdba` 同时含 runner（`p08r2_run.py`）+dev workspace+test raw 8000-8039+verifier+result+治理；`p08r2_run.py:99 def main()` 同一 Python 进程顺序 Step 0→7（Step 3 `:168` "freeze metric" 仅进程内步骤顺序，Step 5 `:248` 才读 test seeds），无跨进程/跨 commit immutable freeze point；grep `freeze|receipt|sha256|hashlib|test_started` on 全部 `p08r2_*.py` 零命中；`p08r2_verify.py:332-335` verifier 只验 dev/test seeds 与 history 不相交，**未核 pre-test receipt/source/contract hash 闭合**（V075 19/19 ACCEPT 是 H7/H8/H9 修复+consistency，非 chronology 闭合证明——consistency≠correctness 第四度重演）。按 confirmatory evidence fail-closed：**取代 D049/V075"恢复第 8 包 / G 族关闭"效力**（D049/V075 corrected-chain engineering asset 维持作 PARTIAL reusable asset；本地诊断证据 coded loss 主导突发深衰落保留为 PARTIAL diagnostic），campaign accepted_valid 8→**7**，G 族 = **STOPPED_WITH_PARTIAL_ASSET**（不允许 P08-R3，禁 coded/interleaving 换名重开）。D050/V076 NDA-ML STRATEGIC_GATE 维持不动（NDA-ML 是 closed-form 非 search 源码事实结论维持，不触发 NDA_ML_BODY_REOPEN）。**纠正本身不计有效包**（count_excludes=science_integrity_repair，同 P07-R/P08-R/P08-R2 修复模式）。完成纠正后进入重定向 P09 = `H_16APSK_CONFIDENCE_ADAPTIVE_BPS_SEARCH`（换机制族，对象=`bps_cpr`(`:91-118`) 真实 B×N exhaustive search 非 NDA-ML body 非 coded/interleaving 轴）。CP041/D050/V076 NDA-ML STRATEGIC_GATE 维持；CP040/D049/V075 engineering asset 维持。epoch 78，仍 0 active carrier，active_lane CAMPAIGN_EXPLORATION_DISPATCH）
> 创建: 2026-07-23 | 最后更新: 2026-08-01

## 专题信息

- 上游设计专题：`2026-07-20-research-direction-lab-system`
- 长程权威链：`mission-log.md`
- 详细过程：T###、`projects/thesis-fso/worker-logs/step-###-*`、artifacts、D/V
- 本文件职责：只保存原始目标、当前范围、不变量、当前 gate 和下一合法动作

## 范围边界

### 原始目标（冻结）

在用户只中转 T 路径和四项完成索引的协作方式下，让 fork 主控跨多个真实工作包稳定保持目标、在局部失败后合法换路、控制治理成本，并提高形成可用论文方法与材料的概率；运行一段时间后由原 system design 对话根据磁盘证据审计。

### 当前范围

- T001–T026 的完整 disposition、method delta、轮换和重量见 `mission-log.md` CP001–CP025。
- T019 后产生两个局部 `METHOD_SIGNAL`；T025/T026 形成
  `PACKAGING_BOUNDARY` 与 `WRITING_MATERIAL`，但 active scientific carrier、
  formal method 和当前论文主方法仍均为 0。
- G1 科学线关闭，claim ceiling 保持
  `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`；现有方法卡、小节和图只作次级/扩展资产。
- R009 效果审计与 system D019/V013 最小协议修订均已完成并同步个人 Skill。
- 修订终验后，下一轮 live test 以
  `METHOD_SIGNAL → Step 1–3/3.5/4a → PROMOTION_READY/active carrier`
  的端到端转化作为毕业方法生产成功。
- **2026-07-30 campaign 授权（D039）**：在完成 10 个有效科学大包前不因 0 READY 要求 thesis pivot。
  对**已完成方法**（DA-NDA 选择器 `ccisp_family1_selector_a_30seed.json` 0.8–1.5 dB、SC-NDA-ML `_mve_results.json` 等）
  的**新失效条件/鲁棒性**做子问题探索；每 package 遵守 problem-bearing probe → conventional adapter →
  条件式 method factory 三阶段门控；至少 5 机制族、同族≤2 连续、第 5 包内部校准不停线、第 10 包 campaign 裁决。
  `PREFORMAL_METHOD_FACTORY` 解禁为本 campaign 服务（problem-first 门控内）。

### 明确不含

- 不运行科学实验、重开已关闭轴、进入 Step 5/Contract/Execute 或恢复 science-scout；
- 不修改 session-governance、建设 controller/scheduler、通用基础设施或 per-fork manifest；
- 不获取私有全文，不把摘要冒充全文；
- 不修改 protected history、formal scientific owners 或 thesis framework；
- 不把流程 PASS、包装或写作材料冒充正式方法；
- 不要求用户读取技术日志或判断科学正确性；
- **不换名重开已关闭轴（TL-30）**：NDA-ML 本体 / G1 science repair / CB1 collapse family / Pilot-Jones 小轴 / PMD-PDL-Jones-CD 星地移植；
- **不把复现旧结果当新方法（FR-23）**：每个 package 必须注入新失效条件，复现 anchor 只是基线；
- **不用 oracle/true-truth 当部署输入或 Go 判据（TL-32/FR-25）**：true SNR 只用于生成信号和离线评价。

### 范围变更记录

- **2026-08-01，live D047（scope-change）**：用户授权 P08 coded-chain 场景扩展（voice "行"）。
  - 原因：P05-D/P07-H 撤回 coded chain 的唯一障碍是"无真实 codec"（非"coded 问题无科学价值"）；用户授权建立 source-auditable 最小真实 coded baseline 即移除该 blocker。source-code 事实核查（subagent）确认仓库零 coded 基础设施。
  - 新范围：允许建立来源可审计的最小真实 coded baseline（优先 DVB-S2 LDPC component r2/3 16QAM-BICM；只 LDPC 无 BCH 须称 component），并运行 P08-P10 coded-layer package。新增 family G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL。
  - 明确不含：阈值模型冒充译码 / 随机玩具 LDPC 冒充标准码 / TX-truth LLR 进 deployable decide / 未验证 codec 结果写论文 / 凭记忆手写 DVB-S2 parity / 用临时随机 H / pyldpc 随机码冒充标准 / 凭包名认定 / 悄悄换码率帧长。
  - **执行结果（CP038/V073，2026-08-01 完成）**：DVB-S2 不可闭合（sionna v2.0 已删 DVB-S2 / ldpc 是 QEC / commpy 仅 demo protograph），选 5G NR LDPC（sionna 2.0.1，3GPP TS 38.212 BG2）+ 16QAM Gray BICM over dual-pol SOP。Phase 0B sandbox + 算法正确性门 12 项 ALL PASS + AWGN waterfall 三区。Phase A verdict `PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE`（coded loss 主导是不可恢复突发深衰落，非 LLR 失配；单一 AWGN σ²≈最强传统校准）。Phase B/C 不运行（gate 顺序）。独立 verifier V073 15/15 ACCEPT。
  - 影响：active_lane 维持 CAMPAIGN_EXPLORATION_DISPATCH，authority → D047，epoch 73→74；families_started +G（关闭，PROBLEM_ABSENT），same_family_consecutive=0；新增 allowed CODED_CHAIN_BUILD + forbidden G_CODED_LLR_CALIBRATION_FAMILY_REOPEN；campaign accepted_valid 7→**8**。claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC。仍 0 active carrier、无 protected owner/formal/Skill/thesis framework 改动、无 push。
- 2026-07-23，system D017：建立只受 foreground control 授权的 live-test mission。
- 2026-07-23 至 2026-07-28，formal D062–D066、live D001–D025：Pilot-Jones、
  B10/B12、B1、A4、C15、B9、C16/Q14 等依次运行、拒收、局部 Kill 或返回池；
  逐次理由与边界保留在 `decisions.md`、`verifications.md` 和 CP001–CP017。
- 2026-07-26，system D018 / live D026：旧协议连续 17 包无方法增量，启用
  pre-formal method factory、formal/method 双账和三层记录。
- 2026-07-28 至 2026-07-29，live D027–D033：T019–T025 形成两个诊断 signal、
  一个 bounded package；逐次正式化与拒收理由见 CP018–CP024。
- **2026-07-29，live D034 / system D019**：接收 T026 写作材料并暂停 T027。
  - 原因：R009 确认旧阶段方法增量 0/17，后段 signal→formal 转化仍为 0/2，且真实协作基本每次交互都会压缩。
  - 新范围：只修改恢复三问、工厂硬路由、promotion preflight、事件式 recovery receipt，并压缩 current snapshot。
  - 影响：下一 live test 必须验证 signal→active carrier/`PROMOTION_READY`；包装和写作材料不计毕业方法成功。
- **2026-07-29，live D035 / V061**：T027 入口最小纠偏（用户中转指令）。
  - 原因：原 T027（频域/子带均衡族）未过 problem-bearing testbed preflight 门1——
    `_dual_pol_channel.py:127-132` 信道只有逐符号 GG 幅度、SOP 旋转、AWGN，**无色散/多径/FIR/频率选择性**，
    频域/子带无可作用的物理自由度；其 comparator 也非已确认的传统/任务适配/同信息对象；task-control
    `control_epoch=59` 与 topic epoch 60 不一致（validator `stale_control_epoch`）；`action_class` 写
    preparation 但正文要求运行实验，语义不一致。
  - 新范围：method-production.md 补入口四门（每门 file:line，禁"未测族/REOPENED/testbed 曾产 signal"放行）；
    T027 **原位重写**为唯一四门全过的替代入口（逐符号/更新粒度均衡族，comparator 首选逐符号
    stochastic-gradient CMA），不新建 T028；频域族作 rejected task brief 保留、不运行。
  - 影响：active_lane → `SPRINT003_DISPATCH_READY_ENTRY_REDIRECTED`，authority → D035；
    频域/子带族加入 `forbidden_actions`（`FREQUENCY_DOMAIN_SUBBAND_FAMILY`）；无科学 carrier 变更、
    无 protected history / formal owner 改动。
- **2026-07-29，live D036 / V062**：T027 端到端完成（最终纠偏 → 科学执行 → 独立验证 → 主控接收，用户中转指令，一轮内无停顿）。
  - 最终纠偏（修 D035/T027/V061 证据等级与授权语义）：①门2 证据等级——sprint-001"块末更新几何
    =结构性吸引子原因"已被 V052 拒收，降级为 source-backed 疑似作用点；②comparator 冻结为
    canonical Godard-with-z（`cb1_cell_runner.py:124-129`，禁 `_cma.py` scalar-error 缺 z 冒充），
    μ dev 单独调谐；③action_class→`PREFORMAL_METHOD_FACTORY`（epoch 60→61，不再用 preparation 掩盖
    实验），授权仅本次 bounded sprint；④method-production.md 终态集 3→5（+ `PROBLEM_RESOLVED_BY_
    CONVENTIONAL_COMPARATOR` + `EXECUTION_INVALID`），补 Gate-2 evidence grade + comparator
    gradient identity 两段。
  - sprint-003 执行（commit `689151c`）：4 个更新粒度构造（block-64 anchor、tuned per-symbol
    Godard-with-z comparator、block-8/16、sliding-window recursive），dev 冻结后跑 fresh held-out
    （7 cells × 20 test seeds，禁 seeds 71–80）。独立 verifier V062 **PASS**（梯度身份逐方法核、
    raw→aggregate 独立复算吻合<1e-4、verdict 唯一正确）。verdict = **`NO_DIAGNOSTIC_SIGNAL`**
    （最佳 block8 vs comparator Δ=−0.00293、CI 跨 0、未过 MDE；comparator 只 1/7 cell 消除 collapse）。
  - 影响：CB1 更新粒度均衡族轴关闭（无 signal 即退出）；active_lane →
    `SPRINT003_PREFORMAL_FACTORY_BOUND`；authority → D036；仍 0 active carrier、无 protected owner
    / formal 改动；method-production.md 终态集与 Gate-2/comparator 段更新（同步 Skill）。
- **2026-07-30，live D037 / V063**：CB1 轮换后入口六门评估 → STRATEGIC_GATE（用户中转指令）。
  - 原因：用户要求在 CB1 collapse 家族之外选一个真正 problem-bearing 的新 testbed 跑一次新
    method-factory sprint；主控评估三候选（A 传统 CPR VV 在 adversarial_sourced|snr14 / B NDA-ML
    跨问题扩展 / C U24 high-SOP non-swap BER detection），**无一逐项过六门**：A 门1 FAIL（仅 oracle-gap
    无传统机制失败，TL-32 禁当 Go；组合方法失败属已拒收 B10/B12 实例 master-state:149）+ 门6 FAIL
    （verdict REJECTED）；B 门1 FAIL（NDA-ML 是已完成赢家非失败方法）；C 门4 FAIL（D051 已关闭检测线
    control seeds 有 oracle events；non-swap 标签需 TX-truth oracle 属禁止动作）。候选扫描 problem_truth
    ≥4 四个（U24/U10/U05/U23），U05 hold 且出路阻塞、U23 并入 U24。channel 源物理自由度窄。
  - 新范围：**不开 sprint、不建 T028、不修 protected owner/Skill/thesis framework**；active_lane →
    `STRATEGIC_GATE_AWAITING_USER_DECISION`，authority → D037；新增 `forbidden_actions`：
    `PREFORMAL_METHOD_FACTORY`（暂移除允许，等用户授权新 problem-bearing 入口）、
    `CB1_COLLAPSE_RECOVERY_FAMILY`。无 protected history / formal owner 改动、无 push。
  - 影响：仍 0 active carrier；mission_method_delta `NONE`（STRATEGIC_GATE 非方法进度）；交用户三
    选项决策：(1) 升级 channel 模型（FR-18 ~1 天基础设施），(2) 论文范围决策（G1 bounded + 局部负面
    harvest），(3) 接受 0 carrier 下"协议稳定+可靠负面+1 bounded asset"收尾审计。
- **2026-07-30，live D038 段A→V064 / CP029**：用户选项(1) channel 物理扩展大包段A 三候选六门评估无一过门1-3
  → `PHYSICS_BACKED_TESTBED_UNAVAILABLE`。fiber 现象（PMD/PDL/CD/复 Jones 双折射）无星地物理起源、
  四 primary 零命中、D066 已关 sub-symbol Jones 轴；段B/C/D 不运行、不造第四 impairment。选项(1) 已尽。
- **2026-07-30，live D039 / 用户 campaign 授权**：用户授权至少 10 个有效科学大包的新子问题探索预算；
  完成 10 个有效包前不因 0 READY 要求 thesis pivot。
  - 原因：D038 段A 穷尽了 channel 物理自由度路径（fiber→星地移植不成立），但"该领域无问题可做"不成立——
    用户把对象转向对**已完成方法的新失效条件/鲁棒性**做子问题探索（FR-23 问题驱动，非空白驱动）。
  - 新范围：`PREFORMAL_METHOD_FACTORY` 解禁为本 campaign 服务（problem-first 三阶段门控内）；建立最轻量
    rolling queue（control block 计数器，不建 controller）；至少 5 机制族、同族≤2 连续、第 5 包内部校准不停线、
    第 10 包 campaign 裁决；setup/治理/任务准备/接口修复/纯复现/入口 preflight 不计有效包数。
  - 影响：active_lane → `CAMPAIGN_EXPLORATION_DISPATCH`，authority → D039，epoch 64→65；
    新增 forbidden：`NDA_ML_BODY_REOPEN`/`G1_SCIENCE_REPAIR`/`PILOT_JONES_SMALL_AXIS_REOPEN`/
    `REPRODUCTION_AS_NEW_METHOD`；移除 D038 末"交用户(2)/(3)"等待。仍 0 active carrier、无 protected
    owner/formal/Skill/thesis framework 改动、无 push。P01（CPR 选择器 SNR 失配鲁棒性）本轮立即端到端执行。
- **2026-07-30，live D040 / V066**：P02 cand_rank 工作区确认端到端完成 → `PROBLEM_RESOLVED_BY_REGION_RETUNING`。
  - 原因：P01 留下的条件式子群体信号（cand_rank@weak/低SNR +0.32~+0.43 vs adapter）需 fresh confirmation。
    读新 test 数据前冻结目标区 weak×{5,7,9}、边界 weak@11/moderate@{5,7,9}、MDE=0.15、方法身份全复用 P01
    冻结码、cheap alternative=weakretune（cand_rank body + dev 调谐 ref）。fresh held-out（{60..70}∪{81..89}∪
    {90..99}=30 seed，全 disjoint 历史）primary cand_rank−adapter=+0.3578 [+0.3381,+0.3775] 90/0/0；cheap-alt
    weakretune−adapter=+0.4539（反超 cand_rank）、cand_rank−weakretune=−0.0961 |mean|≤MDE → §5 Step 1 触发
    PROBLEM_RESOLVED_BY_REGION_RETUNING。cand_rank 冻结 ref=9.0 非 load-bearing，dev 调谐同一 conventional
    lever（ref 9→11）即捕获并略超其增益，无可区分 deployable action，不产方法卡/不晋升。
  - 新范围：A 族（CPR 选择器鲁棒性）同族连续=2 达 D039 §4 上限，**关闭**；P03 必须换机制族（B/C/D/E）。
    cand_rank/weakretune/SNR-mismatch/region-retune 子轴关闭，禁换名重开（TL-30）。一次包内确定性修复
    （seed-count 算术 20→30 补 90–99，判据/dev-ref/方法/MDE/§5 顺序全不变，20 与 30 seed verdict 同）已披露。
  - 影响：active_lane 维持 `CAMPAIGN_EXPLORATION_DISPATCH`，authority → D040，epoch 65→66；
    campaign 计数 accepted_valid 1→2、current P02→P03、A 族连续=2（P03 换族重置）；新增 forbidden
    `A_CPR_SELECTOR_ROBUSTNESS_FAMILY_REOPEN`。仍 0 active carrier、claim ceiling `LOCAL_SLICE /
    NONBINDING_DIAGNOSTIC`、无 protected owner/formal/Skill/thesis framework 改动、无 push。
- **2026-07-30，live D041 / V067**：P03 定点/资源-性能协同设计（B 族首包）端到端完成 → `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`。
  - 原因：绑定裁决撤回无效 T030（FOE-residual→CPR cascade 入口）：①1 MHz 是 FOE **前**的 warning 参数
    （`decisions.md:233`：shared channel 保留 `F_RESIDUAL=1 MHz`，是 FOE 步骤要**移除**的 CFO，非移除后残差）；
    ②历史多普勒量级远低于 FOE 分辨率（A3 Kill D010：τ_c~1ms→159Hz，8.2µs 时序下 1MHz/s 仅移 8.2Hz，破 FOE 需 >7.4GHz/s）；
    ③未证明真实 post-FOE residual（FR-26）；④comparator/残差范围未冻结；⑤邻近已关闭 B10/B12。T030 保留 rejected brief
    不计有效 P03。新 P03 = B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN。
  - 执行：对已完成 DA/NDA CPR 选择器注入"定点部署"新失效条件（FR-23 问题驱动）。可信 bit-true Q(W,F) 模型
    （饱和二补码、round-half-up、block-float per-window 共享 exponent、accumulator 加宽 log2(N)+guard、
    非线性算子 I/O 量化），float-bypass 0/132,000 逐 window 决策与浮点 `A.decide` 一致。Phase A uniform
    位宽阶梯 {(6,4)…(16,14)} dev 0–9：uniform(8,6) 已到 regret 地板（gain-bearing 区 +0.027 dB），地板
    branch-statistical（(16,14) Q≤2⁻⁴⁰ 仍持续 +0.685/+0.806 dB @高SNR cell，集中锚点增益本身 ~0 处）。
    Phase B 4 mixed candidate（dev 10–19 tune，held-out 30–49）：最佳 `two_exp(8,6)` Pareto-主导 uniform(14,12)
    但优势 +0.0166 dB = 0.11×MDE=0.15 → `mixed_strictly_better_by_mde=[]`，无可区分 deployable action。
  - 新范围：B 族（定点/资源-性能协同设计）连续=1（首包）。campaign 计数 accepted_valid 2→3、current P03→P04、
    families_started 追加 B。新增 forbidden `FOE_RESIDUAL_CPR_CASCADE_FAMILY`。resource 严格 proxy（无真实综合工具，
    不声称 FPGA LUT/DSP/功耗/吞吐）。仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、
    无 protected owner/formal/Skill/thesis framework 改动、无 push。两次包内确定性修复（float-bypass 分母叙述
    726k→132k；Phase-BC 键名 bug 修复并重跑）已披露。
- **2026-07-30，live D042 / V068**：P04 连续 GG OOD 选择器鲁棒性（C 族首包）端到端完成 → `PROBLEM_ABSENT_ON_CONTINUOUS_GG`。
  - 原因：绑定裁决撤回无效 P04 入口（16APSK 环比失配 + 湍流标签失配）四条 FAIL——①γ（环比）是调制格式配置非当前
    信道随机量；②冻结选择器 `decide(raw,γ_db,γ_lin)` 信息边界干净（不读环比/标签，只读分支输出错误计数）；③matched/
    configured demod 是显然常规解；④两入口均无 selector 可作用面。新 P04 = C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS，合法
    问题改写为"固定/AWGN 拟合的 CV decision boundary 在文献 σ_R²∈[0.2,3.5] 范围内、训练未见过的连续 GG 分布上是否产生
    selector-specific regret"。σ_R²→(α,β) 用 Al-Habash plane-wave 闭式（`system_model.tex:16-21`，验证复现 3 锚点 ≤2.70%）；
    显式 (α,β) 注入经 `generate_shared_realization_apsk(turb_params=...)` 复用 TL-13 共享信道；锚点回归 gate 0 mismatch 证明
    注入忠实。
  - 执行：pooled held-out interior regret = **+0.1459 dB**（CI=[+0.0827,+0.2090]），统计存在（CI_low>0）但**低于冻结 MDE=0.15**；
    dev（seeds 0-9）+0.1393 与 held-out（seeds 30-49）+0.1459 一致（差 0.007 dB）。Phase A problem gate（pooled，冻结于读结果前）
    未过 → Phase B/C 不运行 → `PROBLEM_ABSENT_ON_CONTINUOUS_GG`。诚实子区间：9/30 interior cell 超 MDE 且 CI_low>0（σ_R² 0.3/0.9/
    1.35 × γ 5-11，最强 σ_R²=0.30 γ=9 +0.678 dB），但**非 OOD-specific**——同一 over-NDA-select 在 weak 训练锚点上更强
    （anchor pooled +0.2306 > interior +0.1393；weak 锚点 σ_R²=0.2 γ{5,7,9,11}=+0.39/+0.78/+0.98/+0.56 均 > interior σ_R²=0.45 同 cell）。
  - 新范围：C 族（连续 GG OOD 选择器鲁棒性）连续=1（首包）。campaign 计数 accepted_valid 3→4、current P04→P05、
    families_started 追加 C。无新增 forbidden（16APSK 环比/湍流标签入口属"无作用面"非"换名重开已关闭轴"；连续 GG OOD 是独立
    mechanism family）。一次包内确定性修复（sigma2_to_ab 在 3 训练 σ_R² 用冻结四舍五入锚点对保 byte-exact 回归，内部点用
    Al-Habash）已披露。仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、无 protected owner/formal/
    Skill/thesis framework 改动、无 push。
- **2026-07-30，live D043 / V069**：P05 ML polarization equalizer OOD safe online adaptation（D 族首包，mid-calibration 包）端到端完成 → `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`。
  - 原因：binding decision 撤回 P05-D（FEC/旋转模糊：无真实 codec / threshold eval 非 FEC / TX-bit rotation resolver privileged / pilot resolver 旧线 D032 已裁决）与 P05-E（window/complexity：重复 B1 adaptive phase-window / "NDA 比 VV 复杂"旧担忧不成立 / selector 统计非主计算量 / P03 已覆盖定点轴），上述准备不计有效 P05。新族 = `D_ML_POLARIZATION_EQUALIZER_OOD_SAFE_ONLINE_ADAPTATION`，对象 = `ButterflyCNNEqualizer2x2`（`common/_ml_equalizer.py:104`，双偏振蝶形 CNN MSE 监督，Q-CMA-FADE 方法层，contract H2/B4）——**与 NDA-ML CPR selector（P01-P04 对象）不同方法身份**（不同类别/explore 目录/session）。
  - 执行：Phase 0 身份门 CLOSED（frozen-ML 确定性复现 state_hash byte-identical `03e91429dfed74c6`；corrected StandardCMA2x2 Godard-with-z byte-identical；provenance=当前 params.py strong=(4.2,1.4)，D036 已记 1.5/0.8→4.2/1.4 drift 用当前真值保可复现；in-dist anchor 坐实 D022 修正后不变量 9：ML swap fixed≈0.5 / standard-CMA no-swap fixed≈0）。Phase A fresh problem gate（PRIMARY=fixed-label BER swap-visible，不变量 10；PI-BER swap-blind 报 secondary）：两 cell（anchor N5M/fg30/20dB + provenance-OOD N5M/fg100/20dB，**不提高 SOP/f_G**）fixed-label ML−CMA = +0.4990/+0.4981 CI_low>0 wins=3/3 cma_div_frac=0（CMA 不共同退化）→ 问题成立。Phase B 三 comparator（同预算/prefix-only/receiver-visible）：standard-CMA-continuation recovered=True 两 cell（mean fixed-BER 0.00018/0.00117 ≪ MDE=0.05）；DD-LMS（~0.45，slicer 在 swap 喂错标签锁错盆地）与 periodic-pilot-finetune（~0.499，D032 weak 化身坐实 D032 KILL）均未恢复 → `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`。Phase C 不运行。
  - **mid-calibration（第 5 包内部校准，不停线）**：accepted 序列 P01 NO_SIGNAL / P02 RESOLVED_REGION / P03 RESOLVED_UNIFORM / P04 ABSENT / P05 RESOLVED_BY_CONVENTIONAL —— 5 包全 honest negative 0 signal；族覆盖 4（A 关闭/B/C/D 连续=1）；**P05 是首个换对象包**（前 4 包全 DA/NDA CPR 选择器，P05 换 ButterflyCNN ML equalizer，机制距离显著扩大，非在旧 selector 打转）；可写入 thesis 资产 = Ch3/Ch4 双口径警示（ML swap vs standard-CMA no-swap，contract H2/D023 适用边界）+ D032 KILL 独立佐证 + ML identity freeze 三阶段门控框架。趋势：每新失效条件要么 sub-MDE 要么被常规 comparator 解决；campaign 5/10 半预算仍 0 signal，但族覆盖健康递增。P06 需第 5 机制族（建议 E 信息复杂度边界）。
  - 新范围：D 族（ML equalizer OOD online adaptation）连续=1（首包）。campaign 计数 accepted_valid 4→5、current P05→P06、families_started 追加 D。无新增 forbidden（P05-D/E 撤回是"无作用面/重复"非"换名重开已关闭轴"；D 族是独立 mechanism family；periodic-pilot 作 comparator 仅佐证 D032 KILL 非复活）。三次包内确定性修复（metric-signature PI→fixed-label 不变量10/D018强制；dtype complex128→64；recovered 判据方向）全披露 V069 复核。仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、无 protected owner/formal/Skill/thesis framework 改动、无 push。
- **2026-07-31，live D044 / V070**：P06 E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION（E 族首包，一次性修复型 PROBLEM_BEARING_PROBE，修复旧 F3-A 科学无效性）端到端完成 → `NO_CAUSAL_HISTORY_INCREMENT`。
  - 原因：binding decision 撤回旧 P06（E 信息复杂度边界/window-length，重复 B1 adaptive phase-window + P05-E window/complexity；NDA 已有 whole-window/segmented time support；无真实 latency/resource budget；不能旧机制换名当第五族）。旧 F3-A 科学无效（`run_f3a_history.py:195-196` 把 `max(history_mi)-max(block0_mi)` 边际 MI 最大值之差误标 conditional-MI；`state/current.yaml:161-170`/`portfolio/current.yaml:173-181` 已标 INVALIDATED_AS_CONDITIONAL_MI；旧 +0.060 bits/+0.036 R² 不继承）。新 P06 = E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION，一次性修复型入口，不调窗口/不做 selector/不做 Pilot-Jones/不微调 ButterflyCNN，本轮失败关闭禁第二个 evaluator-repair 包。
  - 执行：M = 冻结 `standard_cma_godard_with_z`（mu=0.03/n_tap=11/R2=1.32/block=64）；C = 源闭合 GG 动态 ρ=exp(-Δt/τ_c) τ_c=1/(2π·f_G)，frame=140k sym（dt=56µs），f_G∈{30,100,1000}Hz → ρ_frame=0.99/0.97/0.70；强湍流 (α,β)=(4.2,1.4)（params.py 真值）。Phase 0 物理身份门 ALL PASS 6 conditions（GG 边缘 KS 0.056-0.144 < 0.15、块 ACF relerr<0.2% 与 ρ^lag 一致、ρ_frame 与 exp(-Δt/τ_c) 一致、冻结 CMA 重跑 relerr=0 byte-identical 0 divergence）。Phase A 严格因果信息门（fresh seeds train200-214/dev215-224/test225-239 全 disjoint 历史 11-150/30-99；trajectory-level split；6 conditions × 40 traj = 4800 frames；features 仅用 frame≤t 接收机可见量，target=下一帧 fixed-label SER/failure，TX 仅离线评分）：dev fail 428/1140 floor=30 MET；test（180 traj 配对）history-expanded ridge R²=0.320 > current-only 0.040（MSE 减少per-traj macro mean=2.25e-02 CI=[4.72e-03,4.68e-02] CI_lo>0，严格因果增量统计存在）**但 persistence R²=0.853（EWMA 0.853/AR1 0.848）远优 history**；逐 condition（含动态 fg1000 ρ=0.70）persistence 0.68-0.95 全胜 history 0.04-0.88 → 更便宜常规 temporal baseline 已远优解决 → **`NO_CAUSAL_HISTORY_INCREMENT`**。Phase B/C 不运行（gate 顺序）。verifier V070 **7/7 ACCEPT**（causality alignment/truth-future leakage/trajectory split/raw→aggregate/ACF/seed discipline/verdict 唯一性与逻辑全过；dev_fail raw=428=reported；ACF relerr<0.2% 全 condition；test seed 与历史零重叠；history features 仅 frame≤t）。
  - 新范围：E 族（因果跨帧历史信息）连续=1 首包即关闭（绑定裁决禁第二个 evaluator-repair 包）。campaign 计数 accepted_valid 5→6、current P06→P07、families_started 追加 E（**第 5 族"≥5 族"达成**）。新增 forbidden `E_CAUSAL_CROSS_FRAME_HISTORY_FAMILY_REOPEN`。无包内确定性修复（一次跑通）。仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、无 protected owner/formal/Skill/thesis framework 改动、无 push。旧 F3-A `state/current.yaml`/`portfolio/current.yaml` INVALIDATED 标记不动。
- **2026-07-31，live D045 / V071**：P07 F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG（F 族首包）端到端完成 → `NO_DIAGNOSTIC_METHOD_SIGNAL`。
  - 原因：binding decision 撤回旧 P07-entry 的 F（symbol-timing offset）/G（场景扩展）/H（FEC/APSK）三条未冻结扫描。三条独立 FAIL：①F——`_channel.py:97-169`/`_dual_pol_channel.py` 信道只有逐符号 `signal=tx*sqrt(h)*carrier`+AWGN，**无过采样/脉冲成形/分数延迟**（grep `oversamp|pulse_shape|rrc|upsample|fractional_delay` 零命中），1-sps 下 timing offset 无可作用物理自由度；②G——未冻结 M-C-A 且易重入已关闭 P04（连续 GG OOD）/FOE-residual 轴；③H——coded chain blocked（P05-D 撤回：无真实 codec）+ APSK 环比入口 P04 已撤回（γ 是调制配置非信道随机量，selector 不读环比）。保留 rejected brief，**不计有效 P07**。新 P07 = `F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG`（candidate-universe.yaml U07），**严格区别于 P03**（P03=selector 内部定点 Q(W,F) 数字后处理；P07=模拟前端 AGC+ADC 作用于 rx_raw 在整个冻结接收链之前）。
  - 执行：M=冻结接收链（`run_case_multidelta` per-window：blind/pilot MMSE+`A.per_block`+`A.decide`+离线 BER）；C=源闭合 GG 动态幅度（α,β∈{weak/moderate/strong}，SNR 5/9/13/17/21 dB，N_DFT=256/block，400 windows/cell，f_dot=150e6，mod='m16apsk'）；A=固定增益在两损害间折中——过高→峰值 clipping，过低→深衰落有效量化分辨率不足。Phase 0 可信因果 AGC/ADC adapter ALL 5 BLOCKER gates PASS（signed I/Q quantizer round-half-up+饱和不 wrap+signed 对称；float-bypass 重构≤2^-40；**float-bypass 接收链 byte-identical `run_case_multidelta`**；window-0=nominal 因果性；AGC class 体+`quantize_iq` 体零 forbidden 子串 AST）。Phase A 问题成立（dev-best fixed-gain g=0.75 regret **+1.028/+0.924/+0.909 dB** across W6/8/10，CI_low 全>0，14-15/15 cell ≥MDE=0.15；clipping rate 随 gain 单调 g0.5→2.5%/g0.75→15%/g1.0→30%/g4.0→91%，低 gain 侧分辨率损失高 gain 侧峰值 clipping——**clipping–resolution 折中真实存在**）。Phase B 最强传统 AGC=causal-RMS 把 regret 降到 **+0.896/+0.794/+0.767 dB**（缓解 0.12-0.20 dB，仍 5-6×MDE，`conv_resolves=False` 未解决）。Phase C 4 候选（dual-tc/clipping-aware/robust-pct/hysteretic）paired delta（conv−cand）最佳 dual_tc = **−0.016/−0.004/−0.017 dB** CI 全跨 0（|Δ|≪MDE），clipping_aware/robust_pct/hysteretic 全 ≤0 更差 → **`NO_DIAGNOSTIC_METHOD_SIGNAL`**（问题真实存在、常规 AGC 部分缓解、无方法增量）。
  - 新范围：F 族（AGC/ADC 动态范围）连续=1（首包，NO_SIGNAL 未关闭，P08 可选 F 第 2 包连续≤2）。campaign 计数 accepted_valid 6→**7**、current P07→P08、families_started 追加 F（第 6 族）。无新增 forbidden（F/G/H 撤回是"无可作用物理自由度/重入已关闭轴"非"换名重开已关闭轴"；F 族是独立新 mechanism family）。一次包内确定性修复（Phase-BC JSON 序列化 numpy bool_ bug → `_to_jsonable` 递归转 native 后重跑，计算/数据/verdict 全不变，V071 V10 复核 raw→aggregate relErr≤1e-9）已披露。仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、无 protected owner/formal/Skill/thesis framework 改动、无 push。

- **2026-08-01，live D048 / V074**：P08 coded-chain 科学完整性修复（P08-R，SCIENCE_INTEGRITY_REPAIR，不计有效包数）端到端完成 → `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`。
  - 原因：用户 P08-R 执行指令冻结旧 P08 科学结论（V073 ACCEPT / PROBLEM_ABSENT_AFTER_STRONG_LLR_BASELINE / G 族关闭 / accepted_valid=8 全部撤回），要求 systematic-debugging 全流程修复六项科学合同缺陷。
  - 六根因（p08r_prefail_evidence.md 逐 file:line）：H1 GG provenance（硬编码 (α,β) 与 params.py 脱钩且档位错位）/ H2 runtime information（σ²=1/(2γ_bar) 来自循环变量）/ H3 oracle action space（单 global scalar 不覆盖候选）/ H4 metric contract（Primary A 全 inf 静默退 raw FER-delta，MDE 从未生效）/ H5 coded identity（未传 num_bits_per_symbol，worker-log 谎称 triangle interleaver）/ H6 state lifecycle（16 cw 当独立样本，raw 缺逐 cw 证据）。
  - 执行：coded-chain 身份冻结 option A（真 3GPP §5.4.2.2 interleaver，out_int 1534/1536 moved）→ 新建 p08r_* 修正链（GG params import/receiver-visible prefix σ²/O0-O1-O2 oracle ladder/重新冻结 metric/trajectory-cluster）→ fresh seeds（dev 6000-6019/test 7000-7039 disjoint history）→ frozen cell weak@1000Hz@12dB（dev B0 FER=0.169）→ test mean FER B0/B1/B2/O0/O1/O2=0.115/0.115/0.113/0.115/0.115/0.109 → Δ(B0−O2)=+0.0055 CI=[0,0.014]≪MDE_fer=0.2347 → mechanism decomposition 4/40 不可恢复深衰落（O2 也译不出，h_truth 0.29-0.41）→ PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE。
  - 新范围：G 族（coded-LLR-calibration）**关闭**（corrected chain 下 coded loss 主导仍是不可恢复突发深衰落 10% trajectory，非 LLR 失配；单一 receiver-visible σ²≈最强传统校准，oracle 仅 0.55% FER headroom≪MDE）。campaign 计数 accepted_valid 7→**8**（恢复）、current P08-R→P09（入口准备不运行）。新增 forbidden `G_CODED_LLR_CALIBRATION_FAMILY_REOPEN`（取代旧 V073 版本，注明 corrected chain 下同 verdict）。D048 取代 D047 科学有效性部分（入口裁决仍 active）；V074 取代 V073 科学层（V073 保留标"合同一致性通过但科学合同六项漏审"）；旧 artifacts 加 INVALIDATED_BY_P08R.md 保留不删。P08 codec/AWGN 基础设施保留为 PARTIAL reusable asset（interleaver 激活/(α,β)import/σ²来源/oracle 粒度/统计单位全部修复）。future-work seed（非缺陷）：equalize 盲 h 估计用 gamma_bar 作噪声底。
  - 影响：active_lane 维持 CAMPAIGN_EXPLORATION_DISPATCH，authority → D048，epoch 74→75；仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、无 protected owner/formal/Skill/thesis framework 改动、无 push。
- **2026-08-01，live D049 / V075**：P08-R2 receiver 信息边界 + AST 门 + 统计功效合同三根因修复（P08-R2，SCIENCE_INTEGRITY_REPAIR，不计有效包数）端到端完成 → `PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`（同物理机制，但这次在真正 γ-free corrected receiver 链下得出）。
  - 原因：用户 P08-R2 执行指令冻结 P08-R 科学结论（V074 ACCEPT / G 族关闭 / accepted_valid=8 撤回），指出 V074 漏审三项承重科学合同（H7 receiver 仍读 true SNR / H8 AST 不递归 / H9 统计合同非法），要求 systematic-debugging 全流程修复。
  - 三根因（p08r2_prefail_evidence.md 逐 file:line + p08r2_h7_reproduce.json 数值复现）：H7（`p08r_chain.py:341-360` equalize 读 self.gamma_bar 三处——盲 h 噪声底/h_est/mmse_equalize 第3参；数值复现 max\|ΔeqX\|=0.145/max\|ΔLLR\|=7.02 证 deployable decide 间接消费 true SNR）/ H8（`p08r_verify.py:109-129` check #5 只扫 method 函数体字面不递归进 real.equalize → 漏审 H7；sub-agent 把 equalize gamma_bar 错标 "future-work seed 非缺陷" 被 H7 数值复现证伪）/ H9（MDE=0.2347 是固定 n=40 后 power 阈值非先验；CI_lo=0 当排除；`p08r_run.py:286 strongest_conv=np.minimum(B1,B2)` per-trajectory cherry-pick）。
  - 执行：新建 p08r2_* 修正链（不动 p08r_*）——`estimate_pre_eq_noise_from_prefix` 用 32-sym prefix LS 解 2×2 H_eff（4 复未知数/64 方程/60 dof）得 receiver-visible σ²_pre；`CodedRealizationR2.equalize` 用 σ²_pre（替代 1/(2γ)）+ γ_vis=1/σ²_pre（替代 gamma_bar）传 mmse_equalize；amp_limit(3.0) 固定绝对 clip 保留；B0/B1/B2 的 post-eq σ²（demapper）不变。metamorphic 门：固定 realization 只翻 gamma_bar (6-22dB)，max\|Δeq\|/max\|ΔLLR\|=**0.0 精确**（H7 修复 runtime 铁证）。正确功效设计：先验 MDE=0.05（非 post-hoc）/ B2 单一 comparator（去 min(B1,B2)）/ EVIDENCE_INSUFFICIENT 终态（CI_hw>MDE/2）。fresh seeds（dev 9000-9019/test 8000-8039，disjoint from P08-R 6000-6019/7000-7039 + campaign history）→ frozen cell weak@1000Hz@12dB → test mean FER B0/B1/B2/O0/O1/O2=0.155/0.155/0.148/0.155/0.153/0.139 全聚集 → Δ(B0−B2)=+0.0063 CI=[+0.0008,+0.0141] hw=0.0066；Δ(B2−O2)=+0.0094 CI=[+0.0016,+0.0195] hw=0.0090 ≪ MDE=0.05 → mechanism 3/40 不可恢复深衰落 traj（O2 也 2/40 译不出）→ PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE。
  - 独立 verifier：V075 脚本 19/19 PASS（含 H7 递归 AST 0 违规 + metamorphic 门 Δ=0.0 + H9 先验 MDE + 无 min(B1,B2) + EVIDENCE_INSUFFICIENT 可达 + fresh seeds + raw→aggregate relErr=0.0）+ 独立 sub-agent（fresh context，不信任 executor）7 项全 ACCEPT（H7 leak 复现/H7 fix 正确/metamorphic runtime/H8 verifier 递归/H9 统计/fresh seeds/verdict sanity+recompute），无 executor 自述与实际差异。
  - 新范围：G 族（coded-LLR-calibration）**关闭**（真正 γ-free corrected chain 下 coded loss 主导仍是不可恢复突发深衰落 3/40 traj，非 LLR 失配；oracle B2-O2 headroom +0.0094≪MDE）。campaign 计数 accepted_valid 7→**8**（恢复）、current P08-R2→P09（入口准备不运行）。更新 forbidden `G_CODED_LLR_CALIBRATION_FAMILY_REOPEN`（取代 V074 版本，注明 γ-free corrected chain 下同 verdict + H7/H8/H9 修复）。D049 取代 D048 科学有效性部分（GG/oracle/identity/H4-H6 修复 + D047 入口裁决仍 active 作 PARTIAL reusable asset）；V075 取代 V074 科学层（V074 保留标"16/16 consistency + H1-H6 PASS 但 H7/H8/H9 漏审"）；旧 P08-R artifacts 加 INVALIDATED_BY_P08R2.md 保留不删。D048 PARTIAL 资产（5G NR LDPC/CodecAdapterR/真 3GPP interleaver/GG params import/O0-O1-O2 ladder/H4 dev-freeze/H6 trajectory-cluster）在 p08r2_chain.py verbatim 复用。
  - 影响：active_lane 维持 CAMPAIGN_EXPLORATION_DISPATCH，authority → D049，epoch 75→76；仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、无 protected owner/formal/Skill/thesis framework 改动、无 push。**TL 教训登记**：P07-R/D046 → P08/D048 → P08-R2/D049 是 "consistency≠correctness" 教训三度重演——verifier 必须递归遍历 deployable 调用图（不只复述合同/扫函数体字面）+ 跑运行时 metamorphic 门；此条作为 sim-preflight mve-validation.md 强化项候选（跨 session 沉淀）。
- **2026-08-01，live D050 / V076**：P09 `COMPUTE_CONSTRAINED_NDA_ML_SEARCH` 入口门裁决 **STRATEGIC_GATE**（不计有效包）。
  - 原因：用户授权 P09 端到端执行，冻结问题 M = "当前 full-search NDA-ML"、A = "均匀穷举大量候选导致计算冗余"、双门 B（objective evaluations 减少 ≥4× + 性能非劣 ≤0.10 dB）、最强廉价 comparator = "dev-tuned uniform coarse grid"，并明文允许"若无法证明计算问题或 novelty boundary，终止为 STRATEGIC_GATE，不计包"。入口门源码核查（主线程 Read + grep 零命中 + Explore 子 agent fresh context 交叉）证伪承重前提 A：NDA-ML（`common/_recovery.py:171-273` `nda_ml_recovery`，D005 Go/D007 修正后的 GW Step 4a 维度 D 验证赢家）是 closed-form 解析估计（升 M0=8 幂去调制 + `np.angle(raised.mean())` 整块 / K=8 段每段一次 `np.angle(raised[lo:hi].mean())` / 单次 FFT argmax+Quinn-Rife），**无 candidate 枚举、无 objective 在候选集上求值、无可裁剪搜索结构**。生产 driver `sc_nda_ml_sim.py:180-187` 逐块调一次 closed-form。grep `full-search|exhaustive|candidate|grid_search|phase_grid|coarse|coarse-to-fine|hierarchical|objective.*eval|enumerate` on `_recovery.py`/`sc_nda_ml_sim.py`/`_b11_params.py` 零命中。代码库唯一 exhaustive search `bps_cpr`（`_recovery.py:91-118`）是 Pfau 2009 竞争对手非 NDA-ML 本体（ADVISOR_BRIEFING 报 NDA-ML ≈ BPS 0.006-0.14 dB）。`_db_caliber_and_complexity.md:51-61` NDA-ML 已 16 mult/symbol（VV 24），无 coarse-grid/coarse-to-fine/hierarchical comparator 存在。
  - 裁决：method-production 入口四门 3 FAIL（门1 NDA-ML 估计器内无 search 自由度可裁剪 / 门2 无 lever 可作用 / 门3 dev-tuned coarse grid 无网格可 coarse 化；门4 file:line 已举）；双门 B primary cost metric 失效（无 objective eval 可数）；Phase A 备选终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_COARSE_SEARCH 不适用（语义前提是存在 search 可被 coarse grid 解决，这里连 search 都没有）；动估计器本体减计算（跳块/块间状态复用/换升幂/减 K 段）= 替换研究对象且触发 `NDA_ML_BODY_REOPEN` forbidden，双重禁止。STRATEGIC_GATE 是唯一合法终态。
  - 新范围：**不重开 G 族**（P09 入口否非 G 新证据，维持 D049 关闭）；**不重提 P09 同对象**（COMPUTE_CONSTRAINED_NDA_ML_SEARCH 承重前提证伪，换名重提同 NDA-ML-low-complexity 框架属 TL-30 禁换名重开）；不触发同族连续计数（P09 未启动新族）；不改 protected owner/formal/Skill/thesis framework。
  - 影响：active_lane 维持 CAMPAIGN_EXPLORATION_DISPATCH，authority → D050，epoch 76→77；campaign accepted_valid 维持 **8/10**（P09 不计包，count_excludes=entry_preflight_only，同 CP028/CP029 入口评估无 sprint 先例）；current 维持 P09（入口已否待重指定）；same_family_consecutive 维持 0；仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`、无 protected owner/formal/Skill/thesis framework 改动、无 push。下一合法动作：重新指定 P09 入口（须过 problem-bearing 入口四门，禁重开已关闭 A/E/F/G 族及 NDA_ML_BODY_REOPEN/FOE-residual cascade 等所有 forbidden axis），或用户授权 P10 campaign-level 裁决。

## 已确认结论

### 不变量

- 顶部 control 只绑定前台动作，不拥有科学事实。
- conversation summary 只定位文件，不能改变 active lane。
- `topic-index.md` 是当前快照；`mission-log.md` 是完整紧凑长链；T/worker/artifact 保存包细节。
- 每个执行包关闭一个科学决策不确定性，但可包含多个有界动作。
- formal science disposition 与 mission method delta 必须分账。
- candidate 轮换留在 exploration mission；formal 晋级才新建或恢复 formal topic。
- executor 不修改 formal/current/mission owners；master 接收后更新。
- MVE 执行与科学验收分离，用户不承担技术正确性判断。
- 包装、写作材料和可靠负面都可 harvest，但不自动成为主方法。

### 其他结论

- CP001–CP017 的状态保存基本成功，方法生产失败；问题主要是动作路由，不只是记忆丢失。
- T019 后工厂显著提高近端发现速度；当前端到端 formal-method yield 为 0/2。
- G1 的最佳位置是高阶调制扩展、discussion、附录或未来工作，不是当前主贡献。
- 恢复效果过去只有静态证据；RC001 首次显式记录，但耗时与读取数因规则生效前未测。

## 进展线索

| 阶段 | 结果 | 权威入口 |
|---|---|---|
| CP001–CP007 | phase 1：多次 semantic/identity 修复，0 方法增量 | mission-log |
| CP008–CP017 | Goal/形式化链：10 包连续 drift/stall，累计 17/17 `NONE` | mission-log |
| CP018–CP019 | T019/T020 方法工厂：第 2 包产生首个因果诊断 signal | mission-log |
| CP020–CP023 | Q15→G1 formalization：产生第二 signal，但 formal conversion 失败 | mission-log |
| CP024–CP025 | G1 bounded package→论文小节与两图；science ceiling 不变 | mission-log / T025–T026 |
| R009 / D034 | 纵向效果审计完成；进入 system D019 最小修订 | R009 / decisions.md |
| S003 | 下一入口选择：两 signal preflight=STRATEGIC_GATE，硬路由 method factory | S003 |
| S003→D035/V061 | T027 入口纠偏：频域/子带族 preflight 门1 失败（无物理自由度）撤回；原位重写为逐符号/更新粒度均衡族（四门全过），comparator=逐符号 SGD-CMA | S003 / T027 / V061 |
| S003→D036/V062 | T027 端到端完成（最终纠偏+执行+验收一轮内无停顿）：verdict `NO_DIAGNOSTIC_SIGNAL`；CB1 更新粒度族轴关闭；疑似作用点（块末更新）因果性未被确认（collapse 在所有更新粒度下持续） | T027 / sprint-003 `689151c` / V062 |
| S003→D037/V063 | CB1 轮换后三候选六门评估无一过门（A CPR/VV 仅 oracle-gap + verdict REJECTED；B NDA-ML 已完成赢家；C U24 检测线 D051 关闭 + 需 oracle 标签）；U05 hold 出路阻塞、U23 并入 U24；channel 物理自由度窄 → `STRATEGIC_GATE`，不制造第四弱候选 | D037 / V063（无 sprint/无 commit） |
| S003→D038 段A/V064 | 用户选项(1) channel 物理扩展大包段A 三候选（complex time-varying Jones / PDL / PMD-色散-跨符号记忆）六门评估无一过门1-3 → `PHYSICS_BACKED_TESTBED_UNAVAILABLE`：fiber 现象无星地物理起源（各向同性大气无 birefringence）、四星地 primary 零命中、sat.1553 等三篇 dangling、唯一可溯源参数 D066 实测 headroom 0.0804dB≪0.5dB、时变复 Jones 轴已被 D066:3415-3416 关闭；段B/C/D 不运行、不造第四 impairment、诚实终止 | D038 / V064 / CP029（无 sprint/无 commit） |
| D039 / P01→V065 | 用户授权 10-有效包探索 campaign（不因 0 READY 要求 thesis pivot）；P01 = CPR 选择器 SNR 失配鲁棒性端到端执行：Phase A 问题成立（weak@5/7/9 δ=−3 / weak@11 δ=+3 / moderate@13 δ=+3 损害≥0.3dB CI<0）→ Phase B 非相干 pilot adapter 恢复 4/5 cell → Phase C 5 候选最佳 cand_rank pooled +0.1358 未过 MDE=0.15 → `NO_DIAGNOSTIC_SIGNAL`；verifier 8/8 PASS；条件式子群体信号 cand_rank@weak/低SNR 降级 future-work | D039 / V065 / CP030 / worker-log step-028（无独立 commit，待主控统一） |
| D040 / P02→V066 | P02 cand_rank 工作区确认（A 族第 2 包=上限）：fresh confirmation P01 条件式子群体信号。读新数据前冻结目标区/边界/MDE=0.15/方法身份全复用 P01 冻结码/cheap-alt=weakretune(dev 调谐 ref)。dev(50–59)选 ref=11.0；fresh held-out({60..70}∪{81..89}∪{90..99}=30)primary cand_rank−adapter=+0.3578[+0.3381,+0.3775]90/0/0；cheap-alt weakretune−adapter=+0.4539反超、cand_rank−weakretune=−0.0961|mean|≤MDE → §5 Step 1 触发 `PROBLEM_RESOLVED_BY_REGION_RETUNING`。cand_rank ref=9.0 非 load-bearing，同一 conventional lever dev 调谐即超，无可区分 deployable action，不产方法卡/不晋升。verifier 8/8 PASS（raw→aggregate 0.000e+00、seed 零碰撞、git diff 冻结文件空、true γ 绝不进 decide、独立重跑字节级一致）。A 族关闭，P03 必须换族 | D040 / V066 / CP031 / worker-log step-029（无独立 commit，待主控统一） |
| D041 / P03→V067 | P03 定点/资源-性能协同设计（B 族首包）：绑定裁决撤回无效 T030（FOE-residual→CPR，1MHz 是 FOE 前 warning 参数非 post-FOE residual），新 P03 = B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN。对已完成 DA/NDA 选择器注入"定点部署"新失效条件（FR-23）。可信 bit-true Q(W,F) 模型（饱和二补码/round-half-up/block-float 共享 exponent/accumulator 加宽/非线性 I/O 量化），float-bypass 0/132,000 逐 window 决策与浮点 `A.decide` 一致。Phase A uniform 阶梯 {(6,4)…(16,14)} dev 0–9：uniform(8,6) 已到 regret 地板（gain-bearing +0.027 dB），地板 branch-statistical（(16,14) Q≤2⁻⁴⁰ 仍持续，集中高 SNR 锚点增益 ~0 处）。Phase B 4 mixed candidate（dev 10–19/held-out 30–49）：最佳 two_exp(8,6) Pareto-主导 uniform(14,12) 但 +0.0166 dB = 0.11×MDE → `mixed_strictly_better_by_mde=[]`，无可区分 deployable action → `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`。verifier V067 10/10 PASS（raw→aggregate 0.000e+00、float-bypass 独立重跑 0/48000、信息边界 AST 干净、resource 措辞严格 proxy）。不产方法卡/不晋升。resource proxy（op×bit/storage_bit）明确标 proxy 无真实综合 | D041 / V067 / CP032 / worker-log step-030（无独立 commit，待主控统一） |
| D042 / P04→V068 | P04 连续 GG OOD 选择器鲁棒性（C 族首包）：绑定裁决撤回无效 16APSK 环比/湍流标签入口（四条 FAIL：γ 是调制配置非信道随机量、selector 不读环比/标签、matched demod 常规解、无作用面），新 P04 = C_CONTINUOUS_GG_OOD_SELECTOR_ROBUSTNESS。合法问题"AWGN 拟合 CV 边界在连续 GG 形状 OOD 下是否产生 selector-specific regret"。σ_R²→(α,β) 用 Al-Habash 闭式（`system_model.tex:16-21`，验证复现锚点 ≤2.70%）；显式 (α,β) 注入经 `generate_shared_realization_apsk(turb_params=...)`；锚点回归 gate 0 mismatch。pooled held-out interior regret **+0.1459 dB**（CI=[+0.0827,+0.2090]）<冻结 MDE=0.15；dev +0.1393 一致（差 0.007）。Phase A 门（pooled，读结果前冻结）未过 → Phase B/C 不运行 → `PROBLEM_ABSENT_ON_CONTINUOUS_GG`。诚实子区间 9/30 cell > MDE（σ_R² 0.3/0.9/1.35 × γ 5-11，最强 +0.678 dB）但非 OOD-specific（weak 训练锚点 regret +0.39/+0.78/+0.98/+0.56 更强；anchor pooled +0.2306 > interior +0.1393）→ selector 是通用 NDA-over-selector，连续 GG 形状不让边界退化。verifier V068 8/8 PASS（raw→aggregate 0.000e+00、锚点门独立重跑 0 mismatch、seed 隔离干净、信息边界 AST 干净、冻结文件未改、verdict 唯一正确、子区间诚实）。不产方法卡/不晋升。weak-side-low-SNR 子区间作 future-work seed 与已关闭 A 族重叠不重开 | D042 / V068 / CP033 / worker-log step-031（无独立 commit，待主控统一） |
| D043 / P05→V069 | P05 ML polarization equalizer OOD safe online adaptation（D 族首包，mid-calibration 包）：binding decision 撤回 P05-D（FEC/旋转模糊：无真实 codec/threshold eval 非 FEC/TX-bit rotation privileged/pilot resolver D032 旧线）+ P05-E（window/complexity：重复 B1/NDA 比 VV 复杂不成立/selector 非主计算量/P03 已覆盖定点轴），新族 D 对象=ButterflyCNNEqualizer2x2（**≠ NDA-ML CPR selector**）。Phase 0 身份门 CLOSED（frozen-ML 确定性复现 state_hash byte-identical `03e91429dfed74c6`；corrected StandardCMA2x2 Godard-with-z byte-identical；provenance=当前 params.py strong=(4.2,1.4)；in-dist anchor 坐实 D022 修正后不变量 9：ML swap fixed≈0.5 / standard-CMA no-swap fixed≈0）。Phase A PRIMARY=fixed-label BER（swap-visible 不变量 10；PI-BER swap-blind 报 secondary）两 cell（anchor N5M/fg30 + provenance-OOD N5M/fg100，**不提高 SOP/f_G**）fixed-label ML−CMA=+0.4990/+0.4981 CI_low>0 wins=3/3 cma_div_frac=0 → 问题成立。Phase B standard-CMA-continuation recovered=True 两 cell（mean fixed-BER 0.00018/0.00117≪MDE=0.05）；DD-LMS（~0.45 slicer 错标签）/periodic-pilot（~0.499 D032 weak 化身坐实 KILL）均未恢复 → **`PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`**。Phase C 不运行。verifier V069 ACCEPT（10/10 + 方法身份非混淆全 PASS；raw→aggregate relErr=0；gate/预算公平/Phase-C 抑制/verdict 唯一性源码级验）。不产方法卡/不晋升。harvest：Ch3/Ch4 双口径警示（强化 H2/D023 适用边界 + 不变量 9/10/11）+ D032 KILL 独立佐证 + ML identity freeze 三阶段门控框架。**mid-calibration**：5 包全 honest negative 0 signal，族覆盖健康 4 族 A/B/C/D，P05 首个换对象包（非旧 selector 打转）。3 次包内确定性修复（metric-signature/dtype/recovered-logic）全披露 | D043 / V069 / CP034 / worker-log step-032（无独立 commit，待主控统一） |
| D044 / P06→V070 | P06 E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION（E 族首包，一次性修复型 PROBLEM_BEARING_PROBE，修复旧 F3-A 科学无效性）：binding decision 撤回旧 P06（E 信息复杂度边界/window-length 重复 B1/P05-E 四条 FAIL），新 P06 修复旧 F3-A（`run_f3a_history.py:195-196` marginal-MI max-diff 误标 conditional-MI；旧 +0.060 bits/+0.036 R² 不继承）。M=冻结 standard_cma_godard_with_z；C=源闭合 GG ρ=exp(-Δt/τ_c) frame=140k sym dt=56µs f_G∈{30,100,1000} ρ_frame=0.99/0.97/0.70。Phase 0 物理身份门 ALL PASS 6 conditions（GG 边缘 KS 0.056-0.144、块 ACF relerr<2%、冻结 CMA 重跑 relerr=0）。Phase A 严格因果信息门（fresh seeds 全 disjoint 历史，6 cond×40 traj=4800 frames，trajectory-level split，features 仅 frame≤t）：history-expanded ridge R²=0.320 > current-only 0.040（MSE 减少per-traj macro CI=[4.72e-03,4.68e-02] CI_lo>0 严格因果增量统计存在）**但 persistence R²=0.853 远优**（逐 condition 含动态 fg1000 persistence 0.68-0.95 全胜 history 0.04-0.88）→ **`NO_CAUSAL_HISTORY_INCREMENT`**。Phase B/C 不运行。verifier V070 **7/7 ACCEPT**（causality/leakage/split/raw→aggregate/ACF/seed/verdict 全过）。不产方法卡/不晋升。harvest：Ch3/Ch4 receiver-observability 边界（跨帧信息被帧间持续性主导）+ 方法论附录教训（marginal-MI≠conditional-MI）+ 物理诚实资产（deployable frame rate≪τ_c 跨帧动力学边界）。**第 5 族"≥5 族"达成**。E 族首包即关闭（禁第二个 evaluator-repair 包）。无包内确定性修复（一次跑通） | D044 / V070 / CP035 / worker-log step-033（无独立 commit，待主控统一） |
| D045 / P07→V071 | P07 F_AGC_ADC_DYNAMIC_RANGE_UNDER_GG（F 族首包，**≠ P03 定点**）：binding decision 撤回旧 P07-entry F/G/H 扫描三条 FAIL。旧 P07 verdict `NO_DIAGNOSTIC_METHOD_SIGNAL`（Phase A +0.91~+1.03 dB / Phase B causal-RMS +0.77~+0.90 dB / Phase C 4 候选无增量）。**⚠️ 科学结论已被 D046/V072 取代——见下行**。V071 10/10 ACCEPT 但只查 consistency（保留标"合同一致性通过但物理正确性漏审"）。1 次包内确定性修复（Phase-BC JSON bool_ bug）。 | D045 / V071 / CP036 / worker-log step-034 |
| D046 / P07-R→V072 | **P07-R 科学完整性修复（取代 D045 科学有效性部分；D045 入口裁决仍 active）**。systematic-debugging 三根因最小失败测试全部复现：H1 SCALE 致命（`quantize_iq` 返回 q=Q(gz) 但 receiver 喂 q 未 /g，下游 scale-DEPENDENT 函数不可恢复）/ H2 CONTROL（CausalRMSAGC g_next=target/rms(q) 漏 g_current）/ H3 LIFECYCLE（每 window 独立 seed 独立 gg_block ACF≈0 无时间相关）。新建 p07r_*（gain-aware ADC q/g + corrected incremental AGC + stateful AR(1) trajectory，旧 p07_* 不动标 INVALIDATED）。fresh-seed Phase A（dev 300-309 零重叠）deployable 位宽 W8/W10 dev-best g=0.5 regret **+0.03~+0.07 dB ≪MDE=0.15** 全 rho → **verdict `PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION`**（旧 +0.91dB 完全是 H1 SCALE artifact；折中真实单调但单侧，静态低增益即解决）。Phase B/C 不运行。verifier **V072 PART2 10/10 ACCEPT**（沿调用链查物理正确性不止 consistency）。**campaign 恢复 7/10，F 族关闭**（静态低增益即解决无方法空间）。 | D046 / V072-PART1+2 / CP037 / worker-log step-035 |

| D048 / P08-R→V074 | **P08 coded-chain 科学完整性修复（取代 D047 科学有效性部分；D047 入口裁决仍 active）**。systematic-debugging 六根因最小失败测试全部复现（p08r_prefill_evidence.md）：H1 GG provenance（p08_phaseA_gate.py:86 硬编码 scenes 与 params.py:100-228 三档全不一致且档位错位）/ H2 runtime information（6 处 σ²=1/(2γ_bar) 来自循环变量）/ H3 oracle action space（_oracle_sigma2 单 global scalar 不覆盖候选）/ H4 metric contract（Primary A 全 inf 静默退 raw FER-delta，MDE 从未生效）/ H5 coded identity（LDPC5GEncoder 未传 num_bits_per_symbol，worker-log 谎称 triangle interleaver）/ H6 state lifecycle（16 cw 当独立样本）。新建 p08r_*（旧 p08_* 不动标 INVALIDATED）：option A 真 3GPP interleaver + GG params import + receiver-visible prefix σ² + O0/O1/O2 ladder + 重新冻结 metric + trajectory-cluster。fresh-seed Phase A（dev 6000-6019/test 7000-7039，frozen cell weak@1000Hz@12dB）：test mean FER B0/B1/B2/O0/O1/O2=0.115/0.115/0.113/0.115/0.115/0.109；Δ(B0−O2)=+0.0055 CI=[0,0.014]≪MDE_fer=0.2347；mechanism 4/40 不可恢复深衰落（O2 也译不出，h_truth 0.29-0.41）。Phase B/C 不运行。verifier **V074 16/16 ACCEPT**（脚本 + 独立 sub-agent fresh context 沿 caller→callee 检查科学信息边界，H1-H6 + AST + mechanism 独立重算一致）。**campaign 恢复 8/10，G 族关闭**（corrected chain 下 coded loss 主导仍不可恢复突发深衰落非 LLR 失配）。⚠️ **科学结论已被 D049/V075 取代——见下行**（V074 漏审 H7 equalize true-SNR 上游泄漏 / H8 AST 不递归 / H9 统计合同非法）。 | D048 / V074 / CP039 / worker-log step-037（无独立 commit，待主控统一） |
| D049 / P08-R2→V075 | **P08-R2 receiver 信息边界 + AST 门 + 统计功效合同三根因修复（取代 D048 科学有效性部分；D048 GG/oracle/identity/H4-H6 修复 + D047 入口裁决仍 active 作 PARTIAL reusable asset）**。systematic-debugging 三根因 prefill（p08r2_prefail_evidence.md 逐 file:line + p08r2_h7_reproduce.json 数值复现）：**H7 receiver 信息边界**（p08r_chain.py:341-360 equalize 读 self.gamma_bar 三处：盲 h 噪声底/h_est/mmse_equalize 第3参 SNR γ；数值复现固定 realization 只翻 gamma_bar 12→18/8dB，max\|ΔeqX\|=0.145/max\|ΔB0 LLR\|=7.02 证 deployable decide 间接消费 true SNR）/ **H8 AST verifier 盲区**（p08r_verify.py:109-129 check #5 只扫 method 函数体不递归进 real.equalize 漏审 H7；sub-agent 把 equalize gamma_bar 错标 future-work seed 被数值复现证伪）/ **H9 统计合同**（MDE=0.2347 固定 n 后 power 阈值非先验；CI_lo=0 当排除；strongest_conv=min(B1,B2) per-trajectory cherry-pick）。新建 p08r2_*（不动 p08r_*，D048 PARTIAL 资产 verbatim 复用）：estimate_pre_eq_noise_from_prefix 用 32-sym prefix LS 解 2×2 H_eff（4 复未知数/64 方程/60 dof）得 receiver-visible σ²_pre；CodedRealizationR2.equalize 用 σ²_pre + γ_vis=1/σ²_pre 替代 gamma_bar；amp_limit(3.0) 保留。**metamorphic 门**（p08r2_metamorphic_gate.py）：翻 gamma_bar 6-22dB，所有 cell worst ΔeqX/ΔLLR=**0.0 精确**（H7 runtime 铁证）。正确功效设计：先验 MDE=0.05（非 post-hoc）/ B2 单一 comparator（去 min(B1,B2)）/ EVIDENCE_INSUFFICIENT 终态（CI_hw>MDE/2）。fresh seeds（dev 9000-9019/test 8000-8039，disjoint from P08-R 6000-6019/7000-7039 + history）。Phase A：test mean FER B0/B1/B2/O0/O1/O2=0.155/0.155/0.148/0.155/0.153/0.139 全聚集；Δ(B0−B2)=+0.0063 CI=[+0.0008,+0.0141] hw=0.0066；Δ(B2−O2)=+0.0094 CI=[+0.0016,+0.0195] hw=0.0090≪MDE=0.05；mechanism 3/40 不可恢复深衰落（O2 也 2/40 译不出）。Phase B/C 不运行。verifier **V075 19/19 ACCEPT**（脚本含 H7 递归 AST 0 违规 + metamorphic Δ=0.0 + H9 先验 MDE + 无 min(B1,B2) + EVIDENCE_INSUFFICIENT 可达 + raw→aggregate relErr=0.0；独立 sub-agent fresh context 7 项全 ACCEPT 无 executor 自述差异）。终态 **`PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE`**（同物理机制，但这次在真正 γ-free corrected chain + 先验 MDE + 新 seeds + 无 cherry-pick 下得出）。**campaign 恢复 8/10，G 族关闭**。**TL 教训**：P07-R/D046 → P08/D048 → P08-R2/D049 "consistency≠correctness" 三度重演，verifier 必须递归遍历调用图 + 跑运行时 metamorphic 门。 | D049 / V075 / CP040 / S007（无独立 commit，待主控统一） |
| D050 / P09→V076 | **P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 入口门 STRATEGIC_GATE（不计有效包，count_excludes=entry_preflight_only，同 CP028/CP029 无 sprint 先例）**。用户冻结问题 M="当前 full-search NDA-ML"/A="均匀穷举大量候选导致计算冗余"/双门 B（objective eval 减少 ≥4×+性能非劣 ≤0.10 dB）/最强廉价 comparator="dev-tuned uniform coarse grid"，明文允许"若无法证明计算问题终止为 STRATEGIC_GATE 不计包"。入口门源码核查（主线程 Read+grep 零命中+Explore 子 agent fresh context 交叉）**证伪承重前提 A**：NDA-ML（`common/_recovery.py:171-273` `nda_ml_recovery`，D005 Go/D007 修正后 GW Step 4a 维度 D 验证赢家）是 closed-form 解析估计（升 M0=8 幂去调制+`np.angle(raised.mean())` 整块 `:232`/K=8 段每段一次 `np.angle(raised[lo:hi].mean())` `:224`/单次 FFT argmax+Quinn-Rife `:249-258`），**无 candidate 枚举/无 objective 在候选集上求值/无可裁剪搜索结构**。生产 driver `sc_nda_ml_sim.py:180-187` 逐块调一次 closed-form，无 per-window objective eval 可数。grep `full-search\|exhaustive\|candidate\|grid_search\|phase_grid\|coarse\|coarse-to-fine\|hierarchical\|objective.*eval\|enumerate` on `_recovery.py`/`sc_nda_ml_sim.py`/`_b11_params.py` **零命中**。代码库唯一 exhaustive search `bps_cpr`（`_recovery.py:91-118`，B 测试相位×Nw 符号距离度量）是 Pfau 2009 **竞争对手非 NDA-ML 本体**（ADVISOR_BRIEFING 报 NDA-ML ≈ BPS 0.006-0.14 dB）。`_db_caliber_and_complexity.md:51-61` NDA-ML 已 16 mult/symbol（VV 24），无 coarse-grid/coarse-to-fine/hierarchical comparator 存在。method-production 入口四门 3 FAIL（门1 无 search 自由度可裁剪/门2 无 lever 可作用/门3 dev-tuned coarse grid 无网格可 coarse 化；门4 file:line 已举）路由 STRATEGIC_GATE 而非 factory task；双门 B primary cost metric 失效（无 objective eval 可数）；Phase A 备选终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_COARSE_SEARCH 不适用（语义前提是存在 search 可被 coarse grid 解决，这里连 search 都没有）；动估计器本体减计算（跳块/块间状态复用/换升幂/减 K 段）= 替换研究对象且触发 `NDA_ML_BODY_REOPEN` forbidden（topic-index control L24，TL-30），双重禁止。verifier **V076 13/13 ACCEPT**（NDA-ML closed-form/driver 无 objective eval/grep 零命中/BPS 是竞争对手/前提 A 证伪/双门失效/comparator 无对象/coarse-search 终态不适用/入口四门 3 FAIL/NDA_ML_BODY_REOPEN 禁止/STRATEGIC_GATE 唯一合法/计数正确/无 truth leakage trivially）。终态 **`STRATEGIC_GATE`**。campaign 维持 **8/10**，P09 不计包，无 sprint/无 held-out seed/无 artifact/无 commit 之外产物。不重开 G 族（P09 入口否非 G 新证据），不重提 P09 同对象（TL-30 禁换名重开）。 | D050 / V076 / CP041 / S008（无独立 commit，待主控统一） |

## 未决项

- CP028 `STRATEGIC_GATE` 已解决：先经 D038 段A（PHYSICS_BACKED_TESTBED_UNAVAILABLE，选项(1) 已尽），
  再由 D039 用户 campaign 授权覆盖（10-有效包预算，不要求 thesis pivot）；
- 仍 0 active carrier；某 package 出 `DIAGNOSTIC_METHOD_SIGNAL` 且过 promotion preflight 前不晋级；
- campaign 计数（topic-index control block `campaign` 段）：`accepted_valid_packages=8`，budget=10，
  current=P09（入口门 STRATEGIC_GATE，待重指定）；setup/治理/任务准备/接口修复/纯复现/入口 preflight 不计；**P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 入口门 STRATEGIC_GATE 不计包**（承重前提 A 证伪，count_excludes=entry_preflight_only），不计入 accepted_valid；
- 第 5 包（P05）内部校准**已完成**（S005 §mid-calibration，不停线）：5 包全 honest negative 0 signal，族覆盖 4（A 关闭/B/C/D 连续=1），P05 首个换对象包；第 10 包（P10）做 campaign-level pivot/continue 裁决；
- **P07-R 后族覆盖 6 族**（A 关闭/B/C/D/E 关闭/**F 关闭**）；P01-P07 verdict 序列 NO_SIGNAL/RESOLVED_REGION/RESOLVED_UNIFORM/ABSENT/RESOLVED_BY_CONVENTIONAL/NO_CAUSAL_HISTORY_INCREMENT/PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION —— 7 包全 honest negative 0 signal；**P07-R 修正**：旧 P07 `NO_DIAGNOSTIC_METHOD_SIGNAL`（+0.91dB）已被 D046 冻结为 H1 SCALE artifact，corrected 链下静态低增益即解决（W8/W10 +0.03~+0.07dB≪MDE），F 族关闭；
- 同族连续≤2 包；至少 5 机制族（A CPR 选择器鲁棒性**已关闭**（P01+P02 达上限）/ B 定点资源协同设计**已开**（P03 连续=1）/ C 连续 GG OOD 选择器鲁棒性**已开**（P04 连续=1）/ D ML polarization equalizer OOD online adaptation**已开**（P05 连续=1，首个换对象包）/ E 因果跨帧历史信息**已开+已关闭**（P06 首包即关闭）/ F AGC/ADC 动态范围**已开+已关闭**（P07-R 修复后问题不存在于 deployable 位宽）/ G coded-LLR-calibration **已开+已关闭**（P08-R2 corrected γ-free chain 下 coded loss 主导不可恢复突发深衰落，oracle B2-O2 headroom≪MDE））；**"≥5 族"已达成（7 族）**，P09 入口门 STRATEGIC_GATE 后待用户重新指定入口（须过入口四门，禁重开已关闭族及 forbidden axis）；
- 已关闭轴不得换名重开（TL-30）：NDA-ML 本体 / G1 science repair / CB1 collapse family / Pilot-Jones 小轴 / PMD-PDL-Jones-CD 星地移植 / **A 族 CPR 选择器鲁棒性（cand_rank/weakretune/SNR-mismatch/region-retune 子轴）** / **FOE-residual→CPR cascade（T030 撤回）** / **E 族因果跨帧历史（cross-frame history / F3-A-repair / temporal-prediction 子轴，P06 首包即关闭）** / **F 族 AGC/ADC 动态范围（D046/V072-PART2：静态低增益即解决无方法空间）** / **G 族 coded-LLR-calibration（D049/V075：corrected γ-free chain 下 coded loss 主导不可恢复突发深衰落，oracle headroom≪MDE）** / **P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 同对象禁重提（D050/V076：NDA-ML 是 closed-form 无 search 可裁剪，承重前提证伪；换名重提 NDA-ML-low-complexity / compute-constrained-NDA-ML / NDA-ML-coarse-grid 等同对象属 TL-30 禁换名重开）**；P05 periodic-pilot 作 comparator 仅佐证 D032 KILL 非复活；P07 的 symbol-timing-offset（F）/场景扩展（G）/FEC-APSK（H）子轴已撤回（"无可作用物理自由度/重入已关闭轴"）；
- 下一真实压缩事件需量化 elapsed time、files read、lane/gate match；
- G1 只保留 bounded thesis asset，不重开科学修复；
- 频域/子带均衡族仅在信道源码被升级到含色散/多径/频率选择性后才可能重审，当前作 rejected task brief 保留。

## 当前位置

**2026-07-30 D039（用户 campaign 授权）**：D038 段A 穷尽 channel 物理自由度路径后，用户授权 10-有效包
探索 campaign（voice.md 2026-07-30 "至少跑10大包？"）。对象从"造新 channel 物理自由度"转向"对已完成
方法的新失效条件/鲁棒性做子问题探索"（FR-23 问题驱动）。active_lane → `CAMPAIGN_EXPLORATION_DISPATCH`，
authority → D039，epoch 64→65。建立最轻量 rolling queue（control block 计数器，不建 controller）：
`exploration_budget_valid_packages=10` / `accepted_valid_packages=0` / `current_package=P01`；至少 5 机制族、
同族≤2 连续、第 5 包内部校准不停线、第 10 包 campaign 裁决。`PREFORMAL_METHOD_FACTORY` 解禁为本 campaign
服务（problem-first 三阶段门控内）；setup/治理/任务准备/接口修复/纯复现/入口 preflight 不计有效包数。

**P01（本轮端到端执行）= CPR 选择器 SNR 失配鲁棒性**。原 DA-NDA 两层 selector（`_a4_switch_common768_
30seed.py:97-107`）在两处依赖运行时 nominal SNR：①stage-1 CV 边界 `cv_awgn_theory(gamma_db)=0.74+
0.12exp(-gamma_db/5)`（`:93-94`）× margin 1.10；②stage-2 噪声扣除 `1/(2*gamma_lin)`（`:106`）+ γ_eff
vs 13 dB。冻结 anchor `ccisp_family1_selector_a_30seed.json`（30 seed × weak/moderate/strong × 5–25 dB，
common-768 口径）增益集中在 weak/moderate/strong 中低 SNR（5–13 dB，DA 占用 30–95%）：weak@9dB
+1.50dB、moderate@9dB +1.05dB、strong@9dB +0.83dB（oracle bound 仅作上限）。

**P01 已完成（CP030/V065）**：Phase A problem-bearing probe（独立 executor 复现 anchor 150/150 cell 逐 seed 精确，
verifier 独立重跑 3/3 一致；dev 前冻结损害判据 ≥0.3dB drop+CI<0；注入 δ∈{−3..+3}dB → 问题成立：weak@5/7/9 δ=−3
−0.339/−0.393/−0.324、weak@11 δ=+3 −0.704、moderate@13 δ=+3 −0.344，CI 上界<0）→ Phase B 非相干块 pilot SNR 估计
adapter（δ-invariant，true γ 不进 decide）恢复 4/5 损害 cell（+0.746/+1.113/+1.241/+0.957/+0.706 dB），仅 weak@9
残余 −0.323 → Phase C 5 个机制不同 robust 候选 vs adapter（held-out seeds 30–49）：最佳 cand_rank pooled
**+0.1358 [+0.1207,+0.1510]**，未过冻结 MDE=0.15 → **verdict `NO_DIAGNOSTIC_SIGNAL`**。verifier V065 PASS（8/8，
verdict 唯一正确）。条件式子群体信号 cand_rank 仅 weak@5/7/9 超 adapter ≥MDE（+0.385/+0.432/+0.323），机制连贯、
系统性非 cherry-pick，降级为 future-work seed。无 protected 文件改动；true γ 绝不进 decide；dev 0–9/held-out 30–49 隔离。
worker-log `projects/thesis-fso/worker-logs/step-028-p01-cpr-snr-mismatch.md`；artifact `results/p01_cpr_snr_mismatch/`。

**P02 已完成（CP031/V066）**：P01 留下的条件式子群体信号（cand_rank@weak/低SNR +0.32~+0.43 vs adapter）
的 fresh confirmation。读新 test 数据前冻结目标区 weak×{5,7,9}、边界 weak@11/moderate@{5,7,9}、MDE=0.15、
方法身份全复用 P01 冻结码（adapter/cand_rank 不改一行）、cheap alternative=weakretune（cand_rank body +
dev 调谐 ref，同一 conventional lever 仅把 stage-1 ref 当 dev-可调旋钮）。dev（seeds 50–59，3 target cell）
调谐 ref∈{7..11} 单调增，选 ref=11.0（唯一 argmax）。fresh held-out（seeds {60..70}∪{81..89}∪{90..99}=30，
全 disjoint anchor/P01 dev/P01 held-out/dev/pollution）：primary cand_rank−adapter=**+0.3578 [+0.3381,+0.3775]**
90/0/0；per cell weak@5/7/9 +0.3665/+0.4279/+0.2790 全 CI_low>0，去最佳 cell 余 2 仍 +0.3228 无单 cell 独占。
cheap-alt 裁决：weakretune−adapter=**+0.4539**（weakretune 反超 cand_rank）、cand_rank−weakretune=**−0.0961**
|mean|≤MDE。§5 Step 1 触发 → **verdict `PROBLEM_RESOLVED_BY_REGION_RETUNING`**。cand_rank 冻结 ref=9.0 非
load-bearing——dev 调谐同一 conventional lever（ref 9→11）即捕获并略超其增益，无可区分 deployable action，
不产方法卡/不晋升。verifier V066 PASS（8/8，raw→aggregate 相对误差 0.000e+00、seed 零碰撞、git diff 冻结文件空、
true γ 绝不进 decide、独立重跑 2 seed 字节级一致）。一次包内确定性修复（seed-count 算术 20→30 补 90–99，判据/dev-ref/
方法/MDE/§5 顺序全不变，20 与 30 seed verdict 同）已披露。worker-log `step-029-p02-cand-rank-operating-regime.md`；
artifact `results/p02_cand_rank_operating_regime/`。

**P03 已完成（CP032/V067）**：绑定裁决撤回无效 T030（FOE-residual→CPR cascade 入口，1MHz 是 FOE 前 warning
参数非 post-FOE residual，保留 rejected brief 不计有效 P03），新 P03 = B_FIXED_POINT_RESOURCE_PERFORMANCE_CODESIGN。
对已完成 DA/NDA CPR 选择器注入"定点部署"新失效条件（FR-23 问题驱动）。可信 bit-true Q(W,F) 模型（饱和二补码、
round-half-up、block-float per-window 共享 exponent、accumulator 加宽 log2(N)+guard、非线性算子 I/O 量化），
float-bypass **0/132,000** 逐 window 决策与浮点 `A.decide` 一致。Phase A uniform 位宽阶梯 {(6,4),(8,6),(10,8),
(12,10),(14,12),(16,14)} dev 0–9：uniform(8,6) 已到 regret 地板（gain-bearing 区 pooled **+0.027 dB**），地板
branch-statistical（(16,14) Q≤2⁻⁴⁰ 仍持续 +0.685/+0.806 dB @高SNR cell，集中锚点增益本身 ~0 处）。Phase B
4 mixed candidate（dev 10–19 tune，fresh held-out 30–49）：最佳 `two_exp(8,6)` Pareto-主导 uniform(14,12)
（held-out +0.1729 vs +0.1895 dB @ op×bit 348 vs 536）但优势 **+0.0166 dB = 0.11×MDE=0.15** →
`mixed_strictly_better_by_mde=[]`，无可区分 deployable action → **verdict `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`**。
verifier V067 **10/10 PASS**（raw→aggregate 0.000e+00、float-bypass 独立重跑 0/48000、信息边界 AST 干净、
resource 措辞严格 proxy 无真实综合、verdict 唯一正确）。不产方法卡/不晋升。harvest：(a) DA/NDA 选择器 8-bit
uniform Q(8,6) 决策与浮点 byte-exact（Ch5 FPGA §5.4/§5.5 bit-cost/resource proxy 工程证据）；(b) stage-2 噪声
扣除高 SNR 下溢张力真实但 sub-MDE（two_exp mean-normalization 弱提示，future-work seed）。两次包内确定性修复
（float-bypass 分母叙述 726k→132k；Phase-BC 键名 bug 修复并重跑）已披露。worker-log
`step-030-p03-fixed-point-codesign.md`；artifact `results/p03_fixed_point_codesign/`。

**P05 已完成（CP034/V069）**：campaign 第 5 个有效包（ML polarization equalizer OOD safe online adaptation 族 D，同族连续=1）。
binding decision 撤回无效 P05-D（FEC/旋转模糊）/P05-E（window/complexity），新族 D 对象=ButterflyCNNEqualizer2x2（≠ NDA-ML CPR selector）。
Phase 0 身份门 CLOSED；Phase A PRIMARY=fixed-label BER（swap-visible 不变量 10）问题成立（两 cell +0.4990/+0.4981）；Phase B standard-CMA-continuation
（Godard-with-z 在线）recovered 两 cell（0.00018/0.00117≪MDE）→ `PROBLEM_RESOLVED_BY_CONVENTIONAL_ONLINE_EQUALIZER`；Phase C 不运行。verifier V069 ACCEPT。
**mid-calibration（第 5 包内部校准，不停线，已完成）**：P01-P05 verdict 序列 NO_SIGNAL/RESOLVED_REGION/RESOLVED_UNIFORM/ABSENT/RESOLVED_BY_CONVENTIONAL
—— 5 包全 honest negative 0 signal。族覆盖 4（A 关闭/B/C/D 连续=1）。**P05 是首个换对象包**（前 4 包全 DA/NDA CPR 选择器，P05 换 ButterflyCNN
ML equalizer，机制距离显著扩大，非在旧 selector 打转）。校准结论：campaign 不是在旧 selector 周围打转，但仍 0 signal——每新失效条件要么 sub-MDE
要么被常规 comparator 解决。campaign 5/10 半预算。可写入 thesis 资产：Ch3/Ch4 双口径警示（ML swap vs standard-CMA no-swap，H2/D023 适用边界）+ D032 KILL
独立佐证 + ML identity freeze 三阶段门控框架。

**P06 已完成（CP035/V070）**：campaign 第 6 个有效包（E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION 族 E 首包，一次性修复型 PROBLEM_BEARING_PROBE，**第 5 族"≥5 族"达成**）。
binding decision 撤回旧 P06（E 信息复杂度边界/window-length 重复 B1/P05-E），新 P06 修复旧 F3-A 科学无效性（`run_f3a_history.py:195-196` marginal-MI max-diff 误标 conditional-MI；旧 +0.060/+0.036 不继承）。
Phase 0 物理身份门 ALL PASS 6 conditions（GG 边缘 KS 0.056-0.144、块 ACF relerr<0.2%、rho_frame fg30/100/1000=0.99/0.97/0.70、冻结 CMA 重跑 relerr=0）；Phase A 严格因果信息门（fresh seeds 全 disjoint 历史，6 cond×40 traj=4800 frames，trajectory-level split）：
history-expanded ridge R²=0.320 > current-only 0.040（MSE 减少per-traj macro CI_lo>0 严格因果增量统计存在）**但 persistence R²=0.853 远优**（逐 condition 含动态 fg1000 persistence 0.68-0.95 全胜 history 0.04-0.88）→ **`NO_CAUSAL_HISTORY_INCREMENT`**。Phase B/C 不运行。verifier V070 **7/7 ACCEPT**。
E 族首包即关闭（绑定裁决禁第二个 evaluator-repair 包）。harvest：Ch3/Ch4 receiver-observability 边界（跨帧信息被帧间持续性主导）+ 方法论附录教训（marginal-MI≠conditional-MI）+ 物理诚实资产（deployable frame rate≪τ_c 跨帧动力学边界）。worker-log `step-033-p06-causal-cross-frame-history.md`；artifact `results/p06_causal_cross_frame_history/`。

**当前位置**：P07-R 修复完成（D046/V072-PART2 取代旧 P07 科学结论），accepted_valid_packages=7/10，仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。
**族覆盖 6 族**（A/B/C/D/E/F，A、E、F 已关闭）。P01-P07 verdict 序列 NO_SIGNAL/RESOLVED_REGION/RESOLVED_UNIFORM/ABSENT/RESOLVED_BY_CONVENTIONAL/NO_CAUSAL_HISTORY_INCREMENT/PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION —— 7 包全 honest negative 0 signal。**P07-R 诚实结论**：旧 P07 的"clipping–resolution 折中真实存在 +0.91dB"完全是 H1 SCALE artifact（`quantize_iq` 返回 q=Q(gz) 但 receiver 喂 q 未 /g，下游 scale-DEPENDENT 函数不可恢复）；corrected 链下静态低增益（g=0.5）即把 deployable 位宽 W8/W10 regret 降到 +0.03~+0.07dB≪MDE，无方法增量空间 → F 族关闭。

下一合法动作：**Package 08（必须换不同机制族——F 已关闭；候选 G coded-LLR-calibration 新族，或 B/C/D 第 2 包连续≤2；禁重开已关闭 A/E/F 族及所有 forbidden axis）**。
本轮（2026-08-01）用户已授权 coded-chain 场景扩展（voice "行" → D047 scope-change），P08 = G_CODED_LLR_CALIBRATION_UNDER_GG_RESIDUAL 端到端执行。

---

**【当前位置 — 以本块为准，覆盖上方过时叙述，2026-08-01 D050】**

**当前位置**：P09 `COMPUTE_CONSTRAINED_NDA_ML_SEARCH` 入口门裁决 **STRATEGIC_GATE**（D050/V076/CP041），accepted_valid_packages 维持 **8/10**，仍 0 active carrier、claim ceiling `LOCAL_SLICE / NONBINDING_DIAGNOSTIC`。本轮无 sprint/无 held-out seed/无 artifact/无 commit 之外产物。

P09 入口门否决原因：用户冻结的承重前提 A（"当前 full-search NDA-ML 均匀穷举大量候选导致计算冗余"）被源码证伪——NDA-ML（`common/_recovery.py:171-273` `nda_ml_recovery`，D005 Go/D007 修正后 GW Step 4a 维度 D 验证赢家）是 closed-form 解析估计（升 M0=8 幂去调制 + mean-angle / K=8 段 / 单正弦 FFT argmax+Quinn-Rife），**无 candidate 枚举/无 objective 在候选集上求值/无可裁剪搜索结构**；grep `full-search|exhaustive|candidate|grid_search|coarse|hierarchical|objective.*eval` 零命中；代码库唯一 exhaustive search `bps_cpr` 是 Pfau 2009 竞争对手非 NDA-ML 本体。双门 B primary cost metric 失效（无 objective eval 可数）；Phase A 备选终态 PROBLEM_RESOLVED_BY_CONVENTIONAL_COARSE_SEARCH 不适用（无 search 可被 coarse grid 解决）；动估计器本体减计算 = 替换研究对象 + 触发 `NDA_ML_BODY_REOPEN` forbidden。STRATEGIC_GATE 唯一合法终态。

**族覆盖 7 族**（A/B/C/D/E/F/G，A/E/F/G 已关闭）。有效包 verdict 序列（8 包）：P01 NO_SIGNAL / P02 RESOLVED_REGION / P03 RESOLVED_UNIFORM / P04 ABSENT / P05 RESOLVED_BY_CONVENTIONAL / P06 NO_CAUSAL_HISTORY_INCREMENT / P07-R PROBLEM_ABSENT_AFTER_GAIN_CALIBRATION / P08-R2 PROBLEM_ABSENT_AFTER_RECEIVER_VISIBLE_STRONG_LLR_BASELINE —— 8 包全 honest negative 0 signal。P09 入口门 STRATEGIC_GATE 不计包（count_excludes=entry_preflight_only）。

下一合法动作：**重新指定 P09 入口**（须过 problem-bearing 入口四门；禁重开已关闭 A/E/F/G 族及 NDA_ML_BODY_REOPEN/FOE-residual cascade 等所有 forbidden axis；P09 COMPUTE_CONSTRAINED_NDA_ML_SEARCH 已否不可换名重提同 NDA-ML-low-complexity 对象——TL-30），或**用户授权 P10 campaign-level 裁决**（提前到第 9-10 包做 portfolio pivot/continue 决策）。
