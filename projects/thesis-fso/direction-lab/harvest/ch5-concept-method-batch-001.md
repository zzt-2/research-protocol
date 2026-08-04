# Ch5 概念方法构造批次 001

> 2026-08-04 | 来源: T007 / S015 / D023 / CP004 | action_class: CONCEPT_METHOD_CONSTRUCTION
> 性质: design-only 概念原型卡。survivor 不是 METHOD_SIGNAL、不是 Go，不能进论文正文；
> 实验前必须回 GW Step 1–3/3.5/4a。无仿真、无代码、无检索、无科学 claim。
> 继承 T006（已修订为 `NO_CONSTRUCT_SURVIVES`）：候选源切换到 Ch5 部署/计算流程。

## 1. Terminal verdict

**`NO_CONSTRUCT_SURVIVES`**：5 张原型卡全部碰撞或被廉价替代吸收。

- **P1 跨模块升幂中间量复用**（FOE 的 `rx**M0` 复用给 CPE）→ 被最强廉价替代吸收（编译器/单
  算一次的 trivial DAG 重排；且 LMMSE 路径已存在幅度无关升幂 `rx/|rx| → **M0`，证明升幂表示
  本身已是可替换组件而非方法动作）。分类 `ENGINEERING_COMPONENT`。
- **P2 选择后驱动 h 估计**（lazy-h，只算被选分支的 h）→ 碰撞：与 route-B select-before-execute
  同执行合同（2B/T005，`branch_route_b`），且 route-B 的 timed kernel 已把
  `estimate_h_*_perblock` 计入被选分支成本；P2 是 route-B 的动作重命名，不产生独立 action
  delta。分类 `REJECT`（existing action collision）。
- **P3 升幂域幅度无关化 / 去乘法缩放**（LMMSE `rx/|rx|→**M0` 部署化）→ 被廉价替代吸收：LMMSE
  已实现该变体且 `#15` 论文复现失败（高 SNR BER floor，`_recovery.py:280-286` DEPRECATED）；
  幅度无关化是估计器内部数值表示，不是独立部署动作，且改估计器本体触发 `NDA_ML_BODY_REOPEN`
  禁令（D050）。分类 `REJECT`（dead-end collision + forbidden body reopen）。
- **P4 两阶段粗-细 CFO/相位计算预算**（adaptive FFT zero-pad / 分段预算）→ 碰撞：P09 early-stop
  BPS 同"计算预算自适应"动作签名已被 KILL（记账欺骗 + π/4 对称 B_used 恒定 + truth-resolved
  BER，`step-040-p10:32`），且 D050 证 NDA-ML closed-form 无可裁剪搜索结构，自适应 FFT 预算 =
  换估计器本体 = `NDA_ML_BODY_REOPEN`。分类 `REJECT`（dead-end collision + forbidden body
  reopen）。
- **P5 跨窗 CFO/相位缓存调度**（omega 缓存、块间状态复用）→ 碰撞：每窗独立 seed + 块常数
  i.i.d. h（`_channel.py:27-32` / `generate_shared_realization_apsk` 每窗新 seed），跨窗 CFO 无
  物理连续性可缓存；同 Ch4 C2 跨窗记忆 Gate 1 不过（物理自由度不存在）。P06 跨帧历史已 KILL
  （last-value R² 0.85 > causal-history R² 0.32）。分类 `REJECT`（物理前提不存在 + dead-end
  collision）。

筛选维度按 brief §3 五条：部署动作真实发生 / 相对已有贡献独立 action delta / 复杂度下降由真实
调用数定义 / 不被缓存/固定参数/编译器优化/CCISP action 吸收 / 能否形成完整一章 / 最小实现可在
现有资产完成。P1/P3 命中"被廉价替代吸收"，P2 命中"与 CCISP action 重复"，P4 命中"被既有 KILL
吸收 + 换估计器本体禁令"，P5 命中"物理前提不存在 + 既有 KILL"。无一张在五维上同时独立。

**下一批必须更换的候选源/研究对象**：当前接收链的部署/计算流程自由度已被 route-B 执行合同
（h 估计、分支选择、单支执行）、closed-form 估计器本体（不可重开）、每窗独立 seed（无跨窗
缓存物理前提）和既有 KILL（P09 early-stop、P06 跨帧、A1 adaptive-K、A 族 selector 鲁棒）共同
锁死。建议下一批把候选源切换到 **接收链之外或输入侧**（如发射侧 Tx-PMF 协同见 A9 recipe、或
AMC/rate control 见 2D 但需新 GW+授权），或更换研究对象到 **真实存在跨窗物理连续性的信道**
（如块间相关 GG / AR(1) 时间相关信道），否则 Ch5 在当前资产上无法产生独立于 route-B 的新部署
方法动作。

## 2. Current computation-action map

> 先画当前接收链的本地计算/数据流。以下基于权威 route-A caller
> (`simulator/run_ccisp_family1_selector_a_30seed.py`) 与 branch-routed caller
> (`explore/.../_a4_branchrouted_30seed.py`) 的逐行核对，所有 `[FACT]` 带本地指针。

