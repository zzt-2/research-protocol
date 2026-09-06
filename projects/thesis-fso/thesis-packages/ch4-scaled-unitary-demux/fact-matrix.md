# 第四章正式事实矩阵

> 用法：每一行是一张作者材料卡。只从“可写结论”列取句意；同时带上“必须披露”，并服从“禁止外推”。

## A. 方法与实现事实

| ID | 可验证事实 | 权威指针 | 图表入口 | 可写结论 | 必须披露 | 禁止外推 |
|---|---|---|---|---|---|---|
| M01 | 目标切片以 $H\approx gQ$ 描述 2×2 偏振混合，其中 $g>0$、$Q\in U(2)$ | `ch4_formal_raw.json`；`tables/ch4-formal-configuration.md` | `figures/ch4-method-flow.svg` | 目标场景具有“公共尺度 + 酉方向”的低维结构 | 这是冻结目标切片，不是任意偏振信道模型 | 不称适用于全部 PDL/PMD/FIR 信道 |
| M02 | 接收机输入仅含已知导频 $X_p$、接收导频 $Y_p$ 和接收载荷 $Y$ | `production_core.py:407-470` | `tables/ch4-method-role-comparison.md` | 两种结构尺度判据均为 receiver-visible | 真值只进入理论参考和离线评分 | 不把真值信息写入可部署方法 |
| M03 | 普通 LS 为 $\hat H_{LS}=Y_pX_p^H(X_pX_p^H)^{-1}$ | `scaled_unitary.py:44-61` | `algorithm-box.md` | 先以同一短导频获得无约束 2×2 信道估计 | 所有方法共享相同导频观测 | 不把普通 LS 写成本文创新 |
| M04 | 对 $\hat H_{LS}=U\operatorname{diag}(s_1,s_2)V^H$，共同结构方向为 $\hat Q=UV^H$ | `scaled_unitary.py:64-87`；`production_core.py:414-449` | `figures/ch4-method-flow.svg` | 方法族共享由 SVD 提取的酉方向 | 两种结构变体共享方向，只改变尺度判据 | 不把两种变体包装成两个独立核心方法 |
| M05 | 前向误差尺度为 $\hat g_F=(s_1+s_2)/2$，解复用矩阵为 $W_F=\hat Q^H/\hat g_F$ | `scaled_unitary.py:75-87` | `algorithm-box.md`；`figures/ch4-method-flow.svg` | 主变体以前向 Frobenius 误差确定公共尺度，即在信道域最小化到 scaled-unitary 集合的距离 | 该原子属于经典矩阵逼近的场景迁移 | 不称发明 Procrustes、polar 或 unitary projection |
| M06 | 导频重构变体先用 $\tau=1$ 形成 $W_0=\hat Q^H/s_1$，再由当前导频闭式求 $\hat a$ 并令 $W_P=\hat aW_0$ | `production_core.py:387-441` | `algorithm-box.md`；`figures/ch4-method-flow.svg` | 强变体在解复用输出域以导频重构误差标定尺度 | 1.0 是起始奇异值下限参数；$\hat a$ 随观测变化 | 不称“重构尺度固定为 1.0” |
| M07 | 导频重构变体返回的 `h_hat` 是校准前继承量；校准后的证据体现在 $W_P$ 与求逆残差 | `production_core.py:436-470`；`data/ch4-formal-mechanism.csv` | `figures/ch4-formal-mechanism.svg` | 该变体的合法机理指标是尺度校准后的求逆残差 | channel NMSE 不作为其自身估计器证据 | 不用 inherited channel NMSE 证明该变体更准 |
| M08 | 调参奇异值下限方法使用 $\tilde s_i=\max(s_i,\tau s_1)$ 后求逆 | `production_core.py:430-438` | `algorithm-box.md`；`tables/ch4-method-role-comparison.md` | 主对比基线是可部署的奇异值正则化接收机 | 参数由独立调参样本冻结 | 不把它写成未调参或故意偏弱基线 |
| M09 | 正式切片中，中等湍流 $N_p=2$ 的 $\tau=0.5$；中等湍流 $N_p=4/8/16$ 与弱/强湍流 $N_p=2$ 的 $\tau=1.0$ | `data/ch4-formal-pilot-sensitivity.csv`；`tables/ch4-formal-configuration.md` | `tables/ch4-method-role-comparison.md` | 正式对比逐 scene×pilot 使用独立调参映射 | 必须逐切片披露参数 | 不沿用“全部切片统一 $\tau=1$” |
| M10 | 输出是两路 post-demux、pre-CPR 复符号流 | `production_core.py:451-470`；`tables/ch4-formal-configuration.md` | `figures/ch4-method-flow.svg` | 第四章方法完成偏振解复用并向后续每偏振 CPR 提供接口 | 第三章只作为模块接口，未联合启用 | 不声称已有 Ch4+Ch3 联合 BER |
| M11 | $\rho=s_1/s_2$ 只作为接收端可见诊断量 | `scaled_unitary.py:75-87`；`production_core.py:421-470` | `algorithm-box.md` | 可用奇异值比描述结构偏离程度 | 当前没有运行时阈值或自动切换 | 不把 $\rho$ 写成已验证的在线门控 |

