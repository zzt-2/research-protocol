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

> status: active
> date: 2026-07-20
> 取代：D005 中"裁决达到 PROBLEM_SURVIVES_CONVENTIONAL_BASELINE 后才允许 bounded ML Scout"的条件触发部分（现在已满足，授权生效）
> 被取代：无
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
