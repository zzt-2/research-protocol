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
