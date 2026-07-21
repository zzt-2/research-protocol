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
