# P06 — E_CAUSAL_CROSS_FRAME_HISTORY_INFORMATION（冻结合同）

> 2026-07-31 | campaign 6/10 candidate | family E（首包）| 状态: FROZEN-before-execution
> 来源: 绑定裁决 D044（撤回旧 P06 window/complexity 入口）；修复旧 F3-A 科学无效性
> 旧 F3-A 无效性: `run_f3a_history.py:195-196` 把 `max(history_mi) - max(block0_mi)`（两个不同特征集上的边际 MI 最大值之差）当成 conditional MI；`state/current.yaml:161-170` / `portfolio/current.yaml:173-181` 已标 `INVALIDATED_AS_CONDITIONAL_MI`。

## 0. 一次性修复型 PROBLEM_BEARING_PROBE（性质冻结）

- 本包**只**修复旧 F3-A 的科学无效性，用严格因果的 held-out 预测增量取代错误的"conditional MI"声明。
- **不继承**旧数值 +0.060 bits 或 +0.036 R²（仅作历史保留）。
- 本轮失败后关闭 E 族，**不允许再开第二个 evaluator-repair 包**。
- 主判据 = held-out 预测增量（MAE/RMSE/R² 增量 + log-loss/Brier/校准），**不报告 MI**（旧 F3-A 的 MI 路径已被否决，原则不再把边际 MI 差称 conditional MI）。

## 1. 冻结问题定义（M-C-A，读任何测试数据前冻结）

**M（冻结的传统可部署接收机）**：`standard_cma_godard_with_z`（`cb1_cell_runner.py:49`，mu=0.03、n_tap=11、R2=1.32、block_size=64，Godard-with-z 梯度 `Δw ∝ (R²-|z|²)·z·r*`）。冻结权重/步长不变；只利用当前帧可见摘要判断下一帧风险。

**C（来源闭合的时间相关 GG 动态）**：按真实 `ρ = exp(-Δt/τ_c)` 生成多帧 trajectory。`τ_c = 1/(2π·f_G)`（Conan 1995），`Δt = frame·t_s`。覆盖**数个 f_G** ∈ {30, 100, 1000} Hz（→ τ_c ≈ 5.3ms / 1.59ms / 0.159ms），不得通过人为加快符号级动态制造问题。强湍流 (α,β) = (4.2,1.4)（provenance = 当前 params.py `TurbulenceParams.turb_strong_*` 真值，Al-Habash plane-wave 闭式，σ_R²=3.5）。

**A（待验证的因果增量）**：过去若干帧的 receiver-visible 状态，**可能**在当前帧摘要 / last-value persistence / EWMA / AR(1) 之外，对下一帧冻结接收机的失效或性能提供严格因果增量。

**预测对齐（强制）**：
- `features(t) = 仅使用 frame ≤ t 的接收机可见量`
- `target(t+1) = 冻结接收机在下一帧的性能/失效`
- 禁止把 h、α/β truth、未来 trace、TX label、seed/cell ID 或 target-frame 事后残差作为特征。

## 2. Frame-level 抽象（物理门控核心）

**物理约束（Phase 0 必须验证）**：在 GG 块步长（block=100 sym → Δt=4e-8s）和 CMA 块步长（64 sym → 2.56e-8s）下，ρ > 0.9997（即便 f_G=1000Hz）。信道在块步长上**准静态**，跨块历史携带的可分辨时间信息极小。

**因此 frame 必须是一个聚合窗口，其持续时间是 τ_c 的不可忽略分数**，而非 64/100 符号块（那是准静态帧，跨帧 ρ≈1 无时间动力学）。frame-level 抽象避免显式模拟约 4 万 symbol-block/τ_c：
- 每个 frame = 一个固定符号数的接收机可观测聚合窗口。
- frame stride Δt_frame 选择使 ρ_frame = exp(-Δt_frame/τ_c) 跨所选 f_G 覆盖有意义范围（不人为加快、不人为放慢）。
- 接收机在每帧上产出冻结可见摘要（cm_error / output_power / update_norm / w_norm / z_amp_max 的帧聚合统计 + 冻结接收机在该帧的 fixed-label SER 失效标签）。

## 3. Phase 0：物理与身份门（读测试前冻结）

frame-level GG state transition（复用 `_gg_time.py` 的 AR(1)，块级 `gg_time_envelope_blockwise`，不显式逐符号模拟）。必须验证四项，任一失败 → `EXECUTION_INVALID`（不计 P06，不进后续阶段）：
1. **GG 边缘分布**：frame-aggregated envelope 的边缘匹配 Gamma-Gamma(α,β) 理论 PDF（`gg_pdf_theory`，KS 统计量）。
2. **指定 lag 的经验 ACF**：经验 ACF[lag] 与理论 ρ^lag 一致。
3. **ρ 与 exp(-Δt/τ_c) 一致**：frame stride 对应 ρ 与解析公式一致。
4. **frozen receiver 单帧结果身份一致**：frame-level 抽象下的冻结 CMA 单帧 fixed-label SER 与原 runner（`standard_cma_godard_with_z` + `evaluate_dual_16qam`）在共享 realization 下身份一致（state_hash byte-identical 或数值相对误差 < 1e-12）。

## 4. Phase A：问题与严格因果信息门

冻结一个已完成的传统接收机（standard-CMA）和明确的下一帧连续性能目标（frame fixed-label SER）+ failure-event 二值目标（frame fixed-label SER > 冻结阈值）。选择只在 dev 完成，test 后不得换目标。

**传统预测 baselines（至少 5 个）**：
1. unconditional prior（训练集均值）
2. last-value persistence（上一帧摘要直接当预测）
3. EWMA（指数加权移动平均，dev 调衰减）
4. AR(1)（当前帧摘要一阶自回归，dev 调系数）
5. current-only ridge/logistic（仅用 frame t 摘要）

