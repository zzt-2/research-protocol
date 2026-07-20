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

> status: active
> date: 2026-07-20
> 取代：无
> 被取代：无
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
