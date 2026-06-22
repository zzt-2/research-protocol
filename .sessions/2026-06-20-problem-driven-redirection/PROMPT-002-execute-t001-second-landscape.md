# PROMPT-002：执行 T001 二次地勘 + 死轴诊断验证

> 来源: S007 | 日期: 2026-06-22
> 新对话开场词：用户会说"读 PROMPT-002 开工"

## 你的角色

你是 research-protocol 项目的执行主线（不是 reviewer，不是 explorer）。本轮任务是**执行**已定案的 T001，产出 landscape.md v3。

## 开工前必读（按优先级，本轮上下文中必须真读过，不许凭记忆）

1. **`T001-second-landscape-preflight.md`**（执行规范，自包含）—— 这是你的主任务文件
2. **`S007-landscape-v2-review-and-second-preflight-design.md`**（为什么这么设计——外部评审挑出方法中性问题，主线 push back，定案拆分方案）
3. **`topic-index.md`** 不变量段（8 条）+ 范围边界 + 处理技术边界（信道建模/AO 算处理，ATP/网络层/QKD 不算）
4. **`projects/thesis-fso/landscape.md`** v2（baseline，你要在此基础上扩到 v3）
5. **`H002-execute-landscape-preflight.md`** 偏航检查 A-E + 检索词原则（方法中性+不锁模块，H002:24/67）
6. **`S004/S005/S006`** 任选一篇快速扫（了解一次地勘的执行模式和工具链状态）

## 报到（session-governance Trigger 1）

读完必读后，按 session-governance Trigger 1 输出 Session Start Confirmation：
- 当前 topic / 原始目标 / 当前范围 / 8 条不变量
- active topic 冲突（应无）
- voice.md 状态（最近一轮 06-22 评审）
- profile.md 状态（未建——尚不足以提炼）

## 第一步：派子 agent 前过用户审检索词（用户红线）

**T001 §2.4 明令**：执行前必须把动作 A + 动作 B 检索词集**分别列给用户过目**。

用户原话（voice.md）："派子 agent 前把检索词先列出来过目"——这是偏航检查 A 的人工把关。

把 T001 §2.1（动作 A 8 主集 + 3 补集）和 §2.2（动作 B 3 死轴词 + 1 对照）列出来，明确标：
- 动作 A 必须是设备/系统词（transceiver/modem/receiver），**禁止**模块词（modulation/synchronization/equalization/channel-estimation/coding/detection）——这是 H02:24/67 明令
- 动作 B 用模块词是**受控诊断例外**，不是地勘

**等用户确认方法中性定位后才派子 agent。不要先跑。**

## 第二步：执行（用户确认后）

按 T001 §2.4 派发：
- **动作 A 和动作 B 分别派 agent**（不混在一个 agent）
- 单 agent ≤15 分钟，超时拆分
- 工具：`tools/search` + `tools/blit --source ieee`（blit 已修复可用，单 query 实际上限 25 条）
- 检索原始数据存档：动作 A 存 `search-archive/2026-06-22/landscape2-*.json`，动作 B 存 `search-archive/2026-06-22/diag-*.json`（文件名前缀区分）

## 第三步：主线合并 + 偏航检查

按 T001 §2.1/§2.2 产出格式：
- 动作 A 结果入 `## 主表（续，二次地勘新增，设备词检索）` 段（7 字段同 v2）
- 动作 B 结果入 `## 死轴冷区诊断验证（诊断，不是地勘；S007 评审后定案）` 段（对比表 + 判读）
- **动作 B 不入主表**（并入 = FAIL）

偏航检查 A-E 全跑（H02/H001 清单）：
- A：动作 A 检索词 grep 验证零模块词
- B：全留自洽 + 5 项 🔴 必填 + 无臆造
- C：不滑回开题 4 线索（VV/DPLL/SEP/编码辅助）当种子
- D：每步说清为什么
- E：跑完停一步看方法论表现

## 第四步：质量评估（停点）

landscape.md v3 落盘后，**不擅自选地**（用户锁定停点）。停下来评估：

1. **动作 A**：设备词补搜涌现了什么新地带？跟 v2 的 430 比增量多大？信号信噪比如何（多少条是"🟡 abstract 无缝信号待精读"，多少真有 abstract 证据）？
2. **动作 B**：死轴冷区占比 v2 vs B 对比，判读是加固/推翻/部分修正？区分了"人数多"和"有缝"吗？
3. **方法论表现**：T001 的拆分（A 地勘 / B 诊断）在执行中是否清晰？有没有动作 A 和 B 混淆的时刻？偏航检查有没有卡壳的地方？

## 第五步：落盘 + handoff

- **S### 编号**：执行前先扫 `.sessions/2026-06-20-problem-driven-redirection/` 确认当前最大 S 编号（截至本 PROMPT 写时是 S007，本轮执行写 S008）
- 写 `S008-second-landscape-and-diag-execution.md`，完整记录执行过程（不只是结论，按用户原话"不要只写结论"）
- 更新 topic-index：进展线索加 S008 条目，悬而未决 #6/#9 更新，当前位置更新
- 更新 voice.md（如果本轮有新的态度/约束原话）
- 更新 `_registry.yaml` last_updated + description 补 S008

## 停点纪律（不能越过）

- ❌ **不选地**（选地是 v3 产出后主线评估的事，不是本轮执行的事）
- ❌ **不进批评汇总**（要等选地后才做）
- ❌ **不改 T001**（T001 是派发时的快照，发现执行中要调，在 S008 记具体问题不回写 T）
- ❌ **不为产出放水四判据**（topic-index 不变量 2）
- ❌ **不滑回先有方法**（偏航检查 A 红线）
- ❌ **单对话超过 3 大步骤主动建议分对话**（AGENTS.md 单对话步骤上限）

## 已知陷阱（T001 §3 全部，这里只提最致命的三条）

1. **动作 A 和动作 B 混淆**（S007 评审核心教训）—— A 入主表 B 入诊断段，物理隔离。混了 = 方法论边界模糊
2. **把 S002 诊断探针当本 T 动作**—— `search-archive/2026-06-21/` 有带 `assumption`/`suboptimal`/`pll`/`costas`/`kalman` 的文件，是 S002 批评探针，不是地勘也不是本 T，不并入
3. **动作 B 死轴占比大涨直接复议 PLL**—— 占比涨只说明做的人多，物理证据（中弱湍流 σ²_R<1 压死没缝）不变

## 工具就绪状态（S005 已修复）

- `tools/search`：API 多源（S2/OpenAlex/Exa），SerpAPI 全程报 not installed 跳过
- `tools/blit --source ieee`：S005 修复后可用（safe_goto domcontentloaded + 注册表代理探测）。冷启动首次可能触发瞬态反爬限流（0 条），warm up 后稳定。建议批量时间隔 2-3s
- `tools/blit --source cnki`：可用（如需要中文，但 S002 经验窄领域信号稀疏，本轮不建议开 CNKI）

## 报告方式

执行完每个大步骤，向用户简报（数字 + 判断），不闷头跑。用户会照偏航检查清单看你偏没偏。

**遇到任何"这个我不确定"的时刻，停下来问用户，不擅自拍板。**
