# Decision Records — Direction Lab 首轮 SCIENCE_SCOUT 正式科学探索

## D001: 选择 CB1 modulation-generic closure 作为首轮共享能力

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据: 调研: `campaigns/science-scout-2026-07-20/portfolio-refresh.v1.yaml` + `campaigns/science-scout-2026-07-20/capability-leverage-atlas.v1.yaml` + 子 agent A/B/C 三方审计（文献/代码/候选） + 用户原话: `voice.md` 2026-07-20 "如果首选共享能力不成立，自动回到 Portfolio 选择下一项；不要在每个小步骤等待用户确认"

### 决策

首轮 SCIENCE_SCOUT campaign 选择 **CB1 modulation-generic closure**（QPSK + 16QAM hash-bound source closure）作为第一个共享能力建设对象。建设完成后运行 baseline-only Atlas（pre-registered MDE 0.005），仅在发现 >MDE headroom 时触发一批 ML Scout；如无 headroom 则记录 LOCAL_NEGATIVE extension 并按 Portfolio priority 自动轮换到下一个候选（U24 或 RC2 cluster）。

### 理由

CB1 在三个独立判据上胜出，不依赖固定打分器（用户 §六）：

1. **实现成本最低**：所有原语已存在（`_modulation.py:24/39/84` 的 qam16_mod/demod/hard_decision 调制感知；`_cma.py:43` cma_radius 从任意星座计算 R²；`_cma.py:74` CMAEqualizer2x2 已参数化 R²；`_gg_time.py` 调制无关）。仅需参数化 `_dual_pol_channel.py:48-55` 的 8 行 symbol-gen + 替换 `stage_a_cell_runner.py:228` 的 QPSK 硬编码 demapper + 重新 pin closure。成本 MEDIUM_half_day，其余 4 个 bundle 均 HIGH_multi_day。
2. **处置最多历史 UNRESOLVED 反例**：D008-D014/D023 的 modulation-driven ordering signals 反例恰好在 modulation 轴上（P03 v1 closure 硬编码 QPSK 使该轴 INFRASTRUCTURE_BLOCKED）。CB1 直接解锁 modulation 轴，是单 bundle 中能处置最多历史 UNRESOLVED 反例的。
3. **最强机制先验可能找到新 headroom**：`explore/cma-fade-divergence/ber_16qam_vs_fg.py:19-23`（D008 Sup-1）显示 16QAM 的 CMA BER 高于 QPSK（modulus mismatch 结构性缺陷），暗示 16QAM 域可能比 P03 找到零 headroom 的 QPSK 域有 MORE headroom。即使失败，LOCAL_NEGATIVE on 16QAM 扩展 P03 边界到第二个 modulation，仍是可毕业的论文结果（边界映射）。

### 排除的替代方案

- **不先建 CB2 soft/coded evaluator**：虽然 paper-main-line 价值 5 最高，但 blocked on CB1（modulation）和 CB3（CSI contract）。须 CB1 → CB3 → CB2 顺序。
- **不先建 CB3 receiver CSI/pilot seam**：第二杠杆但 HIGH 成本（dual-pol 估计推导，现有代码全 single-pol 有静默降级风险）。CB1 成功后再建。
- **不先建 CB4 carrier + dual-pol CPR**：HIGH 成本 + HIGH 风险（SOP theta ≠ carrier phase，foundation-audit:25 警告）。P02 NOT_RUNNABLE。
- **不先建 CB5 receiver snapshot + action replay**：P01 BLOCKED（STATE_SNAPSHOT_MISSING, ACTION_EFFECT_NOT_OBSERVABLE）。最大成本。

### 影响范围

仅在本 campaign worktree（`.worktrees/direction-lab-capability-atlas`）内：
- 参数化 `_dual_pol_channel.py`、`stage_a_cell_runner.py`、`probe_evaluator.py`（新增 modulation 调度，QPSK 路径字节不变）；
- 新建 `scout/cb1-modulation-generic-closure/` 目录承载新 closure 和 baseline Atlas；
- 不修改 canonical-state / portfolio/current.v1 / STATUS.v1 / B001-B003 / P03 Atlas（protected history）；
- 不自动晋级任何结果到 formal Groundwork/Contract/Execute/论文。

### 来源

S001 + 子 agent A/B/C 三方审计 + 用户 §五/§六/§九 执行提示词

---

## D002: 授权状态迁移 READ_ONLY_MIGRATION_PREVIEW → SCIENCE_SCOUT（additive overlay）

> status: active
> date: 2026-07-20
> 取代：无（叠加在 V007-DEPLOYED protected history 之上，不取代）
> 被取代：无
> 依据: 用户原话: `voice.md` 2026-07-20 "你现在获得明确授权，启动 Research Direction Lab 的第一轮正式 SCIENCE_SCOUT campaign" + "将项目模式从 READ_ONLY_MIGRATION_PREVIEW 迁移为本轮限定的 SCIENCE_SCOUT" + 调研: `canonical-state.yaml` + `portfolio/current.v1.yaml`

### 决策

在本轮 campaign 内叠加 SCIENCE_SCOUT 授权模式，**不解除 formal BLOCKED 状态**。迁移通过新建 `campaigns/science-scout-2026-07-20/campaign-contract.v1.yaml` 和 `authorization-projection.v1.yaml` 实现，不回写 `canonical-state.yaml` / `portfolio/current.v1.yaml` / `STATUS.v1.md`。formal Groundwork/Contract/Execute/论文晋级继续阻断。

### 理由

用户明确授权本轮 SCIENCE_SCOUT，但同时明确不含"绕过 Groundwork/Contract/Execute 完成正式晋级"。叠加式迁移既允许 sandbox/Scout 科学工作，又保留 protected history 字节不变，且 stale-debt（`_dual_pol_channel.py` 行尾 SHA 差异、raw artifacts 缺失）在新 projection 显式登记，不假装 self-contained。

### 排除的替代方案

- **不原地改写 canonical-state**：违反 anchor.yaml `canonical_baseline.mutable=false` 和 governance-pilot 不变量。
- **不解除 formal BLOCKED**：用户明确不含"绕过 GW/Contract/Execute 完成正式晋级"。
- **不删除旧 projection**：保留可审计的历史血缘。

### 影响范围

仅本 campaign worktree。新 projection 引用 protected history hashes，不回写。

### 来源

S001 + 用户 §一/§四 执行提示词

---

## D003: 16QAM R²=1.32 和 Gray map provenance 须在实现前补源

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
> 依据: 调研: 子 agent A 文献审计（"16QAM Gray mapping + normalization: only _modulation.py comment, no textbook/paper citation. Closable with targeted sub-search"）+ 用户 §七 "任何 baseline、信道、估计器、指标、仿真参数或新方法进入实现前，必须建立 formula-symbol-parameter-provenance.yaml" + FR-20 (MVE 关键参数溯源) + FR-26 (证据链强制)

### 决策

CB1 实现前必须完成 provenance 硬门：
- **16QAM Gray mapping** + **average-power normalization /sqrt(10)**：标 `DEFINED_HERE` 或补 textbook 来源（Proakis/Sklar）；
- **R²_16QAM = 1.32**：必须交叉验证 analytical E[|s|⁴]/E[|s|²] for the Gray map，并尝试找 Mammasis 2012 / Yang 2002 CMMA 等独立来源；
- **PI-SER (permutation-invariant SER)**：lab-coined，标 `DEFINED_HERE` + 尝试找 BSS permutation-invariance 文献先例；
- **standard-CMA Godard cost**：已有 Godard 1980 + sat.1553 §6 双源，pass；
- **Gamma-Gamma / SOP / Jones**：已有 Andrews+Greenwood+Conan + sat.1553 §6.3 来源，但 sat.1553 在本 worktree 缺失，须重新获取或跨 worktree 引用。

### 理由

用户 §七 硬门：公式/符号/参数进入实现前必须建立 provenance。子 agent A 审计发现 16QAM 关键公式/参数（Gray map、R²=1.32）无任何外部来源，PI-SER 无先例。这些是 CB1 实现的核心，不能"为了让 ML 有用"拍参数（FR-20）。补源是 bounded shared repair，不阻断 campaign。

### 排除的替代方案

- **不跳过 provenance 直接实现**：违反用户 §七 + FR-20 + FR-26。
- **不用 web search 摘要充当公式证据**：用户 §八 "不把搜索摘要当成公式证据"，须 textbook/paper 正文精确出处。
- **不为加速而接受单源**：baseline 关键公式最好有原始/权威来源 + 独立实现 + 数值验证（§七 D）。

### 影响范围

