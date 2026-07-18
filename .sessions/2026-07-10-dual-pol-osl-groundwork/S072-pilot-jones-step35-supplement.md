# [S072] Pilot Jones Step3.5 定向补检索

> 2026-07-16 | GW Step3.5 | 状态：进行中（检索完成，直接竞品获取/精读待办）

## 目标

用精读后的关键词矩阵和 LCOMM 引用链核查更早/更直接的 block-pilot Jones/RSOP 竞争者。

## 记录

6组矩阵查询完成，原始42、canonical去重41；两组FSO+GG精确查询均0。结果归档 `search-archive/2026-07-16/step35-*.json`。LCOMM2026 backward=19、forward=0，归档 `lcomm-2026-{forward,backward}-citations.json`。

直接/高相关新竞品：TCOM 2025 pilot symbols→ML/EM RSOP；JLT 2026短preamble联合SOP/均衡；JLT 2022 FPT获取传输矩阵；JLT 2023 FPT联合偏振/载波；OE 2021三pilot tones逐block估计RSOP矩阵。FSO邻近包含JLT2022 beam mixing、JLT2023 pilot self-homodyne、OE2024训练序列同步。

收敛性较高：新增集中在FPT、block pilot、FSO pilot beam mixing三簇；FSO+GG词面持续0。尚未发现完整“dual-pol OSL GG + 稀疏时域LS Jones + EMA稳定性/fixed-label恢复”同场景论文，但generic block-pilot Jones机制已被进一步占据。

## 决策引用

- D055：generic机制撞车，窄问题待核。
- D056：Step4a前必须精读直接竞品，不能用“完整组合未出现”直接过新颖性（新建）。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

获取并精读TCOM2025/JLT2022/JLT2023/OE2021等直接竞品；更新literature_notes后再闭合Step3.5，不直接进入4a。