每窗（256 sample）route-A 完整计算路径（`run_ccisp_family1_selector_a_30seed.py:36-43`）：

```
generate_shared_realization_apsk(seed=ws)  →  rx_raw, bits, tx, h, phi   [每窗独立 seed]
        │
        ├─ estimate_h_blind_perblock(raw, gl)  → hb          ┐ 两路 h 都算（route-A 盲算两路）
        ├─ estimate_h_pilot_perblock(raw, tx, gl) → hp       ┘
        ├─ mmse_equalize(raw, hb, gl); amp_limit(_, 3.0) → blind均衡信号
        ├─ mmse_equalize(raw, hp, gl); amp_limit(_, 3.0) → pilot均衡信号
        │
        ├─ per_block(blind, pilot, bits, tx):               ← A.per_block 同时跑两路 recovery
        │     ├─ NDA 路: fft_foe_m0_omega(blind, M0)        ← raised_1 = blind**M0  (sc_nda_ml_sim.py:150)
        │     │            → omega
        │     │            nda_ml_recovery(blind*exp(-jωk), M0, assume_df_zero=True)
        │     │              raised_2 = rx**M0              ← (_recovery.py:213)  [第二次升幂]
        │     │              → rc_nda
        │     ├─ DA 路:  da_ml_recovery(pilot, pidx, tx[pidx])
        │     │              → rc_da
        │     └─ resolve + demod → ne_nda, ne_da, ne_nda_common768
        │
        ├─ decide(raw, snr, gl)  → 'da' | 'nda'             ← CV gate + 13 dB gate (route-A: decide 与 per_block 并行无依赖)
        └─ 选 selected_rx = per_block_da(pilot) | per_block_nda(blind)  ← route-A 再取被选分支输出（990/990 identity）
```

branch-routed (route-B) 计算路径（`_a4_branchrouted_30seed.py:358-400`）：

```
generate_shared_realization_apsk(seed=ws)
        │
        ├─ decide(raw, snr, gl)  → 'da' | 'nda'             ← decide 提前到 recovery 前（route-B delta）
        └─ if 'da':  estimate_h_pilot_perblock; mmse_equalize; amp_limit
                     per_block_da → rc_da, selected_rx       ← 只算被选分支（含该分支的 h 估计）
           else:     estimate_h_blind_perblock; mmse_equalize; amp_limit
                     per_block_nda(blind) →
                       fft_foe_m0_omega(blind) → raised_1=blind**M0 (sim:150)
                       nda_ml_recovery(...)   → raised_2=rx**M0 (rec:213)
                       resolve + demod → selected_rx
```

**关键计算事实（供原型卡引用）**：

- `[FACT]` 升幂 `rx**M0` 在 NDA 路内计算两次：`fft_foe_m0_omega:150`（取 FFT 找频峰）+
  `nda_ml_recovery:213`（取 mean-angle 估 CPE）。两者用的是同一 `rx` 但做不同结构化归约（FFT vs
  mean-angle），且 `assume_df_zero=True` 时 FOE 分支被跳过（`_a4_switch_common768_30seed.py:122`），
  此时 `fft_foe_m0_omega` 仍被 route-A 的 `per_block` 调一次（`:120`）但 omega 经 exp 补偿后
  `nda_ml_recovery` 内 `assume_df_zero=True` 再算一次升幂仅取 mean-angle。
- `[FACT]` route-A 盲算两路 h（`hb` + `hp`，`:38`）；route-B 只算被选分支的 h（`:373/391`），
  且 route-B 的 timed kernel（`t_b0`..`t_branch_compute`，`:369/400`）已把被选分支的 h 估计 +
  均衡 + recovery + demod 全部计入 branch compute。即"lazy-h / 只算被选分支 h"是 route-B 的
  既有执行合同，不是新动作。
- `[FACT]` 每窗 `generate_shared_realization_apsk` 用新 seed（`run_ccisp_family1_selector_a_30seed.py:37`
  `seed=ws=start+b`，每窗递增）；信道 `h = gg_block` 块常数 i.i.d.（`_channel.py:27-32` `gg_block`
  按 `BLOCK` 分段，块间独立 `gamma_dist.rvs`）。
- `[FACT]` DA 路不调用 `fft_foe_m0_omega`（DA 用 `da_ml_recovery` 的 pilot 相位回归，无升幂 FFT）；
  升幂重复只在 NDA 路内。
- `[FACT]` LMMSE 估计器（`_recovery.py:276-379`）已实现幅度无关升幂：`rx_n = rx/|rx|`（`:360`）
  → `yM = rx_n**M0`（`:361`），与 NDA-ML 的 `raised = rx**M0`（`:213/243`）是不同的升幂表示。
  LMMSE 标 DEPRECATED（`:280-286`，`#15` 论文 PDF→md 丢公式致高 SNR BER floor，复现失败）。
- `[FACT]` `nda_ml_recovery` 是 closed-form（升幂 + mean-angle / 单正弦 FFT-ML），无 candidate
  枚举、无 objective 在候选集上求值（D050 源码逐行核，`.sessions/.../decisions.md:3024-3059`）。
  唯一 search 是竞争对手 BPS（`bps_cpr`，`_recovery.py:91-118`）。

