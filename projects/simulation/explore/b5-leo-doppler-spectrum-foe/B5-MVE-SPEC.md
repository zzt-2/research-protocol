# B5 短时谱 FOE 三方对照 MVE 规格（契约 + 理论预期）

> 来源: S004（sandbox 完成）→ 对话 4 起草 | 框架: gw-feasibility.md §D
> 日期: 2026-07-08 | 执行方式: 子 agent 写 MVE 脚本 + 运行 + 返回数字，主线独立核查
> 增量形态: 范围扩展（15× 理论 / 14.4× 实测）+ 残频 σ（路径 C 鲁棒性）+ 星历残差鲁棒性

---

## 0. 定位（一段话）

**这是 Step 4a 维度 D MVE**（FR-22 GW 流程强制门控合规：当前在 GW Step 4a 维度 D，sandbox 已 PASS 路径 C 前提，MVE 验证算法正确性 + 星历残差鲁棒性 + consistency）。

B5-Q1 的够格路径**不是 dB 增量**，是**范围优势**（INVARIANT 11）：
- 范围扩展：B5 ±4.5GHz vs 传统 FFT FOE ±312.5MHz = 14.4× 实测（≥10× 门控 PASS）
- 路径 C 鲁棒性：湍流下残频 σ max 16.20MHz << 140MHz 门控（裕度 123.8MHz）
- 绝对指标：残频 σ 6-16MHz（对标 BUPT Arria 10 FPGA demo 会议模板，会议门槛够格）

**Go/Kill 判据分离（FR-25，INVARIANT 4）**：
- **Go 标准**（赢传统 baseline）：B5 范围扩展 ≥10×（FR-15 目标维度）+ B5 > Random（FR-14 先验基线）+ 路径 C 湍流下残频 σ <140MHz
- **Kill 标准**：V1 公式不符 / V3 祖师爷警报（B5 vs [60] Leven 数学同族持平查后仍持平）/ 星历残差扫描残频 σ 超 140MHz / consistency FAIL
- **oracle 上界（FR-21）不当 Kill 门**（D005 务实路线降级，INVARIANT 2）

---

## 1. 核心假设（MVE 要验证的）

**在 2.5 GBaud PM-QPSK 单偏振简化 + 确定性 Doppler 频偏 + GG 湍流 + AWGN 信道下，B5 短时谱 FOE（分块 FFT + 正负功率谱面积比 Rp-n + α=6×10⁸ + 星历预测预补偿 + 3-4 次迭代）相对传统 FFT FOE（4 次幂 blind QPSK 找谱峰，主 baseline）的二维 fair gain：**

- **维度 1（范围扩展）**：≈ 14.4×（±4.5GHz / ±312.5MHz，sandbox 已验证 19/19 vs 1/19，门控 ≥10×）
- **维度 2（残频 σ 鲁棒性）**：湍流下 max 16.20MHz << 140MHz 门控（sandbox 27/27 PASS，裕度 123.8MHz）
- **维度 3（星历残差鲁棒性，sandbox 遗留债务）**：星历残差 ∈ [0, 100MHz] 时 B5 残频 σ 应线性增长但仍 <140MHz

**机制支撑（sandbox S004 闭合）**：
- α=6×10⁸ 暗 ratio 模式（Rp-n 饱和 0.5 × 6e8 = 300MHz ≈ B/8=312.5MHz）
- block ≡ ratio（按块归一化后 Rp-n 尺度无关）
- 测试信号须带限（RRC/低通），平坦白谱 Rp-n≈0 无信息
- B5 大频偏靠星历预测预补偿 + 迭代（纯 FFT 仅 ±1.18GHz，星历+迭代覆盖 ±4.5GHz）

---

## 2. TL-20 理论预期表（MVE 跑之前必须写明，偏离即查）

> **TL-20（INVARIANT 9）**：MVE 跑之前必须写明理论预期表。sandbox 已有实测数据可校准预期锚点。
> 偏离处理：实测偏离预期 >阈值 → 立即查代码/参数，不"再凑凑看"。

### 2.1 残频 σ 随 SNR 预期（固定 weak 湍流 + 1GHz 频偏）

| 指标 | 预期 B5 | sandbox 实测（校准锚点） | 偏离触发 |
|------|---------|-------------------------|---------|
| 残频 σ @ SNR 6dB | 6.9-9.2MHz 量级 | weak 6.95MHz / moderate 7.56MHz / strong 13.28MHz | MVE 偏离 sandbox >3× → 查 bias 校准 + RNG seed |
| 残频 σ @ SNR 13dB | 6.4-13MHz 量级 | weak 6.47MHz / moderate 8.12MHz / strong 14.14MHz | 偏离 >3× → 查 B5Params 字段是否改动 |
| 残频 σ @ SNR 20dB | 6.4-14MHz 量级 | weak 6.45MHz / moderate 8.22MHz / strong 14.20MHz | 偏离 >3× → 查湍流实现 |

