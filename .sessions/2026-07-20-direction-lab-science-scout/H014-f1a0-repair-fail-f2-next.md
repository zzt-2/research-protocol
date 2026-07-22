# Handoff: F1-A0 严格因果修复 Probe FAILED；F1-B tracker 不授权；转 F2 collision check 待用户裁决

> 来源: S013 | 交接目标: 用户裁决 F2 collision check vs harvest 收尾 vs 重测 F1 家族
> 日期: 2026-07-22
> 文件名: H014-f1a0-repair-fail-f2-next.md

## 到哪了（状态）

S013 执行了用户提示词 §一-§九的确定性纠偏 + F1-A0 严格因果修复 Probe。

**纠偏（D021/V010）**：S012/D020/H013 对 F1-A 的科学语义解读被源码级审计撤回。F1-A 的 0.133 macro PI-SER gap 正确分类为 `PRIVILEGED_CSI_PLUS_TX_CALIBRATION_GENIE_GAP`（真 h/θ Jones inverse + TX-truth LS calibration 两路 privileged 叠加，`probe_shared.py:136-175 mmse_equalize_oracle` L148+L168），不是 "per-block MMSE" 或 "纯 model-prior headroom"。11 项审计缺口逐条 `file:line` 定位（见 D021 §理由）：observability 特征读全流 trace 含未来 block / target 是事后 headroom 残差 / F3 是 marginal-MI max-difference 非 conditional MI / blind_affine 从未调用 / F1 未存 fixed-label + 无 raw rows / F1·F3 artifact 的 F4 source hash 与当前源码不一致 / V009 未审科学层 / STATUS.v1.md 在 bf620b3 实际 +9/-4 diff（与 "protected unchanged" 矛盾）/ canonical·project.v1 ownership 冲突未解。D020 不删不改（amends 非 replaces），原始数值保留。

**F1-A0 修复 Probe（`repair-f1a0/`）FAIL**：在 11 cells × test seeds [161-170] = 110 raw rows（141-150 已被 D020 观察禁作 final test）上，严格因果 prefix 特征（index<cut）+ frozen ridge-linear probe（val[151-155] 拟合，test 冻结）预测下一 block h/θ/Jones。结果：**g0 FAIL**——ridge 旋转预测无增量（plugin 0.1685 vs nopred control 0.1683，8 help/13 hurt/89 tie，binomial p≈0.38，不可区分于 coin flip）。E1 CSI-only(0.1681) ≈ E3 privileged(0.1787) ≈ causal_plugin(0.1685) ≈ nopred(0.1683) 全塌缩。15/15 failing-first tests PASS。独立 critic（V011）+ 主线独立复核：**FAIL 存活但原因是物理+已知债非"model-prior 无价值"**——SOP rotation 在 256-symbol eval window 仅 0.06°（预测任务近空 by atlas construction）+ CMA μ=0.03 调债（μ=0.01→0.083 vs μ=0.03→0.369，D005/D007 已 flag，0/110 diverged）。critic 2 子结论 OVERTURNED：(a) blind_affine 跑在 CMA 损坏 z-stream（raw-stream≈0.0000 vs CMA-fed≈0.83）→ g1/g2 失效；(b) E2 budgeted pilot 实现破损（pilot 接收端合成、信道从未发送，E2=0.76 是噪声放大）。

**最终诚实裁决**：**F1-B tracker 不授权（证据不足）；不建一天基建；转 F2 collision check**（提示词 §七 on_fail）。但非普适"model-prior 无价值"结论——若重测须先换 high-SOP-rate atlas + μ-tuned CMA + raw-stream blind_affine + 真 persistence/AR(1) baseline。未改 protected history / STATUS.v1.md / canonical-state；无 push。

## 下一步干什么

**第一件事：用户在 F2 / 收尾 / 重测 F1 三选项中裁决**（见下方决策表）。若选 F2，新对话续接：先做 pilot 家族文献撞车核查（JLT2023 / OE2021 / LCOMM2026 / TCOMM2025 / JLT2022-23），确认不撞 D006/p03 COLLISION 后再跑 F2-A overhead 曲线 Probe（子 agent 文献 + 子 agent Probe）。

## 决策表（交用户）

| 选项 | 内容 | 成本 | 风险 | 预期产出 |
|---|---|---|---|---|
| **A（推荐）** | F2 pilot 撞车核查 + F2-A overhead 曲线 | ~半天（子 agent 文献 + Probe）| 高（JLT2023/OE2021/... 很可能撞车）| 若不撞车则 pilot 家族 headroom Probe；撞车则负面材料 |
| B | harvest / 负面边界论文 pivot（放弃正面方法）| 0 | 低 | 负面材料：CMA μ 调债 + rotation-近空使信息源 Probe 无法分离 + scale-artifact 教训 |
| C | 重测 F1 家族（须先换 testbed）| ~1 天+ | 中 | 须先建 high-SOP-rate atlas + μ-tuned CMA + raw-stream blind_affine + persistence/AR(1) baseline；可能仍 FAIL |
| D | 暂停 Scout，回体系专题（Direction Lab skill/恢复结构优化）| 0 | 低 | 框架加固 |

