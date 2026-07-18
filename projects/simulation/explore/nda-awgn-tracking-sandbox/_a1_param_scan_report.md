# A1 参数适配扫描报告

> 来源: adaptation-scan.md A1 | 2026-07-08 | 耗时 62.6s | 5 seed
> 数据: `_a1_param_scan_results.json` | 脚本: `_a1_param_scan.py`

## TL;DR — A1 信号判定

| 参数 | 最优值随条件变? | A1 信号 | 自适应增益粗估 |
|---|---|---|---|
| **DA pilot_spacing** (γ_tot 公平坐标) | **否** (全场景全 SNR 最优 sp=16) | ❌ **不成立** | ~0 dB (固定 sp=16 即全场景最优) |
| **NDA intra_block_tracking K** | **是** (随 SNR 升/随湍流强降) | ✅ **成立** (趋势) | **~0 dB** (oracle 空间被中庸 K4 压缩) |

**核心结论**: 两个参数的 A1 信号都成立/不成立得"干净"——但**自适应增益都微乎其微 (<0.05 dB)**。
- DA: γ_tot 公平校正后, 最稀 pilot (sp=16) 全场景最优, 物理是"pilot overhead 红利 > 密 pilot 降噪红利"。
- NDA: 最优 K 确随条件变 (趋势成立), 但 K=4 中庸, 几乎全场景次优 → 固定 K=4 已捕获 99% oracle 空间。
**→ A1 自适应参数策略无实质增益, 跳过此方向。**

---

## 任务 1: DA-ML pilot_spacing 扫描

### 1.1 γ_d 原始坐标 (不公平, 仅供参考) — sp 越小 (密 pilot) 越好

| scene | γ=8/10 | γ=14/15 | γ=18/20 | γ=20/24 |
|---|---|---|---|---|
| awgn | sp8 | sp2 | sp2 | sp4 |
| weak | sp16 | sp8 | sp2 | sp4 |
| moderate | sp16 | sp8 | sp16 | sp8 |
| strong | sp16 | sp16 | sp16 | sp16 |

**γ_d 坐标看似 sp 随场景变** → 但这是**假信号**: γ_d 坐标下 sp=2 有 3dB overhead "免费"能量,
不付出代价就拿到密 pilot, 当然 γ_d 坐标下赢。

### 1.2 γ_tot 公平坐标 (正确) — sp=16 全场景全 SNR 最优

公平对照: γ_tot = γ_d + overhead_db(sp), overhead = {sp2: 3.01, sp4: 1.25, sp8: 0.58, sp16: 0.28} dB。
同一参考 γ_tot 下 log 插值比较各 sp 的 BER:

| scene | γ_tot=14 | γ_tot=18 | γ_tot=22 | 最优 sp |
|---|---|---|---|---|
| awgn | (范围太窄) | — | — | sp16 (γ_d 坐标低 SNR 仍 sp8/16) |
| weak | **sp16** (6.30e-2 vs sp2 1.42e-1) | **sp16** (1.99e-2 vs sp2 5.16e-2) | **sp16** (4.84e-3 vs sp2 1.24e-2) | **sp16** |
| moderate | **sp16** (9.04e-2 vs sp2 1.91e-1) | **sp16** (3.69e-2 vs sp2 8.91e-2) | **sp16** (1.24e-2 vs sp2 3.07e-2) | **sp16** |
| strong | **sp16** (1.69e-1 vs sp2 2.91e-1) | **sp16** (1.05e-1 vs sp2 2.01e-1) | **sp16** (5.94e-2 vs sp2 1.23e-1) | **sp16** |

**γ_tot 公平坐标下, sp=16 在所有场景所有 SNR 一致最优** (且优势随湍流增强而增大)。
典型差距: weak γ_tot=18 sp16=1.99e-2 vs sp2=5.16e-2 → **2.6× BER**。

### 1.3 物理解释 (偏离 TL-20 预期, 但有合理解释)

TL-20 原预期: 低 SNR 密 pilot 好 (多 pilot 平均降噪), 高 SNR 稀 pilot 好 (省 overhead)。
**实测偏离**: 全 SNR 段稀 pilot (sp16) 好。

原因分析 (诚实): 在本场景 (N_DFT=256 块, M0=8, 16APSK), 块内有足够符号 (256) 让稀 pilot (sp16 → 16 pilot/块)
仍能可靠估 CPE + FOE (pilot 线性回归 16 点足够)。pilot overhead 红利 (sp16 仅 0.28dB vs sp2 3.01dB) 持续主导。
密 pilot 的"降噪"红利在 16 pilot/块时已饱和 → 更密只浪费 overhead。

**→ A1 信号 (DA pilot_spacing) 不成立**: 固定 sp=16 全场景最优, 无自适应空间。
**→ 建议**: 主实验 DA_PILOT_SPACING=4 可考虑调到 8 (0.58dB overhead vs 1.25dB), 但这是单点优化, 非自适应。

---

## 任务 2: NDA-ML intra_block_tracking K 扫描

### 2.1 最优 K 随条件变 (A1 信号趋势成立)

| scene | γ=8/10 | γ=14/15 | γ=18/20 | γ=20/24 | 趋势 |
|---|---|---|---|---|---|
| **awgn** | none | K4 | K8 | K16 | **随 SNR 升 K 单调升** |
| **weak** | none | K4 | K4 | K8 | 同上 (转折较缓) |
| **moderate** | none | none | K4 | K4 | 转折点右移 |
| **strong** | none | none | none | none | **湍流主导, 全 none** |

