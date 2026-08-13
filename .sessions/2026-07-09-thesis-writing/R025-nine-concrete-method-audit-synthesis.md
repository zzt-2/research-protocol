# [R025] 九个具体方法逐项审计综合

> 2026-08-13 | 关联：2026-07-09-thesis-writing / D032 / D033

## 调研问题

按“相对正确 baseline 有真实改善，完整 recipe 非完全相同即可”的硕士级标准，九个本地已有对象到底是不是具体方法，各自能诚实写到哪一层。

## 发现

### 总判断

九项中，八项具有可命名的具体 recipe；P06 也有预测 recipe，但当前输入是 truth-scored 既往 SER，不能承担 receiver-visible 部署方法。此前“没有第二方法”的主要成因不是资产为空，而是把经典迁移、参数校准、执行架构和数值格式提前按期刊级方法独立性否决。

| 顺位 | 具体方法 | 相对 baseline 的真实差别与结果 | 当前判断 |
|---|---|---|---|
| 1 | CCISP | 每窗接收功率 CV＋盲有效 SNR 代理选择 DA/NDA；9 dB 三档下行 GG 相对 fixed NDA 的 common-payload BER-ratio 改善 `0.832–1.496 dB` | `DIRECTLY_PACKAGABLE` |
| 2 | CCISP select-before-execute | 将既有 command 前移为互斥分支执行门；396,000 窗输出/BER 零差异，分支调用减半，软件时延比 `0.5424` | `DIRECTLY_PACKAGABLE`，仅软件/operation，不外推 FPGA PPA |
| 3 | P01 Pilot-SNR-Calibrated CCISP | 用每窗导频 SNR 估计替换 nominal SNR；五个失配受损点相对失配原 CCISP 均正改善，按冻结门恢复 4/5 | `PACKAGABLE_WITH_CAVEAT` |
| 4 | P02 Low-SNR Reference-Calibrated CCISP | dev 将 stage-1 全局参考点从 9 校准为 11 dB；目标 slice 相对 pilot adapter `+0.4539 dB`，相对 ref=9 `+0.0961 dB` | bounded scenario calibration method |
| 5 | P11 Pilot-Efficient Complex-LS Butterfly FIR | 相同 2×2 11-tap 线性 FIR：50% 标签 Adam 改为 1% 导频闭式 LS；固定 20 dB BER `3.85875e-4→3.17625e-4`，BER CI 跨零，goodput 约 `1.98x` | 具体方法成立；仅局部证据，确认实验 `NOT_RUN`，CMA 吸收 `UNRESOLVED` |
| 6 | P03 Finite-Word-Length CCISP Selector | 浮点控制路径映射到 block-floating Q-format；Q(8,6) gain-bearing regret 约 `0.027 dB`，相对 16-bit 有字长/proxy 降低 | 数值精度方法可包装；无 FPGA PPA |
| 7 | P05 Fixed-Stream-Label Online CMA Receiver | 强 GG/SOP FSO 中用独立在线 CMA 替换 frozen ButterflyCNN；fixed-label BER 约 `0.4992→1.76e-4/1.17e-3`，PI-BER无稳定优势 | 改名限缩后收录；不是 Butterfly continuation |
| 8 | P08-R2 Prefix-Calibrated Decoder-Tuned Coded FSO Receiver | corrected prefix receiver 上增加冻结 LLR clip＋normalized offset-min-sum 调参；单 slice FER `0.1547→0.1484` | `PACKAGABLE_WITH_CAVEAT`，探索性局部结果 |
| 9 | P06 Cross-Frame Last-Value Persistence Predictor | 上一帧 truth-scored SER 预测下一帧 SER；`R²=0.853`，history ridge `0.320` | 只作离线预测/可观测性方法；不能称部署方法或 BER 改善 |

### 关键纠错

1. P11 的 corrected confirmation 从未运行；两个重复对话都在实验前因 candidate-specific authority 缺失停止。不能写科学失败、CMA 已吸收或实验无效。
2. P05 不是从 Butterfly 权重继续训练或串接 CMA；它是对原始 RX 独立运行的标准 CMA 接收机。旧名必须废止。
3. P03 的 `0/132,000 mismatch` 属于 Q(64,40) float-bypass，不属于 Q(8,6)。Q(8,6) 全网格 agreement 约 `48.69%`、pooled regret `0.2005 dB`；正面事实仅是 gain-bearing 区 regret 约 `0.027 dB`及字长/proxy 优势。
4. P08-R2 的 B0 已含 prefix-LS；B2 的增益来自完整 decoder-tuned recipe，不能单独归因 prefix-LS。

### 对论文结构的直接含义

最稳妥 spine 不是继续找第二个“全新科学主方法”，而是：

- Ch3：CCISP 核心自适应 CPR 方法；
- Ch4：CCISP 场景鲁棒扩展，主方法 P01，P02 作为低 SNR 校准子方法/对照；
- Ch5：CCISP 执行与有限字长实现，主方法 select-before-execute，P03 作为数值格式子方法。

这条 spine 至少包含 CCISP、P01/P02、select-before-execute、P03 四个可命名动作，且主题同源、现有证据最多。P11/P05 可作为更独立但证据较弱的备选 Ch4；P08-R2、P06 更适合作补充或后备，不宜优先承重。

## 结论

当前没有继续盲找候选的事实依据。真实问题是方法身份 gate 过严和汇总方式错误：经典算法的场景迁移、小参数校准、控制流程前移、数值格式设计被先验当作“supporting/negative”，从而把至少八个具体 recipe 汇报成“没有方法”。

本轮没有检查任何外部完全重复，九项外部状态均为 `NOT_CHECKED_IN_THIS_READ_ONLY_AUDIT`。这不否定本地方法身份，只表示恢复执行后仍需对最终承重对象做一次 bounded exact-recipe collision check。

## 对决策的影响

D032 得到九项逐项事实支持；D033 完成。暂不新建 thesis spine 决策，等待用户确认是否采用推荐结构及是否恢复任何执行。
