# 第四章评阅与答辩问题卡

本文件只提供“问题—回答证据—材料指针”，不提供逐字答辩稿。

## 方法定位

### 1. 本章到底解决什么问题？

- 短导频条件下，无约束 2×2 LS 的奇异方向和尺度都会受噪声扰动，直接求逆容易放大估计误差。
- 目标信道近似具有“公共尺度 × 酉方向”结构，可将方向与尺度分开处理。
- 指针：`chapter-blueprint.md` 4.1；`fact-matrix.md` M01–M04。

### 2. 方法的独立技术动作是什么？

- 从 LS 估计的 SVD 中提取 $Q=UV^H$，把方向约束到酉流形。
- 分别用信道域前向误差和接收导频重构确定尺度，再构造解复用矩阵。
- 指针：`algorithm-box.md`；`figures/ch4-method-flow.svg`。

### 3. 这是否只是普通极分解的重命名？

- 方向提取本身属于经典矩阵近似工具，不应包装成全新数学定理。
- 章级方法身份来自该工具在短导频双偏振星地接收场景中的完整输入—动作—输出链、尺度判据、基线和边界证据。
- 指针：`claim-and-citation-ledger.md` 的允许主张与引用层级。

### 4. 两种尺度判据是不是两个独立创新？

- 不是。二者共享同一方向—尺度解耦主体。
- 前向误差尺度是正文主方法；导频重构尺度是接收端可实现的强变体和尺度判据消融。
- 指针：`tables/ch4-method-role-comparison.md`；`fact-matrix.md` M05–M07。

## 公平性与基线

### 5. 为什么把调参奇异值下限作为主要基线？

- 它与主方法共享同一 LS/SVD 输入，能直接检验“结构方向 + 尺度处理”是否优于常见的奇异值稳定化。
- 参数按场景和导频切片独立确定，不使用一个统一值替代全部正式结果。
- 指针：`tables/ch4-formal-configuration.md`；`algorithm-box.md` 的基线卡。

### 6. 调参映射是否对主方法不公平？

- 基线参数在对应切片上独立选取；主方法不使用经验调参。
- 所有方法共享同一信道、导频噪声、载荷噪声和配对随机簇。
- 指针：`tables/ch4-formal-configuration.md`；`formal-figure-table-verification.md`。

### 7. 理想 CSI 为什么不算主要基线？

- 理想 CSI 使用仿真真值，接收端不可获得，只表示估计误差消除后的参考空间。
- 可部署方法之间的主要比较是普通 LS、调参奇异值下限和两种结构尺度判据。
- 指针：`tables/ch4-method-role-comparison.md`。

## 数值与机理

### 8. 最有分量的数值结果是什么？

- 中等湍流、$N_p=2$ 时，前向误差尺度相对调参基线的所需 SNR 降低为 0.8705 dB，95% 置信区间为 [0.6182, 1.0883] dB。
- 同条件下导频重构尺度为 0.8747 dB，[0.6289, 1.0784] dB。
- 指针：`tables/ch4-formal-headline-results.md`；`figures/ch4-formal-required-snr-gain.svg`。

### 9. 为什么 $N_p=4$ 时改善很小？

- 导频增加后，无约束估计和调参基线的估计噪声下降，结构先验的边际价值自然缩小。
- 结果仍是统计稳定的小幅优势，不应夸大为工程显著跃升。
- 指针：`figures/ch4-formal-ber-curves.svg`；`figures/ch4-formal-pilot-sensitivity.svg`。

### 10. 为什么 BER 图仍需要完整 SNR 区间？

- 完整曲线显示低 SNR 噪声主导区、工程阈值附近的差异和高 SNR 区的收敛/误码地板，避免只展示两个有利点。
- 所需 SNR 是从完整 BER 曲线在 $3.8\times10^{-3}$ 处插值得到，而不是单点换算。
- 指针：`figures/ch4-formal-ber-curves.svg`；`fact-matrix.md` E01–E04。

### 11. 结构约束为什么能改善 BER？

- 方向投影减少了与目标模型不一致的自由度，尺度处理降低了病态求逆导致的噪声放大。
- 信道 NMSE 与求逆残差只用于支持该解释，不单独证明普遍因果。
- 指针：`figures/ch4-formal-mechanism.svg`；`algorithm-box.md`。

### 12. 为什么不比较导频重构支路的信道 NMSE？

- 该实现返回的信道估计量是校准前继承量；真正被校准的是解复用矩阵。
- 将继承量写成该支路自身的估计结果会造成证据口径错误。
- 指针：`fact-matrix.md` M07、E08；`claim-and-citation-ledger.md` 的禁止主张。

## 适用边界与跨章关系

### 13. 非酉失配扫描说明了什么？

- 在冻结定义下，$\delta\ge 0.1$ 时结构约束方法的排序发生反转，说明强结构先验并非无条件有利。
- $\delta$ 是无量纲结构失配强度，不等同于 PDL 的 dB 值。
- 指针：`figures/ch4-formal-robustness-boundary.svg`；`fact-matrix.md` E09–E10。

### 14. 为什么不声称对 PDL、PMD 或时变 SOP 鲁棒？

- 正式证据没有联合启用这些损伤，当前结果只覆盖冻结的静态 2×2 目标场景及定义明确的失配扫描。
- 未验证项列为后续工作，不从已有数据外推。
- 指针：`claim-and-citation-ledger.md` 的禁止主张；`tables/ch4-formal-configuration.md`。

### 15. 第四章与第三章如何衔接？

- 物理处理顺序是先完成双偏振解复用，再由每个偏振支路执行载波相位恢复。
- 当前只验证模块接口，没有做第三、四章方法的联合仿真，也不改写第三章原有证据场景。
- 指针：`thesis-spine-integration-notes.md`；`figures/ch4-method-flow.svg`。

### 16. 方法是否适合工程实现？

- 核心是固定维度 2×2 LS、SVD 和闭式标量运算，不需要迭代优化或训练。
- 工程适用性仍受信道结构匹配程度影响；可用奇异值比和残差作为离线诊断，但现有证据不支持在线自动切换。
- 指针：`algorithm-box.md` 的复杂度与失效处理卡；`fact-matrix.md` M10–M11。
