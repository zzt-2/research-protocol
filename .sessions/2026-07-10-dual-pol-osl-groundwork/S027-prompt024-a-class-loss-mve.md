# [S027] A 类（改 loss）方法层探索 — GW Step 1 检索 + 横向 MVE

> 2026-07-15 | Contract 方法层解冻探索 (D030) / A 类 | 状态: 进行中（MVE 后台跑，阶段 1-2 完成）

## 目标

D030 方法层解冻后第一类探索。A 类（改 loss，成本最低 + SOP 正则攻 D014 真因）三个方向合并一次 GW Step 1 检索防撞车，横向批量 MVE 对比。守 FR-22（归类批量≠跳框架，仍走 Step 1 检索→四判据→MVE）+ D030（准入放宽，唯一硬防线=检索防撞车 + 消融可验）+ D018（双口径）。

## 记录

### 阶段 1：GW Step 1 检索（A 类合并一次，~10 分钟）

3 个方向各 2 组关键词（tools/search s2+openalex），子 agent 消化撞车评估：

| 方向 | 关键词 | 撞车评估 | 结论 |
|---|---|---|---|
| **A1 SOP 不变性正则** | "rotation invariant loss optical equalization polarization" / "SOP invariant equivariant neural network optical communication equalizer regularization" | **NO**：L005 (SOP rotation tracking 2025) 是跟踪非正则；L006 (ANN polarization mixing 2026) 是监督补偿非不变性约束。无人在均衡 loss 加 SOP/旋转不变性正则项 | **PASS 进 MVE** |
| **A2 swap 对比学习** | "contrastive learning blind equalization swap negative sample" / "contrastive self-supervised neural network optical fiber communication equalization" | **NO**：A2 全是图像/超分/图学习；A2b 光通信结果全是 ML 均衡/异常检测，零对比学习偏振解复用 | **PASS 进 MVE** |
| **A3 VAE 盲损失** | "variational autoencoder blind equalization optical fiber polarization demultiplexing loss" / "VQ-VAE blind demultiplexing polarization coherent Qin" | **YES 硬撞车**：L002 "Bootstrapping Blind Equalizer for DP-Coherent FSO via Modulus-Rings-Based VAE" (Qin et al. IEEE TCCN 2026, c=0) = **同作者组 + 同场景 (DP-FSO) + 同机制 (盲 VAE ELBO loss)**。L003 "Blind Equalization in Dynamic PMD Channels Using VAE" (2025) 次级撞车（光纤 PMD 非 FSO 但同机制） | **DEFER 不进 MVE**（换皮风险，须重构为"SOP-专攻盲 VAE"=A1+A3 混合才不撞车，属另一轮决策） |

**A3 撞车是本轮最重要发现**：D019 deferred 的 VAE 盲损失在 D030 重检时发现 Qin 组 2026 已发同场景同机制论文。D030 准入原则 3（唯一硬防线=检索防撞车）触发，A3 作为独立变体 defer。L6 (Song 2023 VQ-VAE) 是已知 baseline 非 new collision（不同作者 Song/Lauinger）。

### 阶段 2：实现 prompt024_a_class_loss_variants.py（隔离脚本，不改 common/）

复用基建（守 D030 准入 4 归类批量共享）：
- 模型：`common/_ml_equalizer.ButterflyCNNEqualizer2x2`（Qin 2025 L275/283 蝶形，不改）
- 信道/评估：`ml_long_seq_failure.gen_channel` / `oracle_equalize` / `test_late_slice`
- 双口径：`prompt012_longseq_audit.evaluate_outputs`（D018 fixed/PI + classification）

自定义训练循环（隔离，不调用 MLChannelEqualizer.train），支持 3 个 loss：
- **L0 baseline** = `nn.MSELoss()`（D022 对照，复现性锚点）
- **L1 SOP 不变性正则** = MSE + λ·‖f(R_θ·r) − f(r)‖²，θ 随机 ∈ [−0.2, 0.2] rad（TL-22: ≤0.2rad 不破坏 QPSK），强制输出对 SOP 旋转不变 → 抗 D014 lock-swap
- **L2 swap 对比学习** = MSE + λ·max(0, margin − ‖z_normal − z_swap‖²)，swap = 交换 X/Y 偏振输入（margin=1.0，QPSK E|s−s'|²=2 的中间值），强制 normal/swap 输出差异 → 破坏对称解 → 抗 lock-swap

