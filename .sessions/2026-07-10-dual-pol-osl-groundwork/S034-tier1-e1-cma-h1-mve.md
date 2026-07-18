# [S034] Tier 1 执行 — E1 群等变 FAIL + CMA+H1 组合 PASS（弱于 ML+H1）

> 2026-07-16 | GW 方法层 Tier 1 MVE | 状态：执行完成，两方向结论已定
> （承接 S033 swap 全貌诊断 + S032 §F 方法层 8 机制规划。Tier 1 两方向执行）

## 目标

执行 S033 §F 方法层下一步两个优先方向：
1. **方向 1 E1 群等变 NN**（攻 SOP 泛化，prompt030 坐实 ML N=8M/SOP=1e-6 崩塌）
2. **方向 2 CMA+H1 组合**（执行 agent D039 只测 ML+H1，CMA+H1 未测的新方向）

## 记录

### A. 方向 2 CMA+H1 组合 — PASS 28.6×（但弱于 ML+H1）

**脚本**：`prompt031_cma_h1_combo.py`（隔离，复用 prompt030 的 `cma_equalize` + `classify_swap` + `gen_channel`，复用 prompt029 的 `StandardCMA2x2` 作对照移除——改用 prompt030 口径满足铁律 3）。

**实验设计**：N=5M/strong 4.2/1.4/F_G=30/SOP=4e-7/20dB/QPSK/late[4.375M,5M)/seeds 1000-1004。四方法同信道对比：
- (A) CMA-only：`common/_cma.py CMAEqualizer2x2`（块级，与 S033 一致）
- (B) CMA+H1：(A) 输出 → late `classify_swap` → 若 swap 则翻 zX↔zY + 4 旋转校正
- (C) oracle：完美 CSI 下界
- (D) ML+H1：对照（验证 D039 5591× 恢复）

**核心数据（5 seeds）**：

| 方法 | mean fixed BER | mean flip BER | swap 分布 | 改善 |
|---|---|---|---|---|
| CMA-only | 4.8422e-01 | -- | 4 clean_swap + 1 degraded_swap | -- |
| **CMA+H1** | 4.8422e-01 | **1.6926e-02** | 5/5 flipped | **28.6×** |
| ML+H1 | 4.9963e-01 | 8.2480e-05 | 5 clean_swap | 5591× |
| oracle | 3.5280e-05 | -- | -- | -- |

**per-seed CMA+H1 flip BER**：1000=1.81e-3 / 1001=4.72e-5 / 1002=6.65e-3 / 1003=7.44e-5 / **1004=7.60e-2（degraded_swap 拖后腿）**

**关键发现**：
1. **CMA+H1 是独立有效方法**（28.6× 改善 ≠ trivial）。CMA 在线均衡也 swap（5/5，与 S033 不变量 9 一致），翻标签能救回大部分——这与 ML+H1（=PI-BER）机制不同：CMA 在线输出随 SOP 持续演化，翻标签是 post-hoc 把"CMA 锁错"翻回
2. **但 CMA+H1 弱于 ML+H1**（28.6× vs 5591×）。根因：CMA 在线更新在 degraded_swap seed（1004）上输出质量差（fixed=0.43，degraded swap = 残余误差大），翻标签只救到 7.6e-2；而 ML fixed-weight 5/5 全 clean_swap（zX≈sY 独立 QPSK），翻标签完美恢复 ≈ oracle
3. **验证 D039**：ML+H1 flip_ber=8.25e-5 ≈ D039 报的 8.936e-5（微小差异来自 per-seed 取均值方式），确认基建一致

**判定**：CMA+H1 PASS 预注册标准（flip<0.1 且 改善>10×），但作为论文方法层贡献**价值有限**——它弱于已有的 ML+H1（=PI-BER），且本质上仍是"事后翻标签"类（机制 H），不攻 SOP 泛化根因。

### B. 方向 1 E1 群等变 NN — FAIL（约束等变不足以打破时序正交）

**脚本**：`prompt031_e1_equivariant.py`（隔离，自定义训练循环复用 `ButterflyCNNEqualizer2x2` + chunk 模式，加等变一致性 loss）。

**实验设计**：同 D022 域。方法网格：
- L0：`ButterflyCNNEqualizer2x2`，纯 MSE loss（D022 baseline）
- E1（λ=0.01/1.0）：L0 + 等变一致性 loss `‖f(R(θ)·r) - R(θ)·f(r)‖²`，θ~U[0,2π]
- λ=0.0 隐含消融（loss 里 `if lam > 0` 跳过等变项 = 纯 MSE = L0）

**核心数据（seed=1000，3 λ 完整跑完）**：

| 方法 | fixed BER | PI BER | swap 分类 |
|---|---|---|---|
| L0（λ=0） | 4.9937e-01 | 4.9600e-04 | clean_swap |
| E1 λ=0.01 | 4.9939e-01 | 5.3200e-04 | clean_swap |
| E1 λ=1.0 | 4.9940e-01 | 5.2880e-04 | clean_swap |
| oracle | 8.0000e-06 | -- | -- |

**判定**：FAIL（改善 1.0×，E1 best fixed=0.49939 ≈ L0 0.49937）。

