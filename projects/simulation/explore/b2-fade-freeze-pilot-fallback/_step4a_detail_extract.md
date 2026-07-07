# step4a DA pilot vs NDA-ML 实测细节核查（B2-Q2 阶段 0.1 输入）

> 来源: T### 子 agent 核查，主线独立 grep 验证
> 日期: 2026-07-08

> 核查范围: 4 个文件（decisions.md / SC-NDA-ML-MVE-SPEC.md / _time_domain_crlb.py / _recovery.py）
> 辅证: _config.py / params.py / _channel.py（仅用于追溯湍流/线宽/符号率真相源，不在 4 文件清单内但引用了同源常量）
> 纪律: 只提取事实不下判断；每个数字标文件:行号；未找到的写"未找到"

---

## 0. 命名澄清（避免混淆）

任务背景说的"σp² 三档（weak/moderate/strong）"在 step4a 实测里**不是单一标量 σp²**，而是两个正交的物理量：

- **σp²（Wiener PN 每符号方差）**：单值，全场景统一 = `2π·LASER_LW·T_S`。D-007 后统一为 10kHz@2.5GBaud → σp²=2.51e-5。AWGN 场景用它（`_time_domain_crlb.py:134` SIGMA2_P）。
- **fade 场景（weak/moderate/strong）**：用 **Gamma-Gamma 块衰落 α/β** 三档（weak α4/β3, moderate α2.5/β1.8, strong α1.5/β0.8），不是 σp² 三档。生成器 `generate_shared_realization_apsk`（`_channel.py:112`）按 turb_name 取 TURB[α,β]。
- **下文 §3 严格区分这两个量**，不在 σp² 名下塞 fade 三档。

---

## 1. DA pilot 配置（核心）

### pilot spacing
- **spacing = 4**（每 4 符号 1 pilot = 25% overhead）
  - `_time_domain_crlb.py:122` `DA_PILOT_SPACING = 4`
  - SPEC.md L9, L53, L69, L101: "pilot spacing=4"
  - decisions.md D005 L228: "DA ML（pilot sp=4）"

### pilot 类型
- **真符号 pilot（pilot-aided, 非决策错误传播）**
  - SPEC.md L69: "pilot 符号从已知 bits 生成"
  - SPEC.md L53: "DA ML pilot spacing=4 decision-aided"
  - `_time_domain_crlb.py:74` docstring: "DA-ML pilot spacing=4 (25% overhead, 等距 pilot, pilot_sym = 已知 tx 符号, pilot-aided 非决策错误传播 — DA '理想' 形式, 不偏袒 NDA)"
  - `_time_domain_crlb.py:182` `ber_da_awgn` docstring: "逐块 pilot-aided (pilot_sym=已知 tx 符号, 非决策错误传播)"
  - `_time_domain_crlb.py:197` `p_sym = tx_sym[b * N_DFT + pilot_idx_local]`（pilot 符号 = 已知 tx 符号）

### pilot 密度 / 占比
- **25% overhead**（spacing=4 即 1/4 符号是 pilot）
  - SPEC.md L9: "25% pilot overhead"
  - SPEC.md L69: pilot overhead 列 "25%（1.25dB 总能量代价）"
  - `_time_domain_crlb.py:122` 注释: "每 4 符号 1 pilot = 25% overhead"
  - decisions.md D005 L196: "DA 含 1.249dB pilot overhead 总能量代价"

### pilot overhead 1.25dB 怎么算的
- **公式**: `10·log10(spacing / (spacing−1))`，spacing=4 → `10·log10(4/3) = 1.249 dB`
  - `_time_domain_crlb.py:38-39` docstring: "总能量多 10·log10(spacing/(spacing-1))... spacing=4: pilot overhead = 10·log10(4/3) = 1.249 dB"
  - `_time_domain_crlb.py:124` `PILOT_OVERHEAD_DB = 10.0 * np.log10(DA_PILOT_SPACING / (DA_PILOT_SPACING - 1))`
  - **数值验证**: 10·log10(4/3) = 10·log10(1.3333) = 10·0.12494 = **1.2494 dB** ✓（文件四舍五入记 1.249）
  - SPEC.md L74: "DA ML 总能量 SNR = 信息符号 SNR + 1.25dB pilot overhead"
  - decisions.md D004 L142, L155: "DA ML 含 pilot overhead 1.25dB 总能量代价"

