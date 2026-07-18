# Handoff: 开题报告写作

> 来源: fc2b7eb3 (materials重提取+中文文献对话) | 交接目标: 在新对话中完成开题报告撰写
> 文件名: H006-proposal-writing.md

## 已完成边界

1. 三章 materials.md 已完成 A-G 七段式提取，经过独立审查+终审比对+数据验证+中文文献补充，全部 PASS
2. Ch1: 22 篇中文文献（CN01-CN22），Ch2/Ch3 各有中文文献
3. 跨章元分析框架"探索性分化"已写入三章 C 段
4. 跨章符号统一已写入三章 F 段
5. 用户将在新对话提供开题报告模板

## 不要做什么

- 不要改 materials.md，它们是写作素材不是写作目标
- 不要凭空编造数据——所有数字必须能追溯到 materials.md 的 E 段
- 不要把三章写成三个独立报告——开题报告是一个整体，需要统一的背景→现状→方案叙事
- 不要在主对话跑 webSearch/webReader——子 agent 里做
- 不要一上来就写正文——先定义结构、再写大纲、最后逐节写

## 必读（按优先级）

### 素材层（研究协议项目）

1. **三章 materials.md** — 写作的唯一数据来源
   - `/mnt/d/code/study/research-protocol/projects/leo-mega-constellation-gnn-routing/paper_materials/materials.md`
   - `/mnt/d/code/study/research-protocol/projects/leo-ntn-handover-drl/paper_materials/materials.md`
   - `/mnt/d/code/study/research-protocol/projects/leo-congestion-routing/paper_materials/materials.md`
2. **`.sessions/thesis-final-review/topic-index.md`** — 终审结论，特别是跨章统一部分
3. **`.sessions/thesis-structure-research/topic-index.md`** — 论文结构研究，含三章模式、写作规范
4. **`.sessions/thesis-structure-research/R003-writing-norms-contribution-claims.md`** — 贡献声称模板、动词层级、局限性写作规范

### 质量参考层（thesis-platform 项目）

5. **thesis-platform paper-eval S026 坏模式清单** — 写作时必须避开的 25 个坑
   - 路径：`/home/zzt/code/thesis-platform/.sessions/2026-05-15-paper-evaluation/` 中找 S026 相关文件
6. **thesis-platform writing-guide** — 反模式 + 正面范例
   - 路径：`/home/zzt/code/thesis-platform/workflows/paper-eval/` 中找 _writing-guide 或 _system 相关文件
7. **thesis-platform good-examples** — 52 个博士论文正面范例（含通信方向）
   - 路径：`/home/zzt/code/thesis-platform/workflows/paper-eval/` 中找 _good-examples 相关文件
8. **thesis-platform S030 跨层级校准结论** — 什么质量检测有效，用于自查
   - 路径：`/home/zzt/code/thesis-platform/.sessions/2026-05-15-paper-evaluation/topic-index.md`

### 领域参考层

9. **本领域博士/硕士论文** — 需要用 CNKI 或 blit 搜索 LEO 卫星路由方向的学位论文作为写作质量锚点
   - 搜索关键词："低轨卫星 路由 博士论文"、"卫星网络 图神经网络 学位论文"
   - 工具：`bash tools/blit "关键词" --source cnki --doc-type phd`

## 跨章一致性要求

开题报告是一个整体文档，必须保证：

1. **统一研究主题**：三章围绕"LEO 卫星网络中 GNN 的有效性探索"展开
2. **元分析框架**："探索性分化"——GNN 有效性取决于架构复杂度与任务需求匹配
   - Ch1: 规模不变性（规则拓扑 + 监督学习）
   - Ch2: 规模适应性（排列等变性 + DRL）
   - Ch3: 故障弹性（结构漂移下的鲁棒性）
3. **符号统一**：使用 S011 确定的跨章符号方案
4. **延迟模型差异**：Ch1 纯传播延迟 / Ch2 无显式延迟 / Ch3 拥塞惩罚权重——绪论中必须说明
5. **贡献定位**：Ch1=系统性验证、Ch2=规模适应性实证、Ch3=故障弹性实证——不自夸"首次"

## 具体任务

### Phase 0: 准备（开对话后立即做）
1. 读用户提供的开题报告模板
2. 读 R003 写作规范
3. 读 thesis-platform 的 writing-guide 和 bad-patterns（子 agent 做，返回摘要）
4. 搜 2-3 篇本领域优秀博士/硕士论文（子 agent 用 blit --source cnki 搜），了解写作范式

### Phase 1: 定义结构
1. 根据模板 + 三章 materials 的 A 段（研究问题）定义各节结构
2. 确定哪部分是统一的（背景、现状）、哪部分分章展开（方案、技术路线）
3. 大纲产出：节标题 + 每节 1-2 句要点 + 预计字数

### Phase 2: 逐节写正文
按节的独立性分配子 agent：
- **研究背景与意义**（统一段）：从三章 A.1+A.4 合成
- **国内外研究现状**（统一段）：从三章 B 段合成，按方向分组而非按章分组
- **研究内容**（三章分述）：每章的 C 段
- **研究方案与技术路线**（三章分述）：每章的 D 段
- **研究计划与进度安排**：时间线
- **参考文献**：三章 B 段文献合并去重

每个子 agent 注入：
- 对应的 materials.md 段落
- writing-guide 摘要（反模式 + 正面范例）
- 开题报告模板的格式要求

### Phase 3: 质量自查
用 S026 的坏模式清单逐项检查：
- A 层 9 项（结构缺失检测）
- B 层 8 项（内容质量检测）
- C 层 8 项（表达质量检测）
- 修改直到全部通过

## 接口变更

无代码改动。产出物：一个完整的开题报告 markdown 文件。

## 验证阈值

| 验证项 | PASS 标准 |
|--------|----------|
| 模板符合 | 每个模板要求的节都存在 |
| 数据可溯源 | 所有数字能追溯到 materials.md E 段 |
| 跨章一致 | 符号/术语/叙事无矛盾 |
| 坏模式检查 | S026 的 A 层 ≤3 hits |
| 字数 | 符合学校要求（通常 5000-8000 字正文） |
| 参考文献 | 中文 ≥10 篇，总 ≥50 篇，三章文献合并去重 |

## 接收方验证

- [ ] 已读取用户提供的开题报告模板
- [ ] 已读取 R003 写作规范
- [ ] 已确认三章 materials.md 的当前内容
- [ ] 已浏览 thesis-platform 的 writing-guide 摘要
- [ ] 已搜索至少 1 篇本领域学位论文作为参考

## 下一轮

1. 新对话开始后先读本 handoff + 用户提供的模板
2. Phase 0 准备工作（子 agent 读 thesis-platform 参考材料）
3. Phase 1 定义结构后与用户确认
4. Phase 2 逐节写作
5. Phase 3 质量自查