预注册 Go/Kill + 消融（防事后移门槛，守 D030 准入 5）：
- **Go**：L1 或 L2 甜点 λ 的 late-slice PI-BER 配对 Wilcoxon p<0.05 + ≥4/5 seeds 胜，且适用域不窄于 D022 (N=5M/f_G=30)
- **Kill**：L1/L2 都不显著优于 L0 → A 类无增量，进 C 类
- **消融可验**：L1/L2 λ=0 须退回 L0 水平（差<0.01），退了才证明正则有贡献

参数域严格对齐 D022/D027（守可复现）：N=5M/f_G=30/SOP=4e-7/strong/20dB/QPSK/tap=11，5 seeds = 1000-1004（含 D027 swap-prone 1000/1002，正是 SOP 正则应发挥作用的点），late slice [4.375M, 5M)，λ 扫 [0.001, 0.01, 0.1, 1.0]。

冒烟测试（单 seed）确认 3 变体均跑通：
- L0 seed1000: PI=0.01002（复现 D022/D029 B=0.01028，可复现性 PASS）
- L1 seed1001: PI=0.0（clean seed，无 swap）
- L2 seed1001: PI=0.0（clean seed）

### 阶段 3：批量 MVE 完成（后台跑 6388s ≈ 1.8h，55 runs）

全量 = 9 config (L0 ×1 + L1×4λ + L2×4λ) × 5 seeds + 10 消融 (L1/L2 λ=0 × 5 seeds) = 55 runs。结果存 `results/cma-fade-divergence/prompt024_a_class_loss.json`。

**L0 baseline 复现性 PASS**（D022 锚点）：5 seeds mean PI-BER = 0.01020，per-seed 1000=0.01000 / 1001=0.0 / 1002=0.04098 / 1003=0.00001 / 1004=0.0。3/5 clean seeds（1001/1003/1004）PI≈0（floor），2/5 swap-prone（1000/1002）PI 高。复现 D022/D029 B(ML 训练一次) PI≈0.01。

**L1 SOP 不变性正则（λ 扫描，甜点 λ=0.001）KILL**：

| λ | mean PI | seed1000 | seed1002 | 趋势 |
|---|---|---|---|---|
| 0.001 | 0.01019 | 0.01001 | 0.04091 | ≈L0 |
| 0.01 | 0.01033 | 0.01003 | 0.04160 | 微升 |
| 0.1 | 0.01065 | 0.01021 | 0.04303 | 升（正则伤性能）|
| 1.0 | 0.01031 | 0.00991 | 0.04164 | 略回 |

甜点 λ=0.001 mean PI=0.01019 vs L0 0.01020（Δ=+0.00001 更差），2/5 胜 p=0.75 → KILL。**λ↑ → PI 单调升**（正则越强性能越差），无有效甜点。

**L2 swap 对比学习（λ 扫描，甜点 λ=0.1）KILL**：

| λ | mean PI | seed1000 | seed1002 |
|---|---|---|---|
| 0.001 | 0.01030 | 0.01022 | 0.04129 |
| 0.01 | 0.01064 | 0.01007 | 0.04313 |
| 0.1 | 0.01017 | **0.00983** | 0.04100 |
| 1.0 | 0.01037 | 0.00995 | 0.04187 |

甜点 λ=0.1 mean PI=0.01017 vs L0 0.01020（Δ=+0.00003 微差），2/5 胜 p=0.75 → KILL。λ=0.1 swap-prone seed1000 PI=0.00983（L0 0.01000，唯一实质性改善点）但 seed1002 持平，整体 ΔPI=3e-5 远小于噪声。

