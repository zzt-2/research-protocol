# [S006] B5 路 2 Step 3 补精读 + 新 M-C-A 构建（重走 Step 4a 第 1 步）

> 2026-07-08 | 阶段: GW Step 3 补精读 → Step 4a 准备 | 状态: Step 3 + M-C-A 完成，sandbox/MVE 留下一对话
> 来源: H006 接手（路 2 重定位）

## 目标

守 FR-22（路 2 是新 M-C-A 必须重走 Step 3-4a，不直接跑 MVE）：
1. Step 3 补精读 Vieira 2023（同族对照 baseline）+ Diniz 2011（PSI 祖师爷）
2. 基于精读构建路 2 新 M-C-A（修正 H006/topic-index 的初稿）
3. 设计增量归因拆解方案（算子贡献 vs 块结构贡献）

本轮**只做 Step 3 + M-C-A**，sandbox/MVE/Go-Kill 判断留下一对话（守单对话 3 步上限 + profile"急于推进"防线）。

## 记录

### 1. 接收方验证（H006 §接收方验证 4 条全 PASS）

| 验证项 | 结果 | 证据 |
|---|---|---|
| topic-index 不变量段落 | ✅ 读 | 14 条 + D002/D003 范围变更 |
| 范围优势归零（1.00×）| ✅ PASS | `_scope_audit_results.json` experiment_B `range_advantage_remaining: "1.00×"` + fft_eph 19 点全 converged=true |
| 同族 PSA 增量（66%）| ✅ PASS | experiment_C `b5_vs_vieira_sigma.0.5GHz.rel_diff: 0.6628` + α 同量级（B5 6.0e8 vs Vieira 6.12e8）|
| BER 根因非 bug | ✅ PASS | experiment_A `awgn_baseline.ber_at_13db: 0.0` + B5 σ=6.84MHz vs fft σ=0.051MHz |
| depends_on 4 项稳定 | ✅ PASS | _registry.yaml 全 active/closed 无矛盾 |
| 范围未违反"明确不含" | ✅ PASS | 路 2 重定位，不回头救范围优势 |

**⚠ 文档路径偏差登记**（非事实失败）：H006/topic-index 写代码路径 `explore/b5-leo-doppler-spectrum-foe/`，实际在 `projects/simulation/explore/b5-leo-doppler-spectrum-foe/`。路 2 复用代码按实际路径。

### 2. Step 3 补精读（子 agent 执行，主对话集成）

落盘精读笔记：`papers/_read_notes/_vieira2023-diniz2011-psi-same-family.md`

**Diniz 2011（PSI 祖师爷）**：
- 获取状态：**paywall 全锁，abstract 级**（穷尽 tools/download / Optica DirectPDF / arXiv / ResearchGate / S2，全失败）
- 可确认：PSI = 双侧谱（P+/P-）的"a simple power relation（Eq.1）"，RZ 脉冲，compliant with OIF
- **未验证（FR-26）**：Eq.(1) 具体公式（log/线性比/arctan）未知——**不能据 Diniz 原文裁判 B5 vs Vieira 谁忠实继承**
- 意义：Diniz 是 PSI 大类祖师爷，B5/Vieira 都属 PSI 类；具体算子差异是 B5/Vieira 之间的差异

**Vieira 2023（同族对照 baseline，全文 573 行可读）—— 多项推翻 H006/topic-index 初稿**：

| H006/topic-index 初稿 | 精读修正 |
|---|---|
| Vieira 公式 `α·ln(P+/P-)` | ⚠ **是强推断非 verbatim**（L345 是图片，PDF→md 丢失）。基于 L347 文字推断 |
| Vieira α≈6.12e8 Hz（审计 JSON）| ⚠ sandbox **自标定值**，**原文 α=17 GHz**（L349/L375，Vieira 自己 sequential search 重定，非继承 Diniz 21 GHz）|
| L387 ±13GHz 范围 | ⚠ **两阶段联合范围**（coarse PSA + fine Mth-power），**粗估单独 ~10 GHz**。当粗估范围引是误读 |
| 同族增量来自"线性 vs 对数算子" | ⚠ **未拆**：Vieira 无多块均值（单窗 1024 样本），B5 是 1024×16。σ 差可能主要来自块结构降噪，非算子 |
| Vieira 报 σ | ❌ Vieira **只报 BER penalty (dB)**，无 σ。B5 vs Vieira σ 对照是 sandbox 两边重标定后自算 |

