# PROMPT-014: 盲 VQ-VAE 均衡器实现 — 解决监督 vs 盲不公平（债务1）

> 文件名: PROMPT-014-blind-vae-fair-comparison.md
> 用途: 在新对话中执行，实现盲 VQ-VAE 均衡器，做盲 vs 盲公平对比
> 来源: D008 债务1 + R004 批次3 + 用户选定方向 3
> 性质: **方法实现 + 验证。有明确 PASS 标准，是工程任务非开放探索。**

## 0. TL;DR（先读）

你在 `projects/simulation/`。背景：当前 ML 均衡器用 MSE 监督训练（需要 pilot/已知符号），而 CMA 是盲的（不需 pilot）。审稿人必攻击"监督 ML vs 盲 CMA 不公平"。解决 = 实现一个**盲 ML**（VQ-VAE，不需 pilot），做盲 vs 盲公平对比。
**你的任务**：实现 VQ-VAE 盲均衡器（参考 Qin 2026），在双口径 SOP 场景下跟 CMA 盲 vs 盲对比，看盲 ML 是否也优于 CMA。
**产出**：实现 + 对比报告（≤1200 词）+ 脚本 + 结果 JSON。回传主控。
**最高纪律**：1. VQ-VAE 实现易 bug（码本+stop-gradient），必须有 sanity check；2. 守 FR-16（架构信息增量——VQ-VAE 输入两个不同信道要产生不同输出）；3. 不自己写 D###。

## 1. 背景（"了解即可不对照评价"）

### 公平性问题（D008 债务1）

| 方法 | 训练方式 | 需要 pilot？ |
|---|---|---|
| CMA | 盲（恒模代价，在线）| 否 |
| 当前 ML（CNN）| **监督（MSE 到星座点）** | **是**（需已知符号）|
| VQ-VAE（要做）| **盲（重建+commitment loss）** | **否** |

当前对比"ML 优于 CMA"里，ML 用了 pilot 训练而 CMA 没有——审稿人说"ML 赢是因为多了 pilot 信息"。VQ-VAE 解决这个：盲训练，跟 CMA 盲 vs 盲。

### VQ-VAE 原理（Qin 2026，参考 literature_notes L-ML5/6）

VQ-VAE = 向量量化变分自编码器。用于均衡时：
- 编码器：接收信号 → 潜在表示
- 码本：把潜在表示量化到最近的码字（离散化，模拟星座点）
- 解码器：码字 → 均衡后符号
- 损失 = 重建 MSE + commitment loss（编码器输出靠近码本）+ codebook loss（码本靠近编码器输出，stop-gradient）
- **关键**：码本是从数据学的，不需要已知发送符号 → 盲

### 双口径适配

当前 ML 是 2×2 蝶形（wxx/wxy/wyx/wyy）。VQ-VAE 要同样处理双偏振：输入 (rX, rY) → 输出 (zX, zY)。可以保持 2×2 蝶形结构 + VQ-VAE 损失，或用更灵活的编码器。

### ⚠️ 已知风险

1. **VQ-VAE 实现 bug 多**：码本崩溃（所有输入映射到同一个码字）、stop-gradient 放错位置、commitment loss 系数不对。**必须有 sanity check**（码本利用率、训练损失下降、输入不同信道产生不同输出 FR-16）
2. **Qin 2026 已做 VAE vs CMA**（单湍流强度）——我们的增量是双偏振 SOP + f_G 扫描 + 双口径 BER。实现要标 Qin 来源，不能说原创架构
3. **盲训练可能不如监督**：VQ-VAE 盲训练若效果差（BER 远高于监督 ML），也是有价值的结论（"盲 ML 仍优于 CMA"或"盲 ML 不如监督但可接受"）

## 2. 必读（按优先级）

1. `papers/_read_notes/` 里 Qin 2025/2026 精读笔记（L-ML5/6，VQ-VAE 架构 + 损失）——**先查有没有，没有就报告主控**
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D008**（债务1 公平性）+ D018（双口径现状）
3. `projects/simulation/common/_ml_equalizer.py`（当前监督 ML 的 2×2 蝶形结构，VQ-VAE 可复用蝶形 + 换损失）
4. `projects/simulation/explore/cma-fade-divergence/r_lcr_ber_impact.py`（信号模型 + BER 计算）
5. `code-quality.md` 方法论适配性矩阵（GNN/ML 实现规范）

