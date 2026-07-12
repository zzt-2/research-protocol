# PROMPT-009: 批次 3 — 可选新方法探索（盲 VQ-VAE / 自适应步长 / 发散恢复）

> 文件名: PROMPT-009-batch3-optional-new-methods.md
> 用途: 批次 1+2 完成后，视情况选择做。每个任务一个独立对话。
> 来源: R004-direction-full-plan.md 批次 3
> ⚠️ 本批任务全部中风险，做不做取决于批次 1+2 结果 + 用户判断

## 背景

同 PROMPT-007/008。本批是"锦上添花"——如果做成功会显著增强论文方法贡献，但失败也不影响批次 1+2 构成的完整论文。

## 任务选择指南

做完批次 1+2 后，根据结果选：

| 如果... | 则做... |
|---------|---------|
| 审稿人可能攻击"监督 vs 盲不公平" | 任务 1（盲 VQ-VAE） |
| 想给方法层加一个"自适应"亮点 | 任务 2（自适应步长 CMA） |
| 想从"分析+方法"扩展到"分析+方法+恢复协议"完整故事 | 任务 3（发散检测+恢复） |

---

## 任务 1: 盲 VQ-VAE 实现 + BER 对比（B1 / R10）

**做什么**：实现 VQ-VAE（Qin 2026 架构：重建 MSE + commitment loss + stop-gradient），在几个 f_G 下测 BER，跟 CMA（盲）做**盲 vs 盲公平对比**。

**为什么做**：当前 ML 用 MSE 监督（需 pilot），CMA 盲——审稿人会说"不公平"。盲 VQ-VAE 解决这个。如果盲 VQ-VAE 也优于 CMA → "盲 ML 的优势不是来自 pilot 信息而是来自离线学习信道统计"。

**TL-20 预期**：
- VQ-VAE BER 应该比 CMA 好（离线学习 vs 在线更新），但可能比监督 ML 差（无标签约束更弱）
- 预期排名：监督 ML < VQ-VAE < CMA（BER 从低到高）
- 如果 VQ-VAE ≈ CMA → "盲 ML 无优势" → 方法层弱化（但有价值的负面结论）

**实现**：
- 读 `papers/_read_notes/qin2026-vqvae-blind-equalizer.md` 的架构参数（码本大小 + commitment loss 权重 + stop-gradient trick）
- VQ-VAE = ButterflyCNNEqualizer2x2（复用现有）+ VQ 层（码本量化中间特征）+ 重建 MSE loss
- 训练：无标签（盲），用接收信号本身重建（self-reconstruction）
- 测试：跟 CMA 一样，在测试集上算 BER

**参数**：
- 码本大小 K=512, 维度 D=64, commitment β=0.25（VQ-VAE 标准）
- n_tap=11, lr=0.005, batch_size=1024
- SNR=20dB, strong 湍流, f_G=[30,100,300,1000]Hz, 5 seeds

**风险**：VQ-VAE 训练不稳定（码本坍塌问题），可能需要 EMA 更新码本 + restart dead codes。如果训练不收敛 → 标"VQ-VAE 实现困难，future work"

**输出**：
- `common/_vqvae_equalizer.py`（新模块，P4 不改现有）
- `explore/cma-fade-divergence/vqvae_vs_cma_ber.py`
- `results/cma-fade-divergence/vqvae_ber_results.json`

---

## 任务 2: 自适应步长 CMA — μ(f_G) 自动调节（C1）

**做什么**：设计 μ 自适应规则——根据信道动力学速率（f_G 或 LCR）自动调 μ。安全区用大 μ 快收敛，危险区自动降 μ 防发散。

**为什么做**：如果自适应 μ 能同时保收敛速度 + 防发散 → 本身就是方法贡献（非 trivial）。即使不 work 也有价值："固定 μ 的 trade-off 是内在的，简单自适应也解决不了"。

**TL-20 预期**：
- 简单规则 μ_adapt = μ_0 / (1 + f_G/f_G_ref) 可能防发散但 BER 变差（μ 太小跟踪不上）
- 更聪明的规则：用接收信号功率方差估计信道动力学，动态调 μ
- **关键预期**：自适应 μ 有根本 trade-off——降 μ 防发散 vs 升 μ 保跟踪，两者不可兼得

**实现**：
- 在 explore/ 新建脚本（不改 common/_cma.py）
- 自适应规则试 2-3 种：(a) 固定 μ_safe (b) 功率方差自适应 μ (c) LCR 估计自适应 μ
- 跟固定 μ CMA 对比 P_div + BER

**风险**：中高。自适应规则设计不唯一，可能试几种都不 work。时间预算超了就停，记录失败。

**输出**：
- `explore/cma-fade-divergence/adaptive_mu_cma.py`
- `results/cma-fade-divergence/adaptive_mu_results.json`

---

## 任务 3: 发散检测 + 快速恢复协议（C2）

**做什么**：实现发散检测（|w| 超预警阈值时触发）+ 恢复机制（冷重置 / 热启动 / ML 接管），对比恢复时间。

**为什么做**：R7 证明冻结（防发散）无效 → 需要"发散后恢复"。JR-CMA 只做了冷重置（QPSK+OB2B），没量化恢复时间。L-DP5 "hang-up recover requires further work"。

**TL-20 预期**：
- 冷重置恢复时间 >> 热启动 >> ML 接管（从近优权重出发 vs 从初始权重出发）
- 但 ML 接管需要训练数据（pilot），冷重置不需要 → 有 trade-off

**实现**：
- 发散检测：监测 w_norm，超 5× init（预警阈值，比 10× 发散阈值早）触发恢复
- 恢复方式：
  - 冷重置：w 回中心抽头初始化，重新收敛
  - 热启动：w 回最近一次好状态（记录 checkpoint），从那里继续
  - ML 接管：训练好的 ML 直接接管均衡
- 测恢复时间 = 从发散检测到 BER<0.01 的符号数

**风险**：中。需要实现发散检测 + checkpoint + 恢复逻辑。注意 B2 专题教训：前馈架构恢复时间测度可能失效——CMA 是闭环架构所以测度成立。

**输出**：
- `explore/cma-fade-divergence/diverge_recovery_protocol.py`
- `results/cma-fade-divergence/recovery_results.json`

---

## 通用防坑清单（同 PROMPT-007 + 额外）

1-10 同 PROMPT-007。额外：
11. **批次 3 是探索性的**：失败也是合法结果，诚实记录。TL-23 冷静期——好结果先查物理前提
12. **不因为"想要方法贡献"就强行声称成功**：如果 VQ-VAE/自适应μ/恢复 不 work，如实记录"future work"
13. **时间预算**：每个任务 ≤15 分钟子 agent，超了就拆分或采样
