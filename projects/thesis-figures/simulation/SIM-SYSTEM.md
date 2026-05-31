# 仿真体系文档 (SIM-SYSTEM.md)

> ⚠️ **已废弃** — 合并入 `projects/simulation/SPEC.md`。本文件不再更新。

---

## 1. 信号模型（不可修改，已锁定）

### 1.1 物理模型

相干检测 QPSK 星地激光通信系统。

**接收信号**：
```
r[k] = √h[k] · s[k] · exp(jφ[k]) + n[k]
```

- `h[k]`：归一化辐照度（Gamma-Gamma 分布），**不是** 信道幅度系数
- `s[k]`：QPSK 符号，位于 (±1±j)/√2（π/4 旋转星座）
- `φ[k]`：载波相位（多普勒+激光相位噪声+湍流相位）
- `n[k]`：复高斯白噪声，E[|n|²] = 1

**瞬时 SNR**：`γ[k] = γ̄ · h[k]`（线性关系，不是 h²）

### 1.2 文献依据

- γ=γ̄·h 约定：Petkovic 2023, Hu 2025, Colavolpe（相干 FSO 主流）
- γ=γ̄·h² 是 IM/DD 约定，**不适用于本论文**
- 信号模型错误会导致全盘皆错（教训 TL-01）

### 1.3 系统参数

| 参数 | 符号 | 值 | 来源 |
|------|------|-----|------|
| 符号率 | R_SYM | 2.5 Gsps | Zhao 2025 |
| 符号周期 | T_S | 400 ps | 1/R_SYM |
| 载波频率 | f_c | 1550 nm (1.95e14 Hz) | C波段 |
| 激光线宽 | Δν | 10 kHz | 典型值 |
| 多普勒率 | f_dot | 150 MHz/s | LEO 500km |
| 残余频偏 | f_res | 1 MHz | 预补偿后 |
| 信道块大小 | BLOCK | 100 符号 | 相干时间~2-10ms >> 100·T_S |
| 导频开销 | — | 5% (5/100) | 默认值 |

### 1.4 湍流参数

| 等级 | α | β | 物理场景 |
|------|---|---|---------|
| 弱 weak | 4.0 | 3.0 | 夜间/高仰角 |
| 中 moderate | 2.5 | 1.8 | 白天/中仰角 |
| 强 strong | 1.5 | 0.8 | 低仰角/恶劣天气 |

### 1.5 QPSK 星座（关键：影响 VV 的 π/4 偏移）

QPSK 符号位于：**(±1 ± 1j) / √2**，即 π/4 + kπ/2 (k=0,1,2,3)

**这意味着**：
- 4 次方操作 s⁴ = |s|⁴ · exp(j·4·(π/4+kπ/2)) = exp(jπ) · exp(j2kπ) = -1（恒定）
- VV 的 phase estimate = angle(avg)/4 = 真实相位 + π/4 + kπ/2
- **π/4 恒定偏移是 VV 的已知特性，不是 bug**
- 但评估方法必须处理这个偏移（见 §3）

---

## 2. 载波同步方法实现

### 2.1 FOE（FFT 频偏估计）

- 4 次方去调制 → FFT → 峰值检测 → 二次插值
- 精度：~kHz 级（N_fft=1024, zero-padding 8192）
- **残余频偏**：FOE 估计不完美，残余约几十到百 kHz

### 2.2 VV（Viterbi-Viterbi）

- 4 次方去调制 → 滑动窗平均 → angle/4 提取相位
- **已知特性**：π/4 恒定偏移 + π/2 模糊
- **实现文件**：`sim_ch4_systematic_analysis.py` 行 133
- **公式**：`pe = np.unwrap(np.angle(avg)) / M`
- **湍流下表现**：滑动窗平均在深衰落中引入滞后和噪声放大
- **强湍流失败率**：~40%（Track A 100 种子验证）

### 2.3 BPS（Blind Phase Search）

