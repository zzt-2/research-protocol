# Ch4 概念方法构造批次 001

> 2026-08-04 | 来源: T006 / S015 / D023 / CP003 | action_class: CONCEPT_METHOD_CONSTRUCTION
> 性质: design-only 概念原型卡。survivor 不是 METHOD_SIGNAL、不是 Go，不能进论文正文；
> 实验前必须回 GW Step 1–3/3.5/4a。无仿真、无代码、无检索、无科学 claim。

## 1. Terminal verdict

**`CONCEPT_SURVIVOR_AVAILABLE`**：4 张原型卡中 3 张碰撞/降级，1 张保留为 design
candidate（C3，Intra-Window Segmented Phase Tracking），下一步从 GW Step 1 问题定义开始。

- C1 自盲 NDA 残差校准阈值 → 碰撞：SNR-mismatch/region-retune A 族（D040，已 CLOSED）的最强
  廉价替代复刻，分类 `REJECT`。
- C2 状态记忆（跨窗功率/CV 历史）→ 碰撞：simulator 每窗独立重置（每窗新 seed），跨窗状态无
  物理自由度，Gate 1 不过，分类 `REJECT`。
- C3 块内分段相位跟踪自适应化 → 存活：真实 deployable action，机制族不同（CPE 估计几何，
  非 selector 阈值/region/校准），但依赖一个未验证假设，需回 GW。分类 `EXTENSION`。
- C4 选择器两阶段置信度融合 → 被最强廉价替代吸收（CV hard gate 已是该融合的廉价离散版），
  分类 `ENGINEERING_COMPONENT`，本轮不立为 survivor。

排序维度按 brief §3 五条：动作真实可部署 / 不与既有贡献重复 / 不被廉价传统吸收 / 能否形成
完整一章 / 最小实现可在现有资产完成。C3 在"动作真实"和"机制不同"两项独立，在"完整一章"
和"最小实现"两项可闭合，但在"不被廉价吸收"和"失败 fallback"上需 GW Step 4a 验证。

## 2. Existing contribution / dead-end map

| ID | 动作边界 | 终态/分类 | 证据 (`path:line`) |
|---|---|---|---|
| ccisp | CV gate → blind `ĥ_dsp` → 13 dB gate → 只执行 DA/NDA 一支（select-before-execute） | `THESIS_MAIN_METHOD`，Ch3，唯一 ready 主方法 | `internal-method-kernel-inventory.yaml:11-27`；`method.tex:36-71` |
| p01_snr_adapter | pilot-SNR estimate → 校准 selector 工作点 | `NO_DIAGNOSTIC_SIGNAL`，恢复 4/5 harm cell | `internal-method-kernel-inventory.yaml:29-43`；`step-028-p01:86-96` |
| p02_weak_region_retune | stage-1 ref 9→11 dB（region-specific threshold） | `PROBLEM_RESOLVED_BY_REGION_RETUNING`，常规廉价替代 | `internal-method-kernel-inventory.yaml:45-59`；D040 |
| branch_route_b (2B/T005) | raw statistic → controller command → 只执行一支 | single-branch action 与 CCISP select-before-execute 重复；code-path equivalence | `internal-method-kernel-inventory.yaml:61-75`；T005 commit `67970307` |
| p03_fixed_point | 量化 selector 统计量与决策路径 | `PROBLEM_RESOLVED_BY_UNIFORM_PRECISION`，实现点 | `internal-method-kernel-inventory.yaml:77-91` |
| 2A/T004 | pilot-SNR → operating-region calibration → CCISP branch action | 被 ordinary regional retune 吸收（dev 比 conventional 低） | R006 §1；T004 commit `1140134e8` |
| q_a_prime (2D) | predicted receiver state → rate/no-transmit | `UNAUTHORIZED_DEV_ONLY`，需新 GW+授权 | `internal-method-kernel-inventory.yaml:110-125` |
| A 族（CPR selector 鲁棒性） | SNR-mismatch / region-retune / cand_rank / weakretune | CLOSED，同族连续=2 达上限，TL-30 禁换名重开 | D040（`.../longitudinal-test/decisions.md:2514-2547`） |
| p05–p07r/g1/p09 | ML OOD / 跨帧历史 / AGC / scale-artifact / BPS early-stop | 局部负面/方法论反例，禁晋级 | `internal-method-kernel-inventory.yaml:127-144` |

