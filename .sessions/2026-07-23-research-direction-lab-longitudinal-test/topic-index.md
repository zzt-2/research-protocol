# Topic Index: Research Direction Lab 长程真实运行测试

<!-- RDL-CONTROL:START -->
```yaml
rdl_control:
  schema_version: rdl.foreground-control.v2
  control_epoch: 64
  role: LIVE_TEST
  mission: 在真实研究反馈中验证轻量长程运行协议能否稳定推进并积累可用方法材料
  active_lane: PHYSICS_EXTENSION_TERMINATED_AWAITING_USER_DECISION
  authority_pointer: .sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md#D038
  decision_gate: CP029（D038 段A→V064）：用户选项(1) channel 物理扩展大包段A 三候选（complex time-varying Jones / PDL / PMD-色散-跨符号记忆）六门评估无一过门1-3 → PHYSICS_BACKED_TESTBED_UNAVAILABLE。根因：fiber 现象（PMD/PDL/CD/复 Jones 双折射）源于各向异性玻璃波导，自由空间大气各向同性无物理起源；四篇星地 coherent FSO primary（Paillier2020/Zhou2024/Zhang2023/Gu2022）全文 polarization-impairment 零命中；唯一可溯源参数（DGD≤6ps=1.5%T_S、PDL≤1dB）D066 实测 headroom 0.0804dB≪0.5dB；时变复 Jones 轴已被 D066:3415-3416 关闭。遵守"不制造第四 impairment"纪律，段B/C/D 不运行，诚实终止。选项(1)已尽。
  allowed_actions:
    - RECOVER
    - PORTFOLIO_MAP
  forbidden_actions:
    - SCIENTIFIC_EXPERIMENT
    - PREFORMAL_METHOD_FACTORY            # 段A 终止，本大包解禁已耗尽
    - CLOSED_AXIS_REOPEN
    - FREQUENCY_DOMAIN_SUBBAND_FAMILY
    - CB1_COLLAPSE_RECOVERY_FAMILY
    - FORMALIZATION_ONLY_PACKAGE
    - GENERAL_INFRASTRUCTURE_BUILD        # 段A 终止，本大包解禁已耗尽
    - PRIVATE_FULLTEXT_ACQUISITION
    - ABSTRACT_AS_FULLTEXT
    - POST_STEP4A_ADVANCE
    - SCIENCE_SCOUT_REACTIVATION
    - PROTECTED_HISTORY_EDIT
    - FORMAL_MVE
    - PAPER_CLAIM
    - PROTECTED_OWNER_MODIFY
    - ORACLE_GAP_AS_GO
    - FOURTH_IMPAIRMENT_MANUFACTURE       # 段A 已穷尽 fiber→星地移植路径
    - FIBER_IMPAIRMENT_RELOCATED_TO_STAR_GROUND  # 物理上不成立
    - SUB_SYMBOL_JONES_AXIS_REOPEN        # D066:3415-3416 已关闭
  mission_log_ref: .sessions/2026-07-23-research-direction-lab-longitudinal-test/mission-log.md
  mission_checkpoint: CP029
  next_legal_action: 等待用户在 CP028 剩余选项中决策：(2) 论文范围决策（G1 bounded package + 局部负面 harvest 作毕业材料，或开新子问题）；(3) 接受 0 active carrier 下"协议稳定+可靠负面+1 bounded asset"收尾审计。选项(1) channel 物理扩展已尽（PHYSICS_BACKED_TESTBED_UNAVAILABLE）。用户决策前不开新 sprint/T。
```
<!-- RDL-CONTROL:END -->

> 状态: active（CP029/D038 段A→V064：用户选项(1) channel 物理扩展大包段A 三候选六门评估无一过门1-3 → PHYSICS_BACKED_TESTBED_UNAVAILABLE；fiber 现象无星地物理起源、四 primary 零命中、D066 已关 sub-symbol Jones 轴；段B/C/D 不运行、不造第四 impairment、诚实终止；epoch 64 / CP029，仍 0 active carrier；交用户 CP028 剩余选项 (2)论文范围决策 / (3)收尾审计）
> 创建: 2026-07-23 | 最后更新: 2026-07-30

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

