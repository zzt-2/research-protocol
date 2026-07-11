# [R003] Q-CMA-FADE 能出结果的子问题穷举

> 2026-07-11 | 关联：dual-pol-osl-groundwork / D007-D008
> 调研问题：Q-CMA-FADE 方向扩展后，哪些子问题可能产出可发表结果？

## 调研问题

Step C 压力测试（D008）暴露 Q-CMA-FADE 当前框架的三个硬伤（QPSK 弱/方法不新/对比不公平）。用户要求穷举所有可能出结果的子问题，不急于定方向，先把牌摊开。

## 已有资产（不用重做的）

| 资产 | 位置 | 状态 |
|------|------|------|
| GG 时间域衰落模型 (AR(1), GAR/lognormal) | common/_gg_time.py | PASS |
| CMA 2×2 蝶形均衡器 (Godard 1980, block-wise) | common/_cma.py | PASS |
| ML CNN 蝶形均衡器 (Qin 2025 架构, MSE 监督) | common/_ml_equalizer.py | PASS |
| 发散概率扫描 (384 trials, 128 组合) | results/cma_divergence_scan_results.json | PASS |
| ML vs CMA vs oracle MVE (25 runs) | results/mve_cma_vs_ml_results.json | PASS |
| 压力测试 (16QAM/小步长/SOP 漂移) | results/sup_stress_test_results.json | PASS |
| 数值 AFD/LCR 统计 | gg_time_fading_model.py::fade_statistics | PASS |
| torch 2.6.0+cu124 + CUDA RTX 4070 | scoop py311 | 可用 |

## 子问题穷举（按出结果信心排序）

### 高信心（几乎确定能出数字/曲线）

---

#### R1: CMA 发散解析界 — drift∝μ·σ_n·√(AFD) 形式化

**做什么**：把 Step B 已有的 `drift ∝ μ·σ_n·√(AFD)`（cma_divergence_scan.py L24 注释里已写）形式化。单次深衰落内 CMA 系数漂移量 = μ·R²·σ_n·√(AFD)，发散条件 = 漂移 > 阈值。整体 P_div = 1-(1-P_single)^{N_events}，N_events = LCR×T_obs。

**结果形态**：μ_safe(τ_c, AFD, tap) 设计曲线 — "给定信道统计，选 μ 避免发散"

**为什么能出**：drift 模型是干净的解析关系；AFD/LCR 数值统计已实现（fade_statistics PASS）；Step B 的 384 trials 数据可以直接验证解析界 vs 实测 P_div

**需要做**：推导 P_single 发散条件（漂移 > 10×init_norm 的概率）+ 用数值 AFD/LCR 代入 + 跟 384 trials 对比验证

**风险**：AR(1) 模型是近似（真实 GG 时间相关非严格 AR(1)），解析界可能跟实测差 10-30%。但"近似界"本身也是合法贡献。

**增量定位**：sat.1553 §6.3 L778 空白 = "发散概率未分析" → 我们给半解析界。不是纯解析（用数值 AFD/LCR），但比纯 Monte Carlo 扫描（Step B 已做）更进一步。

---

#### R2: CMMA 深衰落发散扫描 — 证明 modulus mismatch 修复 ≠ 深衰落鲁棒

**做什么**：实现 CMMA（级联多模 CMA，多 R² 匹配 16QAM 多环），跑 Step B 同样的发散扫描。

**结果形态**：CMMA P_div vs CMA P_div 对比表 — 如果 CMMA 也发散 → "多模修复星座失配但修不好深衰落梯度噪声驱动"

**为什么能出**：CMMA 只是改 CMA 的误差函数（多 R² 替代单 R²），代码改动小（_cma.py 加一个 CMAEqualizerMultiModulus 类）。扫描代码已有。

**需要做**：实现 CMMA（16QAM 3 个模值环 R₁²/R₂²/R₃²，按最近环算误差）+ 跑 128 组合 × 3 seeds

