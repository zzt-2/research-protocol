---
project: leo-ntn-handover-drl
direction: 二部图GNN+DDQN实现LEO切换size generalization
method_type: DRL
domain: comms
created: 2026-05-08
updated: 2026-05-24
current_step: 审计完成 → 待补实验
current_stage: Post-Execute
---

# Master Agent: leo-ntn-handover-drl

## §2 项目状态

### 当前位置
- 阶段：**Post-Execute — 审计完成(S003)，待补实验**
- Contract 状态：**frozen (v2)**，2026-05-09 冻结，2026-05-16 正式确认
- 方法类型：DRL

### 审计结果摘要（S003-ch2-audit，2026-05-22）
- **M4 Jain 公平性指标修复已完成**：c_gnn_ddqn.py, b2_topk.py, baselines 代码均已更新
- **审计发现问题**：2 CRITICAL + 3 IMPORTANT 数据矛盾，待修复
- **待补实验**：
  - 多 seed 验证（robustness）
  - N=30/40 规模扩展
  - 乒乓切换率指标补齐
- **paper-materials 修正**：6 项数据修正（参数量核实/标注修正/数值统一）+ 4 项指标补齐 + 5 张可视化图
- **预估工时**：审计估 ~6h 补实验（Ch1 经验表明可能偏高，需实测）

### 已完成步骤
- GW Step 1-4: 2026-05-07~08，6 篇精读，3 个 baseline 选定
- GW Step 5-6: 2026-05-08，仿真器验证通过，3 个 baseline 复现
- Contract Step 0-5: 2026-05-08~09，方案 C 设计完成，新颖性检索通过
- Execute Phase 1: 2026-05-08~09，方案 A 死亡(D021)，GNN 消融完毕(D022)
- Execute 叙事转向: 2026-05-09，转向 size generalization(D023-D025)
- Execute Scaling: 2026-05-09，Phase 1-5 全部完成(D026-D031)
- Execute 新颖性补充: 2026-05-09，D032 IEEE 补充检索通过
- Contract 冻结: 2026-05-09，v2 frozen，2026-05-16 正式确认
- 素材提取: 2026-05-10，paper_materials/ 01-06 共 ~95K
- 素材补充: 2026-05-16，18 篇中文引用 + 预印本验证
- 审计完成(S003): 2026-05-22，M4 Jain 修复 + 2 CRITICAL/3 IMPORTANT 问题 + 待补实验(D033-D034)

### 关键决策（最近 10 条）
- D023: 叙事转向 size generalization | 小规模 GNN 仅+0.8%不成立，转向跨规模泛化
- D024: 二次新颖性检索通过 | 四组系统检索无高度重叠竞争者
- D025: Contract 三阶段实验设计 | 20UE 基线→50-100UE 扩展→size gen 迁移
- D026: sat_capacity 按比例调整 | cap=10 在 100UE 下结构性不可行
- D027: buffer 扩至 200K | 50UE 36K transitions/ep，50K 仅存 1.4ep
- D028: 100UE 同规模 GNN +34% | reward 45,313 vs 33,843，阻塞 -58%
- D029: Size gen 决定性优势 | 20→100UE GNN 35,699 vs MLP -9,710
- D030: 论文叙事最终锁定 | 三级递进：top-K→GNN 大规模→size gen
- D031: B2-50 CUDA 崩溃 | 396维动作空间+50UE 不做额外验证
- D032: 新颖性补充检索通过 | 四要素组合无完全先例，14+组系统检索
- D033: 审计完成+M4 Jain修复 | 三章统一审计，2 CRITICAL+3 IMPORTANT，待补实验
- D034: paper-materials审计待修 | 6项数据修正+4项指标补齐+5张图
- D035: 写法规范+贡献定位修正 | 二部图GNN降级、Jain降级、贡献重定位为集中式DRL
- D036: eps_decay修复 | 原始seed=42固定episode=单场景记忆，eps_decay=20+per-episode随机化让GNN优势更显著(+22.8%)

### 活跃文件
- contract.md: projects/leo-ntn-handover-drl/contract.md (frozen v2)
- decision_log.md: projects/leo-ntn-handover-drl/decision_log.md (D001-D034)
- literature_notes.md: projects/leo-ntn-handover-drl/literature_notes.md
- baseline_report.md: projects/leo-ntn-handover-drl/baseline_report.md
- execution_report.md: projects/leo-ntn-handover-drl/execution_report.md
- novelty_search.md: projects/leo-ntn-handover-drl/novelty_search.md
- paper_materials/: projects/leo-ntn-handover-drl/paper_materials/ (6 files, ~95K)

## §4 FR 防坑检查清单

所有 FR 检查已在 Execute 阶段完成，无未决项。关键结论：
- FR-01 先验覆盖：top-K 压缩后启发式不占优，DRL 有优化空间 ✓
- FR-07 方法类型：DRL，Contract 冻结确认 ✓
- Size generalization 是独立强结论，不依赖 GNN 绝对性能提升 ✓

## §9 当前待办

eps_decay=20 同规模实验 + size gen 评估完成。具体待办：
1. **模型保存修复**：c_gnn_ddqn.py 模型文件名加 seed 后缀，重跑 20UE 3 seed（~15 min）
2. **Size gen 3 模型验证**：用修复后的 3 个独立模型跑 size gen 评估（~5 min）
3. **MLP size gen 对照**：MLP 固定输入维度预期无法迁移，需验证
4. **Ch2 paper-materials 更新**：基于 eps_decay=20 新数据重写
5. **5 张可视化图生成**
6. Phase 4 跨章元分析 + Ch1 paper-materials 重写
