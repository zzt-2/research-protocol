# [S033] 方法层再探索 Tier 0 执行 — B2 非对称功率 KILL + H1 翻转标签确认（trivial）+ 检索批次 1

> 2026-07-16 | GW/Contract 方法层 | 状态：Tier 0 完成，待主控定 Tier 1 走向
> （承接 S032 统一规划。本轮为执行 agent，按 S032 §F 执行图跑 Tier 0 物理前提 MVE + 检索批次 1）

## 目标

按 S032 §F 执行图，跑 Tier 0 两个物理前提 MVE（B2 非对称功率 + H1 CRC 翻转标签），并行派 5 个方向检索批次 1。Tier 0 结论是开关：任一 Go → 围绕展开 Tier 1；全 KILL → 进 Tier 2。

## 记录

### A. 范围拍板（用户）

F1（电控偏振跟踪，硬件层）/ G2（HARQ swap 段重传，协议层）**排除**。理由：F1 撞车重（光纤 PMD 电控偏振跟踪成熟标配）+ 仿真器无 EPC 模型无法 MVE；G2 物理上对永久锁定 swap 无效（D028 swap 一次性永久锁定，SOP 不变重传还错）+ 属协议层。聚焦软件方法层 A-E+H。

### B. 关键事实校正（TL-22 触发，决定 Tier 0 设计）

H1/B2 smoke 初版用 CMA standard 测，得 5/5 clean（0 swap）——与 D028 报的 swap 矛盾。深查发现：
- **swap 载体 = ML fixed-weight**（D015/D018：N=5M late clean-swap），**不是 CMA**
- CMA standard 在新参数域 strong=4.2/1.4 下 5/5 clean（在线跟踪跟上 SOP，0 swap）
- D028 报的 2/5 swap（seed 1000/1003）是**旧参数域 1.5/0.8**（D036 确认），新域 4.2/1.4 下 CMA 不 swap

→ H1/B2 MVE 改为测 **ML fixed-weight**（swap 真正载体）。prompt025 的"swap 5/5"是 ML L0 输出（mean_fixed=0.4996），非 CMA。S032 §A 表格"prompt025 用新参数 swap 5/5"指 ML，本轮澄清。

### C. Tier 0-B2 非对称功率分配 — KILL（D038）

**假设**（S032 §C）：非对称功率（p_X≠p_Y）破坏 CMA 恒模代价 X/Y 对称 → swap 多解消失（治本）。

**MVE**（prompt029_b2_asymmetric_power.py，5 功率比 [0.25,0.5,1.0,2.0,4.0] × 5 seeds × ML+CMA+oracle，22/25 trials，pr=4.0 被 tool timeout 截断但模式一致）：

| power_ratio | ML swap_rate | ML fixed | CMA swap_rate | CMA fixed | oracle BER |
|---|---|---|---|---|---|
| 0.25 | **100%** | 0.4887 | 0% | 0.213（退化）| 0.0360 |
| 0.5 | **100%** | 0.4987 | 0% | 0.0008 | 0.0019 |
| 1.0（基线）| **100%** | 0.4996 | 0% | 4e-5 | 3.5e-5 |
| 2.0 | **100%** | 0.4987 | 0% | 0.0008 | 0.0019 |
| 4.0 | **100%** | 0.4841 | 0% | 0.263（退化）| 0.0358 |

**KILL 根因**：
1. **ML swap_rate=100% 恒定**，非对称功率完全不影响 ML swap。B2 机制（恒模盆地）只对 CMA 成立，但 ML swap 根因是 SOP 泛化（D015：test late 57° 超训练域），与功率对称正交。机制错配（同 D031/D027 同构）。
2. **CMA 在 4.2/1.4 域本就不 swap**（0%），无 swap 可防。
3. **极端功率比伤 BER**：oracle BER 从 3.5e-5@1.0 恶化到 0.036@0.25（弱流 SNR 降 6dB），CMA BER 退化到 0.21-0.29（单 R²=1.0 对非对称两流错配）。BER 代价不可接受。

→ **机制 B 整体倾向 KILL**（B2 是最强治本候选，KILL 后 B1/B5/B7 同根因风险高）。

### D. Tier 0-H1 CRC 翻转标签 — 机制确认（trivial Go，D039）

**假设**（S032 §C H1）：swap 后 CRC 检测 BER 突变 → 翻 X/Y 标签 → BER 恢复，开销≈0。

**MVE**（prompt029_h1_crc_flip_label.py，5 seeds × ML fixed-weight late，fixed/flip/PI/oracle 四口径）：

| | fixed BER | flip BER | PI BER | oracle BER |
|---|---|---|---|---|
| mean（5/5 clean_swap）| **0.4996** | **8.936e-5** | **8.936e-5** | **3.528e-5** |

翻标签恢复 **5591×**（fixed→flip），flip BER = PI BER ≈ oracle。

**结论：H1 机制有效但 trivial**。翻标签 = 选最优排列 = D018 已确立的 PI-BER。H1 没有新方法贡献，只是确认 clean-swap 可被翻标签+4旋转恢复（D018 已证）。**0 degraded-swap**（5/5 全 clean，比 D018 报的 8/10 更干净）。

