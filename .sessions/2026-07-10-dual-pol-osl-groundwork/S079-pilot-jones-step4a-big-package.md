# [S079] Pilot-Jones Step 4a 大包（A0→A′→A/B→D）— 门控 KILL

> 2026-07-23 | 阶段：formal GW Step 4a（D062 带债豁免大包） | 状态：provisional KILL，待主控验收+用户确认
> 来源：T002 / D062 | 关联：S074（续接）/ V036 / H017

## 目标

在一个对话内完成 Pilot-Jones 的 GW Step 4a 大包（A0→A′→A/B→D），关闭"它是否存在结构性方法增量并值得继续"这一科学不确定性。包内按前置门通过则同包直接运行有界 MVE；不停在纯分析或"建议下一轮实验"。

## 记录

### 输入与授权（D062 继承核验）

- D062 debt-waiver 正确继承：Step 3.5 维持 `WAIVED_TO_STEP4A_WITH_BLOCKING_DEBT`（非 PASS）；4 篇 D056 直接竞品（TCOMM2024/JLT2025/JLT2022/JLT2023）全程 `BLOCKED_NO_FULLTEXT`，未冒充已读。
- task-control `validate_task_control.py T002` → PASS（epoch 4，action PILOT_JONES_STEP4A_PACKAGE）。
- 正面 ceiling 最高 `CONDITIONAL_GO_WITH_BLOCKING_LITERATURE_DEBT`；主对手 = 传统 block/frame pilot Jones inversion（B2 族）；oracle 仅上界/Kill 工具（FR-25）。

### Source closure（最小闭包，自包含于当前分支）

- 只读 source worktree `unified-batch-runner` 未修改；7 个预期 SHA 全 MATCH。
- **已知 provenance 断裂记录**：历史 JSON `pilot_6p_ema09_full24` 声称 `batch1_fade_methods.py` SHA `09b1fe2d…`，磁盘唯一文件为 `d8e280…` → 不可 exact replay → 历史 15/15 仅作 diagnostic prior，非新 MVE 结果非 Go 证据（T002 rule 5 + FR-26）。且 15/15 是 pilot-assisted-vs-blind(CMA) 比较，非 pilot-inversion 方法间比较。
- 新最小闭包建于本 worktree：source-closure.yaml / metrics.py（重实现 fixed/PI BER）/ pilot_jones_methods.py（B0/B1/B2/P/O + standard Godard-z CMA core，z 因子核验）/ run_pilot_jones_mve.py（paired-realization runner）/ mve-contract.yaml / test_pilot_jones_step4a.py（10 directed tests）/ result.json。
- **已知简化记录**：信道 2×2 极化混合为 **real rotation**（theta=sop_rate·arange(N)，矩阵 [[c,s],[-s,c]]）→ 条件数恒为 1。此简化不偏 P-vs-B2（各臂共享）但 bound claim ceiling。

### Step 4a A0（§0 + §1 六项致命）

- §0 四判据形式全 PASS（M-C-A 完整；可复用产出；近期 baseline OE2021/LCOMM2026 全文 + 4 篇 BLOCKED；可量化对标）。判据 2/3 不靠"OSL 没人做过"。
- §1 六项致命检查 **两项致命成立**：
  1. **无结构性能差距**：B0→oracle 差距被单一固定 EMA 参数完全吸收（B1 EMA09≈oracle，多 seed bit-equal）。
  2. **FR-01 先验覆盖致命**：固定 EMA09 把主指标覆盖到 oracle；B2a tikhonov 比 B0 更差（给良态矩阵加偏置）；B2b condition_guard 与 B0 逐位相同（从不触发）。
- A0 §2-5 支持：receiver-visible 信息存在但无信号可作用（cond~O(1)）；竞品沉默与"无 OSL 专属结构失效可修"一致；结构原因是良态 pilot-LS 问题里固定平滑器已达天花板。
- semantic smoke（noiseless Jones recovery / 病态 / deep-fade / clean / causality / fixed-label-PI signature）全确认。信道从不产生病态（cond p50=1.10/p95=1.26/max=1.68 strong；deep-turb probe p95=1.38）。

### A′ / A / B + 方法候选

- A′ 六竞争维度：全部要么被简单 baseline 饱和（per-block 方差→B1；temporal lag→B1），要么结构缺席（conditioning cond~1；deep-fade 奇异性 h<0.1 frac=0）。无方法可竞争维度。
- 3 个机制不同候选（非超参变体）：B1 固定 EMA09（参考）/ B2a tikhonov + B2b cond_guard（最强廉价替代）/ P uncertainty-aware temporal tracker（per-block α(cond,innov) trust/memory，提出）。
- 每候选答 4 问（只是 EMA 换参？需 truth？解释 deep-fade vs mismatch？最强 reviewer 反对？）。
- **选定最强提出方法 = P**。结果：P **不赢 B1**（hard 条件 10-seed：0/10 P<B1，6/10 tie，4/10 B1<P）。α 在本信道退化为 ≈0.9 固定（cond/innov 平）。无一候选结构上胜过 fixed EMA/regularized LS → 按 T002 §5.2 必须 Kill，不跑性能 MVE。