关键 collision 约束：Ch4 不能再用 selector 阈值/region/SNR-校准/region-retune 机制（A 族
CLOSED）；不能把 single-branch scheduling 当新动作（2B 重复）；不能跨对象复活
invalidated claim（26/29、uplink、1.2–1.9 dB、74.6%、G1、P09 等）。

## 3. Prototype cards

### Card C1 — Self-Blind NDA-Residual Threshold Calibration

1. **章节槽位 / 方法名**：Ch4 候选；"Receiver-Visible Residual-Driven CPR Selector Calibration"。
2. **M-C-A**：M = CCISP 两阶段 selector；C = nominal-SNR mismatch + GG 工作区漂移使 `ĥ_dsp`
   盲有效-SNR 估计带偏，selector 阈值（13 dB gate / CV τ）错位；A = 用 receiver-visible 当前
   窗残差/统计重估工作点并校准阈值。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：当前窗 raw `|r|²`、blind `ĥ_dsp = mean|r|² − 1/(2γ)`、nominal SNR。
   - 动作：由 `ĥ_dsp` 残差估计工作区偏置 → 校准 `GAMMA_EFF_TH` / `CV_MARGIN` → 驱动既有 DA/NDA
     branch decision。
   - 输出：一条 carrier-corrected 复数序列（同 CCISP 输出契约）。
4. **算法流程**：
   1. 读当前窗 raw `q_k=|r_k|²` 与 nominal SNR；
   2. 算 CV 与 blind `ĥ_dsp`（既有 `_a4_switch_common768_30seed.py:97-107` 的统计量）；
   3. 由 `ĥ_dsp` 与 nominal SNR 的偏差估计工作区偏置 `Δγ`；
   4. 把 `GAMMA_EFF_TH`(13)→`GAMMA_EFF_TH+Δγ` 或 `CV_MARGIN`→校准值；
   5. 用校准后阈值走既有 CV→effective-SNR 两阶段 gate；
   6. 只执行所选 DA 或 NDA 一支；
   7. 输出 256-sample 校正窗。
5. **相对 CCISP / inventory 的新增点**：相对 CCISP，把固定 13 dB/`CV_MARGIN` 改为当前窗
   自校准；相对 P01（pilot-SNR adapter，用 pilot 估 SNR）和 P02（region retune）改用 **盲残差**
   而非 pilot。
6. **传统 comparator / strongest cheap alternative**：
   - comparator：ordinary global/region SNR retune（dev 调一个 ref/阈值）。
   - strongest cheap alternative：**ordinary region retune（ref 9→11 dB）**。
7. **主图 / 核心消融 / 最小实现切片**：主图 = mismatch × GG × SNR 下 selector BER-ratio；
   消融 = estimator-only / calibration-only / full chain；最小切片 = weak@9 dB 单点。
8. **claim ceiling / fallback**：ceiling = "接收侧可见校准提高工作点失配下鲁棒性"；fallback =
   降为校准规则（同 P02 终态）。
9. **标注**：`[FACT]` 13 dB/`CV_MARGIN` 为固定字面量（`_a4_switch_common768_30seed.py:78-79`）；
   `[FACT]` A 族已 CLOSED（D040）；`[FACT]` P02 region retune +0.4539 dB 略胜 cand_rank
   （D040）；`[INFERENCE]` 盲残差校准≈pilot-SNR 校准的廉价复刻。
10. **Collision receipt**：
    - existing action collision：**是**——与 P01 pilot-SNR adapter 动作链同形（estimate SNR →
      recalibrate operating point → branch decision，`internal-method-kernel-inventory.yaml:29-34`）。
    - historical dead end：**是**——2A/T004 同动作链已被 ordinary regional retune 吸收（dev 比
      conventional 低 0.04096 dB，R006 §1）；A 族 SNR-mismatch/region-retune/cand_rank/weakretune
      全 CLOSED（D040），TL-30 禁换名重开。
    - strongest cheap alternative：ordinary region retune（P02 终态已证明吸收同类增益）。
    - reopen condition：盲残差估计能证明提供 pilot-SNR 与 region-retune 都不能提供的独立信息
      增量（[HYPOTHESIS]，无证据）。
    - classification：**`REJECT`**（动作链与已 CLOSED 的 A 族同族，廉价替代已吸收）。

---

### Card C2 — Inter-Window State-Memory Branch Controller

