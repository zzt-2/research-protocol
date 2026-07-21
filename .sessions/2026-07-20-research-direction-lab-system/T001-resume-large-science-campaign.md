# Task Brief: 用轻量 Probe 恢复并连续推进大规模科学 campaign

> 来源: S012 | 产出位置: `projects/thesis-fso/direction-lab/` 与 `.sessions/2026-07-20-direction-lab-science-scout/`
> 日期: 2026-07-21
> 唯一文档: 执行方以本任务书为主，并按其中“必读”恢复仓库事实

---

## 0. TL;DR（执行方先读）

你在 `D:\code\study\research-protocol\.worktrees\direction-lab-capability-atlas`，分支 `codex/direction-lab-capability-atlas`。通用 `research-direction-lab` Skill 已增加轻量 `Probe → Scout → Deep Evidence`、科学语义先行、current projection 和抗膨胀记录方式。

**你的任务**：先把科学专题的现行结论投影到有界 current view，再围绕“双偏振星地 OSL 中合法 ML 信息增量”连续推进多个机制分支；小问题用 Probe，信号通过后才升级 Scout，稳定且论文重要时才进入 Deep Evidence。不要做完一个 Probe 就停下来等用户。

**产出**：可快速恢复的 current state/portfolio/harvest、若干轻量 Probe 或合法 Scout 的科学结果、毕业论文素材索引、一个普通中文总结和一次收尾提交。

**最高纪律（违反一条就废了）**：

1. 必须使用 `research-direction-lab` Skill；先读 `SKILL.md` 全文和它路由到的相关 references。
2. 先恢复 H010/D016 的有效科学状态；不得复述已撤回的 C04/C09 mechanism negative、learned-target-ready 或 thesis-grade exists-vs-learnable 解释。
3. artifact/provenance PASS 不等于科学语义 PASS；任何扩算力前先检查目标对齐、常数/平凡解、identity、输出支撑、最小过拟合、简单 comparator 和信息边界。
4. 一个局部 blocker、Probe FAIL 或候选负面不得终止 campaign；只要还有合法分支，就轮转继续。
5. 通用 Skill/core 不得写入通信项目语义；公式、符号、物理参数和 baseline 必须有可核验来源。baseline 只需正确、任务适配、广泛采用且公平，不默认追 SOTA。
6. 不修改 B001–B003、P03 Atlas、旧 raw artifacts 或 canonical history；不创建 legacy B004；Scout 数字不自动写入论文正文。
7. 普通 Probe 默认只留一个 compact record；不要为它制造 receipt/verifier/synthesis/session/handoff 全套。只有 Scout/Deep Evidence 按风险增加证据链。
8. 整个对话持续推进，不逐小步请示；只有战略范围扩张、不可逆操作或所有合法路径耗尽时才停下来问用户。每个对话只在收尾提交一次，不 push。

## 1. 背景

当前可信科学状态：

- C11 的合法因果 raw-decision policy 在当前局部切片无收益；结论上限为 LOCAL_SLICE/DIAGNOSTIC，不外推方法族。
- truth-assisted affine gap 只保留 LOCAL_SLICE/DIAGNOSTIC；blind-affine 是 receiver-visible comparator，oracle affine 只作 Kill bound。
- C04/C09 旧 raw 坏结果可复现，但 soft-distance 目标存在输入无关常数最优解；候选为 `IMPLEMENTATION_CONFOUND_CONSTANT_COLLAPSE / UNRESOLVED`。
- Portfolio 已有 C01–C13。C05/C08/C10/C11 已运行；C04/C09 需语义重构前置 Probe；C01/C02/C06/C13 为 `NEEDS_SMALL_ADAPTER`；C03/C07/C12 为 `INFRASTRUCTURE_BLOCKED`。
- detector 的传统 min_z2 comparator 在两个 two-class cells 上 AUROC 到顶，但 lead time 均不为正；若继续 detector，目标只能是 lead time、校准或跨条件泛化，不能把 AUROC 当可赢空间。
- 当前 `STATUS.v1.md` 和旧 `portfolio/current.v1.yaml` 仍是较早的 read-only projection，不能覆盖 H010/D016。第一步是有界对账，不是全历史考古。

这是论文前的开放方向发现层。只有出现稳定候选后，才另走 Groundwork/Contract/Execute 正式晋级。

## 2. 任务详情

### 2.1 Phase 0：有界恢复与 current view 对账

按顺序读取：

1. `.sessions/2026-07-20-research-direction-lab-system/H004-probe-recovery-ready.md`
2. `.sessions/2026-07-20-direction-lab-science-scout/H010-s009-semantic-audit-recovery.md`
3. 科学专题 `topic-index.md` 的不变量、D016、V005
4. `projects/thesis-fso/direction-lab/project.v1.yaml`
5. 现有 STATUS/state/portfolio/harvest current files

验证至少三条 H010 事实后，渐进建立或更新：

- `state/current.yaml`：当前授权、最新有效结论、显式 dispositions、下一动作；
- `portfolio/current.yaml`：C01–C13 当前状态与证据指针；
- `harvest/current.yaml`：active/amended/retracted/diagnostic 当前索引；
- `STATUS.md` 或项目现行 STATUS 入口：只投影八问和上述 current pointers；
- Project Adapter 的可选 `probes/portfolio_history/harvest_current` 路径。

