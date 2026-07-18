# [S069] LCOMM 2026 直接撞车精读

> 2026-07-16 | GW Step3 输入 | 状态：已完成单篇精读

## 目标

精读已获取的 LCOMM 2026，核对其 pilot/Jones 机制与当前 6-pilot EMA09 的直接关系。

## 记录

来源：`papers/doi/10.1109_LCOMM.2026.3651445/content.md`，关键行 5–11、23–29、39–45、85–101、109–117、135–153、175–179。

论文场景为相干 DSCM 光纤短中距、DP-16QAM、宽线宽激光；发端两偏振各插入频域 pilot tone，收端由四个 FPT 直接估计2×2 Jones并补偿，同时联合FOE/CPE/RSOP。实验含40 km、10 krad/s，FPT PSR −15 dB；未给出可直接换算的 pilot 符号开销，也未使用逐块稀疏时域LS+EMA。

结论：方法族层面是直接撞车（pilot→Jones→补偿），具体 dual-pol OSL + GG + 稀疏时域6-pilot + EMA09系统组合尚未在该文实现/验证。不能把“EMA=.9”或组合细节直接当新颖性；窄问题仍需比较OSL大气湍流和低pilot预算下的稳定性权衡。

## 决策引用

- D055：泛称机制撞车，问题收窄。

## 范围确认

- 本轮是否在 scope boundary 内：是。

## 后续

补齐Step1 priority硬门后，再精读其余直接/FSO邻近论文；不得因已有仿真正信号跳过Step3.5/4a。
