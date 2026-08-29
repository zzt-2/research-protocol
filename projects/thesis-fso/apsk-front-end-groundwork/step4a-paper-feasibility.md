# Q-C4-2 GW Step 4a 纸面可行性（A0/A′/A/B）

> T052｜2026-08-30｜formal step：GW Step 4a paper dimensions only
> 控制校验：`validate_task_control.py` = `PASS`（epoch 6 / CP006 / `GROUNDWORK_FEASIBILITY_PAPER`）
> 总裁决：`PAPER_DIMENSIONS_PASS`
> 边界：未进入维度 D，未计算 oracle/headroom，未给 Go/Conditional Go，未实现或运行实验。

## 0. Findings-first 结论

| 维度 | verdict | 纸面结论 | 尚未闭合的实证问题 |
|---|---|---|---|
| A0 | `PAPER_DIMENSIONS_PASS` | Q-C4-2 仍是合法 M–C–A 问题；receiver-visible reliability gate 是简单传统 DSP 规则，不需要 ML/MDP | tuned plain RDE/DD 后是否仍有可测 update-contamination 与 BER/FER headroom |
| A′ | `PAPER_DIMENSIONS_PASS` | BER/FER 是首要承重维度；收敛/失锁、错误更新率、pilot/update budget 与复杂度用于机制和工程边界 | 各维度的改善幅度、置信区间与 operating slice |
| A | `PAPER_DIMENSIONS_PASS` | 错环/错判样本会把 RDE/DD 递推推向错误目标；二值 gate 可证伪地改变 2×2 update 的样本集合 | oracle gate、receiver-visible gate 和最强廉价替代之间的实际差距 |
| B | `PAPER_DIMENSIONS_PASS` | bounded Step 3.5 未确认 exact collision；外部邻居只允许 target-scene extension claim，不证明性能 | Di Rosa–Richter 2021 全文缺失，action-level 独立性只能保守表述 |

这四个纸面维度无当前致命信号，但它们只授权主控考虑另行派发维度 D。`PAPER_DIMENSIONS_PASS` 不等于方法成立，也不更新正式 feasibility terminal。

## 1. 固定研究对象与证据边界

研究对象保持 T052 不变：

`有限 pilot 的 2×2 LS 初始化 + 已知 (8,8)-16APSK ring identity + payload receiver residual/decision distance`
`→ 对 RDE 型 2×2 均衡更新逐样本 reliability gate`
`→ semi-blind refined 2×2 demultiplexer`。

物理切片冻结为 memoryless、single-tap、unitary 2×2 Jones mixing 与 equal-branch white noise；这是当前平台 authority 的主动默认值。finite-FIR 只在 receiver filter 或 I/Q timing skew 有正式 authority 后开放，本候选 v1 不借该分支制造 headroom（`projects/thesis-fso/apsk-platform-groundwork/platform-parameter-authority.md:8,101-102,117,200-202`）。

证据只来自 T048/T050、本地三篇 read notes 与平台 authority。Di Rosa–Richter 2021、FEC-SoftRDE 和 MAPSK outer-ring CMA 仅按 T050 已保存的摘要级 ledger 使用；没有把摘要脑补成 LS 公式、butterfly 实现或具体权重。

## 2. A0：问题—方法适配性预检

### 2.1 §0 合法问题门：PASS

**Q#**：`Q-C4-2`。

| 元素 | 冻结定义 |
|---|---|
| M | 相同 pilot、相同 2×2 LS 初值、相同 payload/update/tuning budget 的 LS-only、tuned plain RDE 与 tuned DD-LMS/RLS |
| C | DP-(8,8)-16APSK；memoryless single-tap unitary Jones；有限 pilot；payload 端只使用 constellation/ring identity、当前 demux 输出、receiver residual/decision distance 与过去状态 |
| A | LS-only 不使用 payload；plain RDE 对所有样本执行最近环更新，错环样本会注入错误半径目标；DD-LMS/RLS 的错判样本会注入错误符号目标 |

四判据仍为 4/4：M/C/A 明确；产出是可部署的 gated-refinement 动作链；经典 task-matched baseline 可正确实现；BER/FER、收敛、错误更新、pilot/update budget 与复杂度均可量化。该判断来自 T048 的 Q-C4-2 表与 comparator 冻结（`projects/thesis-fso/literature_notes_apsk_front_end.md:93-100,113`），而不是来自“没有 exact collision”。

