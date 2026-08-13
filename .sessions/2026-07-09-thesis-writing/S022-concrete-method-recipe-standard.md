# [S022] 具体方法 recipe 标准纠偏

> 2026-08-13 | 战略讨论 | STANDARD_CORRECTED

## 目标

纠正 R024 之后主线程仍以“承重对象/动作血缘/支撑组件”代替具体方法清单的问题，冻结“只要相对经典 baseline 有真实改善，且完整 recipe 不完全相同即可作为场景迁移或扩展方法”的务实标准。

## 记录

用户明确要求的不是更多治理分类，而是具体方法。方法不需要具有独立新动作原子；已有方法迁移到本项目场景、改变 estimator/阈值/参数/执行顺序/数值格式，甚至仅目标场景不同，都可构成差别。碰撞只指算法步骤、输入输出、场景和关键配置完全一致，重点是“完全相同”，不是“相似”。

因此，后续必须直接用“方法名—步骤—baseline—已有改善—与既有 recipe 的差别”呈现。已有真实数字的 P01、P11、P02、P05、P06、P08-R2 和 select-before-execute 均先进入具体 recipe 清单；是否适合单独成章是第二层问题，不能在列方法前就以 supporting/工程组件标签隐藏。

### 首批具体方法 recipe

| 方法 | 具体步骤 | 选定 baseline | 已有改善 | 可陈述差别 |
|---|---|---|---|---|
| Pilot-SNR-Calibrated CCISP（P01） | 导频估计当前窗 SNR → 替换 nominal SNR → 执行原 CCISP gate | 使用配置 nominal SNR 的原 CCISP | ±3 dB 失配下恢复 4/5 个 harm cells；原损害 0.324–0.704 dB | 将固定配置驱动的 CCISP 改为本场景 receiver-visible pilot-SNR 校准 |
| Pilot-Efficient Complex-LS Butterfly FIR（P11） | 1% pilots → complex Toeplitz LS → 11-tap 2×2 Butterfly FIR → payload | 50%-label full-label Adam FIR | 实际 20 dB 局部 BER `3.176e-4` vs `3.859e-4`，goodput 约 1.98× | 在本项目双偏振/Butterfly-FIR 条件用低导频闭式 LS 替代标签密集训练 |
| Select-Before-Execute CPR | 先由 selector 产生命令 → 只执行 DA/NDA 一支 → 公共 detector | 两支均执行后再选择 | 396,000 windows 输出零 mismatch；branch calls −50%，软件时延比 0.5424 | 将 CCISP 从结果选择改为执行前调度 |
| Low-SNR Reference-Calibrated CCISP（P02） | 离线冻结 `ref_snr_db=11` → 全 cell 使用同一参考点 → 原 selector | `ref_snr_db=9` 的 adapter/cand-rank | 相对 adapter +0.4539 dB，相对 ref=9 cand-rank +0.0961 dB | 面向本项目 weak/low-SNR 条件重标定 CCISP 工作参考点 |
| Online-CMA-Continued Butterfly Equalizer（P05） | frozen ButterflyCNN 输出/当前 RX → corrected Godard-with-z CMA block update → fixed-label output | 冻结 ButterflyCNN/ML equalizer | 两个 SOP-drift cells 中 fixed-label BER 约 0.499 降至 0.00018/0.00117 | 将经典在线 CMA 迁移为本项目冻结 ML Butterfly 均衡器的持续鲁棒增强 |
| Prefix-LS-Calibrated Coded FSO Receiver（P08-R2） | 32-symbol prefix → LS `H_eff`/噪声估计 → MMSE/LLR → LDPC | 未使用该 receiver-visible calibration 的 corrected B0 | 局部 slice FER 0.155→0.148，差值 +0.0063 | 在本项目 coded FSO 链中用 prefix-LS 消除 hidden-SNR 依赖并校准 LLR |
| Cross-Frame Persistence State Predictor（P06） | 上一帧 receiver-visible state/metric → 直接预测下一帧状态 | current-only / history-expanded ridge | test R² 0.853 vs history ridge 0.320 | 将简单 last-value persistence 用于本项目帧间 FSO/CMA 状态预测 |
| Finite-Word-Length CCISP Selector（P03） | CCISP statistics → Q(8,6) 饱和定点计算 → branch command | 浮点/更宽统一精度 selector | gain-bearing 区 regret 仅约 +0.027 dB，同时字长显著缩短 | 将 CCISP 控制链映射到具体有限字长格式；只作性能—位宽方法，不声称 FPGA PPA |

上述 recipe 的本地证据均存在；“外部是否存在完整 recipe 完全相同”尚未执行新的 exact-duplicate 检索，本轮只冻结筛选标准和现有方法清单。

## 决策引用

- D032：具体方法优先与“非完全相同即可扩展”标准（新建）

## 范围确认

- 本轮是否在 scope boundary 内：是。属于学位论文方法包装战略讨论；不运行实验、不检索文献、不补 Groundwork、不修改代码/Skill/论文正文。

## 后续

直接向用户列出现有证据支持的具体方法 recipe，并明确哪些已具 baseline 改善、哪些仅有设计尚不能计入。待用户确认这种呈现和标准后，再讨论两至三个方法如何分配到 Ch3–Ch5。