1. **章节槽位 / 方法名**：Ch4 候选；"State-Memory Adaptive CPR Branch Controller"。
2. **M-C-A**：M = CCISP 两阶段 selector；C = 每窗独立决策忽略相邻窗的功率/CV 连续性，工作区
   边界处选择抖动；A = 引入跨窗功率/CV 滑动记忆，用相邻窗状态平滑当前窗 branch decision。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：当前窗 raw `|r|²`、nominal SNR + 前若干窗的 CV/`ĥ_dsp` 历史。
   - 动作：滑动平均历史 CV/功率 → 校正当前窗 gate 决策。
   - 输出：一条 carrier-corrected 复数序列。
4. **算法流程**：
   1. 维护长度 W 的 CV/`ĥ_dsp` 滑窗；
   2. 读当前窗统计量并入队；
   3. 用滑窗平滑估计工作区；
   4. 走 CV→effective-SNR gate（阈值由平滑估计校准）；
   5. 只执行所选分支；
   6. 输出 256-sample 校正窗。
5. **相对 CCISP / inventory 的新增点**：引入跨窗状态记忆（CCISP 每窗 stateless）。
6. **传统 comparator / strongest cheap alternative**：fixed-stateless CCISP；P06 last-value
   persistence（已 KILL，R² 0.85 > causal-history R² 0.32）。
7. **主图 / 核心消融 / 最小实现切片**：主图 = 跨窗记忆长度 W vs BER-ratio；最小切片 = weak
   regime 滑窗。
8. **claim ceiling / fallback**：ceiling = "跨窗记忆平滑工作区边界抖动"；fallback = 降为工程平滑。
9. **标注**：`[FACT]` CCISP 每窗独立实现、新 seed（`run_...selector_a_30seed.py:35-36`，
   每窗 `generate_shared_realization_apsk`）；`[FACT]` 信道 `h` 块常数 i.i.d. 于块间
   （`_channel.py:27-32`）；`[FACT]` P06 跨帧历史已 KILL（`internal-method-kernel-inventory.yaml:131`）；
   `[INFERENCE]` 跨窗状态在本仿真器无物理连续性可利用。
10. **Collision receipt**：
    - existing action collision：否（CCISP stateless，无既有跨窗动作）。
    - historical dead end：**是**——P06 causal cross-frame history 已 KILL（last-value R² 0.85 >
      causal-history R² 0.32，`step-033-p06:9-62`）。
    - strongest cheap alternative：**无（物理前提不存在）**。
    - reopen condition：simulator 改为块间相关信道（如 `_gg_time.py` AR(1) 模型接入 CCISP 链；
      当前仅 Q-CMA-FADE 独立轨道用，CCISP 链不 import）。
    - classification：**`REJECT`**（跨窗状态物理自由度不存在：每窗独立 seed + 块常数 i.i.d. h；
      Gate 1 不过——候选 lever 无对应可实现变换。强行做属换名重开已 KILL 的 P06）。

---

### Card C3 — Intra-Window Segmented Phase Tracking Adaptation (SURVIVOR)

1. **章节槽位 / 方法名**：Ch4 候选；"Adaptive Intra-Window Segmented CPE for Turbulence-Affected CPR"。
2. **M-C-A**：M = NDA CPE（`nda_ml_recovery`，`_recovery.py:171-273`）；C = 块内 Wiener 激光线宽
   相位噪声（`σ²_φ=2π·CLW·T_S·N_block≈0.032 rad/块`）在高 SNR 造成 BER floor，且固定块常数
   mean-angle 在 strong 湍流有害；A = 把固定块常数/segK8 跟踪改为按当前窗 receiver-visible
   指标自适应选择块内相位跟踪粒度（segment count / 整块 mean-angle）。
3. **receiver-visible 输入 → 动作 → 输出**：
   - 输入：当前窗 raw 复信号、nominal SNR、CV（功率离散，已有）。
   - 动作：由 CV/有效-SNR 判断湍流/线宽强度 → 选 NDA 块内跟踪粒度（K 段 vs 整块 mean-angle）
     → 跑升幂 mean-angle + 段间 unwrap 插值。
   - 输出：一条 256-sample CPE 校正复数序列。
4. **算法流程**：
   1. 读当前窗 raw `r`，算 CV（`_a4_switch_common768_30seed.py:99-100`）；
   2. 由 CV 判当前窗湍流/线宽工况（weak/moderate/strong 离散档或连续映射）；
   3. 选块内跟踪模式：strong/高线宽 → 整块 mean-angle（当前默认，避免 segK8 在 strong 有害），
     AWGN/高 SNR → K 段（segK8，跟踪块内 PN 漂移）；
   4. 升 M₀=8 次幂，按所选粒度做分段 mean-angle；
   5. 段间 unwrap + 线性插值得逐符号相位轨迹（复用 `_recovery.py:218-227` 既有 segK8 实现）；
   6. 除以 M₀，去旋；
   7. 输出 256-sample 校正窗。