## 3. Prototype cards

### Card P1 — Cross-Module Raised-Power Reuse (M0-domain fusion)

1. **章节槽位 / 方法名**：Ch5 候选；"Shared Raised-Power Compute Graph for NDA FOE+CPE"。
2. **M-C-A**：M = NDA 路（FOE + CPE 两步）；C = `rx**M0` 在同一路内被计算两次（FOE 取 FFT、
   CPE 取 mean-angle），是冗余乘幂；A = 构造联合计算图，升幂一次，FOE/CPE 共享中间量。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：NDA 路均衡后复信号 `blind`、M0=8。
   - 动作：`raised = blind**M0` 算一次 → FOE 取 `raised[:N_fft]` 的加窗 FFT 频峰；CPE 取
     `raised` 的 mean-angle（`assume_df_zero` 分支）或去频后的 mean-angle。
   - 输出：一条 256-sample NDA 校正复数序列（同既有输出契约）。
4. **算法流程**：
   1. 读均衡后 `blind`；
   2. `raised = blind ** M0`（算一次，存中间量）；
   3. FOE：`raised[:N_fft]` 加窗 → FFT → Quinn-Rife 插值 → omega；
   4. CPE：`raised` 经 `exp(-jωk)` 去频后 mean-angle（或 `assume_df_zero` 直取 mean-angle）→ phi；
   5. 补偿 `blind*exp(-j(omega·k + phi))`；
   6. 输出 256-sample 校正序列。
5. **相对 CCISP / inventory 的新增点**：相对 route-B NDA 路的"两次升幂"，改为 DAG 重排共享
   `raised` 中间量。
6. **传统 comparator / strongest cheap alternative**：
   - comparator：route-B NDA 路（两次升幂）。
   - strongest cheap alternative：**编译器/解释器级别的 trivial DAG 重排**（同一表达式
     `rx**M0` 出现两次，任何合理的 lazy/共享计算或显式 `raised = ...` 一次即等价），不改变
     数值结果（identity）。此外 LMMSE 已存在 `rx/|rx|→**M0` 的幅度无关升幂变体（`_recovery.py:360-361`），
     证明"升幂表示"本身是可替换的内部数值组件，不是方法动作。
7. **主图 / 核心消融 / 最小实现切片**：主图 = 操作数对比（两次 vs 一次 M0 升幂）；消融 =
   FOE-only / CPE-only / shared；最小切片 = 单窗 NDA 路操作计数。
8. **claim ceiling / fallback**：ceiling = "联合计算图减少 NDA 路冗余乘幂"；fallback = 该重排
   是 identity（数值不变），复杂度收益需真实综合数字，且可被编译器/CSE 自动完成。
9. **标注**：`[FACT]` 升幂两次（`sim:150` + `rec:213`）；`[FACT]` 两次归约结构不同（FFT vs
   mean-angle）；`[FACT]` LMMSE 已有幅度无关升幂变体（`rec:360-361`）且 DEPRECATED（`:280-286`）；
   `[INFERENCE]` 共享 `raised` 是数值 identity，不改变 BER；`[INFERENCE]` 该重排属 trivial DAG
   优化，编译器/CSE 或一行 `raised = ...` 即等价。
10. **action-signature 检索词 / 命中 / 结论**：检索词 = `复用|中间量|联合计算|fusion|raised.*M0|reuse.*intermediate|计算图融合`
    （`rg` 于 `.sessions/**/decisions.md`、`worker-logs/`、`thesis-lessons.md`、`harvest/`）。命中 =
    `packaging-recipe-library.md:30,179`（中间量复用是 R3 低复杂度 recipe 的已知生成源，非新动作）+
    `thesis-lessons.md:510`（复用已有编号）。结论：升幂复用属 R3 recipe 已知生成源，无既有同轴
    KILL，但被编译器 CSE / 一行重排廉价吸收，不构成独立动作。
11. **Collision receipt**：
    - existing action collision：**否（不是既有方法动作）**——但不是"动作不同"而是"不是动作"：
      升幂共享是计算图微观重排，不构成 receiver-visible 的新执行合同。
    - historical dead end：否（无直接同轴 KILL；LMMSE 是不同估计器变体，非同动作）。
    - strongest cheap alternative：**编译器 CSE / 一行 `raised = ...` 一次**（数值 identity，
      无 BER 变化，零成本吸收）。
    - reopen condition：共享升幂后产生 *非 identity* 的数值或结构变化（如 FOE/CPE 联合优化改
      变估计统计），但这已不是"复用中间量"而是新估计器（触发 `NDA_ML_BODY_REOPEN`）。
    - classification：**`ENGINEERING_COMPONENT`**——最多算实现优化（trivial DAG 重排），本轮不
      立为 survivor。

---

### Card P2 — Demand-Driven (Post-Select) h Estimation

