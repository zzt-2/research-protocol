# [S005] 闭环版 sandbox 救援路线执行——三 Go 仍全不够格，Go1 物理根因证伪 + Go3 增益量级不够

> 2026-07-08 | 阶段: 工作对话（执行阶段 1.5 重设计，闭环 hold + power-boosted pilot）| 状态: 完成，闭环版 sandbox FAIL，H005 交主控定夺 Kill

## 目标

承接主控对话 S004 + H004 交接，本轮工作对话：执行阶段 1.5 重设计（放松前馈化到 [79] 式闭环 hold + 加 power-boosted pilot），重跑闭环版 sandbox 三方对照，守 sim-preflight v1.3.0（V2 三方 + V3 祖师爷 + V5 主线独立重算）+ D002（[79] 式闭环 hold 不撞 D006）+ D003 救援路线 3 风险。

## 记录

### 报到 + 接收方验证（Trigger 1 + Trigger 5）

读完必读清单：topic-index（15 不变量）/ H004 / S004 / decisions（D001-D003）/ 前馈版 sandbox 产出（_sandbox_results.json / _sandbox_three_way.py / _b2_params_draft.py + 阶段 0 六份规约）/ [79] L33（_B2-deep-fade-freeze-increment.md）/ D006（2026-06-20-problem-driven-redirection/decisions.md:313-355）/ 阶段 0.3-0.5 文档 / sim-preflight v1.3.0 + mve-validation + interrupt / thesis-lessons TL-26/27/30/31/32/33。

**接收方验证 5/5 PASS**（含 1 个关键红旗 + 2 个 nuance）：

| 项 | 核查 | 结论 |
|---|---|---|
| D002 前馈化降级合理 | 精读 D006:313-355 + 阶段 0.3 §3.1 | ✅ PASS（[79] 式闭环 hold 不撞 D006）|
| sandbox 物理根因 | Explore agent 核查 _sandbox_three_way.py:114-121 freeze_compensate_block 前馈开环 | ✅ PASS + 🔴 **n_recover 度量退化红旗**（A==C 是 fallback 伪相关，非真实恢复一致）|
| power-boost 是核心物理解 | fade 块 BER 斜率 + C/A 对照 | ✅ PASS（弱赢 weak 高 SNR，moderate 反转）|
| D003 救援路线 3 风险 | decisions.md D003 §137-151 | ✅ PASS |
| 当前范围未违反"明确不含" | explore 私有 `_` 前缀 | ✅ PASS |

### 步骤 1：阶段 0.3 重定性闭环 hold + 0.4 重审公平对照

**0.3 闭环 hold 架构设计**（`_architecture_decision_closed_loop.md`）：
- [79] 式闭环 hold = block 级闭式估计（nda_ml M₀=8 / da_ml pilot）+ 跨块 PI 环路平滑 + fade 期 hold
- D006 不撞论证：鉴相器估载波相位 φ 不估 φ_T，环路 TF 固定不感知湍流，门控用功率
- V3 祖师爷实现一致性：跨块 (integrator, vco_phase) 状态 + fade 期冻结 + 恢复自然收敛
- **n_recover 度量修复**：v2（band 30% + 滑窗均值），修前馈版 ±10% 退化

**实现迭代（C6 公式核对发现的关键 bug）**：
- 第一版用逐符号 DPLL（4th-power 鉴相）→ smoke test A/C BER=0.25（随机猜测级）
- **根因**：4th-power 对 16-APSK 不对（需 M₀=8），DD 鉴相在高 BER 不稳
- **修正**：改用 block 级闭式估计（nda_ml M₀=8 升幂 / da_ml pilot）+ 跨块 PI 平滑
- 修正后 BER 合理（A/C 0.09-0.18，B pilot+boost 0.008-0.18）

**0.4 power-boost overhead 理论预期**（TL-20/TL-27 核算，`_fair_comparison_closed_loop.md`）：
- fade 块内 trade-off 净正（β=2 pilot SNR +2.04dB vs data SNR -0.97dB → 净 +1.07dB）
- 全帧 overhead 小（仅 fade 期 boost，β=2 时 +0.16dB）
- 全局 net fair gain 边缘区（-0.09~+0.16dB），不触发红线 Kill
- **门控结论**：net 不显著 <0，可跑 sandbox 实测

### 步骤 2：阶段 0.5 加参数 + 重跑闭环版 sandbox

