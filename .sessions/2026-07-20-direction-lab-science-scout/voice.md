# Voice — Direction Lab 首轮 SCIENCE_SCOUT 正式科学探索

> 用户/导师原话档案，按日期。除零信息推进/应答外都收，不去重。
> 仅标 →产出(可选) 和 ⟶冲突；导师/批注标来源。原话占主体，不加说明。

## 2026-07-20

> "你现在获得明确授权，启动 Research Direction Lab 的第一轮正式 SCIENCE_SCOUT campaign。" → S001

> "不要开 Goal。不要停在只读规划阶段。在授权范围内连续推进：恢复 → Portfolio Refresh → Capability Leverage Atlas → 共享能力建设 → baseline/headroom 探针 → 多候选批量 Scout → synthesis → harvest → 自动轮换。"

> "如果首选共享能力不成立，自动回到 Portfolio 选择下一项；不要在每个小步骤等待用户确认。只有战略范围改变、重大资源投入、完整 Portfolio 合法路径耗尽或完整 thesis route 二选一时才询问用户。"

> "本对话最终最多提交一次，不 push。"

> "不要用'治理通过'冒充科学进展。必须让我能看懂：这轮到底扩宽了什么；baseline 是否可信；哪些公式和参数有高水平文献支持；到底有没有找到 ML 值得进入的区域；即使没有正结果，留下了什么可以用于毕业论文的内容。"

> "不要把 CMA、P03、residual、pilot 或旧 CandidateMap 当成科学边界。"

> "现在开始：先恢复 STATUS 和授权边界，创建隔离 worktree，然后完成 Portfolio Refresh 与 Capability Leverage Atlas。证据支持后继续建设首个共享能力并运行 baseline Atlas，不要在规划完成后提前停止。"

- "是。你这套我很同意。你快想想怎么改skill，怎么更新日志。当然，baseline说得过去就行，不必追目前最好，只要比大量人都在用的baseline好，那就行。" → D005

## 2026-07-20（续 — SCIENCE_SCOUT 第二对话，baseline 裁决）

> "不要停在规划或接口层；在边界内尽可能连续推进到一次真正的 baseline 科学裁决、明确的基础设施阻断，或合法路径自动轮转。"

> "baseline 不必是当前 SOTA。不得为了'严谨'无限追逐最新方法。"

> "只有正式目标/场景改变、重大资源投入、多个成熟论文路线必须二选一，或所有合法 Portfolio 路径都耗尽时，才询问我。"

> "当有限主张已经有合理 comparator，且显而易见的廉价替代解释已经处置，立即停止扩展 baseline，不做传统算法穷举。"

## 2026-07-21

- "只是一定要保证公平性？我很担心随着推进会出现和baseline标准不一致的问题。以及，这一批没找多少啊？你觉得是多找十几个方向还是直接现在就开始？" → D007
- "是。你稍微改一下skill，然后给我新对话提示词吧" → D007, H004

## 2026-07-21（续 — SCIENCE_SCOUT 第三对话，B01 fairness batch）

> "你现在接续 Research Direction Lab 的正式 SCIENCE_SCOUT。"

> "不要开 Goal。不要 push。整个对话最多做一次 consolidated commit。"

> "本轮目标：在一个连续对话内完成三个宏阶段：A. 恢复与机制级 Portfolio 扩图；B. baseline/readiness 收口并运行首批；C. synthesis、harvest、独立复核和交接。"

> "不要停在规划、接口 smoke 或候选列表。只要存在合法可运行路径，就继续推进。"

> "局部失败、单候选阻断或模型不工作时自动换候选；不要停下来问我。"

> "检测 AUC 再高也不能写成 PI-SER 改善。"

> "如果公平修复后问题被传统方法关闭，保留负面结果并自动轮换其他候选族，不为保住 ML 方向修改条件。" → D008

> "整个对话只做一次 consolidated commit，不 push。"

## 2026-07-21（续 2 — SCIENCE_SCOUT 第四对话，B01-R 科学纠偏批）

> "继续当前 worktree 和分支，不要另开 worktree，不要 push。"

> "本轮不是继续 B02，也不是扩展候选池，而是完成一次有界的 B01-R 科学纠偏批。请连续推进到能够重新裁决"B02 是否 READY"为止，不要只写计划或做表面文档修补。"

> "明确承认并独立复现以下审计发现，不得直接沿用 D008 的裁决。"

> "若任一事实不能复现，记录具体证据，不要猜测。"