5. **相对 CCISP / inventory 的新增点**：CCISP select-before-execute 在 **DA/NDA 分支层** 选择；
   本卡在 **NDA 分支内部** 改 CPE 估计几何（块内跟踪粒度），动作对象是相位估计而非选择器阈值。
   既有 segK8 是固定硬编码（`intra_block_tracking` 字符串，per-scenario 手动，`_recovery.py:196-199`）；
   本卡把它改为当前窗 receiver-visible 自适应。机制族 = CPE 估计几何，非 selector 阈值/region/校准。
6. **传统 comparator / strongest cheap alternative**：
   - comparator：固定整块 mean-angle NDA CPE（B11 锚）；固定 K=8 分段 NDA CPE。
   - strongest cheap alternative：**per-scenario 固定选择**（当前代码已支持：turb 用 'none'，AWGN
     用 'segmented'，由调用方按场景手动设）。C3 的增量 = 用当前窗可见量替代场景标签手动设。
7. **主图 / 核心消融 / 最小实现切片**：主图 = 湍流档 × SNR × 块内跟踪模式 的 NDA BER / BER-ratio；
   消融 = (a) 固定整块 vs 固定 segK8 vs 自适应；(b) 自适应触发量（CV / 有效-SNR / 线宽估计）；
   最小切片 = weak@9 dB 与 strong@高 SNR 两点，比 fixed-mode。
8. **claim ceiling / fallback**：ceiling = "当前窗可见量驱动的块内跟踪自适应在跨湍流/SNR 时优于任一
   固定模式"；fallback = "场景特定块内跟踪选择规则"（工程组件，等价 per-scenario 手动设的自动化）。
9. **标注**：`[FACT]` segK8 实现存在（`_recovery.py:218-227`）；`[FACT]` segK8 "在 strong 湍流有害"
   注释（`_recovery.py:196-198`）；`[FACT]` 块内 Wiener PN `σ²_φ≈0.032 rad/块` 造成 high-SNR BER
   floor（`_recovery.py:199-200`）；`[FACT]` 当前 `intra_block_tracking` 为 per-scenario 手动字符串
   （`_recovery.py:193-199`）；`[FACT]` CCISP 链不 import CMA/`_gg_time`（CMA 仅 Q-CMA-FADE）；
   `[INFERENCE]` 当前窗 CV 与"湍流强度 vs AWGN-PN 主导"相关；`[HYPOTHESIS]` 自适应触发量能区分
   两工况且优于两固定模式之较优者（未验证，需 GW Step 4a）。
10. **Collision receipt**：
    - existing action collision：**否**——CCISP/2A/2B 动作对象是 selector 阈值/region/校准/计算图
      schedule，不在 NDA 分支内部改 CPE 估计几何。segK8 是既有组件但非既有 *方法动作*（固定硬编码，
      `internal-method-kernel-inventory.yaml` 未列为 method_like kernel）。
    - historical dead end：**否（部分相关）**——P06 跨帧历史 KILL 是"跨窗"记忆，本卡是"窗内"分段，
      时间尺度不同；P07r 是 AGC/gain scale，机制不同。无同轴 dead end。
    - strongest cheap alternative：per-scenario 固定选择（已存在代码路径）；C3 增量 = 可见量驱动替代
      场景标签手动设。
    - reopen condition：自适应触发量在跨工况 paired held-out 上稳定优于两固定模式之较优者（超出 MDE）；
      否则降为工程组件。
    - classification：**`EXTENSION`**——真实 deployable action（改 CPE 估计几何），机制族不同，但依赖
      "自适应 > 固定场景选择"的未验证假设；survive 为 design candidate，非 method signal。

---

### Card C4 — Two-Stage Confidence Fusion Selector

1. **章节槽位 / 方法名**：Ch4 候选；"Confidence-Weighted Two-Stage CPR Selector"。
2. **M-C-A**：M = CCISP 两阶段 selector；C = 硬 CV gate + 13 dB gate 的离散二选一在边界附近抖动；
   A = 用两个统计量的置信度/软概率融合替代 hard gate。
3. **receiver-visible 输入 → 动作 → 输出**：输入 CV、blind `ĥ_dsp`、nominal SNR；动作 = 软融合打分
   → DA/NDA 概率 → 选支；输出 = carrier-corrected 序列。
