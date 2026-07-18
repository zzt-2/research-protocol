# [R014] A1+ 新参数小切片诊断

> 2026-07-15 | 关联：2026-07-14-ccisp-content-expansion / D016 / T016

## 调研问题

先以原始文献和确定性复算闭合 A1+ 五档 Gamma--Gamma 参数证据链；仅在 Osborn 30°/10° plane-wave 锚点均以不超过 5% 的相对误差复现后，运行 old-vs-new 3-seed diagnostic probe，并核查路线 B 对 A 的 45/45 bit-exact 等价。

## 发现

### 1. P0 定义卡与证据门

| 项目 | T016 要求 | 本轮 fresh 证据 | 判定 |
|---|---|---|---|
| Al-Habash plane/spherical GG mapping | 原论文页码、公式号、wave type 与适用边界 | `papers/index.json:2066-2074` 为 `status: failed`；`papers/doi/10.1117_1.1386641/metadata.json` 为 `download_status: failed`、`content_file: ""` | BLOCKED |
| Ghassemlooy Family 1 | 本地全文核对三档表及物理条件 | `papers/index.json` 无 DOI `10.1201/9781315151724` 条目；仓库无该书全文 | BLOCKED |
| Osborn plane-wave 锚点 | Table 6、1550 nm、HV5/7、30°/10°数值与定义 | 仓库无 DOI `10.1364/OE.413013` 全文；仅 `papers/doi/10.1364_oe.498562/content.md:386` 的参考文献条目及 `R008b:56-62` 二手记录 | BLOCKED |
| Kaushal spherical-wave uplink 积分 | 原公式号、积分边界、几何与单位 | 仓库无 DOI `10.1109/COMST.2016.2603518` 全文；只有引用和 `R008b:64` 二手公式 | BLOCKED |

本地 `毕设/formulas-master.md:337-345,369-400` 有水平路径 Rytov、HV profile 和带孔径参数的映射摘要，但来源与 T016 指定的四篇原文不同，且不能补齐 Osborn 的路径边界、Table 6 输入和 Kaushal 公式号。按 T016 §1.6，未读到全文的来源不得承担精确公式或数值；二手的“VERIFIED”标签不能替代本轮原文读取。

因此本轮不能合法填写 Osborn/Kaushal 定义卡中的积分上下限、发射/接收高度、孔径/点接收假设和原论文页码/公式号，也不能构造 5% 复现试验。Osborn 二手记录明确把表值称为 plane-wave/downlink，不能改称“上行实测值”。

### 2. 下行 Family 1 确定性复算

以下仅复算 T016 已冻结的 plane-wave 公式，不把二手来源升级为 fresh 原文证据：

\[
\alpha=\left[\exp\!\left(\frac{0.49x}{(1+1.11x^{6/5})^{7/6}}\right)-1\right]^{-1},\quad
\beta=\left[\exp\!\left(\frac{0.51x}{(1+0.69x^{6/5})^{5/6}}\right)-1\right]^{-1},
\]

其中 \(x=\sigma_R^2\)。对 unit-mean Gamma--Gamma，\(E[I]=1\)，\(\mathrm{Var}(I)=\sigma_I^2=1/\alpha+1/\beta+1/(\alpha\beta)\)。

| 档位 | \(\sigma_R^2\) | 未舍入 \(\alpha\) | 未舍入 \(\beta\) | 展示值 | \(\sigma_I^2\) |
|---|---:|---:|---:|---:|---:|
| downlink weak | 0.2 | 11.65104537862684 | 10.122365306725285 | (11.65, 10.12) | 0.1930995126918106 |
| downlink moderate | 1.6 | 4.026521312058279 | 1.9105223344570113 | (4.03, 1.91) | 0.9017627797163633 |
| downlink strong | 3.5 | 4.2256713509586925 | 1.3621952523122576 | (4.23, 1.36) | 1.1444839781738845 |

三档均有 \(\alpha>0,\beta>0\)，且按 GG variance 的严重度为 weak < moderate < strong。strong 点属于强起伏区；Al-Habash 原文对强区拟合的 caveat 因全文缺失，本轮不能 fresh 核对，只保留二手风险标记。

### 3. Osborn 复现与 A1+ 上行两档

| 项目 | 要求 | 结果 |
|---|---|---|
| 30° plane-wave 锚点 | 相对误差 ≤5% | NOT RUN：缺原文公式、HV 常数和路径边界 |
| 10° plane-wave 锚点 | 相对误差 ≤5% | NOT RUN：同上 |
| 积分收敛性 | 网格/容差收敛证据 | NOT RUN：没有合法被积式和边界 |
| uplink moderate spherical \(\sigma_R^2,(\alpha,\beta)\) | P0 后推导 | NOT AUTHORIZED FOR SIMULATION：证据输入未归档，尚未执行复算 |
| uplink strong spherical \(\sigma_R^2,(\alpha,\beta)\) | P0 后推导 | NOT AUTHORIZED FOR SIMULATION：证据输入未归档，尚未执行复算 |

