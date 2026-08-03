# Read Note — Galijasevic 2024

> paper_id: Galijasevic | 首读 2026-08-03 | 用于方向: AMC Groundwork (family-A direct, coded-chain+prediction module) | 重读次数: 0
> 源文件: papers/doi/10.1109_ojcoms.2024.011100/content.md
> 关联: S004 / literature_notes_amc.md

## 身份
- Title: Predicting Channel Conditions for Adaptive LDPC Coding in a Fading Free-Space Optical Channel
- DOI: 10.1109/OJCOMS.2024.011100 | Venue: IEEE OJCOMS, 2024 (gold OA CC-BY 4.0) | 正式发表
- content.md:481 行；title self-check Jaccard≈0.7（PASS）

## M-C-A
- M: 固定码率或 perfect-CSI 零延迟选码
- C: LEO sat FSO 衰落信道 + 相干时间 10ms + **反馈延迟 0-4ms**（对应 150-600km LEO 距离）[content.md:19,55,66,68]
- A: 零阶/无预测在延迟下信道已去相关（autocorrelation 随 τ 下降），固定码率触发深衰落中断；失效位置 §I.A 末[14] + §V 自相关图 [content.md:51,156]
- 方法产出形态: algorithm（多项式预测+阈值表查表选码）+ closed-form family（Polyanskiy normal approximation FER）

## AMC 关键语义
- deployable action: YES — TX LDPC 码率选择（16 个离散值 8/9…8/77，全集 8/9…8/80 共 72 个，PBRL k=8192），由 RX 预测反馈 [content.md:57,74,114,288]
- CSI: RX 估 fading gain（基于 OOK ON/OFF 高斯统计 µ₁/σ₁,µ₀/σ₀）[content.md:158,167]
- decision timescale: per-codeword（码字 3.69-31.5µs ≪ τ₀=10ms）[content.md:114,179]
- CSI feedback delay: **显式 td∈{0,1,2,3,4}ms**，round-trip，error-free 反馈信道 [content.md:19,66,116]
- turbulence: **lognormal** 衰落（FIR 滤波高斯+非线性变换）+ asymmetric Gaussian（基于 APD 实测[21]），PSI=10；**非 GG**；无 pointing [content.md:120,152,263]
- detection: **IM/DD** direct（APD，OOK）；非 coherent [content.md:158,167]
- coding/HARQ: **YES, in ACTION** — PBRL LDPC（72 码率）完整设计（RCA 阈值 + ACE-PEG 提升 d_ACE=6,η=7,lifting 4→256,k=8192）；**无 HARQ** [content.md:57,288,309]
- objective: rate-max（吞吐 = 零延迟吞吐的百分比）[content.md:91,388]
- baselines: zero-delay perfect CSI（100% 上界）；固定码率无反馈（理论积分）[content.md:280,334]
- oracle: YES — zero-delay throughput 作 100% 上界 [content.md:91]
- key numbers: 线性预测 1ms→97.96%、2ms→101.3%；二次预测 3ms→89.92%、4ms→73.67%；码率 8/9…8/77 [content.md:95,97,179,388]
- complexity: polyfit 最小二乘+查表，复杂度低；LDPC 解码硬件成熟（DVB-S2/SDA OCT v3.1.0 标准）[content.md:53,354]

## 与目标重合/缺失
- 重合: **LEO 卫星 + 真实 coded chain（PBRL LDPC 在 ACTION）+ information uncertainty 建模（反馈延迟下预测）+ AMC 码率自适应 + FER 1e-6 工程目标 + 对接 OCT/DVB-S2 标准**
- 缺失: **非 coherent**（IM/DD+OOK）、**非 GG**（lognormal）、**无 HARQ**、无调制阶数自适应（仅码率）
- 直接竞品判定: **adjacent/boundary**（coded-chain + info-uncertainty 维度高度重合，但 coherent+GG 两项缺失，需改造方可 head-to-head）

## 问题四判据
- problem_truth: ✅ | actionability: ✅ | novelty: ✅ | thesis_fit: ⚠️（coded+uncertainty 强对标，但 IM/DD+lognormal 与目标 coherent+GG 不重合，需信道模型替换）
- 结论: thesis_fit 受限（需模型替换才能量化对标）