### 明确不含

- 不运行科学实验、重开已关闭轴、进入 Step 5/Contract/Execute 或恢复 science-scout；
- 不修改 session-governance、建设 controller/scheduler、通用基础设施或 per-fork manifest；
- 不获取私有全文，不把摘要冒充全文；
- 不修改 protected history、formal scientific owners 或 thesis framework；
- 不把流程 PASS、包装或写作材料冒充正式方法；
- 不要求用户读取技术日志或判断科学正确性。

### 范围变更记录

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

## 未决项

- CP028 `STRATEGIC_GATE` **已由用户选项(1)解决（D038/2026-07-30）**：授权一次性端到端大包升级
  channel 物理自由度（complex time-varying Jones / PDL / PMD-色散-跨符号记忆），解禁 PREFORMAL_METHOD_FACTORY
  + GENERAL_INFRASTRUCTURE_BUILD 仅本大包，段间不停下等用户；
- **CP029/D038 段A 已终止（V064）**：选项(1) channel 物理扩展段A 三候选六门评估无一过门1-3 →
  `PHYSICS_BACKED_TESTBED_UNAVAILABLE`；fiber 现象无星地物理起源、四星地 primary 零命中、
  sat.1553 等三篇 dangling、D066 已关 sub-symbol Jones 轴；段B/C/D 不运行、不造第四 impairment；
  PREFORMAL_METHOD_FACTORY + GENERAL_INFRASTRUCTURE_BUILD 解禁已耗尽重归 forbidden；**选项(1) 已尽**；
- 仍 0 active carrier；段D 出 METHOD_SIGNAL 且过 promotion preflight 前不晋级；
- 下一真实压缩事件需量化 elapsed time、files read、lane/gate match；
- G1 只保留 bounded thesis asset，不重开科学修复；
- 频域/子带均衡族仅在信道源码被升级到含色散/多径/频率选择性后才可能重审，当前作 rejected task brief 保留；
- CB1 collapse-recovery 全族（block-size/μ/更新调度/频域/子带/z-only/初始化/cost 变体）按用户绑定结论 + D036/D037 forbidden，不再运行。

## 当前位置

S003 入口选择后，经 2026-07-29 用户中转指令做**最小入口纠偏**（D035/V061）：原 T027 选的
**频域/子带均衡族**未过 problem-bearing testbed preflight 门1（`_dual_pol_channel.py:127-132`
信道只有逐符号 GG 幅度 + SOP 旋转 + AWGN，无色散/多径/FIR/频率选择性，频域/子带无可作用物理
自由度；其 comparator 也未冻结；task-control epoch 59≠60；action_class 与正文语义不一致），
故原 DISPATCH_READY 撤回，频域族作 rejected task brief 保留、不运行。

method-production.md 补了入口四门（物理自由度存在 / 基线失败与作用点一致 / 命名传统同信息
可独立调谐 comparator / 每门 file:line，禁"未测族/REOPENED/testbed 曾产 signal"放行；并厘清
shared anchor vs. identity parity——后者只保护继承基线比较连续性，不禁止跑不同传统算法）。

**2026-07-29 CP027（D036/V062）**：用户中转指令要求一轮内端到端完成"最终纠偏 → 科学执行 →
独立验证 → 主控接收"。最终纠偏（四项）：①门2 证据等级——sprint-001"块末更新几何=结构性吸引子
原因"已被 V052 拒收，降级为 source-backed 疑似作用点（不是已确认机制）；②comparator 冻结为
canonical Godard-with-z（`Δw ∝ (R²−|z|²)·z·r*`，provenance `cb1_cell_runner.py:124-129`，禁
`_cma.py` scalar-error 缺 z 冒充）；③action_class→`PREFORMAL_METHOD_FACTORY`（epoch 60→61）；
④终态集 3→5（+ `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR` + `EXECUTION_INVALID`）。

