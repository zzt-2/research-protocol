# [S007] B5 路 2 Step 4a sandbox 执行 → Kill（算子贡献实测 −1%，M-C-A 核心证伪）

> 2026-07-08 | 阶段: GW Step 4a 维度 A-D（路 2 终判）| 状态: Kill B5-Q1
> 来源: H007 接手（Step 4a sandbox 执行）

## 目标

守 FR-22 执行路 2 Step 4a：2×2 消融拆"B5 线性比 vs Vieira 对数比"算子贡献 vs FFT 分辨率贡献，维度 A-D 全过，Go/Conditional/Kill 判断。

## 记录

### 1. 接收方验证（H007 §接收方验证 3 条全 PASS）

| 验证项 | 结果 | 证据 |
|---|---|---|
| Vieira α=17 GHz 原文值 | ✅ PASS | content.md L349 "minimum mean value error at Δf=10GHz was selected, which was 17 GHz"；L375 "coarse CFE uses an α of 17 GHz"；Diniz [50] 初始 21 GHz |
| Vieira 无多块均值 | ⚠ **部分修正** | content.md L375 "FFT window of 1024 samples (512 symbols)"——**原文是单窗**。但 sandbox 的 `vieira_psa_single` 实际做了 16 块均值（n_blocks=N//n_fft=16，L313-320）以匹配 B5 总样本做公平对照。H007 说"Vieira 无多块"对原文成立，对 sandbox 代码不成立 |
| ±13 GHz 联合范围 | ✅ PASS | content.md L387 "the combination with the coarse CFE stage raises the compensation limit to at least 13 GHz (16-QAM)"——明确是 coarse+fine 联合 |
| depends_on 4 项稳定 | ✅ PASS | _registry.yaml 全 active/closed 无矛盾 |
| 范围未违反"明确不含" | ✅ PASS | 路 2 Step 4a 执行 |

**关键修正**（影响实验设计）：H007/S006 把 2×2 设计成"算子×块结构（单窗/16均值）"是错的——sandbox 里 Vieira 已经做了 16 块均值。真实公平轴是**算子（线性/对数）× FFT 分辨率（n_fft=16/1024）**。本轮按真实代码重新设计 2×2。

### 2. 2×2 消融执行（子 agent 执行 + 主线 V5 独立重算）

落盘：`projects/simulation/explore/b5-leo-doppler-spectrum-foe/_ablation_2x2_results.json`

**四格 σ（MHz，1.0GHz 主点，3 频偏完全一致因残频≈0）**：

| 格 | 算子 | n_fft | σ (MHz) | α 标定值 |
|---|---|---|---|---|
| A | 线性 ratio `(P+-P-)/(P++P-)` | 16 | 11.369 | 7.05e8 |
| B | 对数 `α·ln(P+/P-)` | 16 | 11.372 | 3.42e8 |
| C | 线性 ratio | 1024 | 28.957 | 1.24e9 |
| D | 对数 ln | 1024 | 28.709 | 6.12e8 |

**主线 V5 独立重算（INVARIANT 10，不信子 agent 归因）**：
- 算子贡献（同 n_fft 下对数−线性）：n16 = B−A = +0.003；n1024 = D−C = −0.249 MHz → 均值 **−0.123 MHz**
- FFT 分辨率贡献（同算子下 n1024−n16）：线性 = C−A = +17.59；对数 = D−B = +17.34 → 均值 **+17.46 MHz**
- 总差 D−A = 28.709 − 11.369 = **17.34 MHz**
- **算子贡献占比 = −0.123/17.34 = −0.7%**（与子 agent −0.7% 一致，归因可复现）

**A0 假设验证（M-C-A 的 A：对数比小残频不稳）**：
- f=0（P+≈P- 极端）：B/A σ 比 = 1.0002；f=100MHz（小残频）：B/A σ 比 = 1.0002 → 均 <<1.30 阈值
- **线性-对数算子相关系数（残频≈0 处）= 0.994**——两算子携带几乎相同信息（ln 的 Taylor 展开 ≈ 线性比的尺度变换，差异被 α 吸收）
- **A0 假设证伪**

**公平性核查**：四格同总样本 16384 + 同星历预补（ephem_residual=0）+ 四格独立 α 标定（单点 200MHz，n_seeds=8）+ bias_corr 统一处理（σ 是 std 不含均值，不影响归因）。斜率标定（50/200MHz 两点）交叉验证算子贡献 2.3%，结论稳健。

