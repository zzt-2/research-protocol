# Master-Worker 编排系统

> 状态: dormant | 创建: 2026-05-16 | 最后更新: 2026-05-16
> 专题目录: `.sessions/master-worker-orchestration/`
> 描述: 三层编排架构设计与端到端验证

## 进展线索

| 编号 | 文件                      | 摘要                                                                                                                                                                                                                                                                                                                                                              |
| ---- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S001 | `S001-design-and-test.md` | 三层编排架构（用户/Master/Worker）的完整设计：核心动机（规则执行层缺失）、架构决策（Worker 读框架文件、同时只开 1 个 Worker、三层状态持久化）、master-state 模板 9 章节定义、端到端测试（leo-resilient-routing 定向检索链路验证通过）、3 个已知问题（P1 框架反馈章节缺失、P2 日志重复、P3 stdout/log 关系待明确）、8 个未测试场景、成本估算（GW 全流程 8-15 USD） |

## 已确认结论

1. **Worker 读框架文件（方案 B）**：框架文件经过 6 个项目打磨，Master 翻译必然丢失细节，Worker 应自己读框架文件，Master 只负责精选指定读哪些
2. **上下文隔离是核心优势**：论文全文、搜索 JSON 等重上下文操作在 Worker 独立上下文完成，Master 只接收 ≤50 行结构化摘要，避免主对话上下文溢出
3. **同时只开 1 个 Worker**：简化状态管理、避免文件冲突、Master 能从每个 Worker 输出学习优化下一个 Task
4. **三层状态持久化**：Layer 1 master-state.md（始终最新）、Layer 2 .sessions/ handoff（对话特有上下文）、Layer 3 项目 memory（稳定跨会话信息）
5. **decision_log 由 Master 统一写**：Worker 只返回事实和发现，Master 做判断和记录，保证风格一致
6. **端到端链路验证通过**：Worker 读 Task 文件、读框架文件、执行搜索、写 worker-log、返回 stdout 摘要、不越权修改决策文件——全部通过
7. **claude -p 核心参数可用**：`--append-system-prompt`、`--allowed-tools`、`--max-budget-usd`、`--effort high`、`--permission-mode bypassPermissions` 均验证通过

## 未决项

1. **P1 框架反馈章节缺失**：Worker log 的"框架反馈"和"自评遗漏"两个章节未填写，Task 文件模板需增加显式要求，优先级中
2. **完整 GW 流程串行跑通**：9 个步骤 × N 个 Worker 的完整链路未测试，计划用 beam-hopping 项目从头测试
3. **Worker 超时/崩溃恢复**：Task 文件设计了增量写入但未实际测试
4. **Worker 内子 agent 精读论文**：`claude -p` 内开子 agent 在精读场景未测试
5. **长步骤（Step 7 implement）**：代码生成+验证，5 USD 预算是否充足待验证
6. **Master 上下文溢出恢复**：核心流程（master-state.md + handoff + commit）需跑 3+ 步骤后测试
7. **Contract/Execute 阶段扩展**：当前模板只覆盖 GW 阶段，后续需补充 Contract 和 Execute 的步骤调度表
8. **`--output-format json` 和 `--max-turns`**：可选 flags 未测试

## 当前位置

端到端链路验证通过，架构设计初版完成，待用 beam-hopping 项目跑完整 GW 流程进行实战测试。