### 2.2 残频 σ 随湍流强度预期（固定 SNR + 频偏）

| 湍流 | 预期 B5 σ 范围（MHz）| sandbox 实测 max（MHz）| 门控 140MHz |
|------|---------------------|----------------------|-------------|
| weak | 9.25-10.33 | 10.33 | ✅ 裕度 129.7MHz |
| moderate | 10.36-13.03 | 13.03 | ✅ 裕度 127.0MHz |
| strong | 13.76-16.20 | 16.20 | ✅ 裕度 123.8MHz |
| **MVE 预期** | 同 sandbox 量级（6-16MHz）| — | **>140MHz → 红线警报（路径 C 崩塌）**|

### 2.3 范围扩展预期

| 指标 | 预期 B5 | 预期 baselines | 偏离触发 |
|------|---------|---------------|---------|
| 捕获范围 | ±4.5GHz（星历+迭代）| ±312.5MHz（fft_foe/leven）| B5 <±4GHz → 查星历预测逻辑 |
| 收敛点/19 | 19/19 | 1/19（仅 f=0）| B5 <15/19 → 查迭代收敛 |
| 范围扩展 vs fft_foe | 14.4× | 1× | **<10× → 路径 C 不成立** |
| B5 纯 FFT（无星历）| ±1.18GHz | — | >±2.5GHz → 查 fs 歧义 |

### 2.4 星历残差扫描预期（sandbox 遗留债务，MVE 新增）

> sandbox 模拟星历预测完美（ephemeris_pred=f_true，残频≈0+噪声）。MVE 需测星历预测残差对 B5 残频 σ 的影响。

| 星历残差（MHz）| 预期 B5 残频 σ（MHz）| 门控 | 偏离触发 |
|---------------|---------------------|------|---------|
| 0（完美，sandbox）| 6-16（同 sandbox）| <140MHz | 偏离 sandbox >3× → 查 RNG |
| 50 | 16-60（线性增长）| <140MHz | >140MHz → 路径 C 前提受限 |
| 100 | 30-120（线性增长）| <140MHz | **>140MHz → 路径 C 前提受限，重评估范围优势边界** |

**预期理由**：星历残差直接加到 B5 估计误差上（残频 = 估计误差 + 星历残差），σ 应线性增长。裕度 123.8MHz（sandbox max 16.20MHz）应足够吸收 100MHz 星历残差，但需实测确认。

### 2.5 V3 祖师爷预期（B5 vs [60] Leven 非同族核查）

| 对照 | 机制 | 预期残频 σ | V3 警报判据 |
|------|------|-----------|------------|
| B5 | 频域功率谱面积比 Rp-n（积分量）| 6-16MHz | — |
| [60] Leven | 时域差分相位增量（4 次幂 + 差分）| 0.4-40MHz（范围内）| — |
| **B5 vs [60] Leven** | 频域积分 vs 时域差分，机制正交 | **不应持平（残频 σ 差 >5%）** | **持平 <5% → 查数学同族性，不当合理接受** |

**V3 预期理由**：
- B5 是**频域**功率谱面积比（P+ − P− 积分），靠谱的不对称性估频偏
- [60] Leven 是**时域**差分相位增量（r[n+1]·r[n]* 升 4 次幂 → 相位/4），靠符号间相位旋转估频偏
- 两者估计域正交（频域 vs 时域），数学机制不同族，残频 σ 不应持平
- **若持平**：两种可能 (a) 数学同族（创新性受质疑）(b) 对照不公平（bug/参数掩盖）

**V3 特殊情况**：sandbox 实测 [60] Leven 在 1GHz 频偏时残频 σ=2.9-3.9MHz（范围内），B5 残频 σ=6.5MHz。两者**不持平**（B5 粗 CFO 残频 > [60] Leven 精细估计，符合机制差异）。MVE 需在公平条件（同频偏范围）下复核。

---

## 3. FR-11 架构摘要（B5 是前馈估计器非 DRL，适配）

> FR-11 要求 MVE 必含架构摘要。B5 是前馈频域估计器非 DRL，DRL 框架的"动作空间/决策粒度/奖励语义"适配为：

