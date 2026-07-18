# Handoff: 三章中文文献补充

> 来源: fc2b7eb3 (materials重提取对话) | 交接目标: 在新对话中为三章 materials.md 补充中文文献引用
> 文件名: H005-chinese-literature-supplement.md

## 已完成边界

1. 三章 materials.md 已重提取为 A-G 七段式格式，经过独立审查 + 终审比对 + 数据验证，全部 PASS
2. Ch1 旧 04_literature.md 中已有 17 篇中文论文（CN01-CN17），按方向分组：LEO路由/组网(4) / 星座设计+ISL(4) / GNN综述(4) / DRL优化(3) / 抗毁性安全(2)
3. CNKI 工具链已就绪：`bash tools/blit "关键词" --source cnki` 搜期刊，`--doc-type phd` 搜博士论文，`--doc-type master` 搜硕士论文
4. 三章的 B 段（文献格局）目前只有英文论文，缺少中文文献引用

## 不要做什么

- 不要改 materials.md 的 A/C/D/E/F/G 段，只改 B 段（文献格局）
- 不要把旧的 01-06 文件当作目标——那些已不维护，materials.md 才是唯一权威
- 不要在主对话中直接跑 webSearch/webReader（会上下文爆炸）——中文文献检索用 `tools/blit --source cnki`
- 不要每找到一篇就改一次文件——先全部搜完、筛选完，最后一次性更新三个 B 段

## 必读（按优先级）

1. `.sessions/thesis-final-review/topic-index.md` — 终审结论，特别关注中文文献相关条目
2. `.sessions/2026-05-13-mega-constellation-gnn-routing/H008-0514-step5.md` — 之前的中文文献补充 handoff，包含检索关键词和方向建议
3. `projects/leo-mega-constellation-gnn-routing/paper_materials/04_literature.md` §7.9 — Ch1 已有的 17 篇中文论文列表（CN01-CN17），是参考基线
4. 三章的 `materials.md` — 当前 B 段内容，了解已有哪些英文文献
5. `tools-guide.md` §8 — blit 工具用法
6. `reference_cnki-tools.md`（记忆文件）— CNKI 工具链使用经验

## 当前中文文献状态

| 章节 | 旧文件状态 | 新 materials.md 状态 | 需补充 |
|------|-----------|---------------------|--------|
| Ch1 (GNN routing) | 04 中有 CN01-CN17 (17篇) | B 段无中文文献 | 需迁移+可能扩充 |
| Ch2 (Handover DRL) | 已补充 18 篇（审计报告） | B 段无中文文献 | 需迁移+确认 |
| Ch3 (Congestion routing) | 未确认 | B 段无中文文献 | 需全新搜索 |

## 具体任务

### Step 1: 回顾之前的做法
- 读 Ch1 的 04_literature.md §7.9，看之前怎么组织的中文文献（格式、分组、引用理由）
- 读 Ch2 的 04_literature.md 看是否也有中文文献段
- 确定统一的中文文献格式规范

### Step 2: 为三章搜索中文文献
每章用 `tools/blit --source cnki` 搜索，覆盖方向：

**Ch1 (GNN routing)**:
- 关键词："低轨卫星 路由 综述"、"巨型星座 路由算法"、"图神经网络 卫星网络"、"星间链路 低轨卫星"
- 预期：17 篇旧有 + 可能新增 3-5 篇

**Ch2 (Handover DRL)**:
- 关键词："低轨卫星 切换"、"卫星网络 切换决策"、"深度强化学习 切换"、"非地面网络 移动性管理"
- 预期：需确认旧有 18 篇具体内容，可能需要补充

**Ch3 (Congestion routing)**:
- 关键词："卫星网络 拥塞控制"、"低轨卫星 流量工程"、"卫星网络 负载均衡"、"故障恢复 卫星网络"
- 预期：全新搜索，约 10-15 篇

**通用方向（三章共享）**：
- GNN 综述中文版、DRL 网络优化综述、LEO 星座设计综述
- 这些可以在三章之间交叉引用

### Step 3: 筛选与组织
- 学位论文要求：中文参考文献占比约 10-15%
- 三章合计约 200 篇英文 → 需约 20-30 篇中文
- 优先级：通信学报 > 电子与信息学报 > 计算机学报 > 宇航学报 > 其他
- 每篇给：cite key (CN01-CNxx)、标题、作者、年份、来源、引用理由
- 按方向分组，与英文文献的角色定位一致（竞品/前驱/方法参考/综述）

### Step 4: 更新 materials.md B 段
- 在 B.1 文献角色速览表末尾追加中文文献条目
- 或新建 B.1x 子段"中文学术文献"
- 保持 B.2 竞品区分表不变（中文文献一般不是竞品）

## 接口变更

无代码改动，只编辑三个 markdown 文件。

## 验证阈值

| 验证项 | PASS 标准 |
|--------|----------|
| 中文文献数量 | 每章 ≥10 篇，三章合计 ≥30 篇 |
| 期刊质量 | ≥60% 来自核心期刊（通信学报/电子学报/计算机学报等） |
| 格式一致 | 三章使用统一的中文文献格式 |
| 与 B 段整合 | 中文文献有引用角色标注，非孤立列表 |
| 去重 | 三章之间的通用中文文献（如 GNN 综述）不重复计数 |

## 接收方验证

- [ ] 已读取 Ch1 04_literature.md §7.9 了解之前的中文文献组织方式
- [ ] 已确认 blit --source cnki 工具可用
- [ ] 已确认三章 B 段当前内容
- [ ] 已检查 _registry.yaml 中本专题状态

## 下一轮

1. 新对话开始后先读本 handoff + Ch1 04_literature.md §7.9
2. 用子 agent 并行搜索三章的中文文献（主对话不直接搜）
3. 筛选+组织后一次性更新三个 materials.md
