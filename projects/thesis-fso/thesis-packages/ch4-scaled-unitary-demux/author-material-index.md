# 第四章作者材料总索引

本索引按“写什么”组织，而不是按研究过程排序。正式写作优先使用“主入口”；辅助文件只用于核对、补证或回答质疑。

## 按写作任务取材

| 写作任务 | 主入口 | 辅助材料 | 可直接组织的内容 | 使用警告 |
|---|---|---|---|---|
| 方法身份与章级问题 | `chapter-blueprint.md`、`claim-and-citation-ledger.md` | `fact-matrix.md` | 问题定义、方法身份、贡献边界、章末结论 | 不声称首次、最优或普遍适用 |
| 数学推导与算法步骤 | `algorithm-box.md` | `figures/ch4-method-flow.svg`、`method-figure-semantic-brief.md` | LS、SVD、方向提取、两种尺度、调参基线、复杂度 | 三条支路是并列比较，不是在线选择器 |
| 实验配置 | `tables/ch4-formal-configuration.md` | `fact-matrix.md` | 场景、调制、导频、SNR、BER、配对随机簇 | SNR 是每偏振、衰落前、数据符号 $E_s/N_0$ |
| 承重结果 | `tables/ch4-formal-headline-results.md` | `figures/ch4-formal-ber-curves.*`、`figures/ch4-formal-required-snr-gain.*` | 完整曲线、工程参考 BER、所需 SNR 与置信区间 | 仅中等湍流、$N_p=2/4$ 承担主要性能主张 |
| 导频敏感性 | `figures/ch4-formal-pilot-sensitivity.*` | `data/ch4-formal-pilot-sensitivity.csv` | $N_p=2,4,8,16$ 的趋势与固定 25 dB 结果 | 不外推为任意信道的普遍导频效率 |
| 作用机理 | `figures/ch4-formal-mechanism.*` | `data/ch4-formal-mechanism.csv`、`algorithm-box.md` | 信道 NMSE、求逆残差、方向—尺度解释 | 导频重构支路的信道 NMSE 不是该支路自身估计器证据 |
| 适用性与边界 | `figures/ch4-formal-robustness-boundary.*` | `data/ch4-formal-mismatch.csv`、`fact-matrix.md` | 湍流切片、非酉失配扫描、反转边界 | $\delta$ 是无量纲结构失配，不是 PDL 的 dB 值 |
| 跨章衔接 | `thesis-spine-integration-notes.md` | `figures/ch4-method-flow.*`、`tables/ch4-formal-configuration.md` | 物理顺序、Ch4 输出、Ch3 输入、可写边界 | 只写模块接口，不写联合性能 |
| 答辩准备 | `reviewer-question-bank.md` | `claim-and-citation-ledger.md`、`formal-figure-table-verification.md` | 问题—证据—指针卡 | 问题库是备查卡，不是答辩逐字稿 |

## 材料分层

### 正式作者材料

- 组织骨架：`chapter-blueprint.md`。
- 事实卡：`fact-matrix.md`。
- 公式与算法卡：`algorithm-box.md`。
- 主张与引用卡：`claim-and-citation-ledger.md`。
- 图表：`figures/ch4-formal-*`、`figures/ch4-method-flow.*` 与 `tables/ch4-formal-*`。
- 跨章和答辩：`thesis-spine-integration-notes.md`、`reviewer-question-bank.md`。

### 历史材料

以下资产只用于追溯早期确认，不再作为正式数字来源：

- `data/ch4-confirmation-summary.csv`
- `plot_ch4_results.py`
- `figures/ch4-ber-comparison.svg`
- `figures/ch4-ber-comparison.png`
- `verification.md`

正式写作不得把这些资产中的旧切片、旧统一参数概括或旧图，与 `ch4-formal-*` 结果混用。

### 内部核验材料

以下文件用于回答“数字从哪里来、是否独立复核”，不直接转写为论文语言：

- `canonical-formal-raw-independent-verification.md`
- `canonical-formal-statistics-independent-verification.md`
- `formal-figure-table-verification.md`
- 其余 `*-independent-verification.md`

内部核验标识和流程术语不进入论文正文。

## 建议取材顺序

1. 先用 `chapter-blueprint.md` 固定每节职责。
2. 用 `algorithm-box.md` 与方法图组织方法节。
3. 用配置表和五组正式图建立实验节。
4. 每写一个结论，回查 `claim-and-citation-ledger.md` 的允许范围。
5. 完稿前用 `reviewer-question-bank.md` 逐项检查是否已有证据落点。