**history-expanded 模型（简单、冻结、可解释）**：带过去 K 帧摘要的 ridge/logistic（本轮**禁止深度网络**）。K 与正则化在 dev 调。

**纪律**：
- trajectory-level train/dev/test split（按 trajectory 分，非按 frame 混分——防同一 trajectory 的帧跨 split 泄漏）。
- fresh seed/trajectory ledger，与历史测试 seed（141-150、131-135、30-49 等）隔离。
- 同 trajectory paired comparison（history vs current-only 在同一帧上配对差值）。
- nested/dev-only 调参；test trajectory bootstrap CI。
- 连续目标报 MAE/RMSE/R² 增量；failure 目标报 log-loss、Brier、校准（reliability）。
- **MDE 与事件数下限在读 test 前冻结**。
- 保存逐 trajectory、逐 frame raw rows。
- **不允许把边际 MI 差称 conditional MI**。本轮原则上不报告 MI。

**Phase A 终态（三选一）**：
- 物理条件下有效 failure event 不足 → `PROBLEM_ABSENT_AT_PHYSICAL_TIMESCALE`（有效 P06 计 6/10，不产 METHOD_SIGNAL）
- history-expanded 未稳定超最强 current-only/persistence baseline，或 CI 跨零 / MDE 未过 → `NO_CAUSAL_HISTORY_INCREMENT`（有效 P06 计 6/10，不产 METHOD_SIGNAL）
- 严格因果增量通过 → `CAUSAL_HISTORY_INFORMATION_SIGNAL`，进 Phase B

## 5. Phase B：行动可达性门（仅 Phase A 通过才运行）

先盘点现有代码是否已有 ≥2 个：receiver-visible / 非特权 / 任务匹配 / 可在下一帧执行 / 性能-开销互补 的合法动作（如已有 continue/reset、两种冻结传统模式、safe fallback）。

**禁止**为接上信息信号凭空制造动作；禁止 TX-truth action；禁止重开 DA/NDA selector、Pilot-Jones、P05 ButterflyCNN finetune、CB1 collapse 家族。

若没有现成动作或只需超过"小适配"基础设施 → `INFORMATION_INCREMENT_WITHOUT_ACTIONABLE_CONTROL`（只 harvest observability boundary，不形成方法）。

## 6. Phase C：条件式方法构造（仅 Phase A 通过 + Phase B 存在合法动作才运行）

至少比较：fixed action / persistence threshold / EWMA·AR(1) threshold / current-only policy / history-expanded causal policy / 一个简单 hysteresis-safety gate。相同 trajectory、相同信息、相同动作预算下配对。优先检查便宜传统 temporal policy 是否已解决。

**终态四选一**（唯一）：
- `PROBLEM_RESOLVED_BY_CONVENTIONAL_TEMPORAL_POLICY`
- `NO_DIAGNOSTIC_METHOD_SIGNAL`
- `DIAGNOSTIC_METHOD_SIGNAL`（仅当 history policy 在 fresh test 上超最强传统 temporal comparator、达冻结 MDE、CI 不跨零、无更便宜等价解释；即使通过也只是 pre-formal carrier，不得直接写论文主方法，后续须走 GW Step 3/3.5/4a）
- `EXECUTION_INVALID`

## 7. Seed 纪律（fresh ledger，与历史隔离）

- 历史已用 seed（禁用）：11-50、61-130、131-150（F-Probe）、30-49（P01-P04 held-out）、50-59（P02 dev）、60-99（P02 held-out/P03 held-out/P04）。
- P06 fresh ledger（本包冻结）：train trajectory seeds 200-214（15/condition）、dev trajectory seeds 215-224（10/condition）、test trajectory seeds 225-239（15/condition）。全 disjoint 历史。每 trajectory 独立 seed 生成独立 GG trajectory。
- 共 6 conditions × 40 trajectories = 240 trajectories，每 2.8M symbols → 20 frames/traj = 4800 frames（去前 3 历史 warmup 后有效 ~4080 frames）。

## 7.1 Frame-level 设计（rho 覆盖，物理诚实）

- `frame_symbols = 140_000`（dt = 56µs）。`n_symbols = 2_800_000`（20 frames/traj）。`eval_symbols_per_frame = 8000`（连续窗口，SER 稳定）。
- ρ_frame 跨 f_G：fg=30Hz→0.9895（准静态）、fg=100Hz→0.9654（近静态）、fg=1000Hz→0.7034（**丰富跨帧动力学**）。
- **物理诚实**：不人为加快符号级动态。fg=30/100 准静态是源闭合物理（tau_c=5.3/1.59ms ≫ 帧间隔 56µs），fg=1000 是大气 Greenwood 频率上界。问题只在 fg=1000 有非平凡跨帧动力学——这正是要测的。
- dev scan 确认 fail 事件率：fg=1000 snr=15 → ~63% frames fail（rich regime）；snr=20 → ~15%（rare-event regime）。

## 8. verdict 唯一性

- Phase 0 任一失败 → `EXECUTION_INVALID`（不进 A）。
- Phase 0 通过 → Phase A 三态唯一。
- Phase A `CAUSAL_HISTORY_INFORMATION_SIGNAL` → Phase B（二态：control available / not）。
- Phase A signal + Phase B 有合法动作 → Phase C 四态唯一。
- Phase A signal + Phase B 无合法动作 → `INFORMATION_INCREMENT_WITHOUT_ACTIONABLE_CONTROL`。
- Phase A 非 signal（两态）→ 直接终止，不进 B/C。
