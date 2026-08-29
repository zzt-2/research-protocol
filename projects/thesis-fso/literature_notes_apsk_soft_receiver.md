# Ch5 APSK 软接收机 GW Step 3 文献精读

> T046｜2026-08-30｜精读 6 篇既有 qualified full text。
> T049｜2026-08-30｜Q-C5-1 Step 3.5 bounded exact-recipe closure 完成；未进入 Step 4a、实现或实验。

## 概况与进度

- title 自检：6/6 PASS；完整精读：6/6。
- Step 1/2：上游 T040–T044 COMPLETE；Step 3：COMPLETE；Step 3.5：COMPLETE（T049）；Step 4a：NOT ENTERED。

| L# | 论文 | 角色 | read note |
|---|---|---|---|
| L01 | Layton et al. 2018 | C5-1 mandatory comparator | papers/_read_notes/10.1186_s13638-018-1136-z.md |
| L02 | Xie et al. 2009 | APSK soft-feedback baseline | papers/_read_notes/10.1109_vetecs.2009.5073425.md |
| L03 | Wu et al. 2010 | syndrome-state ancestor | papers/_read_notes/10.1109_lcomm.2010.07.100508.md |
| L04 | Baldi et al. 2016 | failure-gated rescue | papers/_read_notes/10.1186_s13638-016-0769-z.md |
| L05 | He et al. 2021 | syndrome/CRC rescue | papers/_read_notes/10.1109_wcsp52459.2021.9613326.md |
| L06 | Zhao et al. 2023 | reliability-guided rescue | papers/_read_notes/10.1109_iccc59590.2023.10507492.md |

## C5-1 公式、估计量与信息边界

Layton 2018 对星座点 \(x_k\) 使用 \(Y|X=x_k\sim\mathcal N(\mu_k,\Sigma_k)\)。其负对数似然（略去公共常数）为

\[
d_k(y)=(y-\mu_k)^T\Sigma_k^{-1}(y-\mu_k)+\log|\Sigma_k|,
\]

bit LLR 对 bit=0/1 两个 symbol 子集的 likelihood 分别求和。pilot-only 直接估计量为

\[
\hat\mu_k=N_k^{-1}\sum_{i:x_i=x_k}y_i,\quad
\hat\Sigma_k=(N_k-1)^{-1}\sum_{i:x_i=x_k}(y_i-\hat\mu_k)(y_i-\hat\mu_k)^T.
\]

论文明确提到低 pilot 数可跨 frame 或使用 biased shrinkage；blind 情况可做 equal-weight GMM/EM，但没有给 APSK 几何结构化 shrinkage estimator。

- receiver-visible：已知 pilots、其接收样本和 constellation labels；不得使用 data-symbol TX truth。
- causal：只用当前/过去 pilot block；跨 frame pooling 必须有窗口或遗忘规则。
- full covariance 每点 2 个均值+3 个 covariance 自由度；16APSK 共 80 个实参数，低 pilot 下易高方差/奇异。
- 跨偏振只可共享超参数/统计强度，不能假定两 tributary 的瞬时样本相同。

### 公平 comparator ladder

| comparator | 模型 | 必须相同的 budget |
|---|---|---|
| isotropic scalar | 全星座共享 \(\Sigma_k=\sigma^2I\) | pilot 位置/样本数、causal window、LLR 实现、decoder/iterations |
| per-ring scalar | 每环 \(\Sigma_k=\sigma_r^2I\) | 同上；ring label 是已知 constellation 信息 |
| unstructured full | Layton 每点 \(\hat\Sigma_k\) | 同 pilot/sample、同正定 floor/shrinkage family、同更新频率；只允许结构约束不同 |

候选 structured estimator 可写成 \(R(\theta_k)\operatorname{diag}(\sigma_{r,k}^2,\sigma_{t,k}^2)R^T(\theta_k)\)，再做跨环/跨偏振 shrinkage pooling；它改变 estimator，不改变已碰撞的 Mahalanobis/log-det demapping 原子。

## C5-1 exact-collision verdict

**NOT_EXACT_COLLISION / STRONG_PRIMITIVE_COLLISION**。

Layton 2018 已完整覆盖“样本依赖 full 2×2 covariance + Mahalanobis/log-det demapping”，该原子不能声称新颖。完整 recipe 仍有可陈述差别：pilot-only causal estimation、APSK radial/tangential structure、跨环/跨偏振 shrinkage pooling，以及同一 pilot/sample budget 下对 isotropic/per-ring/unstructured-full 的比较。Layton 仅给逐点 sample covariance、跨 frame/biased shrinkage 的一般建议和 blind GMM，没有给上述组合 recipe。此结论只保留 Q#，不是 Go。

## 实验完备性（4 篇）

