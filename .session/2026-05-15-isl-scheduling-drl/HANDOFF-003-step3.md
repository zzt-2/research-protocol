# Handoff 2026-05-15 (Round 3)

## 当前进度
- 阶段：GW Step 3.5 完成，待 Step 4a Go/No-Go
- 状态：进行中
- 本轮完成：
  - Step 3 补充：4 篇竞品精读完成（L09-L12）✅
  - Step 3.5：定向补充检索完成（7 组检索 + 引用链分析）✅
  - 文件：`projects/leo-isl-scheduling-drl/literature_notes.md`（12 精读 + 3 浅读）

## 关键结论

### 12 篇精读论文总结
- **确定性优化（5篇）**：L01 DuJo、L03 DoTD、L06 LPTSO、L07 精英保留、L11 DITO
- **GNN 监督学习（1篇）**：L02 DeepLaDu（技术基础）
- **DRL 方法（4篇）**：L05 SatFlow、L09 Wang TCOM MADRL、L10 Pi MADDPG、L12 Wang TWC 联邦RL
- **启发式路由（1篇）**：L04 ISASR（setup delay 建模）
- **管理架构（1篇）**：L08 Mao 2025

### 创新空白确认（Go/No-Go 关键证据）
1. **所有 4 篇 DRL ISL 论文均使用粗粒度动作空间**：L09(8选1)、L10(选目标卫星)、L12(16选1)、L05(index offset)
2. **所有 DRL 论文均使用 FC 网络**，无 GNN 拓扑感知
3. **无一篇做逐链路建立/拆除/切换三态决策**
4. **GNN+DRL 细粒度 ISL 调度为文献空白**（3 浅读论文中 L14 最接近，但仍聚焦路由而非调度）

### 竞品对标
- **L09 (Wang TCOM MADRL)**：最直接竞品，"3固定+1动态"+DQN，720星收敛，但动作空间粗糙、无GNN
- **L10 (Pi ICC MADDPG)**：最接近MARL方案，冲突惩罚机制可借鉴，但决策粒度300s
- **L12 (Wang TWC 联邦RL)**：异步FL架构可借鉴，16选1动作空间、无GNN
- **L02 (DeepLaDu)**：技术基础——GNN学习对偶变量范式

## 未决问题
- L14 (DMR, GNN+DRL 多路径) 和 L15 (GNN-MAPPO) 下载失败（付费墙），如需精读需用户手动获取

## 下一步
1. **Step 4a Go/No-Go 决策**（`stages/gw-feasibility.md`）：
   - 结构优势论证：GNN 拓扑编码 + DRL 在线决策 vs 最简 FC-DQN
   - 新颖性论据：15 篇文献确认 GNN+DRL ISL 调度为空白
   - 可行性：DeepLaDu GNN 架构可复用，MDP 建模有 L09/L10 参考
   - MVE：最小实例设计
2. 读取框架文件：`stages/gw-feasibility.md`
3. 写 `feasibility_report.md`
