# [S010] 批次 1 数据补完执行结果验证与集成

> 2026-07-12 | GW Step 4a 维度 D MVE 扩展（写作准备） | 状态：批次 1 验证 PASS，集成完成
> （续接：S009 方法层重新定位 + R004 批次规划 + PROMPT-007 执行回传）

## 目标

接收 PROMPT-007 批次 1 执行对话回传，**独立验证结果真实性**（不轻信摘要，P6 分离审查）：
1. N_SYMBOLS 500K→2M 修正的物理依据是否成立
2. 4 个任务结果 JSON 数据是否支撑 D011 + 导师要求
3. executor 报的"已知债务 gg_time seed-bias"是否真实、影响多大、是否阻断结论
4. 集成结论到 topic-index / decisions，判断是否进批次 2

## 记录

### 验证方式

主控独立核对（非信 executor 摘要）：物理计算复算 + JSON 数据直接提取 + seed-bias 实测 20 seeds + 源码确认三方同信道。

### 验证结果逐项

| 检查项 | 结论 | 证据 |
|---|---|---|
| N=500K→2M 物理性 | ✅ 成立 | N=500K@f_G=100Hz=**0.13τ_c**（衰落未展开），N=2M=**0.5τ_c**（充分）。executor 报"N=500K CMA BER 偏低~1000×"合理（0.13τ_c 序列近似准静态，CMA 几乎不跟踪滞后）|
| 任务 1 floor 数据 | ✅ **强支撑 D011** | 直接提取 JSON：35-40dB 时 CMA 卡 0.03-0.10（全 4 f_G 一致），ML/oracle→0。**跟踪滞后 floor 真实存在，不随 SNR 降** |
| 三方同信道 | ✅ 确认 | `ber_vs_snr_scan.py:8` docstring + `:273-276` gen_channel 一次三方复用。D011 相对比较（CMA/ML/oracle 比）**对 seed-bias 免疫** |
| 16QAM modulus mismatch | ✅ 确认（D008 Sup-1 成立） | 16QAM CMA~0.27 vs QPSK~0.10，结构性缺陷真实 |
| 16QAM ML/CMA gap< QPSK | ✅ 真实反预期 | 16QAM ML/CMA 1.1-1.6× vs QPSK 1.6-160×。**"双重惩罚放大 ML 相对优势"假设被数据否证**——高阶星座同时伤 ML 和 oracle，诚实记录，不硬圆 |
| pilot overhead 框架 | ✅ 修正合理 | overhead=N_train/(N_train+N_test) 而非 train_frac×100%。连续传输下 N_train=250K 固定、N_test 任意长→overhead<<1%（0.001dB）。**债务(1) 监督 vs 盲不公平在连续传输假设下基本解除** |
| 发散概率可视化（任务 3） | ✅ 数据自洽 | 从 cma_divergence_scan_results.json 提取，μ≤1e-3 安全区 55/128 组合零发散，μ=1e-2 危险区 f_G=1000Hz 15 组合 P_div=1.0，与 README 一致 |

### ⚠️ seed-bias 债务：真实，影响受限，既有盲点

executor 报 `gg_time_envelope` "seed-dependent bias（h mean 在 0.43–4.28 间波动，理论应稳定）"。**主控实测 20 seeds 确认且更严重**：

```
N=2M, strong(α1.5β0.8), f_G=100Hz:
  h_mean: mean=1.33 std=1.89 CV=1.42  min=0.060 max=7.196
  理论 E[h]=1（GG 归一化），实际单 seed 波动 CV>1
```

**根因（非代码 bug，是 AR(1) + 强相关固有性质）**：
- ρ≈0.97（τ_c≫block·t_s）→ 块间强相关 → 单序列样本均值收敛慢
- N=10M 时 CV 仅降到 0.90（不随 N 趋零），f_G 越大（ρ 越小）CV 越低（f_G=3000Hz CV=0.41）
- Step A 验证（`gg_time_validation.json`）**只查边缘 PDF（KS<0.006），从未查跨 seed 样本均值方差** → 既有盲点，executor 正确识别