| 论文 | claims/scope | 统计规范性 | baseline/消融 | 信道、复杂度、VVUQ |
|---|---|---|---|---|
| L01 | distortion-dominated APSK/QAM；最高约4 dB required-SNR reduction | 无 seeds/CI；BER到 \(10^{-6}\)，AIC用 \(10^8\) symbols | circular/centroid demapper；pilot/coding/modulation/distortion sweeps | TWTA+phase noise；7 vs 4 multiplies，MATLAB <1%；3/2/1 |
| L02 | APSK BILCM-ID 恢复部分 independent-demapping AMI loss | 无 seeds/CI；64800 bits；8×50 iterations | BILCM、CM/BICM limits；1–8 codeword interleaver | AWGN；复杂度定性；2/2/1 |
| L04 | short TC LDPC IA+MRB 兼顾 CER/复杂度 | 无 seeds/CI；CER与 union/ideal reference | SPA/MS/NMS/MRB/hybrid；quantization/TEP/memory | BPSK-AWGN；binary-op/latency公式；3/2/1 |
| L05 | NR quantized NMS error floor 降约1/2–1/10 | 3.4 dB、\(1.82\times10^8\) trials/100 errors；无CI | BP/NMS/post-process；多K/rate | AWGN、5-bit、100 iter、\(\|s\|\le10\)；2/2/1 |

对标结论：传统通信论文常给大样本 BER/FER/CER 与复杂度，但不报 seed、CI 或显著性；后续若获授权，应采用 paired samples 并报告 error count/CI。其消融以 pilot 数、量化位宽、资源预算和机制开关为主。

## 写作架构

### Layton 2018

- 两个 scenario → reduced model → estimator/demapper → MI/BER/pilot/iterative/complexity → model-fit appendix。
- 先用 constellation clusters/covariance ellipses 证 scalar 假设失效，再统一建模，最后回答 rate、coded BER、pilot sensitivity、EXIT、complexity。
- 可复用骨架：先证“scalar 不足”，再定义 estimator，最后用同预算 ladder 证明结构约束增量。

### Baldi 2016

- 应用约束/目标 CER → code/benchmark → decoder+complexity → error/quantization → memory/latency。
- 将性能、平均复杂度、最坏时延和 memory 同时作为成立条件；适合 C5-2 “普通译码失败才救援”的叙述。

## 综合分析

1. metric 层：L01 用 symbol-dependent full covariance 修正 likelihood；L02 用 decoder extrinsic LLR 反馈恢复 APSK BICM loss。
2. iterative decoder 校正：L03 按 check syndrome 状态切换 normalization/offset。
3. failure rescue：L04 IA→MRB；L05 CRC/syndrome→TS flips；L06 reliability+random subset→narrowed SBF。

- full-covariance demapping 原子已存在；低-pilot结构估计、同预算公平性和时变 causal 更新仍未闭合。
- rescue 依赖 syndrome/CRC/LLR/code graph；当前 adapter 只返回 hard information bits。
- 2009–2018 从 iterative feedback 发展到 full covariance；2021–2023 转向高可靠区的 conditional bounded rescue。
- C5-1 合法起点不是重造 Mahalanobis likelihood，而是 receiver-visible/pilot-limited 条件下用 APSK 几何和 pooling 降估计方差。

## 研究问题清单

| Q# | M | C | A | 产出 | 判据1 | 判据2 | 判据3 | 判据4 | verdict | 来源 |
|---|---|---|---|---|---|---|---|---|---|---|
| Q-C5-1 | Layton逐点 unstructured full-cov estimator | 16APSK、pilot-only causal、每点样本少、DP tributaries | 每点 covariance 可独立稳定估计，无需几何/共享结构 | structured shrinkage estimator+同预算 receiver recipe | ✅ | ✅可复用 | ✅直接 baseline+scalar ladder | ✅NMSE/GMI/BER/FER/复杂度 | **4/4** | L01§3.1/4.3；L02 |
| Q-C5-2 | conventional NMS failure termination | quantized high-SNR floor，且可输出 syndrome/CRC/LLR | failure bits 可由局部 syndrome/reliability辨识 | gated bounded rescue | ✅ | ✅ | ✅L05/L06近期 | ✅FER/触发率/时延 | **条件未过**：当前 adapter 无接口 | L03–L06 |

## Step 3 终态

- read count：6/6；Q#：2；四判据全过：1。
- terminal：STEP3_Q_SURVIVES_READY_FOR_MASTER_REVIEW；不自动进入 Step 3.5/4a。
- 唯一 blocker：Q-C5-2 缺 syndrome/CRC/soft reliability adapter；不阻塞 Q-C5-1。

## Step 3.5 补充闭包（T049）

- 6/6 预注册 query：28 raw / 25 cross-query unique；新增 MUST 0 / SHOULD 2。
- Layton 2018 双向 citation-chain：forward 1、backward 37；新增 MUST 0 / SHOULD 0，Round 2 收敛，未启动 Round 3。
- 两轮总计 66 raw / 63 cross-archive unique；新增全文 0、read note 0。
- exact-action verdict：`Q-C5-1 SURVIVES`；最强邻居仍为 Layton 2018 的逐点 unstructured full covariance + Mahalanobis/log-det demapper。
- claim ceiling：不得声称 covariance demapping、Mahalanobis/log-det、generic shrinkage 首次；只保留 pilot-limited APSK radial/tangential structured estimator + 跨环/跨偏振统计强度 pooling 的完整 recipe 差别。
- 证据：`apsk-soft-receiver-groundwork/step3-5-supplement-report.md` 与 `search-archive/2026-08-30/t049-ch5-structured-covariance-step3-5-receipt.json`。
- 本项只完成 Step 3.5，不授权自动进入 Step 4a。