**S032 §C H1 风险（swap 伴随相位/权重偏移）未触发**：flip BER 含 4 旋转校正后≈oracle，clean-swap 无残余相位偏移。

### E. 检索批次 1（5 方向，0 硬撞车）

| 方向 | 查询/命中 | 硬撞车 | 最邻近 | 撞车判据 |
|---|---|---|---|---|
| B2 非对称功率 | 4/59 | NO | Fan 2023（功率不平衡=损伤，方向相反）| PASS |
| B1 非对称调制 | 4/60 | NO | Lau 2014 spectral asymmetry（谱形非阶数）| PASS |
| H1 CRC 翻转 | 4/63 | NO | **Le Bidan 2023（强邻近，须区分）**| PASS |
| E2 排列等变 | 4/18 | NO | RE-MIMO 2020（RF MIMO，借源）| PASS |
| D3 MMA | 5/71 | NO | 2022 singularity-rate（漏测 MMA）+ 2015 Kalman（定性称 MMA=CMA singularity，须实验对冲）| PASS |

JSON 全部落盘 `search-archive/2026-07-15/`。5 方向撞车维度全 PASS，但因 B2 MVE FAIL 不进 Tier 1。

**两个需注意的邻近点**：
- **Le Bidan 2023**（H1）：同场景（GEO 卫星相干光 PolMUX）+ 同问题（盲均衡器 X/Y 模糊），但用帧头静态识别 vs H1 CRC 运行时检测。论文须引用区分。
- **2015 Kalman 论文**（D3）：定性声称"MMA 与 CMA 同样有 singularity 问题"——若 D3 进 MVE，须用触发率数据正面对冲此论断。

### F. Tier 0 结论与 Tier 1 决策（待主控）

S032 §F 规则："Tier 0 任一 Go → 围绕展开 Tier 1；全 KILL → Tier 2"。本轮：
- B2 KILL（D038）
- H1 trivial Go（机制有效但=PI-BER，非新方法，D039）

**H1 的 Go 是 trivial**，不构成"围绕展开"的新方法空间（翻标签=PI-BER 已是 D018 结论）。**Tier 1 走向须主控重判**，选项：

1. **直接进 Tier 1/2 独立方向**（推荐）：跳过"围绕 H1"（无空间），直接跑 E2（排列等变，已检索 PASS）/ D3（MMA，已检索 PASS，须对冲 2015 Kalman）/ E1（群等变，已检索，攻 D031/D015 SOP 泛化痛点）
2. **B1 验证机制 B 整体 Kill**：B1（非对称调制）同构风险高（B2 已证机制 B 对 ML 无效），但跑一个 smoke 确认机制 B 整体关闭
3. **H2/H3 探机制 H**：H1 trivial 但 H2（swap 时刻预测）/ H3（swap 概率纳入 BER 统计模型）未测

**火力重定向信号**（B2 KILL + D031/D027 同构累积）：
- 训练阶段 loss/约束（A 类 D031）+ 预防性约束（D027 V3）+ 非对称功率（B2）→ 都因"swap 是 test 段 ML SOP 泛化，训练段/对称性触及不到"失败
- **最有希望的剩余方向 = E 类架构（群等变/排列等变直接攻 SOP 泛化）+ H 类（接受 swap 让它无害）**

## 决策引用

- D030：方法层解冻 + 归类批量 + 放宽准入（本轮 Tier 0 + 检索守此）
- D014：SOP 极化串扰真因（swap 驱动）
- D015：ML 长序列 SOP 泛化失效（swap 真正根因，本轮 H1/B2 的 swap 目标来源）
- D018：双口径（fixed/PI），本轮 Go 判据用 fixed-label BER（S032 §B PI 失明）
- D027/D028：swap 机制（clean-swap + 永久锁定），H1 翻标签验证基础
- D031：A 类 KILL（训练段 loss 触及不到 test swap）—— B2 同构（非对称触及不到 ML SOP 泛化）
- **D038（新建）**：B2 非对称功率 KILL
- **D039（新建）**：H1 翻标签确认（trivial Go = PI-BER）

## 范围确认

- 本轮是否在 scope boundary 内：是（D030 授权方法层探索；S032 §F Tier 0 是其执行）
- 范围变更：F1/G2 排除（用户拍板，见 A 段）

## 后续

**待主控定 Tier 1 走向**（见 F 段三选项）。我的倾向：**选项 1（直接进 Tier 1/2：E2/D3/E1）**，理由：
1. B2 KILL + D031 同构 → 机制 B（打破对称）对 ML swap 无效已强证据，B1 同构风险高，跑 B1 边际收益低
2. E 类（群等变/排列等变）是唯一**直接攻 SOP 泛化根因**的方向（D015 痛点），最有希望
3. H1 trivial → 机制 H 剩 H2/H3 价值未明，可后置

**关键数据锚点（交主控）**：
- swap 载体 = ML fixed-weight（新参数域 CMA 5/5 clean）—— 后续所有方法层探索基准
- B2 KILL：ML swap_rate 100% 不随功率比，机制 B 倾向整体 KILL
- H1 trivial Go：翻标签=PI-BER，非新方法
- 5 方向检索 0 硬撞车（Le Bidan 2023 / 2015 Kalman 两个须注意邻近点）
