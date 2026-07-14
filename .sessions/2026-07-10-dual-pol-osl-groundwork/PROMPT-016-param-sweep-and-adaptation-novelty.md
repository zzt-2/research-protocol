# PROMPT-016: A 边 — 扩参数域鲁棒性验证（5 seeds）+ 改动1（发散判据驱动 ML 训练调度）新颖性快查

> 文件名: PROMPT-016-param-sweep-and-adaptation-novelty.md
> 用途: 在新对话中执行。两段任务：(1) 5 seeds 扩参数域，拿 ML 优势鲁棒性曲线给论文 results 用；(2) 快查"发散判据驱动 ML 训练调度"的新颖性
> 来源: D022（PROMPT-015 GO，方法层卖点解冻）+ 用户"两边同时推"+ "能不能动一点点让它好一点点"
> 性质: **A 边，低优先机械活 + 新颖性前置查。主控不等本结果，并行推 B 边（PROMPT-017）。**

## 0. TL;DR（先读）

你在 `projects/simulation/`。PROMPT-015 确认 ML 优于 standard-CMA（30 seeds, p=1.19e-6），但**只在一个参数点**（N=5M/QPSK/strong/f_G=30/SOP=4e-7）。而且方法层创新性软（照搬 Qin CNN + 机制说不清）。

**你的任务分两段**：
- **段 1（机械活）**：5 seeds 扩参数域，看 ML 优势在 f_G/SNR/调制变化下稳不稳，拿曲线给论文画图
- **段 2（新颖性快查）**：查"用发散判据驱动 ML 训练调度"有没有人做过——这决定路线 A 能不能从"搬场景"升级为"有方法创新"

**最高纪律**：
1. 段 1 用 **5 seeds**（用户明确：非最终版数据 5 seeds 够；只有写进论文的最终结论才补到 30）
2. 段 2 严守场景鉴别（PROMPT-011 教训）：RF/光纤有人做不算，查 FSO/卫星光
3. 不自己写 D###，结果回传主控

## 1. 必读

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D022**（GO 结论 + 适用边界）+ D006（发散 μ 主导 + 条件判据）
2. `projects/simulation/explore/cma-fade-divergence/PROMPT_015_REPORT.md`（四方法对比 + per-seed 数据）
3. `projects/simulation/explore/cma-fade-divergence/prompt015_unified_baseline.py`（**复用**：四方法对比框架、standard-CMA 实现、ML-original/aligned）
4. `projects/simulation/explore/cma-fade-divergence/ml_long_seq_failure.py`（gen_channel + run_ml_trial + oracle_equalize）
5. `projects/thesis-fso/literature_notes.md` L778-780（JR-CMA/L-DP8：自适应步长在 FSO 的先例——改动1 要跟它区分）

## 2. 段 1：扩参数域鲁棒性验证（5 seeds）

### 目的

PROMPT-015 只在 f_G=30 一个点验证。论文需要展示 ML 优势的**适用边界**——是普遍的还是在特定条件下才显著。

### 参数网格（5 seeds 每个 cell，seeds 1000-1004）

固定：N=5M（或降到 2M 加速？见下）、QPSK、strong 湍流、SOP=4e-7、T_S=1/2.5e9、BLOCK=100

变化维度（**先跑这 3 个，不是全扫描**）：

| 维度 | 取值 | 为什么 |
|---|---|---|
| **f_G** | 30（已知）/ 100 / 1000 | 动态性递增，看 ML 优势是否随 f_G 变化。30 已有 30-seed 数据作锚 |
| **SNR** | 20dB（已知）/ 15dB / 10dB | 降 SNR 看噪声对 ML/CMA 差距的影响 |
| **调制** | QPSK（已知）/ 16QAM | D008 发现 16QAM 下 CMA modulus mismatch，看 ML 在高阶星座的表现 |

**执行建议**：
- f_G 扫 3 点 × 5 seeds = 15 cells（QPSK/20dB，只变 f_G）
- SNR 扫 3 点 × 5 seeds = 15 cells（QPSK/f_G=30，只变 SNR）
- 16QAM 1 点 × 5 seeds = 5 cells（f_G=30/20dB，只变调制）
- 共 ~35 cells，每 cell 四方法（current-CMA/standard-CMA/ML-original/oracle，**ML-aligned 可省**——P015 已证初始化不敏感）
- **N 可降到 2M 加速**（P012 已审计 N=2M 的 ML>CMA 成立）；若 2M 则每 cell 更快

### 产出

每个 cell：四方法的 PI-BER + fixed-BER（双口径并报）+ 超额 PI-BER + 配对 ML vs standard-CMA 胜场。

画三张趋势图（主控后续画）：
1. PI-BER vs f_G（CMA/ML/oracle 三线）
2. PI-BER vs SNR
3. QPSK vs 16QAM 对比

**不画 Go/No-Go 判据**——这是鲁棒性展示不是预注册判决。

