# [S024] PROMPT-022 执行：改动1（物理发散判据驱动 ML 重训练）MVE — KILL

> 2026-07-15 | GW Step 4a 维度 D MVE（路线 A 改动1 验证） | 状态：完成，KILL，回传主控
> 来源: S017 段 2（改动1 新颖性 PASS）+ D028（Q-DP4 整体 Kill，路线 A 唯一存活）+ 主控 PROMPT-022 派发

## 目标

验证改动1（用物理发散判据当 ML 重训练触发信号）能否把 Q-CMA-FADE 方法层从"弱"升"中"，决定是否进 Contract。

## 记录

### 改动1 定义（S017 段 2）

核心创新：用物理发散判据（CMA 权重范数 / 恒模代价突增 / 权重漂移）当 ML 重训练的触发信号。区别于 Qin/Kulmer/Li（冻结训练）、Nasr（固定网格预训练）、B2/JR-CMA（物理阈值 gate 经典 DSP）。

### TL-20 理论预期（实验前写）

关键物理洞察（来自 D013/D014/D027）：
- D013：swap 时 |w| 稳定（1.4142→1.4166 不发散）
- D014：swap 是权重跳盆地（非数值发散）
- D027 V3a：clean swap 时 J_CMA 不突增（swap 盆地恒模，输出互相关≈0）
- 预期：基于恒模/权重范数的判据（D1/D2）物理上检测不到 swap；权重漂移判据（D3）可能有效

### 预筛选（TL-22 物理前提检查，单 seed CMA 物理量分析）

N=5M seed 1000 的 CMA 物理量轨迹分析：

| 判据 | 触发率 | 评价 |
|---|---|---|
| D1 \|w\|>2×init | 80.8% | 太高，退化成在线更新 |
| D1 \|w\|>5×/10×init | 0% | 从不触发（D013 swap 不发散）|
| D2 J_CMA>2×/5×/10×baseline | 0% | 从不触发（D027 clean swap 恒模）|
| D3 Δ\|w\|>0.1×w_train | 52.7% | 偏高 |
| D3 Δ\|w\|>0.3×w_train | 21.7% | 合理范围 |
| D3 Δ\|w\|>0.5×w_train | 10.3% | 合理范围 |

**结论**：D1/D2 物理上无效（0% 触发），D3 是唯一有效判据。脚本据此简化（D1/D2_5.0 复用 B，D3 测 0.3/0.5）。

### 验证1 结果（N=5M, 5 seeds, f_G=30, SOP=4e-7, strong, 20dB, QPSK）

**整体 KILL**。所有 D 方法 PI-BER 精确等于 B（ML 训练一次），无任何改善。

| 方法 | PI-BER mean | ±std | fixed BER | excess PI vs oracle |
|---|---:|---:|---:|---:|
| A standard-CMA | 0.02096 | 0.02690 | 0.20540 | 0.01259 |
| **B ML 训练一次** | **0.01028** | 0.01606 | 0.49529 | 0.00191 |
| C ML 固定周期重训练 | 0.01626 | 0.02204 | 0.01626 | 0.00789 |
| D1 \|w\|>5×init | 0.01028 | 0.01606 | 0.49529 | 0.00191 |
| D2 J_CMA>5×baseline | 0.01028 | 0.01606 | 0.49529 | 0.00191 |
| D3 Δw>0.3×w_train | 0.01028 | 0.01606 | 0.29541 | 0.00191 |
| D3 Δw>0.5×w_train | 0.01028 | 0.01606 | 0.39533 | 0.00191 |
| oracle | 0.00837 | 0.01312 | 0.00837 | 0.00000 |

Per-seed PI-BER：

| seed | A(stdCMA) | B(train_once) | C(periodic) | D3_0.3 | oracle |
|---|---|---|---|---|---|
| 1000 | 0.03932 | 0.00992 | 0.02430 | 0.00992 | 0.00798 |
| 1001 | 0.00005 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |
| 1002 | 0.06533 | 0.04147 | 0.05621 | 0.04147 | 0.03386 |
| 1003 | 0.00006 | 0.00001 | 0.00077 | 0.00001 | 0.00000 |
| 1004 | 0.00005 | 0.00000 | 0.00000 | 0.00000 | 0.00000 |

### Kill 根因分析（TL-22 深查物理前提）

**根因 1（最根本）：改动1 的前提在 PI 口径下不成立**。改动1 说"ML 训练一次失效，需物理判据触发重训练"。但 D018 双口径重审已确认：N=5M ML 训练一次在 **fixed-label** 口径下 BER≈0.5（clean swap），但在 **PI 口径**下 PI≈0.005-0.01（接近 oracle）。本次 5 seeds 验证：B(训练一次) PI=0.01028 ≈ oracle 0.00837（差距仅 0.00191）。**ML 训练一次在 PI 口径下已接近最优，重训练没有改善空间**。