## B. 正式数据与结果事实

| ID | 可验证事实 | 权威指针 | 图表入口 | 可写结论 | 必须披露 | 禁止外推 |
|---|---|---|---|---|---|---|
| E01 | 正式总体含 128 个配对随机簇；每个 pooled 点为 4,194,304 bit | `ch4_formal_raw.json`；`data/ch4-formal-ber-curves.csv` | `tables/ch4-formal-configuration.md` | 各方法在同一随机簇和同一观测上公平比较 | BER 用整数 errors/bits 汇总并采用 Jeffreys 修正 | 不混用旧 confirmation window-mean 口径 |
| E02 | 正式 SNR 网格为 5–41 dB、间隔 2 dB；主结果覆盖中等湍流 $N_p=2/4$ 完整曲线 | `data/ch4-formal-ber-curves.csv` | `figures/ch4-formal-ber-curves.svg` | 主结论来自完整门限附近曲线，而非少数挑选点 | 理想 CSI 仅为理论参考 | 不用旧 14/18 dB 四格替代正式曲线 |
| E03 | 工程参考 BER 为 $3.8\times10^{-3}$，所需 SNR 在 $\log_{10}(BER)$ 域插值 | `ch4_formal_aggregate.json`；`data/ch4-formal-required-snr.csv` | `figures/ch4-formal-required-snr-gain.svg` | 以达到同一 BER 所需 SNR 差定义 dB 增益 | 这是未编码 pre-FEC 工程参考 | 不把同 SNR 下的 BER 差称为 dB 增益 |
| E04 | 中等湍流、$N_p=2$ 时，前向误差尺度相对调参基线降低所需 SNR 0.870474 dB，95% CI 为 [0.618162, 1.088274] dB | `data/ch4-formal-required-snr.csv` | `tables/ch4-formal-headline-results.md`；所需 SNR 增益图 | 短导频条件下存在清晰、统计稳定的门限收益 | 对比对象是独立调参奇异值下限 | 不外推为任意场景固定 0.87 dB |
| E05 | 中等湍流、$N_p=4$ 时，前向误差尺度降低所需 SNR 0.120949 dB，95% CI 为 [0.018893, 0.239227] dB | 同上 | 同上 | $N_p=4$ 仍为统计稳定的小幅优势 | 必须使用“小幅” | 不包装为显著工程跃升 |
| E06 | 导频重构尺度在 $N_p=2/4$ 的增益分别为 0.874731/0.108033 dB，均与前向误差尺度接近 | `data/ch4-formal-required-snr.csv` | `tables/ch4-formal-headline-results.md`；所需 SNR 增益图 | 两种尺度判据共同支持方法族相对基线的有限优势 | 强变体必须展示 | 不声称主变体优于强变体 |
| E07 | 中等湍流下，从 $N_p=2$ 增至 16 时，各方法所需 SNR 整体下降；方法间差距同步缩小 | `data/ch4-formal-pilot-sensitivity.csv` | `figures/ch4-formal-pilot-sensitivity.svg` | 结构约束收益主要集中在极短导频区 | 只描述冻结目标场景内敏感性 | 不声称普遍最优导频长度 |
| E08 | $N_p=2$ 时，前向误差尺度的直接 channel NMSE 低于普通 LS/调参基线；两种尺度变体的求逆残差接近 | `data/ch4-formal-mechanism.csv` | `figures/ch4-formal-mechanism.svg` | 结构约束降低估计/求逆扰动，与 BER 收益方向一致 | 机理图为 matched-cell 描述 | 不把相关性提升为跨模型因果定理 |
| E09 | 弱/中等/强湍流下 $N_p=2$ 的所需 SNR 均在完整网格内达到；结构变体的优势随场景变化且幅度有限 | `data/ch4-formal-ber-curves.csv` | `figures/ch4-formal-robustness-boundary.svg` | 可比较各场景内同条件表现 | 不跨场景合并成一个平均增益 | 不称全湍流强度统一领先 |
| E10 | 中等湍流、$N_p=2$、25 dB 时，$\delta=0/0.05$ 结构变体优于调参基线；从 $\delta=0.1$ 起排序反转 | `data/ch4-formal-mismatch.csv` | `figures/ch4-formal-robustness-boundary.svg` | 非酉偏离给出方法适用边界 | $\delta$ 只称结构失配强度；$\delta=0$ 复用主曲线观测 | 不把 $\delta$ 称为 PDL dB，不隐藏反转 |

## C. 作者取用顺序

1. 方法句：M01 → M03 → M04 → M05/M06 → M10。
2. 公平性句：M08 → M09 → E01 → E03。
3. 主结果句：E04 → E05 → E06。
4. 解释与边界：E07 → E08 → E09 → E10。
5. 每次写作前同时查 `claim-and-citation-ledger.md` 与对应图注。