**参数扩**（`_b2_params_closed_loop.py`，TL-26 溯源）：
- DPLL 环路参数：继承 params.py DPLLParams（omega_n=8e6 / zeta=√2/2）
- power_boost_factor β=2.0（3dB）：来源 DVB-S2 pilot boosting + 物理量级核算最优
- **[79] 全文付费墙不可得**（仅摘要），数值参数无法从 [79] 提取，[79] 仅作机制定性背书

**闭环版 sandbox 全量 21 点**（`_sandbox_closed_loop_three_way.py` + `_sandbox_closed_loop_results.json`，8.1s）：
- alpha=1.0（nonfade 纯跟踪当前块，PI 平滑在 nonfade 引入滞后抵消 fade 优势）
- A 闭环完全 hold / B 闭环 pilot 全程+boost / C 闭环双模+boost

**V5 主线独立核查结论**（三 Go 评估）：

| Go 判据 | 结果 | 详情 |
|---|---|---|
| **Go1 动态恢复 C<A** | ❌ **FAIL** | nR_A==nR_C 全 21 点（0/21 有差异）|
| **Go2 范围扩展** | ❌ **FAIL** | A/C 全 21 点都不可达 HD-FEC（BER 0.08-0.30 >> 3.8e-3）|
| **Go3 稳态 BER fair gain** | ⚠️ **PARTIAL** | weak/moderate 高 SNR fair gain +0.12~+0.42dB，**<0.5dB 阈值**；strong/低 SNR <0 |

### Go1 物理根因证伪（关键发现）

**TL-22 物理前提核查**：闭环 hold 救援路线的核心假设是"fade 期 hold 的相位在 fade 结束后失效，需要恢复过程"。验证：

- hold 相位误差（fade 结束后第 1 块实际相位 vs hold 值）：均值 **0.0515 rad**，max 0.13 rad
- 16-APSK 最小相位间隔 π/8 = 0.39 rad → 0.05 rad 误差误码率增量 <1%
- **物理根因**：当前信道模型下，doppler_phase 是连续慢变的，fade（GG 块衰落 h）只影响幅度不影响相位轨迹 → hold 的相位在 fade 结束后仍然有效 → 无恢复过程

**结论**：Go1 动态恢复在当前信道模型下**物理上不成立**。这不是架构问题（前馈/闭环都一样），是信道模型的物理特性——fade 是幅度衰落，相位是独立的连续 doppler。

### 救援路线总结（跟前馈版结论一致）

**闭环版 + power-boost 确实让 C 赢 A**（fade 块 pilot 比 hold 好，Go3 raw gain +0.12~+0.58dB），但：
1. **Go1 物理不成立**（fade 期相位不漂移，hold 够好）
2. **Go2 无 HD-FEC 可达空间**（A/C 全部 BER >> 3.8e-3）
3. **Go3 增益量级不够**（最高 +0.42dB < D005"赢几 dB" + INVARIANT 13 饱和池警示）

**三 Go 全不够格**（跟前馈版一致）。闭环 hold + power-boost 救援路线未能翻盘。

### D003 救援路线 3 风险实测结果

| 风险 | 实测结果 |
|---|---|
| 风险 1 power-boost overhead trade-off | net fair gain +0.12~+0.42dB（weak/mod 高 SNR），**物理可行但量级不够** |
| 风险 2 跟 [79] 差异够格 | C 赢 A 但仅 +0.4dB，**不够 D005"赢几 dB"** |
| 风险 3 sat.1553 口径 | 守住（未引 sat.1553 +1dB，独立 MVE）|

### 🔴 Go1/Go3 再查：假阳性证伪（用户要求"再查一遍"后的决定性发现）

用户问"能大大方方讲吗"后，再查 Go1 物理根因 + Go3 提升真实性。**两轮再查推翻了本 session 前面报告的所有 Go3 数据**。

**再查 1：Go1 hold 误差（修正前面 0.05rad 错论据）**

前面报"hold 误差 0.05 rad，hold 够好"——**测错了**。用块平均相位测，把残余 CFO（F_RESIDUAL=1MHz）在块内产生的 0.64 rad/sym 斜率平均掉了。

按符号级重测：hold 相位误差均值 **0.32 rad**（max 0.79 rad），来源是残余 CFO 块内斜率 + 块间跳变。但 hold 误差大**不代表 Go1 成立**——Go1 不成立的真实原因是"非 fade 期 blind 每块独立重新锁定（块内闭式估计），fade 结束后一块即重新锁定，无收敛惯性可缩短"（论据修正，结论不变）。

