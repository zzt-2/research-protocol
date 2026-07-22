# [S011] 混合盲均衡/专家路由 — 继承状态纠正与系统研究

> 2026-07-22 | SCIENCE_SCOUT Macro A-prelude / A / B / C | 状态: 进行中

## 目标

1. 对 commit e15ae60（C12/C14/C15/C16 campaign + 重写 current views 为"5 轴穷尽"叙述）做有界 reconciliation：区分"原始数值可复现 / 实现身份正确 / 科学语义有效 / 当前 claim ceiling / 仍 UNRESOLVED"。**不重跑科学实验**。
2. 在纠正后的状态上开展"坍塌感知的混合盲均衡/专家路由"系统研究，连续推进到 A/B/C/D 裁决并完成交接。

## 记录

### 0. 继承状态识别（关键治理发现）

H010（D016/V005）是唯一恢复入口，明确要求"体系设计固定前不启动大规模科学运行"。但 e15ae60 在 H010 **之后**提交，一次性新增 C12/C14/C15/C16 四个 scout（~20k 行）并重写 STATUS/state/portfolio/harvest 为"5 轴穷尽 / 坍塌是信道属性"叙述——**但未新增任何 S###/D###/V###/H###**，注册表 last_updated 仍为 2026-07-21。即 e15ae60 的科学结论未经治理登记，直接变成"当前视图"。

提示词明确禁止直接继承 e15ae60 的 5 条结论（"5 轴穷尽"、"坍塌是信道本质属性"、"不可提取求逆信息"、"可写完整负面边界论文"、"model-based tracker 唯一剩余方向"）。本轮先独立复现并处置 7 个审计问题。

### 1. 七审计项有界 reconciliation（全部 CONFIRM，独立子 agent 核验 + 主线复算）

> 约束：**不重跑科学实验**。只做 reproduce-vs-validity 拆分。

| # | 审计项 | 复现/核验结论 | 科学语义处置 |
|---|---|---|---|
| 1 | C04 动态 hard-decision 目标仍有 A=0/b=星座点 零损失退化解 | CONFIRM — O1-corrected 目标是 self-referential moving target `MSE(A·z+b, hard(A·z+b))`，全局最优 = 常数塌缩(loss=0)；constant-smoke 测的是 blind-affine 的 fixed-target，不是实际训练目标 | C04 恢复 `IMPLEMENTATION_CONFOUND/UNRESOLVED`；C09 同；"context-dependence 无价值"结论**撤回** |
| 2 | C12 oracle 仅 TX truth 估全局 σ² 再跑相同 max-log | CONFIRM — oracle 只换全局 σ²；histogram-MI 对公共 LLR 缩放不敏感（scale-invariant）；synthesis 自 concession | C12 "零 GMI headroom" **不是真上界**，降级为 scale-artifact；H062 撤回；GMI evaluator 资产保留 |
| 3 | C14 truth-Wiener 与中心抽头 cosine≈0.9995，whitening/multistart 不代表初始化族 | CONFIRM — oracle Wiener TX-truth-conditioned（correctly Kill-only）；0.9995 仅 synthesis narrative，shipped src 无 cosine 计算；far-orthogonal probe（cosine 0.03-0.35）只在 narrative，未在 src | C14 仅证明"最强单 init 塌缩"；"init-invariant across direction space"**未由 shipped code 证明**；H063 scope-narrow |
| 4 | C15 对梯度尺度差 ~19× 的方法统一 μ=0.03 | CONFIRM — godard/ring_aware/rccma 共享 μ=0.03，无 per-cost μ/梯度归一化；synthesis 自报 19× 梯度比 | C15 "ring-aware 自洽塌缩" **被 unequal-step 混淆**；H064 撤回机制断言，保留"cold-start freeze"文档化行为 |
| 5 | C16 是简化瞬时 2×2 whitening + real Givens，非完整 complex JADE/ICA，非与 11-tap CMA 能力对齐 | CONFIRM — `hos_equalizer.py` 空间 2×2 + real θ grid + 单标量 phase，无 n_tap/FIR/sliding-window；vs CMA anchor 11-tap 4-filter butterfly block-64 | **C16 不是合法 capability-aligned fallback expert**；H065 保留为"paradigm-distinct 但 task-mismatched"诊断；**关键**：混合路由假设的"26/37 互补"正建立在此非法专家上 |
| 6 | seeds 71–80 已多轮观察，不能作 confirmatory held-out | CONFIRM — 71-80 在 ≥6 独立批（c04/c09/c14/c15/c16/corrector + c12 子集 71-76 + probes 71-73）重复使用；contract 自承认"intentional reuse"；仅 c11(41-50)/b01r(21-30)/atlas(11-20) 真正 disjoint | seeds 71-80 **失去 held-out 资格**；任何 confirmatory test 必须用全新 disjoint seeds |
| 7 | H060 最高只能暂定 LOCAL_SLICE，须排除无效 C12/C16 证据 | CONFIRM — H060 evidence 链含 C12(scale-artifact)/C16(task-mismatch)；排除后 H060 仅剩 C04/C09(confounded)/C14(scope-narrow)/C15(confounded) | H060 **降级 + 拆分**：全域"信道属性"宣称 invalidated；保留为 LOCAL_SLICE "Godard-cost 在本 slice 上塌缩"弱断言 |

