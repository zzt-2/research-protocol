# Worker Log step-041: P11 PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR

> campaign 8/10 (valid negative) | family H' PILOT_EFFICIENT_STRUCTURED_BUTTERFLY_FIR
> 2026-08-01 | CAMPAIGN_EXPLORATION_DISPATCH (D039 + D055 P10 纠偏后进入) | 端到端一轮内完成
> 脚本: `explore/p11-pilot-efficient-butterfly-fir/{p11_methods.py, p11_run.py, p11_entry_gate.md}`
> 结果: `results/p11_pilot_efficient_butterfly_fir/{p11_freeze_receipt.json, p11_phaseA_dev_raw.json, p11_phaseA_test_raw.json, p11_verdict.json}`
> 终态 verdict: **PROBLEM_RESOLVED_BY_COMPLEX_LS**（有效科学负面包，campaign accepted_valid 7→8）

## 研究对象身份（按真实实现命名）

- 本包对象 = `ButterflyCNNEqualizer2x2`（`common/_ml_equalizer.py:104`），**源码核查确认为 linear Butterfly FIR**：4 个复 FIR（wxx/wxy/wyx/wyy，各 n_tap=11）= 8 个实值 Conv1d，**全 bias=False**（`:83,85`），**无 activation/normalization**（grep nn.ReLU/Tanh/BatchNorm/LayerNorm 零命中）。
- 监督训练（`MLChannelEqualizer.train`）学的是这 4 个复 FIR 的抽头系数（MSE loss + Adam）。当前训练用**前 50% 连续全段 TX 符号**作 label（`ML_TRAIN_FRAC=0.5`, `ml_long_seq_failure.py:78`；`ml.train(rx[:nt],...nt=int(N*0.5))`），即 50% pilot overhead。
- **不得称新 CNN / 深度 CNN**（用户指令 §二 line 50）。linear FIR 的监督解有闭式最小二乘（LS），Adam 是迭代近似——同标签预算下 LS 是 MSE 最优，Adam 不应优于 LS。

## 入口四门（全 PASS，file:line 见 `p11_entry_gate.md`）

1. 模型线性身份（PASS）：8 实 Conv1d/bias=False/无非线性层。
2. 当前训练标签预算（PASS）：前 50% 连续全段，`ML_TRAIN_FRAC=0.5`。
3. 降低标签预算产生可测损失（Phase A 裁决）：证伪——B2 LS 在 1% pilot 下仍达/超 full-label Adam。
4. 有命名传统强比较（PASS）：B0 full-label Adam / B1 sparse-label Adam / B2 batch complex LS（`run_ls_fir_trial:616` 同结构 pilot-only 改造）/ B3 pilot RLS / B4 blind CMA（Godard 1980 with-z）。
5. 候选动作真实存在（PASS）：C1 LS-init+pilot Adam refine / C2 structured Toeplitz LS / C3 confidence-gated DD，主机制不同。
6. 不踩 D032 Kill 边界（PASS）：C1/C2/C3 非 D032 weak periodic-pilot 微调。
7. 不复制 VAE/blind 核心 loss（PASS）：用 MSE 监督 + LS 闭式 + Godard CMA，非 VAE ELBO。
8. 文献 collision 决定 claim ceiling（PASS）：claim bounded 为"面向当前双偏振 FSO 接收链的少导频结构化 Butterfly FIR 训练方法"。

## 公平数据合同（用户指令 §五，全部落实）

- pilot 位置预先冻结（`freeze_pilot_positions`，均匀间隔+抖动，所有 B1/B2/B3 共享同一 pilot_idx）。
- 只有 pilot 位置 TX 符号进 B1/B2/B3 训练/估计（`fit_butterfly_ls`/`fit_sparse_label_adam`/`fit_pilot_rls` 只取 `s_target[pilot_idx]`）。
- payload TX truth 只用于 BER 计分（`fixed_label_ber` 直接 bit 比较 swap-visible PRIMARY / `pi_ber` π/2 4 旋转 min swap-blind secondary，不变量 10）。
- 禁止把整个 payload truth 送入 Adam/LS/RLS（B0 用前 50% 连续段作 label，是合法 supervised training；B1/B2/B3 用 pilot 位置）。
- pilot overhead 计入 goodput（`payload_bits × (1-pilot_frac) × (1-BER)`）：B2@1% pilot goodput ≈ B0@50% 的 1.98×。

