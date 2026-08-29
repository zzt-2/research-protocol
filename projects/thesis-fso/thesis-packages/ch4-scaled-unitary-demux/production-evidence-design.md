# Ch4 production-evidence 设计：把有限 confirmation 扩成完整方法章

> 日期：2026-08-30
> 状态：独立 preflight PASS，按阶段门执行
> authority：D061 / V036 / CP023
> 北极星：把 Ch4 从“两个 SNR 点上的有限改善”建设为一章从问题、方法、机制、性能、复杂度到边界均可闭环的硕士论文方法章。

## 1. 先给结论

Ch4 当前的方法身份是成立的：在星地相干光双偏振接收链中，利用短导频对 `2×2` 偏振混合信道做 pilot-LS，再投影到 `gU(2)` 结构并闭式解复用。它不是“新偏振旋转”，承重差异是从 noisy singular values 中估计公共尺度 `g`，再与酉方向共同构成接收机可执行动作。

但旧 confirmation 还不能直接扩写为完整结果章。正式生产前必须解决三个测量风险：

1. 公共 16APSK demapper 当前并非全 16 点全局最近邻，可能把 B2/C4 的纯尺度差异放大为 BER 差异；
2. 不同 `SNR×Np` cell 使用不同随机总体，且单一 RNG 流会让改变 `Np` 同时改变 payload noise，削弱横向曲线的配对解释；
3. B2 `tau=1` 与 C4 使用同一 `UV^H`，必须加入同信息预算的廉价标量归一化对照，辨清收益来自结构化公共尺度估计，还是任何标量校准都能吸收。

因此，生产路线的第一目标不是“让数字更高”，而是确认修正后的 BER 信号真实存在；若存在，再用完整工作区、机制量、导频效率、结构失配和复杂度把故事讲圆。

## 2. 论文故事线

### 2.1 章间接口

- Ch4 输入：双偏振短导频 `X_p,Y_p` 与双偏振 payload 观测 `Y`。
- Ch4 动作：估计 static single-tap `2×2` 偏振信道，构造解复用矩阵 `W`，输出两路复符号序列。
- Ch4 输出：两路已解复用但尚未做载波相位恢复的符号，送入 Ch3 的 per-tributary CPR。
- 统一调制：DP-(8,8)-16APSK，半径比 `2.57`，Gray mapping，`E_s=1`。
- 统一横轴：每偏振、衰落前、data-symbol `E_s/N_0`，不得写成 `E_b/N_0`、OSNR 或双偏振总功率 SNR。

### 2.2 目标问题

在短导频下，unconstrained complex pilot-LS 估计 `H` 的 8 个实自由度；若目标 slice 满足 `H=gQ, g>0, Q∈U(2)`，真实模型只有 5 个实自由度。多余的法向噪声分量会进入矩阵求逆并污染偏振解复用。

本章问题不是“有没有人做过 SVD”，而是：在给定星地相干光短导频接收场景中，能否把已知 `gU(2)` 结构转化为完整、可部署、同开销的 receiver action，并在正确 demapper 下相对经典 pilot-LS 与强简单邻居取得稳定 BER 收益。

### 2.3 方法身份

令

`H_LS = Y_p X_p^H (X_p X_p^H)^{-1} = U diag(s_1,s_2)V^H`。

提出的 scaled-unitary receiver 使用

`Q_hat=UV^H, g_hat=(s_1+s_2)/2, H_hat_SU=g_hat Q_hat, W_SU=V U^H/g_hat`。

方法贡献定位为：经典结构投影在特定星地双偏振短导频接收链中的有界迁移与完整 receiver recipe。不得声称新 SVD、新 Procrustes 理论、首次或 SOTA。

### 2.4 需要回答的五个结果问题

1. **工作区性能**：完整 BER–SNR 曲线上是否稳定优于可部署 baseline？
2. **导频效率**：`Np=2/4/8/16` 时达到工程 BER 参考所需 SNR 如何变化？
3. **作用机制**：channel NMSE、inverse residual 与 BER 的方向是否一致？
4. **适用边界**：不同 turbulence strength 与逐渐偏离 `gU(2)` 的结构失配下，收益何时衰减或反转？
5. **工程代价**：相对 LS/regularized-SVD/廉价标量校准，多出的固定 `2×2` 运算和 payload 主复杂度是什么？

## 3. 正确性修复与历史边界

### 3.1 Demapper 合同

公共 `m16apsk_demod` 的唯一合法定义是：对归一化 `(8,8)-16APSK` 的全部 16 个星座点计算欧氏距离并返回全局最近标签。现有“半径超过中点就强制外环”的捷径违反该合同。

