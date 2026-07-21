# Topic Index: Direction Lab 首轮 SCIENCE_SCOUT 正式科学探索

> 状态: active | 创建: 2026-07-20 | 最后更新: 2026-07-21（S006/D009/H006/V001：B01-R 纠偏批完成，VERDICT B = fairness survives + detector target NOT ready；撤回 B02 授权；rotation 入口 H006）

## 专题信息

- **slug**: `2026-07-20-direction-lab-science-scout`
- **性质**: 正式科学探索（首轮 SCIENCE_SCOUT campaign），不是蓝图/治理/迁移专题
- **worktree**: `.worktrees/direction-lab-capability-atlas`（分支 `codex/direction-lab-capability-atlas`，从 `65db4ef`）
- **流程拥有者**: `.agents/skills/research-direction-lab/SKILL.md`（7-phase loop）

## 范围边界

### 原始目标（冻结，来自用户 2026-07-20 执行提示词）

在双偏振星地 OSL 接收机中的"合法 ML 信息增量"目标范围内，启动首轮正式 SCIENCE_SCOUT campaign：恢复 → Portfolio Refresh → Capability Leverage Atlas → 共享能力建设 → baseline/headroom 探针 → 多候选批量 Scout → synthesis → harvest → 自动轮换。如果首选共享能力不成立，自动回到 Portfolio 选择下一项；不在每个小步骤等待用户确认。

### 当前范围

- 授权状态从 `READ_ONLY_MIGRATION_PREVIEW` 迁移为本轮限定的 `SCIENCE_SCOUT`（新 campaign contract + 新状态投影，不改写历史 projection）；
- 在隔离 worktree 中执行 Portfolio Refresh、Capability Leverage Atlas、共享能力建设、baseline/headroom 仿真、小规模 ML Scout、synthesis、harvest、自动轮换；
- 处理 stale internal checksum / last_completed_batch pointer 等债务时显式登记，用新 projection/event 或明确迁移记录解决；
- 建立并维护 `formula-symbol-parameter-provenance.yaml`（公式/符号/参数来源硬门）。

### 明确不含

- 不修改或重跑 B001–B003、P03 Atlas 的原始历史字节；
- 不创建 legacy B004；
- 不把 Scout/Sandbox 数字自动写入论文正文；
- 不自动宣称 candidate/family/domain 级别结论；
- 不绕过 Groundwork/Contract/Execute 完成正式晋级；
- 不 push、不 merge、不修改 dirty 普通根 worktree；
- 不为让 ML 获胜而修改物理参数、baseline、指标或比较口径；
- 不复制 protected history 数字到新 ledger 而不重新 hash 绑定。

### 范围变更记录

（无；首轮启动）

## 不变量

- canonical baseline = `baseline.standard_cma.godard_z`（含 Godard z 因子），身份严格分离 current-CMA / no-z；不跨域宣称 standard-CMA 永不 swap。
- metric contract = `fixed_label_ber` + `permutation_invariant_ber` 双报；二者语义不得互换。
- B001–B003、P03 Atlas、canonical state、completion events、receipts 字节不可改；B004 不存在且本轮不创建 legacy B004。
- Sandbox/Scout 数字不自动晋级 Groundwork/Contract/Execute/论文；晋级须用户明确 strategy 决策。
- 主对话严禁 WebSearch/webReader；论文精读、web 查询、批量引用筛查必须子 agent 执行。
- 公式/符号/参数进入实现前必须建立 provenance（equation/page/section 精确出处，或标 `DERIVED_IN_PROJECT` + 交叉验证，或 `DEFINED_HERE`）。
- baseline 来源必须区分原始方法/权威复现/代表性使用，正文公式不可用标题联想替代。
- oracle/scoring-only 上界只作 Kill 工具（Step 4a 维度 D / FR-21），不当 Go 判据（FR-25）；Go 标准 = 赢传统未优化 baseline。

## 已确认结论

### 不变量

（首轮启动；尚未产生本专题的架构级不变量。继承自 anchor 的不变量见上节。）

### 其他结论