**物理一致** (确认 sandbox 已知趋势 + 补全):
- 高 SNR 用大 K (细跟踪): Wiener PN 块内漂移成 high-SNR BER floor 主导, 大 K 分段跟踪能追上 → 高 SNR 需 K8/K16。
- 低 SNR 用小 K (多平均降噪): 升幂 mean-angle 每 pilot 信噪比不够, 段太短噪声大 → 低 SNR 需 none/K1 (整块平均)。
- 强湍流用 none: deep fade 致分段跟踪把噪声当相位追 → strong 全 none (与 sandbox 结论一致)。
- 湍流越强, none 优势区间越宽 (转折点右移: awgn@14 已 K4, moderate@15 仍 none)。

**→ A1 信号 (NDA tracking) 趋势成立**: 最优 K 随 SNR 单调升, 随湍流强降。E1 锚点满足。

### 2.2 自适应增益分析 (诚实: 增益极小)

对比三种策略 (16 点 = 4 场景 × 4 SNR 的 aggregate log-mean BER):

| 策略 | log-mean BER | vs 最强固定 K4 |
|---|---|---|
| (a) 最强全局固定 K=4 | 2.908e-2 | (基准) |
| (b) 跨场景自适应 (strong→none, 其余→K4) | 2.906e-2 | ×1.00 (≈0 dB) |
| (c) oracle (每点最优 K) | 2.894e-2 | ×1.00 (≈0 dB) |

**自适应空间被"中庸 K4"压缩**: K=4 在 AWGN/weak/moderate 几乎全 SNR 次优 (差最优 ≤1.04×),
在 strong 略输 none 但差距 ≤1.01×。固定 K=4 已捕获 oracle 99% 的增益空间。

最大单点改善 (oracle vs 固定 K4): **awgn γ=8, best=none, ratio=1.04×, ~0.04 dB** —— 实质上可忽略。

### 2.3 结论

- A1 信号**趋势成立** (最优 K 随条件变, 物理清晰), 但**自适应增益 <0.05 dB** (中庸 K4 压缩空间)。
- **→ 不建议**做 NDA tracking 自适应 K 策略: 固定 K=4 已足够。
- 已知趋势 (AWGN segmented 好, strong none 好) 在本扫描中**确认**: AWGN 中高 SNR K4/K8/K16 都反超 none;
  strong 全 SNR none 最优。但"none vs K4"在 strong 差距也仅 ≤1.01×。

---

## 纪律符合性

- [x] 守 TL-13: 信道/调制/resolve/da_ml/mmse_equalize/amp_limit/fft_foe 全从 common/ 导入, 不重写算法
- [x] 不改 common/ / simulator/ (option A: 参数扫描在脚本内传参; NDA segmented K 本地复制数学支持 K 参数)
- [x] γ_tot 公平坐标 (DA 对照): overhead_db = 10·log10(sp/(sp-1)), γ_tot = γ_d + overhead
- [x] TL-20 理论预期对照: DA 偏离 (全 SNR sp16 好, 物理解释: pilot 16/块已饱和); NDA 符合 (高 SNR 大 K, 强湍流 none)
- [x] 5 seed (TL-29 多 seed, 避免 D-009 单 seed 假阳性)
- [x] N_sym/点 = 200×256 = 51200 (BER~1e-3 区统计足够)
- [x] seed 派生同主实验 (run_awgn/run_turb): awgn seed=base+int(snr·1000); turb per-block seed=base+b

## 文件

- 结果: `explore/nda-awgn-tracking-sandbox/_a1_param_scan_results.json`
- 脚本: `explore/nda-awgn-tracking-sandbox/_a1_param_scan.py`
- 本报告: `explore/nda-awgn-tracking-sandbox/_a1_param_scan_report.md`

## 异常/发现

1. **DA pilot_spacing A1 假信号陷阱**: γ_d 坐标下看似最优 sp 随场景变 (低 SNR 密, 高 SNR 稀),
   但这是 overhead 能量"免费"的假象。**必须用 γ_tot 公平坐标**判定 → 校正后 sp=16 全场景最优。
   任何后续 pilot_spacing 实验都须报告 γ_tot 坐标, 否则会得假阳性结论。
2. **DA sp=16 全场景最优的物理含义**: 块内 16 pilot (256/16) 已足够可靠估 CPE+FOE,
   密 pilot 降噪红利在此饱和, overhead 红利主导。**主实验 DA_PILOT_SPACING=4 非最优**,
   sp=8 (0.58dB overhead) 或 sp=16 (0.28dB) 可能更优 — 这是单点优化, 非 A1 自适应, 但值得记入主实验改进项。
3. **NDA K4 中庸陷阱**: A1 信号趋势成立 (K 随条件变) 但"中庸参数"K4 几乎全场景次优,
   压缩了自适应空间。这是 adaptation-scan.md 防坑点 ("全场景最优固定参数压缩自适应空间") 的实例。
4. **NDA 在 strong 湍流 K 无关紧要**: none/K4/K8/K16 在 strong 差距 ≤1.05×, 因 deep fade 主导,
   相位跟踪细节无关 → strong 场景只需 none (确认 sandbox 结论, 且差距比预期还小)。