### 2. 主线复算：C16 原始数据里的"诊断互补"是否真实可复现

直接读 `c16.../artifacts/result.v1.json`（110 realizations = 11 cells × 10 seeds），不依赖 e15ae60 synthesis：

- CMA macro PI-SER = 0.2507 ✓（与提示词线索 0.2507 一致）
- HOS macro PI-SER = 0.4664 ✓
- CMA>0.3（塌缩）子集 = 37 realizations，其中 HOS 在 26 个上更好 ✓（与线索 26/37 一致）
- per-realization oracle selector min(CMA,HOS) macro = 0.1928（线索 ~0.2073；绝对余量 0.0579 vs 线索 0.0434，同量级，差异来自 macro 定义）

**诊断互补数值可复现**。但（a）该 HOS 是 task-mismatched 非法专家（审计 5），（b）seeds 71-80 失去 held-out 资格（审计 6），（c）oracle 用了事后 PI-SER。故此"headroom"严格为 **DIAGNOSTIC only**，不能授权任何 Go。

### 3. 合法 capability-aligned fallback 候选盘点（inventory）

参考结构：`CMAEqualizer2x2` = 11-tap 4-filter 2×2 butterfly FIR, center-tap init, block_size=64, 单 pass。

- **MMA (Yang-Werner-Dumont 2002)** — `baseline-adjudication-batch/mma_comparator.py`，已 11-tap butterfly 能力对齐，机制不同（per-axis modulus 拆 real/imag）。**唯一干净合法 fallback**。但 D006/D040 已记 MMA FAILED（且受同 μ 公平性问题）。
- **CMMA / RCCMA / ring-aware** — C15 已测，受审计 4 混淆，冗余。
- **DD-LMS** — 仅作 C11 cascade stage-2 存在；**无 standalone cold-start 实现**。冷启动 DD-LMS 通常发散（这正是 cascade 存在的原因）。
- **C16 HOS** — 非法（task-mismatch），不可作 fallback。
- 监督 ML equalizer — 非法（用 TX truth）。

**结论**：合法、能力对齐、机制不同、且未受混淆的 fallback 候选 = **MMA（需公平 μ 重测）+ standalone DD-LMS（需新建，预期冷启动发散）**。这是 Macro A 的输入。

### 4. 决策与处置（见 decisions.md D017 / verifications.md V006）

- D017：e15ae60 5 条结论不直接继承；7 审计项 reconciliation 结果登记；H060 拆分降级。
- V006：7 审计项独立核验 + 主线复算记录（PASS = 审计项全部 CONFIRM；数值可复现但科学语义失效）。
- 本轮**未重跑科学实验**，未建新 controller，未改 protected history。

## 决策引用

- D017：e15ae60 继承结论纠正 + 7 审计项 reconciliation + H060 拆分降级（新建）
- V006：7 审计项独立核验 + 主线复算（新建）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。原始目标 = SCIENCE_SCOUT campaign 的"多候选批量 Scout → synthesis → harvest → 自动轮换"。混合路由研究是同一 anchor（dual-pol OSL 盲均衡）下的候选族研究，未改 formal goal / 场景 / 贡献线。7 审计项 reconciliation 是"恢复正确性"的强制前置（提示词第一节），不扩范围。

