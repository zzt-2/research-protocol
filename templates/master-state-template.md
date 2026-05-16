---
project: {name}
direction: {一句话研究方向}
method_type: {DRL|监督|优化|通用}
domain: {comms|other}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
current_step: {e.g., GW-Step-4a}
current_stage: {GW|Contract|Execute}
---

# Master Agent: {project name}

## §1 角色定义

你是研究项目 `{name}` 的 Master 编排 agent。

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
- 阶段：{GW/Contract/Execute}
- 步骤：{e.g., Step 4a - 方向可行性}
- Contract 状态：{not started|draft|frozen|amended}
- 方法类型：{DRL|监督|优化|通用}

### 已完成步骤
{每步一行：}
- Step 1 (search): {date}, commit {hash}, 产出 search-archive/{date}/{slug}.json
- Step 2 (acquire): {date}, commit {hash}, {N} 篇论文已获取
- ...

### 关键决策（最近 10 条）
{从 decision_log.md 摘要，每条一行：}
- D001: {决策内容} | 原因: {why}
- D002: ...
{更早的决策只保留编号，读 decision_log.md 查全文}

### 活跃文件
- literature_notes.md: projects/{name}/literature_notes.md
- feasibility_report.md: projects/{name}/feasibility_report.md（如已创建）
- baseline_report.md: projects/{name}/baseline_report.md（如已创建）
- decision_log.md: projects/{name}/decision_log.md
- worker-logs/: projects/{name}/worker-logs/

## §3 步骤调度表

| Step | Stage file | Worker 读 | 产出 | Human? |
|------|-----------|----------|------|--------|
| 1 search | gw-search.md | tools-guide.md §2 | search-archive JSON + 候选列表 | 否 |
| 2 acquire | gw-acquire.md | tools-guide.md §3-4, search JSON | papers/*/content.md + 覆盖缺口报告 | 是（缺口确认） |
| 3 read | gw-read.md | templates.md, papers/*/content.md | literature_notes.md | 否 |
| 3.5 supplement | gw-supplement.md | literature_notes.md, tools-guide.md §2 | 更新 literature_notes.md | 否 |
| 4a feasibility | gw-feasibility.md | literature_notes.md, domain-comms.md (if comms), code-quality.md §方法论矩阵 | feasibility_report.md (A/B/D) | 是（Go/No-Go） |
| 5 validate | gw-validate.md | literature_notes.md, feasibility_report.md | Baseline 候选评估表 | 是（Baseline 确认） |
| 4b sim-feasibility | gw-feasibility.md §4b | feasibility_report.md, baseline 表 | feasibility_report.md (C/E) | 是（Go/No-Go） |
| 6 sim-design | gw-experiment.md §sim | literature_notes.md, baseline 表, code-quality.md, reference/sim-template/ | 仿真器设计规格 | 是（设计确认） |
| 7 implement | gw-experiment.md §impl | sim spec, code-quality.md, reference/sim-template/ | baseline_report.md | 否 |

## §4 FR 防坑检查清单

每个步骤完成后，检查该步骤触发的 FR 规则。失败必须报告用户并记录到 decision_log.md。