- CB1 证明当前单模 CMA/长度合同下存在 inner-ring collapse 与 scoring-only oracle gap，但尚未证明问题经过任务适配的传统 baseline 后仍存在。
- baseline 不必是当前 SOTA；一个来源闭环、广泛采用、任务适配且公平的 comparator 足以支撑有限主张。
- **2026-07-21 D007 纠正**：S003 的 raw CMA/MMA 数值与局部失败观察有效，但同 `mu` 不等于公平调参，`N=32768` 不等于约 `1e5` 收敛闭合；当前科学状态退回 `DIAGNOSTIC/SLICE`，不得把 task-mismatch、under-convergence 或 block-end 真因写成已排除/已证明。
- **oracle 边界**：oracle affine 只能证明特权映射存在；receiver-visible trace 是否足以识别该映射仍未验证。C01 可先验证 observability，但检测本身不代表 PI-SER 改善。
- **教科书结果不外推**：MMA > CMA on 16QAM 在 fiber-coherent 成立但在 OSL+GG+SOP+block-end 下不成立（H018）。这是可毕业的负面论文材料。
- **2026-07-21 D008 公平闭合**：CB1 16QAM inner-ring collapse 在 per-method tuning（C08 bandit）、per-symbol 结构变化（C10 block_size=1）、CMA+DD-LMS 级联（C11）下**均存活**（held-out 6/7 cells headroom ≥ MDE）。**坍塌是 Godard cost 在该信道下的深层属性**，不是 block-end 协议 artifact（H021 被 C10 直接否定，H024）。C05 传统阈值 detector 在 long cells AUROC=1.000，pooled 0.6546 → 条件授权 B02 ML detector（narrowed claim）。
- **2026-07-21 D009 纠偏（取代 D008 的 verdict 推论链）**：B01-R 科学纠偏批独立复现 B01 的 10 条审计发现（全部 CONFIRM），用无泄漏 seed 切分 + 真实 validation-optimal fixed-μ CMA（μ=0.01，B01 从未运行）+ 4-cat 标签审计重审。**VERDICT B** = `B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`：fairness 存活更强证据（fixed_μ CMA 在 7/7 held-out cells 显著优于 frozen-μ anchor；C11 在 4/7 显著小改善 |Δ|≤0.026；C10 与 anchor 无显著差异；C08 混合），**但 detector target 不 READY**（4-cat 标签审计显示 B01 的 `oracle_pi_ser > 0.3` 把 AWGN 错误误当 collapse；只有 14/110 seeds 是 true inner-ring；held-out 长窗 cells 的 inner-ring 数 = 0；只有 2 个 held-out cells two-class）。**撤回 B02 ML detector 授权**；rotation 转向非 detector 机制族（equalizer 学习型校正器 C04/C09，或不同信息类 C13/C12）。

## 进展线索

- **S001**：campaign 启动；恢复地基、核验 protected history、建立隔离 worktree `direction-lab-capability-atlas`、登记新专题；完成授权迁移（campaign-contract + authorization-projection）、Portfolio Refresh v1（12 维展开 + 8 新 seeds U45-U52 + 4 re-clusterings + 8 priority candidates）、Capability Leverage Atlas v1（5 bundles 评估，CB1 选为首选）、formula-symbol-parameter-provenance.yaml（11 公式/22 符号/14 参数）。D001 CB1 选择 / D002 授权迁移 / D003 provenance 硬门。
- **S002**：CB1 closure 实施（`_dual_pol_channel.py` 参数化 modulation，11/11 closure + 6/6 regression PASS）；baseline Atlas 运行（11 16QAM cells × 10 seeds）；**发现 10/11 cells headroom ≥ MDE，max 0.333**；独立验证 CONFIRM（clean-room verifier）；harvest H010-H015（POSITIVE_MECHANISM_SIGNAL / FAILURE_MECHANISM inner-ring-collapse / REUSABLE_ASSET closure / INFRASTRUCTURE_GAP _cma identity / EVALUATION_INSIGHT 16QAM PI-SER rotations / LOCAL_NEGATIVE snr=5）；D004 本轮不触发 ML Scout，记录 scoped positive + handoff H001。
- **S002 续接 / D005 / H002**：独立审计指出 comparator 任务适配和收敛不足；历史 Atlas 数字不删除，但证据级别收回 `DIAGNOSTIC/SLICE`。D005 取代 D004 的直接 ML 授权；H002 要求先做一个主传统 comparator + 必要廉价扩展的共享裁决，并行准备其他机制候选。
- **S003 / D006 / H003**：baseline adjudication shared batch 完成。实现 MMA（Yang-Werner-Dumont JSAC 2002）作主 Go comparator，5/5 sanity tests PASS，独立 verifier clean-room bit-identical 复现。axis 1（11 cells × 10 seeds）+ axis 2（4 cells × {N=512, N=32768} × 5 seeds）联合裁决 = `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`。机制：MMA 不优于 CMA（H018），N=32768 headroom 不降反升（H019），block-end protocol 是瓶颈但动 CMA anchor 会破 parity（H021）。harvest H016-H022。Portfolio 新增 4 个机制不同候选 C01-C04。D006 条件授权下一对话做 bounded ML Scout（首选 C01 causal collapse detector）。
- **S004 / D007 / H004**：独立复审确认 D006 对公平性、收敛、因果和 recoverability 解释过强；撤回其 ML 直接晋级，保留 raw evidence/资产/harvest。下一入口改为短时机制级扩图、任务专属 comparator/readiness 纠正和有界公平修复，随后立即批跑 `READY` 子集。
- **S005 / D008 / H005**：B01 fairness batch 完成。Portfolio v3 扩图到 13 候选 9 簇（C01-C13），纠正 readiness/comparator；B01 合同冻结 + 实现 4 候选（C05/C08/C10/C11）+ 7/7 sanity PASS + 11×10 全量运行（43-59s）。结论 `PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT`：held-out 7 cells 上 anchor/C08/C10/C11 各只关闭 1/7；C11 是最佳变体（long cells 改善 0.01-0.03，headroom 仍 ≥6×MDE）；C10 per-symbol 否定 H021；C05 detector pooled AUROC=0.6546（long cells=1.000，short cells=0.5）。harvest H023-H028；独立 verifier CONFIRM HIGH confidence 20/20 PASS。D007 公平性债务 #1/#3/#5/#6 CLOSED，#2/#4 PARTIALLY_CLOSED。**条件授权 B02 ML detector batch**（narrowed claim "ML improves lead time / calibration"）。
- **S006 / D009 / H006 / V001**：B01-R 科学纠偏批完成（用户提出 10 条审计发现，全部独立复现 CONFIRM）。冻结独立合同 + 实现 runner + 4-cat 标签审计 detector + paired bootstrap CI，64.5s 全量运行。VERDICT `B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`：fairness 存活（强证据：validation-optimal fixed-μ CMA μ=0.01 在 7/7 held-out cells 显著优于 frozen-μ anchor；C11 4/7 cells 显著小改善 |Δ|≤0.026；C10 无显著差异 confirm H024；C08 混合），但 detector target NOT READY（4-cat 标签审计后只有 14/110 seeds 是 true inner-ring；held-out 长窗 cells inner-ring=0；只有 2 个 held-out cells two-class）。**撤回 B02 ML detector 授权**。harvest H029-H034；独立 verifier CONFIRM 11/11 checks PASS（V001）。rotation 入口 H006（路径 1：equalizer 学习型校正器 C04/C09，task comparator = fixed_μ CMA μ=0.01；路径 2：不同信息类 C13/C12）。