- B 个候选相位 → 最小距离选择 → 滑动窗平均
- **无 π/4 偏移问题**：公式 `np.unwrap(4 * pe_raw) / 4` 正确处理
- **实现文件**：`sim_ch4_systematic_analysis.py` 行 150
- **湍流下表现**：强湍流失败率 ~45%（比 VV 更高）
- **AWGN 表现**：唯一在无噪声信号上实现 BER=0 的方法

### 2.4 DPLL（数字锁相环）

- 4 次方鉴相器 → 二阶环路滤波 → VCO
- **已知特性**：同 VV，有 π/4 恒定偏移
- **实现文件**：`sim_ch4_systematic_analysis.py` 行 177
- **环路参数**：ω_n=8MHz（默认），ζ=√2/2
- **反馈环路优势**：平滑深衰落噪声，不会灾难性失败

### 2.5 KF（Kalman 滤波）

- 2 状态 (φ, Δf)，状态转移 F=[[1,T_s],[0,1]]
- 判决导引观测 + 导频辅助 h 估计
- **无 π/4 偏移**：观测模型是 angle(r·conj(s_hat))，不做 4 次方
- **实现文件**：`sim_ch4_kf_pilot_h.py` 行 181
- **Q 矩阵**：分湍流参数化，Q[1,1] 是哑参数（B1 测试确认）
- **R 矩阵**：1/(2γ̄h)，但 B2 测试显示 h 估计对 R 无显著价值

---

## 3. 评估方法（关键，当前不一致）

### 3.1 BER 计算方法

| 方法 | 代码 | 机制 | 公平性 |
|------|------|------|--------|
| `ber_count` | 直接解调 | sign(real)>0, sign(imag)>0 | ✅ 公平 |
| `resolve_qpsk` | oracle旋转优化 | 尝试8个旋转(0~2π,π/4步)，选BER最低 | ❌ 使用TX比特 |

### 3.2 不一致问题（当前状态）

| 方案 | BER 计算方法 | 是否有 π/4 偏移 | 实际公平性 |
|------|------------|----------------|-----------|
| FOE+VV | resolve_qpsk | 有（被掩盖） | oracle 加持 |
| FOE+BPS | resolve_qpsk | 无 | oracle 加持但无害 |
| FOE+DPLL | resolve_qpsk | 有（被掩盖） | oracle 加持 |
| KF pilot | ber_count | 无 | ✅ 公平 |

**这意味着**：所有"KF vs Fixed"的对比中，Fixed 有 resolve_qpsk 加持而 KF 没有。**KF 的增益可能被低估**。

### 3.3 正确的评估方法

**方案 A（推荐）：全部用 ber_count + 统一相位模糊处理**
- VV/DPLL 需要先减去 π/4 偏移：`pe_corrected = pe - np.pi/4`
- 或使用差分解调（differential decoding）
- 所有方案用相同的 BER 计算函数

**方案 B：全部用 resolve_qpsk**
- KF pilot 也加上 resolve_qpsk
- 简单但掩盖真实相位跟踪能力

---

## 4. 代码文件清单

| 文件 | 用途 | 状态 | 已知问题 |
|------|------|------|---------|
| `sim_ch4_systematic_analysis.py` | VV/BPS/DPLL 系统性分析 | ✅ 运行通过 | VV/DPLL π/4偏移被resolve_qpsk掩盖 |
| `sim_ch4_kf_pilot_h.py` | 导频辅助 KF（主版本） | ✅ 运行通过 | Q_fine冻结；MMSE用oracle h(20dB可忽略) |
| `sim_ch4_kf_carrier_sync.py` | 原始 KF 仿真 | ⚠️ 有 P-matrix bug | P 矩阵每块重置（TL-09） |
| `sim_ch4_kf_verification.py` | 6 组公平性对照 | ✅ 运行通过 | 同 systemic 的 resolve_qpsk 问题 |
| `sim_ch4_kf_perblock_h.py` | DD 逐块 h 估计 | ✅ 运行通过 | DD 在深衰落下崩溃（TL-10） |
| `sim_kf_stress_common.py` | Track B 公共模块 | ✅ 运行通过 | VV 公式用 unwrap(angle*M)/M（比 systemic 更差） |
| `sim_direction_a.py` | 原始自适应 MVE | ✅ 运行通过 | 已废弃 |
| `verify_systematic.py` | Track A 100种子验证 | ✅ 运行通过 | 同 systemic 的 resolve_qpsk 问题 |
| `sim_ch3_ber_closed_form.py` | Ch3 BER 闭合解 | ✅ 运行通过 | 无已知问题 |
| `sim_ch3_strengthening.py` | Ch3 设计准则 | ✅ 运行通过 | 无已知问题 |