## 后续

- Macro A：用合法 fallback（MMA 公平 μ 重测 + standalone DD-LMS 探针）重测 oracle 互补性。若合法专家间无实用 oracle headroom → 直接裁决 C。
- Macro B：仅在传统阈值留下明确余量时才训 ML router。
- 全程 fresh disjoint test seeds（非 71-80）。
- 详见 hybrid-routing Scout contract。

---

## Macro A 结果 + VERDICT C（2026-07-22 续）

### 实现

- `hybrid-routing-scout-v1/`：batch-contract（frozen A/B/C/D 判据 + 实用阈值 0.03 + 失败分类法）+ `dd_lms_equalizer.py`（legal cold-start DD-LMS，5/5 身份门 PASS）+ `run_macro_a_oracle.py`。
- 合法专家：CMA anchor（μ=0.03）+ MMA（YWD，per-cost μ tuned→0.003）+ DD-LMS（cold-start，μ tuned→0.1）+ oracle unmix（Kill bound）。MMA/DD-LMS 均 11-tap 2×2 butterfly FIR，与 anchor 能力对齐。
- Fresh disjoint test seeds [121-130]（与 11-20/21-30/41-50/71-80 全 disjoint）；validation [101-105]。

### 关键数字（11 cells × 10 test seeds = 110 realizations）

| macro PI-SER | CMA=0.3972 | MMA=0.5031 | DD-LMS=0.4319 | Oracle=0.2196 |
- oracle selector all3 macro = 0.3935 → **headroom over CMA = 0.0037**（阈值 0.03 的 12%，8× 以下）
- complementarity: MMA better 5.5%/worse 58%；DD-LMS better 21%/worse 35%
- collapse 子集（CMA>0.3, n=61）：MMA 更好仅 5/61，DD-LMS 更好仅 5/61——**fallback 在 CMA 塌缩的同一 realizations 也塌缩（correlated failure modes）**
- 仅 2/110 realizations 有任何专家超 CMA >0.03

### VERDICT: **C = COMPLEMENTARITY_INVALID**（D018）

- headroom 0.0037 远低于实用阈值 → 按 frozen contract 直接裁决 C，停止训练 router。
- **Macro B 不运行**：oracle 上界本身已低于阈值，任何 router（阈值/低复杂度/ML）无 headroom 可转化；训练=为 ML 而 ML。
- 机制：合法 FIR 盲均衡器都是近共模目标上的梯度法，共享塌缩盆地（correlated failure）。与 Johnson 1998 / Qian 2002 / Kuncheva 一致。定性已知，非新发现。
- 原 C16 "26/37"确认为非法专家 + 污染 seeds 的伪象。
- 关闭**本具体** hybrid contract；**不关闭**算法选择家族（model-based tracker 维度仍 open）。

### 独立 verifier（V007）

8/8 adversarial check PASS（1 PARTIAL on μ-tuning 非 verdict-changing）。headline 独立重算 bit-identical。verifier 专门测了"convenient conclusion"怀疑论：CMA 给了最强 μ（偏向 verdict C），但 headroom 仍 8× 低于阈值——结论稳健。2 个 caveat：DD-LMS weight-norm bug（已修，0 divergence）+ tune_mu 单 seed（impact 0.00003）。

### 论文价值（Macro C2）

- 方法贡献：无（verdict C）。
- ML 贡献：N/A（无 router）。
- 机制贡献：correlated-failure-mode 真实但定性已知（Johnson 1998），非新。
- 评估贡献：channel-specific 负面 bound（headroom≈0.004 on OSL GG+SOP）= 小负面/boundary note，非 primary spine。
- 负面材料：D017（task-mismatch 伪互补教训）+ 本 D018（correlated-failure 量化）= 可毕业的负面材料，但不构成方法论文主线。
- **结论：本轮不产出毕业论文级"方法"。** 既有有效负面（C11/MMA<CMA/blind-affine harmful/LOCAL_SLICE Godard-collapse）+ 本轮负面 bound 仍为可收获材料。
