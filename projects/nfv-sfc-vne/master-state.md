---
project: nfv-sfc-vne
direction: GNN 双层图匹配 + SFC 依赖链约束的虚拟网络嵌入联合优化
method_type: DRL
domain: comms
created: 2026-05-18
updated: 2026-05-18
current_step: GW-Step-4a
current_stage: GW
---

# Master Agent: nfv-sfc-vne

## §1 角色定义

你是研究项目 `nfv-sfc-vne` 的 Master 编排 agent。

**职责：**
- 持有项目全局状态（本文件 + decision_log.md）
- 通过 `claude -p` 派遣 Worker 执行具体步骤
- 判断 Worker 输出是否通过质量门
- 在 [MUST human] 标记的节点询问用户
- 在检查点提交 git commit

**禁止：**
- 直接读论文 content.md（Worker 做）
- 直接跑 WebSearch / webReader（Worker 做）
- 直接跑长时脚本（Worker 做）
- 未经用户确认做 Go/No-Go 决策
- 一次性派遣多个 Worker（同时只开一个子对话）

## §2 项目状态

### 当前位置
- 阶段：GW
- 步骤：Step 5 完成（Baseline 选定），进入 Step 4b（仿真条件+资源风险验证）
- Contract 状态：not started
- 方法类型：DRL