1. **章节槽位 / 方法名**：Ch5 候选；"Demand-Driven Channel Estimation for Branch-Routed CPR"。
2. **M-C-A**：M = route-A 两路 h 估计（blind `hb` + pilot `hp`）；C = route-A 盲算两路 h，被弃
   分支的 h 计算浪费；A = 把 decide 提前，只算被选分支的 h（lazy-h）。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：raw、nominal SNR、（pilot 分支另需 tx）。
   - 动作：`decide(raw,snr,gl)` → 选支 → 只对被选分支调 `estimate_h_*_perblock` + `mmse_equalize`
     + 该分支 recovery。
   - 输出：一条 carrier-corrected 复数序列。
4. **算法流程**：
   1. 读 raw、snr、gl；
   2. `decide`（CV gate + 13 dB gate，与 CCISP 同）；
   3. 选 'da' → `estimate_h_pilot_perblock` + `mmse_equalize` + `per_block_da`；
   4. 选 'nda' → `estimate_h_blind_perblock` + `mmse_equalize` + `per_block_nda`；
   5. 输出被选分支校正序列。
5. **相对 CCISP / inventory 的新增点**：声称"只算被选分支 h"相对 route-A 盲算两路 h 是新执行
   合同。
6. **传统 comparator / strongest cheap alternative**：
   - comparator：route-A（两路 h）。
   - strongest cheap alternative：**route-B select-before-execute（`branch_route_b` / 2B / T005）**。
7. **主图 / 核心消融 / 最小实现切片**：主图 = branch-compute 操作数（route-A 两路 h vs route-B
   单路 h）；消融 = h 估计开销分解；最小切片 = 单条件操作计数。
8. **claim ceiling / fallback**：ceiling = "demand-driven h 估计减少被弃分支 h 计算"；fallback =
   该执行合同已被 route-B 实现，无独立增量。
9. **标注**：`[FACT]` route-A 两路 h（`run_..._a:38`）；`[FACT]` route-B 只算被选分支 h 且 timed
   kernel 已计入（`_a4_branchrouted:369-400`）；`[FACT]` route-B 与 CCISP select-before-execute
   action 重复（`internal-method-kernel-inventory.yaml:61-75`，2B/T005）。
10. **action-signature 检索词 / 命中 / 结论**：检索词 = `single.branch|branch.compute|scheduling.*saving|cost.*account|少记|lazy.*h|demand|h.*estimate.*after|两路.*复用`
    （`rg` 于 `.sessions/**/decisions.md`、`worker-logs/`、`thesis-lessons.md`、`harvest/`、`simulator/`）。
    命中 = `run_ccisp_family1_selector_a_30seed.py:38`（route-A 两路 h）+ `_a4_branchrouted_30seed.py:369-400`
    （route-B 只算被选分支 h 且 timed kernel 已计入）+ `internal-method-kernel-inventory.yaml:61-75`
    （`branch_route_b` route-B）+ `thesis-method-spines.md:69`（74.6% 禁用）+ R006 §1（2B/T005 动作重复）。
    结论：P2 = route-B 执行合同的动作重命名，无独立 action delta。
11. **Collision receipt**：
    - existing action collision：**是**——P2 的"decide 提前 → 只算被选分支 h + recovery"就是
      route-B 的执行合同（`branch_route_b`，`internal-method-kernel-inventory.yaml:61-75`）。
      P2 是 route-B 的动作重命名，不产生独立 action delta。
    - historical dead end：**是**——2B/T005 已判 single-branch scheduling 与 CCISP
      select-before-execute 动作重复（R006 §1，TL-30）；`internal-method-kernel-inventory.yaml:171`
      禁止 `route B 节省 74.6% 总接收机计算` 等 claim。
    - strongest cheap alternative：route-B 本身（已是 inventory 既有 kernel）。
    - reopen condition：demand-driven h 估计提供 route-B 无法覆盖的独立执行合同（如 h 估计与
      recovery 的不同调度粒度），但当前 h 估计与 recovery 在 route-B 同属"被选分支计算块"，
      无可分离的新调度。
    - classification：**`REJECT`**（existing action collision：与 `branch_route_b` 同动作）。

---

### Card P3 — Magnitude-Free Raised-Power Representation

1. **章节槽位 / 方法名**：Ch5 候选；"Magnitude-Free M0-Power for Hardware-Friendly NDA CPR"。
2. **M-C-A**：M = NDA-ML 升幂（`raised = rx**M0`，含幅度缩放）；C = 升幂后 `|rx|**M0` 缩放项在
   定点/硬件实现增加位宽与乘法器；A = 改用幅度无关升幂 `rx/|rx| → **M0`（相位项），去幅度缩放。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：均衡后复信号、M0=8。
   - 动作：`rx_n = rx/|rx|` → `yM = rx_n**M0` → FOE/CPE 用 `yM`（相位项）替代 `raised`。
   - 输出：一条校正复数序列。
4. **算法流程**：
   1. 读复信号；2) 归一化 `rx/|rx|`；3) 升幂 `**M0`；4) FOE/CPE（同 NDA-ML 结构）；5) 补偿；
   6) 输出。
