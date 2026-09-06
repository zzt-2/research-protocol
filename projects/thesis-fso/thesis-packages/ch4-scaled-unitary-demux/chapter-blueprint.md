# 第四章材料地图与组织清单

> 形态：4.1–4.7 的作者取材卡。不得直接拼接成连续正文。

## 4.1 目标场景与问题定义

| 卡项 | 内容 |
|---|---|
| 要回答的问题 | 短导频下为什么需要对 2×2 pilot-LS 引入结构约束？ |
| 可写事实 | 目标切片满足 $H\approx gQ$；普通 2×2 complex LS 保留模型外自由度；解复用需要稳定求逆 |
| 核心公式 | $Y_p=HX_p+N_p$；$\hat H_{LS}=Y_pX_p^H(X_pX_p^H)^{-1}$；$H\approx gQ$ |
| 图表入口 | `figures/ch4-method-flow.svg`；`tables/ch4-formal-configuration.md` |
| 解释顺序 | 双偏振观测 → 短导频 LS → 结构先验 → 逆矩阵误差传播 |
| 必须披露 | static single-tap、公共尺度、equal circular AWGN、DP-(8,8)-16APSK |
| 禁止外推 | PDL/PMD/FIR/时变 SOP/CFO/CPR/LDPC 已验证 |

## 4.2 公平基线与方法族身份

| 卡项 | 内容 |
|---|---|
| 要回答的问题 | 与谁比较？两种尺度判据是否是两个独立方法？ |
| 可写事实 | 普通 LS 是基础基线；调参奇异值下限是主对比基线；两种结构变体共享 $Q=UV^H$ |
| 核心公式 | $\tilde s_i=\max(s_i,\tau s_1)$；$W_\tau=V\operatorname{diag}(1/\tilde s_i)U^H$ |
| 图表入口 | `tables/ch4-method-role-comparison.md`；`algorithm-box.md` |
| 解释顺序 | 普通 LS → 调参 floor → 共同方向 → 两种尺度准则 → 理想 CSI 参考 |
| 必须披露 | 中等湍流 $N_p=2$ 的 $\tau=0.5$；其余 formal slice 为 1.0；理想 CSI 非部署方法 |
| 禁止外推 | “全局 $\tau=1$，因此所有 baseline 仅差尺度”；“两个独立核心贡献” |

## 4.3 方向—尺度解耦方法推导

| 卡项 | 内容 |
|---|---|
| 要回答的问题 | 共同方向、前向误差尺度和导频重构尺度怎样闭式获得？ |
| 可写事实 | SVD 给出共享方向；主变体在信道域取奇异值均值；强变体在输出域逐观测标定基准逆矩阵 |
| 核心公式 | $\hat Q=UV^H$；$\hat g_F=(s_1+s_2)/2$；$W_F=\hat Q^H/\hat g_F$；$\hat a=\max(0,\operatorname{Re}\langle W_0Y_p,X_p\rangle_F/\|W_0Y_p\|_F^2)$ |
| 图表入口 | `algorithm-box.md`；`figures/ch4-method-flow.svg` |
| 解释顺序 | LS → SVD → 共享方向 → 主变体 → 强变体 → 三支路公平比较 |
| 必须披露 | $\hat a$ 逐观测变化；强变体 `h_hat` 为校准前继承量；$\rho$ 不驱动分支 |
| 禁止外推 | 发明 polar/Procrustes；导频重构尺度固定为 1.0；已实现在线 selector |

## 4.4 正式实验配置与统计口径