sprint-003 由独立 executor 跑（commit `689151c`）：block-64 μ=0.03 anchor（PI-SER 0.31431）、
tuned per-symbol Godard-with-z comparator μ=0.001（0.29685）、block-8/16、recursive CMA，4 构造
× 7 cells × 20 fresh test seeds。独立 verifier V062 **PASS**（梯度身份逐方法核、raw→aggregate
独立复算吻合<1e-4）。**verdict = `NO_DIAGNOSTIC_SIGNAL`**：最佳 block8 vs comparator
Δ=−0.00293、CI [−0.0112,+0.0056] 跨 0、未过 MDE=−0.005；comparator 只 1/7 cell 消除 collapse，
未达 PROBLEM_RESOLVED 判据；候选场在 64× 更新预算跨度上平坦，既非更多更新也非粒度产生可分离
优势。**疑似作用点（块末更新）的因果性未被本 sprint 确认**——collapse 在所有更新粒度下都持续。

CB1 更新粒度均衡族轴按 method-factory 纪律关闭（无 signal 即退出）。当前仍 0 active carrier；
无 protected owner / formal / thesis framework 改动；无 push。下一合法动作：portfolio remap 选
机制不同的合法 carrier，或战略 gate 升级（届时交用户）。

**2026-07-30 CP028（D037/V063）**：用户中转指令要求在 CB1 collapse 家族之外选一个真正
problem-bearing 的新 testbed 跑一次新 method-factory sprint，入口最多三个候选逐项过六门（M-C-A /
物理自由度 / 命名传统 comparator / runnable testbed / primary-fallback packaging / file:line 证据；
rejected/invalidated/privileged 证据不得重新洗成 PASS）。主控评估三候选：

- **A 传统 CPR（VV Nw=128）在 adversarial_sourced|snr14 切片**：门2/3/4/5 PASS，但**门1 FAIL**
  （synthesis 只记 VV 对 oracle O 留 ~0.6dB headroom，是 oracle-gap——TL-32/FR-25 明确 oracle 上界
  只做 Kill 工具不当 Go 判据；P1/P2/P3 组合方法 9–20dB 失败属**已拒收的 B10/B12 实例**
  master-state.md:149 `SCIENCE_VERDICT_REJECTED`，不是可轮换开放轴；VV 本身无可被不同传统 CPR 改善
  的机制失败）+ **门6 FAIL**（verdict REJECTED；U10 evidence 是 SOP/CMA BER failure 非 CPR cycle-slip）。
- **B NDA-ML 跨问题扩展**：**门1 FAIL**（`_mve_results.json` AWGN +1.35dB 等全正增益，是已完成赢家非
  失败方法；`SC-NDA-ML-MVE-SPEC.md` GW Step 4a 维度 D 已封闭）。
- **C U24 high-SOP non-swap BER detection**：门1 部分（U24 是 candidate-map 唯一 pt5 候选；但 D047
  明确"1e-5 fixed=PI 非 swap"），**门4 FAIL**（D051 已关闭检测线——control 4e-6 新 seed 已有 oracle
  events，control-only 失效；non-swap BER 标签需 TX-truth oracle assignment 属用户禁止的
  "oracle/genie 才能构造的动作"；evidence_gap 无 testbed）。

候选扫描完整性：problem_truth ≥4 共四个（U24=候选C、U10=候选A族、**U05 pt4 HOLD_FOR_COMPETITOR_
CLOSURE** 出路阻塞、U23 pt4 MERGE_WITH_U24）。**无遗漏独立入口**。channel 源（`_dual_pol_channel.py:
104-132`）只有 GG 幅度 + 实 SOP 旋转 + AWGN，无多径/色散/FIR/频率选择性，物理自由度本身窄。

**verdict = `STRATEGIC_GATE`**：三候选无一过门，遵守"不得制造第四弱候选"纪律，不开 sprint、不建
T028、不修 protected owner/Skill/thesis framework。独立 verifier V063 **PASS**（事实成立；2 项初版
瑕疵——候选 A 门1 表述不准、U05 漏列——均非承重不改结论，已据 V063 在 D037 内纠正）。**缺的是
problem-bearing 物理问题（非 testbed/comparator 基础设施）**。仍 0 active carrier、
    mission_method_delta `NONE`（STRATEGIC_GATE 非方法进度）、无 push。