CB1 实现前补源。若关键公式/参数无可靠来源：对应能力包不进入 Sandbox，可轮转到资料充分的候选（用户 §八）。

### 来源

S001 + 子 agent A + 用户 §七/§八

---

## D004: 本轮不触发 ML Scout；记录 scoped positive + harvest + handoff

> status: superseded
> date: 2026-07-20
> 取代：无
> 被取代：D005
> 依据: 验证: 独立 verifier CONFIRM (clean-room, canonical prompt013 only) + 调研: CB1 baseline Atlas artifacts + 用户原话: `voice.md` 2026-07-20 "如果首选共享能力不成立，自动回到 Portfolio 选择下一项；不要在每个小步骤等待用户确认" + profile.md "警惕主线急于给方向性结论"

### 决策

本轮 SCIENCE_SCOUT campaign 在 CB1 baseline Atlas 发现 16QAM headroom（10/11 cells ≥ MDE，max 0.333）后，**不立即触发 ML Scout batch**。改为记录 scoped positive（H010-H015）并 handoff 到新对话触发 ML Scout。

### 理由

1. **上下文预算**：本轮已完成 state recovery + 3 资产盘点子 agent + provenance + closure 实施 + baseline Atlas + 独立验证。ML Scout batch 是独立设计任务，应在 clean-context 对话做。
2. **科学严谨**：headroom 真实且独立验证 CONFIRM，但 "ML 能否在合法 comparator 下利用 headroom" 是独立问题。本轮结论是 "headroom found; ML Scout authorized but not yet run"，不是 "ML 会赢"。profile.md "警惕主线急于给方向性结论"（过早 Go 与过早 Kill 同病）。
3. **机制针对性强**：16QAM headroom 由 standard-CMA inner-ring collapse 驱动（~50% seeds at SNR≥15）。ML Scout 应针对 collapse 设计（causal CMA-state features + 学习型 re-init），不是 generic modeling。设计工作需 clean context。
4. **务实可毕业**：本轮已产出 defensible thesis result（16QAM boundary mapping + headroom finding + 失败机制诊断 + 可复用 closure 资产）。ML Scout 是增量贡献，不是毕业前提。

这不违反用户 "不要在每个小步骤等待用户确认" —— 本轮在授权内连续推进到 baseline Atlas + 独立验证 + harvest。handoff 是 campaign 自然 checkpoint，不是停下问用户。下一对话的 ML Scout 仍在 campaign-contract.v1.yaml 的 allowed_actions 内，不需要用户重新授权。

### 排除的替代方案

- **不立即在同一对话触发 ML Scout**：上下文已重；ML 设计应 clean；避免 "急于推进"（profile.md S024/S027）。
- **不宣称 "ML 会赢"**：headroom ≠ ML 获胜。oracle affine 是 Kill tool（FR-21），不是 Go baseline（FR-25）。ML 必须在 nearest-16QAM 这个 Go baseline 上赢才算贡献。
- **不把 H010-H015 自动晋级 thesis main ledger**：promotion requires user strategy decision。

### 影响范围

- 仅记录决策和 harvest；不修改 protected history。
- handoff H001 指定下一对话任务（ML Scout 设计要点）。
- 本轮收尾做单次 consolidated commit，不 push。

### 来源

S002 + 独立 verifier CONFIRM + profile.md

## D005: CB1 降为诊断信号，先做轻量传统 baseline 裁决

> status: active
> date: 2026-07-20
> 取代：D004 中“headroom 已授权下一对话直接进入 ML Scout”的部分
> 被取代：无
> 依据：用户原话: 本专题 `voice.md` 2026-07-20 + critic: S002 续接 baseline 审计 + 验证: `.agents/skills/research-direction-lab/tests/forward/runs/pragmatic-baseline-adjudication/round-red.md` 与 `round-green.md`

### 决策

CB1 的 16QAM 结果只保留为 `DIAGNOSTIC/SLICE`：在验证公平收敛并用一个来源闭环、广泛采用、任务适配的传统 comparator 重新裁决前，不授权 ML 训练。裁决与其他机制候选准备并行推进，不把当前单点变成新的完整流程瓶颈。

### 理由

原结果证明的是单模 Godard-with-z 在当前长度下存在 inner-ring collapse 和 scoring-only oracle gap，但未排除约 `1e5` symbols 收敛尺度、MMA/RDE 这类 16QAM 任务适配方法。实现正确不等于 baseline 足以支撑“需要 ML”。同时，用户明确要求 baseline 说得过去即可，不追当前最好，因此下一批只选一个主传统 comparator，并最多补一个直接处理当前失效的廉价扩展；不做论文级 SOTA 堆叠。

### 排除的替代方案

- **直接执行 H001 的 ML Scout**：否决；会把任务失配或欠收敛制造的 gap 当研究问题。
- **一次实现并穷举所有 MMA/RDE/DD/SOTA 变体**：否决；超出有限主张所需证据，违背务实停止条件。
- **抹去 CB1 正结果和 harvest**：否决；closure、R²、PI-SER evaluator、inner-ring collapse 和 baseline 选择教训仍是有效次级材料。
- **裁决期间暂停整个 Portfolio**：否决；其他共享契约候选可继续准备和排序。

### 影响范围

H001 标记为被取代；新增 H002 作为续接入口。CB1 raw artifacts、历史 harvest 和 protected history 不修改。下一对话先做 baseline 来源/实现/收敛合同与共享批次，再由 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 决定是否运行 ML。

### 来源

S002 续接 / 用户纠正 / Skill D010。

---

## D006: CB1 16QAM inner-ring collapse 裁决为 PROBLEM_SURVIVES_CONVENTIONAL_BASELINE；条件授权 ML Scout

> status: superseded
> date: 2026-07-20
> 取代：D005 中"裁决达到 PROBLEM_SURVIVES_CONVENTIONAL_BASELINE 后才允许 bounded ML Scout"的条件触发部分（现在已满足，授权生效）
> 被取代：D007
> 依据: 验证: `baseline-adjudication-batch/artifacts/baseline-adjudication-v1.json` + `baseline-adjudication-v1-synthesis.md` + 子 agent clean-room verifier（`verifier_mma.py`，bit-identical 复现）+ 用户原话: `voice.md` 2026-07-20 "在边界内尽可能连续推进到一次真正的 baseline 科学裁决"

### 决策

CB1 16QAM inner-ring collapse headroom 经一个广泛采用、任务适配、来源闭环的传统主 comparator（MMA, Yang-Werner-Dumont JSAC 2002）和一个 ~1e5 收敛长度（N=32768）联合裁决后，**仍然稳定存在**。裁决结论 = `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE`。

具体：
1. MMA 在 8/11 short cells (N=512) 上跟 CMA 统计无差异（|Δ PI-SER| < MDE）；在 3/11 long cells (N=8192) 上反而**比 CMA 更差**且 1/10 seeds diverge。
2. N=32768 不仅未消除 CMA headroom，反而 3/4 cells **headroom 增大**（length-invariant collapse rate ≈ 40-60%）。
3. 因此**条件 (a) task-mismatch** 和**条件 (b) under-convergence** 都被排除；headroom 是稳定的、机制相关的残余。

依 H002 / baseline-adjudication 参考，这**条件性授权**（不强制）一个 bounded ML Scout batch 针对 collapse 机制，但：
- ML 的 Go 对手必须是 nearest-16QAM **和** MMA（FR-25）；oracle affine 仍仅 Kill（FR-21）。
- claim ceiling 仍为 SLICE；DOMAIN 仍需关闭其他 blocked axes。
- Portfolio 同时准备 4 个机制不同候选 C01-C04（portfolio-refresh.v2-addendum.yaml）。

### 理由

裁决严格遵守 batch-contract.v1.yaml 的预注册决策规则：
- 条件 (1) MMA headroom ≥ MDE on ≥ 2 atlas-v1 cells → 10/11 PASS
- 条件 (2) N=32768 CMA headroom ≥ MDE on ≥ 1 cell → 4/4 PASS
- 合取 → PROBLEM_SURVIVES_CONVENTIONAL_BASELINE

来源核验：
- MMA 公式（Eq.12-13）+ dual-pol 扩展（Kikuchi JLT 2016 §IV.B）+ R_R²=R_I²=0.82 推导：3 篇独立复现 + 数值验证。
- 5/5 sanity tests PASS（identity gate / R_R² / clean QPSK / clean 16QAM / CMA anchor byte regression）。
- 独立 verifier 子 agent clean-room MMA 实现与主线 bit-identical；w_norm 飙升是合法 thermal divergence（μ∈(5e-4, 1e-3) 稳定性边界）非 bug。

