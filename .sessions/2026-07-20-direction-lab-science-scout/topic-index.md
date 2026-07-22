# Topic Index: Direction Lab 首轮 SCIENCE_SCOUT 正式科学探索

> 状态: dormant（SCIENCE_FREEZE — campaign-level 收口 D022；candidate rotation 暂停；当前无合法 main-method signal；F1=TESTBED_BLOCKED / F3=UNRESOLVED / F4=INFRASTRUCTURE_BLOCKED；F2 lineage 合并入 Pilot-Jones 正式 GW，不建平行链；负面材料只进 harvest/limitations 不 pivot 完整负面论文；下一权威工作 = Pilot-Jones Step 3.5 终审 + Step 4a，见 H015） | 创建: 2026-07-20 | 最后更新: 2026-07-22 S014/D022/V012/H015：campaign-level reconciliation——用户"经过了这么多轮，咱们是不是该整体想想？"触发收口；修正所有继承 D020/H013 旧结论的 stale current views（state/portfolio/harvest/topic-index/registry）；核清 Pilot-Jones 真实门控（Step 3.5 🔄，V028/V029 均 PARTIAL 封锁 Step 4a；master-state:96 "待V030" 是 stale 指针——V030 实属 P03 非 Pilot-Jones）；protected 文件 byte-identical 未改

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
- **2026-07-21 D009 纠偏（取代 D008 的 verdict 推论链；amended by D010）**：B01-R 科学纠偏批独立复现 B01 的 10 条审计发现（全部 CONFIRM），用无泄漏 seed 切分 + 真实 validation-optimal fixed-μ CMA（μ=0.01，B01 从未运行）+ 4-cat 标签审计重审。**初版 VERDICT B** = `B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`。**但 v1 有 7 个实现 flaw**（min_z2 NaN、warmup 错位、伪 5% FPR、机械触发 VERDICT B、ambiguous 计数冲突、μ 网格边界、C11 vs anchor 而非 vs fixed_μ），其中 4 个 P0 机械触发 verdict B。外部评审 intervention → hotfix v2 修复全部 7 个 flaw。
- **2026-07-21 D010 hotfix v2（amended D009；第 4 点 C11_fixed_mu 4/7 阳性 further amended by D011）**：7 个 flaw 全部修复后 verdict 从 B 改为 **A** = `A_B01R_FAIRNESS_SURVIVES_AND_DETECTOR_TARGET_READY`。关键修正：（1）fixed_μ 最优 μ=0.03（非 0.01；grid 扩展后 interior optimum，μ=0.1 diverged）；（2）~~C11_fixed_mu（stage-1=tuned μ=0.03 + DD-LMS）在 4/7 held-out cells 显著优于 fixed_μ CMA（paired CI 排除 0，|Δ|≈0.01）—— 这是整个 campaign 第一个显著超越公平调参传统 baseline 的方法~~ **[D011 撤回]**：合法化重测后该信号消失甚至反向，reclassified as implementation/confound diagnostic；（3）min_z2_ratio 修复后（output_power fallback）在 2 个 two-class cells AUROC=1.000（超过 "tuned" C05 的 0.875/0.5），conventional baseline 已达 ceiling；（4）lead_time 修复后（warmup guard）实际全 ≤ 0（mean=-5.95），detector 没有真正提前预警；v1 的 "+2 blocks" 完全是 warmup artifact；（5）5% FPR 在 n_neg=2/4/6 下不可解析，实际是 50%/25%/17%；（6）4-cat 标签实际 inner=14/awgn=18/healthy=27/ambiguous=51（v1 写过 43/54/20，全错）；（7）~~forward rule（HF8）要求任何未来 corrector batch 用 fixed_μ + blind-affine 双 task comparator~~ **[D011 修正]**：原 line 352 把 oracle_affine_16qam 标 "blind" 是标签错误；真正的 receiver-visible comparator 是 blind_affine_compare_16qam；oracle_affine_bound_16qam 是 Kill bound only（FR-21/FR-25）。VERDICT A **不自动授权 B02**（detector target thin）。等用户决策下一批方向。
- **2026-07-21 D011 c11-legality（amended D010 第 4 点 + forward rule 第 2 comparator）**：合法化重测 C11（统一 bilinear r@w 约定 / 因果 one-pass CMA→DD switch / 同 pass 预算 / dd_step=0 身份门）verdict = **`B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION`**。C11 原实现的 3 个合法性缺陷独立定位（D1 stage-2 用 `np.vdot` 约定突变；D2 stage-2 从 i=0 用 stage-1 final 权重 = 非因果未来信息；D3 每样本访问 3 次 vs comparator 1 次）。合法 C11 在 7 个 held-out cells × 10 fresh test seeds 上 macro paired Δ = **+0.01445**（C11 更差），CI=[−0.00022, +0.04113]；2/7 long cells 显著更差（snr10-fg100-long +0.025；snr15-fg1000-long +0.077），0/7 更好；5/7 short cells 实质 tie。因果 one-pass per-symbol DD-LMS 反而扰动已收敛 fixed-μ 权重。独立 verifier V003 10/10 CONFIRM。**D010 第 4 点 C11_fixed_mu 4/7 阳性 method signal 撤回**。C04/C09 仍不授权；corrector 必须超越 blind_affine_compare_16qam（receiver-visible）才算贡献。等用户决策下一批方向。
- **2026-07-21 D012 C11 scope-narrow（amended D011，进一步 scope-narrow verdict label + 处理 8 audit issues）**：C11 verdict 标签从 `B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION` scope-narrow 到 `C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`，claim ceiling = LOCAL_SLICE / DIAGNOSTIC。**数值结论（macro +0.01445、2/7 long cells 显著更差、4/7 阳性撤回）不变**。8 audit issues 独立核验全部为真，但无一改变 verdict 方向：#4（UTF-8）+ #5（source closure hash）FIXED；#1/#2/#3/#6/#7/#8 DOCUMENTED 为 scope 限制（偏置朝 C11 而非反方向）。19/19 tests PASS（原 13 + 新 6 portability/provenance gate）。
- **2026-07-21 D013（amended by D016）**：保留 truth-assisted affine local bound 与 blind-affine 净负面数字；撤回 `A_LEARNED_CORRECTOR_TARGET_READY` 和“exists-vs-learnable thesis-grade”解释。
- **2026-07-21 D014（superseded by D016）**：C04/C09 raw 坏结果可复现，但 soft-distance 目标存在输入无关常数最优解；当前结论是 `IMPLEMENTATION_CONFOUND_CONSTANT_COLLAPSE`，候选为 `UNRESOLVED`，不是 exact mechanism negative。
- **2026-07-21 D015（amended by D016）**：由机制负面强制轮转的推理撤回；轮转仅可作为后续资源选择。
- **2026-07-21 D016 科学语义修订**：artifact fidelity 与科学语义分离；V004 保留前者，V005 对后者判 FAIL。旧 H009 失效，H010 成为恢复入口。
- **2026-07-22 D018/D019**：合法 CMA/MMA/DD-LMS 专家间 oracle headroom 仅 0.003693，关闭本具体 blind-expert routing contract；这不等于全局无解。下一步从“换算法”退到“新增什么合法信息”，批量 Probe 模型先验、pilot、时间历史和 decoder/soft feedback，再决定投资哪条方法线。
- **2026-07-22 D020/V009**：信息来源组合级 Probe 完成（F1-A model prior / F3-A history / F4-A decoder-soft）。F1-A PASS — model-based MMSE oracle 关闭 0.133 macro PI-SER headroom（D018 blind-router 的 36×），receiver-visible observability |r|=0.65 强相关；F3-A PASS — 历史 block 增 +0.060 bits MI、+0.036 R² 条件信息；F4-A BOUNDARY — corrected analytic GMI headroom +0.0089 但 smoothing-fragile（verifier P1）+ histogram-MI 复现 C12 scale-artifact + F4-B 需 coded chain（BLOCKED）。F1-B（dual-pol GG/SOP model-based tracker）为首选 Scout，需用户授权约一天基建。F2 pilot 待撞车核查。本轮不直接建 tracker/coded chain/pilot 基建。**[D021/S013 AMENDED — 撤回]** F1-A/F3-A 的 PASS 解读失效（见下）。
- **2026-07-22 D021/S013/V010/V011（amends D020）**：**F1-A 重分类 `PRIVILEGED_CSI_PLUS_TX_CALIBRATION_GENIE_GAP`；F1-A0 严格因果修复 Probe FAILED**。撤回 D020 的 "per-block MMSE / observability PASS / conditional-MI PASS / 正面候选 / 授权一天基建"（原始数值保留）。F1-A0 在 11 cells × test seeds [161-170]：CMA μ=0.03=0.3613 / blind_affine(CMA-fed)=0.3556 / E1 CSI-only=0.1681 / E2 pilot=0.7629(实现破损) / E3 privileged=0.1787 / causal_plugin=0.1685 / nopred=0.1683。g0 FAIL（prediction 无增量，binomial p≈0.38）。**主导 confound 非"model-prior 无价值"**：SOP rotation 在 256-symbol eval window 仅 0.06°（预测任务近空）+ CMA μ 调债（μ=0.01→0.083 vs μ=0.03→0.369，D005/D007 已 flag）。critic 2 子结论 OVERTURNED（blind_affine 被 CMA 污染→g1/g2 失效；E2 pilot 从未发送）。**F1-B 不建（证据不足）；转 F2**。V009/V010 integrity 层数值可复现但科学归因层有缺口（hash 闭包破、无 raw rows、无 fixed-label、comparator 未调用）；V011 critic HOLDS-with-refinement。
- **2026-07-22 D017 e15ae60 继承纠正（混合路由研究前置）**：commit e15ae60（C12/C14/C15/C16 + 重写 current views 为"5 轴穷尽"叙述）的数值**可复现**但 7 审计项（V006）全部 CONFIRM 科学语义失效/不足——C04/C09 O1 目标仍是 self-referential moving target（常数塌缩零损失）→ UNRESOLVED；C12 oracle 仅全局 σ² + histogram-MI scale-invariant → 非真上界（H062 撤回）；C14 0.9995 cosine + far-orthogonal probe 仅 narrative 未在 src → 仅证"最强单 init 塌缩"（H063 scope-narrow）；C15 共 μ=0.03 跨 19× 梯度差 → unequal-step 混淆（H064 撤回机制断言）；**C16 是空间 2×2 + real Givens 非 JADE 无 FIR → 非合法 capability-aligned 专家**（H065 重定性）；**seeds 71-80 在 ≥6 批重复使用 → 失去 held-out 资格**；H060 全域"信道属性/5 轴穷尽/不可提取求逆/可写完整负面边界论文/model-based tracker 唯一剩余"5 宣称 **invalidated**，降级为 LOCAL_SLICE 弱断言。混合路由诊断互补（CMA 0.2507 / HOS 0.4664 / 37 塌缩中 26 个 HOS 更好 / oracle selector 0.1928）**数值真实但建立在非法 C16 专家 + 污染 seeds + 事后 oracle 上，仅 DIAGNOSTIC**。合法 FIR 对齐 fallback = MMA（公平 μ 重测）+ standalone DD-LMS（新建）。未重跑科学实验，未建 controller，未改 protected history。

