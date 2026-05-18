# PROMPT: 审计精读提取遗漏 + 修复流程

## 任务

查清楚为什么 Step 3（精读）和 Step 3.5（补充检索精读）没有按 `templates.md` 提取以下两个模板，然后修复流程确保后续不再遗漏。

### 两个必须提取的模板

1. **实验完备性提取模板**（`templates.md` §"实验完备性提取模板"）
   - 每篇精读论文必须提取：声称清单、声称 scope、统计规范性（seeds/error bar/统计检验）、Baseline 矩阵、消融设计、信道模型、拓扑多样性、复杂度报告、VVUQ
   - 结果写入 `literature_notes.md` 每个文献条目的"实验完备性"子节
   - 控制篇幅 ≤20 行/篇

2. **声称-证据映射表**（`templates.md` §"声称-证据映射表"）
   - Contract Step 2/5 用，从论文声称倒推实验需求

### 要查的

1. 读 `stages/gw-read.md`，确认框架文件是否有明确要求这两个提取
2. 搜索上一个对话的历史记录（session_search 搜 "gw-read" "精读" "worker-tasks" 等关键词），找到 Step 3 的 worker 派遣 prompt
3. 查看 `projects/nfv-sfc-vne/worker-logs/` 下 Step 3 的 worker 日志
4. 判断遗漏发生在哪一层：
   - 框架文件 `gw-read.md` 没写要求？→ 修改 `gw-read.md`
   - 框架文件写了但 worker 任务文件没包含？→ 修改 master 派遣流程或 worker-tasks 模板
   - worker 任务包含了但 worker 没执行？→ Worker 质量门问题

### 修复要求

- **必须**找到根因并修改对应的源头文件（框架文件 or 模板 or 派遣协议）
- 不要只修本次项目的数据，要修流程确保其他项目也不再遗漏
- 修改后，对 nfv-sfc-vne 的 13 篇精读论文补提取（实验完备性模板，可用子 agent 并行，每篇从 content.md 提取）
- 声称-证据映射表可以留到 Contract 阶段，但流程要确保不漏

### 相关文件

- `stages/gw-read.md` — Step 3 框架文件
- `templates.md` — 两个提取模板的定义
- `projects/nfv-sfc-vne/literature_notes.md` — 当前精读笔记（缺少实验完备性子节）
- `projects/nfv-sfc-vne/worker-logs/` — Step 3 worker 日志
- `CLAUDE.md` — 全局规则（框架文件是执行规范、转步骤必须先读）

### 恢复上下文

先读：
1. `projects/nfv-sfc-vne/master-state.md`（项目状态）
2. `stages/gw-read.md`（Step 3 框架）
3. `templates.md` §"实验完备性提取模板" 和 §"声称-证据映射表"
4. 用 `session_search` 搜 "nfv-sfc-vne" + "精读" 找历史对话