机制判读（重要 nuance）：
- headroom 不能简单归因 task-mismatch（MMA 没更好甚至更差）。
- 不能简单归因 under-convergence（N=32768 反而更糟）。
- 真因：block-end gradient descent (block_size=64) 在 SOP-rotation + GG-fading 下存在稳定的 seed-and-trajectory-dependent 收敛失败，~40-60% seeds 坍缩到内环，与 N 无关。
- 信息可恢复性：oracle affine 能恢复坍缩 seeds 到 PI-SER≈0，说明恢复信息在 z-stream 中，只是 CMA/MMA trajectory 拿不到。这给 ML collapse detector 留下机制合理性。

### 排除的替代方案

- **不直接进 ML training**：D005 要求先裁决，本轮裁决 = PROBLEM_SURVIVES；授权生效但不在本对话训练 ML（上下文预算 + 需 clean-context 设计）。
- **不追 RLS / FD-MMA / DD-LMS cascade / neural equalizer 等 SOTA**：用户 §三 "baseline 不必是当前 SOTA"；MMA 已是任务适配广泛采用主 comparator，headroom 在其下仍存活就足够。
- **不抹除 H010-H015 正面 harvest**：CB1 closure / R²=1.32 / PI-SER evaluator / inner-ring collapse 诊断 / baseline 选择教训仍是有效次级材料。
- **不外推整个 16QAM 或通信领域**：claim ceiling 严格限 SLICE；DOMAIN 仍 UNRESOLVED。

### 影响范围

- 下一对话（clean context）：设计 bounded ML Scout batch（候选 C01-C04 任选，C01 为首选直接机制匹配）；shared input contract = causal CMA-trace features；dual Go comparator = nearest-16QAM + MMA。
- 本轮 harvest H016-H022 追加到 harvest-addendum.v1.yaml；provenance 追加 F-MMA-COST / F-MMA-R2-16QAM + 符号 + 参数。
- topic-index 不变量段无变更；H021 新增基础设施债务（block-end protocol 是 collapse 瓶颈但不能动 CMA anchor identity）。
- protected history（B001-B003 / P03 / CB1 raw）字节未改。

### 来源

S003（本轮 baseline adjudication shared batch）+ 子 agent verifier + 用户 §三/§五/§六/§七

---

## D007: baseline 公平性未闭合；先扩机制全貌并做有界公平修复

> status: active
> date: 2026-07-21
> 取代：D006 的 `PROBLEM_SURVIVES_CONVENTIONAL_BASELINE` 晋级、统一 Go comparator 与“首选 C01 直接训练”下一动作
> 被取代：无
> 依据: 用户原话: `voice.md` 2026-07-21 + critic: D006/S003 独立复审 + Skill: `2026-07-20-research-direction-lab-system/D011`

### 决策

D006 的原始 CMA/MMA 数值、实现资产和局部失败观察继续有效，但 baseline 公平性与机制因果尚未闭合，科学状态退回 `DIAGNOSTIC/SLICE`。下一对话先做短时机制级 Portfolio 扩图、readiness 纠正和有界公平修复；随后立即运行共享合同下的首个 `READY` 批次，不直接只训 C01。

### 理由

1. CMA/MMA 强制同一 `mu=0.001` 不等于算法各自获得公平调参机会；`mu=1e-4` 仅在一个 cell × 5 seeds 探测，不能代表候选专属 tuning closure。
2. `N=32768` 是预算内最大长度，不等于文献提到的约 `1e5` 收敛尺度，不能宣称欠收敛已经排除。
3. 未运行 smaller-block 或 per-symbol 更新，不能把 block-end protocol 写成已证明真因。
4. oracle affine 使用 TX truth，只证明特权映射存在，不证明 receiver-visible trace 足够识别该映射。
5. C01–C04 分属检测、控制、修正，不能用完全相同的 comparator 列表；C03 又缺 state/action hook，`Y_with_compute` readiness 不成立。
6. 四个候选仍集中在同一 collapse/trace 簇，直接只跑 C01 会重新单点收窄；但穷举或实现十几个候选同样过重。

### 排除的替代方案

- **维持 D006 并直接训练 C01**：拒绝；会在 baseline 公平性和候选全貌未闭合时过早推进。
- **删除 D006 数值或 harvest**：拒绝；原始数据、MMA 实现和局部失败仍是有效诊断与次级论文材料。
- **追逐所有 SOTA 或穷举传统均衡器**：拒绝；只做能改变有限主张的公平调参、收敛和直接机制核验。
- **先实现整个扩展 Portfolio**：拒绝；扩图只做候选全貌、证据和 readiness，随后立即批跑 `READY` 子集。

### 影响范围

H003 被 H004 取代为续接入口。下一轮允许更新 Portfolio、candidate-specific comparator/readiness、共享公平性合同并运行 Scout；继续禁止修改 B001–B003/P03/CB1 历史字节、创建 legacy B004、自动写论文或绕过 GW/Contract/Execute 晋级。

### 来源

S004 / 用户纠正 / system D011 / 独立方法论与候选血缘审计。

---

## D008: B01 完成 PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT；条件授权 B02 ML detector batch

> status: superseded
> date: 2026-07-21
> 取代：D007 中"先做有界公平修复后立即批跑 READY 子集"的执行部分（现已完成；下一动作变为 B02）
> 被取代：D009
> 依据: 用户原话: `voice.md` 2026-07-21 "整个对话最多做一次 consolidated commit" + "只要存在合法可运行路径，就继续推进" + 验证: `fairness-batch-b01/artifacts/fairness-batch-b01-v1.json` + `fairness-batch-b01-v1-synthesis.md` + 独立 verifier subagent (CONFIRM, HIGH confidence, 20/20 PASS) + Skill: `baseline-adjudication.md` + `batch-and-atlas.md`

### 决策

Fairness Batch B01（{C05, C08, C10, C11}，11 cells × 10 paired seeds，per-method tuning budget with divergence penalty）证实 CB1 16QAM 内环坍塌 headroom 在公平调参、per-symbol 结构变化和 CMA+DD-LMS 级联下**仍然存活**：

1. held-out 7 cells 上 anchor/C08/C10/C11 各只关闭 1/7（snr=5 AWGN floor）
2. C11（最佳变体）在 long cells 改善 0.01-0.03 PI-SER（snr10-fg100-long headroom 0.055→0.023）但远未关闭（≥6×MDE）
3. C10 per-symbol 略差于 anchor → **H021 基础设施缺口假设不被支持**
4. C05 detector pooled AUROC=0.6546 ∈ [0.65, 0.85) → **条件授权 B02 ML detector batch，narrowed claim "ML improves lead time / calibration over conventional threshold"**

D007 公平性债务 #1/#3/#5/#6 已 CLOSED，#2/#4 PARTIALLY CLOSED。

### 理由

1. 公平性已用 per-method tuning budget（4 validation cells × 5 seeds × 5 hyperparameter candidates + divergence penalty）严格保证；independent verifier 确认 tuning 在 held-out evaluation 前冻结。
2. 所有 4 个候选（含结构变体 C10 和级联 C11）都未能关闭坍塌，且 C10 直接否定了 H021 的 block-end 瓶颈假设——坍塌是 Godard cost 在该信道下的深层属性，不是协议 artifact。
3. C05 detector 的条件依赖性（long cells AUROC=1.000，short cells AUROC=0.5）说明：信号在长序列上可被传统阈值完美检测，但在短序列上需要 learned temporal model。这正是 ML 的合法贡献区域。
4. claim ceiling 严格限 SLICE；oracle 仍仅 Kill tool（FR-21）；detection AUROC 不等同于 PI-SER 改善（C05 不与 C08/C10/C11 混淆）。

### 排除的替代方案

- **直接训练 ML 检测器跳过 B01**：拒绝；会跳过 D007 要求的公平性收口。
- **关闭 B01 后宣布 ML 无价值**：拒绝；C05 detector AUROC=1.000 在可分 cells 说明信号存在，pooled 0.6546 在 [0.65, 0.85) 授权 narrowed-claim B02。
- **穷举所有传统均衡器（RLS/FD/neural）**：拒绝；用户 §三"baseline 不必是当前 SOTA"；当前有限主张的公平 comparator 已充分。
- **把 C11 的 long-cell 小改善写成 PI-SER 胜利**：拒绝；改善 0.01-0.03 远未关闭 headroom，且只在 3/11 cells 上。
- **把 B01 数字写入论文正文**：拒绝；Scout/Sandbox，晋级需用户 strategy 决策。

### 影响范围