**对路 2 的关键影响**：
1. 同族链 Diniz→Vieira/B5 成立（都是 PSI 类），V3 同族对照对象 = Vieira（机制最近）
2. **Vieira α=17 GHz 是原文值**，sandbox 对照用了自标定 6.12e8——公平性需重新审视（对照原文 Vieira 还是重标定 Vieira，结论可能不同）
3. **增量归因必须拆**：σ 差多少来自算子（线性 vs 对数），多少来自块结构（1 块 vs 16 块均值）。这是 Step 4a 维度 D 核心

### 3. 路 2 新 M-C-A（基于精读构建）

**问题陈述（M-C-A 四要素）**：

- **M（方法/baseline）**：Vieira 2023 PSA coarse CFE，算子 `α·ln(P₊/P₋)`（[推断]），单窗 FFT 1024 样本，α=17 GHz，无多块均值
- **C（条件/场景）**：LEO 星地相干 FSO 残频估计（星历预补后残频 ~MHz 级，**非原 ±4.5GHz 全量程**——D003 已证范围优势归零，路 2 聚焦残频精度）
- **A（失效/不足）**：Vieira 对数比 `ln(P₊/P₋)` 在小残频处（P₊≈P₋）数值放大噪声——ln 在 P₊/P₋→1 时导数发散，小残频估计方差大。**注意：此 A 是 sandbox 侧论证（Vieira 原文未讨论此问题），属假设待 Step 4a 验证**
- **新方法（B5 路 2 定位）**：线性归一化比 `(P₊−P₋)/(P₊+P₋)` 替代对数比，在小残频处数值更稳定（输出有界 [-1,1]，避免 ln 发散）

**问题四判据自检**（守 glossary.md）：
1. 具体技术矛盾？✅ 对数比 vs 线性比在小残频数值稳定性（具体算子差异，非泛泛）
2. 有方法产出形态？✅ B5 线性 Rp-n 算法（sandbox 已实现，common 转正）
3. 有 2019+ baseline？✅ Vieira 2023（IEEE Access，同族最近）
4. 能做对比？✅ sandbox 三方对照框架（B5 / Vieira / fft_foe）已建，公平化后复用

**风险标注**（守 FR-23 增量改进非填补空白 + D003 候选池约束）：
- 这是**增量改进**（线性 vs 对数算子替换），非新空白。守 FR-23：增量改进是合法研究起点，只要 M-C-A 过四判据
- 守 D003：候选池偏弱+方向稀缺，增量改进值得试，**但 Step 4a 要诚实判**——算子贡献太小或拆不清仍 Conditional/Kill

### 4. 增量归因拆解设计（Step 4a 维度 D 核心）

**目标**：B5 vs Vieira 的 σ 差（66%，sandbox 自测）来源拆解——算子贡献 vs 块结构贡献

**2×2 消融矩阵**（公平条件：同星历预补 + 同采样率 + 同带限，D002 教训）：

| | 算子=线性 (B5) | 算子=对数 (Vieira) |
|---|---|---|
| **块结构=16 块均值 (B5)** | A：B5 原配置（σ=9.7MHz）| B：对数+16块（待测）|
| **块结构=单窗 (Vieira)** | C：线性+单窗（待测）| D：Vieira 配置（σ=28.7MHz）|

**增量归因公式**：
- **算子贡献** = (B − D) 或 (A − C)：同块结构下，算子差异带来的 σ 改善
- **块结构贡献** = (C − A) 或 (D − B)：同算子下，块结构差异带来的 σ 改善
- **总差** = D − A = 28.7 − 9.7 = 19.0 MHz（66%）

