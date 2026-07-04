# PROMPT-001: 对话 2 — B7 评点 + B5 全文增量 + B1-B7 总表汇总

> 用于：开新对话时复制粘贴本文件全文到对话框开头
> 专题：`2026-07-02-carrier-sync-v2-deep-read`
> 来源：S003 结尾 + H002

---

## 你的身份与任务

你是**载波同步 v2 精读沉淀专题的对话 2**。上一对话（S003）已完成 B1-B6 六点评点（17 个 Q# 候选）+ v1 量级补料。本轮做三件事：**① B7 Gardner TED 评点 ② B5 全文增量核验 ③ B1-B7 总表汇总交用户排优先级**。

**先报到（session-governance Trigger 1+5）**，报到时必须 FR-26 主线独立 grep 核查 H002 至少 3 条关键事实声称（建议核查：①papers/doi/10.1016_j.optcom.2024.130981/ B5 全文是否真落盘 252 行 ②papers/_read_notes/_B6-z-odpll-opll-increment.md B6 笔记是否真存在 ③H002 §1.10 B1-B6 总计 17 个 Q# 数字）。

## 必读文件（按顺序）

1. `.sessions/2026-07-02-carrier-sync-v2-deep-read/topic-index.md`（**不变量 9 条**——动任何一条必须重新讨论）
2. `.sessions/2026-07-02-carrier-sync-v2-deep-read/H002-conversation2-b4b5b6b7-eval.md`（**本轮 handoff，最重要**）
3. `.sessions/2026-07-02-carrier-sync-v2-deep-read/S003-conversation1-supplement-download-b1b2b3-eval.md`（B1-B6 评点 17 Q# + 补下状态 + 用户手动下 3 篇结果）
4. `.sessions/2026-07-02-carrier-sync-v2-deep-read/S002-download-and-citedby-pool.md`（cited-by 池+下载状态总表）
5. `stages/gw-read.md`（14 字段+7 项结构化提取标准）
6. `.sessions/2026-06-20-problem-driven-redirection/` 下的 H020（原专题总表格式参考，grep 找最新 H### ）

## 本轮 3 件事（守 3 步上限）

### 步骤 1：B7 Gardner TED 评点（派 1 子 agent）
- 素材：`papers/doi/10.1364_ofc.2026.w2a.62/`（B7 锚 OFC 2026）+ `papers/_read_notes/10.1364_ofc.2026.w2a.62.md`（B7 旧笔记 84 行范例）+ `papers/doi/10.1109_tcom.1986.1096561/`（Gardner TED 1986 扫描 PDF md 14 行占位符，核心结论已知可不重读）+ `search-archive/2026-07-03/ofc2026-w2a-62-backward.json`（union 5）
- B7 cited-by 池空（OFC 2026 索引滞后），靠 backward refs 补池
- 派 1 子 agent 写 B7 增量笔记 `papers/_read_notes/_B7-gardner-ted-increment.md`（gw-read 14 字段+7 项含 M-C-A）

### 步骤 2：B5 全文增量核验（主线直接做，不派子 agent）
- 🔴 **用户 2026-07-04 手动下 B5 锚全文到位**：`papers/doi/10.1016_j.optcom.2024.130981/content.md`（252 行，Fan Jiamin 等青岛大学短时谱 CFO）
- 读 252 行 content.md，提取短时谱 CFO 算法细节 + 量化 dB，把 S003 §1.8 B5-Q1 从"待全文核验"升级为有全文支撑的明确判定
- 任务量小（单篇 252 行），主线直接做 ≤10 分钟

### 步骤 3：B1-B7 总表汇总交用户排优先级
- 把 S003 的 17 个 Q# + B7 新增 Q# 汇总成原专题 H020 总表格式（每行：B 点 / Q# / M-C-A 浓缩 / D006 / D005 / 范围 / 待全文）
- **本轮总表仍中性**——交用户排优先级，Go/Kill 留用户排完后对前几名做

### 可省略项
- B4/B6 补 cited-by 验证表：S003 已有 B4/B6 增量笔记，验证表是补充非必需，时间紧省略

---

## 🔴 防偏差纪律（这是第 N 次了，别再犯）

**历史教训**：本专题的开办起因就是"读了就读了啥也没留下"（原专题 B 档 12 点每点只读 1 篇零笔记）。上一专题 profile 记录的"急于推进"已复发 7 次。以下纪律每条都是历史踩坑换来的。

### 1. 守 D018 中性提取不判 Go/Kill（最重要）
- Q# 候选只标 D006/D005/范围，**禁出现**"这个方向死了/值得做/Go/Kill/应该做"判断词
- Go/Kill 是用户的，本轮总表中性，**总表阶段用户排完优先级后才对前几名做**
- "急于推进"防线：还没看全就开始判是病——本轮所有 Q# 只标不判