**风险**：CMMA 可能不发散（多模误差幅度比单模小，梯度噪声更小）→ 结果变成"CMMA 比 CMA 鲁棒" → 方向变弱。但即使如此，"CMMA 在极端深衰落下仍可能发散"也是有价值的结果。

**增量定位**：Agent 1 确认"CMMA 在 GG 深衰落下完全没人测过"（Qin 只测单一中强湍流，JR-CMA 只测 QPSK）。无论结果如何都是新数据。

---

#### R3: 16QAM BER vs scintillation index 扫描曲线

**做什么**：扫 scintillation index（弱/中/强/uplink_strong 4 档），每档测 CMA/CMMA/ML/oracle 的 BER。

**结果形态**：BER vs σ²_I 曲线（4 条线）— 显示 CMA 在哪档开始恶化，ML/oracle 在哪档仍然 OK

**为什么能出**：代码全有，只是参数扫描。16QAM 调制解调已在 sup_stress_test.py 实现。

**需要做**：跑 4 湍流档 × 3 方法 × 5 seeds = 60 runs

**风险**：极低。必定出曲线。唯一风险是曲线太"平"（所有方法差不多）或太"陡"（所有方法在某档都崩溃），但这本身也是结果。

**增量定位**：Qin 2025/2026 都只测单一湍流强度（r₀=0.4mm）→ 我们扫 4 档 = 补 Qin H4 缺口。

---

#### R4: 发散事件与 AFD/LCR 的相关性分析

**做什么**：从 Step B 的 384 trials 里，提取每个 trial 的发散时间点（diverge_idx），跟同一 channel 实现的 AFD/LCR 统计做相关性分析。

**结果形态**：P_div vs AFD(thr) 散点图 + 相关系数；P_div vs LCR(thr) 散点图 + 相关系数

**为什么能出**：Step B 已经记录了 diverge_idx；fade_statistics 已经能算 AFD/LCR。只需把两组数据 join 起来。

**需要做**：重跑 Step B 时同时记录 AFD/LCR（或从已有 seed 重新生成 channel 算 AFD/LCR）+ 算相关系数

**风险**：Step B 发现 f_G（≈LCR）是第二驱动 → LCR 相关性应该高。AFD 相关性可能低（因为 AFD 和 LCR 此消彼长）。但"哪个更重要"本身就是结论。

**增量定位**：把 Step B 的"经验判据"升级为"统计解释" — 发散由 LCR 驱动（事件计数）而非 AFD 驱动（单次持续）。

---

#### R5: CMA 系数漂移模型验证 — 预测 vs 实测

**做什么**：Step B 已记录 w_norm_traj（系数范数轨迹）。用 drift ∝ μ·σ_n·√(n) 模型预测漂移，跟实测轨迹对比。

**结果形态**：预测漂移 vs 实测漂移散点图 + R²

**为什么能出**：w_norm_traj 数据已有（Step B 384 trials 全记录了）。预测模型只需代入 μ/σ_n/时间步。

**需要做**：从 results JSON 提取 w_norm_traj + 代入解析模型 + 算 R²

**风险**：AR(1) 近似 + 块级更新的离散效应可能让 R² 不高。但即使 R²=0.5 也是"模型捕获了主要趋势"的结论。

---

#### R6: QPSK vs 16QAM 发散行为对比

**做什么**：用相同 (μ, f_G, tap) 跑 QPSK 和 16QAM 的 CMA 发散扫描，对比 P_div。

**结果形态**：P_div(QPSK) vs P_div(16QAM) 对比表

**为什么能出**：QPSK 扫描已有（Step B）。16QAM 只需改调制 + R² + 重跑。

**需要做**：16QAM 版 cma_divergence_scan（改 gen_qpsk→gen_16qam, R2=1.0→1.32）

**风险**：极低。必定出数字。预期 16QAM P_div 略高（多模误差更大→梯度噪声更大），但差异可能不大。

---

### 中信心（很可能出结果，但依赖某些条件）

