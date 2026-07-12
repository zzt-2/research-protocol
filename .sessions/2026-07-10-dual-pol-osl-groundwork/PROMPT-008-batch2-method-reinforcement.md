# PROMPT-008: 批次 2 — 方法层加固（CMA 跟踪滞后分解 + CMMA BER + LMMSE 对比）

> 文件名: PROMPT-008-batch2-method-reinforcement.md
> 用途: 在新对话中执行，加固方法层证据
> 来源: R004-direction-full-plan.md 批次 2

## 背景

同 PROMPT-007。方法层 D011 定位："ML 避免 CMA 跟踪滞后惩罚"。本轮深挖 CMA 跟踪滞后的机制 + 补增强基线 BER。

## 必读

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/R004-direction-full-plan.md` — 防坑清单
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` D011 — 方法层定位
3. `projects/simulation/explore/cma-fade-divergence/r_lcr_ber_impact.py` — S009 BER 脚本
4. `projects/simulation/explore/cma-fade-divergence/r2_cmma_divergence.py` — CMMA 实现
5. `projects/simulation/common/_cma.py` — CMA 均衡器（w_norm_traj 在 equalize 返回值里）
6. `projects/simulation/common/_recovery.py` — 如做 LMMSE 对比，查 lmmse_recovery

## 3 个任务（可并行子 agent）

### 任务 1: CMA 跟踪滞后分解 — 瞬态 vs 稳态（A1）

**做什么**：分解 CMA BER 差的原因。CMA 从中心抽头初始化开始收敛，收敛前的 BER（瞬态）应该差，收敛后的 BER（稳态）应该好——但如果稳态 BER 也差，说明 CMA 有内在跟踪滞后。

**方法**：
- 固定 strong 湍流, SNR=20dB, f_G=[100, 1000]Hz（代表慢/快变）
- 跑 CMA μ=1e-3, N=5M 符号
- 每 10000 符号算一个窗口 BER（滑动窗口）
- 画 BER vs 符号序号曲线
- 分解：前 K 符号（瞬态）BER vs 后 N-K 符号（稳态）BER

**TL-20 预期**：
- 瞬态（前 ~50000 符号）：CMA BER 高（从初始权重收敛）
- 稳态（收敛后）：如果信道静态（f_G=30Hz），CMA 稳态 BER 应接近 oracle；如果信道动态（f_G=1000Hz），CMA 稳态 BER 应仍差 oracle（跟踪滞后）
- **关键预期**：f_G 越大，CMA 稳态 BER 越差（跟踪跟不上信道变化）

**输出**：
- 脚本 `explore/cma-fade-divergence/cma_transient_steady_decomp.py`
- 结果 `results/cma-fade-divergence/cma_transient_steady_results.json`
- JSON 含：窗口 BER vs 符号序号 + 瞬态/稳态分界点 + 稳态 BER vs f_G

### 任务 2: CMMA BER vs f_G（G3，R2 只做了 P_div 没做 BER）

**做什么**：R2 证明 CMMA 的 P_div 跟 CMA 一样（不降发散），但没测 BER。这里补 CMMA 的 BER vs f_G。

**TL-20 预期**：
- CMMA BER 应该比 CMA 略好（多模匹配 16QAM 星座）或差不多（如果是 QPSK，CMMA=CMA）
- 但 CMMA 仍是在线更新 → 仍有跟踪滞后 → 稳态 BER 仍比 ML/oracle 差
- 预期排名：ML < oracle < CMMA ≈ CMA（BER 从低到高）

**实现**：
- 从 r2_cmma_divergence.py import CMMAEqualizer2x2
- 固定 strong, SNR=20dB, QPSK, f_G=[10,30,100,300,1000,3000]Hz
- 测 CMMA(μ=1e-3) / CMA(μ=1e-3) / ML / oracle BER

**输出**：
- 脚本 `explore/cma-fade-divergence/cmma_ber_vs_fg.py`
- 结果 `results/cma-fade-divergence/cmma_ber_vs_fg_results.json`

### 任务 3（可选）: LMMSE 均衡器对比（C3）

**做什么**：跑 LMMSE 均衡器（比 CMA 更高级的自适应方法），看是否也有跟踪滞后。

**注意**：先查 common/_recovery.py 里有没有现成的 LMMSE 均衡器（不是载波恢复的 lmmse_recovery，是均衡器的）。如果没有，跳过这个任务（实现 LMMSE 均衡器工作量不小，不值得在这个阶段做）。

如果有现成的 LMMSE 均衡：
- 跑 LMMSE vs CMA vs ML vs oracle BER vs f_G
- TL-20 预期：LMMSE 如果也需要在线估计信道 → 也有跟踪滞后；如果是 oracle CSI → 等于 oracle

## 关键纪律

同 PROMPT-007 防坑清单 1-10。额外：
- **A1 的瞬态/稳态分界**：不要手动选——用 CMA 收敛判据（如窗口 BER 不再单调下降的点）自动定
- **CMMA BER 要用 QPSK + 16QAM 双调制**：QPSK 时 CMMA=CMA（验证实现正确），16QAM 时看 CMMA 是否优于 CMA

## 返回格式

返回 ≤800 词结构化摘要：
1. 任务 1 瞬态/稳态分解：CMA 收敛点 + 稳态 BER vs f_G（跟 oracle gap）
2. 任务 2 CMMA BER：CMMA vs CMA vs ML vs oracle 排名
3. 任务 3 LMMSE（如做了）
4. 脚本路径 + 结果 JSON 路径
5. 对方法层叙事的影响：跟踪滞后分解后，方法层定位是否更精确？