- H004 的 A/B/C 三宏阶段全部完成；H005 成为下一轮续接入口。
- D007 公平性债务闭合；下一动作 = B02 ML detector batch（C01/C02/C06 + causal feature stacker adapter sprint）。
- harvest-addendum.v2-b01.yaml 追加 H023-H028；provenance 沿用 v1。
- topic-index 不变量段无变更；C10/C11/C05 进入 Portfolio READY/baseline 库。
- protected history（B001-B003 / P03 / CB1 raw / canonical-state）字节未改；无 B004；无 ML 训练。

### 来源

S005 / 公平 batch 科学运行 / 独立 verifier CONFIRM / baseline-adjudication + batch-and-atlas 参考。

---

## D009: B01-R 纠偏 — VERDICT B（fairness survives, detector target NOT ready）；撤回 B02 ML detector 授权

> status: amended
> date: 2026-07-21
> 取代：D008 的 `PROBLEM_SURVIVES_FAIR_CONVENTIONAL_TREATMENT → AUTHORIZE_B02_ML_DETECTOR_BATCH_CONDITIONAL` 推论链（verdict 的 fairness-survival 部分被更高保真路径 CONFIRM；B02 detector 授权被 WITHDRAW；C11 "long cells" claim 收紧到 4/7 held-out；C05 pooled AUROC=0.6546 被每 cell AUROC + 严格 4-cat 标签审计取代）
> 被取代：无
> 依据: 用户原话: `voice.md` 2026-07-21 "本轮不是继续 B02，也不是扩展候选池，而是完成一次有界的 B01-R 科学纠偏批" + "请连续推进到能够重新裁决"B02 是否 READY"为止" + "按上述 A/B/C 自动收口" + 验证: `fairness-batch-b01r/artifacts/fairness-batch-b01r-v1.json` + `fairness-batch-b01r-v1-synthesis.md` + `b01-audit-reproduction.md`（10/10 audit findings 复现）+ 独立 verifier subagent (CONFIRM, 11/11 checks PASS) + Skill: `baseline-adjudication.md` + `evidence-and-claims.md`

### 决策

B01-R 科学纠偏批（在隔离 worktree 中，不修改 B01 原始 raw / D008 / H005，新增独立合同 + runner + detector + 4 类标签审计）证实：

1. **B01 的 10 条审计发现全部独立复现**（见 `b01-audit-reproduction.md`）。
2. **公平性存活（强证据）**：在无泄漏 seed 切分（tuning=[11-15], test=[21-30]）+ 真实 validation-optimal fixed-μ CMA（μ=0.01，B01 从未运行的 comparator）下，CB1 16QAM inner-ring collapse headroom 仍在 6/7 held-out cells 上 ≥ MDE。最佳方法 fixed_μ CMA 只关闭 1/7（snr05-short，AWGN floor）。Paired bootstrap CI 显示 fixed_μ CMA 在 7/7 held-out cells 显著优于 frozen-μ anchor；C11 在 4/7 cells 显著改善（|Δ|≤0.026，headroom 仍 ≥6×MDE）；C10 与 anchor 无显著差异（confirm B01 H021 否定）；C08 混合（2 长 cell 微改善 + 1 短 cell 微退化）。
3. **detector target NOT READY**：4 类标签审计（inner_ring_recoverable / awgn_dominated / healthy / ambiguous）显示 B01 的 `oracle_pi_ser > 0.3` binary label 把 AWGN-dominated 错误（oracle 不能恢复）误当 collapse。严格 inner-ring 标签后只有 14/110 seeds（12.7%）是 true positive；**held-out 长窗 cells 的 inner-ring 数 = 0**。Only 2 held-out cells two-class（snr25-short / snr20-fg100-short）；C05 default-grid AUROC=0.875 / 0.75，lead_time=2 blocks，但样本太少不能支撑 B02 ML detector target。
4. **VERDICT B**（`B_B01R_FAIRNESS_SURVIVES_BUT_DETECTOR_TARGET_NOT_READY`）：fairness 存活；detector target 不 ready；**B02 ML detector batch NOT authorized**。

### 理由

1. 严格公平性 + 真实 comparator + 无泄漏切分 + paired CI 是 B01 缺失的科学保真度；补齐后 fairness-survival 部分被 CONFIRM（更可信）。
2. 4-cat 标签审计是核心纠偏：把"看起来像 collapse 的 AWGN 错误"分开后，B02 监督 detector 的合法目标群体太小且不在 held-out 长窗。强行授权 B02 会重蹈 B01 的 label-conflation 覆辙。
3. C11 的长窗改善是真实的（paired CI 显著），但**不是** inner-ring collapse 上的改善（held-out 长窗无 inner-ring seeds）。B01 把它写成"3 个长窗都改善 0.01-0.03"是把 validation cell（snr20-nominal-long）混进 held-out 的 overreach。
4. VERDICT B 自动 rotation（用户 §九"按上述 A/B/C 自动收口"）：候选族转向不依赖 collapse detector 的机制（equalizer 侧学习型校正器 C04/C09，task comparator=fixed_μ CMA；或 C13 pilot-aided / C12 coded 不同信息类）。

### 排除的替代方案

- **维持 D008 并启动 B02**：拒绝；会跳过 B01-R 的科学保真修复，把 AWGN/ambiguous 误当 collapse 监督信号。
- **删除 D008 / B01 raw / H005**：拒绝；B01 的 raw 数值、closure 资产、PI-SER evaluator 仍是有效诊断与次级论文材料（H029-H034）；D008/H005 标 superseded 保留可审计血缘。
- **强行建更大 test seed budget 重试 detector**：拒绝出本轮范围；记录为 §9 open question；下一对话决定。
- **穷举更多均衡器（RLS/FD/neural）**：拒绝；用户 §三"baseline 不必是当前 SOTA"；fixed_μ CMA 已是公平 comparator。
- **把 B01-R 数字写入论文正文**：拒绝；Scout/Sandbox；晋级需用户 strategy 决策。

### 影响范围

- H005 被 H006 取代为续接入口（H005 不删除）。
- B01 raw artifacts（`fairness-batch-b01/artifacts/*`）字节未改；保留为 DIAGNOSTIC history。
- B01-R raw artifacts（`fairness-batch-b01r/artifacts/*`）是新的高保真证据源。
- topic-index 不变量段无变更；harvest-addendum.v3-b01r.yaml 追加 H029-H034；provenance 沿用 v1 + 新增 4-cat label / degradation onset / warning lead time 三个 DERIVED_HERE 推导。
- protected history（B001-B003 / P03 / CB1 raw / canonical-state）字节未改；无 B004；无 ML 训练；无 push。
- B02 detector 路线暂停；下一动作见 H006（rotation 到 C04/C09 学习型校正器或 C13 pilot-aided）。

### 来源

S006 / B01-R 纠偏科学运行 / 独立 verifier CONFIRM 11/11 / baseline-adjudication + evidence-and-claims 参考 / 用户 2026-07-21 10 条审计 + 自动收口授权。

---

## D010: B01-R hotfix v2 — VERDICT B → A（修正 D009）；C11_fixed_mu 是真阳性 signal；forward rule 加 blind-affine 双 comparator

> status: active
> date: 2026-07-21（hotfix）
> 取代：D009 中 VERDICT B 推论链的具体技术内容（fairness-survives 部分不变；detector target 从 "NOT READY" 改 "READY (thin)"；C11/C11_fixed_mu 信号重评；fixed_μ 最优 μ 从 0.01 改 0.03；下一动作加 forward rule 双 comparator 约束）
> 被取代：无
> 依据: 用户原话（外部评审）: "结论：B01-R 比上一轮好很多，真正修复了切分和 fixed-μ baseline；但仍不能按"最终闭环 PASS"接收。当前应标为：PARTIAL / B-like" + "verifier 又漏掉了"全 NaN baseline、warmup 错位、伪 5% FPR"。因此现在不要开 B02，也不要直接开 C04/C09。先在原对话完成这个小修复，交给我再审；通过后再开新对话进入下一批" + 验证: `fairness-batch-b01r/artifacts/fairness-batch-b01r-v1.json`（metadata.hotfix_version=hf2_2026-07-21）+ `fairness-batch-b01r-v1-synthesis.md` v2 + V002 独立 verifier CONFIRM 13/14 + 1 P1 修复

### 决策

外部评审识别的 7 个 B01-R v1 实现 flaw 全部独立确认。hotfix v2 修复全部 7 个，重新运行后 verdict 从 B 改为 **A**：

