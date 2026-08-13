# Task Brief: 从历史资产恢复硕士级 reference-extension 方法候选

> 来源: S020 | 产出位置: `projects/thesis-fso/direction-lab/harvest/`
> 日期: 2026-08-13
> 唯一文档: 执行方以本 T013 为任务合同，可读取仓库内历史材料与源码

## 0. TL;DR（执行方先读）

你在 `research-protocol` 的独立 Codex worktree。项目已有大量被关闭、降级或未晋级的接收机方法资产。

**你的任务**：不用“必须首次、必须击败最新最强方法”的标准，重新从历史材料中恢复真正满足硕士论文要求的完整 reference-extension 方法候选。

**产出**：候选报告、机器映射和独立 verifier 报告各一份；只生成方法卡，不运行实验。

**最高纪律**：

1. 经典 baseline 正确 + 目标场景确有可验证增益 + 完整输入—动作—输出链，即可进入候选；不要求击败所有近期强方法。
2. 强邻居、full-general 方法、近期 baseline 不完全 task-matched 只限制 claim ceiling，不自动 Kill。
3. exact collision 必须严格满足同任务、同条件、同可用信息、同动作且没有独立 delta；否则不得冒充 collision。
4. truth leakage、scale/metric/cost artifact、物理前提不存在、problem absent、明确 scientific/headroom gate FAIL 仍不可复活。
5. select-before-execute 只是 CCISP 内部实现资产，不得作为独立方法候选。
6. 不检索、不下载、不实现、不仿真、不修改 Skill/common/params/正式论文。
7. 完成后使用 task/thread 工具把五项回执自动发送给父任务 `019fccc3-f9f2-7b52-938f-b2b1dda09b10`，不要要求用户中转。

## 1. 背景

项目长期流程把期刊级 novelty closure 当成候选入口门，导致“存在更强邻居”“full-general 方法能力更大”“不是首次”“近期 baseline 不够贴合”等情况被过早关闭。硕士学位论文允许更务实的 reference extension：选一个公认、实现正确的经典 baseline，在本项目目标场景下做完整且有收益的适配，并诚实限制声称范围。

Ch3 的 CCISP 主方法已经确定。本任务要为 Ch4/独立 Ch5 找候选，而不是重审 CCISP，也不是把 supporting asset 硬说成方法。

优先读取：

- `projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.md`
- `projects/thesis-fso/direction-lab/harvest/historical-assets-thesis-grade-remap.yaml`
- `projects/thesis-fso/direction-lab/harvest/internal-method-kernel-inventory.yaml`
- `projects/thesis-fso/direction-lab/harvest/baseline-first-method-batch-001.md`
- `projects/thesis-fso/direction-lab/harvest/ch4-concept-method-batch-001.md`
- `projects/thesis-fso/direction-lab/harvest/ch5-concept-method-batch-001.md`
- 各方向 topic-index / decisions / verifications / handoff 与必要原始结果
- `thesis-lessons.md` 速查表和最近三条

## 2. 任务详情

### 2.1 重新建立候选池

覆盖下列来源，不得只看 T012 的 A/B：

- 因“场景迁移不够新”关闭的候选；
- 因存在强邻居、full-general 方法或 recent baseline debt 降级的候选；
- 已有局部正信号但未形成方法卡的候选；
- 只差一次 bounded confirmation 的候选；
- testbed/infrastructure blocked 但方法身份完整的候选；
- 过去只作为 component 记录、但可能与另一个动作组成完整链的候选。

不要按历史标签投票。沿实际证据重建每个方法身份：

`经典 reference M → 目标场景 C 中的具体不足 → 所提适配动作 A → deployable output`。

### 2.2 每个候选的强制方法卡

每张卡必须包含：

1. 方法名（能作为章节小节标题）；
2. 经典 reference/baseline 及其正确实现证据；
3. 目标场景与 baseline 的具体失配；
4. receiver-visible 输入；
5. 完整动作链和输出；
6. 已有增益证据，或唯一一次 bounded check；
7. 最强廉价替代；
8. 强邻居及仅由其限制的 claim ceiling；
9. 主对比图；
10. 至少两个消融；
11. PASS/FAIL 后的章节落位；
12. 与 Ch3 CCISP 的独立性；
13. 预计最小验证成本。

### 2.3 分类与排序

只使用四类：

- `HISTORICAL_METHOD_CANDIDATE`：已有完整动作与足够证据，可以直接规划章节材料；
- `ONE_BOUNDED_CHECK_AWAY`：动作完整，只差一次可裁决确认；
- `COMPONENT_ONLY`：不能独立成方法，但可嵌入其他候选；
- `SCIENTIFICALLY_INVALID`：有明确科学无效证据。

目标产出 4–8 张前两类方法卡；若诚实复核后不足 4 张，报告实际数量，不凑数。最后给出排名，不自行授权任何实验。

### 2.4 产出格式

只新增或修改以下三个文件：

1. `projects/thesis-fso/direction-lab/harvest/historical-reference-extension-candidate-recovery.md`
2. `projects/thesis-fso/direction-lab/harvest/historical-reference-extension-candidate-recovery.yaml`
3. `projects/thesis-fso/direction-lab/harvest/historical-reference-extension-candidate-recovery-verifier.md`

主报告至少包含：标准纠偏、全候选总表、逐卡方法身份、被排除项边界、Top 3 排名、与 Ch3/Ch4/Ch5 映射、主控下一步选择输入。

YAML 每个候选必须有稳定 ID、class、baseline、condition、action、output、evidence、cheap_alternative、strong_neighbor、claim_ceiling、bounded_check、chapter_fit、cost。

## 3. 已知陷阱

- 不要把“更强方法存在”写成候选失败；只要本文不声称全面最佳，比较经典 baseline 是合法的。
- 不要把“换场景”本身当方法；必须说明场景使 baseline 哪个环节失配，以及新增了什么 deployable action。
- 不要把 P02 全局 ref retune、G1 scale correction、P09 假 early-stop 等改名复活。
- 不要把软件调用减少等同 FPGA 资源减少；没有 RTL/HLS/PPA 就不能写硬件结论。
- 不要预选 P01；它和其他候选同表比较。
- 不要为了达到数量把两个 supporting components 机械拼接；组合后必须形成一个统一决策变量和输出。

## 4. 验收

- [ ] 所有历史候选有 evidence path，分类计数与 YAML 一致。
- [ ] 每个前两类候选具备完整 input→action→output，不是参数改名。
- [ ] 强邻居与 exact collision 已分开。
- [ ] 所有 scientifically invalid 项没有被复活。
- [ ] select-before-execute 未作为独立候选。
- [ ] Top 3 各有主图、消融、廉价替代、claim ceiling 和最小验证。
- [ ] fresh-context verifier 给出 P0/P1/P2。
- [ ] 只提交上述三个 allowlist 文件，一次 commit，不 push；不纳入其他 dirty。
- [ ] 五项回执已自动发送父任务。

## 附：合法终态

- `HISTORICAL_CANDIDATES_RECOVERED`
- `NO_HISTORICAL_METHOD_CANDIDATE`
- `HISTORICAL_EVIDENCE_CONFLICT`
