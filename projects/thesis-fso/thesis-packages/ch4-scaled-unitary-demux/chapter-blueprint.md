# Chapter blueprint — 基于缩放酉约束的短导频偏振信道估计与解复用

> 形态：内部写作蓝图，不是正式论文段落。
> 建议净篇幅：约 14–18 页（随学校模板和与 Ch3/系统模型的复用程度调整）；不以凑页数为目标。

## 4.1 问题与目标场景（1.5–2 页）

### 4.1.1 章间接口与接收信号

- **承重句**：Ch4 接收双偏振短导频与载荷观测，任务是在进入 Ch3 两路 CPR 前估计静态 2×2 偏振混合并完成解复用。
- **公式/图**：`y=Hx+n`；Fig. `figures/ch4-method-flow.svg`。
- **证据**：T068 frozen scene；`confirmation_manifest.json`。
- **写作纪律**：CPR 只作为下游接口，不写成本 confirmation 已启用的损伤。

### 4.1.2 冻结目标验证场景

- **承重句**：本章验证 slice 为 `H=gQ`、`g>0,Q∈U(2)` 的 memoryless static single-tap 模型，并叠加 common scalar Gamma–Gamma 与 equal circular AWGN。
- **表**：场景边界表（DP-(8,8)-16APSK、Np=2/4、14/18 dB、无 PDL/PMD/FIR/时变 SOP/CFO/CPR/LDPC）。
- **证据**：T071 frozen recipe；D052-4；fact matrix B01。
- **引用**：Kikuchi 2011 用于 Jones/PDL/PMD 背景；不能让背景引用扩大验证范围。

### 4.1.3 短导频下的问题定义

- **承重句**：一般 2×2 complex LS 有 8 个实自由度，而 `gU(2)` 只有 5 个；在结构真实且导频短时，未约束 LS 保留 3 个法向噪声自由度并把估计扰动传入逆矩阵。
- **公式**：`dim_R C^{2×2}=8`，`1+dim_R U(2)=5`。
- **证据**：Step4a paper feasibility `:89-112`。
- **边界**：5/8 一阶局部比例是解析预测，不是 BER/NMSE 实测值。

## 4.2 Baseline 与公平比较（1.5–2 页）

### 4.2.1 B0：unconstrained pilot-LS

- **承重句**：B0 在相同 balanced pilots 上计算 `H_LS=Y_pX_p^H(X_pX_p^H)^{-1}`，再直接求逆。
- **代码指针**：`scaled_unitary.py:32-48`、`development.py:140-145`。

### 4.2.2 B1/B2 与 O1

- **承重句**：B1 是 normalized ridge，B2 是 full-SVD singular-value floor；O1 使用真实信道逆，只量化 oracle headroom。
- **重点披露**：confirmation 的 primary comparator 固定为 B2 `tau=1`。
- **代码指针**：`development.py:145-169,185-189`。
- **禁止**：不把 O1 写成 deployable baseline。

### 4.2.3 B2 与 C4 的同方向身份

- **承重句**：`tau=1` 时 B2 与 C4 都采用 `UV^H`，只在公共尺度 `s1` 与 `(s1+s2)/2` 上不同。
- **表/框**：将 B2/C4 两行公式并列；引用 `algorithm-box.md` 的 B2 身份审计。
- **结论上限**：后续 BER 差异只支持公共尺度估计作用，不支持“新偏振旋转”。

## 4.3 缩放酉约束方法推导（2.5–3.5 页）

### 4.3.1 Pilot-LS 与 balanced-pilot 等价性

- **承重句**：先得到 unconstrained `H_LS`；在 exact balanced pilots 下，post-LS projection 与 direct constrained scaled-unitary LS 代数等价。
- **公式**：LS normal equation；balanced Gram `X_pX_p^H=cI`。
- **证据**：Step4a report `:49-81`；correctness C1。
- **禁止**：不把两种表述写成两种 estimator。

### 4.3.2 Frobenius scaled-unitary projection

- **承重句**：对 `H_LS=Udiag(s1,s2)V^H`，nearest scaled-unitary 解为 `Q*=UV^H`、`g*=(s1+s2)/2`。
- **推导顺序**：固定 `Q` 的 trace 形式 → Procrustes/polar 方向 → 对公共尺度求导 → 闭式解。
- **引用**：Schönemann/Higham 经典原子；正式排版前核对 exact bibliographic claim。

### 4.3.3 解复用矩阵与可见诊断

- **承重句**：`W=(g_hat UV^H)^{-1}=VU^H/g_hat`，`z=Wy`；`rho=s1/s2` 只报告 applicability。
- **证据**：`scaled_unitary.py:50-88`。
- **边界**：不定义 `rho` threshold，不把它写成 action。

### 4.3.4 为什么可能改善 BER