### 冻结 MVE contract + Oracle/headroom 门（FR-21）

- mve-contract.yaml 冻结（SHA 见 result.json contract_sha256）：question/hypothesis/falsifier、method equations、information access、state lifecycle、metric signature、canonical generator、shared-realization rule、baseline ladder、parameter sources（FR-20，对抗 deep-turb 标 UNVERIFIED_RANGE）、observed-seed exclusion（41-48）、fresh val/test seeds（2000-2004/3000-3009，disjoint）、cells、pre-registered pass/fail thresholds、oracle/headroom gate、time budget、stop conditions、FR-11 architecture summary。
- 预注册阈值（非事后）：Go = P 赢 B2 paired ≥8/10 + p<0.05；Kill = falsifier (a) cond~O(1)/(b) B1→oracle headroom 可忽略/(c) P 不赢 B2。
- **B1→oracle headroom 可忽略**：strong 条件 B1 多 seed 与 oracle bit-equal；hard 对抗（α=2.0,β=1.0,17dB，MAXIMIZE P headroom）B1 均值 5.31e-3 vs oracle 4.47e-3（预注册 headroom B1/O=1.19，即 B1 比 oracle 差 19%；亚一个数量级；多 seed bit-equal）。预注册 FR-21 kill（B1 在 oracle 2x 内）**触发**。oracle 仅上界/Kill 工具，非 Go 对手（FR-25）。

### MVE 执行 — 未运行（门控 Kill by design）

- 正式 90-cell 性能 MVE **未运行**，门控 Kill 的设计结果而非缺件（T002 rule 4）。两条独立 Kill 门在 semantic-smoke + bounded headroom 阶段同时触发：(1) A0 §1 致命 + FR-01 先验覆盖致命；(2) FR-21 headroom Kill。
- 失效**结构性**（cond~1 信道 + B1==oracle）非统计性——full MVE 不会改变裁决。bounded 10-seed 对抗 probe（result.json bounded_headroom_probe_rows）已给足够精度 headroom 数字。
- paired-realization（每 cell+seed 一实现，各臂共享）；raw rows 存档；每 row 带 config/source/contract SHA、realization fingerprint、information class、denominator。

### 双审查（P6 分离，独立子 agent）

- **Integrity verifier（V036）= PASS**：11 项结构性检查全 PASS（task-control/YAML-parse/tests 10 passed/6 source SHA/contract SHA/raw→aggregate/seeds disjoint/info-boundary 静态+运行/protected 4 SHA/no-fabrication/git diff --check）。唯一记录分歧（headroom 公式 + contract stale 引用数字）为文档一致性非伪造，已修复：result.json 增 contract 预注册公式 B1/O=1.19，contract L199 stale-number 澄清并刷新 SHA。
- **Science critic（V036）= KILL_WITH_CAVEAT**：8 项攻击，KILL 在 real-rotation 信道内稳健（两条独立门、B1 闭合 oracle 天花板、oracle 用对、probe pro-P）。**唯一 rescue avenue 出包范围**：升级 canonical 信道为 complex Jones/PMD/PDL（implementer 自认 known_simplification）会重新引入真实 conditioning 变化——P 的机制轴。critic 明确：**不应把此 KILL 重构为杀"Pilot-Jones 方向"；它只杀 unitary-rotation 实例化**。

## 决策引用

- D062（带债豁免进 Step 4a 大包；本包 provisional verdict 不新建 D063，待主控/用户确认后再决定）。
- V036（integrity PASS + science KILL_WITH_CAVEAT，新建）。
- 无新 D###（provisional verdict 待用户确认）。

## 范围确认

- 本轮在 scope boundary 内：是。完成 A0/A′/A/B；D 未运行因前置致命门 + FR-21 headroom Kill（T002 rule 4 允许）。未进 Step 5/Contract/Execute；未复活 Scout/P03；未建 B004/Queue/Registry；未 push；未改 protected；未改 source worktree。

## 后续

- **Provisional verdict = KILL（待主控验收 + 用户确认，D062 rule 6）**。
- KILL **scope 明确**：限于 unitary real-rotation 信道实例化；**不重构为杀 Pilot-Jones 方向本身**。信道升级（complex Jones / PMD / PDL）+ 4 篇全文解除 BLOCKED 后可重评。
- 若用户接受 KILL：Pilot-Jones 方向回候选池（family 不关闭，同 P03 处置）；thesis-fso formal GW 工作线需另选方向。
- 若用户要求 salvage：唯一在范围内的 rescue = 升级 canonical 信道为带 PMD/PDL 的 complex Jones（出 T002 范围，需新 authorization）。
- 可复用沉淀（Kill 路径）：real-rotation OSL Jones 结构性良态论证（负面/边界材料）；B0/B1/B2/P/O ladder + paired runner + fixed/PI metrics + 10 directed tests；5-min pre-MVE 滤波器（cond-distribution + B1-vs-oracle headroom probe，泛化 FR-21）；排除"generic pilot→Jones→inverse + EMA/Tikhonov/cond-guard 稳定化"于 unitary real-rotation 信道。