---

#### R7: 被动冻结实现与量化 — sat.1553 [79] 从未量化

**做什么**：实现"低功率时停止 CMA 更新"（h < threshold 时不更新权重），量化它能避免多少发散。

**结果形态**：P_div(with freeze) vs P_div(without freeze) + SNR penalty of freeze（冻结期间不跟踪 SOP → 恢复后 SOP 偏差）

**为什么能出**：实现极简（CMA 更新循环加一个 `if h_blk > threshold` 条件）。sat.1553 引 [79] 但自己没量化 → 我们首次量化。

**需要做**：_cma.py 加 freeze 模式 + 跑发散扫描 + 测冻结期间 SOP 漂移

**风险**：**如果冻结太有效（P_div→0）→ "问题被 trivial 方法解决" = 方向根基动摇**。但 Agent 1 分析：冻结期间丢 SOP 跟踪，恢复后有 SOP 偏差 → 冻结不是万能的。这个"不是万能"就是我们切入点。

**增量定位**：sat.1553 [79] Matsuda 2020 提了冻结但没量化效果 → 我们量化 + 指出局限。

---

#### R8: 冷重置 vs 热启动恢复时间对比

**做什么**：JR-CMA 的重置是冷启动（回初始状态）。ML 可以热启动（从冻结/上一好状态续训）。对比恢复时间。

**结果形态**：恢复时间（符号数）vs 衰落深度，冷重置 vs ML 热启动

**为什么能出**：冷重置 = CMA 从 init_norm 重新收敛（代码已有）。ML 热启动 = 从保存的 best_state 继续训练（MLChannelEqualizer 已有 best_state）。

**需要做**：实现"fade 结束后触发恢复"逻辑 + 记录恢复到 BER<threshold 的符号数

**风险**：如果 ML 热启动不比冷重置快 → 结果是 null。但理论上 ML 热启动应该快（从接近最优的权重出发 vs 从初始权重出发）。注意 B2 专题教训：前馈架构恢复时间测度可能失效，需确保 CMA 闭环架构下测度成立。

**增量定位**：JR-CMA 只做了冷重置且未量化恢复时间 → 我们量化 + 提出更好的热启动。

---

#### R9: 冻结 + 热启动混合恢复协议

**做什么**：组合 R7+R8 — 深衰落期间冻结 CMA（防发散），衰落结束后 ML 热启动恢复（快速重收敛）。

**结果形态**：outage 概率 vs 恢复时间权衡曲线（freeze+hot-resume vs cold-reset vs no-action）

**为什么能出**：R7 和 R8 的自然组合。如果两者各自有效，组合更有效。

**需要做**：实现 fade 检测 + freeze 触发 + fade 结束检测 + ML hot resume

**风险**：如果 freeze 已经足够（R7 有效到 P_div→0），热启动就不需要了 → R9 退化成 R7。但如果 freeze 有 SOP 漂移问题（R7 的局限），热启动正好补上。

**增量定位**：L-DP5 "recover from hang-up, requires further work" → 我们给出恢复协议。不是新算法，是设计准则（TL-05 解析/设计贡献比算法安全）。

---

#### R10: scintillation index 扫描下的盲 VAE 鲁棒性

**做什么**：实现 VQ-VAE（Qin 2026 损失比 VAEMR 简单：重建 MSE + commitment loss），在 4 档湍流下测 P_div 和 BER。

**结果形态**：VQ-VAE vs CMA/CMMA 的 BER vs σ²_I 曲线（盲 vs 盲公平对比）

**为什么能出**：torch 可用，VQ-VAE 损失比 VAEMR 简单（不用推导 ELBO 交叉项）。Qin 2026 笔记有完整架构参数。

**需要做**：实现 VQ-VAE（码本 + commitment loss + stop-gradient）+ 跑 4 档湍流 × 5 seeds

