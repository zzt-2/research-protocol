# Task Brief: 从经典方法生成新的硕士级 reference-extension 候选

> 来源: S020 | 产出位置: `projects/thesis-fso/direction-lab/harvest/`
> 日期: 2026-08-13
> 唯一文档: 执行方以本 T014 为任务合同，可读取本地论文、代码、结果和 bounded search 工具

## 0. TL;DR（执行方先读）

你在 `research-protocol` 的独立 Codex worktree。Ch3 已有 CCISP，但 Ch4/独立 Ch5 仍缺方法。

**你的任务**：从公认经典、实现正确的方法出发，在当前星地相干 FSO 仿真器真实支持的目标条件中，构造新的硕士级 reference-extension 方法候选。

**产出**：一批完整方法卡、机器映射和独立 verifier 报告；本轮不进入 Groundwork、不实现、不仿真。

**最高纪律**：

1. 优先“经典 baseline + 真实场景失配 + 完整适配动作”，不是优先找无人做过的名词。
2. 候选只需可能超过正确经典 baseline；不要求超过所有近期强方法，不声称 SOTA。
3. 强邻居用于限定 claim ceiling；只有严格 exact collision、目标场景问题不存在或物理自由度不存在才淘汰。
4. 场景必须由现有代码/参数/真实论文锚点支持，禁止为了方法有用而虚构物理条件。
5. 不用 select-before-execute；硬件方法由独立 FPGA 专题处理，本任务只找算法/接收机方法。
6. 只允许对 Top 3 做小规模检索，不做大而全 novelty closure；不下载新全文。
7. 不实现、不仿真、不进入 GW/Contract/Execute，不修改 Skill/common/params/正式论文。
8. 完成后使用 task/thread 工具把五项回执自动发送给父任务 `019fccc3-f9f2-7b52-938f-b2b1dda09b10`，不要要求用户中转。

## 1. 背景

过去的方向搜索从“证明缺陷已存在、关闭所有强邻居、具备近期 task-matched baseline”才允许形成候选，实际上把 Step 4a/期刊级 novelty 责任前移到了构造阶段。结果是大量方向在形成方法卡前就被关掉。

本任务采用硕士论文的务实标准：经典 baseline 正确；目标场景下所提动作有合理增益空间；方法链完整；比较诚实；不夸大为最优。

必须先读：

- `projects/thesis-fso/direction-lab/harvest/packaging-recipe-library.md`
- `projects/thesis-fso/direction-lab/harvest/peer-thesis-method-packaging-audit.md`
- `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
- `projects/thesis-fso/direction-lab/harvest/baseline-first-method-batch-001.md`
- `projects/thesis-fso/master-state.md`
- `projects/simulation/common/` 和 simulator caller（只读语义）
- `thesis-lessons.md` 速查表和最近三条

## 2. 任务详情

### 2.1 经典 reference 池

从本地已有论文和代码中选 8–12 个经典 baseline，至少覆盖四类动作机制，例如：

- 估计器参数/结构适配；
- 多阶段或条件式恢复；
- 可靠度/置信度加权、门控或 fallback；
- 数据辅助与盲处理的组合；
- 低复杂度近似或资源约束下的算法变体；
- 同步、载波恢复、均衡或检测中的局部动作。

reference 必须有一手全文或代码实现证据。不要因为年代老而排除；经典、通行、容易正确实现正是合法 baseline 的价值。

### 2.2 构造方法卡

先生成 8–12 张初卡，再收敛到 3–5 张 survivor。每张卡必须写：

1. 可命名方法；
2. 经典 baseline；
3. 现有 testbed 明确支持的目标条件；
4. baseline 在该条件下可能失配的具体环节；
5. receiver-visible input；
6. 完整 action；
7. output/fallback；
8. 最强廉价替代；
9. 一次 0.5–1 天 defect smoke；
10. 阳性后 3–7 天 bounded package；
11. 主图和至少两个消融；
12. 强邻居与 claim ceiling；
13. Ch4/Ch5 章节落位和与 CCISP 的区分。

禁止“调一个常数”“换个标签”“把两个模块画进一张框图”作为方法。动作必须改变估计、融合、调度、反馈、状态更新或输出合同之一。

### 2.3 Top 3 bounded collision search

只对初步 Top 3 检索，总计最多 6 个 query（每候选最多 2 个），使用仓库 `tools/search`；至少 3 个实际有结果的 academic source。目的只限：

- 是否存在严格 exact action collision；
- 经典 comparator 是否合理；
- claim ceiling 应限制到何处。

metadata/abstract 不能冒充全文动作事实。没有 exact collision 证据时写 `UNRESOLVED`，不得写“首次”。检索缓存按仓库规范落盘但不提交。

### 2.4 排名

按以下顺序排序，而不是按“新颖度”排序：

1. 动作链是否完整；
2. 目标场景是否真实且由 testbed 支持；
3. defect smoke 是否 0.5–1 天可裁决；
4. bounded package 是否 3–7 天可完成；
5. 与 Ch3 的章节区分度；
6. 强邻居是否只限制表述而非 exact collision。

### 2.5 产出格式

只新增或修改以下三个文件：

1. `projects/thesis-fso/direction-lab/harvest/new-reference-extension-candidate-batch.md`
2. `projects/thesis-fso/direction-lab/harvest/new-reference-extension-candidate-batch.yaml`
3. `projects/thesis-fso/direction-lab/harvest/new-reference-extension-candidate-verifier.md`

主报告至少包含：reference 池、初始卡总表、淘汰理由、3–5 张完整 survivor 卡、Top 3 bounded search receipt、排名、章节映射和主控下一步选择输入。

## 3. 已知陷阱

- 不要再次把“最近强方法更好”当成候选无效；只要我们不声称 SOTA，经典 baseline 对比可以成立。
- 不要寻找“大空白”；从 reference 的具体动作出发，问目标场景使哪个假设失配。
- 不要使用当前仿真器没有的 PMD/PDL/CD/跨窗相关/分数定时/真实 feedback 等自由度，除非只作为明确的 future infrastructure debt，且不得列 survivor。
- 不要复活已有明确 problem absent/gate FAIL 的同一实例；可用新 reference/new action，但必须说明为什么不是改名重开。
- 不要用 oracle 当 Go baseline；oracle 只界定 headroom。
- 不要把 P01 预设为赢家，也不要与历史 lane 争夺“唯一下一包”；只交付自己的候选池。

## 4. 验收

- [ ] reference 8–12 个，至少四类动作机制，均有证据路径。
- [ ] 初卡 8–12 张，survivor 3–5 张；不足时诚实报告。
- [ ] survivor 全部具有完整 input→action→output 与 fallback。
- [ ] 每张 survivor 有真实 testbed 支持、defect smoke、bounded package、主图、消融和 claim ceiling。
- [ ] Top 3 检索不超过 6 queries，至少 3 个实际 academic source；exact collision 与 strong neighbor 分开。
- [ ] 未复活科学无效实例，未使用 select-before-execute。
- [ ] fresh-context verifier 给出 P0/P1/P2。
- [ ] 只提交三个 allowlist 文件，一次 commit，不 push；缓存与其他 dirty 不提交。
- [ ] 五项回执已自动发送父任务。

## 附：合法终态

- `NEW_REFERENCE_EXTENSION_CANDIDATES_AVAILABLE`
- `NO_NEW_CANDIDATE_SURVIVES`
- `SEARCH_OR_EVIDENCE_INCOMPLETE`