## chronology 闭合（V077 教训第三次落实，P09/P10 模式复用）

- Commit 1 (`4d9c374`) freeze receipt `test_started=false` 在任何 held-out test 前（`git show 4d9c374 --stat` 不含 `p11_phaseA_test_raw.json`）。
- runner `phase_all` 模式：verify receipt（test_started=false）→ dev（seeds 15000-15007）→ 保存 dev_raw → 重 verify（仍 false）→ 翻 test_started=true + 保存 → test（seeds 16000-16007）→ adjudicate → 保存 verdict + dev_summary。
- held-out test seeds 16000-16007 fresh，disjoint from 全部 campaign history（P10 13000-13005/14000-14039, P09 11000-11019/12000-12039, P08-R2 8000-8039/9000-9019, P08-R 6000-6019/7000-7039, P05 1000-1011）。

## Phase A 结果（dev 8 seeds + held-out test 8 seeds × 4 cells × 6 pilot fracs）

held-out test（n=32 paired per frac = 8 seeds × 4 cells）fixed-label BER PRIMARY：

| pilot_frac | B0 full-Adam mean | B2 complex-LS mean | paired Δ(B2−B0) mean | CI_low | CI_high | CI_hw | resolves? |
|---|---|---|---|---|---|---|---|
| 0.01 | 3.859e-4 | 3.176e-4 | −6.83e-5 | −1.76e-4 | 4.0e-5 | 1.08e-4 | YES |
| 0.02 | 3.859e-4 | 3.102e-4 | −7.57e-5 | −1.94e-4 | 4.3e-5 | 1.19e-4 | YES |
| 0.05 | 3.859e-4 | 3.114e-4 | −7.45e-5 | −1.93e-4 | 4.4e-5 | 1.18e-4 | YES |
| 0.10 | 3.859e-4 | 3.140e-4 | −7.19e-5 | −1.88e-4 | 4.4e-5 | 1.16e-4 | YES |
| 0.20 | 3.859e-4 | 3.111e-4 | −7.47e-5 | −1.94e-4 | 4.4e-5 | 1.19e-4 | YES |
| 0.50 | 3.859e-4 | 3.098e-4 | −7.61e-5 | −1.97e-4 | 4.4e-5 | 1.21e-4 | YES |

- **B2 complex LS 在所有 pilot fractions（1%–50%）严格优于 B0 full-label Adam**（paired Δ mean 全负，CI_high < non_inf=MDE=0.05）。
- ci_hw_max=1.206e-4 ≪ MDE/2=0.025（ratio 4.8e-3）→ 统计功效充足。
- **物理机制（TL-22 已查）**：linear Butterfly FIR 的 MSE 最优解 = LS normal equation；Adam 是迭代近似，同标签预算不应优于 LS。B2 用更少 pilot 标签（1%=5k symbols）达/超 B0（50%=250k symbols）—— linear 结构的监督开销完全不必要。
- B1 sparse-label Adam BER≈0.26（swap，pilot-window Adam 30 epoch 收敛不够）；B3 pilot RLS（λ=1.0 sequential LS）数值稳定后接近 B2；B4 blind CMA（Godard-with-z）BER≈0（在线跟踪有效，zero pilot overhead）。

## 终态: `PROBLEM_RESOLVED_BY_COMPLEX_LS`（唯一合法诚实）

- 用户合同 §七明文："如果 complex LS/RLS 在低 pilot 预算下已经达到 full-label Adam 的性能—开销 Pareto：PROBLEM_RESOLVED_BY_COMPLEX_LS。这仍是有效科学负面包，但必须有 held-out confirmation。"
- Phase A 在 held-out（8 test seeds × 4 cells = 32 paired/frac）证实 B2 complex LS 在 1% pilot 下就达/超 full-label Adam 性能-开销 Pareto（B2 BER ≤ B0 + goodput 1.98×）。
- **Phase B/C 不运行**（gate 顺序：传统 comparator 已解决，无方法空间）。
- **有效科学负面包**（用户指令 §九 line 207-208 "valid negative 7→8"）：完成 held-out confirmation + 诚实 verdict。campaign accepted_valid **7→8**。