五档候选因此只能给出三档下行确定性复算。两档上行的准确状态是：**当前没有通过 T016 证据门、获准进入仿真的候选值**。这不表示数学上算不出 \((\alpha,\beta)\)，也不表示 A1+ 被证伪、上行模型不可行或新参数效果不好；本轮压根没有执行上行参数复算和 BER probe。不得回流 A2/A3，也不得用 R008b 的示例 0.2/1.5 代替 spherical-wave 推导。

### 4. P1 old-vs-new 诊断矩阵

未运行。用户和 T016 均规定“复算通过后才运行 old-vs-new”；P0 未闭合，因此未生成 probe script、probe JSON、B receiver 结果或 verifier 报告。没有 uplink BER 被产生。

### 5. 六个诊断触发器

| # | 触发器 | 状态 | 说明 |
|---:|---|---|---|
| 1 | B/A 非 45/45 bit-exact | NOT EVALUATED | P1 未运行 |
| 2 | selector 每 cell 单分支均 ≥99% | NOT EVALUATED | P1 未运行 |
| 3 | 15 个下行 cell 的 fixed winner 完全不变 | NOT EVALUATED | P1 未运行 |
| 4 | 至少 8/15 cell selected-vs-fixed-NDA pooled gain 非正 | NOT EVALUATED | P1 未运行 |
| 5 | 核心方向反转、NaN、负参数或 metric-signature 漂移 | NOT EVALUATED | 未生成新结果；下行复算无负参数/NaN，但不足以评价 BER 方向 |
| 6 | uplink P0 未过却仍产生 uplink BER | NOT HIT | P0 未过，且已按门禁停止，没有产生 uplink BER |

六个 P1 诊断触发器中没有“命中”；其中 1--5 是未评估，不是 PASS。阻断正式重跑的直接原因是更早的 P0 证据门失败。

### 6. 实现真相三联卡

```yaml
information_access:
  status: NOT_EXECUTED
  frozen_fact: NDA ambiguity resolution would use tx_bits only as post-hoc evaluation
  online_claim_allowed: false
metric_signature:
  status: NOT_EXECUTED
  intended_population: common-768 non-pilot bits per 256-symbol window
  intended_grid: 5 SNR x 3 seeds x 400 windows
state_lifecycle:
  status: NOT_EXECUTED
  intended_scope: one deterministic shared realization per scene/SNR/seed/window identity
```

### 7. 保留、失效与下一轮前提

- 保留：D016 的路线 B 目标架构；旧参数 V011 的 990/990 历史等价证据；selector、CV、1.10 margin、13 dB、CPR、消歧和 common-768 指标签名的冻结要求。
- 保留：下行 Family 1 三个输入点的确定性数值复算，但其文献来源状态仍是“待本地原文核对”。
- 失效/未建立：A1+ 上行两档、Osborn 5% 复现、old-vs-new 方向、45/45 新参数等价、selector 互补性和 selected-vs-fixed-NDA 方向。
- 下一轮最低前提：先将四个指定来源的可读全文纳入 `papers/` 正规索引；核对原公式号和输入后重做 P0。只有两锚点均 ≤5% 才能设计正式 probe；仍不得自动进入 30-seed。
- 若未来 P1 通过，正式全量合同至少需要独立的 A-style 双分支 evaluator、B branch-routed receiver、新参数注入/真相源方案和从原始 JSON 重算的 verifier。

## 结论

**PARTIAL**。

P0 未闭合：下行三档完成确定性复算，但四项指定本地全文缺失，Osborn plane-wave 锚点无法复现，上行 spherical-wave 两档尚未执行复算、未获准进入仿真。阻断对象是当前证据链和执行授权，不是 A1+ 参数路线。因“复算通过后才运行”的硬门，P1 未运行；应先补齐原始文献落盘并只重做 P0。

## 对决策的影响

- D016 的 A1+ 目标方向不被推翻；当前只因一手证据未归档而暂停 P0，正式参数替换与全量重跑暂未获准。
- 根因分类为 M1 管道断裂：上游子 Agent 的“已读/VERIFIED”结论没有连同原文、页码、公式号和路径边界落盘，违反 FR-26 的证据指针要求；R014 的停止动作正确。
- 不新建 D###：本轮是 T016 预注册门禁按预期中断，没有提出替代路线，也没有形成新参数决策。
- 不修改 `params.py`、论文、图片、Skill、旧权威 JSON、原 A/B runner 或 `common/`。