## 进展线索

- **S001**：campaign 启动；恢复地基、核验 protected history、建立隔离 worktree `direction-lab-capability-atlas`、登记新专题；完成授权迁移（campaign-contract + authorization-projection）、Portfolio Refresh v1（12 维展开 + 8 新 seeds U45-U52 + 4 re-clusterings + 8 priority candidates）、Capability Leverage Atlas v1（5 bundles 评估，CB1 选为首选）、formula-symbol-parameter-provenance.yaml（11 公式/22 符号/14 参数）。D001 CB1 选择 / D002 授权迁移 / D003 provenance 硬门。
- **S002**：CB1 closure 实施（`_dual_pol_channel.py` 参数化 modulation，11/11 closure + 6/6 regression PASS）；baseline Atlas 运行（11 16QAM cells × 10 seeds）；**发现 10/11 cells headroom ≥ MDE，max 0.333**；独立验证 CONFIRM（clean-room verifier）；harvest H010-H015（POSITIVE_MECHANISM_SIGNAL / FAILURE_MECHANISM inner-ring-collapse / REUSABLE_ASSET closure / INFRASTRUCTURE_GAP _cma identity / EVALUATION_INSIGHT 16QAM PI-SER rotations / LOCAL_NEGATIVE snr=5）；D004 本轮不触发 ML Scout，记录 scoped positive + handoff H001。
- **S002 续接 / D005 / H002**：独立审计指出 comparator 任务适配和收敛不足；历史 Atlas 数字不删除，但证据级别收回 `DIAGNOSTIC/SLICE`。D005 取代 D004 的直接 ML 授权；H002 要求先做一个主传统 comparator + 必要廉价扩展的共享裁决，并行准备其他机制候选。
- **S003 / D006 / H003**：baseline adjudication shared batch 完成。实现 MMA（Yang-Werner-Dumont JSAC 2002）作主 Go comparator，5/5 sanity tests PASS，独立 verifier clean-room bit-identical 复现。axis 1（11 cells × 10 seeds）+ axis 2（4 cells × {N=512, N=32768} × 5 seeds）联合裁决 = `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`。机制：MMA 不优于 CMA（H018），N=32768 headroom 不降反升（H019），block-end protocol 是瓶颈但动 CMA anchor 会破 parity（H021）。harvest H016-H022。Portfolio 新增 4 个机制不同候选 C01-C04。D006 条件授权下一对话做 bounded ML Scout（首选 C01 causal collapse detector）。
- **S004 / D007 / H004**：独立复审确认 D006 对公平性、收敛、因果和 recoverability 解释过强；撤回其 ML 直接晋级，保留 raw evidence/资产/harvest。下一入口改为短时机制级扩图、任务专属 comparator/readiness 纠正和有界公平修复，随后立即批跑 `READY` 子集。
- **S005 / D008 / H005**：B01 fairness batch 完成。Portfolio v3 扩图到 13 候选 9 簇（C01-C13），纠正 readiness/comparator；B01 合同冻结 + 实现 4 候选（C05/C08/C10/C11）+ 7/7 sanity PASS + 11×10 全量运行（43-59s）。结论 `PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT`：held-out 7 cells 上 anchor/C08/C10/C11 各只关闭 1/7；C11 是最佳变体（long cells 改善 0.01-0.03，headroom 仍 ≥6×MDE）；C10 per-symbol 否定 H021；C05 detector pooled AUROC=0.6546（long cells=1.000，short cells=0.5）。harvest H023-H028；独立 verifier CONFIRM HIGH confidence 20/20 PASS。D007 公平性债务 #1/#3/#5/#6 CLOSED，#2/#4 PARTIALLY_CLOSED。**条件授权 B02 ML detector batch**（narrowed claim "ML improves lead time / calibration"）。
- **S006 / D009 / H006 / V001**：B01-R 科学纠偏批 v1（用户 10 条审计发现全部独立复现）。VERDICT B（`B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`）。**但 v1 有 7 个实现 flaw** 被外部评审抓出。
- **S008 / D011 / H008 / V003**：C11 合法性裁决 Verdict B（signal disappears after legalization）。根因调查（systematic-debugging Phase 1-3）+ TDD RED→GREEN（13 tests 全 PASS）+ 85s 科学运行 + 独立 verifier 10/10 CONFIRM。C11 原 3 缺陷（复数约定突变 / 非因果未来信息 / 多 pass）独立定位修复；合法 C11 macro +0.01445 更差；2/7 long cells 显著更差。D010 第 4 点（C11_fixed_mu 4/7 阳性）撤回，reclassified as implementation/confound diagnostic。forward rule 第 2 comparator 修正（oracle_affine → blind_affine_compare）。protected history 全未改；无 ML；无 push。**等用户决策下一批方向**。
- **S009 / D012 / D013 / D014 / D015 / H009 / V004（历史运行记录，科学解释已由 S010/D016/V005 修订）**：当时连续完成 C11 收口、corrector adjudication、C04/C09 运行和 artifact verifier。raw 数字、seed/hash 与历史保护保留；其中 `A_LEARNED_CORRECTOR_TARGET_READY`、`EXACT MECHANISM NEGATIVE` 和强制轮转均不得作为当前结论。
- **S010 / D016 / V005 / H010**：外部科学语义审计定位 soft-distance 常数塌缩（四维最小 loss 约 1.30840175，与 plateau 一致）；撤回 D014 机制负面与 D013 learned-target-ready 解释，C04/C09 恢复 `UNRESOLVED`。建立 harvest v7 修订和唯一恢复入口 H010；科学运行暂停，转体系专题设计轻量 Probe 与恢复结构。
- **S011 / D017 / V006**：混合路由研究前置 reconciliation。发现 e15ae60 在 H010 之后提交却未登记 S/D/V/H（注册表 last_updated 仍 2026-07-21），其"5 轴穷尽"叙述未经治理。独立子 agent + 主线复算 7 审计项全部 CONFIRM：数值可复现但 C12/C15/C16 科学语义失效、C14 scope 不足、C04/C09 UNRESOLVED、seeds 71-80 失去 held-out。H060 降级 + 拆分。以 D017 为干净起点进入混合路由 Macro A/B/C。本轮最多新建 1 个 S###（即本 S011），D/V 继续追加。
- **S011 / D018 / V007 / H011**：合法 FIR 专家 Macro A 完成；oracle headroom 0.003693 < 0.03，裁决 C，未训练 router。旧 task-mismatched HOS 互补信号失效。本轮只形成 LOCAL_SLICE 负面与方法论教训。
- **D019 / H012 / V008**：修复 current views 的残留矛盾与无效 harvest YAML；独立终验 PASS。下一轮不把 model-based tracker 当唯一方向，先做信息来源候选族的组合级 headroom/observability Probe。
- **S012 / D020 / V009 / H013**：信息来源组合级 Probe 批次完成。冻结共享 contract（probe-contract.v1.yaml：同 anchor/slice/eval-window/paired-realization/fresh seeds [141-150]）；候选 Map（candidate-map.v1.md：四族 F1-F4 × 作用点 × 动作）；3 个 headroom Probe + 10/10 identity/smoke gate PASS + 独立 verifier CONFIRM（0 P0，1 P1 documented）。F1-A model-prior oracle 0.133 headroom + |r|=0.65 observability = campaign 首个正面信号；F4-A 确认 C12 scale-artifact（histogram invariant）。下一步交用户决策 F1-B 投资选择（推荐 A：~1 天 tracker 基建 + Scout）。**[S013/D021 AMENDED]** 该解读被撤回——见下条。
- **S013 / D021 / V010 / V011 / H014**：**F1-A0 严格因果可观测性修复 Probe FAILED**。S012/D020 的 F1-A "PASS" 解读被源码级审计撤回（D021）：F1 genie 同时用 true h/θ + TX-truth LS calibration（`PRIVILEGED_CSI_PLUS_TX_CALIBRATION_GENIE_GAP`）；observability 特征读全流 trace 含未来 block 且 target 是事后 headroom 残差；F3 是 marginal-MI max-difference 非 conditional MI；blind_affine_compare_16qam 从未调用；F1 artifact 未存 fixed-label/raw rows；F1/F3 artifact 的 F4 source hash 与当前源码不一致（11 项缺口，D021 §理由 逐条 `file:line`）。F1-A0 在 11 cells × test seeds [161-150→161-170] 上 FAIL（g0 prediction 无增量：8 help/13 hurt/89 tie，binomial p≈0.38；E1≈E3≈causal_plugin≈nopred 全 ~0.168）。独立 critic（V011）+ 主线复核：FAIL 存活但原因是 **(SOP rotation 256-symbol eval window 仅 0.06° 使预测任务近空) + (CMA μ=0.03 调债 μ=0.01→0.083)**，非"model-prior 无价值"普适结论；2 子结论 OVERTURNED（blind_affine 被 CMA 污染 → g1/g2 失效；E2 pilot 实现破损）。**F1-B 不建（证据不足）；转 F2 collision check 待用户裁决**。未改 protected history/STATUS.v1.md/canonical-state；无 push；1 次 consolidated commit。