4. **算法流程**：1) 算 CV、`ĥ_dsp`；2) 各映射为置信度/softmax 概率；3) 加权融合；4) 选概率高支；
   5) 执行单支；6) 输出。
5. **相对 CCISP 的新增点**：把 hard gate 改软融合。
6. **传统 comparator / strongest cheap alternative**：fixed CCISP hard gate；**strongest cheap
   alternative = 现有 hard gate 本身已是该融合的廉价离散版（CV 硬门 ≈ CV 权重→∞ 的极限）**。
7. **主图 / 消融 / 最小切片**：边界 SNR 点 BER-ratio；最小切片 = crossover 点附近。
8. **claim ceiling / fallback**：ceiling = "软融合减少边界抖动"；fallback = 工程调门。
9. **标注**：`[FACT]` 两阶段 gate 离散（`method.tex:36-71`）；`[FACT]` A 族 CLOSED；`[INFERENCE]`
   soft fusion 与 hard gate 差异主要在边界薄带。
10. **Collision receipt**：
    - existing action collision：**是（机制同族）**——动作对象仍是 selector 阈值/融合，属 A 族
      selector-robustness 范畴（D040 CLOSED）。
    - historical dead end：A 族 CLOSED（TL-30 禁换名重开）。
    - strongest cheap alternative：hard gate 本身（边界调参即可）。
    - reopen condition：边界带外有稳定独立增益（[HYPOTHESIS]，无证据）。
    - classification：**`ENGINEERING_COMPONENT`**——最多算边界调参工程，本轮不立 survivor。

## 4. Cross-card comparison

| 维度 | C1 残差校准 | C2 跨窗记忆 | C3 块内分段跟踪 | C4 置信度融合 |
|---|---|---|---|---|
| 动作机制族 | selector 阈值/校准 | 跨窗状态记忆 | CPE 估计几何（窗内分段） | selector 融合 |
| 机制是否与 A 族/CCISP 不同 | **否**（A 族） | 是（但物理前提缺） | **是**（CPE 内部，非 selector） | 否（A 族） |
| 动作真实可部署 | 是 | 否（每窗独立 seed） | 是 | 是 |
| 与既有贡献重复 | 是（P01/2A） | 否 | 否（segK8 是组件非方法动作） | 是（CCISP gate） |
| 被廉价传统吸收 | 是（region retune） | — | 部分（per-scenario 固定） | 是（hard gate 本身） |
| 能否形成完整一章 | 否（边界章） | 否 | 可能（CPE 几何 × 工况） | 否 |
| 最小实现可否现有资产 | 是 | 否 | 是（复用 `_recovery.py:218-227`） | 是 |
| **结论** | REJECT | REJECT | **SURVIVE (EXTENSION)** | ENGINEERING_COMPONENT |

## 5. Survivor(s) and why

**唯一 survivor：C3（Adaptive Intra-Window Segmented CPE）**。

保留理由（按 brief §3 五维度）：

1. **动作真实且可部署**：改 NDA 分支内部的 CPE 估计几何（块内分段粒度），对应 simulator 实际
   施加的变换（`_recovery.py:218-227` segK8 已实现，`_channel.py:53` Wiener PN 真实存在）。Gate 1
   通过：物理自由度存在。
2. **不与既有贡献重复**：CCISP/2A/2B 动作对象是 selector 阈值/region/校准/计算图 schedule；C3 在
   NDA 分支内部改相位估计几何，动作对象不同。segK8 是既有 *组件*（固定硬编码）但不是既有 *方法动作*
   （inventory 未列为 method_like kernel）。
3. **机制族不同**：CPE 估计几何 ≠ selector 鲁棒性（A 族），不触发 TL-30 换名重开禁令。
4. **可能形成完整一章**：baseline 缺陷（块内 PN floor + strong 湍流 segK8 有害）→ actual delta
   （可见量驱动块内跟踪自适应）→ 流程（复用 segK8）→ 主图（湍流×SNR×模式 BER）→ 消融（固定 vs
   自适应）→ 边界（自适应退化为场景固定）。章节骨架可画。
5. **最小实现可现有资产**：复用 `_recovery.py:218-227` 既有 segK8，新增可见量→模式映射，无需新
   testbed/信道/baseline。

**C3 的关键风险（未验证，必须 GW 验证）**：
- `[HYPOTHESIS]` "当前窗可见量（CV/有效-SNR）能区分 'AWGN-PN 主导需分段' vs 'strong 湍流主导需
  整块' 两工况"——这是 C3 存活的核心假设。若两工况在可见量上不可分，或 per-scenario 固定选择已达
  最优，C3 降为 ENGINEERING_COMPONENT（场景规则的自动化）。