> "C10 只能否决本次确切 `block_size/μ/N` 配置，除非有额外证据，不得关闭整个 block-end causality。"

> "single-class cell 的 AUROC 写 `NA/UNDEFINED`，禁止写 0.5。"

> "如无法建立可信 collapse 标签，诚实结论应是 DETECTOR_TARGET_NOT_READY，不要强行授权 B02。"

> "不得用跨异质 cell 的单一 pooled AUROC 掩盖 cell composition，也不得把"两个可分 cell AUROC=1"解释成"所有长窗都可靠"。"

> "最终 claim ceiling 最高仍为 SLICE。禁止写"Godard-cost 深层属性""所有传统处理均失败"等超出证据的话。"

> "如果 verifier 发现 P0/P1，修复后重新独立复核；不得靠改报告措辞掩盖执行问题。"

> "请连续执行到重新裁决完成；普通的局部失败、参数不工作或单候选阻断不要停下来问我，按上述 A/B/C 自动收口。" → D009, H006

## 2026-07-21（续 3 — 外部评审 intervention on B01-R v1）

[来源:外部评审] "结论：B01-R 比上一轮好很多，真正修复了切分和 fixed-μ baseline；但仍不能按"最终闭环 PASS"接收。当前应标为：PARTIAL / B-like" → D010

[来源:外部评审] "Verdict B 被 min-z2 bug 强制产生。[min_z2_ratio_score] 只读取 `z2_over_R2_ratio`，但实际 anchor trace 只有 `output_power`。其他代码知道需要从 `output_power` 换算，唯独这个 baseline 没做。因此：所有 min-z2 score 都是 NaN；所有 cell 的 n_scores=0；裁决器又要求两个 detector baseline 都至少有两个 two-class cells；所以 Verdict B 被机械触发。"

[来源:外部评审] "2-block lead time 是 warmup 错位。onset 从 warmup 后开始计算，但 detector 从 block 0 就允许报警。"

[来源:外部评审] "recall@5%FPR 实际不是 5%。每个 cell 只有 2–4 个 negative，不可能可靠估计 5% FPR。"

[来源:外部评审] "C11 的"4/7 显著改善"只成立于相对旧 μ=0.001 anchor。相对新的公平 baseline fixed-μ=0.01，C11 在 7/7 held-out cells 的平均 PI-SER 都更差。因此：C11 不能继续算成正面方法信号。"

[来源:外部评审] "μ=0.01 是 μ 搜索网格的最大值。最优点落在边界，一般意味着搜索范围可能还没覆盖真正最优值。"

[来源:外部评审] "整体评价：这轮有真实科学进展，尤其是发现旧 CMA 严重欠调、建立独立 test seeds、拆开 AWGN 与 recoverable collapse；但 verifier 又漏掉了"全 NaN baseline、warmup 错位、伪 5% FPR"。因此现在不要开 B02，也不要直接开 C04/C09。先在原对话完成这个小修复，交给我再审；通过后再开新对话进入下一批。" → D010, H007

[来源:外部评审] "若评估 DD-LMS，必须运行 fixed-μ=0.01 CMA + DD-LMS，并直接与 fixed-μ CMA 比。"

[来源:外部评审] "C04/C09 若以后运行，除了 system anchor，还必须保留同任务的 blind-affine comparator。" → HF8 forward rule

## 2026-07-21（C11 legality batch / S008 / D011 / H008）

[来源:外部评审] "在统一复数滤波约定、无未来信息、同 pass/同预算、dd_step=0 身份门成立的前提下，合法的 CMA→DD-LMS 是否仍显著优于公平 fixed-μ CMA？" → D011

[来源:外部评审] "先做根因调查，禁止立即修代码。逐调用链核验 standard_cma_godard_with_z 和 c11_cma_dd_lms_cascade 的实际复数滤波约定。"

[来源:外部评审] "公式必须附来源、公式号或页码；若项目已有来源优先复用，不得凭文字重建。"

[来源:外部评审] "新建专门的可执行测试文件，必须亲眼看到每个测试因现有实现问题而失败，再改生产代码。"

[来源:外部评审] "complex convention test: 用手算可验证的复数输入和权重，保证 CMA stage 与 DD stage 使用完全相同的滤波定义。测试必须能抓出 r @ w 与 np.vdot(w,r) 的差异。"

[来源:外部评审] "no-op identity test: dd_step_size = 0 必须满足 C11 stage-2 输出与其 stage-1 comparator 逐位一致；PI-SER、fixed-SER、headroom、divergence、eval window 完全一致；不允许只比较均值。"

