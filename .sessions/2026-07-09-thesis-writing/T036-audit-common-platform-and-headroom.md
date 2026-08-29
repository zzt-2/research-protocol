# Task Brief: 共同平台、headroom 与正确性合同审查

> 来源: S028 | 产出位置: 本 Codex 新对话的最终答复，由主线程按 thread id 回收
> 日期: 2026-08-30
> 唯一文档: 执行方先读本文件；只按本文件列出的本地材料扩展读取

---

## 0. TL;DR（执行方先读）

你在以包含 D043、S028、T036–T038 的最新 commit 为基线创建的 `research-protocol` 隔离 worktree 中；下述路径均相对仓库根。
**你的任务**：只读判断共同 DP-(8,8)-16APSK+BICM/LDPC 相干星地 FSO testbed 应保留哪些真实自由度，如何分配 Ch3/Ch4/Ch5 的问题，才能既有合法 headroom 又不显得人为画靶。
**产出**：一份不超过 2500 汉字的战略审查，直接回复在本对话。

**最高纪律（违反一条就废了）**：
1. 不运行实验/仿真/测试，不修改任何文件或代码，不安装依赖。
2. 不做 web/外部文献检索或下载，不重新精读整篇论文；只用本地已有总结、决策、worker logs 和已下载材料中的现成证据锚。
3. 不设计具体实现、完整参数网格、论文措辞或新方法；每个连续参数最多建议低/中/高三个层级。
4. 不创建候选、不派子任务/新对话；约 15 分钟仍无证据就返回 `UNKNOWN`。
5. 所有事实判断给本地文件路径和行号；推断显式标 `[推断]`。

---

## 1. 背景（了解即可，不要在产出里逐条复述）

- 题目：“星地激光通信信号处理关键技术研究”。
- Ch3 已录用方法：Received-Power-Aware Adaptive CPR，核心为 `(8,8)-16APSK` per-tributary CPR。
- D040 将共同系统身份锁为 DP-(8,8)-16APSK+BICM/LDPC；Ch4/Ch5 使用完整 2×2 链。
- D041 要求未来先正确性门，再开发矩阵、PROVISIONAL 分级、fresh confirmation 和 FINAL 分级。
- D042 只有设计态方法图，尚无实验授权。

优先材料：
- `.sessions/2026-07-09-thesis-writing/decisions.md` 的 D040–D043
- `.sessions/2026-07-09-thesis-writing/S027-batch-evidence-contract-and-backup-portfolio-design.md`
- `.sessions/2026-07-09-thesis-writing/S026-thesis-title-story-fit-and-ccisp-acceptance.md`
- `projects/thesis-fso/worker-logs/step-041-p11-pilot-efficient-butterfly-fir.md`
- `projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.md`

---

## 2. 任务详情

### 2.1 要回答的问题

1. 共同发射—信道—相干接收—DSP 链最少必须有哪些块？
2. Gamma–Gamma、SOP、PDL、PMD/ISI、频偏、相噪、pilot/frame、编码分别由哪章承重，哪些只作共同背景？
3. 哪些自由度在本地证据中真实存在；哪些若加入会像人为制造问题？
4. Ch4 与 Ch5 分别出现什么 receiver-visible 诊断信号才说明存在合法 headroom？
5. 正确性 smoke 必须验证哪些语义，才能避免“能跑但链错了”？
6. 给出唯一推荐平台合同，以及必须排除的两种替代合同。

### 2.2 执行方式

- 先核 D040–D043 的不变量，再用 `rg` 定位上述本地材料的参数/失败证据。
- 只抽取与平台自由度、问题分工和 correctness 有关的事实；不深入方法公式。
- 证据冲突时保留冲突，不自行取平均。

### 2.3 产出格式（强制）

1. 一句话结论。
2. `事实锚表`：事实｜本地证据｜对平台的含义（最多 8 行）。
3. `唯一推荐合同`：共同固定项｜Ch3 专属｜Ch4 专属｜Ch5 专属。
4. `Headroom 与 smoke 门`：Ch4/Ch5 各 3–5 项。
5. `排除与未知`：明确排除两套合同；列 `UNKNOWN` 和所缺证据。
6. `主线程只需拍板的 3 件事`。

---

## 3. 已知陷阱

- 不把“把损伤都加上”当真实；自由度必须服务某章问题且有本地依据。
- 不用干净 AWGN 链得出“方法没空间”，也不用过强人工残差帮方法制造收益。
- 不把 Ch3 原实验追溯改写为 DP/coded 验证。
- 不把 Greenwood frequency 与 SOP rotation rate 混为同一参数。

---

## 4. 验收

- [ ] 结论直接回答“怎样既有 headroom 又不人为画靶”。
- [ ] 至少 5 个事实锚有文件+行号。
- [ ] 明确 Ch3/Ch4/Ch5 损伤分工和正确性 smoke。
- [ ] 无实验、实现、外部检索或新增方法。
- [ ] 输出不超过 2500 汉字。

---

## 附：产出回传位置

本 Codex 新对话最终答复；不写仓库文件。主线程通过 thread id 回收。
