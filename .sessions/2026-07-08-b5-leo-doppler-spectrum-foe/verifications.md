# Verifications — B5-Q1 LEO Doppler 短时谱 FOE 第四候选

> 专题 `.sessions/2026-07-08-b5-leo-doppler-spectrum-foe/` 的验证记录。
> V### 按编号排列，每条关联 S### 或 D###，结论必须是 PASS/FAIL/PARTIAL 三选一。

## V001: 路 2 Step 4a 2×2 算子×FFT 分辨率消融验证（关联 D004 / S007）

> date: 2026-07-08（对话 7）
> 关联: D004（Kill 判定）/ S007（Step 4a sandbox 执行）
> 方法: 2×2 消融（算子线性/对数 × FFT 分辨率 n_fft=16/1024），控制总样本 16384 + 同星历预补 + 四格独立 α 标定，n_seeds=20，3 频偏 [0.5/1.0/2.0 GHz]，weak 湍流 SNR 13dB
> 数据源: `_ablation_2x2_results.json`

### 验证问题

路 2 M-C-A 的核心声称"B5 线性归一化比 vs Vieira 对数比，残频 σ 好 66%"——这 66% 多少来自算子差异（线性 vs 对数），多少来自 FFT 分辨率差异（n_fft=16 vs 1024）？算子贡献是否 >30%（Go 阈值）？

### 结果

**四格 σ（MHz，1.0GHz 主点，3 频偏完全一致因残频≈0）**：

| 格 | 算子 | n_fft | σ (MHz) | α 标定值 |
|---|---|---|---|---|
| A | 线性 ratio | 16 | 11.369 | 7.05e8 |
| B | 对数 ln | 16 | 11.372 | 3.42e8 |
| C | 线性 ratio | 1024 | 28.957 | 1.24e9 |
| D | 对数 ln | 1024 | 28.709 | 6.12e8 |

**贡献分解（主线 V5 独立重算，与子 agent 一致）**：
- 算子贡献（同 n_fft 下对数−线性）：n16=+0.003, n1024=−0.249 MHz，均值 **−0.123 MHz（−0.7%）**
- FFT 分辨率贡献（同算子下 n1024−n16）：线性=+17.59, 对数=+17.34 MHz，均值 **+17.46 MHz（101%）**
- 总差 D−A = 17.34 MHz

**A0 假设验证（对数比小残频不稳）**：
- f=0: B/A σ 比 = 1.0002；f=100MHz: B/A σ 比 = 1.0002 → 均 <1.30 阈值
- linear-log 算子相关系数（残频≈0 处）= **0.994**

**公平性核查**：四格同总样本 16384 + 同星历预补（ephem_residual=0）+ 四格独立 α 标定（单点 200MHz）+ bias_corr 统一处理（σ 是 std 不含均值，不影响归因）。斜率标定（50/200MHz 两点）交叉验证算子贡献 2.3%，结论稳健。

**experiment_C α 标定 bug 发现**：旧 `_scope_audit_results.json` 的 grid C（B5@n_fft=1024）用锚 α=6e8（n_fft=16 标定值）未重标，σ 被压到 14.1MHz（重标后真实 29.0MHz）。此 bug 不影响 D004 Kill 判定（无论 α 是否重标，算子贡献都 <10%），但影响 S005/D003 的"66% 同族增量"叙事（那 66% 其实主要是 FFT 分辨率差）。

### 结论

**FAIL**（路 2 Step 4a 维度 A0+C 双 FAIL）

- 维度 A0（致命缺陷：对数比小残频不稳）：**FAIL**——假设不成立（B/A=1.00 <1.30，相关 0.994）
- 维度 C（信号强度：算子贡献 >30%）：**FAIL**——算子贡献 −1%（<10% Conditional-Kill 阈值）
- 维度 A（对手合法性 Vieira 同族）：PASS
- 维度 B（复现性）：PASS（V5 主线独立重算一致）

路 2 核心（线性比比对数比更鲁棒）证伪。66% σ 差异全部来自 FFT 分辨率参数选择（n_fft=16，B5 锚公开工程参数，Vieira 可同样采用，非独占）。无 salvage → Kill（D004）。

### 来源

`_ablation_2x2_results.json`（子 agent 执行）+ 主线 V5 独立重算 + params.py FFT_POINTS_B5（content.md L87）+ D003 判定阈值

---

## V002: B5 Kill 后 6 类适配扫描 salvage 评估（关联 D004 / S007 §7）

> date: 2026-07-08（对话 7 续，用户追问"能不能挣扎一下"后）
> 关联: D004（Kill 补强）/ S007 §7（salvage 评估）
> 方法: adaptation-scan.md 6 类适配扫描（A1/A4/A5/A6，A2 D002 已做/A3 跳过），n_fft∈{16,64,256,1024} × 9 条件（weak/mod/strong × 8/13/18dB），主线 V5 独立核查
> 数据源: `_adaptation_scan_results.json`

### 验证问题

D004 Kill 只查了"算子贡献"（−1%）。NDA-ML 教训（S013）是算法层无增量但 A4 条件切换出信号。B5 是否在参数/条件/评价维度/失效边界上有 adaptation-scan 信号可翻盘？

### 结果（6 类全无信号）

| 适配类 | 结果 | 关键数据 |
|---|---|---|
| A1 参数适配 | FAIL | 9 条件最优 n_fft 全是 16（all_sigma 核查：n_fft=16 全最小）|
| A4 条件适配 | FAIL | diff_vieira_minus_b5 9 条件全正 [+5.3,+12.5]，无 crossover |
| A5 评价维度 | FAIL | outage P(|resid|>140MHz) 全 0（两法残频都<140MHz）|
| A6 失效边界 | FAIL | B5 σ 非单调（Rp-n 饱和噪声尖峰），两法同点失锁 |

### 结论

**PASS（Kill 确认）**——salvage 评估确认 D004 Kill 成立，6 类适配扫描无任何翻盘信号。

B5 全部优势 = n_fft=16 块数均值降噪（公开工程参数，非独占），无任何条件/维度/边界独占性。主线 V5 核查子 agent 归因可复现（A1 每条件 all_sigma / A4 diff 全正）。

补强了 Kill 完备性：现在不是"只查算子就 Kill"，是"6 类适配全无信号才 Kill"。对 D004 的影响 = 确认（不翻盘）。

### 来源

`_adaptation_scan_results.json`（子 agent 执行）+ 主线 V5 独立核查 + adaptation-scan.md 6 类规则 + S013 NDA-ML 适配教训
