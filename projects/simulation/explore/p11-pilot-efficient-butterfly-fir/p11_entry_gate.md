# P11 PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR — Entry Four-Gate (file:line)

> Package: P11 (campaign 探索包；accepted_valid 当前 7/10，本包若有效无论正负变 8/10)
> Authority: 用户 P11 执行指令（同一对话 P10 纠偏 + P11 端到端，2026-08-01）+ D039 campaign
> Date: 2026-08-01
> 研究对象必须按真实实现命名。源码核查结论：模型确为**线性** Butterfly FIR（非 CNN）。

## 门 1 — 模型身份与可作用物理自由度（PASS）

**研究对象 M**：当前 4 路复线性 Butterfly FIR，以 Adam + 大量已知 TX 符号训练。

源码核查（`common/_ml_equalizer.py`）：
- `class ButterflyCNNEqualizer2x2(nn.Module)` 定义于 `_ml_equalizer.py:104`。
- 由 4 个 `ComplexFIRConv1d` 实现（`_ml_equalizer.py:126-129`，wxx/wxy/wyx/wyy），每个 `ComplexFIRConv1d` = 2 个 `nn.Conv1d`（`_ml_equalizer.py:82-85`，conv_RR + conv_RI）。
- **4 复 FIR × 2(实/虚) = 8 个实值 Conv1d**（`_ml_equalizer.py:112` 注释、`compute_rmps` `_ml_equalizer.py:425-435` `8*n_tap`）。
- **bias=False**：`ComplexFIRConv1d.__init__` 两处 `nn.Conv1d(..., bias=False)`（`_ml_equalizer.py:83,85`）。
- **无 activation / 无 normalization**：`forward`（`_ml_equalizer.py:93-101, 131-168`）只有线性卷积 + 加法组合，无 `nn.ReLU/nn.Tanh/nn.BatchNorm` 等。grep `nn.ReLU|nn.Tanh|nn.ELU|nn.GELU|BatchNorm|LayerNorm|activation|dropout` on `_ml_equalizer.py` 零命中。
- 中心抽头脉冲初始化（`_ml_equalizer.py:86-91`，wxx/wyy 中心=1 其余=0），`init_norm=√2`（`_ml_equalizer.py:179-181`）。

**结论（用户指令 §二 line 50）**：源码确认**没有非线性层** → 明确称为 **linear Butterfly FIR**（不得称新 CNN / 深度 CNN）。这是 2×2 MIMO-FIR 结构，监督训练学的是该 FIR 的抽头系数。linear FIR 的监督解有闭式最小二乘（LS），Adam 训练的计算开销是否必要 = 可作用自由度（训练预算/标签预算）。

**STRATEGIC_GATE 条件**（用户指令 §三 line 79）：模型不是线性 FIR，或标签开销非真实部署问题 → STRATEGIC_GATE 不计包。**当前：模型是线性 FIR（PASS），标签开销问题待门 3 量化。**

## 门 2 — 当前训练真实标签预算（PASS）

**当前训练使用多少 TX 标签、标签位于哪里、是否连续取前 50%**：

- `ML_TRAIN_FRAC = 0.5`（`ml_long_seq_failure.py:78` 注释"前 50% 训练，后 50% 测试"）。
- ML 训练调用 `ml.train(rx[:nt], ry[:nt], sx[:nt], sy[:nt], val_split=0.2)`（`p05_ood_online_adaptation.py:101`），`nt = int(N*0.5)`（`ml_long_seq_failure.py:212`）。
- **标签是前 50% 的每一个符号**（连续前缀，`sx[:nt]` 全段），即 50% TX 符号作 label；非稀疏 pilot。
- 同结构 LS 对照 `run_ls_fir_trial`（`ml_long_seq_failure.py:616-668`）也用 `n_train = int(N*ML_TRAIN_FRAC)`（`ml_long_seq_failure.py:624`），同前 50% 连续段。
- P05 freeze identity 同证（`p05_phase0_identity.py:87`：`train_frac: 0.5, val_split: 0.2`；`p05_phase0_identity.py:7` docstring）。