## 未决项

- **B02 ML detector batch 已撤回授权**（D009）；collapse label 基础设施未建（4-cat 标签审计显示 inner-ring seeds 太少且不在 held-out 长窗；oracle affine 不充分区分 collapse vs AWGN）。
- Portfolio 候选 C01-C13 已写卡：C05/C08/C11 已运行（B01 + B01-R 两次）；C01/C02/C04/C06/C09/C10/C13 = NEEDS_SMALL_ADAPTER；C03/C07/C12 = INFRASTRUCTURE_BLOCKED。
- 下一轮 rotation 方向待用户拍板：路径 1（equalizer 学习型校正器 C04/C09，comparator = fixed_μ CMA μ=0.01）vs 路径 2（不同信息类 C13/C12）。无战略变化时默认路径 1。
- `_cma.py:CMAEqualizer2x2` scalar-error 与 docstring/canonical "Godard-with-z" 不一致（H013 OPEN_ACKNOWLEDGED，pre-existing）。
- 16QAM R²=1.32 未 canonical 化（仅 CB1 closure 中定义）。
- **H021 债务 DOWN-GRADED**：C10 per-symbol 直接测试（H024）+ B01-R paired CI（与 anchor 无显著差异）表明 block-end 协议不是 collapse 瓶颈。
- P03 `claim-scope-validation-receipt.v1.yaml` SHA 与 `claim-scope-assessment.v1.yaml` 不匹配（pre-existing at base commit，与本轮无关）。
- stale `_dual_pol_channel.py` checksum（行尾差异）已在 authorization-projection.v1.yaml 登记。
- **D007 #2 部分闭合 / #4 DOWNGRADED**：convergence N 在 N=8192 上 paired CI 显著（但未到 ~1e5）；oracle recoverability 因 4-cat 标签审计揭示 inner-ring 群体远小于预期而降级（需更丰富 oracle 类或 representation learning）。
- **C05 default-grid fallback**：B01-R 中 C05 macro-AUROC tuning score=-1.0（4-cat 让所有 validation cells single-class），按合同 fallback 到 grid 首项；honest 报告，但 detector 未真调参。
- **Validation cells 在 test seeds 上也运行**：intentional（报告覆盖 + Go/Kill 仅 held-out），无泄漏，但若未来严格隔离需重设计 evaluate_held_out。

## 当前位置

S006 / D009 / H006 / V001：B01-R 科学纠偏批完成，VERDICT B + 独立 verifier CONFIRM。下一入口 H006：路径 1（equalizer 学习型校正器 C04/C09，task comparator = fixed_μ CMA μ=0.01，narrowed claim "learned corrector recovers residual error that DD-LMS (C11) cannot"）或路径 2（不同信息类 C13 pilot-aided / C12 coded）。默认无用户战略变化时走路径 1。