旧文件不删除、不批量重写；用显式 amendment/disposition 表达取代关系，不按 mtime 猜当前结论。完成后立即进入科学工作，不把迁移扩成独立工程。

### 2.2 Phase 1：建立并行机制工作面

从完整现有 Portfolio 而不是单一 winner 出发，至少保持两个机制不同且合法可工作的分支。首轮优先评估：

- C04/C09：只做“修正后的目标是否有输入依赖、能否过常数/identity/最小过拟合”语义 Probe；禁止直接全量重训。
- C01/C02/C06：围绕正 lead time、校准或跨条件泛化做共享 causal feature adapter 的 Probe；传统 min_z2 是任务 comparator，AUROC ceiling 不得包装成 ML 空间。
- C13：先做与旧 pilot-Jones/已有方法的机制去重和合法信息合同 Probe；撞车或信息优势不存在就退出。
- C12：只做 coded-output/LLR evaluator 的 capability/readiness Probe；若是基础设施工程，记录 blocker 后轮转，不为它停住全 campaign。

每个 Probe 只回答一个二元或三态前置问题，并预先写退出条件。默认产物：`probes/<probe-id>/record.yaml`；只有确需复现的中间数据放该 Probe 的 `artifacts/`。

如果首轮没有任何可升级项，从 C01–C13 和历史 Candidate Universe 中按机制证据、论文价值、共享能力杠杆和实现成本刷新下一组，不因全部首轮负面就停止。

### 2.3 Phase 2：批量 Scout

只有 Probe PASS 且问题经过充分传统 comparator 后才进入 Scout。将能共享输入合同、baseline、cells/seeds 和 evaluator 的候选放入同一小批，但不同输出任务保留各自 task comparator。要求：

- validation/test 隔离；候选有相当调参机会，不强制同超参数；
- paired seeds/shared realizations；
- 主指标、MDE/退出条件、claim ceiling 预先冻结；
- 检测/估计指标与最终系统收益分开；
- 先跑可辨识的小 Atlas，发现条件性优势后再扩域，而不是只测一个容易切片或一开始铺满所有轴；
- 发现 bug、泄漏、常数解、非因果或 comparator 不公平时，结果降为 DIAGNOSTIC，修正前不得升级。

Scout 通过后可自动继续相邻可验证切片；局部失败则更新 Portfolio 并换分支。不要每批等待用户确认。

### 2.4 Phase 3：Deep Evidence 与论文收获

只对稳定、机制清楚、能支撑毕业论文叙事的少数信号升级。此时才补完整 provenance、统计、独立 critic/verifier、receipt 和 scope certificate。每个工作单元都做 harvest assessment，但只有具备耐久价值时新增条目；否则记录 `no_durable_harvest_reason`。

持续维护至少三类潜在论文材料：方法正信号、机制/边界/负面结果、可复用评估或基础设施资产。次级结果不得丢失，也不得冒充主贡献。

### 2.5 执行方式

- 主对话负责组合、范围和科学判断；全文精读、web 检索、批量文献筛查、MVE 执行和独立审查按仓库规则委托子 agent。
- 同一时间最多三个子 agent；后批利用前批结果修正，不一次派完。
- 运行仿真前读取 `sim-preflight`、`thesis-lessons.md`、`code-quality.md` 和相关模板；方法论/创新判断读取 science topic decisions 与 thesis lessons。
- 发现连续两轮同机制无新信息或改善不足时截断该机制，回到 Portfolio；不要钻牛角尖。

## 3. 已知陷阱

- “只有一个 paired input”却生成 5 份治理文件；这应保持 Probe。
- receipt/hash 全绿但目标是常数最优；必须先过语义 smoke。
- 旧 handoff 比 amendment 更新或更显眼；显式 lineage 优先，mtime 无效。
- 用 system anchor 替代 detection/control/correction 的 task comparator；禁止。
- detector AUROC 高就声称 PI-SER 改善；禁止。
- 同一个 blocker 反复补接口而不轮转；禁止。
- 为了看起来有产出给每个 Probe 强造 harvest；禁止。
- 为“完整”固定候选数、科学槽位或复杂 scheduler；禁止。

## 4. 验收

- [ ] current view 能在五个入口内恢复，且不复述被 D016 撤回的结论。
- [ ] 至少形成多个机制分支的实际推进；没有因单个 blocker 停止。
- [ ] 每个扩算力项都有 semantic smoke 证据，integrity 与 scientific validity 分开。
- [ ] Probe 记录轻量；只有真正升级项承担 Scout/Deep Evidence 成本。
- [ ] baseline/task comparator、公平调参、公式/符号/参数来源可核验。
- [ ] 正面、负面、诊断性、阻断和次级论文素材均进入 current harvest assessment。
- [ ] protected history 未改，legacy B004 不存在，Scout 数字未自动写论文。
- [ ] 独立 verifier 审查 Scout/Deep Evidence；普通 Probe 不强制独立 verifier。
- [ ] 最终用普通中文说明：真正跑了什么、哪些可写论文、哪些一般、哪些死路、下一轮为什么这样排。
- [ ] 工作树收尾时一次提交，未 push。

## 附：产出回传位置

- 科学 current view 与运行产物：`projects/thesis-fso/direction-lab/`
- 科学战略/重大失败/交接：`.sessions/2026-07-20-direction-lab-science-scout/`
- 不要为普通 Probe 新建 session note。