### da_ml_recovery 调用时传什么参数
- **调用方式**（AWGN + 湍流同一路径，`ber_da_awgn` = `ber_da_turb` 的别名）:
  - `_time_domain_crlb.py:198-199`:
    ```
    rc, _, _ = da_ml_recovery(rx[s_blk], pilot_idx=pilot_idx_local,
                              pilot_sym=p_sym, mod='m16apsk')
    ```
  - 传入: `rx[s_blk]`（256 符号块）、`pilot_idx=np.arange(0, N_DFT=256, spacing=4)`（即 [0,4,8,...,252]，共 64 pilot/块）、`pilot_sym=p_sym`（已知 tx 符号在 pilot 位置）、`mod='m16apsk'`
- **da_ml_recovery 签名**（`_recovery.py:136`）:
  ```
  def da_ml_recovery(rx, pilot_idx, pilot_sym, mod='m16apsk')
  ```
  返回 `(rx_compensated, phi_est, df_est)` — 3 元组（`_recovery.py:168`）
- **实现核心**（`_recovery.py:154-167`）: pilot 数 ≥2 时用线性回归 `θ = φ + 2π·Δf·n·T_s` 闭式估 (φ, Δf)；单 pilot 退化为仅估 CPE。pilot_idx 是块内局部索引 [0,4,...,252]。
- **每块内 pilot 数**: 256/4 = **64 pilot/块**（`_time_domain_crlb.py:189` pilot_idx_local = arange(0,256,4)）

---

## 2. NDA-ML 配置

### 升幂阶数 M₀
- **M₀ = 8**（(8,8)-16APSK 的 LCM(8,8)=8）
  - `_time_domain_crlb.py:119` `M0 = 8`
  - SPEC.md L9: "升 M₀=8 次幂盲去调制"
  - `_recovery.py:185` docstring: "M₀=8 对 8PSK/(8,8)-16APSK（B11 行 75-77）"

### 块大小 / 全帧积分窗口
- **逐块恢复块大小 N_DFT = 256**（= B11 DFT_SIZE）
  - `_time_domain_crlb.py:118` `N_DFT = 256`
  - `_time_domain_crlb.py:125` `BLOCK_SIZE_RESOLVE = 256`（resolve_m16apsk_blockwise 块大小）
  - `_time_domain_crlb.py:64-65` docstring: "逐块恢复 Nblock=256 (=B11 DFT_SIZE): Wiener PN 累积漂移... 全帧恢复线性 (φ,Δf) 模型失效. B11 原文即按 DFT_SIZE=256 块处理"
- **"全帧积分"实际语义**: 每块 256 符号内 NDA 用**全部 256 符号**升幂 mean-angle 估 CPE（vs DA 仅用 64 pilot）。"全帧"指块内全符号，不是整 102400 符号帧。每点 N_sym = 400 块 × 256 = 102400 符号（`_time_domain_crlb.py:550` N_BLOCKS=400）。

### 是否用 assume_df_zero
- **AWGN 场景: assume_df_zero=True**
  - `_time_domain_crlb.py:172` `nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=True, intra_block_tracking='segmented')`
  - `_time_domain_crlb.py:306` 湍流场景 NDA: `nda_ml_recovery(seg_foe, M0, mod='m16apsk', assume_df_zero=True)`（注意: 湍流场景 fft_foe 先粗估 CFO 补偿后再调，见下）
