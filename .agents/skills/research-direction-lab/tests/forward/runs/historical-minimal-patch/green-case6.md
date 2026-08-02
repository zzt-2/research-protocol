# GREEN Case 6 — contribution packaging

> fresh context, read-only, raw adjudication reproduced verbatim below

## 原始裁决

### 1. `THESIS_MAIN_METHOD`

- **冻结的 DA/NDA CPR 窗口级选择器**是当前唯一可用的主方法故事，但它是继承的既有方法，不是本轮 campaign 新产出的 METHOD_SIGNAL。
- 可写范围应冻结为：`(8,8)-16APSK + common-768 + 5–13 dB 增益区间 + 名义/可估 SNR`。P01 重现的典型增益约 `+0.79～+1.56 dB`。
- 不得把 `cand_rank`、G1、P09-C3 或 P11 包装成第二主方法：
  - `cand_rank` 被 P02 的常规区域阈值重调完全解释；
  - G1 被终态判为固定阈值判决器的 scale artifact；
  - P09-C3 是执行无效和冗余计算少报；
  - P11 被降级为 9–15 dB 局部 baseline 资产。

### 2. `THESIS_ENGINEERING_COMPONENT`

主工程组件：

- **P03：选择器控制路径的 bit-true 定点实现与精度选型。**
  - 推荐统一 `Q(8,6)`：增益承载区相对 float 的 regret 约 `0.027 dB`，继续加宽至 `Q(16,14)` 仅改善 `0.0047 dB`；
  - 可声称“在当前实现范围内，以更低位宽保持选择器主要性能”；
  - 资源只能写 `op×bit/storage proxy`，不能写 FPGA 面积、功耗或时延收益。
- **P01/P02：接收机可见的 SNR 适配与区域标定协议**可作为上述组件的部署子模块，而非独立创新：
  - pilot-SNR adapter 对 `±3 dB` 名义 SNR 偏差不敏感，在全部已确认 harm cell 相对失配原方法均改善，并按严格标准解决 4/5；
  - weak/low-SNR 的额外收益由常规区域阈值重调解释，因此应写成校准规则，不写新算法。

### 3. `SUPPORTING_MATERIAL`

- P01/P02：SNR 偏差边界、估计偏差下限、区域重调足够性。
- P04：连续 Gamma-Gamma 内插并未形成 OOD 特有失效；弱湍流低 SNR 的 over-NDA-selection 是局部边界。
- P05：fixed-label 与 PI-BER 对 polarization swap 的评价差异；正确 Godard-with-z CMA 已解决 ML 在线失配。
- P06：跨帧 history 虽优于 current-only，但远逊于 last-value persistence；作为可观测性边界。
- P07-R：ADC/AGC 的 scale、控制递推和 trajectory 生命周期教训；静态低增益已解决问题。
- P08-R2：5G NR LDPC/BICM corrected-chain、receiver-visible 信息门和 LLR 校准负面；只保留最终修复谱系，P08/P08-R 不重复计数。
- P10：ML/CMA 单专家 crossover 不成立，router 无问题基础。
- P11：仅保留 linear Butterfly FIR 身份、1% pilot complex-LS 的 9–15 dB 局部数据和公平 pilot 合同。
- P09：仅保留“真实计算路径、调制对称冗余、paired MDE”方法论教训，所有正向数字禁用。
- G1 两份 harvest/thesis insert 已被 step-042 的 scale-artifact 裁决取代，不能继续作为正向论文材料。

### 4. `ACTIVE_CARRIER`

- **无。**
- `cand_rank`、`two_exp`、P09-C3、G1、P11 均不满足 carrier 条件；不得靠改名重开。
- 继承的 DA/NDA selector 已是完成态主方法锚点，不属于 active carrier。

### 5. Campaign 裁决

- **应停止本轮 campaign，不再开一个探索包。**
- “7/10”只是覆盖计数，不是继续执行的科学理由；当前不存在证据支持的 active carrier，新增一包只会为了补数量而工作。
- 毕业组合已经具备最小可用结构：
  `DA/NDA CPR selector 主方法 + P03 定点实现主工程组件 + P01/P02 部署校准 + P04/P05/P06/P07-R/P08-R2/P11 边界与实现证据`。
- 若外部要求“主方法必须由本 campaign 新产生”，则当前结论应是**战略性方法短缺**，需要重新选研究问题，而不是自动追加 P12。

### 6. 下一合法动作

进入**论文组合固化/方法卡整理**，不再实验：

1. 为继承的 DA/NDA selector 冻结一张主方法卡，明确 nominal-SNR、调制、SNR 区间和 weak/low-SNR 限制。
2. 为 P03 冻结一张工程组件卡，主结论限定为 bit-true `Q(8,6)` 精度—性能折中。
3. 将 P01/P02/P04 合并为同一选择器谱系的鲁棒性与适用边界，避免拆成多个贡献。
4. 清除 G1、P09 的正向声称，并按 step-042 降级 P11 表述。
