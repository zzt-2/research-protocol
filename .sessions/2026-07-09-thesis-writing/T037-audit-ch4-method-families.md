# Task Brief: Ch4 五个均衡方法族战略审查

> 来源: S028 | 产出位置: 本 Codex 新对话的最终答复，由主线程按 thread id 回收
> 日期: 2026-08-30
> 唯一文档: 执行方先读本文件；只按本文件列出的本地材料扩展读取

---

## 0. TL;DR（执行方先读）

你在以包含 D043、S028、T036–T038 的最新 commit 为基线创建的 `research-protocol` 隔离 worktree 中；下述路径均相对仓库根。
**你的任务**：只读审查 S027 的 Ch4 五个机制族，判断哪些在共同 DP-(8,8)-16APSK 平台上物理合法、彼此独立、最可能产生 BER headroom，并给唯一首轮排序。
**产出**：一份不超过 2500 汉字的战略审查，直接回复在本对话。

**最高纪律（违反一条就废了）**：
1. 不运行实验/仿真/测试，不修改文件或代码，不安装依赖。
2. 不做 web/外部文献检索或下载，不重新精读整篇论文；只用本地已有总结、决策和 worker logs。
3. 只审查 `C4-0` 至 `C4-4`；不得新建第六个方法族，不写实现步骤或完整参数网格。
4. 不派子任务/新对话；约 15 分钟仍无证据就返回 `UNKNOWN`。
5. 所有事实判断给本地文件路径和行号；概率只能标“规划先验”，不得伪装成实验结论。

---

## 1. 背景（了解即可，不要逐条复述）

- Ch4 章节身份：双偏振估计/均衡，不与 Ch3 的功率驱动 CPR selector 重复。
- 共同平台：DP-(8,8)-16APSK+BICM/LDPC，相干星地 FSO，Ch5 消费 Ch4 的真实均衡输出。
- 五族：`C4-0` 时序正则 Butterfly-LS；`C4-1` scaled-unitary Jones-LS；`C4-2` APSK 环感知半盲 refinement；`C4-3` 共享支撑稀疏 Butterfly FIR；`C4-4` robust IRLS。
- 当前首轮暂定 `C4-0/C4-1/C4-2`，尚未冻结。

优先材料：
- `.sessions/2026-07-09-thesis-writing/S027-batch-evidence-contract-and-backup-portfolio-design.md`
- `.sessions/2026-07-09-thesis-writing/decisions.md` 的 D039–D043
- `projects/thesis-fso/worker-logs/step-041-p11-pilot-efficient-butterfly-fir.md`
- `projects/thesis-fso/worker-logs/step-005-pilot-jones-temporal-semantics-adjudication.md`
- `projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.md`

---

## 2. 任务详情

### 2.1 要回答的问题

对每个 C4 卡回答：receiver-visible 输入是否真实；动作是否不同于 baseline；需要什么平台自由度；最直接公平 baseline/廉价对手；预期只能承重 BER、开销还是诊断；哪项事实会立即否决。然后给唯一首轮三张及理由。

### 2.2 执行方式

- 先核历史 P11/CMA/Jones 证据，避免把已知 problem-absent 原样复活。
- 按“物理前提→输入—动作—输出→baseline→headroom→停止条件”逐卡审查。
- 如果两卡本质同族，明确要求合并，不替它们另造名字。

### 2.3 产出格式（强制）

1. 一句话结论。
2. `五卡裁决表`：卡｜DESIGN_PRIORITY/CONDITIONAL/DROP_FROM_FIRST_BATCH｜headroom｜baseline｜致命风险｜事实锚。该标签只表示设计排序，不是 Groundwork Go/No-Go，不建立 candidate authority。
3. `唯一首轮排序`：第 1–3 名；每项一句原因。
4. `不应继续的轴`：最多 3 条。
5. `UNKNOWN`：缺什么本地证据。
6. `对 D042/S027 的最小修正建议`，只提建议不改文件。

---

## 3. 已知陷阱

- P11 历史终态不是科学失败，但传统 CMA 很强；不把 Adam 标签训练当唯一 baseline。
- C4-0 与 Kalman/RLS/EMA 可能同属时间轴，不虚增方法数。
- APSK 环感知方法必须面对调好 MMA，而不只面对单模 CMA。
- 只有真实重尾/异常 pilot 才能支持 robust IRLS。

---

## 4. 验收

- [ ] 五张均有明确裁决、baseline 和停止条件。
- [ ] 首轮排序唯一且最多三张。
- [ ] 至少 5 个事实锚含文件+行号。
- [ ] 未新增方法、未实验、未实现、未外部检索。
- [ ] 输出不超过 2500 汉字。

---

## 附：产出回传位置

本 Codex 新对话最终答复；不写仓库文件。主线程通过 thread id 回收。
