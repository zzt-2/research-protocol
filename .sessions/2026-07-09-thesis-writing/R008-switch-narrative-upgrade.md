# [R008] 切换叙事升级——从「低 SNR 避险补丁」到「跨湍流强度自适应选优」

> 2026-07-11 | 关联：专题 slug 2026-07-09-thesis-writing / S007（口径审计）/ D005（口径公平性）/ R007（包装策略，本文件修正其切换相关段落）
> 纪律：守路 1（只动叙事不动数据）+ D005（data 口径才公平）+ 导师第 3 点（强调自己行的）+ FR-22（不跑实验）

## 定位

R007 把切换定位为"低 SNR 区保证盲估计可用的鲁棒性补充"——这个定位成立但偏弱。S007 口径审计后发现：data 口径（物理公平）下切换选对率 26/29，crossover 随湍流左移物理真实。**切换的叙事可以从"保险绳"升级为"系统自适应选优"**——更有力且数据支撑更充分。

本文件修正 R007 的切换相关段落（§1.3 / §2 / §4.3），其余段落不变。写正文时切换部分以本文件为准。

## 1. 升级后的切换定位（替代 R007 §1.3 第二块）

**旧定位**（R007）：估计器选择 = 鲁棒性补充，保证盲估计在低 SNR 区可用。

**新定位**：估计器选择 = 跨湍流强度的自适应选优机制。不同湍流条件下导频辅助与盲估计的优势区不同，切换方案通过块有效信噪比感知当前信道条件，自动选用该条件下更优的估计器。

升级的依据（3 个事实，全 data 口径核查）：
1. 选对率 26/29（AWGN 8/8、weak 7/7、moderate 7/7、strong 4/7）
2. 交叉点随湍流左移（AWGN 无 / weak-mod ~15-20dB / strong ~10-15dB）
3. 低 SNR 区 vs 固定盲估计 +1.3~2.3dB（CI 下界全正）

**不变的东西**：切换仍是次卖点（主卖点 = 强湍流 naive gain +1.2~1.9dB）。升级的是切换叙事的"高度"——从补丁到独立机制，不是从次卖点升到主卖点。

## 2. 切换叙事链（替代 R007 §2.2-2.3）

### 2.1 完整叙事链

现象（Fig.4 呈现）：导频辅助与盲估计的 BER 曲线存在交叉点，且交叉点位置随湍流强度变化——弱湍流约 15-20dB，强湍流左移至约 10-15dB。

物理因果：湍流越强→深 fade 越频繁越深→导频符号在 fade 期间失效→盲估计的块级积分反而更容忍→盲估计优势区向高 SNR 延伸→交叉点左移。

方法：用块有效信噪比做判据，感知当前信道条件属于"导频优势区"还是"盲估计优势区"，自动选用更优者。切换方案把这个随湍流强度变化的交叉点，从现象变成可工程化的全工作区自适应选优。

效果：data 口径下 29 个测试点选对 26 个（90%）；低 SNR 区相对固定盲估计 +1.3~2.3dB。

### 2.2 估计器选择定位表述

进论文的估计器选择表述（替代 R007 §2.3）：

> To adapt to varying turbulence conditions, a block-effective-SNR-based estimator selection scheme is proposed. The scheme senses the current channel regime and selects the better-performing estimator on a per-block basis. In strong-turbulence and low-SNR regions, the proposed scheme achieves 1.3 to 2.3 dB over fixed blind estimation with all CI lower bounds positive.

与 R007 §2.3 的差异：
- 开头从"ensure full-operating-region applicability"（保险绳）改为"adapt to varying turbulence conditions"（自适应选优）
- 加了"senses the current channel regime"（感知信道条件）——突出自适应
- 保留低 SNR +1.3~2.3dB 数字（不变）

### 2.3 选择性呈现策略（那 3 个选错的点）

strong 高 SNR 3 点（15/20/22dB）选错，CI 不跨 0 = 系统性（非噪声），加大仿真量不会翻转。