PS-QAM、DP-64QAM 或 MAPSK 与 `(8,8)-16APSK` 的场景差异只限制/界定 claim；场景差异本身不构成问题、贡献或性能证据。

### 2.2 §1 性能间隙：纸面 PASS，数值 UNKNOWN

- **[论证] LS-only residual**：有限 pilot 的 LS 初值不使用 payload，因此不能在 payload 上继续校正残余 2×2 demux 误差；但当前材料没有给出该残余的数值大小。
- **[论证] RDE/DD update contamination**：RDE 的最近半径硬分配依赖正确 ring assignment；Ready–Gooch 明确记录了错误初始增益/all-pass 初始化可不收敛，而其可信区域门属于载波环，不是均衡抽头 gate（`papers/_read_notes/10.1109_icassp.1990.115806.md:16,19,57`）。DD 则在低可靠判决下存在错误目标传播。
- **已知强基线**：coherent RDE/DD 可接近 RLS-CMA并优于基础 CMA，且 RDE/DD 约为线性复杂度；所以不能从基础 CMA 的弱表现外推出本候选有 headroom（`papers/_read_notes/10.1109_jlt.2009.2021961.md:19`）。

没有纸面数字可支持“≥5%”或任何 BER/FER 改善声称。本维度之所以通过，是因为存在明确、可测、可被 oracle 关闭的残余问题，而不是已经证明差距足够大。若后续 oracle/headroom 计划显示 tuned RDE/DD 后无可测差距，则在实现候选前 `KILL_BEFORE_MVE`。

### 2.3 §2–§4 方法类型适配：PASS（传统 DSP；ML/MDP 条款不适用）

候选不是 ML/DRL，也不建立 MDP。它只在现有 RDE 更新前增加一个确定性的 receiver-visible 二值门。因此：

- 不需要大状态空间、长期奖励、跨场景策略学习或神经网络；
- `S/A/R/P` 与“跨域 ML 成功先例”不作为本传统 DSP 候选的门；
- 采用硬 gate 而不是学习器，正是对“简单方法是否足够”的正面回答；
- smooth weight 仅是同族变体，除非硬 gate 的实证失败机制明确指向量化过粗，否则不进入 v1。

这不是跳过 A0，而是按方法类型执行：本候选的可行性风险集中在“可靠度分数能否识别有害更新”和“识别后是否改善端到端指标”。

### 2.4 §5 负面/邻居证据：PASS_WITH_CLAIM_CEILING

T050 的三轮 bounded closure 覆盖 328 archive rows、305 条去重记录，其中 2019+ 为 140 条 unique records；未确认五要素完全相同的 recipe，但找到三个必须正视的邻居：

1. Di Rosa–Richter 2021 已占用 pilot+payload assignment likelihood+selection-RDE+SOP tracking 主干，但当前只有摘要，且目标为 PS-QAM；
2. FEC-assisted RLS-SoftRDE 2025 已占用 decoder soft-ring reliability weighting+polarization demux 主干，但信息源为 decoder posterior、调制为 DP-64QAM；
3. MAPSK outer-ring CMA 2025 已占用 APSK ring selection 原子，但不是 residual/confidence gate，也未确认 2×2 demux。

证据指针：`projects/thesis-fso/apsk-front-end-groundwork/step3-5-supplement-report.md:17-37,48-60`。

因此外部 evidence 支持的只是“本 bounded slice 未确认 exact collision”；不支持首次、SOTA、通用 soft-ring update 或通用 semi-blind polarization tracking。

### 2.5 §6 先验覆盖与最强廉价替代：PASS_TO_MEASURE

**最强经典 comparator**：同 2×2 LS 初值、独立调优的 plain RDE。
**第二 comparator 族**：同初值、同预算的 DD-LMS 与 DD-RLS。
**最强廉价替代**：`native-RDE-residual hard gate`——只使用 RDE 已计算的最近环残差，以单阈值拒绝大残差更新，不使用额外 nearest-symbol decision distance。

廉价替代与 candidate v1 的区别只有“ring residual 单特征”对“ring residual + nearest-symbol distance 双证据”。若廉价替代吸收全部增益，方法身份应收缩为该更简单 gate，而不是为了复杂度保留双证据 recipe。若 tuned plain RDE、DD-LMS/RLS 和该廉价 gate 已使 receiver-visible gate 没有可测 headroom，才关闭本候选。