**结论**：当前训练用前 50% 连续段的**全部** TX 符号作监督标签。这是部署级 pilot overhead（50% 的符号必须是已知的 training symbol），远高于实际系统 pilot 预算（典型 <10%）。标签开销是真实的部署问题（PASS 前提）。门 3 量化降预算是否产生可测损失。

## 门 3 — 降低标签预算产生可测性能/吞吐问题（待 Phase A 量化，门成立条件）

**假设**：把可用 TX 标签从"前 50% 连续全段"降到真实低开销 pilot fraction（5%/2%/1% 等）后，最强传统方法（batch complex LS / RLS）在相同 pilot 位置、相同 tap、相同 N 下出现达到 MDE 的 fixed-label BER 损失或 pilot-adjusted goodput 损失。

- linear 2×2 FIR 的监督解 = 4 个复 FIR（4L 复未知数，L=n_tap）的最小二乘。pilot 数 n_p 须 ≥ 4L（实数方程 2·n_p ≥ 8L 复 → n_p ≥ 4L）才超定；n_tap=11 → n_p ≥ 44。50% of N=2M = 1e6 远超定，5% = 1e5 仍远超定，但极低 fraction（n_p 接近 4L）会噪声放大。
- Adam 训练同等标签预算下是否优于闭式 LS：linear FIR 的 MSE 最优解就是 LS（normal equation），Adam 是迭代近似——同标签预算 Adam 不应优于 LS（除非非凸正则）。但 Adam 用全段连续标签 vs LS 用稀疏 pilot 标签是**不同信息量**，须公平合同（同 pilot 位置）下比较。
- **门 3 由 Phase A problem gate 量化裁决**（fair pilot contract，见 freeze receipt contract §fair_pilot_contract）。若 Phase A 证伪（低 pilot 下最强 LS/RLS 已达 full-label Adam 性能-开销 Pareto）→ `PROBLEM_RESOLVED_BY_COMPLEX_LS`（有效负面包，须 held-out confirmation）。

## 门 4 — 有命名传统强比较（PASS）

baseline ladder（用户指令 §六，全部须真实存在、有身份、同信息、独立可调）：

- **B0 full-label Adam**：`MLChannelEqualizer.train`（`_ml_equalizer.py:227-366`），Adam + ReduceLROnPlateau + MSE，前 50% 连续全段标签（性能锚点，明确 50% overhead）。
- **B1 sparse-label Adam**：同 `ButterflyCNNEqualizer2x2` 结构（`_ml_equalizer.py:104`），Adam 训练但只用 pilot 位置标签（同 B2 pilot 位置）；与 B0 唯一差是标签预算。
- **B2 batch complex LS**：`run_ls_fir_trial`（`ml_long_seq_failure.py:616-668`）已实现完整 2×2 蝶形 LS（sliding_window_view 构建 (2n, 4L) 增广矩阵 + `np.linalg.lstsq` `_ml_long_seq_failure.py:658`），须改造为只取 pilot 位置行（fair pilot contract）。
- **B3 RLS/LMS 在线**：`dd_lms_adapter`（`p05_ood_online_adaptation.py:252`）已实现 block-grained decision-directed LMS；须改造为 pilot-position LMS（warm-start pilot 后不再 DD）。RLS（递归最小二乘）须新实现（标准 SRLS，pilot 位置更新）。
- **B4 blind CMA**：`CMAEqualizer2x2`（`common/_cma.py:57-193`，Godard 1980 with-z；corrected Godard-with-z 在 `prompt019_mu_compress_mve.py:96-213`），无 pilot（报告性能差但 zero pilot overhead）。

**collision check（grep 零命中）**：grep `pilot.efficient|pilot-efficient|sparse.label.*butterfly|linear.*butterfly.*pilot|structured.*butterfly.*FIR|low.pilot.*FIR` on `common/`+`explore/` 零命中（无同名既有方法）。

## 门 5 — 候选动作真实存在，非给传统 LS 换名（PASS）