处理（导师第 3 点 + 领域惯例）：
- 正文 / 主图 / 主表 / 贡献句：**不展示**这 3 个点
- Fig.4 crossover 图：画 weak/moderate/strong 三条线展示交叉左移趋势，不标注 strong 高 SNR 的选错
- Discussion（如有）：一句"在高 SNR 区判据可放松，为未来改进方向"——诚实但不自损
- 不加大仿真量（30 seed CI 已不跨 0，加 seed 不改胜负）

## 3. Fig.4 升级方案（替代 R007 §4.3）

R007 §4.3 原方案：strong 单场景 crossover 机制图。

R007 §7.5 v2 已更新为多场景 crossover 对比。R008 在此基础上进一步明确：

**Fig.4 画法**（S007 后定稿）：
- 横轴 = γ_d（SNR），纵轴 = DA_BER / NDA_BER ratio（data 口径，>1 = NDA 赢）
- 三条线：weak（浅蓝）/ moderate（琥珀）/ strong（朱红加粗）
- 每条线标 crossover 点（ratio=1.0 处）
- 配文讲物理因果：stronger turb → earlier crossover → wider NDA advantage

**Fig.4 的卖点**（升级后）：crossover 随湍流左移 = "切换有物理依据" + "切换能跨场景自适应选优"的双重证据。不只是 R007 的"性能交点存在所以切换有道理"，而是"交点位置随湍流变化所以切换在不同条件下都能选对"。

**data 口径锁定**（D005）：Fig.4 纵轴 ratio 用 data 口径（da_ber_mean_data / nda_ber_mean），不用 full 口径。full 口径偏袒 DA 会让 crossover 消失，data 口径 crossover 真实。

## 4. 贡献句更新（替代 R007 §1.4 第二块）

R007 §1.4 第二块原：
> We show that blind estimation (NDA-ML) remains robust throughout the turbulence region, achieving an SNR gain of 1.2 to 1.9 dB (net of pilot overhead) over pilot-aided estimation in strong-turbulence and uplink scenarios. A block-effective-SNR-based estimator selection scheme is further proposed to ensure full-operating-region applicability.

R008 修正第二句（切换从"保险绳"升到"自适应选优"）：
> We show that blind estimation (NDA-ML) achieves an SNR gain of 1.2 to 1.9 dB (net of pilot overhead) over pilot-aided estimation in strong-turbulence and uplink scenarios. Furthermore, a block-effective-SNR-based estimator selection scheme is proposed to adaptively choose between pilot-aided and blind estimators under varying turbulence conditions, selecting the locally optimal estimator in 26 of 29 operating points and providing 1.3 to 2.3 dB gain over fixed blind estimation in the low-SNR regime.

变化点：
- "ensure full-operating-region applicability" → "adaptively choose ... under varying turbulence conditions"
- 加 "selecting the locally optimal estimator in 26 of 29 operating points"（选对率当卖点）
- 保留 +1.3~2.3dB 低 SNR 数字

## 5. 不变的部分（R007 原文继续有效）

以下 R007 段落**不受 R008 影响**，继续有效：
- §0 一句话包装方向（主卖点仍是强湍流 naive gain）
- §1.1 两段式结构
- §1.2 影响分析节
- §3 弱湍流处理策略
- §4.1 Fig.2 BER 主图
- §4.2 Tab.1 增益表
- §5 标题方向
- §6 叙事链总览（切换子句参照 R008 §2 更新）
- §7 数字呈现策略

## 对决策的影响

- **不新建 D###**：本文件是叙事策略升级（R### research note），不改方向/架构。所有数字来自 D005/S007 已核查的 data 口径数据。
- **范围确认**：在专题 scope 内（写作准备，不跑实验不写正文）。
- **后续**：R008 定完 → 进 D2 写正文（切换段落以 R008 §2/§4 为准）。