### 2. 守 gw-read 14 字段+7 项结构化提取（硬要求）
- **不允许只写 5 字段中性表**——本轮就是补这项被跳过的动作
- 第 7 项"问题提取"必须含 ≥1 个 M-C-A 候选 或 显式标"本篇无 Q# 候选"
- M-C-A 格式：M=baseline 方法（含具体论文+行号）/ C=条件（含物理参数）/ A=不足（具体描述）
- 范例参考：
  - `papers/_read_notes/_B3-subsystem-coordination-increment.md`（101 行）
  - `papers/_read_notes/_B6-z-odpll-opll-increment.md`（101 行，含 S024 留白复核段范例）
  - `papers/_read_notes/10.1364_ofc.2026.w2a.62.md`（B7 旧笔记 84 行）

### 3. 守子 agent 强制委托（防上下文爆炸）
- 论文全文精读必须子 agent 做，主线只接收 ≤500 词/篇摘要
- **主线严禁 WebSearch / webReader**（每次调用往上下文灌大量 HTML）
- 子 agent ≤15 分钟，一次最多 3 个并发
- 主线负责：目标设定、边界框定、结果集成、最终判断。不负责大量文本逐行消化

### 4. 守 FR-26 主线 grep 核查（防子 agent 造假/脑补）
- 子 agent 报告每条关键声称**必主线独立 grep 磁盘核查**
- dB 数字必须溯源原文（S003 §1.8 范例：核 [60]Leven 原文确认 7dB penalty @ 500MHz 真实）
- **不准脑补**——论文没报的数字不编，标"待全文"或"未量化"
- 子 agent 说"已落盘"必主线 `ls` 核查

### 5. 守 3 步上限
- 本轮 3 步配额：B7 评点 + B5 增量 + 总表汇总
- 如超 3 步主动建议分对话，写 H003 交对话 3
- 单对话执行超过 3 步上下文质量下降（profile 已验证）

### 6. D006 红线 + 范围硬门保留
- **D006**（联合建模进载波同步算法被证伪，Q12 被 Kill）：Q# 候选撞线**只标不砍**，标"撞 D006"留归档
- **范围硬门**：ISL/feeder 出界标状态（如 LEO-LEO OISL 是 ISL 出界，feeder 系统级出界）
- sat.1553 L70 已加注归档（撞 D006），不要删原文

### 7. 复用旧笔记不重写
- B7 旧笔记 `papers/_read_notes/10.1364_ofc.2026.w2a.62.md` 已 84 行，本轮写**增量段**聚焦 Gardner TED 切入点，不重写全文
- B5 旧增量笔记 `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md` 已 96 行，本轮**追加 B5-Q1 全文核验段**，不重写

---

## 本轮特殊点（必知）

1. **B5 全文用户刚手动下到位**（7-4）——B5-Q1 可从"待全文核验"升级为主线直接读 252 行核验
2. **B9 DRE（apn.3.3.036007，440 行）+ B12 MAP（oecc-psc62146，150 行）也已到位**——对话 3/4 受益，**本轮只登记"全文到位"状态不评点**
3. **B7 独立性强**——cited-by 池空（OFC 2026 索引滞后）+ backward refs 独立（Gardner TED 是定时误差检测算法层，跟 B6 OPLL 架构层不同），单独做更扎实
4. **总表阶段才开始 Go/Kill**——本轮总表中性，交用户排优先级，下轮（或用户排完后）才对前几名做 Go/Kill

## 当前已盘点状态（不必重查，直接用）

- **全文 46 篇落 v1 量级**（43 + 用户手动下 3）
- **B1-B6 已评点 17 个 Q#**（撞 D006 0 个明确撞 / D005 倾向够格 8 个 / 范围 out 3 个）
- **仍缺全文**：ao.581648（B10 高相关，Optica AO 订阅墙用户没下）+ 5 篇付费墙（ol.42.002173/ao.57.007915/tcom.1974.1092337/ao.434807/lpt.2025.3644328）

## 产出（交付物）

1. `papers/_read_notes/_B7-gardner-ted-increment.md`（B7 增量笔记 14 字段+7 项含 M-C-A）
2. `papers/_read_notes/_B5-short-time-spectrum-cfo-increment.md` 追加 B5-Q1 全文核验段
3. **B1-B7 总表**（落 S004 或原专题 H020 总表格式，交用户排优先级）
4. `.sessions/2026-07-02-carrier-sync-v2-deep-read/S004-*.md`（本轮 session note）
5. `.sessions/2026-07-02-carrier-sync-v2-deep-read/H003-*.md`（交对话 3 handoff：B8/B9/B10 评点 + literature_notes 并入）

## 结束时
- 本轮 commit 一次（结事统一，不碎提交）
- 更新 topic-index（当前位置+进展线索+last_updated）+ _registry.yaml last_updated

---

## 一句话纪律

**守 D018 中性（不判 Go/Kill）+ gw-read 14 字段+7 项（不偷懒）+ 子 agent 委托（主线不爆上下文）+ FR-26 grep 核查（不信子 agent）+ 3 步上限（不贪多）**。