- **湍流场景: 两阶段** — 先 `fft_foe_m0_omega(seg, M0)` 粗估 CFO 补偿，再 `nda_ml_recovery(assume_df_zero=True)` 估残余 CPE
  - `_time_domain_crlb.py:303-306`:
    ```
    omega_est = fft_foe_m0_omega(seg, M0)
    k = np.arange(N_DFT)
    seg_foe = seg * np.exp(-1j * omega_est * k)
    rc, _, _, _ = nda_ml_recovery(seg_foe, M0, mod='m16apsk', assume_df_zero=True)
    ```
  - 注: `_time_domain_crlb.py` 自带 `fft_foe_m0_omega`（L230-255），不是 `_recovery.py` 的 `fft_foe`（后者是 blind 4 次幂 QPSK 专用，`_recovery.py:37-56`）
- **AWGN 额外: intra_block_tracking='segmented'**（segK8 块内分段跟踪）
  - `_time_domain_crlb.py:161-163` docstring: "D-007 (2026-07-07) 修复: 加 intra_block_tracking='segmented' (segK8 块内跟踪), 与 Formal sc_nda_ml_sim.ber_nda_awgn 对齐"
  - 注: 湍流场景 `ber_nda_turb` **未传** intra_block_tracking（用默认 'none'），即湍流用块常数 mean-angle（`_time_domain_crlb.py:306`）
  - `_recovery.py:197-204` docstring 说明: 'none' 默认整块 mean-angle → 块常数 CPE, 湍流场景用此（sandbox 显示 segK8 在 strong 湍流有害）

### nda_ml_recovery 调用时传什么参数
- **AWGN**（`_time_domain_crlb.py:172-173`）:
  ```
  nda_ml_recovery(seg, M0, mod='m16apsk', assume_df_zero=True,
                  intra_block_tracking='segmented')
  ```
- **湍流**（`_time_domain_crlb.py:306`）:
  ```
  nda_ml_recovery(seg_foe, M0, mod='m16apsk', assume_df_zero=True)
  ```
- **nda_ml_recovery 签名**（`_recovery.py:171-172`）:
  ```
  def nda_ml_recovery(rx, M0, mod='m16apsk', N_fft=None, assume_df_zero=False,
                      intra_block_tracking='none')
  ```
  返回 `(rx_compensated, tau_est, phi_est, df_est)` — **4 元组**（`_recovery.py:237`）
- **注意元组长度差异**: da_ml_recovery 返回 3 元组，nda_ml_recovery 返回 4 元组（多 tau_est）— `_time_domain_crlb.py:198` 用 `rc, _, _ = da_ml_recovery(...)`（3 解包），L172/L306 用 `rc, _, _, _ = nda_ml_recovery(...)`（4 解包）

---

## 3. fade 场景定义

### ⚠️ 区分两类参数

**A. Wiener PN 每符号方差 σp²（单值，全场景统一）**
- **σp² = 2π·LASER_LW·T_S = 2π·10e3·(1/2.5e9) = 2.51e-5**
  - `_time_domain_crlb.py:134` `SIGMA2_P = 2 * np.pi * LASER_LW * T_S_AWGN`
  - `_time_domain_crlb.py:130-131` `LASER_LW = _cfg.system.LASER_LW  # 10e3 Hz` / `T_S_AWGN = 1.0 / _cfg.system.R_SYM  # = 4e-10 s`
  - `_time_domain_crlb.py:133` docstring: "D-007: 从 LASER_LW + T_S 派生 (单载波 10kHz@2.5GBaud → 2.51e-5)"
  - **数值验证**: 2π·10e3·4e-10 = 2π·4e-6 = 2.513e-5 ✓
