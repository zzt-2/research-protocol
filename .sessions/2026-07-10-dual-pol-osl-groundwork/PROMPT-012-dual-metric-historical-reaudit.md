# PROMPT-012: 双口径重审 S005-S011 历史结论 — 固定标签 BER + 排列不变 BER

> 文件名: PROMPT-012-dual-metric-historical-reaudit.md
> 用途: 在新对话中执行，用双口径复核 Q-CMA-FADE 关键结论的成立性
> 来源: D017（主控对 D016 的修正 + 双口径重审任务定义）+ 用户选定"双口径重审"
> 性质: **审计任务，不是探索。对每个历史结论给出双口径数字 + 成立/需修正/否证判定。**

## 0. TL;DR（先读）

你在 `projects/simulation/`。背景：PROMPT-011 发现 CMA 在 SOP 漂移下会发生 X/Y 偏振交换（zX 输出 sY 数据），固定标签 BER=0.47 但排列不变 BER=0.03。这 questioning 了 S005-S011 所有 CMA 相关结论。
**你的任务**：在**固定标签 BER + 排列不变 BER 双口径**下，复核 4 个关键结论，输出"成立/需修正/否证"矩阵。
**产出**：审计报告（≤1500 词）+ 复核脚本 + 结果 JSON。回传主控。
**最高纪律**：1. 双口径同时报，不偏袒任一口径；2. ≥10 seeds（D012/D015 seed-bias 债务）；3. 不改信号模型/参数；4. 不自己写 D###，只报事实+判定建议。

## 1. 背景（理解任务必需的，"了解即可不对照评价"）

### 两口径定义（核心，必须用对）

- **固定标签 BER（fixed-label）**：zX 对 sX、zY 对 sY 算 BER，做 QPSK 4 相位校正（0/90/180/270）。这是 S005-S011 一直用的口径。**问题**：若 CMA 把 X/Y 输出交换了，固定标签会报 0.5（假性失效）。
- **排列不变 BER（permutation-invariant, PI）**：对 zX/zY 的 2 种排列 × 各自 4 相位（共 2!×4×4=32 组合，但实际只需对 sX 比较两个输出口取 min）取最低 BER。**意义**：消除盲分离固有的 X/Y 排列歧义。但注意——**接收端实际不知道哪个口是 X，消歧需要 pilot/帧头开销**，所以 PI-BER 是"有开销辅助下的上界"，不是免费性能。

### 为什么重审（D017 简版）

PROMPT-011 发现 late 段 CMA 发生 X/Y 交换（3/3 seeds），PI-BER 从 0.47 降到 0.03。这意味着：
- S005-S011 报的"CMA BER 高/失效"可能部分是排列交换（PI 下可恢复，需开销）而非真失效
- 但**不是全部**——S005 发散（范数爆炸）、D014 非交换塌缩（corr(zX,sX)=0.32 非 0.877）排列不变也救不了
- 需要逐结论分清：多少是交换型（PI 可恢复）、多少是真失效（PI 也救不了）

### ⚠️ 不要犯的错（D016 的夸大，主控已纠正，你不要重犯）

1. **不要把"代码缺 z 因子"当重审主因**——D017 已证明它不影响性能（标准 CMA 和当前 CMA PI-BER 几乎一样）。重审主因是排列口径。
2. **不要把 PI-BER=0.03 说成"CMA 没失效"**——交换需帧头开销消歧，是"可恢复但有代价的失效"，不是免费。
3. **不要用 3 seeds 下结论**——PROMPT-011 只 3 seeds，你必须 ≥10。

## 2. 必读（按优先级）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D017**（主控修正 + 本任务定义）+ D016（执行对话原始结论，参考其局限）+ D014（极化串扰机制）+ D015（ML 长序列失效）
2. `projects/simulation/explore/cma-fade-divergence/PROMPT_011_REPORT.md`（X/Y 交换发现 + PI-BER 方法）
3. `projects/simulation/explore/cma-fade-divergence/prompt011_cma_root_diagnostic.py`（PI-BER 实现，复用）
4. `projects/simulation/explore/cma-fade-divergence/r_lcr_ber_impact.py`（S009 信号模型）
5. `projects/simulation/common/_cma.py`（CMA 实现；注意缺 z 因子但 D017 证明不影响性能，不要纠结这个）

## 3. 要复核的 4 个结论（逐个双口径判定）

### 复核 1: S005 发散分析（μ 主导发散，条件判据 μ≤1e-3 安全/≥1e-2 危险）

**原结论（D006）**：发散由 μ 主导，发散条件判据已给。
**复核问题**：发散是权重范数爆炸（cur_norm > 10×init）。这个定义跟排列交换无关（范数爆炸≠交换）。但要确认——**发散的 trial 里，有多少是"范数爆炸"vs"排列交换被误判为发散"？**
- 方法：重跑 S005 关键格（μ=1e-2 危险区 + μ=1e-3 安全区，strong, f_G=100/1000），≥10 seeds。对每个发散 trial 检查：是范数爆炸（cur_norm 大）还是只是排列交换（范数稳定但 BER 高）。
- **判定**：若发散主要由范数爆炸驱动（非排列交换）→ **结论成立**。若大量"发散"实为排列交换误判 → **需修正**（发散定义要补排列检查）。

### 复核 2: D014 极化串扰（SOP 驱动）—— 交换型 vs 非交换型比例