| 架构维度 | DRL 框架原义 | B5 适配（前馈估计器）|
|---------|-------------|---------------------|
| **动作空间** | agent 输出的离散/连续动作 | 频偏估计值 Δf_est（连续，Hz）|
| **决策粒度** | 每步/每帧/每块决策 | 块级（n_fft×n_blocks = 16×1024 = 16384 样本一次估计）|
| **对比范式** | vs baseline 的奖励曲线 | 三方对照（B5 / fft_foe / [60] Leven）的残频 σ + 范围 + BER |
| **奖励语义** | reward = 任务目标 | 粗 CFO 残频最小化（|f_true − f_est| → min）|

**FR-12 MVE→Formal 架构差异门控**：MVE 脚本（explore/）vs Formal 脚本（experiments/，consistency 对照）架构比对。差异影响对比机制则重验证。B5 的 consistency：MVE 脚本与 Formal 脚本跑同一组参数 + 同一 seed，输出 bit-exact 一致（实现同步检查，非算法正确性证明）。

---

## 4. 三方对照架构（sim-preflight v1.3.0 C7 + V2，核心）

> sandbox 已实现三方对照（S004），MVE 复用 + 扩展。完整架构见 `_sandbox_three_way.py`。

| 方 | 角色 | 核心实现 | 公式源（V1）|
|----|------|---------|------------|
| **B5 短时谱 FOE** | 候选方法 | 分块 FFT + Hanning + 均值滤波 + Rp-n + α·Rp-n + 星历预测 + 3-4 次迭代（normalize_mode='ratio'）| B5 锚 content.md L73/79/81/83（PDF→md 重建，C6 标注）|
| **传统 FFT FOE** | 主 baseline（FR-15 目标对手）| 4 次幂 blind QPSK 找谱峰（common.fft_foe，1-sps）| common/_recovery.py:37 |
| **[60] Leven Mth-power** | 祖师爷方（V3 警报）| 差分 → 4 次方 → 500 样本求和 → 相位/4（时域差分，1-sps）| [60] Leven content.md L55-65 |

**三方对照公平性**：
- TL-13 共用信道：三方法都用 `generate_shared_realization` 同一 QPSK+GG 湍流+Doppler 实现
- 三方法都前馈归一化：B5 ratio / fft_foe 4 次幂（幅度不敏感）/ leven ratio
- 三方法扫同一 Doppler 范围（±4.5GHz 全量程）
- 双工作点：BER 1e-3（B5Params.BER_TARGET_B5）+ HD-FEC 3.8e-3（B5Params.HD_FEC_THRESHOLD_B5）
- 同一 BER 计算路径：三方法各供 fest，rx_comp = rx_raw · exp(−j·fest·k)，公平隔离 FOE 质量

**Random 先验基线（FR-14）**：B5 > Random。Random 估计器 fest=0（不估），残频=f_true。B5 19/19 收敛 vs Random 会全失败（sandbox 已确认，MVE 复核）。

---

## 5. V1-V6 算法正确性验证清单（sim-preflight v1.3.0，MVE PASS 判 Go 前全过）

> sandbox 已过 V1/V2/V5/V6，MVE 补 V3（祖师爷警报）+ V4（参数变更重审）。

| # | 验证项 | sandbox 状态 | MVE 动作 |
|---|--------|-------------|---------|
| **V1** | 公式逐项核对（C6）| ✅ PASS（C6 重建标注式 1-4，PDF→md 丢失已标红）| 复核（公式不变）|
| **V2** | 三方对照（C7）| ✅ PASS（B5/fft_foe/leven 三方）| 复用 + 加星历残差扫描 |
| **V3** | 祖师爷警报（C8）| ⬜ 待补（B5 vs [60] Leven 非同族核查）| **MVE 新增**：B5 vs [60] Leven 残频 σ 持平 <5% → 查数学同族性 |
| **V4** | 参数变更重审 | ⬜ 待补（sandbox 无参数变更）| **MVE 新增**：星历残差扫描 = 参数变更（ephemeris_pred 从完美→有残差），重审算法对错 |
| **V5** | 子 agent 归因核查 | ✅ PASS（主线独立 grep 重算）| 复核（子 agent 跑 MVE + 主线独立核查）|
| **V6** | 读原文数值（FR-26）| ✅ PASS（B5Params 20 字段全溯源 content.md 行号）| 复核 |

**V3 祖师爷警报具体动作**：
1. B5 vs [60] Leven 在公平条件（同频偏范围 0.5/1/2GHz，同 SNR，同湍流）下对照残频 σ
2. 若 |B5 σ − Leven σ| / max(B5 σ, Leven σ) < 5% → 触发警报
3. 警报响应：查数学同族性（B5 频域积分 vs Leven 时域差分）+ 查对照公平性（bug/参数掩盖）
4. **不当合理结果接受**（NDA-ML D-008 教训：vs VV 持平当合理接受长达 2 session）