修复以测试先行：

- 16 个星座点逐点 round trip；
- 已知反例 `r=0.9155`、沿第一个 inner-point ray，必须选择 inner label `0000`；
- 固定随机云与 brute-force 16 点 argmin 完全一致；
- 平距点不作为承重样本，避免 tie-breaking 偶然性。

### 3.2 历史资产不改写

- `confirmation_manifest/raw/aggregate/receipt` 与旧图表保持原样，其 hash 和历史裁决不重写。
- 新 demapper 只影响新建 demapper replay、production-seam bridge 与后续 production。
- 旧 confirmation 在后续文档中标为“pre-correction historical evidence”，不得与新 raw 合并统计。
- Ch3 已接受资产若曾调用相同 demapper，记为单独的跨章证据债务；本轮不顺手重跑 Ch3，也不让该债务阻塞 Ch4 修正锚点。

## 4. 新生产 seam

### 4.1 随机总体与严格配对

新生成器使用 `SeedSequence` 派生独立子流：

- payload bits；
- Haar unitary `Q`；
- Gamma–Gamma irradiance/gain；
- 最大长度 pilot base noise；
- payload base noise；
- mismatch left/right unitary factors（只用于 mismatch slice，并在 `delta=0` 合成为同一 unitary truth）。

同一 `scenario×latent_window_id` 共享 `bits/Q/g/payload_base_noise`；同一 `Np` 使用 pilot base noise 的冻结前缀；改变 SNR 只按解析系数缩放同一标准噪声。这样：

- 方法间严格 paired；
- SNR 曲线是 common-random-number paired；
- Np sweep 不因 RNG 消耗顺序而更换 payload population；
- bootstrap 以 latent window 为重采样单位，不把相关 cell 当独立样本。

每个 raw window 记录各 latent component hash 与 observation hash。

### 4.2 Balanced pilots

- `Np=2`：冻结的两列正交 pilot；
- `Np=4`：冻结的 `2×4` balanced block；
- `Np=8/16`：重复完整 `Np=4` block，保证 `X_pX_p^H=N_p I`；
- 测试逐个验证 Gram、符号能量、shape 与 prefix/repetition 规则。

### 4.3 可部署对照梯队

主结果至少包含：

- B0：plain unconstrained pilot-LS；
- B2：regularized singular-value-floor inverse，参数由独立 development split 冻结；
- B3_PSC：B2 后接同导频信息预算的非负实标量校准；
- C4：mean-singular scaled-unitary projection；
- O1：true-channel inverse oracle，只作 headroom，不算可部署 baseline。

B3_PSC 的标量只由 `X_p,Y_p` 和 B2 的 pilot 输出估计，不读取 `H_true`、payload bits 或 payload decision truth。其作用是回答“任何廉价尺度修正是否都能吸收 C4”。B1 可以保留在 appendix/data，不占主图视觉预算。

具体令 `Z_p=W_B2Y_p`，在非负实数上最小化 `||aZ_p-X_p||_F^2`，得到

`a_hat=max(0, Re<tr(Z_p^H X_p)>/||Z_p||_F^2)`，并输出 `a_hat W_B2Y`。

分母非正/非有限或输出非有限时直接 invalid；分子非正时按约束最优解取零，不得读取 payload decision 进行补救。论文图例写成 `B2+PSC`（pilot scalar calibration），内部 arm ID 冻结为 `B3_PSC`，避免把描述性 baseline 混写成另一种结构投影。

### 4.4 B2 公平调参

在与 production latent IDs 完全不重叠的 development split 上，对 `tau∈{0,0.25,0.5,0.75,1}` 做有限选择。冻结规则：每个 turbulence scene 与 Np 恰好选择一个 `tau`，不得切换为全局 tau，不得按 SNR 单点选择，不得看 production 结果后改参数。目标函数和 tie rule 以执行计划 Task 5 为唯一实现合同。

## 5. 分阶段证据生产

### Stage A1：historical-observation correction replay

先不建立新 RNG seam。严格沿用旧 `14/18 dB × Np=2/4` cells、旧 seed arithmetic、旧 `make_realization` 和旧 receiver actions，重新生成 4×64 windows；逐窗要求 `realization_hash` 与 `observation_hash` 和历史 `confirmation_raw.json` 完全一致，只允许 demapper/scoring implementation hash 改变。结果写入独立 `demapper_replay_*`，不覆盖旧 raw。

通过条件：

