# 第四章方向—尺度解耦偏振解复用材料包

> 用途：中文硕士学位论文第四章的作者可组织材料。
> 当前边界：方法、图表、事实、主张、跨章接口和答辩问题卡已整理；尚未写成连续章节正文。
> 建议章题：面向短导频相干星地链路的方向—尺度解耦偏振解复用方法。

## 作者入口

按下列顺序取材，可避免把研究过程语言或历史数字带入正文：

1. `author-material-index.md`：按写作任务定位全部材料。
2. `chapter-blueprint.md`：4.1–4.7 的节级职责和证据落点。
3. `algorithm-box.md`：公式、算法步骤、复杂度与失效处理。
4. `fact-matrix.md`：可核对的事实卡及其边界。
5. `claim-and-citation-ledger.md`：允许主张、必须披露和引用层级。
6. `thesis-spine-integration-notes.md`：与第三章及全文主线的接口。
7. `reviewer-question-bank.md`：评阅与答辩问题—证据卡。

`figures/ch4-method-flow.svg` 是可编辑的方法总图；它明确展示共同方向提取、两种结构尺度支路、独立调参基线和第三章模块接口。三条支路是并列实验比较，不是运行时选择器。

## 本章故事骨架

- 问题：短导频下，无约束 2×2 LS 估计包含不受目标物理结构约束的自由度，直接求逆容易放大估计噪声。
- 假设：目标偏振混合在冻结场景中近似“公共尺度 × 酉方向”。
- 动作：从 LS 的 SVD 中提取共同方向 $Q=UV^H$，再用信道域前向误差或当前导频重构确定尺度，形成解复用矩阵。
- 对比：普通 LS、独立调参奇异值下限和理想 CSI 参考；理想 CSI 不属于可部署基线。
- 结果：在中等湍流、短导频场景下，结构尺度判据相对调参基线降低达到工程参考 BER 所需的 SNR；随着导频增加，优势缩小。
- 边界：非酉失配增大后排序会反转，因此本章不声称全场景鲁棒或普遍领先。
- 跨章：第四章输出两路载波恢复前的复符号流，随后进入第三章每偏振 CPR；这里只建立模块接口，未做联合验证。

## 正式作者材料

### 图表与数据

- `figures/ch4-formal-ber-curves.{svg,png}`：中等湍流、$N_p=2/4$ 的完整 5–41 dB BER–SNR 曲线。
- `figures/ch4-formal-required-snr-gain.{svg,png}`：相对调参基线的所需 SNR 降低量及 95% 置信区间。
- `figures/ch4-formal-pilot-sensitivity.{svg,png}`：$N_p=2,4,8,16$ 的导频敏感性。
- `figures/ch4-formal-mechanism.{svg,png}`：信道 NMSE 与尺度处理后的求逆残差。
- `figures/ch4-formal-robustness-boundary.{svg,png}`：湍流切片和非酉失配边界。
- `figures/ch4-method-flow.{svg,png}`：方法输入—动作—输出及跨章接口。
- `data/ch4-formal-*.csv`：上述正式图表的可追溯数据。

### 表格

- `tables/ch4-formal-configuration.md`：完整配置、指标口径、调参映射和跨章接口。
- `tables/ch4-formal-headline-results.md`：四项承重所需 SNR 结果。
- `tables/ch4-method-role-comparison.md`：各方法的输入、动作、输出与比较角色。

### 生成入口

- `extract_ch4_formal_plot_data.py`：从冻结正式聚合结果确定性生成 CSV；`--check-only` 只核对现有输出。
- `plot_ch4_formal_results.py`：从正式 CSV 确定性生成五组结果图。
- `generate_method_figure.py`：确定性生成方法图 SVG 与 PNG。

## 可承重数字

工程参考 BER 为 $3.8\times10^{-3}$。中等湍流下，相对独立调参奇异值下限：

| 方法 | $N_p$ | 所需 SNR 降低量 | 95% 置信区间 |
|---|---:|---:|---:|
| 前向误差尺度 | 2 | 0.8705 dB | [0.6182, 1.0883] dB |
| 前向误差尺度 | 4 | 0.1209 dB | [0.0189, 0.2392] dB |
| 导频重构尺度 | 2 | 0.8747 dB | [0.6289, 1.0784] dB |
| 导频重构尺度 | 4 | 0.1080 dB | [0.0258, 0.2026] dB |

前向误差尺度是正文主方法；导频重构尺度是接收端可实现的强变体与尺度判据消融。现有证据不支持宣称主方法优于强变体。

## 结果使用边界

- 承重性能主张限于中等湍流、$N_p=2/4$ 的正式配对结果。
- 导频长度、机理、湍流切片和失配扫描用于解释适用性，不单独承担普遍因果主张。
- 导频重构尺度中的起始奇异值下限为 1，但每个观测的最终校准标量由当前导频闭式计算，不是固定尺度。
- 该支路返回的信道估计量是校准前继承量，不能作为该支路自身的结构信道估计证据。
- 失配参数 $\delta$ 是无量纲结构失配强度，不是 PDL 的 dB 值。
- 尚未验证 PDL、PMD、FIR、支路不平衡、非等噪声、时变 SOP、CFO、联合 CPR 或 LDPC 全链性能。

## 历史与内部材料

### 历史确认材料

`data/ch4-confirmation-summary.csv`、`plot_ch4_results.py`、`figures/ch4-ber-comparison.*` 和 `verification.md` 只用于追溯早期确认。正式写作不得从中提取数字，也不得与 `ch4-formal-*` 资产混用。

### 内部核验材料

`canonical-formal-raw-independent-verification.md`、`canonical-formal-statistics-independent-verification.md`、`formal-figure-table-verification.md` 及其他 `*-independent-verification.md` 用于追溯和复核。其中的内部核验标识与流程术语不进入论文正文。
