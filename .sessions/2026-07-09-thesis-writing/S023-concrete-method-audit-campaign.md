# [S023] 九个具体方法逐项审计

> 2026-08-13 | 战略讨论 | COMPLETE

## 目标

以 D032 为唯一筛选标准，对九个已有具体方法逐项做独立只读审计，形成可直接比较的方法卡，不恢复实验、Groundwork 或文献检索。

## 记录

审计对象：P01、P11、P05、P08-R2、P02、P06、select-before-execute、P03、CCISP。每项单独一个 T，不允许用 supporting/组件/经典方法等标签跳过具体 recipe。统一输出实际步骤、baseline、数字条件、真实性、最小差别、可写命题和 D032 结论。

三批顺序：

1. T019 P01、T020 P11、T021 P05；
2. T022 P08-R2、T023 P02、T024 P06；
3. T025 select-before-execute、T026 P03、T027 CCISP。

### 第一批回传

- **P01 Pilot-SNR-Calibrated CCISP**：`PACKAGABLE_WITH_CAVEAT`。每窗用 64 个已知导频估计 SNR，并替换原 CCISP 的 nominal SNR 输入；held-out 五个失配受损点相对失配原 CCISP 均为正改善，按冻结的 0.3 dB 恢复门恢复 4/5。不得写全域恢复或无偏估计。
- **P11 Pilot-Efficient Complex-LS Butterfly FIR**：具体 recipe 成立，当前仅有固定 20 dB 局部证据。1% 导频 complex LS 的 BER 为 `3.17625e-4`，50% 标签 Adam 为 `3.85875e-4`，BER 差 CI 跨零；计入导频开销后 goodput 约 `1.98x`。纠正确认实验 `NOT_RUN`，CMA 吸收 `UNRESOLVED`。
- **P05**：旧名 `Online-CMA-Continued Butterfly Equalizer` 不符合动作链。真实 recipe 是“强湍流 FSO/SOP 漂移下的固定流标签在线 CMA 均衡”：标准 CMA 从原始 RX 独立在线均衡，不加载或续接 Butterfly 权重。相对 frozen ButterflyCNN，两个 20 dB cell 的 fixed-label BER 从约 `0.4992` 降至 `1.76e-4/1.17e-3`；PI-BER 无稳定优势。结论为改名限缩后收录。

第一批共同结论：三项都不是“没有方法”。旧流程分别因为局部未全恢复、传统 LS/CMA 解决问题、或动作属于经典方法而将其降成 supporting/negative；按 D032，它们均是可命名的具体 recipe，但证据和命名边界不同。

### 第二批回传

- **P08-R2 Prefix-LS-Calibrated Coded FSO Receiver**：`PACKAGABLE_WITH_CAVEAT`。真正相对 corrected B0 有数字的动作是，在同一 32-symbol prefix residual calibration 链上增加冻结的 LLR clipping 与 normalized offset-min-sum 调参；单一 weak/1000 Hz/12 dB slice 的 FER 从 `0.1547` 降到 `0.1484`，oracle `0.1391`。不得把增益单独归因于 prefix-LS，也不得称 2×2 LS channel identification。
- **P02 Low-SNR Reference-Calibrated CCISP**：可作为 bounded scenario calibration method。用 dev seeds 将 CCISP stage-1 全局参考点从 9 dB 校准并冻结为 11 dB；held-out weak×5/7/9 dB slice 相对 pilot-SNR adapter `+0.4539 dB`，相对 ref=9 `+0.0961 dB`。运行期无区域分类器。
- **P06 Cross-Frame Last-Value Persistence Predictor**：只能修正后有限包装为离线性能状态预测。上一帧 truth-scored SER 直接预测下一帧 SER，test `R²=0.853`，高于 history ridge `0.320`；没有 receiver-visible proxy，也没有下游 BER/控制增益，不能承担完整部署方法。

第二批共同结论：P08-R2 与 P02 是明确的“小动作＋场景化”方法；P06 有方法 recipe 和强预测数字，但因实际输入仍是 truth-scored SER，只能进入分析/预测小节，当前不能冒充部署型接收方法。

### 第三批回传

- **select-before-execute**：`DIRECTLY_PACKAGABLE`。396,000 窗 command、selected output 和 BER 零差异；recovery branch calls 降低 50%，同机软件 caller-path 时延比 `0.5424`。不得外推 FPGA/ASIC PPA。
- **P03 Finite-Word-Length CCISP Selector**：可作为数值精度方法。必须纠正：`0/132,000 mismatch` 属于 Q(64,40) bypass，不属于 Q(8,6)；Q(8,6) 的可写事实是 gain-bearing 区 regret 约 `0.027 dB`及相对 16-bit 的字长/proxy 降低。无 RTL/HLS/FPGA PPA。
- **canonical CCISP**：`DIRECTLY_PACKAGABLE`。权威 headline 仅为 9 dB、三档 downlink GG、相对 fixed NDA、common-payload BER-ratio `0.832–1.496 dB`。

### 主线程综合

九项中八项有可命名的具体方法 recipe；P06 只能作离线预测/可观测性方法。推荐结构是 Ch3 CCISP、Ch4 P01 主方法＋P02 子方法、Ch5 select-before-execute 主方法＋P03 数值格式子方法。P11/P05 是更独立但证据较弱的备选，P08-R2/P06 暂不优先承重。完整横向证据见 R025。

## 决策引用

- D033：九个具体方法逐项只读审计（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。只读审计已有本地证据；不检索、不实验、不补 Groundwork、不修改研究资产。

## 后续

九项逐项只读审计与主线程综合均已完成。等待用户确认论文 spine；在明确确认前不恢复检索、实验、Groundwork 或研究资产修改。