[来源:外部评审] "causal-prefix invariance test: 改变未来样本，不得改变更早时刻的输出、动作或权重。"

[来源:外部评审] "默认选择'因果 one-pass CMA→DD 切换'。只有在权威文献明确要求离线 multi-pass 且本项目愿意把 claim 限定为离线接收机时，才允许 two-pass。"

[来源:外部评审] "不要再修改 fairness-batch-b01r-v1.json / fairness-batch-b01r-v1-synthesis.md / 旧 batch-contract.v1.yaml / 0404f47/57384ed 对应的历史产物。"

[来源:外部评审] "数据切分使用全新 seeds，不复用 11–30：validation/tuning seeds：31–35；test seeds：41–50。"

[来源:外部评审] "不要再把 28 个未校正的 per-cell CI 全称为'显著'。"

[来源:外部评审] "裁决只能三选一：A_C11_CAUSAL_SIGNAL_SURVIVES / B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION / C_C11_ARCHITECTURE_BLOCKED。"

[来源:外部评审] "局部实现失败、参数不工作或旧信号消失时不要停下来问我；继续完成 A/B/C 裁决。" → D011 verdict B

[来源:外部评审] "实现和独立验证必须使用不同 subagent/context。主线程负责范围、证据综合和最终裁决。"

[来源:外部评审] "不得继续把 oracle_affine_bound_16qam 写成 blind affine。" → H043

## 2026-07-21（S009 C11 状态收口 + corrector residual adjudication 启动）

- "C11 状态应收窄为 `C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`，claim ceiling = LOCAL_SLICE / DIAGNOSTIC" → D012
- "允许保留：旧 4/7 阳性由实现混淆造成；当前具体因果 raw-decision 策略没有发现收益；两个 long slices 上明显更差"
- "禁止声称：整个 DD-LMS 家族失败；C11 已被全域关闭；7 个 cells 都充分测试了 DD 阶段"
- "修复 UTF-8 可移植性测试和最小 provenance 记录；按 session-governance 将原正式 Verdict B 标为 amended/PARTIAL，不删除历史"
- "不要重跑完整 C11 科学批，除非独立审查证明某项最小修复会改变已有数值方向"
- "本对话至少完成一个科学 adjudication，并对一个后续机制形成 RUN / LOCAL_NEGATIVE / INFRASTRUCTURE_BLOCKED 之一；普通文档债务不构成提前停止理由"
- "在公平调优的 fixed-μ CMA（当前 μ=0.03）之后，最强 receiver-visible blind affine 能关闭多少可恢复 PI-SER 余量？相对于 TX-truth oracle affine，是否仍存在足够支撑 C04/C09 learned corrector 的合法 residual target？"
- "新建版本化、隔离的 adjudication 目录，不覆盖 B01、B01-R、C11 或旧 Headroom Atlas"
- "oracle affine 只能 Kill，不能 Go"
- "在读取 test 结果前冻结 A/B/C 判据"
- "只允许一次有针对性的 atlas 扩展，禁止无限加 seeds 或调阈值"
- "同一方向连续两轮没有新机制、改善不足 10%，立即轮转"
- "不允许把多个模型名冒充多个机制方向"
- "harvest 必须记录正结果、负结果、baseline 边界、失败机制、评估教训和可复用资产，但不得把数量当作独立贡献数量"
- "禁止只回复'下一步建议'。在合法边界内连续完成上述链条"

## 2026-07-21（S009 外部审计与后续体系重设计）

- "我必须说，你每次说\"极小\"，最后都会跑挺久。所以，咱们的方法论，是不是哪里不太好呢？以及，我问问，咱们现在，有日志吗？如果之后再回顾目前，能知道情况吗？后续汇总起来，会很麻烦吗？" → D016, D012（体系专题）
- "是。你先记日志吧。然后我打算让你改一下skill，之后去大规模跑（需要优化记录方式，让后续能快速恢复，这个得好好想想，且需要推演，之后固定下来。包括文件组织形态）。" → H010, D012（体系专题）

## 2026-07-22（S011 混合盲均衡/专家路由 — 继承状态纠正 + 系统研究）