1. **公平性存活（不变）**：best 方法 C11_fixed_mu 关闭 3/7 < 5/7 threshold。
2. **detector target 从 NOT READY 改 READY (thin)**：min_z2 修复后（output_power fallback）有 2 个 two-class held-out cells；c05_alert_earliness 也有 2 个。但 detector target 是 "thin"：min_z2 在这 2 个 cells AUROC=1.000（ML 不能在 AUROC 上赢 ceiling）；lead time 实际全 ≤ 0（detector 在 onset 之后才 fire，没有真正提前预警）。
3. **fixed_μ 最优 μ 从 0.01 改 0.03**：grid 扩展到 1e-1，μ=0.03 是真正内部最优（μ=0.1 diverged）。
4. **C11_fixed_mu 是真阳性 method signal**：stage-1 继承 tuned μ=0.03 + DD-LMS，在 4/7 held-out cells 显著优于 fixed_μ CMA（paired CI 排除 0），|Δ| ≈ 0.01 PI-SER。v1 的 C11（stage-1=anchor μ=0.001）vs fixed_μ 时 7/7 更差，不是阳性 signal。
5. **forward rule（HF8）**：任何未来 learned-corrector batch 必须用双 task comparator：fixed_μ CMA μ=0.03（system anchor）+ blind_affine_16qam（task-specific Kill, FR-21）。

VERDICT A **不自动授权 B02**：detector target ready 是 "by contract letter" 但 thin；B02 若跑需换目标（lead-time maximization 而非 AUROC；或 generalization 到 single-class cells）。

### 理由

1. v1 的 VERDICT B 是 min_z2 NaN bug 机械触发的，不是科学得出的；修复后真实状态是 A。
2. C11_fixed_mu 的 4/7 显著改善（vs fair fixed_μ baseline，不是 vs 旧 anchor）是 B01-R 的真正科学产出——是整个 campaign 中第一个显著超越"公平调参传统 baseline"的方法。
3. min_z2 AUROC=1.000 揭示：conventional baseline 已在某些 cells 达 ceiling；ML 必须在非 AUROC 维度（lead time / calibration / generalization）赢，否则没贡献。
4. forward rule（HF8）防止未来 corrector batch 重蹈 C11 v1 覆辙（vs 错误 comparator 假装赢）。
5. μ=0.03 是 interior optimum，fixed_μ CMA 现在是真正"充分公平调参"的 baseline（v1 的 μ=0.01 是 grid 边界，不够）。

### 排除的替代方案

- **维持 D009 VERDICT B 并暂停 detector 路线**：拒绝；VERDICT B 是 bug 触发，不是科学结论；修复后必须诚实改 A。
- **直接推导启动 C04/C09 learned corrector**：拒绝（按评审明确要求）；C11_fixed_mu 的 0.01 margin 是 learned corrector 必须超越的 gap，但需用户战略决策 + forward rule 双 comparator 约束。
- **把 C11_fixed_mu 写成"DD-LMS 解决了 collapse"**：拒绝；4/7 cells 改善 0.01 PI-SER，headroom 仍 ≥ 6×MDE；只是"小但显著的渐进改善"，不是问题闭合。
- **删除 D009**：拒绝；D009 标 amended（不 superseded，因为 fairness-survives 部分仍有效），保留可审计血缘。
- **修改 B01 raw / protected history**：拒绝；本轮 hotfix 仅改 B01-R 自身的 artifacts（raw JSON、synthesis、frozen params）和治理文件。

### 影响范围

- H006（v1 handoff）被 H007 取代（不删除，标 amended）。
- B01-R raw artifacts 被 hf2 版本覆盖（v1 在 git commit 0404f47 可恢复）。
- topic-index 不变量段无变更；harvest-addendum.v4-b01r-hotfix.yaml 追加 H035-H038（v1 H029-H034 内容修正）。
- protected history（B001-B003 / P03 / CB1 raw / canonical-state / B01 raw）字节未改；无 B004；无 ML 训练；无 push。
- 下一动作见 H007：VERDICT A + forward rule；**等用户战略决策**（评审明确"通过后再开新对话进入下一批"）。

### 来源

S007 / B01-R hotfix v2 科学运行 / 独立 verifier V002 CONFIRM 13/14+1P1修复 / 外部评审 2026-07-21（7 个 flaw）。

## D011: C11 legality batch — VERDICT B (signal disappears after legalization); 撤回 D010 的 C11_fixed_mu 4/7 阳性子结论

> status: active
> date: 2026-07-21
> 取代：D010 第 4 点（"C11_fixed_mu 是真阳性 method signal"）和 H007 第 2、3 关键发现（fixed_μ μ=0.03 不变；C11_fixed_mu 4/7 显著改善**撤回**）；forward rule 第 2 comparator 修正（oracle_affine_16qam → blind_affine_compare_16qam）。D010 fairness-survives 部分、fixed_μ μ=0.03 部分、min_z2 detector ceiling 部分不变。
> 被取代：无
> 依据: 调研: `c11-legality-batch-v1/R001-c11-legality-root-cause.md`（Phase 1-3 根因调查，含 b01_candidates.py 行号 220/254/287/290 + 数值复现 max|ΔzX|≈1.97 + 数值 SGD 4 个 update rule 比较）+ 验证: `c11-legality-batch-v1/artifacts/result.v1.json`（schema direction-lab.cb1.c11-legality-batch.v1）+ `c11-legality-batch-v1/artifacts/synthesis.v1.md` + 独立 verifier V003（10 项检查全 PASS，每数字独立重算）+ `c11-legality-batch-v1/tests/test_c11_legality.py`（13 tests 全 PASS：8 gates + 4 OLD-impl bug 确认 + 1 contract-path）+ 触发原话: 用户 2026-07-21 任务附件 "在统一复数滤波约定、无未来信息、同 pass/同预算、dd_step=0 身份门成立的前提下，合法的 CMA→DD-LMS 是否仍显著优于公平 fixed-μ CMA？"

### 决策

合法化后（统一 bilinear r@w 约定 / 因果 one-pass CMA→DD switch / 同 pass 预算 / dd_step=0 身份门）重测 C11，verdict = **`B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION`**。

1. **C11 原实现的 3 个合法性缺陷全部独立确认并定位**：
   - D1 复数约定突变：stage-1 用 `r @ w`（bilinear，anchor 约定），stage-2 用 `np.vdot(wxx, rx)`（= `w^H r` Hermitian）。复数权重下二者严格不等；dd_step=0 时 max|ΔzX| ≈ 1.97（≈ 星座点间距）。`b01_candidates.py:290-291`。
   - D2 非因果未来信息：stage-2 从 i=0 开始用 stage-1 final 权重（看完整个 stream 才得到）。`b01_candidates.py:287`。
   - D3 多 pass / 预算不等：每个样本被访问 3 次（stage-1 + replay + stage-2）vs comparator 1 次。`b01_candidates.py:220/254/287`。
2. **合法化后的 C11_legal 在 7 个 held-out cells × 10 个 fresh test seeds 上显著**不**优于 fixed-μ CMA**：macro paired Δ (C11_legal − fixed_μ) = **+0.01445**（C11 更差），95% CI = [−0.00022, +0.04113]。2/7 long cells 显著更差（snr10-fg100-long Δ=+0.025 CI [+0.00078, +0.05117]；snr15-fg1000-long Δ=+0.077 CI [+0.017, +0.139]）；0/7 显著更好；5/7 short cells 实质 tie（|Δ| < 0.001）。
3. **D010 第 4 点 C11_fixed_mu 4/7 阳性 method signal 撤回**：reclassified as implementation/confound diagnostic，由 D1+D2+D3 三缺陷造成。C11_legal 不被 promote 为合法 conventional comparator。
4. **forward rule（HF8）的 task-specific comparator 修正**：D010 写 "blind_affine_16qam (task-specific Kill, FR-21)" 是标签错误（line 352 把 oracle_affine_16qam 标为 blind）。仓库实际有两个独立函数（cb1_evaluator.py:106/132）：
   - `blind_affine_compare_16qam(z_calib, z_eval, ridge)` — z 派生伪标签，无 TX truth，**receiver-visible 同任务 comparator**（合法 Go baseline）
   - `oracle_affine_bound_16qam(z_calib, z_eval, truth_calib, ridge)` — 用 TX truth 做 calibration，**scoring-only Kill bound (FR-21)，禁止当 Go baseline (FR-25)**
5. **C04/C09 learned corrector 仍不授权**：D010 forward rule 的 "超越 C11_fixed_mu 0.01 margin" 失去依据；corrector 必须超越 `blind_affine_compare_16qam`（receiver-visible），不是超越 C11。

### 理由