- pooled `Np=2` 的 paired `BER_C4-B2` 95% CI upper `<0`；
- `Np=4` 两格的 `D=BER_C4-BER_B2` paired CI lower 均 `<=0`，即不存在显著回归；
- 256/256 observation hashes 与历史 raw 一致；
- raw schema、truth firewall 与独立 reducer 全部通过。

停机条件：

- 修正 demapper 后 C4 对 B2 的承重信号消失或反向：停止全量生产，Ch4 回到“方法身份可讲、性能章未成立”的状态；
- 发现 truth leakage、unpaired populations 或无法复算：只修测量链，不扩场景掩盖。

### Stage A2：production-seam bridge

只有 A1 通过后才建立新 RNG seam、B3_PSC 和正式 raw schema。仍运行 `14/18 dB × Np=2/4` 四格，每格 64 个新 latent windows，以验证信号能从历史随机总体迁移到正式 production 总体。

`PRODUCTION_SEAM_BRIDGE_PASS` 同时要求：

- pooled `Np=2` 上 C4 相对 B2 与 B3_PSC 的 paired CI upper 均 `<0`；
- 两个 `Np=4` cell 对 B2/B3_PSC 的 `D=BER_C4-BER_comparator` paired CI lower 均 `<=0`，即不存在显著回归；
- RNG substream、latent pairing、truth firewall、raw-only reducer 与独立复算全部 PASS。

若 C4 对 B3_PSC 不能满足上述条件，terminal=`CHEAP_COMPARATOR_NOT_CLEARED`，停止完整 production 并将 Ch4 返回 claim/structure discussion；不能以“只是 CI 跨零”自行放行。

### Stage B：工程烟测与冻结

仅在 Stage A 通过后执行。用少量 latent windows 检查：

- Ch3 对齐的 SNR 主网格 `5,7,...,35 dB` 是否覆盖 BER 工作区；
- authoritative weak/moderate/strong Gamma–Gamma 参数是否可运行；
- B2 development tuning 是否稳定；
- `Np=8/16`、mismatch 参数化、checkpoint/resume、聚合器与作图器是否端到端贯通。

烟测数字不得进入论文。烟测结束后冻结 manifest、commit、参数、cells、seeds、方法列表和 crossing 规则，再进入 production。

### Stage C：正式 production

不做全笛卡尔积，采用“一个主工作区 + 三个解释切片”：

1. **主 BER 曲线**：moderate turbulence，`Np=2/4`，`SNR=5:2:35 dB`，B0/B2/B3_PSC/C4/O1；
2. **导频 sweep**：moderate，`Np=2/4/8/16`，从同一主网格提取 threshold crossing/required SNR；
3. **turbulence summary**：weak/moderate/strong 固定 `Np=2`，以 required-SNR 做紧凑摘要；moderate 的 Np4/8/16 只服务 pilot sweep；
4. **结构失配**：moderate、`Np=2`、固定 `25 dB`，以维度无关的 singular-value ratio / nonunitarity 连续控制，报告 boundary，不冒充已有 PDL model。

结构失配只采用一个冻结的无量纲构造与 levels：`delta∈{0,0.05,0.10,0.20,0.30,0.40}`。

`H_delta=g U D_delta V^H`，其中 `D_delta=diag(1+delta,1-delta)/sqrt(1+delta^2)`、`0<=delta<1`。因此 `(s_1^2+s_2^2)/2=g^2` 保持不变，true singular-value ratio 为 `(1+delta)/(1-delta)`；同一 latent window 的 `U,V,g` 跨 `delta` 共用。它只表示离开 scaled-unitary manifold 的数学 sensitivity，不映射为 PDL dB。

全部 formal-production cells 一次固定为 128 latent windows；不设置结果驱动的 64→128 扩样规则。A1/A2 的 64 windows 只属于前置门，不进入正式论文数据。

SNR 延伸规则：若 35 dB 尚未为 O1 或关键可部署方法形成目标 BER bracket，按 `37,39,41 dB` 顺序整体延伸相应 slice，达到 bracket 即停；超过 41 dB 仍未到则记为 `unreached`，不得外推画交点。

## 6. 指标与统计合同

