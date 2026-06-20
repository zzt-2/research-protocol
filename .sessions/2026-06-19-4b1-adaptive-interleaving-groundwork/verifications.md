# Verifications — 4b#1 信道感知自适应交织 Groundwork 执行

> 本专题验证记录。V### 从 V001 开始。
> 每条关联 S### 或 D###，结论必须是 PASS/FAIL/PARTIAL 三选一。

---

## V001: FR-21 oracle 上界门控 — 4b#1 自适应交织 BER 增益

> 关联: D001 / S001
> 日期: 2026-06-19
> 结论: **FAIL**（4b#1 BER 维度无增益空间，触发 Kill）

### 验证假设

理想自适应交织（每个仰角用最优 B/D）相对静态交织（固定 B/D）在星地 GG 湍流下有 >0.5dB BER 增益上界。

### 验证方式（三版收敛）

**版本 1：主脚本 MC 上界**（`fr21_ub_adaptive_vs_static_interleaving.py`）
- 模型：burst 长度 Exp(Lburst) 采样，超 B·thandle 即码字错
- N=200000/仰角，仰角 20-90° 步长 5°
- 参数溯源：Cn²_ground=1.7e-14（HV 白天）/ λ=1.55µm / thandle=30bit / Lburst_ref=800@Cn²=1e-15（唐承茂 L1081-1088）
- 结果：自适应 vs 全程最优静态 B=6 BER 增益 = **-0.5 ~ -0.8 dB**

**版本 2：敏感性分析**（`fr21_sensitivity.py`）
- 扫瀑布 BER-B 陡峭度 steepness ∈ {2,4,8,16} + eta_h ∈ {0.1,0.3,0.5,1.0} + 极端仰角/湍流
- 结果：steepness=16 时 +3.3 dB——**判定为伪信号**（瀑布模型用 Lb 均值判定，忽略 burst Exp 尾部）

**版本 3：唐承茂一手校准**（`fr21_calibrated.py`，决定性）
- 用唐承茂表 4-4 实测（Cn²=1e-16→2.1e-6 / 1e-15→6.5e-6 / 1e-14→7.3e-5 BER，B=27 静态）
- 幂律拟合 BER = 3.6e6 × Cn²^0.771，残差 log10 最大 0.187
- 星地 Lburst 范围 60-428 符号，**0/15 仰角超 B=27 容量 810**
- 结果：BER 维度自适应增益 = **0 dB（理论，B=27 全程够用）**

### 结论

**FAIL**。三版收敛：唐承茂 B=27 设计余量过大（覆盖星地全部仰角），BER 由 Cn² 决定不由 B 决定，自适应无 BER 增益空间。

### 关键数据

| 项 | 值 | 来源 |
|---|---|---|
| 星地等效 Cn² 跨度 | 7.5e-17 ~ 5.4e-16（~1 数量级）| HV slant-path 计算 |
| 星地 Lburst 范围 | 60-428 符号 | 线性外推（乐观上界）|
| B=27 容量 | 810 符号 | 27 × thandle(30) |
| 超 B=27 容量的仰角数 | 0/15 | V001 校准版 |
| 唐承茂 B=27 测试 Cn² 跨度 | 1e-16 ~ 1e-14（2 数量级）| 表 4-4 |
| BER 维度自适应增益 | 0 dB（理论）| 唐承茂幂律 + B=27 够用 |

### 脚本位置

- `projects/thesis-figures/simulation/fr21_ub_adaptive_vs_static_interleaving.py` + `_results.json`
- `projects/thesis-figures/simulation/fr21_sensitivity.py` + `_results.json`
- `projects/thesis-figures/simulation/fr21_calibrated.py` + `_results.json`

### 局限性

- Lburst-Cn² 关系用线性外推（乐观上界），强湍流 GG 饱和会让 Lburst 增长变缓，但**不影响 Kill 结论**（即使 Lburst 翻倍，星地仍 << 810）
- 唐承茂幂律只有 3 点，外推到星地 Cn² 范围（比唐承茂测试低 1-2 数量级）有外推风险，但**方向明确**（Cn² 更小 → Lburst 更小 → B=27 更够用）
- 未跑真实 Polar+CA-SCL 译码仿真（FR-21 门控目的就是在跑 MVE 前拦截，这是设计意图不是缺陷）

---

## V002: GG-LLR vs 高斯 LLR 失配量级 — 候选 (c) 译码改进 BER 增益

> 关联: D002 / S003
> 日期: 2026-06-19
> 结论: **FAIL**（理想 CSI baseline 下 (c) 物理空间 ≈ 0，触发 Kill）

