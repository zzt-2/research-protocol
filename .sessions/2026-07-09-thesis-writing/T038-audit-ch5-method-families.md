# Task Brief: Ch5 六个软解调/译码方法族战略审查

> 来源: S028 | 产出位置: 本 Codex 新对话的最终答复，由主线程按 thread id 回收
> 日期: 2026-08-30
> 唯一文档: 执行方先读本文件；只按本文件列出的本地材料扩展读取

---

## 0. TL;DR（执行方先读）

你在以包含 D043、S028、T036–T038 的最新 commit 为基线创建的 `research-protocol` 隔离 worktree 中；下述路径均相对仓库根。
**你的任务**：只读审查 S027 的 Ch5 六个机制族，判断哪些在 Ch4 输出后的 APSK+BICM/LDPC 链上有真实 BER/FER headroom、彼此独立，并给唯一首轮排序。
**产出**：一份不超过 2500 汉字的战略审查，直接回复在本对话。

**最高纪律（违反一条就废了）**：
1. 不运行实验/仿真/测试，不修改文件或代码，不安装依赖。
2. 不做 web/外部文献检索或下载，不重新精读整篇论文；只用本地已有总结、决策和 worker logs。
3. 只审查 `C5-0` 至 `C5-5`；不得新建第七个方法族，不深入跨层 X-1/X-2，不写实现步骤或完整参数网格。
4. 不派子任务/新对话；约 15 分钟仍无证据就返回 `UNKNOWN`。
5. 所有事实判断给本地文件路径和行号；不把 FER 小效应或复杂度收益写成明确 BER 改善。

---

## 1. 背景（了解即可，不要逐条复述）

- Ch5 章节身份：软解调/译码可靠性，真实消费 Ch4 均衡符号和 receiver-visible reliability。
- 六族：`C5-0` 残差 LLR 校准；`C5-1` APSK 径向—切向几何 demapper；`C5-2` syndrome 引导最不可靠位救援；`C5-3` 收敛感知两阶段 NOMS；`C5-4` 选择性 BICM-ID；`C5-5` 可靠性优先调度/预算。
- 当前首轮暂定 `C5-0/C5-1/C5-2`；用户最高目标是 BER/FER 明确更好，B/C 工程收益仅后备。

优先材料：
- `.sessions/2026-07-09-thesis-writing/S027-batch-evidence-contract-and-backup-portfolio-design.md`
- `.sessions/2026-07-09-thesis-writing/decisions.md` 的 D039–D043
- `projects/thesis-fso/worker-logs/step-038-p08r2-receiver-info-repair.md`
- `projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.md`
- `projects/thesis-fso/direction-lab/harvest/ch4-decoder-feedback-method-preflight.md`

---

## 2. 任务详情

### 2.1 要回答的问题

对每个 C5 卡回答：输入是否由接收机可见；动作是否真正改变似然/译码而非缩放换名；最直接公平 baseline/等成本对手；需要什么 Ch4 后残余或 decoder 状态；更可能承重 BER/FER 还是复杂度；哪项事实会立即否决。然后给唯一首轮三张及理由。

### 2.2 执行方式

- 先核 P08-R2 小效应、MDE/oracle headroom 和旧 decoder-feedback 失败边界。
- 按“问题是否存在→输入—动作—输出→baseline→主指标→停止条件”逐卡审查。
- C5-0 与 C5-1 若最终动作都只是同一种 LLR scaling，必须合并；若一项改变二维似然几何，说明为什么仍独立。

### 2.3 产出格式（强制）

1. 一句话结论。
2. `六卡裁决表`：卡｜DESIGN_PRIORITY/CONDITIONAL/DROP_FROM_FIRST_BATCH｜headroom｜baseline｜主指标身份｜致命风险｜事实锚。该标签只表示设计排序，不是 Groundwork Go/No-Go，不建立 candidate authority。
3. `唯一首轮排序`：第 1–3 名；每项一句原因。
4. `只能当 B/C 工程后备的卡`。
5. `UNKNOWN`：缺什么本地证据。
6. `对 D042/S027 的最小修正建议`，只提建议不改文件。

---

## 3. 已知陷阱

- P08-R2 固定 NOMS 只有局部小 FER 改善，不能外推成普遍 headroom。
- 多个温度、clip、alpha/offset 近邻不能虚算多种方法。
- syndrome rescue 必须比较等成本多迭代/restart。
- BICM-ID 与 decoder feedback 基础设施成本高，不能因故事好看而放在第一优先。
- 旧 decoder-feedback C1 的自然 damage/recoverability 失败不能原样复活。

---

## 4. 验收

- [ ] 六张均有明确裁决、baseline、主指标身份和停止条件。
- [ ] 首轮排序唯一且最多三张。
- [ ] 至少 5 个事实锚含文件+行号。
- [ ] 未新增方法、未实验、未实现、未外部检索。
- [ ] 输出不超过 2500 汉字。

---

## 附：产出回传位置

本 Codex 新对话最终答复；不写仓库文件。主线程通过 thread id 回收。