1. **H1 根因假设（R001）被证据支持而非否决**：合法化后原 4/7 信号消失甚至反向（long cells 显著变差），符合 "C11 信号来自约定突变 + 未来信息 + 多 pass 的 artifact" 假设。否决条件（合法实现下信号仍存活）未达到。
2. **合法实现的所有身份/因果/预算测试 PASS**（8 gates + 4 negative-control 全绿，独立 verifier 10 项复核 CONFIRM），裁决 B 不是测试失败或架构阻塞，是真正的科学结果。
3. **long cells C11_legal 反而显著更差**揭示：因果 DD-LMS 对已收敛的 fixed-μ 权重做 per-symbol update 反而**扰动**它们；原 "4/7 改善" 完全靠非因果 full-stream second/third pass 的离线平滑效应。
4. **数据切分严格无泄漏**：validation [31-35] / test [41-50] 全新 seeds，与 B01-R 的 [11-15]/[21-30] 完全不相交（代码 assert）。fixed_μ μ=0.03 从 B01-R HF6 继承（不再 re-tune，无 double-dip）。
5. **switch_point 冻结后才进 test**：plateau block 估算 + offset grid {0,+1,+2} 在 validation 上选，frozen 后才进 test（contract 明禁 "selecting_switch_point_on_test_seeds"）。

### 排除的替代方案

- **维持 D010 第 4 点（C11_fixed_mu 是真阳性 method signal）**：拒绝；4/7 阳性是 D1+D2+D3 缺陷的 artifact，合法化后消失甚至反向。继续维持等于把 implementation confound 当成科学结论。
- **用合法 C11 的 long cells 显著更差反推 "DD-LMS 有害"**：拒绝；这是 LOCAL_RESULT_SLICE（7 cells × 10 seeds × 1 switch policy × 1 μ），不能外推到 "DD-LMS 在该信道下总是有害"。legal C11 在 short cells 与 fixed_μ 实质 tie，DD 没用而非有害。
- **裁决 C（ARCHITECTURE_BLOCKED）**：拒绝；所有身份/因果/预算门 PASS，没有架构阻塞。Verdict C 只能用于真正的能力缺失，不能掩盖测试失败（合同明示）。
- **删 D010**：拒绝；D010 fairness-survives 部分、μ=0.03 部分、min_z2 detector ceiling 部分仍有效，只 amend 第 4 点和 forward rule 第 2 comparator。D010 标 amended 不 superseded。
- **修改 B01-R raw artifacts**：拒绝；contract 明禁。57384ed 的产物保留为历史，新结果走新路径 `c11-legality-batch-v1/artifacts/`。
- **直接开 C04/C09**：拒绝（D010 forward rule 仍有效）；corrector 必须先超越 `blind_affine_compare_16qam` 才算贡献。

### 影响范围

- 仅在本 campaign worktree（`.worktrees/direction-lab-capability-atlas`）内新增 `c11-legality-batch-v1/` 目录（research note + contract + c11_causal.py + run_c11_legality_batch.py + tests + artifacts）。
- D010 标 amended（不 superseded）；H007 标 amended by H008；V002 保留。topic-index 的 "已确认结论 / 其他结论" 段更新。
- harvest-addendum.v5-c11-legality.yaml 追加：复杂约定突变教训 / 非因果未来信息教训 / no-op identity 门教训 / C11 negative result。
- protected history（B001-B003 / P03 / CB1 raw / canonical-state / B01 raw / B01-R raw）字节未改；无 B004；无 ML 训练；无 detector/B02 启动；无 push。
- **detector / B02 仍暂停**（任务 brief 明示）。
- 下一动作见 H008：re-rank equalizer 方向 by residual headroom over `oracle_affine_bound_16qam`（Kill bound）；或 rotate 到 path 2（detector lead-time）；或 rotate 到 C12/C13。**等用户战略决策**。

### 来源

S008 / c11-legality-batch-v1 科学运行 / 独立 verifier V003 CONFIRM V1-V10 全 PASS / R001 根因调查 / 用户任务附件 2026-07-21（强制 systematic-debugging Phase 1-3 + TDD + 独立验证；"局部实现失败、参数不工作或旧信号消失时不要停下来问我；继续完成 A/B/C 裁决"）。

---

## D012: C11 状态收口 — verdict 标签 scope-narrow（amended D011）+ 8 审计问题处理 + 不重跑

> status: active
> date: 2026-07-21
> 取代：D011 的 verdict 标签范围（`B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION` → scope-narrowed `C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`，ceiling = `LOCAL_SLICE / DIAGNOSTIC`）。**D011 的数值结论（macro +0.01445、2/7 long cells 显著更差、4/7 阳性撤回）不变**；D011 标 amended 不 superseded。
> 被取代：无
> 依据: 调研: 用户 2026-07-21 任务附件列出的 8 条 C11 已知问题 + 独立核验（见 S009 §Phase 1 表 + synthesis.v1.md §10 表）+ 验证: `c11-legality-batch-v1/tests/test_c11_legality.py` 19/19 PASS（新增 6 个 portability/provenance/scope gate tests）+ 手算 short-cell eval window DD 覆盖（64/128 at offset=+2）+ 触发原话: 用户 2026-07-21 任务附件 "C11 状态应收窄为 `C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`，claim ceiling = LOCAL_SLICE / DIAGNOSTIC" + "修复 UTF-8 可移植性测试和最小 provenance 记录；按 session-governance 将原正式 Verdict B 标为 amended/PARTIAL，不删除历史"

### 决策

**1. Verdict 标签 scope-narrow**：
- 保留原标签 `B_C11_SIGNAL_DISAPPEARS_AFTER_LEGALIZATION`（traceability）
- 新增 scope-narrowed 标签 **`C11_EXACT_CAUSAL_RAW_DECISION_POLICY_NO_BENEFIT`**
- claim ceiling 收窄为 **`LOCAL_SLICE / DIAGNOSTIC`**
- 允许声称：（a）旧 4/7 阳性是 implementation confound；（b）当前具体 raw-decision 策略（causal one-pass + nearest-16QAM DD + switch_point=plateau+{0,1,2} + dd_step grid [0..3e-4]）无收益；（c）2 个 long cells 显著更差
- 禁止声称：（a）整个 DD-LMS 家族失败；（b）C11 已被全域关闭；（c）7 个 cells 都充分测试了 DD 阶段（short cells 只 ~一半符号进 DD）

**2. 8 条审计问题的独立核验 + 处理**（全部独立核验，全部为真，但都不改变 verdict 方向）：
- #1（no-op test switch=10**9）：DOCUMENTED + 锁定 finite-switch 变体共存
- #2（finite-switch 证的是冻结权重不等于持续 fixed-μ）：DOCUMENTED 两 test 答不同问题
- #3（held-out switch/plateau 未完整预冻结）：DOCUMENTED P1 debt，偏置朝 C11
- #4（Windows UTF-8）：**FIXED** 4 处 open() 加 encoding="utf-8"
- #5（artifact 缺 source closure hash）：**FIXED** 新增 `_source_closure_hashes()` 记录 9 源文件 SHA-256
- #6（dd_step + offset 在网格边界）：DOCUMENTED scope limit，两方向都不会翻 verdict
- #7（short-cell eval window ~一半符号在 DD）：DOCUMENTED 手算验证 64/128，只影响 tie 的 short cells
- #8（DD raw-decision 无 phase/permutation resolution）：DOCUMENTED scope limit，让 C11 更差而非更好

**3. 不重跑 C11 科学批**：用户 brief 明示 "不要重跑完整 C11 科学批，除非独立审查证明某项最小修复会改变已有数值方向"。本轮独立审查结论：8 条问题无一改变数值方向（macro +0.01445 不变；2/7 long cells 显著更差不变）。因此不重跑。

### 理由

1. **数值方向稳健性**：每个审计问题要么不影响 verdict 方向（#1/#2/#3/#6/#7/#8 是 scope 限制或文档清晰度），要么偏置朝 C11（#3 让 held-out 用自己 plateau、#8 让 DD 更差）——没有任何一条会让 "C11 no benefit" 变成 "C11 benefit"。
2. **P1 修复的成本/收益**：#4（UTF-8）和 #5（source hash）是 reproducibility 关键，修复成本低（几行 + 几个 test 锁定），收益高（fresh Windows 可复现 + artifact 可溯源）。
3. **scope-narrow 而非 supersede**：原 verdict B 的数值结论正确，只是 claim 范围过宽。amended 保留历史血缘，superseded 会丢数值结论。
4. **不重跑的工作守恒**：用户 brief 明示 "同一方向连续两轮没有新机制、改善不足 10%，立即轮转"；重跑 C11 无新机制，应轮转到 corrector residual adjudication。

### 排除的替代方案