所有代码在 `projects/thesis-figures/simulation/` 下。
Python 环境：`~/.venvs/torch/bin/python`

---

## 5. 已知 Bug 和修复状态

| Bug | 严重度 | 影响范围 | 状态 | 修复方案 |
|-----|--------|---------|------|---------|
| VV π/4 恒定偏移 | 高 | 所有使用 VV/DPLL 的结果 | **已确认，未修复** | 评估方法统一或实现内补偿 |
| resolve_qpsk 掩盖 CPR 失效 | 高 | 所有 BER 对比结论 | **已确认，未修复** | 统一用 ber_count |
| P-matrix 每块重置 | 中 | sim_ch4_kf_carrier_sync.py | **已确认，未修复** | 传递 P_init/P_final |
| VV unwrap(angle*M)/M 在长序列崩溃 | 中 | sim_kf_stress_common.py | **已确认** | 用 unwrap(angle)/M |
| 不同信道实现对比 (TL-13) | 中 | sim_ch4_kf_pilot_h.py | **Track B 已修复** | 共享信道生成 |
| Q_fine 频率跟踪冻结 | 低 | 所有 KF 实现 | **已确认** | Q[1,1] 是哑参数，影响可忽略 |
| MMSE 用 oracle h | 低 | 所有实现 | **已验证** | 20dB 下影响可忽略 |

---

## 6. 验证过的结论 vs 待验证的结论

### 已验证（高置信度）

1. ✅ DPLL 在强湍流下 0% 灾难性失败率（Track A 100 种子）
2. ✅ VV/BPS 在强湍流下 ~40-45% 灾难性失败率（Track A）
3. ✅ KF pilot 增益在共享信道后仍然显著（Track B A1）
4. ✅ Q[1,1] 是哑参数（Track B B1）
5. ✅ P 矩阵初始化不敏感（Track B B3）
6. ✅ 导频前置式最优（Track B B5）
7. ✅ 激光线宽增加→KF增益增加（Track B C2）

### 待重验证（评估方法不一致导致可能错误）

1. ⚠️ DPLL 强湍流优于 KF pilot（D1）→ DPLL 有 resolve_qpsk 加持
2. ⚠️ VV 弱湍流有害（D2）→ resolve_qpsk 在弱湍流下放大约 862×
3. ⚠️ 最优 Fixed 参数 M_vv=256, ω_n=20MHz → 基于 resolve_qpsk 评估
4. ⚠️ KF 增益具体数字（+11/+12/+7 dB）→ 对手评估不公平，实际可能更高

### 已证伪

1. ❌ "湍流感知 R 矩阵"是贡献（B2+D3 双重验证）
2. ❌ "导频 h 估计对 R 有价值"（B2）
3. ❌ "KF 全湍流增益"→ 仅弱/中等有效

---

## 7. 新对话启动检查清单

新对话开始仿真工作前，**必须**：

- [ ] 读本文件（SIM-SYSTEM.md）
- [ ] 确认信号模型：r=√h·s·exp(jφ)+n, γ=γ̄·h
- [ ] 确认评估方法：ber_count vs resolve_qpsk，必须统一
- [ ] 确认已知 bug 列表（§5）
- [ ] 确认要修改的文件和已知问题（§4）
- [ ] 读 `thesis-lessons.md`（13 条教训）

---

## 8. 变更日志

| 日期 | 变更 |
|------|------|
| 2026-05-31 | 创建文档。记录 π/4 偏移 bug、resolve_qpsk 不一致、验证结论状态 |