> "继续现有 SCIENCE_SCOUT 专题，开展'坍塌感知的混合盲均衡/专家路由'系统研究。本轮属于 SCIENCE_SCOUT，不进入正式 Groundwork/Contract/Execute，不把 Scout 数字写进论文正文。"
> "不要另开 worktree，不要 push。整个对话最多一次 consolidated commit。不得修改 B001–B003、P03 Atlas、旧 batch 原始 artifacts、canonical protected history；旧错误结论只能追加 amendment、supersede 或 invalidate，不得删除历史。"
> "本轮不是只写计划。请连续推进到混合均衡路线得到一个有证据的 A/B/C/D 裁决，并完成交接。普通候选失败、参数失败、局部阻断不要停下来问用户。" → S011
- "不得直接继承 e15ae60 的以下结论：'五个机制轴已经穷尽'；'16QAM 内环坍塌是 OSL 信道本质属性'；'仅从接收统计量中不可能提取求逆信息'；'可直接写成完整负面边界论文'；'model-based tracker 是唯一剩余方向'。" → D017
- "不得为了'整理状态'重跑科学实验，也不要建立新的通用控制器。" ⟶推翻 e15ae60 的 H060 "信道属性" 全域宣称
- "失败标签必须有 receiver-visible 诊断定义和 scoring-only 评价定义，两者分开。不得再用单一 PI-SER > 0.3 代替全部失败机制。"
- "oracle 只作 Kill/headroom bound，不能作 Go comparator。"
- "如果简单阈值已经达到 ceiling，记录'ML 无必要'，不要为了 ML 而 ML。"
- "不要因为'没搜到'就声称新颖。"
- "寄了？咋办呢？你这边交接一下新对话。但之后呢？" → D019, H012

## 2026-07-22（S012 信息来源组合级 Probe）

> "本轮要回答：哪一种新增、合法、运行时可获得的信息，最可能打破当前盲均衡器的相关失败，并形成可写进毕业论文的正面方法？"
> "候选必须按'信息来源 × 作用点 × 输出动作'组织，不能按 EKF、GRU、Transformer 等模型名拆方向。"
> "先列全、归类、去重，再统一排序。不要先凭标题把某一候选排第一。"
> "本轮不是只写表。完成 Map 后，对四个信息族尽可能并行执行最轻量的前置 Probe。"
> "不能继续把 MDE=0.005 或 0.03 自动称为'通信可用'。"
> "若最强候选需要约一天或更大的新基础设施：不要直接开建；完成所有轻量 Probe 后统一向用户报告投资选择。" → D020
> "不要以代码量、测试数或文档数作为主要进展。先回答科学余量、物理价值和毕业价值。"

## 2026-07-22（S013 F1-A0 严格因果修复 Probe — 科学语义纠偏+修复）

> "你继续充当执行者。当前 HEAD=bf620b3，分支 codex/direction-lab-capability-atlas，未 push。本轮不是实现 F1-B tracker，也不是进入正式 Scout。本轮只做：1. 修正 S012/D020/V009/H013 中的科学语义；2. 执行一个不超过半天的 F1-A0 causal observability repair Probe；3. 给出是否值得再投资一天 tracker 的新证据。" → D021
> "不把现有 0.133 gap 继续称为 per-block MMSE 或纯 model-prior headroom；不把 |r|=0.65 称为 channel-state observability。" → D021
> "旧记录必须保留；用 superseded/corrected/partial 等状态形成血缘，不重写历史为'从未发生'。" → D021
> "不得使用 TX truth calibration。它是纯 CSI genie。"（对 E1）→ D021
> "141-150 已经被观察，禁止作为新的最终测试集。" → D021
> "truth 只允许作为离线 label 和评分依据，不得进入 inference input。"（对预测目标）→ D021
> "不得使用 EKF/PF/GRU/Transformer/NN。" → D021
> "资源决策阈值不能称为'通信可用阈值'。" → D021
> "如果 FAIL：不实现 tracker；将 F1-B 标为当前证据不足；下一建议改为 F2 collision check。" → D021
> "如果 PASS：仍然不要实现 tracker；只报告投资依据、预计基建和风险，等待主控授权。" → D021
> "先补会失败的测试，再修实现。" → D021
> "验证必须分两种角色：1. integrity verifier；2. scientific critic。两者都要形成独立、可定位的报告文件，不能只在 verifications.md 中写一句 agent 已检查。" → V010, V011
> "不再修改 campaign contract 中声明 protected 的 STATUS.v1.md；不静默修改 project.v1.yaml/STATUS 的 controller ownership 冲突，只记录并报告。" → D021 (gap #10/#11)
> "做一次确定性数字 grep，保证 artifact、synthesis、D、V、Handoff、current projection 数字一致；全轮一次 commit，不 push；最终返回 changed files、测试命令与结果、独立审查结论、commit SHA。" → S013 §收尾