- **维持 D011 原 verdict 标签不做 scope-narrow**：拒绝；claim 范围过宽会让 "C11 已被关闭" 的误读合法，违反 LOCAL_SLICE 原则。
- **supersede D011（删旧 verdict 标签）**：拒绝；数值结论未变，supersede 会丢血缘。amended 保留旧标签 + 新增 scope-narrowed 标签。
- **重跑 C11 科学批**：拒绝；用户 brief 明示不要，且 8 条问题无一改变数值方向。
- **修复 #6（扩 dd_step/offset 网格）**：拒绝；偏置方向不支持翻 verdict，且会触发重跑。只在 synthesis 标 scope limit。
- **修复 #7（改 short-cell eval window 让全部符号进 DD）**：拒绝；short cells 是 tie，与 DD 覆盖无关；改了反而引入新变量。只在 synthesis 标 scope limit。
- **修复 #8（加 phase/permutation resolution 的 DD policy）**：拒绝；这是新机制，超出 "C11 状态收口" 范围，应走下一个独立 batch（如果 corrector adjudication 转 A 的话）。

### 影响范围

- 仅在本 campaign worktree（`.worktrees/direction-lab-capability-atlas`）内：
  - `c11-legality-batch-v1/run_c11_legality_batch.py`：加 `hashlib` import + `_source_closure_hashes()` + `_sha256_of_file()` + 4 处 open() encoding
  - `c11-legality-batch-v1/tests/test_c11_legality.py`：2 处 open() encoding + 新增 `TestPortabilityAndProvenance` 类（6 tests）
  - `c11-legality-batch-v1/artifacts/synthesis.v1.md`：加 §10（audit issues 表 + verdict scope）
- D011 标 amended（不 superseded）；H008 标 amended by H009（待写）；V003 保留。
- topic-index 的 "已确认结论 / 其他结论" 段更新（D011 增加 scope-narrowed 标签）。
- protected history（B001-B003 / P03 / CB1 raw / canonical-state / B01 raw / B01-R raw / `result.v1.json`）字节未改；原 artifact 不改（新 source-closure hash 只在未来 run 的 metadata 出现）。
- 无 ML 训练；无 B004；无 detector/B02 启动；无 push。

### 来源

S009 §Phase 1 / 用户任务附件 2026-07-21（8 条 C11 已知问题清单 + scope-narrow 指令 + 不重跑指令）/ 19/19 tests PASS / 手算 short-cell eval window DD 覆盖 64/128。

---

## D013: Corrector residual-headroom adjudication — VERDICT A (learned-corrector target ready); blind affine is NET NEGATIVE

> status: amended by D016
> date: 2026-07-21
> 取代：无（新批次，独立产物）
> 被取代：D016（保留 truth-assisted bound 与 blind comparator 数字，撤回 learned-corrector target-ready 解释）
> 依据: 调研: `corrector-residual-headroom-v1/batch-contract.v1.yaml`（冻结 A/B/C 判据 + 信息边界测试）+ 验证: `corrector-residual-headroom-v1/artifacts/result.v1.json`（schema direction-lab.cb1.corrector-residual-headroom.v1）+ `corrector-residual-headroom-v1/artifacts/synthesis.v1.md` + 独立 verifier V004（8/8 任务 PASS，重算 3 cells bit-identical，blind/oracle 信息边界对抗测试 PASS）+ `corrector-residual-headroom-v1/tests/test_information_boundary.py`（12/12 PASS）+ 触发原话: 用户 2026-07-21 任务附件 "在公平调优的 fixed-μ CMA（当前 μ=0.03）之后，最强 receiver-visible blind affine 能关闭多少可恢复 PI-SER 余量？相对于 TX-truth oracle affine，是否仍存在足够支撑 C04/C09 learned corrector 的合法 residual target？"

### 决策

新建隔离版本化目录 `corrector-residual-headroom-v1/`（不覆盖 B01/B01-R/c11-legality）。在 fresh paired seeds（val [61-65] / test [71-80]，与所有先前批次不相交）+ 同 z-stream / 同 eval window / 同 paired realization 下比较：

1. `fixed-μ CMA μ=0.03 + nearest 16QAM`（baseline low bound）
2. `blind_affine_compare_16qam`（receiver-visible，tune ridge → frozen 1e-8）
3. `oracle_affine_bound_16qam`（Kill bound only，FR-21/FR-25）

**裁决 = `A_LEARNED_CORRECTOR_TARGET_READY`**。关键数字（7 held-out cells × 10 test seeds = 70 paired）：
- macro H_total = +0.0617 PI-SER（recoverable headroom 存在；CI [+0.0024, +0.1210]）
- macro G_blind = **-0.0084**（blind affine **净负面**；CI [-0.0153, -0.0025]）
- macro H_residual = +0.0664（blind 后仍存在 residual；CI [+0.0147, +0.1270]）
- macro coverage_blind = -0.19（blind 不关闭 headroom，反而扩大）
- H_residual ≥ MDE 在 **6/7** cells（仅 snr05-short 不达 MDE；oracle 在该 cell 也无力）

### 理由

1. **信息边界测试 12/12 PASS**（blind 不读 TX truth；oracle 显式读 TX truth；perturbing TX truth leaves blind bit-identical AND changes oracle；三者同 z-stream / 同 window / 同 paired realization；fixed-label 与 PI-SER 分开报告；source closure hash 记录）。独立 verifier V004 adversarial 复核 8/8 PASS。
2. **blind affine 是净负面**揭示：z-derived pseudo-labels 在 fixed-μ CMA 收敛后无法识别有用 affine 映射。fixed-μ CMA 已抽出 channel 的 affine 结构；residual 是非-affine（residual ISI + AWGN + SOP drift）。
3. **oracle affine 证明 residual IS recoverable by SOME affine**（H_total 显著），但 receiver-visible proxy（z-derived）too noisy to identify the same map。这正是 "exists vs learnable" 的关键 gap。
4. **数据切分严格无泄漏**：val [61-65] / test [71-80] 与所有先前批次 [11-50] 完全不相交；ridge 在 val 上选后冻结才进 test。

### 排除的替代方案

- **裁决 B（blind 已关闭）**：拒绝；blind coverage 为负，未关闭任何 headroom。
- **裁决 C（UNRESOLVED）**：拒绝；H_residual 远超 MDE，CI 下限 +0.015 > 0，灵敏度足够。
- **treat blind affine degradation 为 A 的 blocker**：拒绝；用户 brief 的 A 定义是 "blind 后仍存在稳定 residual"，blind 退化只让 residual 更大、learned target 更容易。

### 影响范围

- 仅在本 campaign worktree 内新增 `corrector-residual-headroom-v1/`（contract + runner + tests + 3 artifacts）。
- protected history 全未改（独立 verifier V004 确认）。
- 授权 C04/C09 shared corrector batch（D014）在同一对话运行。
- 无 ML 训练（本批）；无 push。

### 来源

S009 §Phase 2 / 用户任务附件 2026-07-21（强制 A/B/C 冻结 + fresh seeds + 信息边界测试 + source closure hash）/ 独立 verifier V004 CONFIRM。

---

## D014: C04/C09 shared corrector batch — VERDICT CANDIDATE_BLOWS_UP for both (EXACT MECHANISM NEGATIVE for context-dependent affine hypothesis)

> status: superseded by D016
> date: 2026-07-21
> 取代：D011 的 "C04/C09 learned corrector 不授权" 推论（D013 授权后本批执行，结果为 negative）
> 被取代：D016（raw 坏结果保留；机制负面由 objective-induced constant collapse 取代）
> 依据: 调研: `c04-c09-shared-corrector-v1/batch-contract.v1.yaml`（冻结 train/val/test seeds + cell split + HP 公平性）+ 验证: `c04-c09-shared-corrector-v1/artifacts/result.v1.json` + `c04-c09-shared-corrector-v1/artifacts/synthesis.v1.md` + 独立 verifier V004（8/8 PASS，重算 candidate macro PI-SER ≈ 0.928，near random-decision ceiling 0.9375）+ `c04-c09-shared-corrector-v1/tests/test_corrector_identity.py`（12/12 PASS）+ 触发原话: 用户 2026-07-21 任务附件 "如果是 A：在同一对话建立 C04/C09 shared adapter；将它们作为同一个 corrector batch 一起运行，不按 MLP/GRU/Transformer 名称拆成多个假方向；conventional task comparator 必须是 receiver-visible blind affine；若两者均失败，记录 exact mechanism negative，并轮转，不继续做网络微调"

### 决策

D013 裁决 A 后，在本对话建立 shared adapter（`apply_correction(z_eval, A, b) = z_eval @ A.T + b`），训练两个函数类：
- C04_mlp：MLP 映射 z_calib SUMMARY STATISTICS → context-specific (A, b)
- C09_gru：GRU encoder over z_calib TIME SERIES → context-specific (A, b)

