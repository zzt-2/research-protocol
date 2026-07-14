# [S015] PROMPT-013 回传主控核验 + baseline 混杂决策

> 2026-07-13 | GW Step 4a 维度 D MVE 扩展 | 状态：D021 已验证；PROMPT-015 GO
> 2026-07-13 续接 | 统一合法 baseline 重比完成并落盘

## 目标

独立核验 PROMPT-013（Q1 交换质量 + Q2 机制）回传数据，确认执行对话结论可信；集成进治理文档；据 Q2 暴露的 baseline 混杂与用户决策，立项统一合法 baseline 重比（D021）。

## 记录

### 恢复时的状态分歧（FR-26 证据链）

压缩恢复提示词说"PROMPT-013/014 刚派出等回传"。仓库实际状态：

| 子对话 | 恢复快照 | 仓库实际 |
|---|---|---|
| PROMPT-014 | 等回传 | ✅ 已处理：S014/D019(rejected,deferred)/V003(PARTIAL) |
| PROMPT-013 Q1 | 等回传 | ✅ 已 PASS 落盘 `prompt013_swap_quality.json`（30 seeds） |
| PROMPT-013 Q2 | 刚派出 | ✅ 已完成落盘 `prompt013_swap_mechanism.json`（6 trials），执行对话已写 D020/V004 |

恢复快照是压缩时刻的旧投影，以仓库为准。

### Q1 独立核验（不信任摘要）

从 `prompt013_swap_quality.json` 原始 30 per-seed 值独立重算：

| 指标 | stored | recomputed | 一致性 |
|---|---|---|---|
| CMA 超额 PI-BER mean | 0.014718 | 0.014718 | OK |
| ML 超额 PI-BER mean | 0.001154 | 0.001154 | OK |
| 配对 ML 胜 | 30/30 | 30/30（0 tie, 0 CMA 赢） | OK |
| Wilcoxon p | 1.8626e-9 | 1.8626e-9 | OK |

holdout 20 seeds（1010-1029）独立复现：ML 20/20，p=1.91e-6。

**Q1 PASS 属实**：ML 相对 current scalar-error CMA 的交换质量优势在 30 seeds 下统计显著（p<1e-8），远强于 10-seed 版（p=0.0020）。口径修正（连续超额 PI-BER + Wilcoxon 主判）消除了阈值摇摆问题。

口径提醒（写作勿混）：12.75× 是 N=5M **超额** PI-BER 之比；3-3.8× 是 N=2M **绝对** PI-BER 之比。不同长度不同口径。

### Q2 独立核验（关键：standard CMA 消除差距）

从 `prompt013_swap_mechanism.json` 的 6 trials 重算 current vs standard CMA：

| seed | group | ML(Q1) | current CMA | **standard CMA** | standard 降幅 |
|---|---|---|---|---|---|
| 1006 | high-gap | 0.0 | 3.31e-2 | 4.40e-5 | **752×** |
| 1017 | high-gap | 0.0 | 3.22e-2 | 4.68e-5 | **688×** |
| 1011 | high-gap | 3.42e-2 | 5.90e-2 | 5.61e-2 | 基本无效（5%） |
| 1024 | low-gap | 0.0 | 4.56e-5 | 4.56e-5 | 已≈0 |
| 1028 | low-gap | 0.0 | 4.96e-5 | 4.68e-5 | 微降 |
| 1029 | low-gap | 0.0 | 5.24e-5 | 4.40e-5 | 微降 |

核验确认报告数字属实。但报告措辞"两个高差 seed 上几乎消除差距"需精确补充：**第三个 high-gap seed（1011）上 standard 无效**——说明 standard CMA 不是普遍消除差距，而是只在部分样本上。

机制结论（与报告一致）：
- **H_a（代价函数错位）证伪**：current CMA 高/低 NMSE 比 1.98（需≥3），方向不一致
- **H_b（在线更新推坏）unknown**：freeze 主阈值 current/standard 均 0/3 达标
- **H_c（容量差异）排除**：两者均 88 实自由度；但 ML 交叉支路 wxy/wyx 实际初始化为 1（`_ml_equalizer.py:88-89`），注释说 0（L114），CMA 为 0（`_cma.py:81-86`）——**初始化混杂**

### 主控判断：方法层卖点被严重收窄