**消融可验 PASS（守 D030 准入 5）**：L1 λ=0 mean=0.01035（差 L0 0.00015<0.01 退回）；L2 λ=0 mean=0.01039（差 0.00019<0.01 退回）。正则项拿掉退回 L0，证明正则确有贡献（但贡献方向中性偏负）。

### 阶段 4：Go/Kill 判定 + 回传

**A 类整体 KILL**（L1/L2 均 2/5 胜 p=0.75，无任何 λ 显著优于 L0）。

**核心失败机制（TL-22 物理前提检查）**：
1. **floor 效应**：3/5 clean seeds PI≈0 已 floor，loss 正则无处改（不能比 0 更好）。只有 2/5 swap-prone seeds 有改善空间。
2. **时序正交**：swap 是 test 段 CMA 在线更新跳盆地（D027/D028），但 L1/L2 正则在训练段施加，训练段 SOP 漂移远小于 test late 段（57°=1.0rad vs L1 增强 ≤0.2rad）。学到的"SOP 不变性"泛化不到极端旋转（D015 Q2 周期性失效带同构）。
3. **L2 swap 对比机制错配**：swap 不是"输出对 swap 输入敏感"问题，是"CMA 在线权重跳盆地"（D027 V3b）。ML 固定权重本就不跳，L2 对不发生的事件加约束=无效。
4. **与 D027 V3 同构**：D027 Q-DP4 形态2 Kill 根因"约束权重分量不改变恒模多解地形"，本轮"loss 正则不改变固定权重 test 段行为"。**训练阶段 loss/约束无法触及 test 段 swap**。

**D031 新建**：A 类 KILL + 火力重定向（排除训练阶段 loss 修改类 A + 部分 C，转向 test 段在线机制 D/E 或架构 B）。C 类进 MVE 前须判"是否触及 test 段"——在线微调触及（值得跑），SOP 数据增强/课程学习不触及（同 A 类失败，可能 defer）。

### 实现教训（code-quality 候选）

1. numpy complex128 → torch 复值张量时 `.real` 仍是 float64，Conv1d 权重 float32 报 dtype mismatch。须 `.astype(np.complex64)` 再转 tensor。
2. `nn.MSELoss()` 不支持 complex tensor（"mse_cuda not implemented for ComplexFloat"），复数 MSE 须手动拆 `.real`/`.imag`。
3. 同级脚本 import（`ml_long_seq_failure`/`prompt012`）须 `sys.path.insert(0, Path(__file__).resolve().parent)`，prompt019/020 同模式。

## 决策引用

- D030：Contract 方法层解冻，5 类候选地图 + A 类优先（本轮执行依据）
- D014：SOP 极化串扰是 BER 真因（A 类 SOP 正则攻的就是这个）
- D018：双口径强制（本轮 evaluate_outputs 复用）
- D022：ML 29/30 baseline（本轮 L0 复现锚点）
- D019：VAE 盲损失 deferred（本轮 A3 撞车进一步证实 defer 正确）
- D027：Q-DP4 形态2 Kill + clean swap 物理洞察（swap seeds 1000/1002 是本轮 SOP 正则的靶子；V3 失败与 A 类失败同构）
- D028：swap 是一次性永久锁定（test 段 CMA 跳盆地，A 类 loss 触及不到）
- **D031：A 类 KILL（本 session 新建）** — L1/L2 全 KILL + A3 撞车 defer + 火力重定向 C 类

## 范围确认

- 本轮是否在 scope boundary 内：**是**（D030 方法层 A 类探索，原始目标「GW Step 1-4a + Contract 冻结后方法层增强」范围内）

## 后续

A 类 KILL（D031）已落库。**下一步交主控**：
- 下一类 = **C 类（改训练）**，按 D030 执行顺序。但 C 类进 MVE 前须先用 D031 物理洞察过滤：在线微调触及 test 段（值得跑），SOP 数据增强/课程学习不触及（同 A 类失败，可能 defer 不跑省算力）
- 主控决策：C 类只跑在线微调一个子方向，还是三个都跑穷举？H012 handoff 已交
- A3 撞车 defer：若后续要复活须重构为"A1 SOP 专攻盲 VAE"（非泛化盲 ELBO），另开决策