**V4 参数变更重审具体动作**：
1. 星历残差从 0（完美）→ [50, 100]MHz（有残差）是 CRITICAL 参数变更
2. 重审：星历残差影响哪些算法路径？（B5 估计误差 = FFT 估计误差 + 星历残差）
3. 原参数（完美星历）下的结论（路径 C PASS）在新参数下还成立吗？（需实测确认）
4. 是否需要补 sandbox 验证新参数下算法对错？（MVE 星历残差扫描即此验证）

---

## 6. 星历残差扫描设计（sandbox 遗留债务，MVE 新增）

> sandbox 模拟星历预测完美（ephemeris_pred=f_true，残频≈0+噪声）。MVE 需测星历预测残差对 B5 残频 σ 的影响（H004 已知债务）。

**设计**：
- 扫星历残差 ∈ [0, 50, 100] MHz（3 点，模拟真实星历预测残差量级）
- 固定 SNR 13dB + weak 湍流 + 1GHz 频偏（sandbox 主测条件）
- 每点 20 seed 统计残频 σ
- 判定门控：残频 σ <140MHz（路径 C 前提不崩塌）

**实现**：
- `est_b5(..., ephem_residual=residual)`：星历预测把 f_true 预补偿到残频 residual
- sandbox 是 `ephem_residual=0`（完美星历），MVE 扫 `ephem_residual ∈ [0, 50, 100]MHz`
- 残频 σ = std(f_true − fest) 跨 seed

**预期**：残频 σ 线性增长（星历残差直接加到估计误差），但 <140MHz（裕度 123.8MHz 足够）。

---

## 7. consistency bit-exact（MVE vs Formal，实现同步检查）

> consistency 是"实现同步检查"（MVE 和 Formal 跑同一套代码路径），**不是"算法正确性证明"**（NDA-ML D-008 教训：两套都漏同一 bug 时 consistency 假 PASS）。

**设计**：
- Formal 脚本 = MVE 脚本的"正式版"（转正进 experiments/，去掉 `_` 前缀 + 探针标注）
- MVE vs Formal 跑同一组参数 + 同一 seed，输出 bit-exact 一致
- 判定：残频 σ / fest_hz / BER 三项 bit-exact（浮点 0 ulp 差异，或相对误差 <1e-15）

**实现路径**：
1. MVE 脚本 `mve_b5_short_time_spectrum.py`（explore/，带 `_` 前缀探针 + meta 字段）
2. Formal 脚本 `sc_b5_short_time_spectrum.py`（experiments/，MVE 通过后转正）
3. consistency 检查：MVE vs Formal 跑同一 seed，比较输出 JSON

**守 sim-preflight**：consistency（实现同步）+ V1-V6（算法正确性）两者都过才有效。

---

## 8. pass/fail 标准（预定义，D005 务实路线 + FR-25 Go/Kill 分离）

> 守 D005 务实路线（INVARIANT 2 最高优先级）：Go 判据=赢传统未优化 baseline（传统 FFT FOE）范围维度；FR-21 oracle 上界降级为参考不当 Kill 门。
> 守 FR-25 Go/Kill 标准分离：Go 标准=赢传统 baseline / Kill 标准=V3 警报或 MVE FAIL 或星历残差崩塌。

主指标：**范围扩展 + 残频 σ 鲁棒性 + 星历残差鲁棒性**

| 判定 | 条件 | 含义 |
|------|------|------|
| **Go (§D PASS)** | 范围扩展 ≥10×（FR-15）AND B5 > Random（FR-14）AND 路径 C 湍流 σ <140MHz AND 星历残差扫描 σ <140MHz AND V1-V6 全过 AND consistency PASS | B5 可进 Step 5（转正 common + experiments）|
| **Conditional Go** | 范围扩展 + 路径 C 成立但星历残差扫描接近 140MHz 边界（100-140MHz）| 范围优势受限，记录边界条件，转 Step 5 但标注星历残差上限 |
| **Kill/Fail** | 范围扩展 <10× OR V3 祖师爷警报触发（B5 vs [60] Leven 持平查后仍持平）OR 星历残差扫描 σ >140MHz OR V1 公式不符 OR consistency FAIL | 核心假设不成立，B5 降级/排除，报红线警报 |

