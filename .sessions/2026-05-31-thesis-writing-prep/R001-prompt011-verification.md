# [R001] PROMPT-011 实验残酷验证

> 2026-06-02 | 验证 | 完成
> 关联: PROMPT-011-innovation-enhancement.md

## 调研问题

PROMPT-011 创新点增强 4 个实验的结论是否经得起严格审查？用户明确表示"提高警惕"，预期大部分结论可能被推翻。

## 验证方法

逐条手算验证公式、逐行审查代码、检查 TL-13/TL-20/TL-22/TL-25 合规性。

## 发现

### 实验 3: E[1/h] 发散性判据 — 存活（信心:高）

**数学验证**:
- GG(α,β) = Gamma(α,1/α) × Gamma(β,1/β) 独立乘积 ✓
- E[1/X] for X~Gamma(k,θ) = k/(k-1)·1/θ，收敛条件 k>1 ✓
- E[1/h] = α/(α-1)·β/(β-1) ✓
- weak(4,3)=2.00, moderate(2.5,1.8)=3.75, strong(1.5,0.8)=+∞ 全部手算确认 ✓
- MC 采样方法与 GG 定义一致（gamma_dist.rvs 独立采样相乘）✓

**因果链审查**: "E[1/h]发散→VV失效"方向正确但是充分条件非充要条件。VV失效还有块边界相位跳变原因。

**定位**: 纯数学结果无懈可击。因果链标注为"充分条件"即可。

### 实验 2: DPLL 帧级锁相失效 — 存活（信心:中高）

**公式验证**:
- B_L = ω_n·(1+4ζ²)/(8ζ) = 0.5303·ω_n ✓（ζ=√2/2）
- σ_φ² = B_L·T_s/(2γ̄h): 数字域噪声带宽×DD鉴相器噪声方差 ✓
- P_frame = 1-(1-P_block)^500: 独立块假设下正确 ✓

**数值验证** (strong/15dB/50MHz 手算):
- B_L·T_s = 26.5e6 × 4e-10 = 1.06e-2
- 失锁条件 h < 2.72e-4 → GG 强湍流下 P_block 非零 ✓
- P_frame=0.745 vs sim 0.80，7% 偏差在 10 seeds CI 内 ✓

**问题**:
1. 线性化 σ_φ 在 h→0 时过高估计 → P_frame 是**上界**
2. 10 seeds CI 很宽，精确匹配不可靠
3. "失锁不可恢复"假设由仿真确认但非严格证明
4. 独立块假设忽略 DPLL 积分器跨块记忆

**定位**: 解析框架正确，P_frame 应定位为上界估计。

### 实验 1: 16-QAM NMSE 灵敏度 — 存活（信心:中，有 bug 需修）

**代码正确性**:
- Gray 映射: 00→-3, 01→-1, 10→+3, 11→+1，相邻差1bit ✓
- DD-DPLL 鉴相器: angle(rx·exp(-jφ̂)·conj(ŝ)) 标准 ✓
- MMSE 均衡机制: 高SNR下等效缩放 √(h/h_noisy)，QPSK 免疫/QAM 不免疫 ✓

**发现 Bug — TL-13 违规**:
- `generate_qam16_signal` 中 `gg_block()` 和 `doppler_phase()` 使用全局 RNG
- `rng = np.random.default_rng(seed)` 只控制 bits 生成
- Oracle 循环和 NMSE 循环对同一 seed 产生**不同信道实现**
- 影响：退化估计方差放大，但期望值无偏。大效应(+6~12dB)定性结论不受影响。

**发现 — 噪声模型问题**:
- 乘性噪声 h_noisy = |h·(1+σn)| 在 NMSE=0dB 时引入 ~55% 正偏置
- LS 估计实际为加性噪声: h_est = h + σ_LS·n
- 相对比较（QPSK vs QAM）仍然有效（两边同样模型），绝对退化值可能偏高

**发现 — 实际意义有限**:
- NMSE=-20dB 时两种调制退化均 <1dB → LS 精度对两者都够
- 创新点应表述为"调制依赖性分析"，而非"设计准则"

**修复方案**: 改用 `generate_shared_realization` 模式，统一全局种子控制。

### 实验 5: 跨章 BER 验证 — 存活（已保守定位）

偏差 >20%，定位为补充分析不写入论文。无问题。

## 修正清单

1. **实验 1 TL-13 修复**: `generate_qam16_signal` 改用 `np.random.seed()` 控制全局 RNG，确保 oracle/NMSE 共享信道
2. **实验 2 定位修正**: P_frame 标注为"上界估计"
3. **实验 3 定位修正**: 因果链标注为"充分条件"
4. **实验 1 噪声模型说明**: 代码注释标注乘性模型与 LS 加性模型的差异

## 对决策的影响

- D###: 无需新建决策。4 个实验全部存活，修正后可写入论文
- CONCLUSIONS.md 已有 C3-05/C4-10/C4-11 待修正后确认

## 16-QAM 扩展实验（续）

### 16-QAM DPLL ω_n 扫描 + SNR 曲线

新增 `sim_qam16_dpll_sweep.py`，900 次试验（6 ω_n × 3 湍流 × 5 SNR × 10 seeds），683 秒完成。