## 3. 任务分解

### 步骤 1：查 Qin 精读笔记确认 VQ-VAE 架构细节

先读 `papers/_read_notes/` 找 Qin 2025/2026（L-ML5/6）。确认：
- 编码器/解码器结构（层数/通道/激活）
- 码本大小 + 维度
- 三个 loss 项的系数
- stop-gradient 位置
- **若笔记缺失或细节不足 → 报告主控，先补精读再实现，不要凭记忆猜架构**

### 步骤 2：实现 VQ-VAE 盲均衡器

- 新建 `common/_vae_equalizer.py`（VQVAEEqualizer2x2）
- 保持 2×2 蝶形输出结构（zX/zY），编码器/解码器按 Qin
- 损失：重建（输入→输出的 MSE，**不用发送符号**）+ commitment + codebook
- **Sanity check（必须过，FR-16）**：
  - 码本利用率 >50%（没崩溃）
  - 训练损失单调下降
  - 两个不同信道输入产生不同输出（信息增量）

### 步骤 3：盲 vs 盲对比

固定 N=2M（S009/D018 确认 ML 优势的参数域），strong, SNR=20dB, SOP=4e-7：
- f_G ∈ {30, 100, 1000} Hz
- 对比：CMA(盲) / VQ-VAE(盲) / 监督ML(参考) / oracle
- **≥10 seeds，双口径 BER（fixed + PI）**
- **PASS 标准**：VQ-VAE 盲 BER 优于 CMA 盲（哪怕只是略优），证明"盲 ML 也赢"
- **FAIL 标准**：VQ-VAE 盲 BER ≈ 或差于 CMA → 盲 ML 无优势（监督 ML 的优势来自 pilot 信息）

## 4. 执行方式

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（torch 2.6.0+cu124, CUDA RTX 4070）
- 工作目录: `projects/simulation/`（`common/_vae_equalizer.py` + `explore/cma-fade-divergence/vae_vs_cma_blind.py`）
- 复用 r_lcr 的 gen_channel（不改信号模型）
- VQ-VAE 训练参数先跟 Qin，若不收敛再调

## 5. 已知陷阱

1. **码本崩溃**：训练初期所有输入映射同一码字。用 EMA 更新码本或增加 commitment 系数
2. **stop-gradient**：codebook loss 的梯度不能流回编码器（否则码本和编码器一起漂）。用 `sg` 标记
3. **盲训练无标签**：重建损失是输入→输出，不是输出→发送符号。别误用发送符号
4. **公平性细节**：CMA 也是盲的但在线更新；VQ-VAE 盲但离线训练。严格说还有"在线 vs 离线"差异，但至少都"不需 pilot"，比监督 vs 盲公平
5. **seed-bias**：≥10 seeds

## 6. 产出格式（强制）

```
# PROMPT-014 报告：盲 VQ-VAE 公平对比

## TL;DR
[盲 ML 是否优于盲 CMA + 码本是否健康]

## VQ-VAE 实现
[架构（标 Qin 来源）+ sanity check 结果（码本利用率/信息增量 FR-16）]

## 盲 vs 盲对比
[表格：f_G × {CMA盲/VQ-VAE盲/监督ML/oracle} 双口径 BER，≥10 seeds]

## PASS/FAIL 判定
[盲 ML 是否优于盲 CMA]

## 对主控决策的建议
[公平性债务是否解除 + 论文怎么写盲对比]

## 产出路径
[common/_vae_equalizer.py + explore/.../vae_vs_cma_blind.py + results JSON]
```

## 附：基线（不用重跑）
- CMA(盲) N=2M PI-BER ≈ 0.11-0.13（D018，f_G=30/100/1000）
- 监督 ML(当前) N=2M PI-BER ≈ 0.03-0.04，优于 CMA 3-3.8×
- oracle ≈ 0.01-0.02
- 目标：VQ-VAE 盲 BER 介于 CMA 和监督 ML 之间（若接近监督 ML 最好；若只略优于 CMA 也可接受）