Q1 的 30-seed 优势（铁证）里，**至少 high-gap 部分（seed 1006/1017）是 current-CMA 实现 bug 贡献的**——换成 standard CMA（补 z 因子）差距消失。这是 D016→D017"代码 bug 假说"的精准回归：D017 用 10-seed 均值（被 low-gap 拉平）否决了假说，Q2 在差距来源处（high-gap seed）推翻了 D017。

**能说的**：ML 优于项目中 scalar-error CMA 实现（30/30, p=1.86e-9）
**不能说的**：ML 优于经典/标准 CMA——standard CMA 在 2/3 high-gap seed 消除差距

ML 交叉支路初始化混杂（wxy/wyx=1 vs CMA=0）是第二个未排除因素：ML 从满蝶形起点出发，CMA 从对角起点出发，Q1 优势可能部分来自初始化而非监督学习。

### 用户决策

通过 AskUserQuestion：
1. baseline 混杂处理 → **"统一合法 baseline 后重比"**（推荐项）
2. PROMPT-014 盲 VAE → **"等 baseline 混杂解决后再说"**（不选 A 也不选 B，挂起）

### 治理文档更新

- **D021 新建**（统一合法 baseline 重比）：精确列出两个混杂的代码位置、预注册 Go/No-Go 判据、排除的替代方案
- **D019 加 deferred 标记**：A/B 二选一挂起，等 D021 结果
- **topic-index 更新**：当前位置指向 PROMPT-015；进展线索加 S015
- **D020/V004**：执行对话已写，结论与主控核验一致，未改动

### PROMPT-015 统一合法 baseline 重比（2026-07-13 续接）

按 D021 预注册合同，在不修改 common/ 与 params.py 的隔离脚本中完成 30 个 seed（1000–1029）的统一比较。每个 seed 使用 N=5,000,000、QPSK、strong turbulence、f_G=30、SOP=4e-7，并共享同一信道 realization；主指标为测试尾段 PI-BER，辅助并报 fixed-label BER。

结果完整性：checkpoint 30/30、无 pending、seed 唯一且范围正确；current-CMA、standard-CMA、ML-original、ML-aligned、oracle 的原始 BER 全部 finite；两个 ML 变体均记录 constructed/trained/inferred=true，实际 device=cuda；结果 summary 可由原始 trials 重算，experiment signature 与当前脚本参数一致，10 个来源文件 SHA 一致。

统计结果：standard-CMA vs ML-original 为 ML 29/30 胜，exact two-sided Wilcoxon W=23.0，p=1.1920928955078125e-6；standard-CMA vs ML-aligned 同为 29/30 胜、W=23.0、p=1.1920928955078125e-6。两条预注册主判据（p<0.05 且 ML 胜场≥25/30）均通过，overall gate=GO。current-CMA vs ML-original 控制比较为 ML 30/30 胜，p=1.862645149230957e-9。

解释边界：本实验支持在已注册参数域内将 standard-CMA 作为合法 baseline 后，ML 仍保留 PI-BER 优势；不支持“所有场景 ML 普遍优于 CMA”。ML-original 与 ML-aligned 均值差为 7.6e-7，仅作初始化敏感性描述，不能作因果归因。fixed-label 接近 0.5 的样本仍需按极化交换解释，不能替代 PI-BER。

产出已落盘：PROMPT_015_REPORT.md、prompt015_unified_baseline.py、test_prompt015_unified_baseline.py，以及 gitignore 下的 30-seed JSON。V005 记录验证证据。本次不进入 Contract，不自动解冻 D019。

## 决策引用

- D020（执行对话建）：PROMPT-013 机制归因失败，ML 相对 current CMA 优势不可泛化为相对经典 CMA 的机制优势
- D021（新建）：统一合法 baseline 重比，修正 standard CMA + ML 初始化混杂，30-seed 三方对比
- D019（加 deferred）：盲 VAE A/B 挂起等 D021

## 范围确认

- 本轮是否在 scope boundary 内：是（PROMPT-013 回传核验 + 据结果做 baseline 决策，属 GW Step 4a 维度 D MVE 扩展的 baseline 合法性范畴）

## 后续

- 将 D021 状态更新为“已验证 GO”，后续若推进方法层，沿标准 CMA 合法 baseline 使用本次报告的范围化措辞
- 保持 D019 盲 VAE 挂起，除非主控另行明确解冻并重新注册验证合同
- 进入下一阶段前仍需单独读取对应阶段框架文件；本次 PROMPT-015 不进入 Contract