## 纪律（和下一步直接相关）

- 不复活 D018 blind-expert router、p03 pilot→Jones→inverse、C12 全局-σ² oracle、C16 非-FIR HOS。
- F1-A0 FAIL 不等于"model-prior/CSI/TX-truth 无价值"普适结论——主导 confound 是 rotation 0.06° + CMA μ 债。
- oracle（F1-A 0.133 / E3 0.179）只作 Kill/headroom bound，不作 Go 判据（FR-25）。
- F2 pilot 进前必须先撞车核查（D006/p03 COLLISION）。
- 不把 MDE=0.005 / 0.03 称通信可用阈值；资源决策阈值≠通信可用阈值。
- 不改 STATUS.v1.md（protected，矛盾仅记录）；不静默改 canonical/project.v1 ownership 冲突。

## 旧结论哪些被纠正

- "per-block MMSE headroom" → oracle affine scoring-only bound（含 TX-truth calibration）。
- "F1 observability PASS / 双门 PASS" → INVALIDATED（特征含未来 block，target 是事后残差）。
- "F3 conditional-MI PASS" → INVALIDATED（marginal-MI max-difference）。
- "F4 true upper bound / family boundary" → PARTIAL（smoothing-fragile）。
- "ML 存在真实信息增量 / 第一个合法正面候选 / 授权一天基建" → 全撤回。
- D020 原始数值（0.133 headroom、|r|=0.65、+0.060 MI、+0.036 R²）保留作历史，不删。

## 接口变更（如有代码改动）

无跨模块接口变更。新增 `repair-f1a0/`（contract + src/{repair_shared,run_f1a0_causal}.py + tests + artifacts + scientific-critic-report）为独立 Probe 子目录，复用 `probe_shared.py` 的 channel/evaluator 路径模式但独立 import。

## 失败数据附录（F1-A0）

| 方法 | macro PI-SER | CI[lo,hi] | fixed_label_ser | 备注 |
|---|---|---|---|---|
| CMA μ=0.03 (E0) | 0.3613 | [0.297,0.445] | =pi_ser | 公平传统 comparator |
| blind_affine (CMA-fed) | 0.3556 | [0.284,0.449] | =pi_ser | critic L1：被 CMA 污染（raw-stream≈0.0000）|
| E1 CSI-only | 0.1681 | [0.072,0.278] | =pi_ser | 纯 CSI genie，无 TX-truth |
| E2 budgeted pilot (32) | 0.7629 | [0.755,0.772] | =pi_ser | critic L2：实现破损（pilot 从未发送）|
| E3 privileged (CSI+TX-truth) | 0.1787 | [0.076,0.297] | =pi_ser | 旧 F1-A genie，仅归因 |
| causal_plugin (候选) | 0.1685 | [0.073,0.278] | =pi_ser | ≈ E1 ≈ nopred |
| causal_plugin_nopred | 0.1683 | [0.073,0.278] | =pi_ser | g0 control |

- g0：plugin-nopred diff +0.00025；8 help / 13 hurt / 89 tie；binomial p≈0.38。
- μ-sweep（snr15-short, seeds161-163）：μ=0.003→0.159 / μ=0.01→0.083 / μ=0.03→0.369 / μ=0.05→0.577。
- SOP rotation 256-symbol window：0.06°（sop_rate=4e-6）。
- 0/110 rows diverged（max cma_pi_ser=0.930 < RANDOM_CEILING 0.9375）。

## 已知债务（原则与现实差距）

| 债务 | 原则 | 当前状态 | 触发解决条件 |
|------|------|---------|-------------|
| STATUS.v1.md "protected unchanged" vs bf620b3 +9/-4 diff | protected history 不可改 | 矛盾记录在 D021 gap #10，未改 | 主控裁决（是否回退 diff 或承认 STATUS 非 protected）|
| canonical/project.v1 vs SCIENCE_SCOUT projection ownership | 单一 controller | 冲突未解，D021 gap #11 | 主控裁决 ownership |
| F1-A0 artifact 未存 ridge 权重+prefix features+per-sample h/θ | raw rows 可重算 | V011 标记，g0/0.06° 部分依赖模型推导非数据 | 下一 Probe 补 raw-rows 字段 |
| blind_affine comparator 跑在 CMA 输出 | 公平 comparator | critic L1 OVERTURNED g1/g2 | 重测须 raw-stream blind_affine |
| F1-A0 无真 persistence/AR(1) baseline | g1 须对 no-information baseline | g1 用 blind_affine 代理（双污染）| 重测补 persistence/AR(1) |