### 已完成步骤
- Step 1 (search): 复用方向侦察搜索结果（2026-05-16/17/18），25+ 搜索文件覆盖 NFV/SFC/VNE，满足质量门槛
- Step 2 (acquire): 2026-05-18，17 篇获取成功（9 arXiv + 6 DOI + 1 已有 + 1 bonus），0 失败
- Step 3 (read): 2026-05-18，9 篇精读完成，literature_notes.md 已创建（313行）
- Step 4a (A0/A'/A/B): 2026-05-18 在方向侦察 S002 中完成，全部通过，Go 决策已确认
  - A0: 性能间隙✅(接受率差20.7%、收入差36.2%) 问题结构适配✅(图到图映射) 跨域先例✅(c=159) MDP非平凡✅
  - A': 跨规模泛化维度覆盖=0，全新竞争维度
  - A: GNN参数共享→跨不同substrate规模零样本迁移
  - B: 新颖性确认(0篇精确交叉) 可行性强(SizeShiftReg+Virne) 空白原因=技术刚解锁
- Step 3.5 (supplement): 2026-05-18，Round 1 收敛。新增 8 篇论文（GraphVNE/FlagVNE/CONAL/GPG-VNFE/ReViNE/ICC2025-SFC/DRL-BSFC + 1篇下载错误）。关键发现：(1) GraphVNE graph matching 非真正 assignment；(2) FlagVNE 仅跨 VNR size 不跨 PN；(3) SFC 依赖链+matching 无直接竞品。差异化空间确认。
- Step 4a D (MVE): 2026-05-18，已完成。MVE PASS。GNN(DualGAT) epoch1: AC=0.966, R2C=0.748 > MLP(30ep) AC=0.942, R2C=0.682 > GRC AC=0.880, R2C=0.543。R2C GNN vs MLP +9.7%。feasibility_report.md 已创建。
- Step 4a: A0/A'/A/B/D 全通过，建议 Go，待用户确认。

### 关键决策（最近 10 条）
- D001: 方向侦察 Go 决策：#1 NFV/SFC 双层图匹配 + SFC 依赖链 | 原因: A0/A'/A/B 全通过，空白确认(0篇精确交叉)
- D002: 核心卖点定位为"双层图上的VNE联合优化" | 原因: 避免"跨规模泛化"与 Ch3 leo-congestion-routing 撞车
- D003: GNN 架构走 Node-Edge 联合嵌入（matching-style）| 原因: 与 hgat-dag 的 HGAT 拉开距离
- D004: 跨规模降级为论文级共享特性 | 原因: Ch3 已占据跨规模泛化作为核心贡献
- D005: 论文统一叙事"GNN 驱动的 LEO 网络多层智能优化" | 原因: Ch3=流量路由(调度层), 本项目=服务放置(编排层), 双层图 vs 单层拓扑
- D006: Step 4a Dimension D (MVE) 需补做 | 原因: 组合新颖性方向不应跳过 MVE
- D007: Step 1 复用方向侦察搜索结果 | 原因: 25+ 搜索文件，满足所有质量门槛
- D008: Step 3.5 收敛确认 | 原因: Round 1 精读后无新盲区，SFC 依赖链+matching-style GNN 无直接竞品
- D009: 核心差异化 = SFC 依赖链约束 + matching-style GNN（vs GraphVNE 特征增强）| 原因: GraphVNE IPFP 不可微且仅提取标量分数；FlagVNE/CONAL 不处理 SFC；跨规模作为辅助亮点
- D010: Step 4a Go 建议 | 原因: A0/A'/A/B/D 全通过，MVE 实证 GNN vs MLP R2C +9.7%，待用户确认
- D011: Baseline 选定 | 原因: B1 GRC(启发式)+B2 PPO-DualGAT+(SOTA)+B3 pg_mlp(MLP消融)+B4 CONAL(约束竞品)+B5 PPO-DualGCN(GNN变体)，全部 Virne 内置

### 活跃文件
- literature_notes.md: projects/nfv-sfc-vne/literature_notes.md ✅（13篇精读+11篇浅读+补充检索更新+Baseline交叉验证）
- feasibility_report.md: projects/nfv-sfc-vne/feasibility_report.md ✅（A0/A'/A/B/D 全维度评估完成，MVE PASS）
- baseline_report.md: projects/nfv-sfc-vne/baseline_report.md（待创建）
- decision_log.md: projects/nfv-sfc-vne/decision_log.md ✅（D001-D007）
- worker-logs/: projects/nfv-sfc-vne/worker-logs/
- search-archive: 复用 search-archive/2026-05-{16,17,18}/ 中 NFV/SFC/VNE 相关文件

## §3 步骤调度表

| Step | Stage file | Worker 读 | 产出 | Human? | 状态 |
|------|-----------|----------|------|--------|------|
| 1 search | gw-search.md | tools-guide.md §2 | search-archive JSON + 候选列表 | 否 | ✅ 复用 |
| 2 acquire | gw-acquire.md | tools-guide.md §3-4, search JSON | papers/*/content.md + 覆盖缺口报告 | 是（缺口确认） | 进行中 |
| 3 read | gw-read.md | templates.md, papers/*/content.md | literature_notes.md | 否 | 待开始 |
| 3.5 supplement | gw-supplement.md | literature_notes.md, tools-guide.md §2 | 更新 literature_notes.md | 否 | ✅ 完成(Round 1 收敛) |
| 4a feasibility | gw-feasibility.md | literature_notes.md, domain-comms.md, code-quality.md | feasibility_report.md (A/B/D) | 是（Go/No-Go） | A0/A'/A/B/D✅ 待用户确认Go |
| 5 validate | gw-validate.md | literature_notes.md, feasibility_report.md | Baseline 候选评估表 | 是（Baseline 确认） | ✅ B1-B5选定 |
| 4b sim-feasibility | gw-feasibility.md §4b | feasibility_report.md, baseline 表 | feasibility_report.md (C/E) | 是（Go/No-Go） | ✅ C/E无致命，Go待确认 |
| 6 sim-design | gw-experiment.md §sim | literature_notes.md, baseline 表, code-quality.md, reference/sim-template/ | 仿真器设计规格 | 是（设计确认） | 待开始 |
| 7 implement | gw-experiment.md §impl | sim spec, code-quality.md, reference/sim-template/ | baseline_report.md | 否 | 待开始 |

## §4 FR 防坑检查清单

| ID | 检查内容 | 触发步骤 | 失败动作 |
|----|----------|----------|----------|
| FR-01 | 先验覆盖：简单规则在主指标上是否已达 ≥90% 最优？ | 4a (A0§6) | 主指标 ≥95% 且无次指标维度 → Kill |
| FR-02 | 性能溯源：每个性能间隙数字是否标注 [实证]/[外推]/[论证]？ | 4a (A0§1) | [外推] 不可作 Go 核心论据 |
| FR-03 | 增强基线：对比是否用竞品增强版（+合理特征）？ | 4a (A) | 增强后差距 <5% → 重新定位或 Pivot |
| FR-04 | 实例保真：MVE 简化是否保留了核心假设依赖的结构属性？ | 4a (D) | 简化移除关键特征 → 更换实例 |
| FR-05 | 竞争维度：多目标问题是否按指标维度分解？创新声称是否在未覆盖维度？ | 4a (A') | 所有维度先验覆盖都高 → Kill |
| FR-06 | 工具集成：新工具/数据源操作链路是否已写入 tools-guide.md？ | 任意 | 未文档化 → 阻塞，先更新文档 |
| FR-07 | 方法类型：确认 [DRL]，跳过不适用规则 | 初始化 | 跳过时记录到 decision_log |
| FR-08 | 范式对齐：算法选择是否与领域 top-3 成功论文范式一致？ | 4a (A), 6 | 偏离须论证为何偏离+为何仍可行 |
| FR-09 | GNN 信息冗余检查 | 4a, 6 | GNN 输入特征存在冗余 → 降维 |
| FR-10 | 空间隔离约束决策模式 | 6 | 动作空间必须覆盖所有 baseline |
| FR-11 | MVE 架构溯源 | 4a (D) | MVE 结果必须含架构摘要 |
| FR-12 | MVE→Formal 架构差异门控 | 6 | 正式设计与 MVE 差异影响对比 → 重验证 |
| FR-13 | 动作空间表达力下界审计 | Contract S4 | data-flow.md 必须审计模型决策空间覆盖 |

### §4b 经验推理协议

**当前方法**：GNN (Node-Edge 联合嵌入, matching-style) + DRL

**已知风险预判**：
- 图结构：双层图（substrate + VNR），非规则，GNN 天然适配 ✅
- 动作空间：VNE 是离散组合决策（节点映射+链路映射），需确认表达力
- 规模变化：substrate 规模可变，VNR 规模可变，size generalization 有意义 ✅
- 查 code-quality.md 方法论适配性矩阵确认推荐范式

**Worker 返回后症状监控**：
- GNN 消融无贡献 → 查 B3 (规模不匹配)
- RL 不收敛 → 查 A1 (top-K 不匹配), A3 (方法-问题不匹配)
- 奖励被单一分量主导 → 查 C1 (分量失衡)

### §4c 症状-模式快速索引

| Worker 可能报告的症状 | 应查的模式 | 触发步骤 |
|----------------------|-----------|----------|
| PPO 训练完全不收敛 | A1, A3 | 7 |
| RL 无法超越简单先验/启发式 | A2, FR-01 | 4a, 7 |
| 奖励被单一分量主导 (>80%) | C1 | 6, 7 |
| 小规模有效、全规模崩溃 | C2, C5 | 7 |
| GNN 消融几乎无贡献 | B3, A2 | 4a, 7 |
| 仿真器跑出离谱数值 | C3 | 7 |
| "零竞争"但感觉不对 | B1 | 1, 4a |

## §5 决策权限

| 决策类型 | 谁决定 | 示例 |
|----------|--------|------|
| Go/No-Go（方向） | **用户确认** | Step 4a 结论 |
| Go/No-Go（仿真） | **用户确认** | Step 4b 结论 |
| Baseline 选定 | **用户确认** | Step 5 候选表 |
| 仿真器设计 | **用户确认** | Step 6 规格 |
| 覆盖缺口处理 | **用户确认** | Step 2 缺口报告 |
| 步骤完成质量 | Master 判断 | 质量门 pass/fail |
| Worker 重试/调整 | Master 决定 | 失败处理 |
| 低风险操作决策 | Master 决定 | 搜索关键词、下载顺序 |

## §6 提交检查点

| 触发条件 | commit 消息格式 |
|----------|----------------|
| Worker 完成一个步骤 | `{step} 完成: {摘要}` |
| Go/No-Go 决策确认 | `Go/No-Go: {decision} ({step}). D{NNN}` |
| 用户手动操作后 | `manual: {用户做了什么}` |
| 对话即将结束 | `checkpoint: {current_step} 状态保存` |

## §7 上下文管理规则

### 常驻（始终在上下文）
- 本文件（master-state.md）
- decision_log.md 最近 10 条
- 当前步骤的 stage file（Master 进入新步骤时读）

### 按需读取
- decision_log.md 全文（历史决策查询时）
- literature_notes.md（Step 3.5 以后）
- feasibility_report.md（Step 4b 以后）
- baseline_report.md（Step 6 以后）
- Worker log 全文（需要审计时）
- code-quality.md（Step 4a/6/7 派遣前）

### 不加载
- 论文 content.md
- 搜索结果原始 JSON
- 训练日志
- 仿真器源码

## §8 Worker 派遣协议

### 派遣前检查清单
- [ ] master-state.md 已更新
- [ ] Task 文件已写入 worker-tasks/
- [ ] 上一步产出文件已验证存在
- [ ] Task 文件中的框架文件清单与方法类型匹配
- [ ] worker-logs/ 目录存在

### 每步预算

| Step | 预算 (USD) | 超时 |
|------|-----------|------|
| 2 acquire | 1.5 | 15 min |
| 3 read | 3.0 | 15 min |
| 3.5 supplement | 2.0 | 15 min |
| 4a feasibility (D only) | 3.0 | 15 min |
| 5 validate | 1.5 | 10 min |
| 4b sim-feasibility | 2.0 | 10 min |
| 6 sim-design | 2.0 | 15 min |
| 7 implement | 5.0 | 15 min |

## §9 失败恢复

### Worker 失败
1. 读 worker log（如已写入）
2. 评估：部分完成是否有价值？
3. 可修复：调整 Task 文件重新派遣（最多 2 次）
4. 不可修复：报告用户，由用户决定

### Master 上下文溢出
1. 完成当前步骤（尽量不中断）
2. 更新 master-state.md
3. 写 handoff 到 .session/{date}-{project}/H{NNN}-{slug}.md
4. 提交
5. 告知用户："上下文即将满。请开新对话，说 'resume project nfv-sfc-vne'"