- **2026-07-30，live D038**：用户选定 CP028 STRATEGIC_GATE 三选项之 (1)——升级 channel 模型引入新物理自由度。
  - 原因：CP028 判定"缺的是 problem-bearing 物理问题（非基础设施）"——channel 源
    `_dual_pol_channel.py:104-132` 只有 GG 幅度+实 SOP 旋转+AWGN，物理自由度本身窄。用户选项(1)
    直接针对该根因，且要求端到端大包、段间不停下等用户（voice.md 2026-07-30）。
  - 新范围：**解禁** `PREFORMAL_METHOD_FACTORY` + `GENERAL_INFRASTRUCTURE_BUILD`（仅本 D038 大包，一次性
    有界）；四段串行链——段A 物理入口六门筛选（独立 subagent，≤3 候选：complex time-varying
    Jones/differential phase / physically justified PDL / PMD-色散-跨符号记忆；每门 file:line；三全败即
    `PHYSICS_BACKED_TESTBED_UNAVAILABLE` 不制造第四）→ 段B 只扩一个 channel 自由度（新 common/_*.py
    + params.py FR-20 参数类，旧路径 byte-identical；独立物理 verifier 先确认）→ 段C conventional
    baseline adjudication（shared anchor + 任务匹配传统 comparator + 廉价扩展，`PROBLEM_SURVIVES_`
    `CONVENTIONAL_BASELINE` 才进段D）→ 段D 条件式 method factory（独立 executor 跑 3–5 机制不同最小
    方法，vs tuned comparator，`DIAGNOSTIC_METHOD_SIGNAL`/`NO_DIAGNOSTIC_SIGNAL`）。
  - 影响：active_lane → `CHANNEL_PHYSICS_EXTENSION_DISPATCH`；authority → D038；control epoch 62→63。
    其余 D037 forbidden 全保留（`CB1_COLLAPSE_RECOVERY_FAMILY`、`FREQUENCY_DOMAIN_SUBBAND_FAMILY`、
    `CLOSED_AXIS_REOPEN`、`POST_STEP4A_ADVANCE`、`PROTECTED_OWNER_MODIFY`、`PROTECTED_HISTORY_EDIT`、
    `PAPER_CLAIM`、`PRIVATE_FULLTEXT_ACQUISITION`、`ABSTRACT_AS_FULLTEXT`、`FORMAL_MVE`）；新增
    `ORACLE_GAP_AS_GO`、`FOURTH_IMPAIRMENT_MANUFACTURE`、`SCIENTIFIC_EXPERIMENT_BEFORE_TESTBED_VERIFICATION`。
    无 protected history / formal owner / Skill / thesis framework 改动；无 push。仍 0 active carrier；
    段D 出 METHOD_SIGNAL 且过 promotion preflight 前不晋级。
- **2026-07-30，live D038 段A 终止 / V064 / CP029**：段A 物理入口六门评估完成，三候选全失败。
  - 原因：fiber 现象（PMD/PDL/CD/复 Jones 双折射）源于各向异性玻璃波导介质，自由空间大气各向同性
    **无物理起源**；四篇星地 coherent dual-pol FSO primary（Paillier 2020 `9120341.md` / Zhou 2024
    `10305071.md` / Zhang 2023 `10301506.md` / Gu 2022 `app12073331`）全文 PMD/PDL/DGD/Jones/色散
    **零命中**；本地+公开检索**无星地 polarization-impairment primary**；params.py 引用的
    sat.1553/s24248036/photonics10121312 三篇 content.md **本地不存在**（dangling）。唯一可溯源参数
    （Valjus DGD≤6ps=1.5%T_S、PDL≤1dB）D066 实测 headroom **0.0804 dB ≪ 0.5 dB**。**时变复 Jones 轴
    已被 D066（groundwork `2026-07-10-dual-pol-osl-groundwork/decisions.md:3381`，排除项 :3415-3416
    "不继续追求 verified DGD≫T_S 或 sub-symbol Jones 新轴"）关闭，非未测新问题。**
  - 段B/C/D 不运行（用户授权终止：三候选均失败即 `PHYSICS_BACKED_TESTBED_UNAVAILABLE`，不制造第四
    impairment）。PREFORMAL_METHOD_FACTORY + GENERAL_INFRASTRUCTURE_BUILD 解禁已耗尽，重归 forbidden。
  - 影响：active_lane → `PHYSICS_EXTENSION_TERMINATED_AWAITING_USER_DECISION`；authority 仍 D038；
    control epoch 63→64；mission CP029（no-method=3，无 sprint）；新增 forbidden：
    `FIBER_IMPAIRMENT_RELOCATED_TO_STAR_GROUND`、`SUB_SYMBOL_JONES_AXIS_REOPEN`。仍 0 active carrier、
    `mission_method_delta=NONE`（终止非方法进度）、无 protected owner/formal/Skill/thesis framework 改动、无 push。
  - **选项(1) 已尽**。下一合法动作交用户 CP028 剩余：(2) 论文范围决策（G1 bounded + 局部负面 harvest
    或开新子问题）；(3) 接受 0 active carrier 下"协议稳定+可靠负面+1 bounded asset"收尾审计。