当前无法判断先验覆盖率；必须把上述廉价替代加入后续同预算比较，不能按想象 Kill，也不能从 `NOT_EXACT_COLLISION` 推出性能空间。

## 3. A′：竞争维度分解

| 竞争维度 | 承重级别 | 正确比较 | 方法预期增量 | 纸面风险 |
|---|---|---|---|---|
| post-demux BER / coded FER | **主承重** | paired seeds/cells；同 pilot、初值、payload window、tuning budget | 在错环/错判样本占比非零的 slice，减少污染后降低 BER/FER | tuned RDE/DD 可能已把 residual 压到不可测 |
| 收敛长度、失锁/发散率 | 次承重，可与 BER/FER联合 | 到固定 BER 门限的 symbols；失败率与 CI | gate 避免坏更新导致的回退或发散 | 过严 gate 也会减慢收敛 |
| accepted update 中的错误更新率 | **机制诊断，不单独承章** | oracle 离线标注 ring/decision correctness；部署方法不得读取 | 相对 plain RDE/DD 降低有害更新比例 | 代理改善可能不传导到 BER/FER |
| pilot budget / payload update budget | 工程次承重 | 同 pilot；同时报告 update-opportunity 与 actual accepted updates | 在有限 pilot 下利用可靠 payload，或以更少实际更新匹配性能 | 不能把“少更新”与“更好选择”混为一谈 |
| 复杂度/时延 | 解释或 B 级工程支撑 | 报告距离计算、比较器、更新次数和 wall-clock/caller-path成本 | hard gate 只加常数级距离/比较并可能省更新 | 单独的 proxy op count 不足以证明方法 |

承重顺序冻结为：`BER/FER > 收敛/失锁 > pilot/update budget > 复杂度`。错误更新率只解释机制。若只有错误更新率改善而 BER/FER、收敛和真实成本均无改善，不能形成方法结果；若 BER/FER 非劣但 pilot/update 或真实计算成本显著下降，可按 D044 的 B 级工程路线评估，但不能改写为 BER 优势。

## 4. A：结构优势、可证伪机制与 oracle/headroom 计划

### 4.1 Candidate recipe v1：双证据二值 reliability-gated RDE

1. **Pilot 初始化**：仅在固定 pilot prefix 上估计 unconstrained 2×2 LS demultiplexer `W0`；所有 comparator 复用完全相同的 `W0`。
2. **Payload 输出**：对每个 payload symbol 计算 `z_k = W_k y_k`。
3. **Receiver-visible 双证据**：对每个输出支路计算：
   - 到最近 `(8,8)-16APSK` constellation point 的归一化 decision distance；
   - 到该点所属已知 ring radius 的归一化 ring residual。
4. **硬门**：只有两项均低于冻结阈值时 `g_k=1`，否则 `g_k=0`。阈值只在 development split 上调优，eval 前冻结。
5. **2×2 更新**：复用 canonical RDE 的 ring-error update；唯一方法增量是将对应逐样本/逐支路梯度乘以 `g_k`。不增加学习器、decoder feedback、多阶段权重或 truth-based fallback。
6. **输出**：得到 payload-refined 2×2 demultiplexer及 `accepted_update_count`、两种 distance 的诊断日志；输出仍遵守 Ch4→Ch5 的 `z/G_eff/Sigma_n/flags/constellation_id` 接口。

### 4.2 可证伪机制

plain RDE 在 ring assignment 错误时把输出拉向错误半径；DD-LMS/RLS 在 symbol decision 错误时把抽头拉向错误 symbol。v1 的结构优势不是“APSK 不同”，而是用两个 receiver-visible 一致性证据拒绝更可能携带错误目标的更新，从而改变进入 2×2 recursion 的样本条件分布。

该机制可被以下任一事实推翻：

- harmful update 的条件概率不随两种 distance 增大；
- receiver-visible hard gate 与 oracle-correctness gate 的 accepted set 几乎无关；
- 减少错误更新后 BER/FER、收敛/失锁或真实成本均不改善；
- 改善完全由更少更新、额外 tuning 或更有利的初始化造成；
- ring-residual-only 廉价 gate 达到相同性能，双证据没有信息增量。

### 4.3 最小 oracle/headroom 计划（本轮不执行）