| ID | 检查内容 | 触发步骤 | 失败动作 |
|----|----------|----------|----------|
| FR-01 | 先验覆盖：简单规则在主指标上是否已达 ≥90% 最优？ | 4a (A0§6) | 主指标 ≥95% 且无次指标维度 → Kill |
| FR-02 | 性能溯源：每个性能间隙数字是否标注 [实证]/[外推]/[论证]？ | 4a (A0§1) | [外推] 不可作 Go 核心论据 |
| FR-03 | 增强基线：对比是否用竞品增强版（+合理特征）？ | 4a (A) | 增强后差距 <5% → 重新定位或 Pivot |
| FR-04 | 实例保真：MVE 简化是否保留了核心假设依赖的结构属性？ | 4a (D) | 简化移除关键特征 → 更换实例 |
| FR-05 | 竞争维度：多目标问题是否按指标维度分解？创新声称是否在未覆盖维度？ | 4a (A') | 所有维度先验覆盖都高 → Kill |
| FR-06 | 工具集成：新工具/数据源操作链路是否已写入 tools-guide.md？ | 任意 | 未文档化 → 阻塞，先更新文档 |
| FR-07 | 方法类型：确认 [DRL]/[监督]/[优化]/[通用]，跳过不适用规则 | 初始化 | 跳过时记录到 decision_log |
| FR-08 | 范式对齐：算法选择是否与领域 top-3 成功论文范式一致？ | 4a (A), 6 | 偏离须论证为何偏离+为何仍可行 |
| FR-09 | GNN 冗余：mixer 有全局状态时 GNN encoder 是否有增量信息？ | 4a (A), 6 | 无法论证增量 → 不用 GNN encoder |
| FR-10 | 空间隔离约束：是否需要显式执行（顺序选择+遮蔽）而非 RL 隐式学习？ | 4a (A), 6 | 空间隔离约束 → 优先顺序选择/mask |

### §4b 已验证失败组合

选算法前对照，命中任一组合直接排除：

| 动作空间特征 | 算法 | 失败原因 | 验证项目 |
|-------------|------|----------|----------|
| 连续分数 + top-K 选择 | PPO (Normal 分布) | top-K 不可微切断梯度 | ISL, BH |
| 离散选择 + 图结构信号 | Gaussian policy | 信用分配稀疏，噪声破坏稳定 | BH |
| 高维连续 (100+ 维) | A2C | 能力不足，训练不稳定 | RIS(竞品撤稿) |
| 空间隔离约束 + 同时决策 | 任意 RL | agent 看不到邻居动作意图 | BH(×2) |
| GNN encoder + 全局状态 mixer | QMIX/QPLEX | 信息冗余，GNN 无增益 | BH |

### §4c 症状→模式索引

收到 Worker 结果后快速匹配：

| 症状 | 可能的模式 | 参考 |
|------|-----------|------|
| PPO 训练完全不收敛 | A1 (top-K), A3 (方法不匹配) | beam-hopping, isl-scheduling |
| RL 无法超越简单先验 | A1, A2 (信号不足) | isl-scheduling, mega-constellation |
| 多算法全部失败 | A3 (问题-方法不匹配), A5 (信息冗余) | beam-hopping (×2) |
| GNN encoder 不如 FC | A5 (mixer 全局状态冗余) | beam-hopping |
| 空间隔离约束 RL 学不会 | A3, FR-10 | beam-hopping |
| 奖励被单一分量主导 | C1 (分量失衡) | 4/6 项目 |
| 小规模有效全规模崩溃 | C2 (规模), C5 (buffer) | isl-scheduling, ntn-handover |
| "零竞争"但感觉不对 | B1 (假蓝海) | beam-hopping |
| 创新点搜到竞争论文 | B2 (创新点被推翻) | mega-constellation, ris-phase |
| 仿真器跑出离谱数值 | C3 (边界 bug) | hgat, mega-constellation |
| GNN 消融几乎无贡献 | B3 (规模不匹配), A2 | ntn-handover |

### §4d 推理协议

Master 在两个时间点执行模式匹配：

**派遣前（预检）**：
1. 确认当前方法的图结构类型和动作空间类型
2. 查§4b 已验证失败组合：命中 → 排除该算法，换方案
3. 查§4a FR-08：方法是否在方法论适配性矩阵的"推荐范式"列？不在 → 需论证
4. 在 Task 文件中提醒 Worker 注意匹配到的风险模式

**接收 Worker 结果后（后检）**：
1. 读 Worker structured summary
2. 用§4c 症状→模式索引匹配：Worker 报告的异常是否匹配已知模式？
3. 匹配到 → 在 decision_log 记录模式 ID，按模式建议处理
4. 未匹配到 → 报告用户："已知模式已全部排除，可能是新问题"
5. Worker log 的"框架反馈"章节可能记录新的失败模式 → 如果发现新模式，提议更新§4b/§4c

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

### 不加载
- 论文 content.md
- 搜索结果原始 JSON
- 训练日志
- 仿真器源码

### Worker 结果处理
- Worker 返回 stdout：Master 读 structured summary（≤50 行）
- Worker log 全文：projects/{name}/worker-logs/step-{N}-{slug}.md（需要时再读）
- Master 根据 summary 判断质量 → 更新本文件和 decision_log.md

## §8 Worker 派遣协议

### 派遣前检查清单
- [ ] master-state.md 已更新
- [ ] Task 文件已写入 worker-tasks/
- [ ] 上一步产出文件已验证存在
- [ ] Task 文件中的框架文件清单与方法类型匹配
- [ ] worker-logs/ 目录存在

### 派遣后处理清单
- [ ] 读 Worker stdout 中的 structured summary
- [ ] 验证产出文件存在
- [ ] 检查该步骤的 FR 规则
- [ ] 检查质量门
- [ ] 更新 decision_log.md
- [ ] 更新 master-state.md
- [ ] 如需用户介入：呈现给用户，等待回复
- [ ] 更新 literature_notes.md 步骤进度表（如适用）
- [ ] 提交
- [ ] 准备下一步 Task 文件

### 派遣命令模板

```bash
claude -p \
  --append-system-prompt "你是无状态研究 Worker。先读任务文件 projects/{name}/worker-tasks/step-{N}-task.md，然后执行。Worker log 增量写入 projects/{name}/worker-logs/step-{N}-{slug}.md（崩溃时部分 log 必须存在）。不修改 decision_log.md 和 master-state.md。" \
  --allowed-tools "Bash Read Glob Grep Write Edit Agent" \
  --max-budget-usd {budget} \
  --effort high \
  --permission-mode bypassPermissions \
  "执行 GW Step {N}，项目 {name}。先读 projects/{name}/worker-tasks/step-{N}-task.md"
```

### 每步预算

| Step | 预算 (USD) | 超时 |
|------|-----------|------|
| 1 search | 1.0 | 10 min |
| 2 acquire | 1.5 | 15 min |
| 3 read | 3.0 | 15 min |
| 3.5 supplement | 2.0 | 15 min |
| 4a feasibility | 3.0 | 15 min |
| 5 validate | 1.5 | 10 min |
| 4b sim-feasibility | 2.0 | 10 min |
| 6 sim-design | 2.0 | 15 min |
| 7 implement | 5.0 | 15 min |

### Task 文件格式

派遣前 Master 写入 `projects/{name}/worker-tasks/step-{N}-task.md`：

```markdown
# Worker Task: Step {N} - {step name}

## 你的角色
无状态 Worker，执行一步 GW 协议。

## 必读框架文件（按顺序）
1. `{path}` — {用途}
2. `{path}` — {用途}

## 具体指令
{Master 根据项目状态填写，包含：研究方向、方法类型、已有数据路径等}

## 输出路径
- 主产出：{path}
- Worker log：projects/{name}/worker-logs/step-{N}-{slug}.md

## 质量门
{从 stage file 复制，Worker 自检用}
- [ ] {gate 1}
- [ ] {gate 2}

## 约束
- 最长运行 {N} 分钟
- 不读未列出的文件（除非执行中发现必要）
- Worker log 增量写入
- 不修改 decision_log.md、master-state.md
```

### Worker Log 格式

Worker 结束时写入 `projects/{name}/worker-logs/step-{N}-{slug}.md`：

```markdown
# Worker Log: Step {N} - {step name}

## 任务指令
{收到的指令摘要，3-5 句}

## 读取的框架文件
| 文件 | 用途 | 使用章节 |
|------|------|----------|

## 执行过程
1. {操作}: {描述} → {结果}
2. ...

### 工具使用
| 工具 | 调用次数 | 说明 |
|------|---------|------|

## 关键发现
{按步骤类型结构化：search（候选分布）、read（方法提取）、feasibility（各维度结论）等}

## 质量门自评
- [ ] {gate}: {pass/fail + 证据}

## 框架反馈
### 困惑/冲突
{框架文件中不清楚、矛盾、缺失的地方}

### 自评遗漏
{Worker 认为可能没做透的点}

## Master 摘要（≤50 行）

### 状态
- 步骤结果：{SUCCESS|PARTIAL|FAILURE}
- 质量门：{ALL_PASS|PARTIAL_PASS|FAIL}
- 需要人工：{YES|NO} — {原因}

### 产出文件
1. {路径} — {描述}

### 关键发现（3-5 条）
-

### 建议下一步
{一句话}

### 风险/警告
{Master/用户应该知道的}
```

## §9 失败恢复

### Worker 失败
1. 读 worker log（如已写入）
2. 评估：部分完成是否有价值？
3. 可修复：调整 Task 文件重新派遣（最多 2 次）
4. 不可修复：报告用户，由用户决定

### Worker 超时
1. 进程被 kill，读部分 worker log
2. 如果 Worker 在做子 agent 工作：拆分为更小的 Task
3. 减小 scope 后重试

### Master 上下文溢出
1. 完成当前步骤（尽量不中断）
2. 更新 master-state.md
3. 写 handoff 到 .session/{date}-{project}/HANDOFF-{NNN}-{slug}.md（记录派遣历史、失败详情、用户偏好）
4. 提交
5. 告知用户："上下文即将满。请开新对话，说 'resume project {name}'"

### 恢复流程
新 Master 对话按以下优先级读取：
1. master-state.md（本文件）
2. .session/ 下最新 HANDOFF
3. 当前步骤的 stage file
4. decision_log.md（最近决策）
