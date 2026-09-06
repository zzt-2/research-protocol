# 第四章主张与引用台账

> 用法：先选 claim，再取证据和引用；不得由引用候选反向扩张主张。

## 1. 可写主张

| Claim | 推荐表述要点 | 数据/实现证据 | 必须披露 | 证据层级 |
|---|---|---|---|---|
| CL-01 方法身份 | 将经典酉/极分解结构估计迁移为短导频双偏振方向—尺度解耦解复用方法链 | `algorithm-box.md`；`production_core.py:407-470` | 经典原子迁移；不是新的 Procrustes/极分解理论 | 方法实现 + 本地全文邻域 |
| CL-02 接收端可实现性 | 主变体与强变体只使用已知导频和接收观测 | `production_core.py:387-470` | 理想 CSI 仅为真值参考 | 实现真值 |
| CL-03 极短导频主收益 | 中等湍流、$N_p=2$ 时，主变体相对调参基线所需 SNR 降低 0.870 dB | `data/ch4-formal-required-snr.csv` | BER=$3.8\times10^{-3}$；95% CI [0.618,1.088] dB | 正式统计 |
| CL-04 $N_p=4$ 小幅收益 | 中等湍流、$N_p=4$ 时，主变体降低 0.121 dB | 同上 | 95% CI [0.019,0.239] dB；必须称“小幅” | 正式统计 |
| CL-05 强变体 | 导频重构尺度在 $N_p=2/4$ 的增益为 0.875/0.108 dB，与主变体接近 | 同上 | 不声称主变体优于强变体 | 正式统计 |
| CL-06 导频敏感性 | 随导频数增加，各方法所需 SNR 下降，结构变体相对优势缩小 | `data/ch4-formal-pilot-sensitivity.csv` | 只限冻结中等湍流场景 | 正式派生数据 |
| CL-07 作用机理 | 结构方向—尺度约束降低直接信道 NMSE/求逆残差，与 BER 收益方向一致 | `data/ch4-formal-mechanism.csv` | 导频重构尺度只用求逆残差，不用继承的信道 NMSE | 同条件配对的解释指标 |
| CL-08 结构边界 | 非酉结构失配达到 $\delta=0.1$ 后，结构变体相对调参基线的排序反转 | `data/ch4-formal-mismatch.csv` | $\delta$ 不是 PDL dB；必须保留反转 | 配对边界切片 |
| CL-09 跨章接口 | 输出可接后续每偏振 CPR | `figures/ch4-method-flow.svg`；`thesis-spine-integration-notes.md` | 未联合运行、未联合验证 BER | 模块接口 |

## 2. 必须披露清单

- 调参基线来自独立调参样本；中等湍流 $N_p=2$ 的 $\tau=0.5$，其余正式切片为 $\tau=1.0$。
- 导频重构变体的 $\tau=1$ 只生成基准逆矩阵；校准量 $\hat a$ 每个观测闭式计算。
- 导频重构变体的 `h_hat` 是校准前继承量，不能用其 channel NMSE 证明方法有效。
- $N_p=4$ 是统计稳定的小幅优势；两种尺度判据结果近等效。
- 理想 CSI 是仅使用真值的理论参考，不是可部署基线。
- 失配参数 $\delta$ 只表示结构失配强度；$\delta\ge0.1$ 的反转属于方法边界。
- Ch4 输出为 post-demux/pre-CPR、未编码 pre-FEC 符号；Ch3 只作为模块接口。
- 正式结论使用完整 5–41 dB 曲线；旧 14/18 dB 四格仅保留历史追溯。

## 3. 禁止主张

| 禁止表述 | 原因 | 可替换表述 |
|---|---|---|
| “首次提出 polar/Procrustes/unitary 信道估计” | 数学原子与通信邻域均已有经典工作 | “将经典结构估计迁移到目标短导频星地相干切片” |
| “主变体优于导频重构变体” | 四项正式结果近等效，未做二者优势检验 | “两种尺度判据均优于调参基线” |
| “在任意偏振信道下鲁棒领先” | $\delta\ge0.1$ 已出现排序反转 | “在 near-scaled-unitary 区域有效，并给出失配边界” |
| “$\delta$ 表示 PDL dB” | $\delta$ 是仿真 adapter 的无量纲结构失配强度 | “结构失配强度 $\delta$” |
| “导频重构尺度固定为 1.0” | 1.0 是基准奇异值下限参数；$\hat a$ 随观测变化 | “逐观测导频重构校准” |
| “导频重构变体改善 channel NMSE” | 该 channel NMSE 是校准前继承量 | “改善尺度处理后的求逆残差” |
| “理想 CSI 是最强可部署基线” | 使用仿真真值 | “理论参考/性能余量” |
| “第四章与第三章已联合验证” | 未联合启用；幅度归一化可能改变 selector 统计 | “提供模块化接口，联合验证待后续完成” |
| “达到 SOTA/全面领先近期方法” | 未做近期强方法全面横向实验 | “相对独立调参的经典基线取得有限改善” |

## 4. 本地引用入口

| 论证职责 | 本地来源 | 当前证据层级 | 可承担内容 | 不得承担内容 |
|---|---|---|---|---|
| 短训练、低维酉/SU(2) 偏振解复用邻居 | Roudas et al., *Optimal Polarization Demultiplexing for Coherent Optical Communications Systems*, JLT 2010；`papers/doi/10.1109_jlt.2009.2035526/content.md:601,877-879,1289-1299,3263-3265` | 本地全文精读 | 短训练、2×2 酉解复用与非酉边界背景 | 不证明本章完整方向—尺度方法链已被发表 |
| Jones/unitary、PDL/PMD 与 2×2 DSP 背景 | Kikuchi, *Digital coherent optical communication systems: fundamentals and future prospects*, ELEX 2011；`papers/doi/10.1587_elex.8.1642/content.md:273-331` | 本地全文精读 | 系统背景、PDL/PMD 与 2×2 解复用边界 | 不证明本章闭式尺度判据 |
| 数据辅助 Kabsch/酉估计强邻居 | *Capacity Bounds Under Imperfect Polarization Tracking*, TCOM 2022；`step3-5-c4-1-exact-recipe-closure.md:102,118` | 本地元数据与摘要记录；全文未读 | 相关工作候选、提醒披露强邻居 | 不承重精确公式或“无人做过” |
| Procrustes/polar/scaled matrix-nearness 原子 | Schönemann 1966、Higham 1986、Eldar–Forney 2002；`step3-5-c4-1-exact-recipe-closure.md:103,119-120` | 本地结构化研究记录；非统一全文级 | 说明数学原子经典、限制 originality claim | 正式公式引用前仍需核 bibliographic identity |
| 完整方法链的重合边界 | `projects/thesis-fso/polarization-demux-groundwork/step3-5-c4-1-exact-recipe-closure.md:113-146` | 本地候选级检索与碰撞台账 | 支撑“未确认完整方法链相同”的有限定位 | 不写成穷尽检索或绝对首次 |

## 5. 证据优先级

1. **数字主张**：formal raw/aggregate → 正式 CSV → 图/表。
2. **方法动作**：`production_core.py` / `scaled_unitary.py` → `algorithm-box.md` → 方法图。
3. **场景与边界**：正式配置表、mismatch CSV、完整曲线。
4. **文献背景**：本地全文优先；abstract/metadata 只作候选。
5. **禁止**：用旧 confirmation 数字、内部质量标签或记忆补数字。