**核心失败机制（TL-22 物理前提检查）**：
- **根因 = 约束等变（soft equivariance）仍在训练段施加**：等变 loss `‖f(R(θ)r) - R(θ)f(r)‖²` 在训练 chunk 上计算，训练段 SOP 漂移远小于 test late 57°。学到的等变性泛化不到 test late 的极端旋转
- **与 A1（D031 KILL）同构**：A1 是 SOP 不变性正则，E1 是 SOP 等变性正则，两者本质都是"训练段加几何约束"。D031 已证"训练段 loss/约束触及不到 test 段 swap"，E1 再次确认
- **三度同构失败**：A1（D031 不变性正则 KILL）+ A2（D031 对比学习 KILL）+ E1（本轮等变正则 FAIL）→ **训练段任何几何约束都无法打破训练/test 时序正交**
- 等变约束只让训练 loss 收敛稍慢（L0 97s → E1 228s/259s），但最终 swap 行为完全不变

**与 A1 的区别（已在脚本 TL;DR 说明，MVE 证否）**：
- 假设：等变性是架构级约束（群结构保证全角度成立），不同于 A1 的局部 loss 正则
- 实测：约束等变（soft, loss 惩罚）不等价于严格等变（hard, 群卷积）。soft 等变仍需训练数据覆盖目标角度，跟 A1 一样泛化不到 test late
- 要实现严格等变需群卷积（如 e2cnn 库的 SO(2) 等变层），但那要重写整个网络架构（超出本轮隔离脚本能做范围），且 S032 §C B 类已 defer（D033：固定前馈架构不保证对未见 SOP 等变）

### C. 对方法层战场的影响

1. **E1 FAIL 进一步加固"训练段几何约束无效"结论**（A1/A2/E1 三度同构）。剩余攻 SOP 泛化的出路 = **严格群卷积架构**（hard equivariance，需 e2cnn 等库重写）或 **test 段在线机制**（D 类 CMA+ML 混合已在 D036 KILL，但 CMA+H1 本轮显示 CMA 在线+事后翻转有效）
2. **CMA+H1 PASS 但弱于 ML+H1**：方法层仍无超越 D022（ML PI 优势窄域）+ D039（ML+H1=PI-BER trivial）的新贡献。CMA+H1 可作论文 limitations 写（"CMA 在线+翻标签也有效但弱于 ML 固定权重+翻标签"），但不构成方法层升级
3. **Tier 1 两方向执行完毕**：E1 FAIL + CMA+H1 PASS（弱）。S032 §F Tier 1 剩余 E2（排列等变 deep sets/transformer）/ D3（MMA）未测，可独立并行。但 E1 的失败预示 E2（同为 ML 架构攻泛化）大概率同构 FAIL（排列等变也不改变训练/test 时序正交）

## 决策引用

- D031：A 类 KILL（训练段 loss 触及不到 test 段 swap）——E1 FAIL 与此同构
- D033：B 类整体 defer（固定前馈架构不保证 SOP 等变）——E1 约束等变证否此判断
- D038：B2 非对称功率 KILL（swap 载体=ML fixed-weight）
- D039：H1 ML+H1 trivial Go（=PI-BER 5591×）——本轮 CMA+H1 对照验证
- S033 不变量 9/10/11：swap 是 SOP 物理现象 CMA/ML 都 swap / fixed-label 是真记分牌 / correlation 口径分类
- 无新建决策（本轮是 Tier 1 执行，结论进 topic-index，方向定位见后续）

## 范围确认

- 本轮是否在 scope boundary 内：是（S033 §F 方法层下一步方向 1+2，D030 授权的方法层解冻探索）
- 无范围变更

## 后续

**关键结论更新（进 topic-index 进展线索）**：
- E1 群等变 FAIL（约束等变不足以打破训练/test 时序正交，与 D031 三度同构）
- CMA+H1 PASS 但弱于 ML+H1（28.6× vs 5591×，degraded_swap 拖后腿）
- 训练段几何约束类方法（A1/A2/E1）全 FAIL，火力应转向**严格群卷积架构**或 **test 段在线机制**或 **H 类（接受 swap）**

**方法层下一步（待主控决定）**：
1. E2 排列等变（deep sets/transformer）—— 与 E1 同构风险高（同为 ML 架构攻泛化），但排列等变 ≠ 旋转等变，机制不同可一测
2. D3 MMA（CMA 直系变种）—— 独立方向，须对冲 2015 Kalman 邻近点
3. H2 swap 时刻预测 / H3 swap 概率纳入 BER 统计模型 —— H 类剩余，未测
4. 严格群卷积（e2cnn SO(2) 等变层重写网络）—— E1 soft 失败后的 hard 方向，成本高（需新依赖库 + 重写架构）

**债务**：
- E1 只跑了 seed=1000（耗时控制：单 seed 三 λ = 561s，5 seeds 会超时）。单 seed 足够判定（L0/E1 数字几乎完全相同 0.49937/0.49939/0.49940，3+ seeds 不会反转"无变化"结论），但严格发表需补 seeds
- CMA+H1 完整 5 seeds（与 S033/prompt030 一致口径）