5. **相对 CCISP / inventory 的新增点**：声称幅度无关升幂相对含幅度的升幂减少定点乘法器/位宽。
6. **传统 comparator / strongest cheap alternative**：
   - comparator：route-B NDA 路（含幅度升幂）。
   - strongest cheap alternative：**LMMSE（`_recovery.py:360-361`）已实现 `rx/|rx|→**M0`**；
     且 LMMSE 标 DEPRECATED（高 SNR BER floor，复现失败）**。此外幅度归一化是估计器内部数值
     表示，AGC/归一化是标准部署组件（G1 教训：scale artifact 可由 AGC 移除）。
7. **主图 / 核心消融 / 最小实现切片**：主图 = 位宽/乘法器 vs BER；消融 = 含幅度/幅度无关升幂；
   最小切片 = 单点 BER + 操作数。
8. **claim ceiling / fallback**：ceiling = "幅度无关升幂减少定点乘法器"；fallback = AGC 前置 +
   标准归一化（非新动作）。
9. **标注**：`[FACT]` LMMSE 已实现幅度无关升幂且 DEPRECATED（`rec:280-286,360-361`）；
   `[FACT]` 改 NDA-ML 升幂表示 = 改估计器本体（D050：`nda_ml_recovery` closed-form，改其数值
   表示触发 `NDA_ML_BODY_REOPEN`）；`[FACT]` G1 教训：scale artifact 可由 AGC 移除
   （`step-042-g1:24-81`）；`[INFERENCE]` 幅度归一化属标准部署组件，非独立方法动作。
10. **action-signature 检索词 / 命中 / 结论**：检索词 = `近似算子|去乘法器|查表|CORDIC|approximate|hardware.friendly|LUT|rx/np.abs|幅度无关|magnitude.free`
    （`rg` 于 `.sessions/**/decisions.md`、`worker-logs/`、`thesis-lessons.md`、`harvest/`、`common/`）。
    命中 = `_recovery.py:280-286,360-361`（LMMSE 幅度无关升幂 + DEPRECATED）+ `internal-method-kernel-inventory.yaml:135`
    （G1 scale artifact 由 AGC 移除）+ `step-042-g1:24-81`（G1 KILL）+ `.sessions/.../decisions.md:3024-3059`
    （D050 `NDA_ML_BODY_REOPEN`）。结论：幅度无关升幂变体（LMMSE）已存在且 DEPRECATED；改 NDA-ML
    升幂表示触发 forbidden body reopen；AGC 是最强廉价替代。
11. **Collision receipt**：
    - existing action collision：否（不是既有方法动作），但改估计器本体。
    - historical dead end：**是**——LMMSE（幅度无关升幂变体）复现失败已 DEPRECATED
      （`rec:280-286`）；G1 safe-gated normalization 已 KILL 为 scale artifact
      （`internal-method-kernel-inventory.yaml:135`，`prohibited_promotions: G1_METHOD_SIGNAL`）。
    - strongest cheap alternative：**AGC 前置 / 标准幅度归一化**（G1 终态：scale calibration 由
      AGC 平凡解决）。
    - reopen condition：幅度无关升幂在定点/硬件上提供 *独立于 AGC 的* 复杂度收益且有合法 BER
      非劣——但这要求改 NDA-ML 本体（触发 `NDA_ML_BODY_REOPEN`，forbidden）。
    - classification：**`REJECT`**（dead-end collision：LMMSE/G1 已证幅度归一化非独立动作；
      改估计器本体触发 `NDA_ML_BODY_REOPEN` 禁令）。

---

### Card P4 — Two-Stage Coarse-Fine CFO/Phase Compute Budget

1. **章节槽位 / 方法名**：Ch5 候选；"Adaptive FFT/Compute-Budget Allocation for NDA FOE+CPE"。
2. **M-C-A**：M = NDA 路 FOE（FFT 找频峰）+ CPE；C = 固定 `nfft_zp=N_fft*8` 零填充 FFT 在低 CFO
   残余时计算冗余；A = 按当前窗 CFO 估计置信度自适应分配 FFT 零填充/搜索预算（粗-细两阶段）。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：均衡后复信号、当前窗 CFO 估计置信度代理。
   - 动作：粗 FFT（小零填充）定位频带 → 按 CFO 量决定细 FFT 零填充预算 → CPE。
   - 输出：一条校正复数序列。
4. **算法流程**：1) 粗 FFT 找频带；2) 代理判 CFO 大小/置信度；3) 选细零填充预算；4) 精细 FFT
   估 omega；5) CPE；6) 补偿；7) 输出。
5. **相对 CCISP / inventory 的新增点**：声称自适应 FFT 预算相对固定零填充减少 FFT 点数。
6. **传统 comparator / strongest cheap alternative**：
   - comparator：固定零填充 NDA FOE。
   - strongest cheap alternative：**P09 early-stop BPS 同"计算预算自适应"动作签名**；且
     D050 证 NDA-ML closed-form 无可裁剪搜索结构（FOE 是单次 FFT argmax + 插值，非搜索）。
7. **主图 / 核心消融 / 最小实现切片**：主图 = CFO 量 × 自适应 vs 固定 FFT 点数 vs BER；消融 =
   粗/细阈值；最小切片 = 单 CFO 点。
8. **claim ceiling / fallback**：ceiling = "自适应 FFT 预算减少 FOE 计算量"；fallback = 固定零
   填充（单次 FFT 已是 closed-form）。