| 卡项 | 内容 |
|---|---|
| 要回答的问题 | 完整曲线、随机总体、BER 和 required-SNR 怎样定义？ |
| 可写事实 | 128 paired latent clusters；5–41 dB/2 dB 网格；每 pooled 点 4,194,304 bit；Jeffreys BER；门限插值 |
| 核心公式 | $\hat p_J=(e+0.5)/(n+1)$；$SNR_{gain}=SNR_{req,baseline}-SNR_{req,variant}$ |
| 图表入口 | `tables/ch4-formal-configuration.md`；`data/ch4-formal-ber-curves.csv`；`data/ch4-formal-required-snr.csv` |
| 解释顺序 | 场景 → pilot/SNR 网格 → 配对总体 → BER → 门限交点 → 簇级置信区间 |
| 必须披露 | BER 为 post-demux/pre-CPR、uncoded pre-FEC；工程参考为 $3.8\times10^{-3}$ |
| 禁止外推 | 同 SNR BER 差冒充 dB 增益；旧四格与 formal 曲线混合 |

## 4.5 主结果

| 卡项 | 内容 |
|---|---|
| 要回答的问题 | 在最关键的 $N_p=2/4$ 下，方法族相对调参基线提高多少？ |
| 可写事实 | 主变体增益 0.870/0.121 dB；强变体 0.875/0.108 dB；四项 CI lower 均为正 |
| 核心公式 | 见 `tables/ch4-formal-headline-results.md` |
| 图表入口 | `figures/ch4-formal-ber-curves.svg`；`figures/ch4-formal-required-snr-gain.svg`；headline 表 |
| 解释顺序 | 完整 BER 曲线 → 工程门限 → 绝对 required SNR → 增益/CI → 两变体近等效 |
| 必须披露 | $N_p=4$ 是小幅优势；理想 CSI 仅显示余量；强变体不能隐藏 |
| 禁止外推 | 主变体胜强变体；0.12 dB 是“大幅提升”；全面优于近期强方法 |

## 4.6 导频敏感性、机理与适用边界

| 卡项 | 内容 |
|---|---|
| 要回答的问题 | 增益为何集中在短导频？结构失配时会怎样？ |
| 可写事实 | pilot 增大后差距缩小；主变体直接 NMSE 更低；两结构变体求逆残差接近；$\delta\ge0.1$ 时排序反转 |
| 核心公式 | channel NMSE；inverse residual；结构失配 adapter 只作为冻结数据定义 |
| 图表入口 | `figures/ch4-formal-pilot-sensitivity.svg`；`figures/ch4-formal-mechanism.svg`；`figures/ch4-formal-robustness-boundary.svg` |
| 解释顺序 | pilot sensitivity → matched mechanism → scene-local comparison → mismatch reversal |
| 必须披露 | 强变体 channel NMSE 不适用；$\delta$ 不是 PDL dB；各场景内同条件比较 |
| 禁止外推 | 混合均值因果；全场景鲁棒领先；隐藏 $\delta\ge0.1$ 反转 |

## 4.7 跨章接口与章末收束材料

| 卡项 | 内容 |
|---|---|
| 要回答的问题 | Ch4 如何接入 Ch3？本章贡献上限是什么？ |
| 可写事实 | Ch4 输出两路 post-demux/pre-CPR 复符号；Ch3 可按每偏振支路处理；现有证据未联合运行 |
| 核心公式 | $Z=WY=[z_x,z_y]^T$；后续接口 $z_x\to CPR_x$、$z_y\to CPR_y$ |
| 图表入口 | `figures/ch4-method-flow.svg`；`thesis-spine-integration-notes.md` |
| 解释顺序 | 模块输出 → 物理处理顺序 → 共同母模型 → 未联合验证 → 有界贡献 |
| 必须披露 | 逆幅度归一化可能改变第三章 selector 的 $|r|^2$ 统计；不得沿用联合 BER |
| 禁止外推 | 端到端联合性能、第三章证据已是 DP/coded、旧总纲仍有效 |

## 作者使用检查

- [ ] 每节至少引用一项正式图/表或公式卡。
- [ ] 每个数字能回到正式 CSV。
- [ ] 每个方法动词能回到 `production_core.py`/`scaled_unitary.py`。
- [ ] 每节同时写入“必须披露”，不只摘有利数字。
- [ ] 不从本文件复制成长段；按学校模板自行组织句子。
