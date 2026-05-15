# Handoff 2026-05-15

## 当前进度
- 阶段：GW Step 3 完成，待 Step 3.5（定向补充检索）
- 状态：进行中
- Contract 状态：N/A
- 本轮完成：
  - Step 1: 4组检索合并105篇，AI审查22篇候选
  - Step 2: IEEE校园网自动下载，精读池从7篇扩充到16篇，实际精读8篇
  - Step 3: 8篇精读完成，`literature_notes.md` 已写入
    - L01 Geng TVT 2025 — GNN+元学习功率分配
    - L02 Zhang TWC 2026 — 动态超图NN
    - L03 Gong TWC 2026 — 分层MADRL BH（核心竞品）
    - L04 Graph-Theoretic BH WCL 2026 — 图论BH（最接近GNN的非NN方法）
    - L05 Zhao/Gong TWC 2025 — DT+MA3C+MADDPG BH+PA
    - L06 Liu arXiv 2025 — 3D-GNN用户调度（**有开源代码**）
    - L07 Zheng ChinaComm 2023 — 势博弈+内点法BH
    - L08 Xie arXiv 2025 — PPO混合动作多星BH

## 关键上下文
- **核心创新点验证**: GNN for BH pattern design = **零篇论文确认**（蓝海）
- **GNN方法借鉴**: L01(图构建+聚合函数)、L02(超图+GRU)、L06(3D超边图+SoftTop+开源代码)
- **DRL baseline**: L03(QPLEX分层)、L05(MA3C+MADDPG)、L08(PPO扁平)
- **图论参考**: L04(精确干扰足迹+动态图着色) → GNN可直接在干扰图上做消息传递
- **最关键发现**: 所有DRL方法(QPLEX/PPO/MA3C)都不建模波束间空间干扰耦合，仅靠距离约束或惩罚项处理干扰 → GNN的明确优势切入点

## 未解决决策
- Step 3.5 定向检索方向：GNN在非卫星调度/分配问题中的应用、BH仿真环境参考实现
- 需确认精读覆盖面是否足够（8篇≥5门槛达标）

## 下一步
1. **Step 3.5 定向补充检索**（新对话执行）
   - 搜索 GNN 在调度/资源分配问题中的应用（非卫星领域方法迁移）
   - 搜索 BH 仿真环境参考实现
   - 更新 `literature_notes.md`
2. **Step 4a Go/No-Go 决策**
   - 读 `stages/gw-feasibility.md`
   - 评估维度 A(方向根基)、B(竞品态势)、D(MVE验证)
3. 文件路径:
   - 精读产出: `projects/leo-beam-hopping-gnn/literature_notes.md`
   - 检索结果: `search-archive/2026-05-15/beam-hopping-merged.json`
   - 覆盖面报告: `projects/leo-beam-hopping-gnn/coverage-gap-report.md`