## 验证阈值（验证体系）

| 验证项 | PASS 标准 | 阈值来源 | 历史通过率 |
|--------|----------|---------|-----------|
| F1-A0 failing-first tests（15 项）| 全 PASS | repair-f1a0/probe-contract.v1.yaml | 15/15（本轮）|
| g0 prediction 增量 | plugin<nopred 显著（binomial p<0.05）| 提示词 §七 g1 | FAIL（p≈0.38）|
| g1/g2 vs comparator | 优于 fixed-CMA + blind_affine | 提示词 §七 g2 | confounded（critic L1）|
| g6 PI vs fixed-label 不反转 | 两 metric 结论一致 | 提示词 §七 g6 | vacuous（bit-identical）|
| source-closure hash 闭包 | 全 src MATCH | D021 gap #8 | 2/2 src MATCH（本轮）；旧 F1-A/F3 artifact 的 F4 hash 仍 DIFFER |
| raw rows 重算 aggregate | diff=0 | D021 gap #7 | cma macro diff 0.00e+00 |

## 用户/advisor voice（关键指令，verbatim）

- "不把现有 0.133 gap 继续称为 per-block MMSE 或纯 model-prior headroom；不把 |r|=0.65 称为 channel-state observability。"
- "旧记录必须保留；用 superseded/corrected/partial 等状态形成血缘，不重写历史为'从未发生'。"
- "如果 FAIL：不实现 tracker；将 F1-B 标为当前证据不足；下一建议改为 F2 collision check。"
- "如果 PASS：仍然不要实现 tracker；只报告投资依据、预计基建和风险，等待主控授权。"
- "验证必须分两种角色：integrity verifier + scientific critic。两者都要形成独立、可定位的报告文件。"
- "不再修改 campaign contract 中声明 protected 的 STATUS.v1.md；不静默修改 project.v1.yaml/STATUS 的 controller ownership 冲突，只记录并报告。"
（完整原话见 `voice.md` 2026-07-22 S013 段。）

## 必读（不超过 8 个）

1. `.sessions/2026-07-20-direction-lab-science-scout/topic-index.md`（不变量 + 当前位置 + D021/S013 结论）
2. 本文件 `H014-f1a0-repair-fail-f2-next.md`
3. `.sessions/2026-07-20-direction-lab-science-scout/decisions.md` 的 D021（含 F1-A0 精化措辞）+ V010 + V011
4. `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/repair-f1a0/scientific-critic-report.md`（V011 critic 5 攻击）
5. `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/repair-f1a0/artifacts/F1-A0-result.v1.json`（110 raw rows + 7 method dual metric）
6. `projects/thesis-fso/direction-lab/scout/info-source-portfolio-probe/synthesis.v1.md`（末尾 AMENDMENT 段）
7. `projects/thesis-fso/direction-lab/portfolio/current.yaml`（F1 RETRACTED / F2 NEXT 状态）
8. `projects/thesis-fso/direction-lab/STATUS.v1.md`（protected，不改；矛盾见 D021 gap #10）

## 接收方验证（续接对话时必须完成）

- [ ] 已读取 topic-index 的不变量段落。
- [ ] 已验证至少 3 条关键事实：
  - F1-A0 g0 FAIL：plugin 0.1685 vs nopred 0.1683，binomial p≈0.38 → 从 `F1-A0-result.v1.json:raw_rows` 重算；
  - CMA μ 债：μ=0.01→0.083 vs μ=0.03→0.369 → 重跑 μ-sweep（`repair_shared` + `atlas_runner.standard_cma_godard_with_z`）；
  - F1-A 重分类：`probe_shared.py:mmse_equalize_oracle` L148 + L168 同时用 true h/θ + TX-truth LS → 读源码确认。
- [ ] 已检查 `_registry.yaml` 的 depends_on/conflicts_with。
- [ ] 已确认当前范围不含 formal promotion、push、protected history 改动、blind-router/pilot-Jones/C12/C16 复活、tracker 实现。

## git 状态

- worktree: `D:/code/study/research-protocol/.worktrees/direction-lab-capability-atlas`
- branch: `codex/direction-lab-capability-atlas`
- 本轮 consolidated commit 待提交（不 push）。接收时以 `git log -1` 核验实际 SHA。

## 下一轮

用户裁决 F2 / 收尾 / 重测 F1 / 暂停回体系。若 F2：先子 agent 文献撞车核查（JLT2023/OE2021/LCOMM2026/TCOMM2025/JLT2022-23），不撞车后跑 F2-A overhead Probe。