**下一合法动作交用户三选项**：(1) 升级 channel 模型引入新物理自由度（complex Jones/PMD/PDL/色散，
FR-18，需 ~1 天基础设施授权，会改变所有方法竞争格局）；(2) 论文范围决策（G1 bounded package +
局部负面 harvest 作毕业材料，或开新子问题）；(3) 接受 0 active carrier 下"协议稳定+可靠负面+1
bounded asset"收尾审计。用户决策前不开新 sprint/T。

**2026-07-30 D038（用户选定选项1）**：用户已以选项(1)解决 CP028 STRATEGIC_GATE（voice.md
2026-07-30）。授权一次性端到端大包，四段串行、段间不停下等用户：

- **段A 物理入口筛选**（进行中）：独立文献/物理 subagent 比最多 3 候选——(a) complex time-varying
  Jones / differential phase coupling；(b) physically justified PDL；(c) PMD、色散或其他有跨符号记忆的
  coherent dual-pol FSO impairment。不假定任何 fiber 现象在星地成立。每候选过**六门**：①与当前
  coherent dual-pol 星地 FSO 范围直接相关（file:line）②≥2 篇可访问 primary/fulltext 支持存在/模型/
  参数范围③真实参数量级核算（当前 symbol rate/frame/处理窗口内可见，差≥3 数量级 Kill）④明确传统/
  同任务/同信息/可调谐 conventional comparator⑤能写成具体 M-C-A⑥约一天内可隔离实现+验证+小批诊断。
  每门给全文或源码 file:line。oracle gap 不当 Go。三全败 → `PHYSICS_BACKED_TESTBED_UNAVAILABLE`，
  不制造第四 impairment。
- **段B**（段A 通过后）：只扩六门全过的排名第一 impairment；新 `common/_*.py` + `params.py` 新参数类
  （FR-20 全溯源），旧默认路径 byte-identical（P4/TL-13）；建理论预期（TL-20）+ 退化/regression 测试；
  独立物理 verifier 先确认公式/单位/时间尺度。
- **段C**（段B 物理身份 PASS 后）：shared anchor + 任务匹配传统 comparator + 廉价扩展；paired
  realization / dev 冻结 / fresh held-out / raw / CI。`PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 才进
  段D；传统 comparator 已解决则 `PROBLEM_RESOLVED_BY_CONVENTIONAL_COMPARATOR`。
- **段D**（段C 问题仍存才触发）：独立 executor 构造运行 3–5 机制不同最小方法，单独 dev 调谐，
  vs tuned comparator，raw/paired CI/help-hurt-tie/语义 smoke/消融/复杂度 →
  `DIAGNOSTIC_METHOD_SIGNAL` 或 `NO_DIAGNOSTIC_SIGNAL`；signal 同时给 primary + fallback packaging。
- 段链完成后一次统一更新 topic-index/mission-log/D/V/必要 owner，一次 commit 不 push。
