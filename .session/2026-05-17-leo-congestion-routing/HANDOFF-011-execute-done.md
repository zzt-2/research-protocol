# Handoff 2026-05-17 — Execute Step 2 完成

## 当前进度
- 阶段：Execute Step 2（核心实验+消融完成）
- 状态：E01-E09 全部完成，Contract 假设全部验证通过
- Contract 状态：amended（K-path 离散动作空间）
- 本轮完成：E01-v2 + E02-E06 + E08-E09，共 10 组实验

## 实验结果总览

### 核心实验 (P0) — 全部 PASS
- **E01-v2** (66节点): GNN/ECMP=0.818 PASS, GNN/MLP=0.822 PASS
- **E04** (48节点 0.7×): GNN/ECMP=0.924 PASS, MLP崩溃(比ECMP差34%)
- **E05** (288节点 4.4×): GNN/ECMP=0.900 PASS, MLP/ECMP=1.031
- **E06** (720节点 10.9×): GNN/ECMP=0.948 PASS, MLP/ECMP=0.996

### 对比实验 (P1)
- **E02** (无故障): GNN/ECMP=1.095 — 故障是优势激活条件
- **E03** (极端突发): GNN/ECMP=0.860 — GNN仍优于ECMP 14%

### 消融实验 (P1)
- **E08** (故障率 0-15%): 甜点在8-10%, GNN赢17-20%
- **E09** (流量模式): 均匀=GNN赢11%, 重型=GNN赢18%

### 待做 (P2)
- E10: GNN层数消融 {1,2,3} — 需重训 (~1.5h)
- E11: 注意力头数消融 {2,4,8} — 需重训 (~1.5h)
- E12: 故障模式对比（随机vs区域vs级联）

## 关键决策
- D17: E01 GNN/MLP=0.863 FAIL 分析 → seed敏感性, 非架构缺陷
- D18: E01-v2(800ep+entropy=0.02) + E04 确认核心假设成立

## 产出文件
- `simulator/results/e01_results.json` — E01 原始
- `simulator/results/e01_v2_results.json` — E01-v2 (PASS)
- `simulator/results/e04_quick_results.json` — E04 泛化
- `simulator/results/e05_e06_results.json` — E05+E06 泛化
- `simulator/results/e02_e03_results.json` — E02+E03 对比
- `simulator/results/e08_e09_results.json` — E08+E09 消融
- `run_e01.py`, `run_e01_v2.py`, `run_e04_quick.py`, `run_e02_e03.py`, `run_e05_e06.py`, `run_e08_e09.py`

## 下一步
1. 可选: E10/E11 架构消融（需重训，P2优先级）
2. 可选: E12 故障模式对比
3. Step 3 假设判定（E01-v2 已 PASS，正式记录）
4. Step 6 结果可视化
5. 论文材料整理

## 恢复读取顺序（新对话）
1. 本 HANDOFF 文件
2. `master-state.md`
3. `contract.md`
4. `simulator/results/e01_v2_results.json`（核心结果）
5. `stages/execute.md` — Step 3/4/6 后续步骤