- 最强廉价替代（per-scenario 固定选择）已存在代码路径；C3 必须证明可见量驱动 *稳定优于* 场景标签
  手动设，而非仅省去场景标签。这正是 GW Step 4a 要裁的。

**为何 C1/C2/C4 不存活**：C1、C4 同属 A 族 selector 机制（D040 CLOSED，TL-30 禁重开），且最强廉价
替代已吸收；C2 物理前提不存在（每窗独立 seed + 块常数 i.i.d. h），Gate 1 不过。

## 6. Next formal entry

**仅 GW 入口，不写实验任务。**

C3 的下一合法动作 = **Groundwork Step 1 问题定义**：

- Step 1（问题定义）：把 C3 的 M-C-A 写成过四判据的问题——M = NDA CPE（固定块内跟踪模式）；
  C = 块内 Wiener PN + 湍流工况使任一固定模式（整块 / segK8）在不同工况下各有失效；A = 当前窗
  receiver-visible 可见量驱动的块内跟踪粒度自适应。需回答：这相对 per-scenario 固定选择是否构成
  FR-23 意义上的问题（M 在 C 下因 A 失效），而非"自适应化"包装。
- Step 2（检索验证）：定向查 NDA/盲 CPE 块内跟踪自适应是否已被同行做过（post-survivor 定向查重，
  非本轮 broad search；brief 禁 broad search before survivor）。
- Step 3 / 3.5（精读 + 预印本验证）。
- Step 4a（可行性 Go/No-Go，维度 D）：在此才允许跑 MVE/oracle 上界（FR-20/FR-21）——裁 C3 核心假设
  （可见量能否区分两工况且稳定优于固定场景选择）；oracle 上界 <0.5 dB 直接 Kill（FR-21）。

**C3 不是 METHOD_SIGNAL、不是 Go，不能进论文正文。** 在 GW Step 4a 通过前禁止任何仿真/实验/代码
实现。survivor 数 = 1（≤2 上限满足）。

---

## 证据来源汇总（所有 `[FACT]` 的本地指针）

- selector 固定阈值 `GAMMA_EFF_TH=13.0`/`CV_MARGIN=1.10`：`projects/simulation/explore/nda-awgn-tracking-sandbox/_a4_switch_common768_30seed.py:78-79`
- selector 每窗 stateless + 读 raw `|r|²`/CV/blind `ĥ_dsp`：同文件 `:97-107`
- 每窗独立 seed 新实现：`projects/simulation/explore/nda-awgn-tracking-sandbox/run_ccisp_family1_selector_a_30seed.py:35-36`
- 信道块常数 i.i.d. h：`projects/simulation/common/_channel.py:27-32`
- Wiener 线宽 PN + CFO/Doppler：`projects/simulation/common/_channel.py:51-53,81-87`；线宽参数 `simulator/_b11_params.py:46-51`
- NDA segK8 实现 + "strong 湍流有害" + 块内 PN σ²_φ≈0.032 rad/块：`projects/simulation/common/_recovery.py:196-200,218-227`
- NDA 8th-power 模 2π/8 模糊用 tx_bits 解（BER-only，non-genie 部署缺口）：`projects/simulation/paper/ccisp2026/sections/method.tex:34-35`
- CCISP select-before-execute / 分支选择：`method.tex:36-71`；branch-route B：`internal-method-kernel-inventory.yaml:61-75`
- A 族 CLOSED（SNR-mismatch/region-retune/cand_rank/weakretune，TL-30 禁换名重开）：`.sessions/2026-07-23-research-direction-lab-longitudinal-test/decisions.md:2514-2547`（D040）
- 2A/T004 被廉价 retune 吸收、2B/T005 single-branch 与 CCISP 重复：`.sessions/2026-07-20-research-direction-lab-system/R006-lightweight-method-construction-lane-design.md:19-24`
- P06 跨帧历史 KILL（R² 0.85 > 0.32）：`internal-method-kernel-inventory.yaml:131`
- CCISP 链不 import CMA/`_gg_time`（仅 Q-CMA-FADE 独立轨道）：探索代理确认 `common/_cma.py:3`、`_gg_time.py` 仅 Q-CMA-FADE 用
- task-control validator：`python .agents/skills/research-direction-lab/scripts/validate_task_control.py T006...` → `PASS`
