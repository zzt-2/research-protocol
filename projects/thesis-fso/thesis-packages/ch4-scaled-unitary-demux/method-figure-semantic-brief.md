# Method figure semantic brief

## Figure claim

该图只解释“短平衡导频如何产生缩放酉 2×2 偏振信道估计、如何控制 payload 解复用，以及两路解复用输出如何进入 Ch3 CPR”。它不表示 PDL/PMD/FIR/LDPC 或 CPR 与本方法已联合验证。

## 冻结标签

- 双偏振接收块 `[r_x,r_y]^T`
- 短平衡导频 `X_p,Y_p`
- 双偏振载荷 `y=[y_x,y_y]^T`
- pilot-LS `H_LS`
- `H_LS=UΣV^H`
- `g_hat=(s1+s2)/2`
- `H_SU=g_hat UV^H`
- `rho=s1/s2`（仅适用性诊断）
- 逆矩阵解复用 `W=VU^H/g_hat, z=Wy`
- Ch3 CPR X 路 / Y 路
- `s_hat_x, s_hat_y`
- 目标验证场景：静态 2×2 酉混合 + 公共尺度

任何生成或局部修订不得改写这些标签的技术含义。

## Layout spec

- 画布：约 1100×510 比例，论文/学位论文紧凑横图，不使用 slide banner。
- 上区：低饱和橙色，表示短导频估计和参数控制。
- 下区：低饱和蓝色，表示载荷数据流。
- 左→右阅读：接收块分流；导频经 LS、SVD/投影产生 `W`；payload 由 `W` 解复用；两路分别进入 Ch3 CPR。
- 橙色点划箭头=导频估计/参数控制；蓝色实线=payload 数据流。颜色与线型双编码，保证黑白可区分。
- 容器仅表示流程区域；不添加矩阵/星座/icon miniature，避免暗示未验证机制。

## Arrow contract

| source | target | meaning | encoding |
|---|---|---|---|
| 双偏振接收块 | 短平衡导频 | 提取 receiver-known pilot observations | 橙色点划 |
| 双偏振接收块 | 双偏振载荷 | payload observations | 蓝色实线 |
| 短平衡导频 | pilot-LS | pilot data | 橙色点划 |
| pilot-LS | SVD/缩放酉投影 | 2×2 LS estimate | 橙色点划 |
| SVD/缩放酉投影 | 逆矩阵解复用 | 估计的 demux matrix `W` | 橙色点划 |
| 双偏振载荷 | 逆矩阵解复用 | payload data | 蓝色实线 |
| 逆矩阵解复用 | 两个 Ch3 CPR | 两路 demultiplexed streams | 蓝色实线分支 |

## Evidence and exclusions

- 语义来源：`scaled_unitary.py:32-88`、`development.py:125-182`、D052/T073。
- 两路 Ch3 CPR 是章节间接口，不是本 confirmation 中启用的损伤模块；图内明确画在 C4 demux 之后。
- 禁止画 PDL、PMD、FIR、LDPC、时变 SOP、CFO 或运行时 `rho` gate。
- 非文字 primitive：仅用中性框、区域和箭头，无需领域 icon；符合 Semantic Primitive Evidence Gate。
