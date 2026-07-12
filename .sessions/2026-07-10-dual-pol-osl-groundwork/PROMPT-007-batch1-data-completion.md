# PROMPT-007: 批次 1 — 数据补完（BER曲线 + 16QAM + pilot开销）

> 文件名: PROMPT-007-batch1-data-completion.md
> 用途: 在新对话中执行，补完写论文必须的数据
> 来源: R004-direction-full-plan.md 批次 1

## 背景

你是 Q-CMA-FADE 研究的执行对话。方向状态（读必读文件确认）：
- 分析层完整：CMA 发散概率/条件判据/机制澄清（高 μ 数值不稳定，非深衰落触发）
- 方法层 D011 新定位：ML 避免 CMA 跟踪滞后惩罚（CMA 安全μ BER 差 oracle 2.9-2266×，ML 全 f_G 优 CMA 1.8-数百倍）
- 4 个任务要补完

## 必读（按优先级）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/R004-direction-full-plan.md` — 防坑清单 + 任务定义
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D011 — 方法层定位
3. `projects/simulation/explore/cma-fade-divergence/README.md` — 脚本清单 + 参数溯源表
4. `projects/simulation/explore/cma-fade-divergence/r_lcr_ber_impact.py` — S009 BER 实验脚本（你要扩展它）
5. `projects/simulation/explore/cma-fade-divergence/sup_stress_test.py` — 16QAM 调制解调实现

## 你要做的 4 个任务

### 任务 1: BER vs SNR 曲线（导师必须的，F1）

**做什么**：固定 strong 湍流（α=1.5, β=0.8），扫 SNR 10-40dB（间隔 2-5dB），每个 SNR 测 CMA(μ=1e-3) / ML / oracle BER。跑 3-4 个代表性 f_G（30/100/300/1000 Hz）。

**TL-20 预期**：
- 低 SNR（<15dB）：三者 BER 都高（>0.1），ML 略优 CMA
- 中 SNR（15-25dB）：ML 接近 oracle，CMA 因跟踪滞后始终差几倍
- 高 SNR（>25dB）：ML≈oracle，CMA 仍有残余 BER（跟踪滞后天花板）
- 整体趋势：ML 和 oracle 曲线应接近平行（差一个 offset），CMA 曲线应有一个 floor（跟踪滞后导致的 BER 下限）

**参数**（从 params.py 读，不硬编码）：
- N_SYMBOLS = 500_000（BER 精度够到 1e-4 量级；如要 1e-5 需 5M+）
- SOP_RATE = 4e-7 rad/sym（1 krad/s，sat.1553 §6.3 真实值）
- BLOCK = 100, T_S = 1/2.5e9
- ML: n_tap=11, lr=0.005, batch_size=1024, train_frac=0.5
- CMA: n_tap=11, μ=1e-3（安全区步长）, R2=1.0（QPSK）, block_size=64
- SNR_SWEEP = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 40] dB
- F_G_SWEEP = [30, 100, 300, 1000] Hz
- N_SEEDS = 5（导师说"5seed就行"）
- 调制：QPSK

**输出**：
- 脚本 `explore/cma-fade-divergence/ber_vs_snr_scan.py`
- 结果 `results/cma-fade-divergence/ber_vs_snr_results.json`
- JSON 结构：每个 (f_G, snr) 的 {cma_ber_mean, cma_ber_std, ml_ber_mean, ml_ber_std, oracle_ber_mean, oracle_ber_std, n_seeds}

**关键**：
- oracle_equalize 用 sup_stress_test.py 的实现（撤销 SOP + MMSE on h）
- CMA 用 μ=1e-3（安全区），不是危险区 μ——这里测的是"即使安全步长 CMA 也有跟踪滞后"
- ML 训练数据用该 SNR + f_G 的前 50% 符号，测试用后 50%（Freire 陷阱 2 无泄漏）

### 任务 2: 16QAM BER vs f_G（G1，D008 债务）

**做什么**：用 16QAM 调制，固定 SNR=20dB，扫 f_G=[10,30,100,300,1000,3000]Hz，测 CMA / ML / oracle BER。

**TL-20 预期**：
- 16QAM 的 CMA BER 应该比 QPSK 更高（modulus mismatch 结构性缺陷，D008 Sup-1 已发现）
- ML 在 16QAM 也应优于 CMA（因为 ML 不受 modulus mismatch 限制）
- 跟 QPSK 对比：16QAM 的 ML vs CMA gap 可能更大（CMA 的 modulus mismatch + 跟踪滞后双重惩罚）

**实现**：
- 16QAM 调制解调：从 sup_stress_test.py 复用 gen_16qam / demap_16qam / compute_ber
- CMA R2 = 1.32（16QAM Godard R²，sup_stress_test.py:56）
- 其余参数同任务 1（但固定 SNR=20dB，扫 f_G）

**输出**：
- 脚本 `explore/cma-fade-divergence/ber_16qam_vs_fg.py`
- 结果 `results/cma-fade-divergence/ber_16qam_vs_fg_results.json`

### 任务 3: 发散概率可视化数据（F2，主控做）

**做什么**：从 cma_divergence_scan_results.json 提取 P_div vs (μ, f_G) 的数据，整理成热图/曲线可用的格式。

这个任务在主控对话做，不需要子对话。

### 任务 4: pilot overhead 量化（G2，主控做）

**做什么**：ML 监督学习用了 train_frac=0.5（50% 符号训练）。等效 pilot overhead = 50% → SNR 损失 = 10*log10(1/(1-0.5)) = 3.01dB。但实际训练可以跨帧复用（连续传输只需初始训练一次），所以 effective overhead 更低。

计算：
- 最坏情况 overhead（每帧重训练）= train_frac × 100%
- 最好情况 overhead（训练一次永久使用）= 0（首次训练成本摊薄到无穷帧）
- 折中：假设每 N 帧重训练一次，overhead = train_frac / N

**输出**：一个简短的计算表，写进 results 或直接放 README

## 关键纪律（防坑清单）

1. **TL-20 先建预期**：跑之前写"预期结果是什么"，偏离即查
2. **TL-22 物理前提**：好结果先查 5 分钟物理前提
3. **SOP_RATE = 4e-7**（1 krad/s 真实值），不是 Step B 旧的 1e-4（250 krad/s）
4. **不假设因果链**：跑出来什么就是什么，不为了"好看"调参数
5. **BER 用 pre-FEC**：曲线至少到 1e-3
6. **baseline = CMA（μ=1e-3 安全步长）**：测的是"即使安全步长 CMA 也差"
7. **C6 公式溯源**：CMA 公式标 sat.1553 Eq.28/48/50 + Godard 1980；ML 标 Qin 2025 L275/283
8. **C7 三方对比**：CMA / ML / oracle 全含
9. **Freire 6 陷阱**：MTRS / batch≥1024 / MSE / 分离 / BER 非 EVM / RMpS
10. **守 TL-25 起飞检查**：脚本头部标 `# TL-25 checklist: [1/2/3/4/5/6] 全部确认`

## 返回格式

返回 ≤800 词结构化摘要：
1. 任务 1 BER vs SNR：每个 f_G 的 CMA/ML/oracle 曲线趋势 + 关键 crossover 点
2. 任务 2 16QAM：16QAM vs QPSK 的 CMA/ML gap 对比
3. 任务 4 pilot overhead：计算结果
4. 脚本路径 + 结果 JSON 路径
5. 任何意外发现