### 3. 新发现：experiment_C α 标定 bug（影响 S005 旧结论）

主线 V5 核查 `_scope_advantage_audit.py` L421-422：experiment_C 的 grid C（B5@n_fft=1024）用了锚 `alpha=ALPHA`（=6e8，是 n_fft=16 标定值），**没有为 n_fft=1024 重标 α** → σ 被人为压到 14.1MHz（重标后真实 29.0MHz）。

影响：
- **S005/D003 的"66% 同族增量"叙事误导**：那 66% 其实主要是 FFT 分辨率差（n_fft=16 vs 1024），不是算子差。experiment_C 用未重标 α 去拆"FFT 分辨率贡献"会高估算子贡献
- **不影响 D004 Kill 判定**：无论 α 是否重标，算子贡献都 <10%（重标后更明显：n_fft=1024 下 C=29.0 vs D=28.7，算子贡献 −0.25 MHz）。bug 只是让旧结论的归因不准，不改变 Kill 结论
- **教训登记**（D004 教训 2）：跨 n_fft 对照必须每格独立 α 标定，锚 α 只能用于锚 n_fft

### 4. Step 4a 维度 A-D 全过

| 维度 | 结果 | 判定 |
|---|---|---|
| **A0 致命缺陷** | M-C-A 的 A（对数比小残频不稳）实测不成立：B/A=1.00 <1.30，相关 0.994 | **FAIL** |
| **A 对手合法性** | Vieira 2023（同族，2019+）合法 | PASS |
| **B 复现性** | 2×2 消融可复现，V5 主线独立重算一致 | PASS |
| **C 信号强度** | 算子贡献 −1%（<10% Conditional-Kill 阈值）| **FAIL** |
| **D oracle 上界** | FR-21 降级参考（D003 路线，不当 Kill 门）| — |

**维度 A0+C 双 FAIL → Kill（D004）**。

### 5. Salvage 评估（无）

- **算子贡献**：−1%（证伪，无 salvage）
- **参数贡献（n_fft=16）**：B5 锚论文确实规定 n_fft=16（params.py FFT_POINTS_B5，content.md L87 "16-point FFT" + "1024 sets mean filtering"），但这是**公开工程参数**，Vieira 或任何人可同样采用 → 不构成独占贡献，无算法创新
- B5 相对 Vieira 既无算子贡献也无独占参数贡献 → 无 salvage 角度

### 6. Kill 判定（D004）

路 2 Step 4a 维度 A0+C 双 FAIL，无 salvage → **Kill B5-Q1**。

守 D003 候选池约束：用户"方向没那么多"是说"增量改进值得试不要轻易 Kill"，不是"明知证伪还强行 Go"。核心被证伪时，方向稀缺不能当强行 Go 理由（D003 原文"值得试≠强行 Go"）。

## 决策引用

- **D004（新建）**：路 2 同族精度改进也 Kill——算子贡献实测 −1%，M-C-A 核心证伪
- **V001（新建）**：路 2 Step 4a 2×2 消融验证 FAIL（关联 D004）
- D003（判定阈值：算子贡献 <10% → Conditional-Kill）
- D002（公平对照强制——本轮 2×2 严守同星历/同样本/独立 α 标定）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。Step 4a sandbox + Go/Kill 判断是 H007 明确任务
- **salvage 评估（§7）**：用户追问"能不能挣扎一下"触发，跑 6 类适配扫描是 Kill 后诚实 salvage，属收尾合规（adaptation-scan.md 明确"跑 MVE/Contract/Execute 实验前找增量方向"，Kill 复核同理）
- 未扩范围：Kill 判定后未开新候选（候选池决策是用户的事，本轮只收尾 B5）

### 7. Salvage 评估（6 类适配扫描，用户追问"能不能挣扎一下"后）

**触发**：Kill B5 后用户让看 S013（NDA-ML 适配扫描）+ 新 skill（adaptation-scan.md 6 类），问"能不能挣扎一下"。认知盲点：D004 Kill 只查了"算子贡献"（B5 算子 vs Vieira 算子，−1%），**没跑完整 6 类适配扫描**。NDA-ML 教训（S013）是算法层无增量但 A4 条件切换出信号——同样扫描可能给 B5 翻盘。