- D-007 后 σp² 从旧的 1.26e-5（500kHz B11 场景）降到 2.51e-5… **更正**: 决策 D-007 L265 写"σ²p 从 1.26e-4 降到 2.51e-5（相位噪声强度差 5 倍）"，即**旧值 1.26e-4（500kHz@25GBaud: 2π·500e3·4e-11=1.26e-4）→ 新值 2.51e-5（10kHz@2.5GBaud）**，弱 5 倍。
  - **不一致提示**: 上面 D-007 L265 说旧值 1.26e-4，但 params.py:599 注释写 "2π·500kHz·40ps=1.26e-4"（40ps = T_S_B11 = 1/25e9），两个一致。但 `_time_domain_crlb.py:133` 自己的注释只说"2.51e-5"没给旧值，旧值只在 decisions.md 和 params.py 注释里。

**B. Gamma-Gamma 块衰落 α/β（weak/moderate/strong 三档，fade 场景用此非 σp²）**
- **weak: α=4.0, β=3.0**（`params.py:98, 108`）
- **moderate: α=2.5, β=1.8**（`params.py:118, 128`）
- **strong: α=1.5, β=0.8**（`params.py:138, 148`）
- 这些 α/β 通过 `_config.py:15` `TURB = _CFG.get_turb_dict()` 聚合，`generate_shared_realization_apsk`（`_channel.py:112`）按 turb_name 取 `a, b = TURB[turb_name]` 生成 GG 块衰落 h。
- SPEC.md L98: "星地湍流（weak/moderate/strong via generate_shared_realization_apsk）"
- `_time_domain_crlb.py:556` `TURB_LEVELS = ['weak', 'moderate', 'strong']`

### 符号率 BAUD_RATE / R_SYM
- **R_SYM = 2.5e9 sym/s（2.5 GBaud）**
  - `params.py:46` `R_SYM: float = Field(2.5e9, ...)`
  - `_time_domain_crlb.py:131` `T_S_AWGN = 1.0 / _cfg.system.R_SYM  # = 4e-10 s`
  - `_config.py:10` `R_SYM = _CFG.system.R_SYM`
- D-007 后 AWGN 场景也统一到 2.5GBaud（旧 B11 场景是 25GBaud，已废）
  - decisions.md D-007 L247: "AWGN 场景从'B11 复现场景（25GBaud/500kHz）'重定义为'我们方法的单载波 AWGN 验证（2.5GBaud/10kHz）'"

### 线宽 LASER_LW
- **LASER_LW = 10e3 Hz（10 kHz）**
  - `params.py:81` `LASER_LW: float = Field(10e3, ...)`
  - `_time_domain_crlb.py:130` `LASER_LW = _cfg.system.LASER_LW  # 10e3 Hz`
  - `_config.py:13` `LASER_LW = _CFG.system.LASER_LW`
  - source: `params.py:85` "Valjus sat.1553 §4.2 L438：星地 FSO ECL 典型 0.1-1MHz@28GBaud... 单载波 2.5GBaud 配 ECL (1-100kHz) 是典型。10kHz@2.5GBaud → ΔνTs=2.51e-5 落在该区间低端"
  - audit_flag: `AuditFlag.WARNING`（`params.py:88`）
- D-007 后全场景统一 10kHz（旧 AWGN 用 500kHz，已废，见 decisions.md D-007 L247）

### 块结构 N_BLOCKS × block_size
- **N_BLOCKS = 400，N_DFT = 256**（逐块恢复块大小）
  - `_time_domain_crlb.py:550` `N_BLOCKS = 400  # 400×256 = 102400 ≥ 1e5 ✓`
  - 每点 N_sym = 400 × 256 = **102400 符号**（守 FR-21 N≥1e5）
  - SPEC.md L100: "每点 N_sym = 102400 符号（400 块 × 256，守 FR-21 N≥1e5）"
