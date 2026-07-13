# PROMPT-015: 统一合法 baseline 后重比 — 修正 standard CMA + ML 交叉支路初始化混杂

> 文件名: PROMPT-015-unified-baseline-reaudit.md
> 用途: 在新对话中执行，解除 PROMPT-013 暴露的两个 baseline 混杂，做 30-seed 三方对比，判定 ML 卖点是否成立
> 来源: D021（统一合法 baseline 重比立项）+ S015（主控对 PROMPT-013 的独立核验）
> 性质: **预注册的 Go/No-Go 判决实验。目标是回答"去掉 baseline 混杂后，ML 相对经典 CMA 的交换质量优势是否还在"。**

## 0. TL;DR（先读）

你在 `projects/simulation/`。背景：PROMPT-013 确认 ML 相对**项目 current CMA 实现**交换质量更优（30/30, p=1.86e-9），但 Q2 暴露两个 baseline 混杂：
1. current CMA 梯度缺输出因子 z（scalar-error），standard CMA（补 z）在 2/3 high-gap seed 上消除差距（0.033→4.5e-5，752×/688×）
2. ML 交叉支路 wxy/wyx 中心初始化为 1，CMA 为 0——两者起点不同

**你的任务**：解除这两个混杂，在预注册 30 seeds 上做 current-CMA / standard-CMA / ML 三方对比，用预注册判据判定 ML 优势是否经得起合法 baseline。
**产出**：三方对比研究报告（≤1200 词）+ 验证脚本 + 结果 JSON。回传主控。
**最高纪律**：1. 判据已预注册（D021），不得事后移动门槛；2. 诚实记录（Go 或 No-Go 都接受）；3. 不自己写 D###。

## 1. 两个混杂的精确定义（必须完全按此解除）

### 混杂 1：CMA 梯度因子 z

- **current**（`common/_cma.py:163-166`）：`e = R² − |z|²`；`w += μ·e·conj(r)` —— **缺 z**
- **standard**（Q2 实现 `explore/cma-fade-divergence/prompt013_swap_mechanism_q2.py:302-305`）：`w += μ·(e·z)·conj(r)` —— **有 z**（标准 Godard 1980）

**处理方式**：三方对比必须同时包含 current 和 standard 两个 CMA 变体。**不改 `common/_cma.py`**（共享文件，隔离诊断原则）。在隔离脚本里复用 Q2 的 `_cma_deltas` 函数（它已正确实现两个变体）。

### 混杂 2：ML 交叉支路初始化

- **CMA**（`common/_cma.py:81-86`）：wxx/wyy 中心=1，**wxy/wyx=0**（对角初始化）
- **ML**（`common/_ml_equalizer.py:88-89`，`ComplexFIRConv1d.__init__`）：**4 个 FIR 中心全=1**（wxx/wyy/wxy/wyx 中心都=1），注释 `_ml_equalizer.py:114` 说"wxy/wyx=0"与实现不符

**处理方式（预注册，二选一对照，不拍板单一修法）**：同时跑两个 ML 初始化版本，避免人为偏置：
- **ML-original**：保持现状（4 FIR 中心全=1）——反映现有实现的真实性能
- **ML-aligned**：wxy/wyx 中心改为 0（与 CMA 对齐）——消除初始化混杂后的公平比较

两个版本都跟两个 CMA 变体比。这样无论 ML-aligned 结果如何，都不会被指责"人为削弱/增强 ML"。**不改 `common/_ml_equalizer.py`**，在隔离脚本里通过 monkey-patch 或子类化改初始化。

## 2. 必读（按优先级）

