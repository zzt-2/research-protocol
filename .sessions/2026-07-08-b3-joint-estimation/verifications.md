# Verifications — B3-Q2 子系统协同联合估计第三候选

> 专题 `.sessions/2026-07-08-b3-joint-estimation/` 的验证记录。V###/K### 条目按编号排列。

## K001: B3-Q2 Kill 验证——三切口全物理 FAIL（TL-20 理论预期 + TL-22 物理前提双重证据）

> 关联: D004（Kill 决策）/ S004（对话 3a+3b）
> 日期: 2026-07-09
> 结论: **PASS（Kill 成立）**——三切口物理 FAIL 经双重独立验证，非参数问题非实现 bug

### 验证对象

B3-Q2 三增量切口（CPE 联合 / Doppler 维度 / 星地场景）在物理量级 + CRB 理论下是否可兑现。

### 验证方法

**TL-20 理论预期（主线物理量级分析）+ TL-22 物理前提核查（子 agent 4 否决条件深查 + 主线独立 grep 核查）双重独立验证**，不依赖仿真跑数（仿真只确认物理结论，不翻盘）。

### 验证结果

#### 切口① CPE 联合——CRB ≈ 0 dB（理论证死）

| 项 | 结果 | 证据 |
|---|---|---|
| CPE joint-vs-separate CRB | ≈ 0 dB | `_stage0_1b_single_link_crb_upper_bound.md` L88："CRB 只依赖 N、γ、Δν，不依赖是否共享" |
| jphot CPE 结构 | FSTS 只做 FS+FOE，CPE 另用"相位噪声估计+DD-LMS" | jphot-L101/L243 |
| 唯一非零项 | 开销受限上界 ≤+2.4dB（开销分配论据，非估计理论增益，jphot 结构下不兑现）| 0.1b L91 |
| **结论** | **CPE 联合 ≈ 0 dB，FAIL** | 理论铁律 |

#### 切口② Doppler 维度——物理量级可忽略（TL-22 深查）

物理量级（f_dot=56 MHz/s，B5 锚 L147 LEO NEO 600km 过顶最大全 Doppler 斜率）：

| 尺度 | 2.5GBaud | 10GBaud | FOE 分辨率 | 量级差 |
|---|---|---|---|---|
| 块内（BL=20）频偏变化 | 0.45 Hz | 0.11 Hz | 610 kHz / 2.4 MHz | — |
| **块间（TS=320）频偏跳变** | **7.2 Hz** | **1.8 Hz** | **610 kHz / 2.4 MHz** | **5 个数量级** |
| 帧（8192）Doppler 相位 | 1.9e-3 rad | 1.2e-4 rad | 激光相位噪声 RMS ~1 rad | 3-4 数量级 |

**破坏缓变假设需 f_dot**：4768 GHz/s（2.5GBaud）/ 76294 GHz/s（10GBaud）= 物理 LEO 最大值的 **8.5 万 / 136 万倍**。

**4 否决条件深查（子 agent + 主线独立 grep B5 L143-149 + params.py:904 核查）**：

| 否决条件 | 推翻主线？ | 证据 |
|---|---|---|
| (a) 残余 f_dot >> 56MHz/s | **否** | 残余 ≤ 全 Doppler（物理必然）；B5 L57 残余频偏 ≤500MHz 但无残余 f_dot；主线用 56MHz/s 全量已最保守 |
| (b) 56MHz/s 用错物理量 | **否** | B5 L147 "rate of change, slope of Doppler shift" = df/dt；LEO 文献量级数十 MHz/s（600km→56, 400km→90, 1000km→29）；GHz/s 系激光频率不稳定度非轨道斜率 |
| (c) jphot 在 56MHz/s 失效 | **否** | jphot 从未测 LEO Doppler；块尺度缓变假设成立（7Hz << 610kHz） |
| (d) 公式/单位错 | **否** | π·f_dot·t² ✓（∫2π·f·t·dt）；1/(4·N_fft·T_S) ✓（FFT bin / M=4） |

**关键佐证**：B5 L149 自己的 Doppler 跟踪是"750 measurements lasting ~13 min"——分钟级跨帧，证明 Doppler 斜率只在跨帧才有意义，单帧 μs 级捕捉不到。

**结论**：Doppler 切口物理可忽略，FAIL。

#### 切口③ 星地场景——非增量（D002 已定性）

jphot 地面→星地是场景迁移非算法增量，dB 优势来自 FOE BL²（jphot 已 claim）。FAIL。

#### 综合：gain_vs_M2 ≈ 0 + §0.4.5 三层全物理 FAIL

- M3 = M2 + CPE(≈0) + Doppler(≈0) → gain_vs_M2 ≈ 0（D003 增益归因熔断触发）
- L1（全条件 gain_vs_M2>0）：CPE+Doppler 都≈0 → FAIL
- L2（Doppler crossover）：Doppler 物理可忽略，扫不出 crossover → FAIL
- L3（jphot 高 Doppler 失效）：缓变假设成立不失效 → FAIL

### 排除的假阳性

- **"实现 bug 导致假阴性"**：smoke test 9/9 PASS（5 接口功能正确），BER 统计含 QPSK 模糊 resolve。骨架 L1 FAIL（7/28）不是 bug，是物理信号
- **"f_dot_est 占位未接"**：即使接了真实 block-df 回归，物理 f_dot 下块间跳变 7Hz 测不出，回归无效
- **"T_S/baud-rate 问题"**：3a 曾怀疑，3b 物理分析推翻——T_S 方向反了（10GBaud T_S 更小 → Doppler 更小），且 T_S 非根因，物理量级在任何 baud 下都 FAIL

### 结论

**PASS（Kill 成立）**。三切口全物理 FAIL，经 TL-20 理论预期 + TL-22 物理前提（4 否决条件 0/4 推翻）双重独立验证，主线独立 grep 核查关键源文件（B5 L143-149 / params.py:904 / 0.1b CRB L88）。这不是参数问题、不是实现 bug、不是"还没调好"——是物理量级鸿沟 + 估计理论铁律。跑全量 sandbox 只确认不翻盘。

### 验证完整性声明

- ✅ TL-20 理论预期已建（物理量级分析，S004 记录）
- ✅ TL-22 物理前提已查（子 agent 4 否决条件 0/4 推翻）
- ✅ 主线独立 grep 核查子 agent 关键声称（B5 L147 f_dot / params.py:904 DOPPLER_RATE_B5 / 0.1b CRB L88）
- ✅ FR-26 证据链完整（每断言标文件+行号）
- ✅ FR-25 Go/Kill 标准分离（Kill 依据是物理量级 + CRB，非 oracle 上界，非"急于收敛"）
- ⚠️ 未跑全量 sandbox（物理已死，跑只确认不翻盘，省算力符合 D005 务实路线）