### 验证假设

GG-aware LLR（B3，对 I 积分边际似然）相对高斯 LLR 在 IM/DD+OOK+GG 信道下有 >0.5dB BER 增益。

### 验证方式（三 baseline 横向 MC，两版收敛）

**版本 1：无 CSI 盲高斯判决当 baseline（v1，被否决）**
- 脚本：`fr21_gg_llr_vs_gauss_llr.py` v1
- baseline B1：`y > η/2`（把衰落 I 当确定值 1，无 CSI）
- 结果：σ²_R=0.2 工作区峰值 "增益" **+25.9 dB**
- **判定为伪信号**（TL-22 触发）：BER_gauss 地板 5.3e-2（SNR=20dB 不下降），诊断显示 100% 错误来自深衰落（s=1 但 I·η<0.5 判成 s=0），噪声仅贡献 1e-6，P(I<0.5)=9.1% 正好等于地板值。这层地板与 LLR 失配无关，是"无 CSI"导致的——baseline 立了稻草人

**版本 2：理想 CSI 高斯 LLR 当 baseline（v2，决定性）**
- baseline B2：`L=(2ηÎ·y-η²Î²)/(2σ²)`，Î=I（仿真理想 CSI，通信领域默认）
- proposed B3：GG-aware，对 I 积分边际似然（MC 混合高斯核密度估计）
- N_mc=2e6/条件，σ²_R ∈ {0.2, 1.0, 3.5, 8.0}，SNR ∈ {-5..30}dB
- 结果：所有 σ²_R 下 B3 一致地比 B2 差 **−1.28 ~ −1.82 dB**

| σ²_R | 闪烁指数 σ²_I | (c) 工作区峰值增益 (B3 vs B2) |
|---|---|---|
| 0.2（弱）| 0.194 | −1.82 dB |
| 1.0（中）| 0.707 | −1.82 dB |
| 3.5（强）| 1.105 | −1.28 dB |
| 8.0（极强）| 1.292 | −1.60 dB |

### 结论

**FAIL**。v2 物理自洽：理想 CSI 下高斯 LLR（B2）已最优，GG-aware LLR（B3）信息更少（只有统计先验无当前 Î）→ BER 严格更高（差 1-2dB）。信息论必然。(c) 在合理 baseline 下物理空间 ≈ 0。

v1 的 25dB 伪信号来自 baseline 选择错误（无 CSI 盲判决），非 LLR 失配空间。

### 关键数据

| 项 | 值 | 来源 |
|---|---|---|
| v1 伪信号峰值（B1 baseline）| +25.9 dB @ σ²_R=0.2 | v1 脚本（已否决）|
| v1 伪信号根因：BER_gauss 地板 | P(I<0.5)=9.1%，100% 来自深衰落 | 诊断脚本 |
| v2 (c) 峰值（B2 baseline）@ σ²_R=0.2 | −1.82 dB | v2 脚本 |
| v2 (c) 峰值（B2 baseline）@ σ²_R=1.0 | −1.82 dB | v2 脚本 |
| 星地 LEO 常规仰角 σ²_R | <1（45-90°）/ <2.6（20° 强端）| HV slant-path 计算 |
| 星地常规仰角对应 v2 行 | rytov=0.2/1.0 → (c) −1.8dB | 自洽 |

### 脚本位置

- `projects/thesis-figures/simulation/fr21_gg_llr_vs_gauss_llr.py`（v2 最终版，含 B1/B2/B3 三 baseline）
- `projects/thesis-figures/simulation/fr21_gg_llr_vs_gauss_llr_results.json`

### 局限性

- 未查唐承茂 PDF L1276 公式原图（`picture [297x29]`）确认其 CSI 假设。基于"FSO 仿真默认理想 CSI"常识 + v2 物理自洽性（B3 一致比 B2 差）判定 B2。残余不确定性：若唐承茂实际用 B1（无 CSI，极罕见），(c) 在 B1 baseline 下有大空间但那是"统计先验 > 无先验"的价值，非 LLR 失配改进
- 硬判决 BER 作软判决译码增益的代理上界。Polar+SCL 实际增益可能更小（软信息失配在译码后部分吸收）。但这不影响 Kill 结论：硬判决已证 B3 < B2，软判决只会放大此差距
- GG (α,β) 参数用标准表值（Andrews Ch9），非唐承茂具体设定拟合。但结论对 (α,β) 鲁棒（4 个 σ²_R 跨度大，趋势一致）