1. `.sessions/2026-07-10-dual-pol-osl-groundwork/decisions.md` **D021**（本任务决策 + 预注册判据）+ D020（PROMPT-013 PARTIAL 结论）
2. `projects/simulation/explore/cma-fade-divergence/PROMPT_013_REPORT.md`（Q2 发现 + standard CMA 数据）
3. `projects/simulation/explore/cma-fade-divergence/prompt013_swap_mechanism_q2.py`（**复用**：`_cma_deltas` 函数 L294-306 是 standard CMA 的正确实现；`run_cma_diagnostic` 是隔离 CMA 运行器；`evaluate_outputs` 是 PI-BER + swap 分类）
4. `projects/simulation/explore/cma-fade-divergence/prompt013_swap_quality_q1.py`（**复用**：Q1 的 30-seed 框架 + 连续指标 + Wilcoxon 配对检验）
5. `projects/simulation/common/_cma.py`（current CMA，L163-166 梯度）+ `common/_ml_equalizer.py`（ML，L88-89 初始化）
6. `projects/simulation/explore/cma-fade-divergence/ml_long_seq_failure.py`（`gen_channel` 信号模型 + `run_ml_trial` + `oracle_equalize`，复用）

## 3. 实验设计（预注册，锁定）

### 冻结参数（与 PROMPT-013 Q1 完全一致，保证可比）

- N=5M 符号，SOP=4e-7，GAMMA_BAR=100（20dB），T_S=1/2.5e9，BLOCK=100，strong 湍流，QPSK
- f_G=30 Hz
- seeds 1000–1029（**与 Q1 完全相同的 30 seeds**，shared realization per seed）
- CMA: n_tap=11, μ=MU_SAFE（从 ml_long_seq_failure 导入，与 Q1 一致）, R2=R2_QPSK, block_size=64
- ML: n_tap=11, lr=0.005, batch_size=1024, n_epochs=20, patience=5, train_fraction 与 Q1 一致

### 四个方法

| 标签 | 实现 | 初始化 |
|---|---|---|
| **current-CMA** | `_cma.py` 原样（缺 z） | 对角（wxx/wyy=1, wxy/wyx=0） |
| **standard-CMA** | Q2 `_cma_deltas` 的 standard 分支（有 z） | 对角（同上） |
| **ML-original** | `_ml_equalizer.py` 原样 | 满蝶形（4 FIR 中心全=1） |
| **ML-aligned** | ML 但 wxy/wyx 中心改 0 | 对角（与 CMA 对齐） |
| **oracle** | MMSE，已知信道（参考上界） | — |

每 seed 共享同一 realization（gen_channel 的 rX/rY/sX/sY），五个方法都用同一份。

### 预注册判据（Go/No-Go，写死在 D021，不得事后改）

**主判据（连续指标）**：
- 每方法每 seed 的**相对 oracle 超额 PI-BER** = PI-BER(方法) − PI-BER(oracle)
- 三组配对比较（双侧精确 Wilcoxon 符号秩检验 + 配对胜场）：
  1. **standard-CMA vs ML-original**（核心：去掉 z 因子混杂后 ML 还赢吗）
  2. **standard-CMA vs ML-aligned**（核心：去掉 z 因子 + 初始化混杂后 ML 还赢吗）
  3. current-CMA vs ML-original（对照，应复现 Q1 的 30/30）

**Go 判据**（方法层卖点立住）：配对 1 **和** 配对 2 都满足 p<0.05 且 ML 胜场 ≥25/30
**No-Go 判据**（卖点塌缩）：配对 1 **或** 配对 2 不满足（p≥0.05 或 ML 胜场 <25/30）
**中间态**（卖点需重新定位）：配对 1 满足但配对 2 不满足（去掉 z 混杂 ML 还赢，但去掉初始化混杂后不赢）——诚实报告，交主控判断

**辅助描述（不参与 Go/No-Go）**：clean/degraded-swap 分布，同时报 0.05 和 0.01 两阈值，注明"分类仅描述性"。

### 次要产出（机制线索，不参与 Go/No-Go）

记录 standard-CMA 在哪些 seed 上消除差距、哪些不消除（Q2 已发现 seed 1011 standard 无效）。若 No-Go，这个分布帮助主控理解"差距是纯 bug 还是有真实成分"。

## 4. 执行方式

