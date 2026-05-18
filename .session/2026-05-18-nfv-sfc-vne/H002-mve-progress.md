# Handoff: nfv-sfc-vne MVE 进行中

> 来源: S001 + Step 3.5 + MVE | 交接目标: 继续 MVE 并完成 Step 4a
> 文件名: H002-mve-progress.md

## 已完成边界

1. **Step 1-3**: 搜索+获取+精读完成（17篇下载，9篇精读 → literature_notes.md）
2. **Step 3.5 补充检索**: Round 1 收敛。8篇新论文（4精读+4浅读）。差异化空间确认。
3. **Step 4a A0/A'/A/B**: 方向侦察中已完成，全部通过
4. **MVE 进度**:
   - Virne 仿真器已安装：`projects/nfv-sfc-vne/Virne/`（pip install -e）
   - GRC baseline: AC=0.88, R2C=0.543（Waxman100, 21s）
   - PPO-DualGAT+ epoch0: AC=0.885, R2C=0.526（未收敛，每 epoch ~7min）
   - pg_mlp 报错：特征维度不匹配（输入18维，期望21维）

## 不要做什么

- 不要重新搜索/下载论文（已充分覆盖）
- 不要跳过 MVE（组合新颖性方向不可跳过）
- 不要把"跨规模泛化"作为核心卖点（已被 Ch3 占据）
- GNN 架构走 Node-Edge 联合嵌入（matching-style），不用 HGAT
- MVE 中 pg_mlp 的特征维度问题需修复后再跑，或直接用 Virne 论文数据作为证据

## 必读

1. `projects/nfv-sfc-vne/master-state.md` — 全局状态
2. `projects/nfv-sfc-vne/literature_notes.md` — 13篇精读+11篇浅读
3. `stages/gw-feasibility.md` §D — MVE 设计要求
4. `.session/direction-scouting/S002-2026-05-18.md` — Go 决策详情

## 下一轮

### MVE 完成（最优先）

**方案 A（推荐）**: 用 Virne 论文已发表数据作为 MVE 主要证据
- PPO-DualGAT RAC=78.1% vs PPO-MLP 71.9% on WX100（相对提升 +8.6%）
- PPO-DualGAT 在大 VN(size≥6)上优势更明显，小 VN(size≤3)与 MLP 接近
- 我们的验证运行确认 Virne 仿真器可在 RTX 4070 上正常工作
- 补充：修复 pg_mlp 特征维度问题并跑完整 30 epochs 验证

**方案 B**: 修复 MLP + 跑完整实验
- pg_mlp 报错：输入18维特征，MLP期望21维
- 可能需要调整 `learning.yaml` 中 `feature_constructor` 配置
- 或改用 `ppo_att`（attention-based，非 GNN）作为 MLP 替代对比

**MVE 架构摘要**（FR-11，待写入 feasibility_report.md）:
- 动作空间: 离散节点选择（双向：先选虚拟节点再选物理节点）
- 决策粒度: per-VNR（逐请求处理，每请求内逐节点放置）
- 对比范式: PPO-DualGAT（GNN跨图编码）vs PPO-MLP（全连接网络）vs GRC（启发式排序）
- 奖励语义: fixed intermediate reward (0.1) + episode-level R2C

### MVE 通过后
- 写 feasibility_report.md（含 A0/A'/A/B/D 全部维度）
- 用户确认 Go/No-Go
- 进入 Step 5 (Baseline 选定)

### 关键差异化总结（Step 3.5 确认）
1. **SFC 依赖链约束 + matching-style GNN**: 无人做过（GraphVNE 仅特征增强，FlagVNE/CONAL 不处理 SFC）
2. **跨 PN 规模泛化**: 无人做过（FlagVNE 仅跨 VNR size）
3. **端到端可微 matching**: GraphVNE 的 IPFP 不可微