- **信道块大小（h 块内恒定）BLOCK = 100**（与逐块恢复块 256 不同）
  - `params.py:476` `BLOCK: int = Field(100, ...)` description "信道块大小（块内 h 恒定）"
  - `_config.py:16` `BLOCK = _CFG.experiment.BLOCK`
  - `_time_domain_crlb.py:110` import `BLOCK as CH_BLOCK` "信道块大小 (params ExperimentParams.BLOCK=100, h 块内恒定)"
  - `generate_shared_realization_apsk`（`_channel.py:128`）`n_blocks = Ns // BLOCK`（即 256 符号里 h 在每 100 符号变一次，但调用方按 256 一块恢复）
- **per-block h 估计块大小**: 用 CH_BLOCK=100 对齐（`_time_domain_crlb.py:258, 275` `estimate_h_blind_perblock` / `estimate_h_pilot_perblock` 的 block 参数默认 CH_BLOCK）
- **resolve 块大小**: 256（`_time_domain_crlb.py:125` BLOCK_SIZE_RESOLVE=256）

---

## 4. BER 测试条件

### HD-FEC 阈值
- **3.8e-3（7% HD-FEC）**
  - `_time_domain_crlb.py:121` `HDFEC = 3.8e-3  # 7% HD-FEC threshold BER (B11 行 181/191)`
  - SPEC.md L82, L86-88: "公平对照 BER gain @ HD-FEC threshold (BER=3.8e-3)"
  - decisions.md D005 L192: "公平对照 fair gain @ HD-FEC（BER=3.8e-3）"
  - `_recovery.py:121`（`_time_domain_crlb.py` 内）和 `_time_domain_crlb.py:84` docstring "HD-FEC threshold = 3.8e-3 (7%, B11 行 181/191)"

### 每点符号数 N
- **N = 102400 符号**（400 块 × 256）
  - `_time_domain_crlb.py:550` + SPEC.md L100 + `_time_domain_crlb.py:592` meta `'N_per_point': N_BLOCKS * N_DFT`
  - 守 FR-21: N≥1e5（102400 ≥ 1e5 ✓）

### weak 场景 OSNR 工作点
- **γd 扫描点**: weak（含所有湍流场景）`SNR_TURB = [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0]` dB
  - `_time_domain_crlb.py:555` `SNR_TURB = [5.0, 10.0, 15.0, 20.0, 22.0, 24.0, 26.0]`
  - 注: 这里的"SNR"是数据有效 SNR γ_d（per-symbol），不是总能量 SNR
  - `_time_domain_crlb.py:408` `Ns = N_DFT` 注 "逐块 256 符号"
- SPEC.md L99: "总能量 SNR γ_tot（dB）：...湍流 [5,10,15,20,22,24,26]"
- **D004 L157 引用的 "5dB weak"** 即 γ_d = 5 dB（最低扫描点）

### BER 0.38 / 0.29 的精确测试条件
- **来源**: decisions.md D004 L157: "DA pilot 在 deep fade 处 BER 崩溃（5dB weak 0.38 vs NDA 0.29），NDA 全帧积分对单点 fade 鲁棒"
- **精确条件**: γ_d = 5 dB（SNR_TURB 第一个点），weak 湍流（α4/β3），**NDA BER = 0.29，DA BER = 0.38**
  - 即 NDA 用全 256 符号/块升幂 mean-angle 估 CPE → BER 0.29；DA 用 64 pilot/块 pilot-aided ML → BER 0.38
  - 这个数字是**形态 C 论据的核心反证**：在 deep fade（低 SNR + weak 湍流）下，DA 反而比 NDA 差（0.38 > 0.29）
- **未找到**: 这两个具体数字（0.38 / 0.29）在 `_mve_results.json` 里的精确行（4 个指定文件里没读 `_mve_results.json`，该 JSON 不在核查范围）。decisions.md D004 L157 是唯一出处在 4 文件清单内。
- **注意**: D005（L192-203）报的是 HD-FEC 工作点的 fair gain（weak +1.199 dB），不是 5dB 低 SNR 点的绝对 BER。0.38/0.29 是 D004 引用的**低 SNR 工作点**（5dB γ_d）绝对 BER，用于论证"DA 在 deep fade 崩溃"。D005 没复述 0.38/0.29 这两个数。
- **seed**: weak 场景 `SEED_TURB0 = 2000`（`_time_domain_crlb.py:558`），每块 `seed=seed0 + b`（`_time_domain_crlb.py:422`），即 seed 2000..2399 跨 400 块。

