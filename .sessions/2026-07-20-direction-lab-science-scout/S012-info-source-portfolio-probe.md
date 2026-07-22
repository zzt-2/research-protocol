# [S012] 信息来源组合级 Probe — F1-A/F3-A PASS，F4-A BOUNDARY；F1-B 投资选择待用户

> 2026-07-22 | SCIENCE_SCOUT（D019/H012 续接） | 状态: 本轮完成，交用户决策 F1-B 投资

## 目标

回答 D019/H012 的科学问题："哪一种新增、合法、运行时可获得的信息，最可能打破当前盲均衡器的相关失败，并形成可写进毕业论文的正面方法？" 对四类信息来源（channel-model prior / sparse pilot / causal history / decoder-soft）做组合级 headroom/observability Probe，统一排序后决定投资哪条方法线。

## 记录

### 1. 接收 H012（session-governance Trigger 1/5）

独立核验 3 条关键事实全部 PASS：
- hybrid oracle headroom `0.003693` + 阈值 `0.03`（result.v1.json aggregate 重算 bit-identical）
- test seeds `121-130` 与所有 prior disjoint（contract prior_used_do_not_reuse 核对）
- state/portfolio/harvest YAML 可解析，recovery_entry=H012

### 2. 候选族 Map（提示词 §三：先列全、归类、去重，再排序）

派 3 个 explore 子 agent 并行盘点：portfolio/negatives、代码与 runner、接收机处理链 + 物理门限。
产出 `candidate-map.v1.md`：四族 F1-F4 × 作用点 × 输出动作，每个候选 12 项属性。
**关键去重**：HYBRID_ROUTING（D018）、pilot→Jones→inverse（p03 COLLISION）、C12 全局-σ² oracle（D017/V006 scale-artifact）、C16 非-FIR HOS（D017）、C04/C09 self-referential 目标（D016/D017）。
**关键修正（FR-26）**：子 agent 报"C12 scale-artifact provenance NOT FOUND"，主线读 `soft_demap.py:344` + V006:220 确认 oracle 仅估全局 σ²——artifact 真实存在，子 agent 遗漏。

### 3. 冻结共享 Probe contract（提示词 §四：先冻结 8 项再跑）

`probe-contract.v1.yaml`：同 anchor（standard_cma_godard_z, fixed-μ=0.03）/ 同 11-cell slice / 同 eval-window(256) / 同 paired realization / fresh disjoint seeds [131-135 val / 141-150 test]（**不碰 71-80**）。冻结 question/hypothesis/falsifier/legal information/comparator/semantic smoke/budget/claim ceiling。verdict_criteria 四态。YAML 解析 + seed 纪律 assert PASS。

### 4. 共享 runner + 3 个 Probe（TDD-ish：先 smoke 再全量）

`probe_shared.py`（共享基础设施：make_realization/eval_window/metrics/run_cma_anchor/mmse_equalize_oracle/reconstruct_jones/bootstrap_ci/source_closure_hashes）。
路径深度修正（本 batch 比 hybrid-routing-scout-v1 浅一级，REPO_ROOT=parents[6] 非 parents[7]）。用系统 python 3.11.9（torch venv 无 pydantic）。

三个 Probe runner：
- `run_f1a_model_prior.py`：model-prior oracle headroom + receiver-visible observability 相关性
- `run_f3a_history.py`：因果历史条件互信息 + 预测 R² 增量
- `run_f4a_soft_gmi.py`：corrected per-symbol σ² soft/GMI oracle（修正 C12 scale-artifact）

### 5. Probe 结果

| Probe | verdict | 关键数字 |
|---|---|---|
| F1-A model prior | **PASS**（headroom+observability） | headroom 0.1329（CI [+0.078,+0.196]），obs \|r\|=0.651 |
| F3-A history | **PASS**（conditional info） | MI +0.060 bits，R² +0.036 |
| F4-A decoder-soft | **BOUNDARY**（thin+fragile+blocked） | analytic GMI +0.0089（smoothing-fragile），histogram −0.021（scale-invariant 复现 C12 artifact） |

**F4-A 关键方法论发现**：初版用 histogram-MI GMI 得 −0.021（scale-invariant，复现 C12 artifact）。主线诊断发现 histogram-MI 对所有 LLR 的公度缩放不变（用 analytic GMI 验证：c=0.5/1/2/10 时 analytic 变化而 histogram 不变）。改用 analytic GMI（scale-sensitive 真上界）作 primary，verdict 改为 BOUNDARY。这是 verifier 会攻击的核心点，已用 scale-invariance smoke test 锁定。

### 6. 10/10 identity/smoke gate PASS

`test_probe_identity.py`：seed 纪律 / F1-A 无 eval-truth 泄漏 / 常数输出 / paired realization / F3-A causal-prefix 不变性 + 无未来样本 / F4-A histogram scale-invariant + analytic scale-sensitive + oracle 读 truth / source-closure hash。

### 7. 独立 verifier V009 CONFIRM（P6 separation）

9 项 adversarial check：8 PASS + 1 PARTIAL；0 P0；1 P1（F4-A smoothing 敏感性已写入 result.json）。headline 数字独立重算 bit-identical。

### 8. 统一排序 + 投资选择

`synthesis.v1.md`：F1-B（model-based tracker）首选（headroom 上界 0.133 + obs 0.65 + 主结果潜力），但需 ~1 天基建 → 依提示词 §六**不直接建**，交用户决策 A/B/C/D。

## 决策引用

- D020：信息来源组合级 Probe 结果；F1-A/F3-A PASS，F4-A BOUNDARY；授权考虑 F1-B Scout（新建）
- V009：独立 verifier CONFIRM（新建）
- D019/H012：前置（D020 执行其 next_action）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。信息来源组合级 Probe 是 D019/H012 明确授权的 next_action；未触碰"明确不含"（不改 protected history、不自动晋级、不 push、不复活 blind-router/pilot-Jones/C12-global-σ²/C16）。
- 专题膨胀：本专题现 12 个 S###（S012 新建，为本轮唯一新增）；仍 < 15 阈值。

## 后续

- **交用户决策 F1-B 投资选择**（A 推荐 / B F3-B 次组件 / C F2 撞车核查 / D thesis pivot）。
- 用户选 A 后：建 dual-pol GG/SOP model-based tracker（KF/EKF on Jones）→ MMSE，公平对比 fixed-μ CMA + blind_affine_compare_16qam；oracle 只作 Kill。
- F2 pilot 若进：必须先做撞车核查（JLT2023/OE2021/LCOMM2026/TCOM2025/JLT2022-23）。
- F4-B 若进：必须先建 coded chain（INFRASTRUCTURE_BLOCKED）+ 解决 smoothing-window 依赖。
