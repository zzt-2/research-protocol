# [S035] Tier 1 执行 — D3 MMA KILL + E2 排列对称破缺（待 E2 结果填）+ standard-CMA z 因子债

> 2026-07-16 | GW 方法层 Tier 1 MVE | 状态：执行中（D3 完成，E2 跑中）
> （承接 S033 swap 全貌诊断 + S032 §F 方法层 8 机制规划。Tier 1 两方向：D3 MMA + E2 排列等变）
> 与 S034（E1 群等变 + CMA+H1，提示词1）并行，互不依赖

## 目标

执行 S033 §F 方法层下一步两个独立方向（与提示词1 的 E1/CMA+H1 并行）：
1. **方向 2：D3 MMA 多模算法**（CMA 直系变种，攻 swap 盆地对称）— GW Step 1 检索 + MVE
2. **方向 1：E2 排列等变网络**（攻 swap 的排列对称）— GW Step 1 检索 + MVE

## 记录

### A. 三铁律复述（承接提示词）

1. swap 是 SOP 物理现象，CMA 和 ML 都 swap（S033 不变量 9）
2. Go 判据用 fixed-label BER（PI-BER 对 swap 失明，S033 不变量 10）
3. swap 分类用 correlation 口径（不用 divergence trigger，S033 债务）

### B. 方向 2：D3 MMA — GW Step 1 检索 + MVE 完成（KILL）

**GW Step 1 检索**（子 agent，3 查询 ~25-28 唯一论文）：
- **0 硬撞车**（GO 可跑 MVE）。FSO+SOP swap 场景无 MMA 专题
- 邻近 = 光纤色散场景 MMA-singularity 线（Yang 2002 JSAC / Vgenis 2010 / Kikuchi 2011 OE 19(10)9868），全是 fiber 相干接收机非 FSO
- OFC 2026 EKF（Liu, DOI 10.1364/ofc.2026.w2a.67）是 FSO comparator 但用 EKF 打 RSOP 不打 swap
- ⚠️ 2015 Kalman 邻近点**未定位到**（执行 agent 报告标注疑似误标注，主线是 Vgenis-Roudas-Kikuchi-Yang 无 "Kalman 2015"）

**MVE 结果**（prompt032，5 seeds × {MMA, standard-CMA, current-CMA, oracle} + SOP=0 消融，301s）：

| 方法 | mean fixed BER | swap 率 | mean PI BER |
|---|---|---|---|
| MMA (R²_R=R²_I=0.5) | 0.0112 | 0/5 | 0.01124 |
| **standard-CMA (有 z 因子)** | **0.0002** | **0/5** | 0.00023 |
| current-CMA (无 z 因子) | 0.4842 | 5/5 | — |
| oracle | 0.0000 | 0/5 | 0.00004 |

**D3 MMA KILL**：MMA vs standard-CMA 0/5 胜，p=0.5000，无增量。消融 SOP=0 两者都正常（PASS）。

**核心失败机制**：信息论边界先验应验。MMA 模值分离是**实/虚轴**分离，不是 **X/Y 轴**分离，对 X/Y swap 期望下仍不变。MMA 打破的是 CMA **相位旋转不变性**（只依赖 |z|²），但这不等于打破 **X/Y 排列对称**，两者正交。更关键：standard-CMA 有 z 因子在新域本就不 swap，MMA 没有超越空间。

### C. 附带重大发现：standard-CMA z 因子在新域不 swap（S033 不变量 9 部分修正债）

**D3 MMA MVE 揭示的关键事实分化**：
- standard-CMA（有 z 因子，Godard 1980 标准）：新域 4.2/1.4 下 **5/5 不 swap**（fixed≈2e-4）
- ML ButterflyCNN（监督，固定权重）：新域 4.2/1.4 下 **5/5 clean-swap**（fixed≈0.495，prompt024 L0 证实）
- current-CMA（无 z 因子，common/_cma.py）：5/5 swap（复现 prompt030/S033）

→ **S033 不变量 9 "CMA 和 ML 都 100% swap" 部分是 current-CMA 无 z 因子 bug 的假象**。prompt030/S033 用的 `common/_cma.py`（current-CMA，无 z），用正确实现的 standard-CMA，CMA 在新域不 swap；只有 ML swap。

**这修正 swap 归因**：swap 主要是 **ML 固定权重的 SOP 泛化失败**（D015 原结论回归），不是"CMA 也 swap"。S033 核心张力（"D022 ML 优势只在 PI，fixed 无赢家"）需重新审视——fixed 口径 standard-CMA(0.0002) 完胜 ML(0.495)，D022 方法层卖点被进一步削弱。

**此债须主控复查**（不在本轮任务范围）：prompt030/S033 应用 standard-CMA 重跑确认 swap 全貌是否改变。本轮只记录现象 + 落 D040，不推翻 S033（须主控独立验证后决策）。

### D. 方向 1：E2 排列等变网络 — GW Step 1 检索 + MVE（待结果填）