---

## 5. DA ML 在 fade 崩溃机制（只提取不下判断）

### D004/D005 给的机制解释
- **D004 L150**（strong 场景结论，非 weak）: "strong HD-FEC 不可达（物理上限，oracle@26dB=1.96e-2 也不可达），但 NDA 全工作区赢 DA（形态 C 鲁棒性，**DA pilot 在 deep fade 崩溃**）"
- **D004 L157**（weak 5dB 具体论据）: "形态 C（湍流）: DA pilot 在 deep fade 处 BER 崩溃（5dB weak 0.38 vs NDA 0.29），**NDA 全帧积分对单点 fade 鲁棒**"
- **D005 L208**（strong 物理上限论证）: "strong HD-FEC 不可达 = 物理上限（oracle 真 h@26dB min BER=1.96e-2 > 3.8e-3，**deep fade 主导**），非估计器缺陷 → 形态 C（NDA 全工作区赢）成立"
- **SPEC.md L12**（假设陈述）: "形态 C（星地湍流）: weak/moderate @ HD-FEC gain ≥ 0.5 dB（DA pilot 受 fade + NDA 全帧积分鲁棒）；strong 全工作区 NDA 赢（**DA pilot 在 deep fade 崩溃**）"

### 机制归因（原文怎么说的）
- **"NDA 全帧积分对单点 fade 鲁棒"** — SPEC.md L12, D004 L157: NDA 用全 N 符号（块内 256 全符号）平均，单点 fade 被 dilute；DA pilot 如果落在一个 fade 块里，64 pilot 都受该块 h 拖累
- **"DA pilot 在 deep fade 崩溃"** — D004 L150, L157, SPEC.md L12: 表述为 DA 的 pilot-based 估计受 fade 退化（pilot 位置 h 低 → pilot SNR 低 → φ̂ 噪声大 → BER 高）

### 有没有提到 pilot 间距 vs fade 相干时间的对比？
- **未找到**。4 个文件里**没有**任何地方对比 pilot spacing（=4 符号 = 1.6 ns @ 2.5GBaud）与 fade 相干时间/相干长度。机制解释停留在"NDA 全帧积分 dilute 单点 fade"层面，未量化 fade 块（BLOCK=100 符号 = 40 ns）与 pilot spacing 的尺度关系。
- 相关注释（非对比，仅尺度）: `_time_domain_crlb.py:64-65` 提到 Wiener PN 在 256 符号块内累积漂移（"σ²_φ=2π·CLW·T_S·N_block≈0.032 rad/块"），但这是 PN 不是 fade。
- **per-block h 估计尺度**: DA pilot 在每 100 符号（CH_BLOCK）内用 pilot 估 h（`_time_domain_crlb.py:275-290`），NDA 盲估每 100 符号 h（`_time_domain_crlb.py:258-272`）。fade 块 = 100 符号，pilot spacing = 4 符号（每 fade 块约 25 pilot）— 这个尺度关系代码里有但**无文字讨论其与"DA 崩溃"的因果**。

---

## 6. pilot overhead 1.25dB 公平对照框架

