# PROMPT-010: ML 长序列失效专题研究 — SOP 漂移下固定权重方法的边界

> 文件名: PROMPT-010-ml-long-seq-failure-investigation.md
> 用途: 在新对话中执行，查清"ML 在长序列/SOP 大漂移下是否也失效"这个动摇方法层核心的问题
> 来源: 主控对话深查 D014 时发现（2026-07-12）
> 性质: **这是研究/诊断任务，不是跑固定实验。要回答开放问题，先建假设再设计实验证伪。**

## 0. TL;DR（先读）

你在 `projects/simulation/`。手上有一套 CMA/ML/oracle 双偏振均衡仿真。
**你的任务**：查清一个动摇方法层核心结论的问题——**ML 均衡器在长序列（SOP 累积漂移大）下是否也会像 CMA 一样失效？如果是，"ML 优于 CMA"的结论适用边界是什么？**
**产出**：结构化研究报告（≤1500 词）+ 验证脚本 + 结果 JSON，回传给主控。
**最高纪律**：1. 这是开放问题，先写假设+证伪判据再跑；2. 跑出来什么记什么，不为"好看"调参数；3. 不要自己写决策(D###)，只报事实，决策由主控定。

## 1. 背景（理解任务必需的，标"了解即可不对照评价"）

研究项目 Q-CMA-FADE：星地 GG 湍流下 CMA 发散分析 + ML 均衡缓解。方法层一直声称"ML 优于 CMA"（S009/D011/D012/D013/D014）。

**主控在验证 D014 时发现一个可能动摇该结论的现象（需你查清）**：

之前所有"ML 优于 CMA"的 BER 对比都用 **N=2M 符号**。主控把序列拉到 N=5M 后发现：
- ML（CNN 监督，前 50% 训练后 50% 测试）：N=2M 时 test-late BER=0.0000，**N=5M 时 test-late BER=0.4999（崩）**
- CMA：N=2M 和 N=5M 的 test-late BER 都 ≈0.5

疑似原因：ML 固定权重（离线训练），test 段 SOP 累积旋转超出训练见过的角度范围后，固定权重跟不上 SOP 漂移，失效。N=2M 时 test 段 SOP 只漂 22.9°（训练见过，ML 行）；N=5M 时 test 段漂 57.3°（超出训练范围，ML 崩）。

**如果这个猜想成立，意味着**：ML 并未真正"解决"CMA 的问题，只是短序列（小 SOP 漂移）下表现好。方法层"ML 优于 CMA"有隐藏前提（序列短/SOP 漂移小）。这动摇 S009/批次1/批次2 的核心结论。

**了解即可，不对照评价**：分析层贡献（发散概率/条件判据/CMMA 不降发散/冻结无效）与本题无关，那些是确定的。

## 2. 必读（按优先级）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D014**（机制：SOP 驱动极化串扰）+ D011（原方法层定位）+ D012（批次1）
2. `.sessions/2026-07-10-dual-pol-osl-groundwork/S011-batch2-method-reinforcement.md`（末尾"主控续接"段有相关性诊断 + SOP×f_G 矩阵 + ML 长序列失效的初步证据）
3. `projects/simulation/explore/cma-fade-divergence/r_lcr_ber_impact.py`（S009 BER 脚本，gen_channel 信号模型 + ML 训练接口）
4. `projects/simulation/common/_ml_equalizer.py`（ML 架构：注意它**也是 2×2 蝶形** wxx/wxy/wyx/wyy，跟 CMA 同构）
5. `projects/simulation/common/_cma.py`（CMA equalize 返回 zX/zY/w_norm_traj）
6. `projects/simulation/explore/cma-fade-divergence/README.md`（参数溯源表）

## 3. 要回答的核心问题（分层，逐个证伪）

### Q1（最关键）：ML 在长序列下失效是真实的，还是单次偶然？

主控只跑了 1 seed（N=2M/5M）。你必须**多 seed（≥10）+ 多 N** 确认。
- N ∈ {2M, 3M, 5M, 8M}，每 N 跑 ≥10 seeds，f_G 固定 30Hz，SOP=4e-7，strong，SNR=20dB，QPSK
- 报：ML test-late BER（test 段后 1/4）的 mean±std，按 N 分组
- **判据**：若 N 增大时 ML test-late BER 单调上升且 N=5M 时显著 > early 段 → 失效真实。若各 N 都接近 0 → 主控的单次结果是偶然，ML 长序列不失效。

### Q2：失效的边界条件是什么？（量化"SOP 漂移阈值"）

把 SOP 漂移量当作自变量，找 ML 开始失效的临界点。
- 固定 N=5M，扫 SOP_RATE ∈ {0, 1e-8, 1e-7, 4e-7, 1e-6, 1e-5}（对应不同 SOP 漂移速率）
- 或固定 SOP_RATE，扫 N（等价扫 test 段 SOP 累积旋转）
- 报：ML test-late BER vs "test 段 SOP 累积旋转角度"
- **目标**：找出 ML 失效的 SOP 旋转临界角（如"test 段漂移超过 X° 后 ML BER 显著上升"）。这个临界角是论文里"ML 适用边界"的关键数字。

### Q3：失效机制是什么？（确认是 SOP 漂移超出训练范围，还是别的）

主控猜想是"固定权重跟不上 test 段 SOP 漂移"。设计对照实验确认：
- **对照 A**：训练集覆盖更大 SOP 角度范围（如训练用 SOP_RATE 更大的数据，或训练数据更长覆盖更多旋转）→ test 同样漂移下，ML 是否不崩？
- **对照 B**：周期性重训练（每 test 段 1/4 用前 1/4 重新训练 ML）→ 是否解决？
- **对照 C**：非 ML 固定 LS-FIR（纯线性回归前馈，主控已测 N=5M 下也崩 BER=0.50，你复现确认）
- **判据**：若对照 A（训练覆盖更大 SOP）使 ML 不崩 → 确认机制是"训练 SOP 范围不足"。若对照 B（重训练）解决 → 机制是"权重需随 SOP 更新"。

### Q4（可选，时间够再做）：这是不是所有固定权重方法的通病？

测 1-2 种其他固定权重方法（如非 ML 的 LS-FIR，主控已初步测过）在同样的 N/SOP 扫描下是否同样失效。若是 → 结论泛化到"所有固定权重方法"。

## 4. 执行方式

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（3.11.9, torch 2.6.0+cu124, CUDA RTX 4070）
- 工作目录: `projects/simulation/`（脚本放 `explore/cma-fade-divergence/`，结果放 `results/cma-fade-divergence/`，注意 results/ 被 gitignore 不入 git）
- 复用 `r_lcr_ber_impact.py` 的 gen_channel（**不要改信号模型**，保持跟 S009/批次1 一致：SOP=4e-7, GAMMA_BAR=100, T_S=1/2.5e9, BLOCK=100）
- ML 训练接口：`MLChannelEqualizer(n_tap=11, lr=0.005, batch_size=1024, n_epochs=20, device='cuda', patience=5)`，`ml.train(rX[:nt], rY[:nt], sX[:nt], sY[:nt], val_split=0.2, verbose=False)`，`ml.equalize(rX[nt:], rY[nt:])` 返回 dict 含 `zX`/`zY`
- Q1 优先（最关键），时间紧的话 Q2/Q3 可降 seed 数

## 5. TL-20 假设声明（跑之前写，跑完对照）

先写你的预期，跑完对照（偏离即查）：
- H1（主控猜想）：ML 长序列失效真实，机制是固定权重跟不上 test 段 SOP 漂移。预测 N↑ 或 SOP_RATE↑ → ML test-late BER↑。
- H2（备选）：ML 不失效（主控单次是偶然/seed-bias）。预测各 N 下 ML test-late BER 都≈0。
- **证伪条件**：若 H1 成立，应有 ML test-late BER 与"test 段 SOP 累积旋转角度"强正相关（r>0.7）。

## 6. 已知陷阱（基于历史失败）

1. **seed-bias**：h_mean 跨 seed CV≈1.0（D012），绝对 BER 噪声大。**必须多 seed（≥10）+ 报 mean±std**，单 seed 结果不可信。
2. **N=2M 的假象**：N=2M test 段短（SOP 漂移小），所有方法看起来都还行——不要用 N=2M 下结论，要扫 N。
3. **切片对齐**：ML test 段是 rX[nt:]，长度 N-nt，算"test-late"要在 test 段内取后 1/4，不是原序列的后 1/4（主控第一次就切错了，注意）。
4. **不要改信号模型/参数**：跟 S009/批次1 保持一致才能横向对比。如要扫 SOP_RATE 那是 Q2 的自变量，不是"改参数让结果好看"。
5. **BER 计算做 4 旋转相位校正**（QPSK π/2 模糊），参考 r_lcr 的 compute_ber_phase_corrected。
6. **不要自己写 D### 决策**：你只报事实+数据，"这对方法层意味着什么"由主控判断。产出里可以写"对主控决策的建议"但不自作主张。

## 7. 产出格式（强制，回传给主控）

返回 ≤1500 词结构化研究报告：

```
# PROMPT-010 研究报告：ML 长序列失效边界

## TL;DR
[一句话结论：ML 长序列是否失效 + 边界 + 机制]

## Q1: 失效是否真实（多 seed 多 N）
[表格：N × ML test-late BER mean±std + 判定]

## Q2: 失效边界（SOP 临界角）
[ML test-late BER vs SOP 累积旋转角 + 临界角数字]

## Q3: 失效机制（对照 A/B/C）
[对照结果 + 机制确认]

## Q4（如做）：固定权重通病性
[结论]

## TL-20 假设对照
[H1/H2 哪个成立 + 证据]

## 对主控决策的建议（不自作主张）
[这些发现对 D011/D014 方法层叙事的影响建议，但不写决策]

## 产出路径
- 脚本: explore/cma-fade-divergence/ml_long_seq_failure.py
- 结果: results/cma-fade-divergence/ml_long_seq_failure_results.json
```

## 附：主控已查到的关键事实（你不用重跑，作为基线对照）

- 单 seed（seed=1, f_G=30, SOP=4e-7, strong, 20dB, QPSK）：N=2M ML test-late BER=0.0000，N=5M ML test-late BER=0.4999
- 同 seed CMA test-late：N=2M=0.4934，N=5M=0.4996
- 相关性诊断（N=5M late 段）：CMA 的 corr(zX,sY)=0.92（极化串扰），ML 的 corr(zX,sX)≈0 corr(zX,sY)≈0（完全乱码，非串扰是另一种失效）
- 非 ML 固定 LS-FIR（N=5M, 训练前1M）：test-late BER=0.50（也失效）
- SOP=0 时所有方法都不失效（SOP 是唯一诱因）
- test 段 SOP 累计旋转：N=2M→22.9°，N=5M→57.3°（训练只见过 0° 到 train 段旋转角）