**核心发现**:
- ω_n=20MHz 在 moderate/strong 15-30dB 全部最优或近最优
- strong 20-30dB 下 16-QAM 与 QPSK 最优 ω_n 完全一致（20MHz）
- 低 SNR (10dB) 16-QAM 偏好更小 ω_n（2-5MHz），噪声容忍度更低
- 强湍流 BER 平台 ~1.2%（30dB 不可消除）

**新增结论**: C4-12 (ω_n 一致性), C4-13 (VV/BPS 不兼容), C4-14 (强湍流 BER 平台)

**三层设计准则**:
1. 选方法: 高阶调制只能用 DD-CPR（VV/BPS 不兼容）
2. 选参数: ω_n=20MHz 对两种调制都近最优 → 固定参数设计可行
3. 看边界: 强湍流 BER 平台 ~1% 是硬限制，16-QAM 在强湍流下不可用

### 16-QAM 多方法扩展（BPS/KF 支持 16-QAM 判决）

**代码改动** (`common.py`):
- 新增 `hard_decision(z, mod='qpsk')` 统一判决函数，支持 QPSK sign() 和 16-QAM 最近点
- `bps_cpr` 新增 `mod` 参数，改用 `hard_decision`
- `kf_unified` / `kf_pilot_recovery` / `kf_oracle_recovery` / `kf_frame_h_recovery` 均新增 `mod` 参数
- 所有 KF 内部判决改为 `hard_decision(rx_rotated, mod=mod)`

**快速测试** (`test_qam16_multimethod.py`): 3 turb × 3 seeds × 20dB, Ns=10000

| 条件 | DD-DPLL | BPS-16QAM | KF-oracle-16QAM |
|------|---------|-----------|-----------------|
| weak 20dB | 3.9~6.9e-3 | 4.3~7.1e-3 | 4.3~7.0e-3 |
| moderate 20dB | 9.3~15.2e-3 | **10.9e-3~25.8%** ⚠ | 9.7~16.8e-3 |
| strong 20dB | 42~48e-3 | **54.9e-3~18.1%** ⚠ | 46.8~63.8e-3 |

**关键发现**:
- **BPS-16QAM 灾难性失效（已修复）**: moderate seed=1 突然 25.8%，strong 有两 seed 超 15%。
  - **根因诊断**: hard_decision 函数正确（5/5 sanity check 通过）。问题在 BPS 距离度量 `|rotated-dec|²` 对非恒包络 16-QAM 失去相位分辨力——metric 最优/次优比仅 1.02，无法可靠区分测试相位。非恒包络（内外点幅度差 9×）使度量被幅度差异主导。
  - **修复**: 两步修复成功：
    1. 归一化度量: `|rotated-dec|²/(|dec|²+ε)` 消除幅度影响
    2. 增大参数: B=64（相位分辨率 5.6°）、Nw=241（更长的平均窗口补偿度量噪声）
  - **修复后结果**: BPS-16QAM 与 DD-DPLL 性能几乎一致（moderate: 1.46e-2 vs 1.52e-2; strong: 4.18e-2 vs 4.20e-2）
  - **代价**: 计算量约 8×（B×2, Nw×4）
- **KF-oracle-16QAM 稳定**: 比 DD-DPLL 略差（~10-30%），无灾难性失败。与 QPSK 下"KF ≤ DPLL"结论一致。
- **DD-DPLL 最鲁棒**: 所有条件下一致表现最好。

**代码改动汇总** (`common.py`):
1. 新增 `hard_decision(z, mod='qpsk')` — 统一 QPSK/16-QAM 判决函数
2. `bps_cpr` 新增 `mod` 参数 + 归一化度量（mod≠'qpsk' 时 `|rot-dec|²/(|dec|²+ε)`）
3. `kf_unified` / `kf_pilot_recovery` / `kf_oracle_recovery` / `kf_frame_h_recovery` 均新增 `mod` 参数

**16-QAM 载波恢复方法对比总结**:
| 方法 | 兼容性 | 性能 | 代价 | 推荐度 |
|------|--------|------|------|--------|
| VV (4次方) | ❌ 不兼容 | — | — | 不可用 |
| BPS | ✓ 需 B≥64,Nw≥241 | ≈ DD-DPLL | 计算 8× | 可用但重 |
| KF-oracle | ✓ 需 16-QAM 判决 | 略差于 DPLL | 需导频/已知h | 无增益 |
| DD-DPLL | ✓ | 基线 | 最低 | **推荐** |

**对创新点(2)的影响**:
- C4-13 需修订: "VV/BPS 不兼容"→"VV 不兼容；BPS 需更高参数代价；KF 无增益"
- 三层设计准则第 1 层从消极排除变为积极排除（比了、排除了替代方案）
- 新增设计维度: 方法选择需考虑计算复杂度（BPS 8× 计算量 vs DD-DPLL）

**待办**:
- 正式实验: 用 B=64/Nw=241 跑 10 seeds × 5 SNR × 3 turb 的 BPS-16QAM 完整扫描
- 考虑是否也跑 KF-pilot-16QAM（需要 oracle FOE 包装）
- CONCLUSIONS.md 新增 BPS-16QAM 结论（C4-13 修订 + C4-15 BPS 参数代价）