### D004 怎么定义"公平对照"
- **D004 L142**（决策正文）: "公平对照框架确立: DA ML 含 pilot overhead 1.25dB 总能量代价，NDA-ML 纯数据，比较在相同总功率/相同信息率下"
- **D004 L155**（理由）: "公平对照物理依据: DA ML pilot overhead 1.25dB 是真实能量代价（相同总功率下 DA 信息符号有效 SNR 低 1.25dB）"
- **D004 L165**（排除 naive 对照）: "用 naive 对照（不计 pilot overhead）: 否决。naive gain AWGN -0.55dB 误导（DA 总能量没算 pilot 代价），公平对照才反映真实系统对比"
- **SPEC.md L73-77**（公平对照框架定义）:
  - "DA ML 总能量 SNR = 信息符号 SNR + 1.25dB pilot overhead"
  - "NDA-ML 总能量 SNR = 信息符号 SNR（纯数据）"
  - "BER 曲线按总能量 SNR 比较（相同总功率/相同信息率）"

### DA 含 1.25dB pilot overhead 总能量代价具体怎么实现（代码层面）
- **核心**: BER 曲线按数据有效 SNR γ_d 跑（两方案同信道同符号率公平），但报告 gain 时 DA 的 γ_d **加 PILOT_OVERHEAD_DB（1.249 dB）** 得等效总能量 γ_tot
  - `_time_domain_crlb.py:38-44` docstring: "BER 曲线仍按 γ_d (符号率 SNR) 跑 (两方案同信道同符号率公平); gain@HD-FEC 报告时 DA-ML 的 γ_d 加 1.249 dB = 等效总能量"
- **代码实现 1**: 每点记录两个总能量字段
  - `_time_domain_crlb.py:389-391`（AWGN）:
    ```
    'snr_db_total_nda': float(snr),          # NDA 总能量 = γ_d（0% overhead）
    'snr_db_total_da': float(snr) + PILOT_OVERHEAD_DB,  # DA 总能量 = γ_d + 1.249
    ```
  - `_time_domain_crlb.py:451-452`（湍流）同上
- **代码实现 2**: gain 计算
  - `_time_domain_crlb.py:486-489`:
    ```
    # 公平 gain = (DA 总能量) - (NDA 总能量) = (s_da_d + overhead) - s_nda_d
    gain_hdfec = (s_da_d + PILOT_OVERHEAD_DB) - s_nda_d
    ```
  - 即 gain@HD-FEC = DA 达到 HD-FEC 所需总能量 − NDA 达到 HD-FEC 所需总能量；正 = NDA 赢
- **代码实现 3**: 逐点公平 gain（高 SNR 主判据）
  - `_time_domain_crlb.py:505-516`: 对每个 γ_tot，NDA 跑 γ_d=γ_tot，DA 要跑 γ_d=γ_tot−1.249 才同总能量；fair_gain = (DA 达 NDA BER 所需 γ_d + 1.249) − γ_tot
- **PILOT_OVERHEAD_DB 常量**: `_time_domain_crlb.py:124` = 10·log10(4/3) = 1.2494 dB

### NDA 纯数据符号怎么处理
- **0% overhead，全 N 符号都是数据**
  - SPEC.md L70: NDA-ML pilot overhead 列 "0%"
  - `_time_domain_crlb.py:75-76` docstring: "公平对照: DA 数据 BER 仅在 data 符号位置算 (pilot 不算)"
  - BER 计算: NDA 全 256 符号都算 BER（`_time_domain_crlb.py:176-177` resolve + demod 全块）；DA 只在 data 位置算（pilot 位置 mask 掉，`_time_domain_crlb.py:188-213`）
  - 即 DA 的 BER 分母 = (256−64)×4 = 768 bit/块；NDA 的 BER 分母 = 256×4 = 1024 bit/块
- **NDA 盲 h 估计**（无 pilot，公平非 oracle）: `estimate_h_blind_perblock` ĥ=mean(|rx|²)−1/(2γ)（`_time_domain_crlb.py:258-272`），per-block（CH_BLOCK=100）块内平均
- **DA pilot h 估计**: `estimate_h_pilot_perblock` ĥ=mean(|r(p)/s(p)|²)（`_time_domain_crlb.py:275-290`），pilot 位置平均