## 3. 段 2：改动 1 新颖性快查（发散判据驱动 ML 训练调度）

### 背景：为什么查这个

方法层当前是"照搬 Qin CNN + 新场景"，创新性软。主控提出一个可能的小改动：

> 分析层确认了 CMA 发散的**条件判据**（S005：μ×σ_n×AFD 阈值关系；S008：μ 主导 + LCR 次级 + 深衰落非必要触发）。当前 ML 是固定训练（train 一次用到底）。**改动**：ML 根据信道状态（接近发散条件时）触发重训练/微调。

**核心创新点**（如果能成立）："分析层发散判据驱动的 ML 均衡器训练调度"——Qin 没做过（Qin 固定训练），JR-CMA 没做过（JR-CMA 调 CMA 步长不调 ML）。

### 要查的问题

**Q-new-1**：自适应/在线重训练 ML 均衡器在光通信有没有人做过？
- 关键词：online retraining equalizer、adaptive neural network equalizer、incremental learning equalizer、adaptive DNN equalizer
- 场景鉴别：RF/光纤的在线学习均衡器可能有，查 FSO/卫星光
- 区分：有人做"ML 均衡器"（Qin/Nasr）≠ 有人做"根据信道状态自适应重训练 ML 均衡器"

**Q-new-2**：用物理判据/发散检测来触发 ML/NN 训练有没有人做过？
- 关键词：physics-informed training trigger、divergence-aware retraining、channel-state-aware learning rate
- 这是改动 1 的核心——不是"在线学习"本身（那是老话题），是"用发散判据当触发信号"

**Q-new-3**：JR-CMA 的自适应步长 vs 改动 1 的训练调度，本质区别是什么？
- JR-CMA：调 CMA 在线更新步长 μ_CMA
- 改动 1：调 ML 重训练触发（ML 权重是离线学的，训练完冻结；改动是"何时重训练"不是"在线更新权重"）
- 查：这个区别在文献里有没有被清晰区分，还是被混为一谈

### 产出

每个问题给：有无先例 + 代表论文（标题/场景/做了什么）+ 改动 1 能否与它们区分。

**致命判断**：如果"自适应重训练 ML 均衡器"已被覆盖（尤其 FSO 场景），改动 1 也是"场景迁移"不值做。如果"用物理判据触发训练"无人做过，改动 1 有真创新空间。

## 4. 执行方式

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（torch 2.6.0+cu124, CUDA RTX 4070）
- 工作目录: `projects/simulation/`
- **段 1**：复用 prompt015 脚本框架，隔离脚本 `prompt016_param_sweep.py`，不改 `common/`
- **段 2**：`tools/search`（英文）+ `tools/search --source cnki`（中文）；已有论文库先查
- **先跑段 2 再跑段 1**——段 2 查完如果改动 1 死了，段 1 还是要跑（拿鲁棒性数据），但你知道方法层没有升级空间了
- 或者**并行**：段 2 开子 agent 查，段 1 你自己跑

## 5. 已知陷阱

1. **seed 数**：段 1 用 5 seeds（用户明确非最终版够用）。但若某 cell 的 ML vs CMA 胜场是 3/5 这种接近的，标注"需加 seed 确认"
2. **PI-BER 双口径**：fixed + PI 必须并报（D018 规定）
3. **N=2M vs 5M**：若用 2M 加速，注意 P012 审计只覆盖 f_G=30/100/1000 的 N=2M；新参数点（不同 SNR/16QAM）用 2M 须标注"未独立审计 2M 在这些点的适用性"
4. **16QAM**：D008 发现 CMA modulus mismatch，ML 也受影响（批次1发现 ML/CMA gap 反预期小于 QPSK）。诚实记录，不挑数据
5. **改动 1 的陷阱**：R7"冻结无效"的阴影。改动 1 的"重训练触发"如果触发太频繁 = 等于全程在线训练（那就不是离线 ML 了）；触发太少 = 等于固定训练（那改动没意义）。查文献时注意这个边界

## 6. 产出格式（强制）

```
# PROMPT-016 研究报告：扩参数域鲁棒性 + 改动1新颖性

## TL;DR
[ML 优势在扩参数域稳不稳 + 改动1 有没有创新空间]

## 段 1：扩参数域（5 seeds）
### f_G 扫描
[per-cell PI-BER + 配对胜场 + 趋势]
### SNR 扫描
### 16QAM
### 小结
[ML 优势的适用边界]

## 段 2：改动 1 新颖性
### Q-new-1 自适应重训练 ML 均衡器
### Q-new-2 物理判据触发训练
### Q-new-3 与 JR-CMA 的区别
### 小结
[改动1 能/不能升级为方法创新]

## 对主控决策的建议
[路线 A 的天花板 + 改动1 值不值得投入]

## 产出路径
[脚本 + 结果 JSON + 检索记录]
```