**判定阈值**（守 D003 教训，前置门控 P5）：
- **算子贡献 > 30%**（即算子贡献 ≥ 5.7 MHz）→ B5 算子有真贡献，Go 候选
- **算子贡献 < 10%**（≤ 1.9 MHz）→ 主要靠块结构，算子增量弱，**Conditional/Kill**
- **10%–30%** → 灰色区，看块结构是否独立可专利 + 叙事可接受

**已有数据**（experiment_C ablation_source_attribution）：
- B5 n_fft=16（原配置）σ=9.7MHz
- B5 n_fft=1024 σ=14.1MHz
- Vieira n_fft=1024 σ=28.7MHz
- ⚠ 但这只控制了 FFT 点数，**没控制块均值数**。Vieira 是单窗（1 块），B5 是 16 块均值。需补测 B/C 两格才能拆清

**待 Step 4a 补测**（下一对话）：
1. 补 B 格（对数算子 + 16 块均值）和 C 格（线性算子 + 单窗）
2. 明确 α 选择：对照原文 Vieira（α=17 GHz）还是重标定（6.12e8）——两个都跑，看是否影响结论
3. 指标：残频 σ（主）+ BER（辅，需完整链路加 CPE，D002 教训：BER 路径 MHz 敏感）

### 5. 路 2 Step 4a 维度检查清单（下一对话执行）

守 FR-21（oracle 上界降级为参考）/ FR-25（Go/Kill 标准分离）/ D003（诚实判）：

| 维度 | 路 2 内容 | 判据 |
|---|---|---|
| A0 致命缺陷 | 对数比小残频数值不稳（假设）| 实测验证，不成立则 Kill |
| A 对手合法性 | Vieira 2023（同族，2019+，传统未优化 baseline 默认）| ✅ 已满足 |
| B 复现性 | sandbox 已实现两边算子 + 2×2 消融框架 | 待补 B/C 格 |
| C 信号强度 | 算子贡献 > 30%（增量归因拆清后）| 待测 |
| D oracle 上界 | FR-21 降级参考（D003 路线，不当 Kill 门）| — |
| FR-14 先验 baseline | fft_foe（传统）作参照已有 | ✅ |
| FR-15 贡献目标 baseline | Vieira（同族，贡献声称要超越的对手）| ✅ |

## 决策引用

- 无新建决策（本轮是 Step 3 精读 + M-C-A 构建，不涉及方向变更。D003 路线不变）
- 复用 D003（路 2 重定位）+ D002（公平对照强制 + V3 同族对照）

## 范围确认

- 本轮是否在 scope boundary 内：**是**。路 2 Step 3 补精读 + 新 M-C-A 是 D003 明确的下一步
- 未扩范围：sandbox/MVE/Go-Kill 判断全部留下一对话（守单对话 3 步上限）

## 后续

**下一对话（Step 4a 执行）必读**：
1. 本 S006（M-C-A + 增量归因设计）
2. `_vieira2023-diniz2011-psi-same-family.md`（精读笔记，含 FR-26 债务）
3. `_scope_audit_results.json`（experiment_C 现有数据）
4. `projects/simulation/explore/b5-leo-doppler-spectrum-foe/_scope_advantage_audit.py`（sandbox 框架，复用）

**下一对话任务**：
1. 补测 2×2 消融 B/C 格（对数+16块 / 线性+单窗）
2. 拆算子贡献 vs 块结构贡献，判是否 >30%
3. Step 4a 维度 A-D 全过 → Go/Conditional/Kill 判断
4. **守公平对照**（D002 教训）：B5 和 Vieira 同星历预补 + 同采样率 + 同带限，无特权
5. **守 V3 同族对照**（D002 教训）：对照对象 = Vieira PSA（不是 [60]Leven）

**已知风险（下一对话要注意）**：
- B5 锚全文失败（FR-26 债务）：B5 算子定义是重建非 verbatim，若 Go 进 Contract 需补全文
- Vieira 公式 L345 是图片：α·ln 是推断，需回原 PDF 核
- sandbox Vieira α 是自标定非原文：对照设计要明确选哪个 α
- profile 第 7 次"急于推进"防线：Step 4a 维度 A-D 全过才判 Go，不跳维度