9. **标注**：`[FACT]` NDA FOE 是单次 FFT argmax + Quinn-Rife 插值（`sim:150-166`），非搜索、
   非候选枚举（D050）；`[FACT]` P09 early-stop BPS KILL（记账欺骗 + π/4 对称 B_used 恒定 +
   truth-resolved BER，`step-040-p10:32`，`internal-method-kernel-inventory.yaml:171`）；`[FACT]`
   改 NDA-ML FOE 结构 = 改估计器本体（`NDA_ML_BODY_REOPEN`，D050）；`[INFERENCE]` 自适应 FFT
   零填充属"计算预算自适应"同动作族，与 P09 同签名。
10. **action-signature 检索词 / 命中 / 结论**：检索词 = `coarse.to.fine|迭代.*FOE|动态.*预算|计算预算|adaptive.*fft|zero.?pad|early.?stop|动态.*计算|sparse.*update|early.?termin`
    （`rg` 于 `.sessions/**/decisions.md`、`worker-logs/`、`thesis-lessons.md`、`harvest/`）。命中 =
    `step-039-p09:9,30,40`（P09 early-stop BPS C3 8× reduction）+ `step-040-p10:32`（C3 三重无效
    KILL）+ `.sessions/.../decisions.md:3024-3059`（D050 STRATEGIC_GATE：NDA-ML closed-form 无可裁剪
    搜索结构）。结论：自适应计算预算与 P09 同动作签名（已 KILL）；D050 证 FOE 是单次 FFT argmax +
    插值非搜索，自适应预算无作用对象。
11. **Collision receipt**：
    - existing action collision：否（FOE 预算自适应不是既有 CCISP 动作）。
    - historical dead end：**是**——P09 early-stop BPS（`COMPUTE_CONSTRAINED_NDA_ML_SEARCH`）同
      "计算预算自适应"动作签名已被 KILL 为三重无效（`step-040-p10:32`）。D050 STRATEGIC_GATE：
      NDA-ML closed-form 无可裁剪搜索结构，自适应预算 = 换估计器本体 = `NDA_ML_BODY_REOPEN`
      （forbidden）。`assume_df_zero=True` 时 FOE 分支被跳过，CFO 残余自适应预算无作用对象。
    - strongest cheap alternative：固定零填充 FFT（closed-form，已是最低复杂度）。
    - reopen condition：FOE 存在可裁剪的搜索/枚举结构（D050 已证不存在）；或新信道引入大 CFO
      使 FOE 成本可观——但后者改 testbed 且 `assume_df_zero=True` 主线已跳过 FOE。
    - classification：**`REJECT`**（dead-end collision：P09 同签名 KILL + D050 forbidden body
      reopen）。

---

### Card P5 — Inter-Window CFO/Phase Cache Scheduling

1. **章节槽位 / 方法名**：Ch5 候选；"Cross-Window CFO/Phase Cache for NDA CPR"。
2. **M-C-A**：M = 每窗独立 NDA FOE/CPE（无跨窗状态）；C = 相邻窗 CFO/相位有连续性时逐窗从零
   重估浪费；A = 缓存上一窗 omega/phi，按连续性增量更新或跳过重估。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：当前窗复信号 + 前窗 omega/phi 缓存。
   - 动作：判断 CFO 连续性 → 复用/增量更新缓存 omega → CPE。
   - 输出：一条校正复数序列。
4. **算法流程**：1) 维护 omega/phi 滑窗；2) 读当前窗；3) 判连续性；4) 复用或重估；5) CPE；
   6) 补偿；7) 输出。
5. **相对 CCISP / inventory 的新增点**：引入跨窗 CFO/相位缓存（CCISP 每窗 stateless）。
6. **传统 comparator / strongest cheap alternative**：每窗 stateless NDA；P06 跨帧历史（已 KILL）。
7. **主图 / 核心消融 / 最小实现切片**：主图 = 缓存长度 vs BER/操作数；消融 = 复用/重估阈值；
   最小切片 = 单条件缓存命中率。
8. **claim ceiling / fallback**：ceiling = "跨窗 CFO 缓存减少重估"；fallback = 跨窗状态无物理
   连续性，缓存无效。
9. **标注**：`[FACT]` 每窗独立 seed（`run_..._a:37` `seed=ws=start+b`）；`[FACT]` 信道 `h` 块
   常数 i.i.d.（`_channel.py:27-32`）；`[FACT]` P06 跨帧历史 KILL（last-value R² 0.85 >
   causal-history R² 0.32，`internal-method-kernel-inventory.yaml:131`）；`[FACT]` Ch4 C2 跨窗
   记忆 Gate 1 不过（`ch4-concept-method-batch-001.md:124-132`，每窗独立 seed + 块常数 i.i.d.
   h，跨窗状态无物理自由度）；`[INFERENCE]` CFO `f_res·k·T_S` 在每窗内独立生成（`_channel.py:51`
   `doppler_phase` 用 `np.random.seed(seed)` 重置），跨窗无连续可缓存。