**风险**：VQ-VAE 实现工作量中等（码本初始化 + stop-gradient trick 容易出 bug）。如果 VQ-VAE 在深衰落下也"发散"（训练 loss 爆炸或推理输出垃圾）→ 结果是"盲 ML 也不行" → 方向变弱。但即使如此也是有价值结论。

**增量定位**：Qin 2025/2026 只测单一湍流 → 我们扫 scintillation index = 补 H4 缺口。盲 vs 盲 = 公平对比。

---

### 低信心（不确定能出，但有探索价值）

---

#### R11: 深衰落感知损失（fade-aware ELBO/MSE）

**做什么**：Qin 的 ELBO 假设 AWGN（σ_w² 解析解）。深衰落下噪声 = 乘性闪烁 + 加性 AWGN，非高斯。把闪烁统计纳入损失。

**结果形态**：fade-aware loss vs standard MSE/ELBO 的 BER 对比

**为什么可能出**：理论上更匹配信道 → 应该更好。Agent 2 建议首选。

**风险**：增益可能 <1dB（FR-21 Kill 风险）。闪烁统计纳入损失的方式不唯一，可能试几种都不 work。且 VAE 损失推导复杂，如果用 MSE 监督版改（加权 MSE），创新性又不够。

**判断**：这是"方法贡献最强但风险最高"的选项。不适合作为第一个目标，适合在 R10 验证 VQ-VAE 基线后再试。

---

#### R12: CMA 发散后的星座畸变分类学

**做什么**：分析 CMA 发散后的输出星座 — 是均匀散开？偏移？旋转？缩放？不同发散模式对应不同物理机制。

**结果形态**：发散模式分类（"均匀噪声型"/"偏移型"/"旋转型"）+ 每种模式的触发条件

**为什么可能出**：Step B 的 diverge_idx 之后的数据可以分析。只需后处理。

**风险**：可能所有发散都是"均匀散开"一种模式 → 没有分类学意义。但如果发现有不同模式 → 有趣的物理发现。

**判断**：低成本后处理，顺手做。不一定能出但试一下不亏。

---

## 策略组合建议（不在本笔记定论，留给讨论）

以上子问题不是互斥的。可能的组合：

| 组合 | 包含 | 贡献形态 | 工作量 | 风险 |
|------|------|---------|--------|------|
| **最小可发表** | R1+R3+R4 | 发散解析界 + BER 曲线 + 统计解释 | 低（后处理为主） | 低 |
| **中等故事** | R1+R2+R3+R7+R8 | + CMMA 对比 + 冻结量化 + 恢复时间 | 中 | 中 |
| **完整故事** | R1+R2+R3+R7+R8+R9+R10 | + 混合恢复协议 + 盲 VAE 对比 | 高 | 中高 |

## 对决策的影响

这些子问题里：
- **R1/R4/R5 是纯分析**（用已有数据后处理），几乎零风险，应该先做
- **R2/R3/R6/R7 是小改代码+重跑**，高信心出结果
- **R8/R9 是恢复协议**，中信心，是方法贡献的核心候选
- **R10/R11 是盲 VAE**，工作量大但方法贡献最强
- **R12 是顺手后处理**

建议优先级：先做 R1/R4/R5（零成本验证分析层价值）→ 再做 R2/R7（确认 CMMA 和 freeze 的行为）→ 根据结果决定要不要上 R8-R11。

## 结论

Q-CMA-FADE 方向**有多条能出结果的路径**，但每条的"含金量"不同：
- 分析层（R1/R4/R5）几乎确定能出，但贡献偏轻（半解析界 + 统计解释）
- 对比层（R2/R3/R6）确定能出数据，增量定位清晰（补 Qin H4）
- 恢复层（R7/R8/R9）是方法贡献的核心，但依赖 freeze 是否有效的前置判断
- 盲 VAE（R10/R11）方法贡献最强但工作量最大

**最现实的路径**：先花 1-2 个对话做 R1/R4/R5（零风险验证）+ R2/R7（关键前置判断），根据结果再定要不要上恢复协议或盲 VAE。