## 未决项

- **F2 collision check vs harvest 收尾 vs 重测 F1 家族（待用户裁决，S013/H014）**：F1-A0 FAIL 后三选项。(a) F2 pilot 撞车核查（JLT2023/OE2021/LCOMM2026/TCOMM2025/JLT2022-23）；(b) pivot 到 harvest/负面边界论文；(c) 重测 F1 家族须先换 high-SOP-rate atlas + μ-tuned CMA + raw-stream blind_affine + 真 persistence/AR(1) baseline（V011 五项）。
- **STATUS.v1.md "protected unchanged" vs bf620b3 实际 +9/-4 diff 矛盾（D021 gap #10）**：本轮不改（提示词禁），交主控裁决。
- **canonical project.v1 vs SCIENCE_SCOUT projection controller ownership 冲突未解（D021 gap #11）**：本轮不静默修改，仅记录报告。
- **F1-A0 artifact 债务（V011）**：未存 ridge probe 权重 + prefix-feature 向量 + per-sample h/theta，0.06° 从模型推导非数据验证。下一 Probe 须补 raw-rows 字段。
- **B02 ML detector batch 不自动授权**（D010）：detector target 是 "ready" by contract letter 但 thin（2 个 two-class cells；ML 不能在 AUROC 上赢 ceiling；lead time 负）。B02 若跑需换目标。
- **C04/C09 科学状态为 UNRESOLVED**（D016）：本次失败先归因于训练目标常数塌缩；不立即重跑，等新 Probe 方法固定。
- **新的科学 rotation 暂停**：先在体系专题完成 D012 的 Probe/恢复/文件组织设计、推演和 Skill 修订。
- Portfolio 候选 C01-C13 已写卡：C05/C08/C10/C11 已运行（B01 + B01-R 两次）；C11 合法版已运行（c11-legality-batch-v1，Verdict B，D012 scope-narrow）；C04/C09 已运行（c04-c09-shared-corrector-v1，BLOWS_UP）；C01/C02/C06/C13 = NEEDS_SMALL_ADAPTER；C03/C07/C12 = INFRASTRUCTURE_BLOCKED。
- `_cma.py:CMAEqualizer2x2` scalar-error 与 docstring/canonical "Godard-with-z" 不一致（H013 OPEN_ACKNOWLEDGED，pre-existing）。
- 16QAM R²=1.32 未 canonical 化。
- **H021 债务 DOWN-GRADED**：C10 per-symbol 直接测试 + B01-R paired CI（与 anchor 无显著差异）表明 block-end 协议不是 collapse 瓶颈。
- **D007 #2 部分闭合 / #4 DOWNGRADED**：convergence N 在 N=8192 上 paired CI 显著（未到 ~1e5）；oracle recoverability 因 4-cat 标签揭示 inner-ring 群体远小于预期而降级。
- **C05 未真调参**：default-grid fallback；synthesis 措辞收紧为 "default-grid C05"；后续 detector batch 在更丰富 label infra 上重 tune。
- **detector target thin**：VERDICT A 但仅 2 two-class cells；conventional min_z2 已 AUROC=1.000 ceiling；ML 须在 lead time / calibration / generalization 上赢，不能在 AUROC 上赢。
- **C11 dd_step + switch_point 在 long cells 上不稳**（D011 NEW）：因果 per-symbol DD 对已收敛 fixed-μ 权重反而扰动；若未来要重新评估 DD-LMS 需多 switch policy + 更稳 dd schedule。
- **C11 audit issues #1/#2/#3/#6/#7/#8 已 DOCUMENTED 但未 FIX**（D012）：均为 scope 限制（非缺陷），偏置朝 C11 而非反方向；若未来要重新评估 DD-LMS 需先解决（扩 dd_step/offset grid / 改 short-cell eval window / 加 phase/permutation resolution）。