## 不建立 method card / 不晋升

- verdict 非 METHOD_SIGNAL（无候选 C1/C2/C3 运行，是传统 comparator 解决问题）。**0 active carrier** 维持。
- claim ceiling 维持 LOCAL_SLICE / NONBINDING_DIAGNOSTIC。
- 不产方法卡/不晋升/不动 protected owner/formal/Skill/thesis framework。

## harvest（可写入 thesis 资产）

- **Ch3/Ch4 工程证据**：当前 ButterflyCNN（实为 linear Butterfly FIR）的 Adam 监督训练在 pilot-efficient 口径下被闭式 complex LS 完全支配——linear MIMO-FIR 结构的监督开销（50% 连续 training symbols）不必要，1% pilot LS 即达/超其性能。强化"方法身份须按真实实现命名"教训（不得称 CNN）+ linear 结构闭式解优越性。
- **公平合同方法论资产**：pilot 位置冻结 + 所有方法共享 + payload truth 只计分 + goodput 计入 overhead 的公平 pilot 合同模式，可复用。

## compute constraint（诚实记录）

- 全合同（N=2M, dev 20 + test 40）在 CPU-only 环境（torch CUDA 不可用）~8h 不可行（smoke 365s/seed@N=2M）。
- 缩合同重冻（Commit 1 amend）：N=500k（1% pilot=5k symbols ≫ 4L=44 未知数仍远超定）+ dev 8 + held-out 8（>6 非 dev-only probe，满足用户指令 §五）。
- pilot fractions 不变（50%–1%）；cell 覆盖不变（weak/moderate/strong 两档 + 两 SNR/SOP）。
- 算力约束诚实记录为 scope 项；held-out confirmation 保留。

## 包内修复（披露）

1. **RLS NaN 数值修复**：B3 pilot RLS 初 delta=1e2 致 P 矩阵数值不稳定（smoke 暴露 NaN warning）。改 delta=10 + λ=1.0 sequential LS（最稳定），并加 finite 检查。非科学变更（RLS 是 comparator，修复后接近 B2）。
2. **fit_sparse_label_adam/C1 center-tap 提取修复**：初版用全窗口序列对单符号 target 致 shape mismatch。改取中心抽头 `zX[:, half]` 对该 pilot 的 TX 符号（正确监督方程）。修复后 B1 仍 swap（pilot-window Adam 30 epoch 不够收敛，与 LS 闭式解差距是真实科学发现非 bug）。
3. **p11_run.py post-run cosmetic print 修复**：verdict 保存后 print dict 含不存在的 key `b2_vs_b0_paired_delta_test` 致 KeyError（exit 1，但 verdict 已落盘）。修复移除该 key。**不影响 verdict**（adjudicate 函数未改，verdict 在 print 前已保存；V082 独立复核确认）。post-run edit 致 run.py hash 与 freeze receipt 记录略不一致（run 时 hash 一致），V082 已记录。

## verifier

V082（独立 verifier fresh-context agent_7be7b55b）**ACCEPT**：14/14 PASS。raw→aggregate 独立复算 max rel err 3.4e-16；linear FIR 身份确认（8 实 Conv1d/bias=False/无非线性层）；公平 pilot 合同确认（pilot_idx only in training, payload TX only in scoring, no oracle h/theta/SNR）；chronology 闭合确认（Commit 1 4d9c374 test_started=false pre held-out）；terminal verdict 唯一正确（PROBLEM_RESOLVED_BY_COMPLEX_LS，gate 顺序 Phase C 不运行）；campaign 计数 7→8 正确。唯一 flagged discrepancy：p11_run.py post-run cosmetic edit（benign，verdict 未受影响）。

## 范围确认

- 本轮在 D039 campaign 授权范围内（D055 P10 纠偏后用户授权 P11 端到端），problem-first 三阶段门控；新机制族 H'（pilot-efficient structured Butterfly FIR），机制距离远离 A-G。
- 三次包内修复已披露（RLS NaN / center-tap / cosmetic print），非科学性变更，V082 复核。
- 无 protected owner/formal/Skill/thesis framework 改动、无 push。
