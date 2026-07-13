# PROMPT-013: ML clean-swap vs CMA degraded-swap 交换质量差异机制深挖

> 文件名: PROMPT-013-swap-quality-mechanism.md
> 用途: 在新对话中执行，搞清为什么 ML 的 X/Y 交换比 CMA 干净（这是真方法贡献点）
> 来源: D018（PROMPT-012 审计完成）+ 用户选定方向 2
> 性质: **机制研究，先建假设再设计验证。目标是回答"为什么"，产出可写进论文的方法贡献。**

## 0. TL;DR（先读）

你在 `projects/simulation/`。背景：PROMPT-012 双口径审计发现，长序列 SOP 漂移下 CMA 和 ML 都发生 X/Y 偏振交换，但**质量不同**——ML 10/10 clean-swap（PI-BER 0.005，接近 oracle），CMA 8 clean + 2 degraded-swap（PI-BER 0.032，有残余均衡损失）。
**你的任务**：搞清**为什么 ML 的交换比 CMA 干净**——这是真方法贡献（不是换皮，是机制解释）。
**产出**：机制研究报告（≤1500 词）+ 验证脚本 + 结果 JSON。回传主控。
**最高纪律**：1. 先建假设再验证；2. 诚实记录（若差异不显著或机制查不清，如实报告）；3. 不自己写 D###。

## 1. 背景（理解任务必需的，"了解即可不对照评价"）

### 已确认的事实（PROMPT-012，10 seeds, N=5M, SOP=4e-7, f_G=30, strong, 20dB）

| 方法 | fixed-BER | PI-BER | 分类 |
|---|---|---|---|
| CMA | 0.477 | **0.032** | 8 clean-swap + 2 degraded-swap |
| ML | 0.497 | **0.005** | 10 clean-swap |
| oracle | 0.004 | 0.004 | normal |

- **clean-swap**：zX↔zY 整体交换，PI（用 zY 解 sX）BER 接近 oracle（<0.01）
- **degraded-swap**：发生了交换但 PI 后仍有残余损失（BER 0.06-0.17），即交换不彻底/伴有均衡误差
- **ML 的 PI-BER(0.005) < CMA 的 PI-BER(0.032)**——ML 交换后恢复得更干净

### 为什么这是真方法贡献

这个差异**不是 trivial**的：两个方法都交换了（都会丢流标签，都需要开销消歧），但 ML 交换后信号质量更好。如果机制能解释清楚（"ML 的监督代价让交换更彻底/CMA 恒模代价留下残余"），这就是论文里"为什么用 ML 而不只随便换个固定权重方法"的核心理由。

### ⚠️ 警惕

PROMPT-012 只 10 seeds 且 2 个 degraded 可能是噪声。**先确认差异真实**（加 seed 到 ≥30，看 CMA degraded 比例是否稳定），再深挖机制。

## 2. 必读（按优先级）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D018**（审计结论 + clean/degraded 分类）+ D017（PI 口径定义）
2. `projects/simulation/explore/cma-fade-divergence/PROMPT_012_REPORT.md`（per-seed 数据 + 分类方法）
3. `projects/simulation/explore/cma-fade-divergence/prompt012_longseq_audit.py`（PI-BER + swap 分类实现，复用）
4. `projects/simulation/common/_cma.py`（CMA 梯度：恒模代价 e=R²−|z|²）+ `common/_ml_equalizer.py`（ML：MSE 监督，2×2 蝶形同构）

## 3. 要回答的问题（分层）

### Q1（前置）：交换质量差异真实吗？（加 seed 确认）

PROMPT-012 只 10 seeds，CMA 2/10 degraded 可能是偶然。
- 加到 **≥30 seeds**，N=5M, SOP=4e-7, f_G=30, strong, 20dB
- 报：CMA degraded-swap 占比 / ML degraded-swap 占比 / 两者 PI-BER 分布
- **判据**：若 CMA degraded 比例（如 20%）显著高于 ML（如 0%）且 PI-BER 差异（0.03 vs 0.005）在 ≥30 seeds 下显著 → 差异真实，进 Q2。若差异消失（两者都 clean 或 PI-BER 接近）→ 差异是噪声，**诚实报告"无显著差异"，本方向终止**。

### Q2（核心）：为什么 ML 交换更干净？（机制假设）

Q1 确认差异真实后，建假设解释。候选（你基于理解自己定/补充）：

- **H_a（代价函数差异）**：CMA 恒模代价 e=R²−|z|² 只看幅度，交换后幅度仍满足恒模 → CMA "满意"于次优交换解，不再优化相位/均衡残余。ML 的 MSE 代价看完整星座点（幅度+相位），交换后若星座点不准则代价仍高 → ML 被迫把交换做得更彻底（星座点回归更准）。
  - **验证**：提取 CMA degraded-swap trial 的输出星座图，看残余是相位旋转还是幅度散布。若主要是相位/星座散布 → 支持 H_a。
- **H_b（权重结构差异）**：CMA 在线更新，权重在 SOP 漂移中逐步漂到交换解，过程"拖泥带水"留下中间态。ML 离线训练，权重一次性学到干净的交换映射。
  - **验证**：看 CMA 权重范数轨迹在交换发生点附近是否有振荡（在线更新的拖尾），ML 权重是固定无轨迹。
- **H_c（抽头数/表达力）**：ML CNN 抽头表达力 vs CMA FIR——但两者都是 11 tap 2×2 蝶形同构，这条大概率不成立。快速排除。

**每个假设写明证伪条件**，只验证最有希望的 1-2 个。

### Q3（可选）：clean vs degraded 的决定因素是什么？

扫 f_G / SNR / μ，看什么条件下 CMA 容易 degraded、ML 保持 clean。这给论文"ML 优势的适用条件"画边界。

## 4. 执行方式

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（torch 2.6.0+cu124, CUDA RTX 4070）
- 工作目录: `projects/simulation/`（脚本 `explore/cma-fade-divergence/`，结果 gitignored）
- 复用 prompt012 的 PI-BER + swap 分类（`prompt012_longseq_audit.py`）
- 不改信号模型（SOP=4e-7, GAMMA_BAR=100, T_S=1/2.5e9, BLOCK=100）
- **Q1 优先**，差异不真实就停，不硬挖机制

## 5. 已知陷阱

1. **seed-bias**：≥30 seeds（Q1 确认用），报 per-seed + 占比
2. **PI-BER 不是免费**：报告时注明需帧头开销
3. **degraded 分类要严格**：定义清楚 clean（PI<0.01）/ degraded（0.01<PI<0.2）/ collapse（PI>0.2）的阈值，别主观
4. **别把 2/10 当结论**：Q1 必须加 seed

## 6. 产出格式（强制）

```
# PROMPT-013 研究报告：ML vs CMA 交换质量机制

## TL;DR
[差异真实吗 + 机制是什么 + 对方法贡献的意义]

## Q1: 差异真实性（≥30 seeds）
[CMA/ML degraded 占比 + PI-BER 分布 + 统计显著性]

## Q2: 机制（如差异真实）
[验证的假设 + 证据 + 机制结论]

## 对主控决策的建议
[这个机制能不能作为论文方法贡献点 + 怎么写]

## 产出路径
[脚本 + 结果 JSON]
```

## 附：基线（不用重跑）
- CMA N=5M PI-BER=0.032（8 clean + 2 degraded），ML PI-BER=0.005（10 clean），10 seeds
- 两者都 2×2 蝶形 11-tap 同构，差异来自代价函数（恒模 vs MSE）+ 训练方式（在线 vs 离线）