**影响判定（决定性）**：
- ❌ **不影响 D011 核心结论**：D011 是相对比较（CMA/ML/oracle 同 seed 同 h），h-bias 对分子分母同向偏置，比率（CMA/oracle、ML/CMA）有效
- ⚠️ **影响绝对 BER 水平的跨 seed 平均**：CV=1.0 + 仅 5 seeds → 绝对 BER 点噪声大。解释了任务 1 反常点（f_G=1000@30dB ML=0.0156 vs @35dB 0.0007 的跳变 = seed 噪声非物理）
- ⚠️ **论文须写 limitations**：建议关键 BER 点加到 ≥20 seeds 或报告 per-seed 比率分布而非绝对均值
- ❌ **非阻断**：核心贡献是"跟踪滞后 floor 存在性"（结构性，全 seed 一致）+ "ML/CMA 比率"（免疫），非绝对 BER 精度

### 对 R004 防坑清单的对齐

| 防坑项 | 执行情况 |
|---|---|
| TL-20 先建预期 | ✅ executor 写预期 + 主控独立核对 PASS（floor 成立）|
| TL-22 物理前提 | ✅ executor 主动发现 N=500K 不足（0.13τ_c）改 2M——正是 TL-22 价值体现 |
| SOP_RATE=4e-7 | ✅ JSON meta 确认 |
| 不假设因果链 | ✅ 16QAM 反预期诚实记录未硬圆 |
| BER 到 1e-3 | ✅ 任务 1 多点低于 1e-3（ML/oracle 到 1e-5），CMA floor 在 1e-2 可见 |
| baseline=CMA(μ=1e-3) | ✅ 测的是安全步长跟踪滞后 |
| C7 三方对比 | ✅ CMA/ML/oracle 全含 |

### 综合判定

**批次 1 PASS**。4 个任务全部完成，数据支撑 D011 + 导师要求（BER 曲线到 1e-3 + 方法层有 BER 证据 + 16QAM 双调制验证）。

**3 个需记录的新事实**：
1. seed-bias 债务（见上，写 limitations，非阻断）
2. 16QAM ML/CMA gap< QPSK（反预期，高阶星座同时伤 ML/oracle，叙事需调整：不强卖"16QAM ML 优势更大"）
3. pilot overhead 在连续传输假设下基本解除（债务(1) 部分缓解）

## 决策引用

- D011：方法层定位"ML 避免 CMA 跟踪滞后惩罚"——**批次 1 BER vs SNR floor 数据直接验证 PASS**
- D008：16QAM modulus mismatch 真实——**批次 1 16QAM 数据确认，但 ML 相对优势< QPSK 是反预期**
- **D012 新建**：批次 1 数据确认 + seed-bias 影响判定 + 16QAM 反预期记录 + 判断进批次 2

## 范围确认

- 本轮是否在 scope boundary 内：是（GW Step 4a 维度 D MVE 扩展的写作数据准备，R004 批次 1）
- 无范围变更

## 后续

1. **批次 1 完成，可进批次 2**（CMA 跟踪滞后分解 / CMMA BER / LMMSE）—— 见 D012 判定
2. **seed-bias 债务**：批次 2/3 关键 BER 点建议加 seed 数到 ≥20，或改报 per-seed 比率；写入论文 limitations
3. **16QAM 叙事调整**：论文不卖"16QAM ML 优势更大"，改卖"16QAM CMA modulus mismatch 是结构性缺陷（BER 高 2.7×），ML 在两调制都优于 CMA 但高阶星座 ML 也受 oracle 上界限制"
4. 专题文件膨胀预警：本专题已 10 个 S 文件（≥8 警告），后续若开新实质阶段考虑转新专题