训练用 MSE(z_corrected_calib, hard_16qam(z_corrected_calib))（receiver-visible only，NO TX truth）。train [81-90] / val [91-95] / test [71-80]（test slice = D013 adjudication 的 blind_affine test slice，paired comparison）；training cells (4 val cells) disjoint from held-out test cells (7)。HP 公平（smoke 显示所有 8 HP 组合 val_loss plateau 在 1.3084，non-discriminating；train ONE representative HP per class）。

**两个 candidate 均裁决 `CANDIDATE_BLOWS_UP`**：
- C04_mlp：macro PI-SER_candidate = **0.928**（near 16QAM random-decision ceiling 0.9375），macro Δ(cand−blind) = **+0.624** CI [+0.483, +0.753]，0/7 cells beat blind by ≥ MDE，worst degradation vs fixed_cma = +0.783。
- C09_gru：macro PI-SER_candidate = **0.928**，macro Δ(cand−blind) = +0.624 CI [+0.483, +0.753]，0/7 cells beat blind，worst degradation = +0.782。

### Exact mechanism negative（核心科学发现）

**Context-dependent affine hypothesis 被 REJECTED for this anchor + channel**：
1. fixed-μ CMA 已抽出 channel 的 affine 结构；residual 是非-affine（residual ISI + AWGN + SOP drift）。
2. z_calib（receiver-visible calibration）**不含足够信息识别 corrective affine**——因为本来就没有有用的 corrective affine 可识别。blind affine 从另一角度确认（net negative）。
3. learned corrector 没有 useful target 可拟合：要么学 identity（匹配 fixed-μ CMA，无改善），要么学 overfit-to-noise 的 non-identity map（scrambles z_eval，本批 outcome）。
4. oracle affine 证明 recoverability 存在但仅通过 TX truth；receiver-visible proxy 太 noisy 无法识别同一 map。

**"exists vs learnable" gap 是 thesis-grade 发现**：adjudication（D013）证明 residual EXISTS（oracle closes it）；C04/C09 证明 residual NOT LEARNABLE from receiver-visible signals。

### 理由

1. **identity 测试 12/12 PASS**（candidate forward 不含 truth 参数；training loss body 不含 truth；affine application 形式正确；shared adapter 两类统一 contract；train/val/test seeds pairwise disjoint + 与 prior [11-65] disjoint；training cells disjoint from held-out；source closure hash）。
2. **训练损失 plateau 在 ~1.31 不论 HP 或函数类**——模型学不到 useful mapping。1.31 ≈ 每个实坐标距任何 16QAM grid level 平均 ~1.1；模型可达下界。
3. **independent verifier V004 adversarial 复核 8/8 PASS**：重算 candidate macro PI-SER = 0.928 ≈ random ceiling；fresh Windows pytest 12/12 PASS；protected history 全未改；source closure SHA-256 全 match。

### 排除的替代方案

- **继续网络微调**：拒绝；用户 brief 明示 "若两者均失败，记录 exact mechanism negative，并轮转，不继续做网络微调"。HP grid 已显示 non-discriminating。
- **加 Transformer 或其他函数类**：拒绝；用户 brief 明示 "不允许把多个模型名冒充多个机制方向"。MLP+GRU 已是两个代表性函数类。
- **改训练 loss（用 Godard-cost unsupervised）**：超出本批 scope；应走下一个独立 batch（如果未来要重新评估 corrector 路线）。
- **改 anchor 或 channel**：超出本批 scope；本批的 negative 是 "在 fixed-μ CMA μ=0.03 + 16QAM atlas 下" 的 LOCAL_NEGATIVE。

### 影响范围

- 仅在本 campaign worktree 内新增 `c04-c09-shared-corrector-v1/`（contract + adapter + runner + tests + 3 artifacts）。
- protected history 全未改。
- **C04/C09 当前 corrector 路线在 this budget + information access 下 CLOSED**。按用户 brief 自动轮转：下一对话检查 C13（去重 pilot→Jones→inverse 微变体）或转 C12 soft-output/coded。
- 无 push。

### 来源

S009 §Phase 3 / 用户任务附件 2026-07-21（强制 shared adapter + 公平 tuning + blind affine 作 task comparator + 失败即轮转）/ 独立 verifier V004 CONFIRM。

---

## D015: S009 收尾 — 轮转到下一机制 family（C12/C13），本轮 SCIENCE_SCOUT 链条完成

> status: amended by D016
> date: 2026-07-21
> 取代：无
> 被取代：D016（因 exact mechanism negative 而强制轮转的推理撤回；轮转仅可作为资源选择）
> 依据: 验证: D012 + D013 + D014 三批 verdict 全独立 verifier V004 CONFIRM + 触发原话: 用户 2026-07-21 任务附件 "本对话至少完成一个科学 adjudication，并对一个后续机制形成 RUN / LOCAL_NEGATIVE / INFRASTRUCTURE_BLOCKED 之一；普通文档债务不构成提前停止理由"

### 决策

S009 当时按用户 brief 完成了 C11 状态收口、corrector headroom adjudication、C04/C09 shared batch 和 V004 artifact 复核，并据此决定下一轮可轮转到 C12/C13/detector 等其他机制族。

**D016 修订**：上述“完成了运行链条”的历史事实保留；D013 learned-target-ready、D014 exact-mechanism negative 以及由此强制轮转的科学推理撤回。当前是否轮转只能是资源选择，不能写成本批科学结论。

### 理由

旧决策依据 D013/D014/V004；D016/V005 后确认 V004 没有覆盖目标函数语义，C04/C09 失败首先来自常数塌缩。

### 排除的替代方案

- **删除 D015**：拒绝；保留决策血缘。
- **继续把轮转写成科学必然**：拒绝；其前提已失效。

### 影响范围

下一科学方向未由 D015 锁定；先执行体系专题 D012 的方法与恢复结构重设计。

### 来源

S009 / V004；由 S010 / D016 / V005 修订。

---

## D016: S009 外部科学审计——C04/C09 为目标函数常数塌缩，撤回机制级负面

> status: active
> date: 2026-07-21
> 取代：D014
> 修订：D013、D015
> 被取代：无
> 依据：S010 的目标函数解析、artifact plateau 对照与 runner/contract 审计；V005 科学语义复核 FAIL

### 决策

1. D013 只保留 `TX_TRUTH_ASSISTED_AFFINE_GAP_PRESENT / LOCAL_SLICE / DIAGNOSTIC`。truth-assisted affine bound 与 blind-affine 净负面数字有效，但 `H_residual=blind-oracle` 包含 blind comparator 自身损害，不能据此自动授权 learned corrector。
2. D014 的 C04/C09 raw 运行结果保留，科学裁决改为 `IMPLEMENTATION_CONFOUND_CONSTANT_COLLAPSE`。训练目标存在输入无关常数最优解，候选状态恢复为 `UNRESOLVED`；不得声称 `z_calib` 无信息、residual 非 affine、receiver-visible affine 不可学习或方法路线已关闭。
3. D015 中由“exact mechanism negative”强制轮转的因果链撤回。轮转仍可作为资源分配选择，但不是本批证据强制的科学结论。
4. V004 保留 artifact fidelity、hash、seed split、protected-history 等验证价值；其科学语义确认由 V005 修订为 FAIL。
5. 旧 artifact 不覆盖、不删除。本次用 S010、H010 和 harvest v7 构成 append-only 修订链。

### 理由

soft expected-distance 目标在 `A=0` 且输出常数约 `±0.6075` 时达到四维 loss 约 `1.30840175`，精确解释所有配置的 `1.3084` plateau。该最小反例比网络结构、超参数或全量统计更接近根因。旧证据链证明了错误目标的可复现性，却没有证明候选机制失败。

### 排除的替代方案

- **补更多超参数或 seeds**：拒绝；不能消除目标函数的输入无关最优解。
- **删除或重写旧 artifact**：拒绝；保留历史，靠显式 amendment 修正当前态。
- **把 D013 全部判无效**：拒绝；truth-assisted bound 与 blind comparator 的 raw 数字仍有效，只需收窄语义。
- **立即重跑 corrected v2**：拒绝；先完成 Probe/恢复/文件体系重设计，避免再次把“小修”扩成完整重链。

### 影响范围

仅修订 S009 的科学解释、当前恢复入口与 harvest 状态；C11 D012 不变；不修改代码、旧 artifact、baseline、protected history 或 Skill。

### 来源

S010 / V005。触发原话为流程与记录体系要求，见本专题及体系专题 `voice.md` 2026-07-21。