**根因 2：物理判据检测不到 swap**。预筛选证实 D013/D027 的物理洞察：
- D1（权重范数突增）：swap 时 |w| 不发散 → 0% 触发（5×/10×init）
- D2（恒模代价突增）：clean swap 时 J_CMA 不突增（swap 盆地恒模）→ 0% 触发
- D3（权重漂移）：唯一能触发的判据（SOP 持续旋转→Δw 增），但触发后重训练无效（因根因 1）

**根因 3：C（固定周期重训练）反而比 B 更差**。C PI=0.01626 > B PI=0.01028。原因：周期重训练每段用更少数据（1/4 test 段 ≈ 625K 符号）训练，ML 学得不如用 2.5M 训练一次。**D015 Q3-B 报的 PI=0.002 是 fixed-label 4 旋转 BER 非 PI-BER，口径不同**。

### 与 D015 Q3-B 的口径差异（重要）

D015 decisions 文字写 "Q3 对照 B 周期重训练 PI-BER=0.002"，但代码 `ml_long_seq_failure.py` Q3-B 实际用的是 `compute_ber_phase_corrected`（4 旋转相位校正 fixed-label BER），**不是 D018 的完整 2! 消歧 PI-BER**。本次用 `evaluate_outputs`（PI 口径）重新评估，C 的 PI=0.01626（非 0.002）。这是口径差异，不是代码 bug——D015 Q3-B 的 0.002 是 fixed-label 4 旋转口径下的值。

### 守纪律情况

- ✅ FR-22：改动1 是 Q-CMA-FADE 方法层升级验证（已过 A0/A'/A/D），不跳维度
- ✅ FR-25：Go/Kill 分离。Go 标准 = D 优于 B（训练一次），不用 oracle 当 Go 判据
- ✅ D018：fixed/PI 双口径并报（见上表 fixed BER 列）
- ✅ TL-20：理论预期先行（D1/D2 无效预期被预筛选证实）
- ✅ TL-22：物理前提检查（预筛选单 seed CMA 物理量 → 确认 D1/D2 物理上无效）
- ✅ TL-26：物理判据阈值标来源（|w| 阈值参考 D006 发散判据；J_CMA 阈值标基线=训练段均值）
- ✅ 隔离原则：不改 common/，新建 prompt022_modification1_mve.py

### 执行细节

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（torch 2.6.0+cu124, CUDA RTX 4070）
- 每 seed ~170-460s（取决于 D3 触发次数），5 seeds 总 ~1500s
- 优化：共享初始 ML 训练（B/C/D3 共用 deepcopy），D1/D2 0% 触发判据复用 B 结果
- 预筛选省了大量无效计算（D1 9 变体 → 1 对照，D2 3 变体 → 1 对照）

## 决策引用

- **D029 新建**：改动1（物理判据驱动 ML 重训练）KILL — 前提在 PI 口径下不成立 + 物理判据检测不到 swap
- 关联 D018（PI 口径确立）、D015（ML 长序列 fixed-label 失效）、D013（swap 不发散）、D027（clean swap J_CMA 不变）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。PROMPT-022 是改动1 的 Go/Kill 验证（topic-index 当前位置路线 A 任务）

## 后续

回传主控后由主控决策：
1. **改动1 KILL 的含义**：路线 A（Q-CMA-FADE D022 + 改动1）失去"升级方法层"的最后一张牌。Q-CMA-FADE 方法层停留在 D022 的"ML 在 N=5M/f_G=30 窄域 PI 优于 standard-CMA"（29/30，p=1.19e-6），方法层定性为"弱"（无架构创新 + 窄域 + 无重训练机制）
2. **GW Step 4a 双偏振 OSL 全部候选评估完成**：Q-DP1 Kill / Q-DP3 Kill / Q-DP4 Kill / 改动1 Kill。唯一存活 = Q-CMA-FADE 分析层（强）+ 方法层（弱，D022 窄域）
3. **主控须决定**：接受 Q-CMA-FADE 当前形态（分析层强 + 方法层弱）进 Contract/写作，还是继续找方法层升级路径（但目前所有升级路径已 Kill）

产出：
- 脚本：`projects/simulation/explore/cma-fade-divergence/prompt022_modification1_mve.py`
- 结果：`projects/simulation/results/cma-fade-divergence/prompt022_modification1_mve.json`（5 seeds + summary）