**原结论（D014）**：SOP 驱动 CMA 极化串扰，corr(zX,sY)=0.92。
**复核问题**：late 段失效里，多少是纯交换（corr(zX,sY)高 + corr(zY,sX)高，PI 可恢复）、多少是非交换塌缩（corr 都低，PI 救不了）？
- 方法：N=5M, SOP=4e-7, f_G=30, strong, ≥10 seeds。late 段对每 seed 分类：交换型（zX↔sY 且 zY↔sX，PI-BER<<fixed-BER）/ 同源奇异（zX≈zY）/ 非交换塌缩（corr 都<0.5）/ 发散。
- 报：各类型占比 + 双口径 BER。
- **判定**：若大部分是交换型（PI 可恢复）→ D014"等于断开"**需修正**为"可恢复但需开销"。若有显著非交换塌缩 → **D014 真失效部分保留**。

### 复核 3: D015 ML 长序列失效 —— 排列不变口径下 ML 是否也失效

**原结论（D015）**：ML 长序列（N=5M）test-late BER=0.497（固定标签），全 10 seeds 崩。
**复核问题**：**这是最关键的**。排列不变口径下 ML 是不是也 0.5，还是也能降到 0.03？
- 方法：N=5M, SOP=4e-7, f_G=30, ≥10 seeds，ML（前 50% 训练后 50% 测试）。双口径 BER。
- **判定**：
  - 若 ML PI-BER 也 ≈0.5（排列救不了）→ D015 **成立**，ML 真失效（固定/PI 都崩）
  - 若 ML PI-BER ≈0.03（排列可恢复）→ D015 **需修正**，ML 也是交换型，跟 CMA 同病
- **这条决定 ML 卖点存不存在**，务必查清。

### 复核 4: S009/批次1 "ML 优于 CMA" —— 双口径下还成不成立

**原结论（S009/D012）**：ML 全 f_G 优于 CMA（1.8-数百倍）。
**复核问题**：N=2M（S009 用的）下，双口径对比 ML vs CMA。
- 方法：N=2M, SOP=4e-7, f_G=[30,100,1000], strong, ≥10 seeds。CMA/ML 双口径 BER。
- **判定**：
  - 若 fixed-label 下 ML<<CMA 但 PI 下 ML≈CMA → 原"ML 优于 CMA"**是排列假象**（CMA 交换拉高了 fixed BER）
  - 若 PI 下仍 ML<CMA → **结论保留**（ML 真优，非排列因素）
- 注：结合 D015（长序列 ML 也失效），即使 N=2M PI 下 ML 优，也只在小 SOP 漂移范围成立。

## 4. 执行方式

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（3.11.9, torch 2.6.0+cu124, CUDA RTX 4070）
- 工作目录: `projects/simulation/`（脚本 `explore/cma-fade-divergence/`，结果 `results/` gitignored）
- 复用 `prompt011_cma_root_diagnostic.py` 的 PI-BER 实现 + `r_lcr_ber_impact.py` 的 gen_channel（不改信号模型：SOP=4e-7, GAMMA_BAR=100, T_S=1/2.5e9, BLOCK=100）
- **优先级**：复核 3（ML PI-BER）最关键，先做。复核 2/4 次之。复核 1（S005 发散）大概率不受影响，最后做。

## 5. 已知陷阱

1. **seed-bias**：≥10 seeds + 报 per-seed + mean±std
2. **PI-BER 不是免费性能**：报告时必须注明"需帧头/pilot 开销消歧"
3. **ML test 段切片**：test 段内取后 1/4 作 late，不是原序列后 1/4（PROMPT-010 切错过）
4. **发散 vs 交换**：发散是范数爆炸（cur_norm>10×init），交换是范数稳定但输出换了偏振。复核 1 要分清
5. **不要纠结代码 z 因子**：D017 已证不影响性能，不是重审重点

## 6. 产出格式（强制，回传主控）

返回 ≤1500 词审计报告：

```
# PROMPT-012 审计报告：双口径重审 S005-S011

## TL;DR
[一句话：4 个结论各成立/需修正/否证]

## 复核矩阵
| 结论 | fixed-BER | PI-BER | 判定 | 理由 |
|---|---|---|---|---|
| S005 发散(μ主导) | ... | ... | 成立/需修正/否证 | ... |
| D014 极化串扰 | ... | ... | ... | 交换型X% / 非交换X% |
| D015 ML长序列失效 | ... | ... | ... | ML PI-BER=? |
| S009 ML优于CMA | ... | ... | ... | PI下ML?CMA |

## 各复核详细数据
[per-seed + 分类（交换/同源/塌缩/发散）占比]

## 对主控决策的建议（不自作主张）
[哪些结论能进论文 / 哪些要重写叙事 / ML卖点是否存在]

## 产出路径
[脚本 + 结果 JSON]
```

## 附：关键基线（你不用重跑，对照用）

- CMA(当前实现) N=5M fixed-label late BER=0.47, PI-BER=0.03（PROMPT-011，3 seeds，主控复现确认）
- late 段 X/Y 交换：corr(zX,sY)=0.877, corr(zY,sX)=0.874（主控独立复现）
- 标准 CMA PI-BER=0.035 ≈ 当前实现 0.031（代码 z 因子不影响性能，D017）
- ML N=2M fixed-label test-late BER=0.05（D015，但 PI 口径未测——你要补）
- oracle late BER≈0.004-0.014