- **承重句**：在 strict model 内，投影删除 LS 的法向估计噪声并保留公共尺度与酉混合的切空间分量，从而可能减少逆矩阵对估计误差的传播。
- **证据链**：Step4a local variance argument → confirmation BER；中间不把解析 prediction 冒充实测 NMSE。
- **反事实**：结构失配时投影可能有偏，因此结论不外推 nonunitary truth。

## 4.4 算法流程、有效性与复杂度（1.5–2 页）

### 4.4.1 算法框

- **承重句**：按 `algorithm-box.md` 的 13 步冻结输入、SVD、投影、逆矩阵、输出与 invalid 路径。
- **图**：`figures/ch4-method-flow.svg`。

### 4.4.2 Fail-closed 条件

- **承重句**：exact rank deficiency、zero singular value 和 NaN/Inf 触发 invalid，而不是产生伪 inverse。
- **证据**：`scaled_unitary.py:20-29,32-76`。
- **披露**：near-zero tolerance 与自动 fallback 未冻结。

### 4.4.3 复杂度

- **承重句**：附加成本是固定 2×2 SVD；payload 主成本仍为 2×2 矩阵对 `N` 个双偏振符号的乘法。
- **写法**：报告 `O(N_p)+O(N)` 与固定小矩阵操作；不从 Python runtime 推断硬件时延。

## 4.5 Confirmation 设置与复现合同（1.5–2 页）

### 4.5.1 四格设计

- **承重句**：采用预冻结 `14/18 dB × Np=2/4` 四格，每格 64 个 fresh paired windows；四臂/五臂共用 realization。
- **表**：cell、seed base、B1 eta、B2 tau、windows、payload bits。
- **证据**：`confirmation_manifest.json`；T071。

### 4.5.2 Metric signature

- **承重句**：cell BER 为总错误 bit/总 payload bits；paired CI 对逐 window `BER_C4−BER_B2` 做 PCG64 bootstrap。
- **参数**：seed `2026083004`，2000 resamples。
- **复现**：`python plot_ch4_results.py --check-only`。

### 4.5.3 Truth firewall 与 state lifecycle

- **承重句**：deployable arms 不读取 `H_true` 或 transmitted bits；truth 只用于 O1/scorer；每个 static window 独立重置。
- **代码**：`development.py:125-213`、`run_confirmation.py:31-80`。
- **禁止**：不支持 cross-window tracking claim。

## 4.6 Confirmation 结果（2–3 页）

### 4.6.1 四格 BER 全量展示

- **承重句**：四格 C4 相对 B2 的 BER 相对降幅为 7.37%、2.62%、8.38%、5.06%，individual paired CI upper 均小于 0。
- **图**：`figures/ch4-ber-comparison.svg`；纵轴从 0 起。
- **表**：`data/ch4-confirmation-summary.csv` 的四个 cell rows。
- **解释顺序**：先说明 B2/C4，再用 B0/O1 提供普通 LS 与 oracle 上下文；不选择性删小增益格。

### 4.6.2 Pooled Np=2 结果

- **承重句**：两个 Np=2 cell 合并 128 windows 后，B2/C4=`0.06076145/0.05608821`，相对降幅 7.69%，CI=`[-0.00686385,-0.00282661]`。
- **表**：CSV `pooled_np2` row。
- **纪律**：pooled 是预注册 secondary aggregation，不作为第五个独立 cell。

### 4.6.3 有界解释

- **承重句**：结果支持 strict target slice 中公共尺度估计的有限 BER 改善；不支持新旋转、SOTA 或全损伤普适性。
- **必须回扣**：B2/C4 同 `UV^H`；O1 仍有正 headroom。

## 4.7 适用边界与章末小结（1–1.5 页）

### 4.7.1 已验证与未验证边界

- **表**：已验证（static unitary/common scalar/equal AWGN/短 balanced pilots）与未验证（PDL/PMD/FIR/时变 SOP/CFO/CPR/LDPC）。
- **承重句**：P2 只限制外推，不否定冻结 slice 内证据。

### 4.7.2 章末小结

- **承重句 1**：本章给出从 pilot-LS 到 scaled-unitary projection、闭式解复用及 Ch3 CPR 接口的完整 receiver recipe。
- **承重句 2**：fresh confirmation 相对正确且廉价的 B2 显示有限但一致的 BER 改善。
- **承重句 3**：贡献定位是经典结构估计在特定星地相干短导频场景的有界迁移。
- **禁止**：不新增摘要式“首次/领先”措辞。

## 写作前逐节门

- 任何数字先查 `fact-matrix.md` 与 CSV；无 pointer 不写。
- 任何方法公式先查 `algorithm-box.md` 与实现；不凭记忆补符号。
- 引用候选在正式落 bib 前核对全文/metadata；摘要级来源不得承重 exact formula。
- 图、caption 与正文首次出现顺序中必须解释 B2、C4、O1 和 `rho` 身份。