**Go/Kill 判据分离（FR-25）**：
- **Go 标准**：赢传统未优化 baseline（传统 FFT FOE）范围维度 14.4×——会议门槛放宽（D005），范围/绝对指标算够格
- **Kill 标准**：V3 祖师爷警报 / 星历残差崩塌 / V1 公式不符 / MVE FAIL
- **oracle 上界（FR-21）不当 Kill 门**：B5 是范围优势非 dB 增量，CRB 不适用

**MVE 结果需主控对话做 Go/Conditional/Kill 判断**（profile 画像：不宜主线一口气塞完，MVE 跑数后主控对话单独判断）。

---

## 9. 扫描设计（MVE 主表 + 星历残差扫描）

### 9.1 MVE 主表（复用 sandbox + 加 V3 复核）

- 调制：QPSK 单偏振（B5 锚 PM-QPSK 简化，MVE 隔离 FOE 增量）
- 符号率：2.5 GBaud（B5 锚论文场景，B5Params.R_SYM_B5）
- 信道：GG 湍流（weak/moderate/strong）+ AWGN + 确定性 Doppler 频偏（f_dot=0）
- Doppler 扫描：±4.5GHz 全量程（19 点 × 0.5GHz step，sandbox 已有）
- SNR：6/13/20 dB（3 点，覆盖 B5 锚区间）
- 每点：20 seed（蒙特卡洛，seed 固定可复现）
- 三方：B5（星历+迭代）/ fft_foe / [60] Leven
- 输出：每方每 (turb, snr, f_D) 的 {fest_hz, residual_std_hz, ber}

### 9.2 星历残差扫描（MVE 新增）

- 固定条件：SNR 13dB + weak 湍流 + 1GHz 频偏
- 扫星历残差 ∈ [0, 50, 100] MHz（3 点）
- 每点 20 seed 统计残频 σ
- 输出：每星历残差点 B5 残频 σ + 门控判定（<140MHz PASS）

### 9.3 V3 祖师爷警报复核（MVE 新增）

- 公平条件：同频偏范围 [0.5, 1, 2] GHz + 同 SNR 13dB + 同湍流 weak
- B5 vs [60] Leven 残频 σ 对照
- 警报判据：|B5 σ − Leven σ| / max < 5% → 触发

---

## 10. 执行约束

- **时间预算 ≤ 900s**（AGENTS.md 子 agent 上限）
- 脚本放 `projects/simulation/explore/b5-leo-doppler-spectrum-foe/mve_b5_short_time_spectrum.py`
- **信号生成三方共用**（TL-13）：同一 QPSK 2.5 GBaud 信号 + 相同 seed + 相同 Doppler 扫频
- **B5Params 从 params.py import**（禁硬编码）
- **信道从 common/_channel.py import**（TL-13，禁自建）
- **前馈开环不撞 D006**（INVARIANT 13）：B5 normalize_mode='ratio'，禁环路 TF
- **不污染 common**（INVARIANT）：explore 探针不进 experiments，MVE + consistency 双通过才转正
- 输出 JSON 含 meta 字段（仿 sandbox）+ V1-V6 验证记录 + 星历残差扫描 + consistency 检查
- 环境：`~/.venvs/torch/bin/python`（AGENTS.md 约定）

---

## 11. 子 agent 返回（≤500 词摘要）

返回必须含：
1. MVE 主表关键点（范围扩展 + 湍流下残频 σ max，对标 sandbox 14.4× + 16.20MHz）
2. 星历残差扫描结果（0/50/100MHz 三点残频 σ + 门控判定）
3. V3 祖师爷警报判定（B5 vs [60] Leven 残频 σ 差，是否 <5%）
4. consistency bit-exact 判定（MVE vs Formal 是否 bit-exact）
5. 任何偏离 TL-20 预期的点（标注"DEVIATION"）
6. 一句话判定建议（Go/Conditional/Kill）+ 理由（但**最终 Go/Kill 由主控对话判断**，子 agent 只给建议）
7. 环境用哪个 python，运行耗时

不返回：完整曲线数据（存 JSON）、完整代码（存脚本文件）。主控对话读 JSON 复核（V5 主线独立重算归因）。

---

## 12. 转正流程（MVE + consistency 双通过后）

1. `short_time_spectrum_foe` + `short_time_spectrum_foe_iterate` 进 `common/_recovery.py`（去 `_` 前缀）
2. `leven_mthpower_foe` 进 `common/_recovery.py`（祖师爷对照转正）
3. B5Params 已在 params.py（S004 落盘）
4. MVE 脚本转 `experiments/`（去 `_` 前缀）
5. 写 S005 session note + H005 handoff（MVE PASS 则交 Step 4a 收尾 / FAIL 则报红线警报）

**转正守"双通过才进 common"**（INVARIANT：MVE + consistency 都过）。
