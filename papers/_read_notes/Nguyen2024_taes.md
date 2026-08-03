# Read Note — Nguyen 2024

> paper_id: Nguyen2024 | 首读 2026-08-03 | 用于方向: AMC Groundwork (family-A direct, delayed-CSI/predictive rate+power) | 重读次数: 0
> 源文件: papers/doi/10.1109_taes.2024.3403809/content.md
> alt_ids: 10535712（主工作区历史路径 papers/downloads/2026-05-30/）
> 关联: S004 / literature_notes_amc.md

## 身份
- Title: Adaptive Rate/Power Control With ML-Based Channel Prediction for Optical Satellite Systems
- DOI: 10.1109/TAES.2024.3403809 | Venue: IEEE TAES 60(5):7498-7509, Oct 2024 (Q1) | 正式发表
- Crossref 独立验证：title/authors/venue/vol(60)/issue(5)/pages(7498-7509)/year(2024-10)/publisher(IEEE) 逐字段匹配；content.md H1 Jaccard=1.0
- provenance: 主工作区机构 IEEE Xplore 授权下载（2026-05-30），**非公开 OA**（页脚 "Authorized licensed use limited to: BEIJING INSTITUTE OF TECHNOLOGY"）；迁移后 SHA256 与原始一致（PDF b49f5abf…/MD 27f25473…）
- content.md:546 行

## M-C-A
- M: 固定功率 rate-adapt（AM[6]）+ 理想连续功率 AMP[16]
- C: LEO-sat-to-UAV FSO + **反馈时延数 ms >> 相干时间 <1ms** 导致 CSI 过期 [content.md:33-43,81脚注2,353-367]
- A: AMP 连续功率 per-bit 调整在卫星链不可行 + 过期 CSI 严重恶化自适应传输；失效位置 §I Motivation + Remark 1 + §IV-B [content.md:33-43,229,353-367]
- 方法产出形态: SAMP 算法（Alg.4）+ 解析平均功率/能量效率 + ESN 多步预测器

## AMC 关键语义
- deployable action: YES — TX 运行时联合 **rate（subcarrier K-QAM 星座 K∈{4,8,16,32,64,128}）+ power（EDFA 离散增益列表 Pt=[Pt,1…Pt,N]）**，per-burst/per-channel-state；AMP（理想连续功率）+ SAMP（离散功率，Alg.1-3）[content.md:73,231-273,317]
- CSI: **ESN 多步预测**，从 M=20 历史信道增益预测 N 个未来值 [content.md:133-175,381]
- decision timescale: per-burst Tb（固定等时长 slot <相干时间）[content.md:75,243]
- CSI feedback delay: **反馈时延数 ms，相干时间 <1ms**；仿真设时延=nTb，n 步预测克服 n ms [content.md:81脚注2,357,391]
- turbulence: **lognormal 弱湍流**（UAV<1km 论证，Rytov σ_R²∈{0.0075,0.1020}），**非 GG** [content.md:93,355]
- pointing: **Beckmann 指向误差**（非零均值 misalignment）+ modified-Rayleigh 近似 [content.md:107-115]
- detection: **IM/DD 风格** subcarrier K-QAM；瞬时 BER `BER_j(h)=0.2·exp(−3·Pt,j²·h²/(2·σn²·(K_Aj−1)))` → γ∝h²；**未提及 coherent/homodyne/heterodyne** [content.md:73,297]
- coding/HARQ: **动作中无 FEC/LDPC/HARQ**；HARQ 仅 related work [8] 引用，与 SAMP 解耦 [content.md:31,179-191,475]
- objective: min E[P_t] s.t. (16a) 速率≥τ_req, (16b) Pr_out≤Pr_out,tar, (16c) BER≤BER_tar, (16d) P_t≤P_t,max + max η_EE=E_b/(P_t·T_b) [content.md:179-191,289]
- baselines: AM[6]（固定功率变星座）、理想 AMP[16]（上界）、SAMP（本文）；ML 预测 ESN vs SVM[34]/LSTM[35]/GRU[36] [content.md:321,381]
- oracle: 理想 AMP[16] 作上界；SAMP 接近 AMP；ξ=50°,1Gb/s AM↔AMP/SAMP gap≈0.85dB [content.md:335]
- key numbers: K={4,8,16,32,64,128}；速率 0.6/1/1.2Gb/s；jitter 11.15-20.07μrad（Δ40Mb/J）；ESN 比 delayed-CSI 提升 EE ~110/160Mb/J；ESN 训练时间远<LSTM/GRU，精度相近 [content.md:317,325,329,351,355,383]
- complexity: ESN 仅训练输出层（ridge 线性回归），复杂度低；EDFA 增益切换 μs 级；UAV hover 固定点（Gaussian 抖动）[content.md:43,81脚注3,107,169]

## 与目标重合/缺失
- 重合: **LEO 卫星 FSO 下行 + 过期 CSI + ESN 多步预测 + 运行时联合 rate/power AMC（SAMP）+ 湍流+指向复合信道**
- 缺失: **非 coherent**（subcarrier K-QAM IM/DD 风格，γ∝h²）、**非 GG**（仅弱湍流 lognormal）、**无 coded chain**（动作无 FEC/HARQ）、**非 sat-ground**（sat-to-UAV UAV<1km）、**info uncertainty 局限**（显式排除估计/量化误差，仅建模反馈时延）[content.md:81脚注2,407]
- 直接竞品判定: **YES（结构性差异）** — family-A（delayed-CSI + 预测 + rate/power）直接竞品，但与 coherent/GG/coded-chain 目标在检测/湍流/编码/几何四轴正交

## Nguyen 是否已独占"outdated CSI + ML prediction + joint rate/power"？→ **YES（全部覆盖且耦合）**
但残片清晰可声明（有 evidence，非推测）：
1. **coherent 检测残片** — γ∝h² IM/DD 风格，全文无 coherent/homodyne [content.md:73,297]
2. **GG 强/中湍流残片** — 显式限弱湍流 lognormal（UAV<1km, σ_R²≤0.1020），GG 全程未提 [content.md:93,355]
3. **coded chain 残片** — 动作集仅(K,Pt)，无 FEC/HARQ；HARQ 仅 related work [8] [content.md:31,179-191,475]
4. **sat-ground 几何残片** — sat-to-UAV（UAV<1km），非传统 sat-ground [content.md:71,93]
5. **广义 info uncertainty 残片** — 显式排除估计/量化误差（out-of-scope），仅建模反馈时延 [content.md:81脚注2,407]

## 问题四判据
- problem_truth: ✅ | actionability: ✅ | novelty: ✅ | thesis_fit: ✅（量化数字齐全，但场景需重做信道/检测模型才能直接对比）
- 结论: 全过（但 thesis_fit 的"可量化对标"需先做 coherent/GG 模型替换）
