# [S066] 6-pilot Jones EMA09 正式 GW Step1 检索

> 2026-07-16 | GW Step1 | 状态：进行中（主体检索完成，第三来源已补齐，待质量审查）

## 目标

验证“稀疏 pilot + Jones inverse + EMA”在 coherent optical/FSO 的直接撞车和可成立的窄问题，不以组合细节冒充新颖性。

## 记录

两组独立检索共6个定向查询，已保存 `search-archive/2026-07-16/`。首组三查询43条，实际主要OpenAlex 39、S2 2；第二组围绕EMA/Kalman、训练符号2×2、FSO overhead补检索。

直接/高碰撞：JLT 2023 frame pilot channel response + feed-forward compensation；IEEE Communications Letters 2026 frequency-domain pilot Jones/demux + FOE/CPE/RSOP；Optics Communications 2021 out-of-band pilot SOP tracking；2022 Kalman/2025 ML覆盖高速时变跟踪。故“pilot-assisted polarization tracking / Jones前馈逆补偿”不能作为贡献。

FSO邻近：2018 JOSAA湍流下自适应偏振控制，2021 Nature Photonics、2022/2023 JLT的pilot-assisted self-coherent/self-homodyne等；未直接等同当前纯DSP稀疏时域pilot形态。

可继续核查的窄问题：**传统 block/frame pilot Jones inversion 在 dual-pol OSL 的 GG + 高速 SOP + 低pilot预算下，短pilot LS估计抖动/病态导致fixed-label恢复不稳定；如何在≤10% overhead内稳定估计并量化开销—估计稳定性—恢复性能。** 仿真证据：2p灾难性失败，原6p seed47仅6.33%改善，EMA09后完整24 cells原门槛15/15。

## 决策引用

- D054：候选晋级正式GW Step1。
- D055：泛称方法撞车，问题收窄到OSL低开销稳定性权衡（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

第三来源 Tavily 已补齐14条，新增pilot-tone/phase-noise邻近论文和专利证据；Exa/Firecrawl空结果不计覆盖。随后 Step2 获取2023 JLT、2026 LCOMM、2021 pilot SOP、FSO邻近论文。未完成Step2/3前不再扩方法实验。