**方法**：派子 agent 跑 A1/A4/A5/A6（A2 D002 已做/A3 无证据跳过），落盘 `_adaptation_scan_results.json`。主线 V5 独立核查关键论断（n_fft 全条件最优=16 / 无 crossover）。

**结果：6 类全无信号，确认 Kill 成立，没有挣扎空间。**

| 适配类 | 扫描内容 | 结果 | 物理解释 |
|---|---|---|---|
| A1 参数适配 | n_fft∈{16,64,256,1024} 跨 9 条件（weak/mod/strong × 8/13/18dB）| **FAIL**：最优 n_fft 全是 16 | 块数均值降噪（1/√n_blocks）恒主导，频率分辨率从不反转 |
| A4 条件适配 | B5(16) vs Vieira(1024) σ 差跨 9 条件 | **FAIL**：diff 恒正 [+5.3,+12.5]，无 crossover | B5 全条件赢，但赢的是公开参数（n_fft=16）非独占 |
| A5 评价维度 | outage P(|resid|>140MHz) / IQR / 收敛迭代 | **FAIL**：outage 全 0（两法残频都<140MHz，都够好）| σ 优势（B5 13-21 vs Vieira 23-29MHz）不转化为通信可用性 |
| A6 失效边界 | 扫频偏残频找失效点 | **FAIL**（子 agent 主动降级误报）| B5 σ 非单调（Rp-n 饱和噪声尖峰），两法同点失锁 |

**V5 主线核查**（INVARIANT 10，不信子 agent 归因）：亲自核 A1 每条件 all_sigma——n_fft=16 全是最小（weak_8dB: {16:8.05,64:16.6,256:24.2,1024:13.6}；moderate_13dB: {16:10.2,64:23.9,256:23.3,1024:23.4} 等 9 条件无一例外）。A4 diff_vieira_minus_b5 9 条件全正。归因可复现。

**Salvage 物理结论**：B5 的全部优势 = n_fft=16（1024 块均值，σ 按 1/√1024 降）vs n_fft=1024（16 块均值，σ 按 1/√16 降）。这是**纯粹的块数均值降噪**，是公开工程参数选择，任何人都能用，**无任何条件/维度/边界独占性**。NDA-ML 的 A4 信号（条件切换）在 B5 不复现——这里方法间优势关系单调锁定（B5 全条件赢但赢的是公开参数）。

**子 agent 诚实表现**：两处主动 defy-save——A5 用物理意义维度（outage 通信可用性非"换指标直到赢"）全 0 时诚实报"σ 优势无可用性落地"；A6 初判误报信号后深查发现 B5 σ 非单调，主动降级无信号，不把噪声尖峰当失效边界卖。

**对 Kill 判定的影响**：**确认 D004 Kill 成立，不翻盘**。但补强了 Kill 的完备性——现在不是"只查算子就 Kill"，是"6 类适配扫描全无信号才 Kill"。教训：Kill 前应跑完整 adaptation-scan，不只查单一维度（见 D004 教训补充）。



## 后续

**B5-Q1 收尾**。Kill 后代码保留（common 的 short_time_spectrum_foe + leven_mthpower_foe + explore 下全部脚本 + _ablation_2x2_results.json）作 baseline 库扩展 + 教训素材。

**用户决策点**（H008 交接）：
- 候选池现状：NDA-ML 卡 D-008/D-009 / B7 待 MVE（active）/ B3-Q2 阶段 0 进行中（active）/ B2 Kill / **B5 Kill（本轮）**
- 用户决定：① 推 B7 出 MVE 结果 ② 等 B3-Q2 阶段 0 ③ 开新候选 ④ 回看其他方向（如 thesis-method-redirection 的 16-QAM CPR 种子）

**可复用资产**（给其他候选）：
- 2×2 消融框架（算子×参数维度拆贡献来源）——任何"X 算子比 Y 算子好"的声称都该先做消融
- experiment_C α 标定 bug 教训——跨 n_fft/块结构对照必须独立 α 标定
- 公平对照框架（同星历/同样本/同 α 标定方法）——D002 教训的实操化

**专题去向**：B5 Kill 后专题转 closed（待用户确认是否还有 salvage/复盘需求，本轮先 active 留 H008 交接）。