## 当前位置

S014 / D022 / V012 / H015：**SCIENCE_FREEZE — campaign-level 收口。** 用户"经过了这么多轮，咱们是不是该整体想想？"触发整体反思。裁决（D022）：SCIENCE_SCOUT candidate rotation 暂停（本专题置 dormant）；**当前没有合法 main-method signal**；F1=TESTBED_BLOCKED（rotation 0.06° 使 testbed 对 F1 家族近空）/ F3=UNRESOLVED（F3-A 非 conditional MI）/ F4=INFRASTRUCTURE_BLOCKED（coded chain）；**F2 pilot lineage 合并入已有 Pilot-Jones 正式 Groundwork，不建平行 Scout（F2 collision check 本轮不执行）**；负面材料只进 harvest/limitations，**不 pivot 完整负面论文**（H060 全域 5 宣称已被 D017 invalidated）。修正所有继承 D020/H013 旧结论的 stale current views（state/portfolio/harvest/topic-index/registry）。核清 Pilot-Jones 真实门控：**Step 3.5（🔄 in progress）**，V028/V029 均 PARTIAL 显式封锁 Step 4a；master-state.md:96 的"待V030"是 **stale 指针**（V030 实属 P03 residual-headroom 终验，非 Pilot-Jones）；Pilot-Jones Step 3.5 缺一个独立终审 V### + 4 个直接竞品全文精读（OE2021 已读，JLT2022-23/TCOMM2025/LCOMM2026 仅 abstract）。**下一权威工作 = Pilot-Jones Step 3.5 终审 + Step 4a prerequisites**（见 H015），不是新 F2 collision search。protected 文件（STATUS.v1.md / project.v1.yaml / canonical-state / 历史 artifacts）byte-identical 未改；STATUS.v1.md = STALE_PROTECTED（不是当前科学事实源），project.v1.yaml = historical read-only-preview adapter（不是当前授权 owner）；当前可信事实源 = 修正后的 state/current.yaml + D022/H015。无仿真/Probe/collision check；无 tracker/pilot/ML/testbed 实现；无 push。唯一恢复入口 H015。
