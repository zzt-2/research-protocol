# Handoff 2026-05-16

## 当前进度
- 阶段：Groundwork Step 4a 完成 → Step 5（Baseline 选定）
- 状态：进行中
- Contract 状态：未开始
- 本轮完成：Step 4a MVE 两轮验证通过（24节点 + 66节点+链路故障），决策 Go

## 关键上下文

### MVE 结果（核心决策依据）

**MVE-1: 24节点 Walker delta，无故障**
- GNN MLU: 0.809 ± 0.040（3 seeds × 150 eps）
- MLP MLU: 0.979 ± 0.047
- SP: 0.958, ECMP: 0.799
- GNN/MLP = 0.83（GNN 低 17%）→ **GNN >> MLP 验证通过**
- 但 GNN ≈ ECMP → 小拓扑下简单方法够用

**MVE-2: 66节点 Walker delta (6×11)，8%链路故障（公平对比，相同场景）**
- GNN MLU: 1.096 ± 0.126
- ECMP MLU: 1.244 ± 0.180
- MLP MLU: 1.373 ± 0.216
- SP MLU: 1.474 ± 0.220
- **GNN/ECMP = 0.88 → GNN 低 12%，方向验证通过**
- GNN/MLP = 0.80 → GNN 低 20%

### 核心洞察
1. **GNN 优势来源**：全局负载聚合 + 拓扑异常适应，不是纯拓扑路由
2. **激活条件**：链路故障打破等价路径后 ECMP 退化，GNN 仍能有效路由
3. **24节点太小**：等价路径多，ECMP 足够好。66节点+故障才体现出 GNN 优势
4. **后续仿真器必须包含链路故障场景**

### 项目状态
- Step 1-3.5 在前一轮对话完成（检索、论文获取、精读、定向补充）
- Step 4a MVE 在本轮完成
- Step 5-7 待执行

### MVE 代码文件
- `mve_env.py` — 环境定义（Walker delta 拓扑 + 非均匀流量 + 逐流路由）
- `mve_train.py` — GNN/MLP 模型 + PPO 训练
- `mve_66.py` — 66节点+链路故障扩展环境 + 公平评估
- `run_mve.sh` — 运行脚本

### 已完成的前期工作（前轮对话）
- Step 1: 87条候选（必读15/建议读20），size gen × 拥塞路由交叉为真空
- Step 2: 10篇论文 content.md 已获取
- Step 3: 10篇精读 + 3篇写作架构 + 综合分析
- Step 3.5: TELGEN 竞品发现 + 定位修订（per-link 负载均衡 + size gen）
- 缺失论文：GNN-ASSSP, DLBR, LARRI, FlexSATE, CA-GAR（5篇未获取）

### 已确认的关键决策
- D1: R1+R2 搜索策略，87 条候选
- D2: 差异化定位 = per-link 负载均衡（vs per-flow/per-path）
- D4: GMR(L02)架构最接近（MPNN+DDPG per-path 流量分割）
- D5: 研究定位 = per-link 负载均衡 + size generalization
- D7: MVE Go（见上文结果）

### 核心风险
1. **[已缓解] GNN ≈ MLP**：MVE 已验证全局聚合有效
2. **[中] TELGEN 竞品**：Zhou 2025 ToN 已做 GNN+TE+size gen，差异化须聚焦 LEO 时变拓扑
3. **[中] 仿真复杂度**：66节点+链路故障+动态流量的仿真器比 MVE 复杂得多

## 下一步
1. **读 `stages/groundwork.md` Step 5 规范**（Baseline 选定）
2. **选定 Baseline**：ECMP（MVE 中的主要竞品）+ GMR（最接近的 GNN 竞品）+ SP
3. **Step 4b 执行可行性评估**：读 `stages/gw-feasibility.md` 维度 C/E
4. **Step 6 仿真器设计**：基于 MVE 代码扩展，加入链路故障、动态流量、per-link 决策
5. **Step 7 Baseline 复现**

## 项目文件索引
- `projects/leo-congestion-routing/master-state.md` — Master 编排状态
- `projects/leo-congestion-routing/decision_log.md` — 决策日志（D1-D7）
- `projects/leo-congestion-routing/literature_notes.md` — 文献笔记
- `projects/leo-congestion-routing/mve_env.py` / `mve_train.py` / `mve_66.py` — MVE 代码