### D005 验收引用（公平对照落实核查）
- **D005 L215**: "per-block h 行 250-282 / **公平对照 PILOT_OVERHEAD_DB 行 124** / 两阶段 FOE 行 285-297 / resolve_m16apsk_blockwise 行 167/300 / generate_shared_realization_apsk 行 411 / N_BLOCKS=400×256=102400"
- **D005 L196**: "主指标全过 SPEC §5 Go 门（公平对照 BER gain @ HD-FEC，DA 含 1.249dB pilot overhead 总能量代价）"

---

## 附录: 不一致 / 注意事项记录

1. **BER 0.38/0.29 出处单一**: 仅 decisions.md D004 L157 一处引用，4 文件清单内无 `_mve_results.json` 原始数据交叉验证。0.38/0.29 是 5dB γ_d weak 绝对 BER，D005 报的 weak fair gain +1.199 dB 是 HD-FEC 工作点（更高 SNR），两者不冲突（不同 SNR 点）。

2. **σp² 旧值叙述**: decisions.md D-007 L265 说"旧 σ²p=1.26e-4（500kHz@25GBaud）→ 新 2.51e-5（10kHz@2.5GBaud）"，弱 5 倍。但 `_time_domain_crlb.py:133` 自身注释只说新值 2.51e-5，未提旧值；旧值仅在 decisions.md / params.py:599 注释里。**数值核对**: 2π·500e3·(1/25e9)=2π·500e3·4e-11=2π·2e-5=1.257e-4 ≈ 1.26e-4 ✓。

3. **da_ml_recovery vs nda_ml_recovery 元组长度**: da_ml 返回 3 元组 (rx_comp, phi_est, df_est)（`_recovery.py:168`），nda_ml 返回 4 元组 (rx_comp, tau_est, phi_est, df_est)（`_recovery.py:237`）。`_time_domain_crlb.py` 调用处解包长度匹配（L198 `rc, _, _` vs L172/L306 `rc, _, _, _`），无 bug。

4. **湍流场景 NDA 不用 segmented**: AWGN 场景 NDA 用 intra_block_tracking='segmented'（segK8），湍流场景用默认 'none'（块常数 mean-angle）。`_recovery.py:199-200` docstring 明示"湍流场景用此 (sandbox 显示 segK8 在 strong 湍流有害)"。这是 AWGN vs 湍流的算法路径差异（非 bug，设计选择）。

5. **"deep fade 崩溃"机制无量化对比**: 4 文件内无 pilot spacing（4 符号）vs fade 相干时间/相干长度的对比讨论。机制停留在"NDA 全帧积分 dilute 单点 fade"定性层面。fade 块 = CH_BLOCK=100 符号，每 fade 块约 25 个 pilot，这个尺度关系代码层面存在（pilot_idx 步长 4 + h 块 100）但无文字归因到"DA 崩溃"。

6. **task 提到的 fft_foe (L37) / psa_foe_recovery (L435) 签名核查**:
   - `_recovery.py:37` `def fft_foe(rx, N_fft=1024, nfft_zp=8192)` — blind 4 次幂 FOE（QPSK 专用，M=4 固定，L40 `r4 = seg**4`），返回 `2π·f_est_norm`（标量，L56）。**注意**: step4a MVE **不用这个** fft_foe（它是 QPSK 专用 M=4），而是用 `_time_domain_crlb.py:230` 自带的 `fft_foe_m0_omega(rx, M0_power)`（升 M₀=8 次幂版 FOE，返回 omega rad/sample）。
   - `_recovery.py:435` `def psa_foe_recovery(rx, pilot_idx, pilot_sym)` — Pilot-Aided FOE（B7 baseline），返回 (rx_comp, df_est) 2 元组。**step4a MVE 未调用 psa_foe_recovery**（grep `_time_domain_crlb.py` 无 psa_foe 引用）；DA 路径用 `da_ml_recovery`（它内部已含 Δf 线性回归，`_recovery.py:154-161`），不需单独 psa_foe。