- Python: `/c/Users/zzt/scoop/apps/python311/current/python`（torch 2.6.0+cu124, CUDA RTX 4070）
- 工作目录: `projects/simulation/`（脚本放 `explore/cma-fade-divergence/`，结果 gitignored）
- **隔离脚本**：新建 `prompt015_unified_baseline.py`，不改 `common/` 下任何共享文件
- **复用** Q1 的 30-seed 框架、连续指标、Wilcoxon；复用 Q2 的 standard CMA 实现
- ML-aligned 的初始化修改：用 monkey-patch `ComplexFIRConv1d.__init__` 或子类化，不改源文件。验证修改生效（打印 4 个 FIR 的中心值确认 wxy/wyx=0）
- **每 trial 报 elapsed_s**，估算总时长（5 方法 × 30 seeds，ML 训练是大头）

## 5. 已知陷阱

1. **seed-bias**：h_mean 跨 seed CV≈1.0（AR(1) ρ≈0.97，非 bug）。30 seeds 是 Q1 已用数量，保持一致；报 per-seed + mean±std
2. **PI-BER 不是免费性能**：报告注明需 pilot/帧头开销消歧
3. **别让硬阈值决定 Go/No-Go**：clean/degraded 分类只作辅助描述（同时报 0.05/0.01），主判据是连续超额 PI-BER + Wilcoxon。PROMPT-013 已发现阈值摇摆（CMA degraded 2/10 vs 4/10）
4. **别只看均值**：Q2 的教训——standard CMA 在均值上看似无差别（D017 的错误），但在 high-gap seed 上消除差距。报 per-seed 配对，不只看均值
5. **shared realization 必须严格**：每 seed 一个 gen_channel 输出，五个方法共用。偏离则不可比
6. **ML-aligned 不是"削弱 ML"**：是为了公平。若 ML-aligned 比 ML-original 差，说明原初始化有信息泄漏（初始就耦合 X/Y 帮助了学习）；若差不多，说明初始化不是混杂来源。两种结果都有价值

## 6. 产出格式（强制）

```
# PROMPT-015 研究报告：统一合法 baseline 三方对比

## TL;DR
[Go / No-Go / 中间态，一句话 + 核心数字]

## 四方法对比（30 seeds, N=5M, SOP=4e-7, f_G=30）
[per-seed PI-BER 表 + 超额 PI-BER 均值 + clean/degraded 分布]

## 三组配对统计检验
[每组 Wilcoxon p + 配对胜场 + 是否满足主判据]

## Go/No-Go 判定
[按预注册判据判定，引用具体数字]

## 机制线索（次要）
[standard-CMA 在哪些 seed 消除差距；ML-original vs ML-aligned 差异]

## 对主控决策的建议
[ML 卖点是否成立 + 怎么写论文 + 是否需要进一步实验]

## 产出路径
[脚本 + 结果 JSON + 测试]
```

## 附：已有基线（不用重跑，作对照验证）

| 比较 | Q1/PROMPT-013 已确认 | 本任务应复现 |
|---|---|---|
| current-CMA vs ML-original | ML 30/30, p=1.86e-9, CMA超额0.0147 vs ML0.00115 | 应一致（同 seeds 同实现） |
| standard-CMA（6 seeds Q2） | high-gap 1006/1017 降 752×/688×；1011 无效 | 30 seeds 上看是否系统性 |
| ML-aligned | 未测 | 本任务首次 |

## 附：Go/No-Go 后的影响（主控用，执行对话了解即可）

- **Go**：方法层卖点"ML 优于经典 CMA"立住，可进写作准备
- **No-Go**：卖点塌缩为"ML 优于一个有 bug 的 CMA 实现"，需重新定位方法层贡献（可能转回纯分析层 + limitation），或回头处理 D019 盲 VAE 寻找不依赖此混杂的新卖点
- **中间态**：交主控判断，可能需要进一步拆解（如 fixed weight 非 ML 对照）