- 主指标：pooled bit-count BER，即 `Σ bit_errors / Σ payload_bits`。
- uncertainty：以 latent window 为单位的 paired bootstrap 95% CI，formal resamples=`5000`；同一命名比较使用冻结 seed。
- threshold：`3.8×10^-3` 只称为本项目独立采用的 7% HD-FEC engineering reference；它不是 Ch3 的既有门限。authority 冻结为本地 `papers/_read_notes/10.1109_jphot.2022.3161795.md` 的直接应用记录、`projects/simulation/simulator/_b11_params.py:64` 与 `.sessions/2026-07-09-thesis-writing/R012-params-narrative.md:59`，不得引用 `B11Params.HD_FEC_THRESHOLD=7e-2` 的历史错误值。
- cell BER 的 headline 始终为原始 bit counts。仅为 log 插值，对所有 cell 使用 Jeffreys 平滑 `BER_J=(errors+0.5)/(bits+1)`；零误码点在 log 图上画于该值并加 downward-limit 标记，不冒充非零实测 BER。
- required SNR：只在相邻网格点跨越 threshold 时对 `log10(BER_J)`–SNR 线性插值；无 bracket 写 `unreached`。
- required-SNR gain 的 uncertainty 必须按共同 latent ID 联合重采样整条 SNR 曲线，并在每个 bootstrap replicate 内分别重算 crossing 与差值。若任一 arm 不可达，gain=`unreached`；若少于 95% replicates 同时形成 bracket，不报告 CI，terminal=`CROSSING_UNSTABLE`。
- SNR 延伸触发时，相应 `scene×Np` slice 的全部 arms 使用相同 latent IDs 一起运行，不允许只延伸 C4 或 baseline。
- mechanism：channel NMSE、inverse residual、singular values、`rho=s1/s2`；`rho` 只作诊断，不成为动作或事后 gate。
- scene summary：必须预先选择 required-SNR / log-BER AUC / representative BER 中的主摘要，禁止看结果后换成更漂亮的指标。
- runtime：Python wall-clock 只作复现诊断；论文复杂度以运算结构和 MAC/小矩阵分解计数为主，不宣称 FPGA latency。

## 7. 最终章节证据包

### 图

1. Fig. 4-1：接收机 IAO 流程 + `H_LS→SVD→gU(2)` singular-value 投影几何；
2. Fig. 4-2：完整 BER–SNR 曲线（moderate，Np=2/4）；
3. Fig. 4-3：达到工程 BER 参考所需 SNR 随 Np 的变化；
4. Fig. 4-4：NMSE 与 inverse residual 的机制对应；
5. Fig. 4-5：turbulence robustness 与 structure-mismatch boundary 的紧凑双面板。

### 表

1. 系统/信道/调制/随机性/统计配置表；
2. B0/B2/B3_PSC/C4/O1 的输入、动作、参数、truth access 和公平性表；
3. 复杂度与工程代价表；必要时附 required-SNR 数值表。

### 章节闭环

`星地双偏振短导频问题` → `结构自由度诊断` → `scaled-unitary 接收动作` → `同开销强邻居与廉价替代` → `全工作区 BER` → `导频效率` → `NMSE/residual 机制` → `turbulence 与 mismatch 边界` → `复杂度` → `与 Ch3 CPR 的接口`。

## 8. 明确不做

- 不为了提高数字更改 demapper、SNR 定义、噪声功率或删除不利 cell；
- 不引入 PDL/PMD/FIR/CFO/CPR/LDPC 来“制造”C4 优势；
- 不把 smoke/tuning split 数字写进论文；
- 不用强邻居限制之外的期刊级 novelty gate 否决硕士方法章；
- 不隐藏已知廉价替代的吸收结果；
- 不在 Ch4 未依次通过 A1 demapper replay 与 A2 production-seam bridge 前继续 Ch5、补文献或开新候选。

## 9. 成功等级与停机解释

- **A 级**：相对 B2/B3_PSC 有稳定 BER/required-SNR 改善，机制量同向，边界清楚；可作为有力 Ch4。
- **B 级**：required-SNR 改善约 `0.2–0.3 dB` 或 BER 收益有限但跨工作区稳定，且 NMSE/residual 与导频效率证据完整；足以作为专业硕士方法章。
- **C 级**：约 `0.1–0.2 dB`、只在短导频区稳定，但机制和复杂度故事完整；可写但必须降低标题和贡献措辞。
- **停止**：低于 `0.1 dB` 且只在孤立点出现，或未通过 B3_PSC 前置门，或修正 demapper 后反向；不再用额外损伤、参数或选择性统计“救图”。

structure-mismatch boundary 的机器定义：在依次增大的 tested delta 上，找到 C4 相对 B0 的 paired `BER_C4-BER_B0` 95% CI lower 首次 `>0` 的点；boundary 报告为该点与前一个 tested delta 之间的 bracket。若到 `0.40` 仍未显著回归，报告 `boundary>0.40`；若 `0.05` 即回归，报告 `boundary<0.05`；若显著性非单调，不强行给单一 boundary，只报告完整 tested pattern。