**GW Step 1 检索**（子 agent，4 查询 ~48 唯一论文）：
- **0 硬撞车**（GO 可跑 MVE）。偏振解复用/盲分离攻 swap 场景无排列等变专题
- 邻近 = 音频 BSS 排列等变（Audioslots arXiv 2305.05591）非光学；Pan 2026 OE（10.1364/oe.582599）盲 CMA-DNN 仍困 swap 证实空白
- 与 E1（群/旋转等变攻 SOP 旋转）检索空间不重叠

**关键 smoke 验证**：标准 ButterflyCNN 蝶形结构**精确排列等变**（输入 rX/rY 交换 → 输出 zX/zY 精确交换，|zX(orig)-zY(swap)|=0.000000）。→ 架构本身对 swap 不敏感，这是 swap 盆地等势的架构根源。

**E2 机制重新定义**（基于 smoke 验证 + D3 发现）：E2 不是"加排列等变"（标准架构已是），而是"**打破排列对称性**"——非对称锚点（gX≠gY 可学习门）+ 排列敏感正则（强制正常/交换输入输出差异 ≥ margin）。

**MVE 设计**（prompt033）：
- L0 baseline：标准 ButterflyCNN（asym=False，已验证 5/5 clean-swap）
- E2 变体：AsymButterflyCNN（asym=True，非对称门 + λ·排列敏感正则）
- λ_grid = [0.01, 0.1, 1.0]
- Go = E2 mean fixed_ber < L0 + ≥4/5 胜 + p<0.05 + mean<0.2

**[待 E2 结果填]**：L0 baseline 5/5 clean-swap（fixed≈0.4996）已复现。E2 λ 扫描结果待跑完。

### D-补. E2 MVE 结果（λ≤0.1 已充分证否 KILL，λ=1.0 待 checkpoint 补）

**E2 KILL**（D041）。非对称锚点 + 排列敏感正则对 ML swap **完全无效**：

| variant | λ | seeds | mean fixed BER | swap 率 | 结果 |
|---|---|---|---|---|---|
| L0（标准 ButterflyCNN）| 0 | 5/5 | 0.4996 | 5/5 clean-swap | 复现 prompt024 |
| E2（非对称锚点+排列正则）| 0.01 | 5/5 | 0.4996 | 5/5 clean-swap | 与 L0 完全相同 |
| E2 | 0.1 | 2/5 | 0.4996 | 2/2 clean-swap | 与 L0 完全相同 |
| E2 | 1.0 | 0/5 | — | — | 待 checkpoint 补 |

**核心失败机制（与 D040 同构，第四度证实）**：E2 打破的排列对称不是 swap 真因。swap 真因是 ML 固定权重的 SOP 泛化失败（D015/D040），排列正则在训练段施加但 swap 发生在 test late 段——时序正交。即使 smoke 验证 E2 成功打破排列等变性（|zX(orig)-zY(swap)|=0.35≠0），test 段 SOP 旋转仍让固定权重漂错盆地。

**第四度同构失败链**：D031（A 类 loss 训练段）→ D027 V3（约束训练段）→ D040（D3 MMA 附带发现）→ D041（E2 排列对称训练段）。四度证实"训练阶段修改触及不到 test 段 swap"。→ 后续方法层必须转向 **test 段在线机制**（CMA 在线跟踪优势，D015 N=8M）或 **CSI-aided**（pilot 前置，D037 DEFER）。

## 决策引用

- D040：D3 MMA KILL（无增量）+ standard-CMA z 因子债（本轮新建）
- D041：E2 排列对称破缺 KILL（λ≤0.1 全 clean-swap，本轮新建）
- D014：SOP 极化串扰是 BER 真因
- D018：双口径强制（fixed/PI 并报）
- D030：方法层解冻 + 归类批量 + 消融可验
- D031：A 类 KILL（时序正交）— D040/D041 第四度同构证实
- S033 不变量 9/10/11：swap 物理现象 / PI 失明 / D022 仅 PI 口径

## 范围确认

- 本轮是否在 scope boundary 内：是（S033 §F Tier 1 执行，两独立方向）
- 无范围变更

## 后续

**本轮产出**：
- prompt032_d3_mma_mve.py + prompt032_d3_mma_mve.json（D3 MMA 完成）
- prompt033_e2_perm_symmetry_break_mve.py + prompt033_ckpt.json（E2 跑中）
- D040 已落库（D3 MMA KILL + z 因子债）
- S035 本文档

**待办（交主控）**：
1. E2 结果出来后落 D041 + 填 S035 §D
2. **standard-CMA z 因子债**：主控复查 prompt030/S033 是否应用 standard-CMA 重跑，确认 S033 不变量 9 是否需修正
3. 更新 topic-index 进展线索 + 当前位置

**守纪律**：守 FR-22（每方向 GW Step 1 检索防撞车）+ D030（消融可验）+ D018（双口径）+ S033 不变量 9/10/11 + 铁律 #2（fixed-label BER 作 Go 判据）+ 铁律 #3（correlation 分类口径）。