10. **action-signature 检索词 / 命中 / 结论**：检索词 = `流水|并行|缓存|pipeline|cache|warm.?up|window.*reuse|block.*reuse|跨窗|跨帧|causal.*history|state.*memory`
    （`rg` 于 `.sessions/**/decisions.md`、`worker-logs/`、`thesis-lessons.md`、`harvest/`）。命中 =
    `internal-method-kernel-inventory.yaml:131`（P06 跨帧历史 KILL，R² 0.85 > 0.32）+
    `ch4-concept-method-batch-001.md:124-132`（C2 跨窗记忆 Gate 1 不过）+ `_channel.py:27-32,70`
    （每窗独立 seed + 块常数 i.i.d. h + RNG 重置）+ `run_..._a:37`（每窗新 seed）。结论：跨窗 CFO/相位
    缓存物理前提不存在（无连续性可缓存）；与 P06/C2 同轴已 KILL。
11. **Collision receipt**：
    - existing action collision：否（CCISP stateless，无既有跨窗缓存动作）。
    - historical dead end：**是**——P06 causal cross-frame history 已 KILL（
      `internal-method-kernel-inventory.yaml:131`）；Ch4 C2 跨窗记忆 Gate 1 不过（物理自由度
      不存在）。
    - strongest cheap alternative：**无（物理前提不存在）**。
    - reopen condition：simulator 改为块间相关信道（如 `_gg_time.py` AR(1) 接入 CCISP 链；当前
      仅 Q-CMA-FADE 独立轨道用，CCISP 链不 import，`ch4...c2:129-130`）。
    - classification：**`REJECT`**（物理前提不存在：每窗独立 seed + 块常数 i.i.d. h + 每窗重置
      RNG 的 doppler_phase；跨窗 CFO/相位无连续性可缓存。Gate 1 不过；强行做属换名重开已 KILL
      的 P06 / Ch4 C2）。

## 4. Cross-card comparison

| 维度 | P1 升幂复用 | P2 demand-h | P3 幅度无关升幂 | P4 自适应 FFT 预算 | P5 跨窗 CFO 缓存 |
|---|---|---|---|---|---|
| 动作机制族 | 计算图中间量复用 | 执行合同（lazy h） | 数值表示/近似 | 计算预算自适应 | 跨窗状态缓存 |
| 动作真实可部署 | 是（DAG 重排） | 是 | 是（改估计器本体） | 是（改 FOE 结构） | 否（每窗独立 seed） |
| 与既有贡献重复 | 否（非既有方法动作） | **是**（route-B） | 否（改本体） | 否（非既有动作） | 否 |
| 被廉价传统吸收 | **是**（CSE/一行） | route-B 本身 | **是**（AGC/LMMSE） | 固定零填充 | — |
| 触发既有 KILL / 禁令 | 否 | 2B/T005 | LMMSE/G1/D050 | P09/D050 | P06/C2 |
| 物理自由度存在 | 是 | 是 | 是 | 是 | **否**（Gate 1 不过） |
| 复杂度下降由真实调用数定义 | 否（identity） | 是（但属 route-B） | 否（AGC 可移除） | 否（closed-form 无搜索） | 否（无连续性） |
| 能否形成完整一章 | 否（实现优化） | 否（重复） | 否（边界） | 否（重复） | 否（物理前提缺） |
| 最小实现可否现有资产 | 是 | 是（即 route-B） | 是（LMMSE 已在） | 是 | 否 |
| **结论** | ENGINEERING_COMPONENT | **REJECT** | **REJECT** | **REJECT** | **REJECT** |

## 5. Survivor(s) and why

**无 survivor。**

5 张卡全部碰撞或被廉价替代吸收：

- **P1**（ENGINEERING_COMPONENT）：升幂复用是数值 identity 的 trivial DAG 重排，被编译器
  CSE / 一行 `raised = ...` 平凡吸收；不构成 receiver-visible 的新执行合同。
- **P2**（REJECT）：demand-driven h 估计 = route-B select-before-execute 执行合同
  （`branch_route_b` / 2B / T005），动作重命名，无独立 action delta。
- **P3**（REJECT）：幅度无关升幂的变体（LMMSE）已存在且 DEPRECATED；幅度归一化是 AGC/标准
  部署组件（G1 终态）；改 NDA-ML 升幂表示触发 `NDA_ML_BODY_REOPEN` 禁令（D050）。
- **P4**（REJECT）：自适应 FFT 预算与 P09 early-stop BPS 同"计算预算自适应"动作签名，已被
  KILL 为三重无效；D050 证 NDA-ML closed-form 无可裁剪搜索结构，自适应预算 = 换估计器本体 =
  `NDA_ML_BODY_REOPEN`。
- **P5**（REJECT）：跨窗 CFO/相位缓存物理前提不存在（每窗独立 seed + 块常数 i.i.d. h + 每窗
  重置 RNG），Gate 1 不过；与 P06 跨帧历史 / Ch4 C2 跨窗记忆同轴（已 KILL）。