后续维度 D 若获授权，只需在 platform-authorized memoryless single-tap unitary Jones + equal-white-noise slice 上做 paired 最小计划：

1. 固定 `(8,8)-16APSK` mapping、pilot prefix、LS `W0`、payload realization 与 tuning budget；每次只改变一个 conditional axis。
2. 跑 `LS-only`、`plain RDE`、`DD-LMS`、`DD-RLS`、`native-RDE-residual hard gate`、`candidate v1`。
3. 增加一个**非部署 oracle gate**：仅当 payload 的 ring/symbol assignment 与发送真值一致时允许 canonical update。oracle 只估上界，不可进入候选输入。
4. 同时给两种公平口径：
   - 相同 payload update opportunities；
   - 与 v1 相同 actual accepted-update count 的 uniform-subsampled plain RDE，用于隔离“选择质量”与“少更新”。
5. 主看 paired BER/FER；辅看收敛/失锁、错误更新率、accepted updates 与真实运行成本。所有阈值/步长/forgetting factor 独立调优但共享 tuning-call budget。

最小计划只回答三问：问题是否存在；oracle rejection 是否有 headroom；receiver-visible gate 是否回收了可测比例的 oracle headroom。它不加入 filter/FIR、PMD、PDL 数值、联合 CFO/phase/IQ stress，也不把平台 correctness smoke 当方法结果。

## 5. B：新颖性—可行性解耦

### 5.1 新颖性事实

- bounded Step 3.5 未确认五要素 exact recipe collision，故 Q-C4-2 保持 `SURVIVES`；
- Di Rosa–Richter 2021 已显著占用 pilot/payload likelihood-selected RDE 主干；
- FEC-SoftRDE 已占用 soft-ring reliability-weighted polarization-demux 主干；
- MAPSK outer-ring CMA 已占用 APSK ring-selection 原子。

所以候选最多定位为：**receiver-distance reliability-gated RDE 在有限-pilot、LS-initialized DP-(8,8)-16APSK 2×2 receiver 上的 target-scene extension**。不得写“首次提出 pilot-aided RDE”“首次 reliability-gated equalizer”“首次 semi-blind polarization tracking”。

### 5.2 可行性预测

可行性来自可证伪的 update-contamination 机制、RDE/DD 已成熟的 2×2 update 载体以及 strong neighbors 对“选择/软信息可改变均衡更新”的机制先例。它不来自 exact-collision 缺失，也不来自 APSK 与 PS-QAM 的场景不同。

当前只能预测：当有限 pilot 留下可测 residual，且 plain RDE/DD 的错误目标更新非零时，receiver-visible gate 可能降低污染；是否传导到 BER/FER 必须由维度 D 回答。

### 5.3 空白零假设

| 空白可能原因 | 反驳/处理 | 当前状态 |
|---|---|---|
| exact recipe 实际已被 Di Rosa–Richter 2021 覆盖，只是全文不可用 | 其摘要明确为 PS-QAM，并未确认 pilot-only 2×2 LS、具体权重公式和 butterfly；因此不能判 exact collision，也不能声称独立 | **唯一 blocker** |
| tuned plain RDE/DD 或 native-residual gate 已足够，双证据无增量 | 强制把三者作为同预算 comparator/cheap alternative；若吸收则收缩 recipe 或关闭 | 待维度 D |
| memoryless unitary single-tap + LS 已把问题解决，payload refinement 没有 headroom | 先做 LS-only residual 与 oracle-correctness gate 上界；无 headroom 则实现前 Kill | 待维度 D |
| hard gate 拒绝过多有效更新，收敛变慢或低 SNR 全拒绝 | 同时报告 acceptance、收敛和 BER/FER；只有分数有排序信息但二值化过粗时才 Pivot 到 smooth weight | 待维度 D |

没有一个零假设能仅靠现有纸面证据直接判死候选；但前三项均能在最小 headroom 计划中被明确裁决。

## 6. Step 4a-D 前冻结合同

### 6.1 Fair comparator

- `LS-only`；
- 同 `W0` 的 independently tuned plain RDE（主 comparator）；
- 同 `W0`、同预算的 DD-LMS 与 DD-RLS；
- native-RDE-residual single-threshold hard gate（最强廉价替代）；
- CMA/MMA 只作 canonical reference，不得成为唯一主 baseline。