**再查 2：Go3 提升真实性——🔴 假阳性证伪（决定性）**

发现 blind 估计在高 SNR BER 饱和（0.09 下不去），疑似 bug。做决定性分解实验（weak 24dB，400 块，逐块分类，**同一 h 均衡同一信道实现**）：

| 处理 | fade 块 BER | 非 fade 块 BER |
|---|---|---|
| blind（nda_ml M₀=8）| **0.00322** | **0.00122** |
| pilot（da_ml）| 0.00330 | 0.00123 |
| hold（常数补偿）| 0.00466 | — |

**决定性发现**：fade 块 **pilot 对 blind 没有任何优势**（0.00330 vs 0.00322，pilot 微输）。blind 在非 fade 块完全正常（0.00122 随 SNR 正常下降），无 bug。

**前面 Go3 "+0.4dB" 是假的**：`_sandbox_closed_loop_three_way.py` 的 `c2_ber_fade_da_ml` 用 **pilot h 均衡**，`c2_ber_fade_closed_hold` 用 **blind h 均衡**——h 均衡口径不一致（pilot h 本身比 blind h 准），不是公平对照。同一 h 均衡下 pilot ≈ blind，Go3 增益消失。

**根因**：fade 块 BER 高的主因是 SNR 低（信号弱），pilot 和 blind 都受同样的 SNR 限制——pilot 已知符号去调制，但噪声仍在，低 SNR 下估计精度都差。B2-Q2 核心命题"fade 期 pilot-aided fallback 比 blind freeze 更优"在当前信道 + SNR 区间**不成立**。

**B2-Q2 没有真实提升**（不是量级问题，是提升不存在）。前馈版 +0.02dB / 闭环版 +0.4dB 都是 h 均衡口径不一致的假阳性。

### Kill 最终依据（交用户定夺）

1. **Go1 动态恢复不成立**（非 fade 期 blind 一块锁定无惯性，不是架构问题）
2. **Go3 提升是假阳性**（h 均衡口径 bug，公平对照下 pilot≈blind）
3. **Go2 无 HD-FEC 可达空间**
4. B2-Q2 核心命题（pilot fallback 优于 blind freeze）在当前信道实证不成立

## 决策引用

- D001（继承）：开 B2-Q2 专题
- D002（继承）：前馈化降级，[79] 式闭环 hold 不撞 D006
- D003（继承）：救援路线 + 3 风险
- 无新建决策（Kill/继续由主控+用户定夺，红线"禁替用户决定 Kill"）

## 范围确认

- 本轮是否在 scope boundary 内：**是**（阶段 1.5 重设计 + 重跑 sandbox）
- 守 executor 角色边界：产实测数据 + Go/Kill 建议，不自己决定 Kill
- 守 profile "Go/Kill 是用户的"：三 Go FAIL 后建议 Kill，交主控+用户
- **诚实交代**：本 session 前半段报告的 Go3 +0.4dB 是 h 坞衡口径 bug 导致的假阳性。用户追问"能大大方方讲吗"后再查发现（再查 2）。前面的 S004 V5 核查也没抓到这个口径问题（V5 只核查了 n_recover 全等 + fair gain 算式，没核查 c2 子集 BER 的 h 均衡是否一致）——这是 V5 的盲区，记教训

## 后续

### 主控对话跟进点（H005 交接）

1. **Go3 假阳性**是否被认真对待（h 均衡口径 bug，公平对照下 pilot≈blind，B2-Q2 无真实提升）
2. **Go1 物理根因**（非 fade 期 blind 一块锁定无惯性）
3. **Kill 决策**：核心命题实证不成立 + 无真实提升 → 建议 Kill，交用户定夺

### 产出物清单（本轮交付）

1. ✅ `_architecture_decision_closed_loop.md`（闭环版架构决策 + D006 不撞 + 度量修复设计）
2. ✅ `_fair_comparison_closed_loop.md`（power-boost overhead 理论预期表 + 公平对照更新）
3. ✅ `_b2_params_closed_loop.py`（B2Params 扩 power_boost + DPLL 参数，TL-26 溯源）
4. ✅ `_closed_loop_freeze.py`（闭环 freeze 实现 + n_recover v2 度量修复）
5. ✅ `_sandbox_closed_loop_three_way.py`（闭环版三方对照脚本）
6. ✅ `_sandbox_closed_loop_results.json`（21 点结果 + meta 字段）
7. S005（本文件）
8. H005（交主控定夺 Kill，下一步写）