**为何没有一张存活**：当前接收链的部署/计算流程自由度已被四个约束锁死——
(a) **route-B 执行合同**（h 估计、分支选择、单支执行已统一，P2 无独立增量）；
(b) **closed-form 估计器本体不可重开**（D050 `NDA_ML_BODY_REOPEN` 禁令，P3/P4 触发）；
(c) **每窗独立 seed 无跨窗物理连续性**（P5 Gate 1 不过）；
(d) **计算图微观重排是 identity**（P1 被廉价吸收）。
在当前资产上，Ch5 部署/计算流程候选源已无独立于 route-B 的新方法动作空间。

按 brief §3，连续两个构造周期无 survivor 时须判候选来源/thesis target 需调整。本批（Ch5）与
T006（Ch4，已 `NO_CONSTRUCT_SURVIVES`）已是连续两个构造周期无 survivor。

## 6. Next formal entry

**无 survivor → 无 GW 入口。** 不写任何实验任务、不进 GW、不进 Contract/Execute。

**下一批必须更换的候选源或研究对象**（设计建议，非本轮可执行动作）：

1. **候选源切到接收链之外/输入侧**：如发射侧 Tx-PMF 协同（A9 recipe，概率整形 + CPR 协同，
   `packaging-recipe-library.md:113-123`），或 AMC/rate control（2D，但需新 GW + 用户授权，
   `internal-method-kernel-inventory.yaml:113-128` `q_a_prime` 标 `UNAUTHORIZED_DEV_ONLY`）。
2. **研究对象换到真实存在跨窗物理连续性的信道**：如块间相关 GG / AR(1) 时间相关信道
   （`_gg_time.py` AR(1) 模型当前仅 Q-CMA-FADE 独立轨道用，CCISP 链不 import；接入后才解锁
   跨窗缓存/记忆类方法，见 P5/C2 reopen condition）。
3. **更换 testbed 到真实硬件**：若 Ch5 想成立"部署/硬件友好"章，需真实 FPGA/RTL 工具链
   （R4 recipe，`packaging-recipe-library.md:172`）；当前无合法综合，复杂度/资源 claim 无
   authority（`asset-claim-matrix.yaml:144-151` `resource_proxy_note: NO real synthesis`）。

以上为设计层建议，需用户在新对话裁决是否换源/换对象/换 testbed；本轮不执行、不检索、不开 GW。

---

## 证据来源汇总（所有 `[FACT]` 的本地指针）

- route-A 完整计算路径：`projects/simulation/simulator/run_ccisp_family1_selector_a_30seed.py:36-43`
- route-B 完整计算路径 + timed kernel：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_branchrouted_30seed.py:358-400`
- 升幂 `rx**M0` FOE（第一次）：`projects/simulation/simulator/sc_nda_ml_sim.py:150`
- 升幂 `rx**M0` CPE（第二次）：`projects/simulation/common/_recovery.py:213`（assume_df_zero 分支）/ `:243`（FFT-df 分支）
- LMMSE 幅度无关升幂 `rx/|rx|→**M0`：`projects/simulation/common/_recovery.py:360-361`；DEPRECATED 标记 `:280-286`
- 每窗独立 seed：`run_ccisp_family1_selector_a_30seed.py:37`（`seed=ws=start+b`）
- 信道块常数 i.i.d. h：`projects/simulation/common/_channel.py:27-32`（`gg_block` 按 BLOCK 分段，块间独立 `gamma_dist.rvs`）
- doppler_phase 每窗重置 RNG：`_channel.py:70`（`np.random.seed(seed)`）+ `:51-54`（CFO 相位项）
- NDA-ML closed-form（无可裁剪搜索结构）：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:3024-3059`（D050 STRATEGIC_GATE）
- P09 early-stop BPS KILL（三重无效）：`projects/thesis-fso/worker-logs/step-040-p10-single-expert-router.md:32`
- P09 记账欺骗（`:329` 全算 64 再 `:348` 只计 B_used）：`step-040-p10:25`
- route-B / 2B / T005 single-branch 与 CCISP 重复：`internal-method-kernel-inventory.yaml:61-75`；R006 §1
- route-B timed kernel 含 h 估计：`_a4_branchrouted_30seed.py:369-400`
- P06 跨帧历史 KILL（R² 0.85 > 0.32）：`internal-method-kernel-inventory.yaml:131`
- G1 scale artifact 由 AGC 移除：`internal-method-kernel-inventory.yaml:135`（`p05_p06_p07r_g1_p09_boundaries`）；`projects/thesis-fso/worker-logs/step-042-g1-promotion-groundwork-scale-artifact.md:24-81`
- Ch4 C2 跨窗记忆 Gate 1 不过：`projects/thesis-fso/direction-lab/harvest/ch4-concept-method-batch-001.md:124-132`
- CCISP 链不 import `_gg_time` AR(1)：`ch4-concept-method-batch-001.md:129-130,291`
- R3/R4 recipe（低复杂度/定点硬件，sample 支持）：`packaging-recipe-library.md:171-172`
- R6 分层 REJECT（0/12，coarse-to-fine/pipeline 不得硬贴）：`packaging-recipe-library.md:174`
- 资源 claim 无合法综合：`asset-claim-matrix.yaml:144-151`（`resource_proxy_note: NO real synthesis`）
- task-control validator：`python .agents/skills/research-direction-lab/scripts/validate_task_control.py T007...` → `PASS`