候选（用户指令 §八，最多三个，每个单一主机制）：
- **C1 LS-init + 少量 pilot Adam refinement**：`run_ls_fir_trial`（`ml_long_seq_failure.py:658` lstsq）初始化 `ButterflyCNNEqualizer2x2` 权重 → 少量 pilot 位置 Adam 微调。主机制 = 闭式初始化减少 Adam 收敛所需标签数。**必须证明不是"多跑几步 Adam"**（同总 Adam 步数预算下 LS-init 仍优）。
- **C2 regularized structured 2×2 Toeplitz LS**：在 `run_ls_fir_trial` 上加 Toeplitz/蝶形结构正则（ exploit linear 2×2 MIMO-FIR 结构，非通用 LS）。主机制 = 显式利用 Butterfly/FIR 结构约束。
- **C3 pilot-init + receiver-visible confidence-gated DD refinement**：`dd_lms_adapter`（`p05_ood_online_adaptation.py:252`）pilot warm-start → receiver decision（非 payload truth）+ confidence gate 决定何时 DD 更新。主机制 = confidence-gated decision-directed。

**候选非换名**：C1/C2/C3 主机制不同（init / 结构正则 / DD refinement），且都不是单纯"把 batch complex LS 改个名当方法"（用户指令 §八 line 179）。

## 门 6 — 不踩 Kill 边界 / 不复制 VAE blind 核心 loss（PASS）

- **D032 periodic-pilot fine-tune Kill 边界**（用户指令 §二 line 59）：D032 周期性 pilot 微调（weak Adam 1-step 周期更新）无增量（P05 periodic-pilot comparator `p05_ood_online_adaptation.py:288` 坐实）。**P11 不重开 D032**：C1 是 LS-init（非 weak Adam 周期更新）；C3 是 confidence-gated DD（非周期 pilot 微调）。若 Phase A/B 发现候选等价于 D032 weak periodic-pilot → 判 KILL。
- **VAE/blind equalizer 禁复制核心 loss**（用户指令 §二 line 60）：`_vae_equalizer.py` 的 VAE ELBO 是 Qin 核心贡献（`_ml_equalizer.py:20-23` 注释明示不用 Qin VAE loss）。P11 用 MSE 监督（同 B0/B1）+ LS 闭式，**不复制 VAE ELBO**。blind CMA（B4）只用 Godard `(R²-|z|²)²` 自监督，非 VAE。
- **不复制现有 VAE/blind FIR 论文核心 loss**：C1/C2 用 supervised MSE/LS，C3 用 Godard CMA + confidence gate，均非 VAE ELBO / 非任何 blind FIR 论文的核心生成 loss。

## 门 7 — 文献 collision 决定最高 claim ceiling（PASS，已纳入 claim ceiling）

- claim ceiling 冻结为"面向当前双偏振 FSO 接收链的少导频结构化 Butterfly FIR 训练方法"（用户指令 §十）。
- 不得声称：首创 MIMO LS / 首创少导频均衡 / 新型深度 CNN / 完全盲均衡 / 通用光通信均衡器。
- 文献 collision 在 freeze receipt 记录（pilot-efficient equalization / 2×2 MIMO FIR / coherent optical equalization 是成熟领域，claim 严格 bounded）。

## 入口门综合裁决：CONDITIONAL-PASS → 进 frozen contract + Commit 1

门 1/2/4/5/6/7 PASS（file:line 已举）。门 3（降低标签预算产生可测损失）由 Phase A problem gate 量化裁决——若 Phase A 证伪 → `PROBLEM_RESOLVED_BY_COMPLEX_LS`（有效负面包须 held-out confirmation）；若 Phase A 证实且 Phase C 候选过 METHOD_SIGNAL 门 → `PILOT_EFFICIENT_BUTTERFLY_METHOD_SIGNAL`。

**STRATEGIC_GATE 触发条件（用户指令 §三 line 79）**：若核查发现模型不是线性 FIR（已否——是线性），或标签开销非真实部署问题（门 3 由 Phase A 裁决，当前不成立 STRATEGIC_GATE）。