共享：pilot symbols、LS implementation、payload realization、Jones/noise realization、最大 update opportunities、tuning-call budget、seed/cell set 与 evaluation pipeline。各算法允许独立调步长/forgetting factor/threshold，但不得给 candidate 更多 tuning calls。

### 6.2 Receiver-visible firewall

候选运行时允许：pilot positions/symbols（只用于 `W0`）、当前/历史接收样本、当前 `Wk`、demux 输出、固定 constellation/ring identity、nearest-point/ring distances、过去 accepted-update 状态。

候选运行时禁止：true Jones matrix、clean payload symbols、truth SNR/noise realization、oracle ring/symbol correctness、eval BER/FER、decoder posterior/LLR、未来样本或 whole-eval-window statistics。oracle truth 只能离线计算 headroom，必须与 deployable result 分栏报告。

### 6.3 最小消融

1. plain RDE；
2. ring-residual-only hard gate；
3. decision-distance-only hard gate；
4. v1 双证据 hard gate；
5. oracle-correctness gate（upper bound，非部署）；
6. v1 与 update-count-matched uniform-subsampled RDE。

smooth weight 不属于首轮最小消融。只有 hard gate 显示可靠度排序有效、但阈值量化导致明显拒绝/收敛折衷时，才作为同族 Pivot。

### 6.4 预期方向

- 错误更新率：oracle gate 最低；v1 应低于 plain RDE/DD，且不高于单特征 gate；
- BER/FER：在问题-bearing slice 上，v1 应优于 tuned plain RDE/DD；若只与 CMA 比较则不构成通过；
- 收敛：v1 可减少回退/发散，但过严阈值可能增加达到目标 BER 的 symbols；
- budget/complexity：v1 接受更新数应不高于 plain RDE，额外计算限于两种距离和比较；不得只用 proxy op count 声称真实时延收益。

这些都是待检验方向，不是结果数字。

### 6.5 Pre-MVE Kill / Pivot 条件

**`KILL_BEFORE_MVE`**（任一成立）：

1. LS-only 在目标 slice 已无可测 residual，oracle-correctness gate 对 tuned RDE/DD 的 BER/FER、收敛/失锁和真实成本均无 headroom；
2. receiver-visible distance 对 harmful update 没有可重复的判别信息，v1 不能回收任何 oracle headroom；
3. 所有改善在 update-count-matched comparator 下消失，证明收益只来自少更新；
4. 候选必须读取 truth/decoder feedback/未来 eval statistics 才能工作；
5. Di Rosa–Richter 全文确认五要素 exact recipe collision，且目标场景没有可陈述的真实适配 delta。

**`PIVOT`**（有明确可修复方向）：

1. ring-residual-only gate 吸收双证据增益 → 收缩为更简单的 native-residual gate recipe；
2. 双证据有排序信息但 hard threshold 拒绝过多 → 同族 Pivot 为单调 smooth weight；
3. 只有某一 receiver-visible 分数有信息增量 → 删除无效分数并冻结单特征 recipe；
4. candidate 只在 receiver-local finite-FIR/filter 分支有 headroom → 暂停并等待正式 filter/FIR authority，不借 UNKNOWN 参数推进。

## 7. 唯一 blocker

**`FULLTEXT_UNAVAILABLE_DI_ROSA_2021`**。

Di Rosa–Richter 2021 是最强 action-level 邻居，但当前 worktree 只有摘要证据；其 pilot initialization、逐样本选择/权重公式和明确 2×2 butterfly 实现均未核。该缺口限制独立性与 claim ceiling，不阻止在 memoryless single-tap slice 上设计/比较 v1；若后续全文证明五要素完全相同，则按 §6.5 重新裁决。

平台 receiver filter/FIR authority 缺口不是本 candidate v1 的 blocker，因为 v1 明确冻结在 single-tap memoryless 默认模型；它只阻止未来把 filter/timing-skew finite-FIR 分支纳入 correctness 已验证或方法 claim。

## 8. 最终裁决

`A0=PAPER_DIMENSIONS_PASS / A′=PAPER_DIMENSIONS_PASS / A=PAPER_DIMENSIONS_PASS / B=PAPER_DIMENSIONS_PASS`。

总体为 `PAPER_DIMENSIONS_PASS`。下一合法科学动作只能由主控另行授权维度 D；在此之前不得把本报告表述为 Go、方法信号、实验通过或可开始写正式论文正文。
